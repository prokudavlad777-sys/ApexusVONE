# APEXUS 1V
### Advanced AI Desktop Assistant

**Version:** 1.0  
**Project Status:** Initial Development  
**Language:** Ukrainian Interface  
**Platform:** Windows  
**Technology:** Python, PySide6, DeepSeek API

---

## 1. Overview

**APEXUS 1V** is a desktop artificial intelligence application designed to provide users with a modern, accessible, and efficient environment for interacting with AI models.

The project focuses on combining a professional graphical user interface, reliable API communication, local conversation history, configurable application settings, and a modular software architecture.

APEXUS 1V is designed to run as a native desktop application on Windows. It can be launched directly from the terminal or through a dedicated Windows batch file.

The application uses the DeepSeek API to generate AI responses. Its architecture is designed to support future improvements, including additional AI providers, conversation management features, customizable interface settings, and more advanced AI capabilities.

The primary objective is to create a functional, maintainable, and extensible AI assistant rather than a static interface prototype.

## 2. Project Objectives

The main objectives of APEXUS 1V are:

- Provide a clean and professional desktop AI interface.
- Integrate an external AI model through a reliable API connection.
- Display AI responses in a readable conversation format.
- Preserve conversation history locally.
- Support convenient application startup through the Windows terminal.
- Keep the interface responsive during API requests.
- Protect API credentials by using environment variables.
- Organize the codebase into reusable and maintainable modules.
- Establish a foundation for future AI features and integrations.

## 3. Core Features

### 3.1. Modern Graphical Interface

APEXUS 1V features a dark, modern interface designed for clarity and usability.

The interface should include:

- A large, bold, bright blue **APEXUS 1V** title.
- A dark graphite and black background.
- Blue and purple accent colors.
- Rounded buttons and input fields.
- Clear typography and consistent spacing.
- Subtle animations and visual transitions.
- A dedicated conversation area.
- A sidebar for navigation and chat history.
- A settings panel for application configuration.

The interface must remain visually consistent across the application.

### 3.2. AI Conversation System

The conversation system provides the primary interaction between the user and the AI model.

Expected functionality includes:

- Sending text messages to the AI model.
- Receiving responses through the configured API.
- Displaying user messages and AI responses separately.
- Supporting Enter to send messages.
- Preventing empty messages from being submitted.
- Displaying a loading indicator while a response is being generated.
- Handling failed requests without crashing the application.
- Preserving the conversation context when supported by the selected model and API configuration.

The application must not generate fake AI responses when the API is unavailable.

### 3.3. DeepSeek API Integration

APEXUS 1V uses the DeepSeek API as its initial AI provider.

The integration must support:

- Secure API key configuration.
- Sending requests to the configured model.
- Receiving and displaying API responses.
- Handling network errors and timeouts.
- Reporting authentication failures.
- Handling rate limits and service errors.
- Managing unexpected or invalid API responses.
- Keeping API communication separate from interface code.

API credentials must never be embedded directly into the source code or committed to a public repository.

### 3.4. Local Conversation History

The application should support local conversation storage so that users can access previous sessions.

Planned capabilities include:

- Creating new conversations.
- Saving messages locally.
- Displaying previous conversations in the sidebar.
- Opening an existing conversation.
- Preserving message order.
- Assigning readable conversation titles.
- Handling missing or corrupted history files gracefully.

A lightweight local storage solution, such as SQLite or JSON, may be used depending on the implementation requirements.

### 3.5. Application Settings

The settings panel should provide access to supported configuration options.

Possible settings include:

- Interface preferences.
- Conversation behavior.
- Selected AI model.
- Local history management.
- Application startup preferences.

Only settings that are actually implemented should be displayed as functional controls.

### 3.6. Terminal Startup

APEXUS 1V must support direct startup through the Windows terminal.

The primary startup command is:

```bash
python main.py
```

A secondary startup method must be available through:

```bat
run.bat
```

The terminal should display useful startup messages, diagnostic information, and readable error descriptions.

