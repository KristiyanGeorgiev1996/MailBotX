# 📧 Comprehensive Automated Tests for Telegram & Gmail Bot

This file contains a full suite of automated tests for a Telegram bot integrated with Gmail. The tests are divided into five main categories, covering functional, regression, negative, unit, and API contract tests. They ensure the bot works reliably, processes emails correctly, and sends Telegram messages as expected. Screenshots of all successful (green) test runs are located in the `screenshots/` folder.

---

## 🗂 Folder Structure
```
/telegram-gmail-bot-tests
│
├── tests/
│   ├── test_api_contract.py
│   ├── test_e2e.py
│   ├── test_negative.py
│   ├── test_regression.py
│   ├── test_unit.py
│   └── screenshots/
│       ├── Screenshot-1-Unit-Tests.png
│       ├── Screenshot-2-Test-API-Contract.png
│       ├── Screenshot-3-Test-Negative.png
│       ├── Screenshot-4-Test-Regression.png
│       └── Screenshot-5-Test-E2E.png
│
└── README.md
```

---

## 🗂 Test File Overview

### 1️⃣ `test_api_contract.py`

**Purpose:**  
Validates that the Telegram and Gmail integration follows the expected API contract. These tests ensure that payloads sent to Telegram and email structures conform to specifications.

**Key Tests:**
- **Message content combinations:** text, empty messages, long messages, HTML tags, emojis, mixed content.
- **Inline keyboards:** single button, multiple buttons, empty keyboard.
- **Payload validation:** ensures `text`, `parse_mode`, and `inline_keyboard` are correctly formed.
- **Exception handling:** simulates `requests.post` failure and ensures the function handles exceptions gracefully.

**Screenshot Tag:**  
`![API Contract Tests](screenshots/test_api_contract.png)`

---

### 2️⃣ `test_e2e.py`

**Purpose:**  
End-to-end tests of the bot, validating the full flow from commands to email processing and Telegram message delivery.

**Key Tests:**
- **Bot commands:** `/start`, `/stop`, `/test`, `/status`, `/last`, `/stats`, `/menu`.
- **Email processing edge cases:**  
  - HTML content  
  - Empty subjects  
  - Long email bodies  
  - Emojis  
  - Multipart emails  
- **Integration of commands and emails:** verifies messages handle all edge cases correctly.
- **Negative scenarios in E2E:**  
  - Invalid commands do nothing  
  - Bot OFF prevents message sending  
  - API exceptions are handled safely

**Screenshot Tag:**  
`![E2E Tests](screenshots/test_e2e.png)`

---

### 3️⃣ `test_negative.py`

**Purpose:**  
Negative and edge-case tests to ensure the bot handles unexpected scenarios gracefully.

**Key Tests:**
- **Invalid commands:** `/invalid` or unknown commands do not trigger actions.
- **Bot OFF behavior:** ensures no messages are sent when the bot is disabled.
- **IMAP exceptions:** simulates failures in login, select, fetch, logout.
- **Telegram API exceptions:** ensures `send_telegram_message` handles exceptions without crashing.

**Screenshot Tag:**  
`![Negative Tests](screenshots/test_negative.png)`

---

### 4️⃣ `test_regression.py`

**Purpose:**  
Regression tests for critical functions and helper methods to ensure that code changes do not break existing functionality.

**Key Tests:**
- **update_stats:** checks existing and new files, combinations of `processed`, `sent`, `ignored`, and large numbers (millions+).
- **save_last_email:** validates saving the last email with `from`, `subject`, and `time`.
- **bot_is_running:** verifies behavior with existing or missing status file.
- **Telegram bot helper functions:**  
  - `get_status()`  
  - `get_last_email()`  
  - `get_stats()`  
  - `set_status(True/False)`

**Screenshot Tag:**  
`![Regression Tests](screenshots/test_regression.png)`

---

### 5️⃣ `test_unit.py`

**Purpose:**  
Unit tests for individual functions in the bot and Gmail integration, using dummy files and fixed time to test logic independently of external resources.

**Key Tests:**
- **bot_is_running:** with existing and missing files.
- **update_stats:** handles new and existing files, correctly accumulates statistics.
- **save_last_email:** validates saving with mocked `datetime.now()`.
- **send_telegram_message:** checks payload formation and exception handling.
- **Telegram bot helpers:** `get_status`, `get_last_email`, `get_stats`, `set_status`.
- **handle_command:** tests all valid commands (`/start`, `/stop`, `/test`, etc.) and unknown commands.

**Screenshot Tag:**  
`![Unit Tests](screenshots/test_unit.png)`

---
