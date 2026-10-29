"""Налаштування APEXUS 1V та шляхи до локальних даних."""
from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, fields
from pathlib import Path

APP_NAME = "APEXUS 1V"

MODELS = {
    "deepseek-chat": "DeepSeek Chat (швидка)",
    "deepseek-reasoner": "DeepSeek Reasoner (міркуюча)",
}

DEFAULT_SYSTEM_PROMPT = (
    "Ти — APEXUS, дружній та уважний AI-помічник. "
    "Відповідай українською, чітко й по суті, якщо користувач не просить іншу мову."
)


def data_dir() -> Path:
    """Папка для історії чатів і налаштувань (на Windows — %APPDATA%\\APEXUS_AI)."""
    base = os.environ.get("APPDATA") or str(Path.home())
    path = Path(base) / "APEXUS_AI"
    path.mkdir(parents=True, exist_ok=True)
    return path


def atomic_write_json(path: Path, data) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)


@dataclass
class Settings:
    model: str = "deepseek-chat"
    temperature: float = 0.7
    max_tokens: int = 2048
    system_prompt: str = DEFAULT_SYSTEM_PROMPT
    api_key: str = ""  # необов'язково; пріоритет має змінна середовища DEEPSEEK_API_KEY
    font_size: int = 15
    animations: bool = True
    api_url: str = "https://api.deepseek.com/chat/completions"

    def get_api_key(self) -> str:
        return os.environ.get("DEEPSEEK_API_KEY", "").strip() or self.api_key.strip()

    @staticmethod
    def _path() -> Path:
        return data_dir() / "settings.json"

    @classmethod
    def load(cls) -> "Settings":
        path = cls._path()
        if not path.exists():
            return cls()
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            known = {f.name for f in fields(cls)}
            return cls(**{k: v for k, v in raw.items() if k in known})
        except (OSError, ValueError, TypeError):
            return cls()

    def save(self) -> None:
        try:
            atomic_write_json(self._path(), asdict(self))
        except OSError as exc:
            print(f"[APEXUS 1V] Не вдалося зберегти налаштування: {exc}")