The application must not silently close when a startup error occurs.

## 4. Technology Stack

The project uses the following technologies.

| Technology | Purpose |
|---|---|
| Python 3.12+ | Primary programming language |
| PySide6 | Desktop graphical interface |
| DeepSeek API | AI response generation |
| SQLite or JSON | Local conversation storage |
| Python threading or asynchronous operations | Non-blocking API communication |
| pip | Dependency installation |
| Windows Batch | Convenient application startup |

The implementation should minimize unnecessary dependencies and use stable, compatible library versions.

## 5. Project Structure

The recommended project structure is:

```text
APEXUS-1V/
├── main.py
├── interface.py
├── chat.py
├── settings.py
├── requirements.txt
├── run.bat
├── README.md
├── .gitignore
├── .env.example
├── assets/
│   ├── icons/
│   └── images/
├── data/
│   └── conversations/
└── logs/
```

### File Responsibilities

**`main.py`**

Initializes the application, configures startup behavior, creates the main window, and starts the Qt event loop.

**`interface.py`**

Contains the graphical interface, including the main window, sidebar, message area, input field, buttons, and visual components.

**`chat.py`**

Handles conversation logic, API communication, request processing, and response management.

**`settings.py`**

Manages application configuration and supported user preferences.

**`requirements.txt`**

Lists the Python packages required to install and run the application.

**`run.bat`**

Provides a convenient Windows startup method and displays useful error information.

**`README.md`**

Contains project documentation, installation instructions, configuration details, and troubleshooting guidance.

**`.env.example`**

Provides an example of the required environment variable configuration without containing a real API key.

**`.gitignore`**

Prevents sensitive credentials, temporary files, logs, and other unnecessary files from being committed to version control.

## 6. System Requirements

### Minimum Requirements

- Windows 10 or a compatible newer Windows release.
- Python 3.12 or a compatible supported version.
- Internet access for cloud-based AI requests.
- An active DeepSeek API key.
- Sufficient disk space for Python and project dependencies.

### Recommended Requirements

- Windows 11.
- A current stable Python installation.
- A reliable internet connection.
- A terminal capable of displaying Unicode text.
- An editor such as Visual Studio Code for development and maintenance.

A dedicated GPU is not required for API-based inference because AI processing is performed by the remote provider.

## 7. Installation Guide

### Step 1: Install Python

Install a compatible Python version from the official website:

https://www.python.org/downloads/

During installation, enable the option to add Python to the system PATH when available.

Verify the installation:

```bash
python --version
```

Also verify that pip is available:

```bash
python -m pip --version
```

### Step 2: Open the Project Directory

Open Windows Terminal or Command Prompt.

Navigate to the directory containing the APEXUS 1V project:

```bash
cd path\to\APEXUS-1V
```

Replace the example path with the actual project directory.

### Step 3: Create a Virtual Environment

A virtual environment helps isolate the application's dependencies from other Python projects.

Create the environment:

```bash
python -m venv .venv
```

Activate it in Command Prompt:

```bat
.venv\Scripts\activate.bat
```

If using PowerShell, run:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 4: Install Dependencies

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

Wait until installation completes. If an error occurs, inspect the terminal output and verify that the Python version is compatible with the listed dependencies.

### Step 5: Configure the API Key

Obtain an API key through the official DeepSeek platform:

https://platform.deepseek.com/

Configure the `DEEPSEEK_API_KEY` environment variable.

For the current Command Prompt session:

```bat
set DEEPSEEK_API_KEY=YOUR_API_KEY
```

Replace `YOUR_API_KEY` with the actual credential. Do not include the example placeholder as a real key.

For persistent configuration, use Windows environment variable settings or a properly configured local `.env` file if the application explicitly supports it.

Never publish API keys in source code, screenshots, public repositories, or shared configuration files.

### Step 6: Launch the Application

Run:

```bash
python main.py
```

Alternatively, launch:

```bat
run.bat
```

The application should initialize, display its graphical interface, and report any startup problems through the terminal.

## 8. API Configuration

