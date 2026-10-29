"""Логіка чатів: модель даних, локальне сховище та запити до DeepSeek API."""
from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict, dataclass, field

import requests
from PySide6.QtCore import QThread, Signal

from settings import Settings, atomic_write_json, data_dir

DEFAULT_TITLE = "Новий чат"
MAX_HISTORY = 40  # скільки останніх повідомлень відправляти в API


class ApiError(Exception):
    """Помилка, текст якої можна показати користувачу."""


@dataclass
class Message:
    role: str
    content: str
    ts: float = field(default_factory=time.time)


@dataclass
class Chat:
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    title: str = DEFAULT_TITLE
    created: float = field(default_factory=time.time)
    updated: float = field(default_factory=time.time)
    messages: list[Message] = field(default_factory=list)


class ChatStore:
    """Локальне збереження історії чатів у JSON."""

    def __init__(self) -> None:
        self.path = data_dir() / "chats.json"
        self.chats: dict[str, Chat] = {}
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            for item in raw.get("chats", []):
                msgs = [
                    Message(m["role"], m["content"], m.get("ts", time.time()))
                    for m in item.get("messages", [])
                    if m.get("role") in ("user", "assistant") and isinstance(m.get("content"), str)
                ]
                if not msgs:
                    continue
                chat = Chat(
                    id=item["id"],
                    title=item.get("title", DEFAULT_TITLE),
                    created=item.get("created", time.time()),
                    updated=item.get("updated", time.time()),
                    messages=msgs,
                )
                self.chats[chat.id] = chat
        except (OSError, ValueError, KeyError, TypeError):
            try:  # зберігаємо пошкоджений файл, щоб нічого не втратити
                self.path.replace(self.path.with_name("chats.corrupt.json"))
            except OSError:
                pass
            self.chats = {}

    def save(self) -> None:
        data = {"chats": [asdict(c) for c in self.chats.values() if c.messages]}
        try:
            atomic_write_json(self.path, data)
        except OSError as exc:
            print(f"[APEXUS 1V] Не вдалося зберегти історію: {exc}")

    def sorted_chats(self) -> list[Chat]:
        return sorted(self.chats.values(), key=lambda c: c.updated, reverse=True)

    def get(self, chat_id: str | None) -> Chat | None:
        return self.chats.get(chat_id) if chat_id else None

    def new_chat(self) -> Chat:
        chat = Chat()
        self.chats[chat.id] = chat
        return chat

    def add_message(self, chat: Chat, role: str, content: str) -> None:
        chat.messages.append(Message(role, content))
        chat.updated = time.time()
        if role == "user" and chat.title == DEFAULT_TITLE:
            title = " ".join(content.split())
            chat.title = (title[:38] + "…") if len(title) > 38 else title
        self.save()

    def rename(self, chat_id: str, title: str) -> None:
        chat = self.get(chat_id)
        if chat and title.strip():
            chat.title = title.strip()[:60]
            self.save()

    def delete(self, chat_id: str) -> None:
        self.chats.pop(chat_id, None)
        self.save()

    def clear_all(self) -> None:
        self.chats.clear()
        self.save()


def request_completion(settings: Settings, history: list[Message]) -> str:
    """Синхронний запит до DeepSeek API. Викликати лише з окремого потоку."""
    key = settings.get_api_key()
    if not key:
        raise ApiError(
            "API-ключ DeepSeek не знайдено. Задайте змінну середовища DEEPSEEK_API_KEY "
            "або введіть ключ у «Налаштуваннях»."
        )

    messages = []
    if settings.system_prompt.strip():
        messages.append({"role": "system", "content": settings.system_prompt.strip()})
    messages += [{"role": m.role, "content": m.content} for m in history[-MAX_HISTORY:]]

    payload = {
        "model": settings.model,
        "messages": messages,
        "temperature": settings.temperature,
        "max_tokens": settings.max_tokens,
        "stream": False,
    }
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}

    try:
        resp = requests.post(settings.api_url, headers=headers, json=payload, timeout=(10, 180))
    except requests.exceptions.Timeout:
        raise ApiError("Час очікування відповіді вичерпано. Спробуйте ще раз.") from None
    except requests.exceptions.ConnectionError:
        raise ApiError("Немає зʼєднання з сервером DeepSeek. Перевірте інтернет.") from None
    except requests.exceptions.RequestException as exc:
        raise ApiError(f"Помилка мережі: {exc}") from None

    if resp.status_code != 200:
        known = {
            400: "Некоректний запит (код 400). Перевірте налаштування моделі.",
            401: "Невірний API-ключ (код 401). Перевірте DEEPSEEK_API_KEY.",
            402: "Недостатньо коштів на рахунку DeepSeek (код 402).",
            422: "Некоректні параметри запиту (код 422).",
            429: "Забагато запитів (код 429). Зачекайте хвилину й повторіть.",
            500: "Помилка на сервері DeepSeek (код 500). Спробуйте пізніше.",
            503: "Сервер DeepSeek перевантажений (код 503). Спробуйте пізніше.",
        }
        detail = ""
        try:
            detail = resp.json().get("error", {}).get("message", "")
        except ValueError:
            pass
        text = known.get(resp.status_code, f"Помилка API (код {resp.status_code}).")
        raise ApiError(f"{text}\n{detail}".strip())

    try:
        text = resp.json()["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError):
        raise ApiError("Сервер повернув відповідь у неочікуваному форматі.") from None

    text = (text or "").strip()
    if not text:
        raise ApiError("Модель повернула порожню відповідь. Спробуйте ще раз.")
    return text


class ChatWorker(QThread):
    """Окремий потік, щоб інтерфейс не зависав під час генерації."""

    succeeded = Signal(str, str)  # chat_id, текст
    failed = Signal(str, str)  # chat_id, повідомлення про помилку

    def __init__(self, chat_id: str, settings: Settings, history: list[Message], parent=None):
        super().__init__(parent)
        self.chat_id = chat_id
        self.settings = settings
        self.history = list(history)

    def run(self) -> None:
        try:
            text = request_completion(self.settings, self.history)
            self.succeeded.emit(self.chat_id, text)
        except ApiError as exc:
            self.failed.emit(self.chat_id, str(exc))
        except Exception as exc:  # непередбачена помилка не повинна ламати застосунок
            self.failed.emit(self.chat_id, f"Непередбачена помилка: {exc}")
