# MailBotX
📬 Telegram Email Notifier - Automatically sends Gmail emails to Telegram with rich formatting and inline buttons. Personal project with MIT license.

![Bot Screenshot](Images/MailBotX-Image.png)

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Telegram](https://img.shields.io/badge/Telegram-Bot-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

MailBotX is a **Telegram bot** that automatically sends **new Gmail emails** as notifications directly to your Telegram chat.  

It’s a personal project, designed for learning and automation purposes.  

---

## 📌 Features

- Sends unread Gmail emails to Telegram
- HTML formatted messages with preview and timestamp
- Inline button linking to Gmail
- Commands: `/start`, `/stop`, `/status`, `/last`, `/stats`, `/test`, `/menu`
- Logs statistics and last email in JSON files
- Checks Gmail every 10 minutes

![Bot Demo](docs/screenshots/bot_demo.gif)

---

## 📁 Project Structure

```text
MailBotX/
├─ main.py                  <- Starts the Telegram bot and Gmail checking loop
├─ telegram_bot.py          <- Handles Telegram commands and messaging
├─ gmail_service.py         <- Connects to Gmail, checks emails, sends notifications
├─ config.py                <- Loads configuration and tokens from .env
├─ .env                     <- Stores BOT_TOKEN, CHAT_ID, EMAIL_ADDRESS, EMAIL_PASSWORD
├─ bot_status.json          <- Stores bot status
├─ stats.json               <- Stores email statistics
├─ last_email.json          <- Stores last email
├─ docs/                    <- Documentation folder
│   ├─ index.md             <- Landing page
│   ├─ installation.md      <- Installation guide
│   ├─ usage.md             <- How to use the bot
│   ├─ env.md               <- .env setup guide
│   ├─ screenshots/         <- Screenshots and GIFs
```
---

## ⚙️ Installation

See full instructions in the [Installation guide](docs/installation.md) in the Docs folder.

---

## 💻 Usage

Check the [Usage guide](docs/usage.md) for commands and instructions to run the bot.

---

## 🔗 Documentation / GitHub Pages

All Markdown files with screenshots and GIFs are available as a landing page:

[MailBotX Docs / GitHub Pages](https://KristiyanGeorgiev1996.github.io/MailBotX/)

---

## ⚠️ Security

- Never upload `.env` with your credentials to GitHub.  
- Use `.env.example` with placeholder values.

---

## 📜 License

MIT License – free to use, but always credit the author.