APEXUS 1V must read its API credentials from the environment rather than from hardcoded strings.

Example Python configuration:

```python
import os

API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not API_KEY:
    print("Error: DEEPSEEK_API_KEY is not configured.")
```

This example demonstrates the credential check. The complete application must integrate it with its own error handling and user interface.

The selected model identifier, API endpoint, and request parameters must match the current official DeepSeek API documentation.

API availability, model identifiers, pricing, rate limits, and supported parameters may change over time. These values must not be assumed to remain constant.

## 9. User Interface Guidelines

The interface is a central part of the APEXUS 1V identity.

### Branding

The primary title must read:

**APEXUS 1V**

It must appear in a large, bold, bright blue font and remain clearly visible against the dark background.

The title must be implemented as a real interface element rather than embedded in a static background image.

### Layout

The main window should be divided into three functional areas:

1. **Navigation Sidebar:** Provides access to new chats and conversation history.
2. **Conversation Area:** Displays messages and AI responses.
3. **Message Input Area:** Allows users to enter and send messages.

Settings may be presented in a separate page, dialog, or panel.

### Visual Feedback

The interface should communicate application state clearly.

Examples include:

- A loading indicator during response generation.
- Disabled send controls while a request is being processed, when appropriate.
- Informative error messages after failed requests.
- Confirmation when a conversation is created or saved.
- Clear visual separation between user messages and AI responses.

Animations must remain lightweight and must not interfere with usability.

## 10. Performance and Reliability

The application must remain responsive during network operations.

API requests should run through a worker thread or an appropriate asynchronous mechanism. Long-running operations must not block the Qt graphical interface.

The application should also:

- Handle connection failures.
- Apply reasonable request timeouts.
- Avoid sending duplicate requests accidentally.
- Validate user input.
- Recover from recoverable API errors.
- Preserve conversation data when possible.
- Avoid unnecessary background processes.
- Release resources when the application closes.

Error handling must provide enough information to diagnose problems without exposing API credentials or other secrets.

## 11. Security and Privacy

Security is an important requirement for any application that communicates with external AI services.

APEXUS 1V should follow these principles:

- Store API credentials outside the source code.
- Exclude local secrets from version control.
- Avoid printing credentials in logs.
- Validate external API responses.
- Avoid executing AI-generated code automatically.
- Avoid exposing local files to the model without explicit application functionality and user authorization.
- Clearly indicate when messages are transmitted to an external service.
- Store local conversations only as required by the application's features.
- Provide an appropriate way to remove locally stored conversation history.

Users should understand that messages sent to an external AI provider are processed according to that provider's applicable policies and terms.

## 12. Testing and Quality Assurance

Before a release, test the following areas.

### Startup Tests

- The application starts through `python main.py`.
- The application starts through `run.bat`.
- Missing dependencies produce readable errors.
- Invalid configuration is handled correctly.

### Interface Tests

- The main window opens successfully.
- The APEXUS 1V title is large and blue.
- Navigation controls work.
- Messages appear in the correct order.
- Enter and the send button behave as expected.
- The interface remains responsive.

### API Tests

- A valid API key allows requests to be submitted.
- Missing credentials produce a clear error.
- Network failures are handled gracefully.
- Invalid API responses do not crash the application.
- The application displays actual API responses rather than fabricated content.

### History Tests

- Conversations can be created.
- Messages are saved correctly.
- Existing conversations can be reopened.
- Invalid or missing history data is handled safely.

### Release Verification

Before publishing a release, verify that:

- All required files are present.
- Dependencies are documented.
- No API credentials are included.
- The startup instructions are accurate.
- The application does not depend on undocumented local files.
- All advertised features are implemented and tested.

## 13. Troubleshooting

### Python Is Not Recognized

If Windows reports that Python cannot be found, install Python or correct the system PATH configuration.

Verify availability using:

```bash
python --version
```

If necessary, try:

```bash
py --version
```

### Required Module Is Missing

Install the dependencies from the project directory:

```bash
python -m pip install -r requirements.txt
```

Confirm that the virtual environment is activated if one is being used.

### API Key Is Missing

Verify that the environment variable is configured:

```bat
echo %DEEPSEEK_API_KEY%
```

This command may display the key in the terminal. Do not share screenshots or terminal logs containing the credential.

If the variable is empty, configure it and restart the application from the same terminal session.

### API Requests Fail

Check the following:

- Internet connectivity.
- API key validity.
- Current provider availability.
- Model identifier and endpoint configuration.
- API usage limits and account status.
- Error messages returned by the service.

### The Interface Freezes

Check that API requests and other time-consuming operations are not running on the main GUI thread.

### The Application Closes Unexpectedly

Launch the application directly from the terminal:

```bash
python main.py
```

Read the traceback and identify the relevant file and line number before attempting a fix.

## 14. Development Roadmap

The following roadmap describes potential future development. These features are planned possibilities and must not be considered implemented until verified.

### Version 1.0: Core Application

- Modern PySide6 interface.
- Large blue APEXUS 1V branding.
- DeepSeek API integration.
- Basic chat functionality.
- Local conversation history.
- Windows terminal startup.
- Error handling and configuration management.

### Version 1.1: Improved Conversation Management

- Conversation renaming.
- Improved history navigation.
- Search through saved conversations.
- Message copying.
- Improved response formatting.
- Additional interface preferences.

### Version 1.2: Expanded AI Configuration

- Configurable model selection where supported.
- Adjustable generation parameters where supported.
- Improved API diagnostics.
- More detailed request status information.
- Better handling of long conversations.

### Version 2.0: Multi-Model Architecture

- Support for additional AI providers.
- A common interface for model integrations.
- Configurable provider selection.
- Model comparison tools.
- Optional review of responses by a second model.
- Improved context and request management.

### Future Development

Additional possibilities include document analysis, file import, custom prompt profiles, exportable conversations, plugin support, and optional local AI integrations.

Each feature should be introduced only when its implementation, security implications, dependencies, and user experience have been evaluated.

## 15. Contribution Guidelines

Contributions should improve reliability, usability, maintainability, or functionality.

Recommended practices include:

- Keep modules focused on clearly defined responsibilities.
- Use descriptive function and variable names.
- Follow consistent Python formatting conventions.
- Document non-obvious behavior.
- Avoid unnecessary dependencies.
- Test changes before submitting them.
- Never commit API credentials.
- Update the README when installation steps or user-facing behavior change.

Bug reports should include the operating system, Python version, steps to reproduce the issue, and relevant error messages with sensitive information removed.

## 16. Versioning

APEXUS 1V uses a versioning approach intended to distinguish major changes, feature additions, and fixes.

- **Major releases** may introduce significant architectural or compatibility changes.
- **Minor releases** may add functionality while preserving the general application structure.
- **Patch releases** may address defects, reliability issues, and small improvements.

The version number must reflect the actual state of the released software.

## 17. License

A license has not been specified for this project.

Before distributing APEXUS 1V publicly, select an appropriate license and document any applicable third-party dependency licenses.

Do not claim that the software is open source or grant permissions that have not been explicitly established.

## 18. Disclaimer

APEXUS 1V is an independent software project that integrates with an external AI service.

It is not an official DeepSeek product and should not imply endorsement by DeepSeek or any other AI provider.

AI responses may contain inaccurate or incomplete information. Users should independently verify important information before relying on it.

The availability and behavior of external services are subject to the applicable provider's terms, policies, and technical limitations.

## 19. Project Philosophy

APEXUS 1V is built around three core principles:

**Functionality:** Every advertised control should perform its intended task.

**Reliability:** Errors should be handled clearly, and the application should remain stable under normal operating conditions.

**Extensibility:** The architecture should allow new capabilities to be introduced without unnecessarily rewriting the entire application.

The long-term goal is to develop APEXUS 1V into a capable, configurable, and dependable AI desktop environment.

---

**APEXUS 1V**  
*Intelligence. Precision. Control.*
