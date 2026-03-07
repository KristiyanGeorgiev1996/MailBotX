# 📬 MailBotX

![Python](https://img.shields.io/badge/Python-3.11-blue) ![Telegram](https://img.shields.io/badge/Telegram-Bot-green)

**Author:** [KristiyanGeorgiev1996 - Chris]  
**License:** MIT License (MIT)  

---

## 📝 Description

This is a **personal project** created to automatically notify about new Gmail emails directly in Telegram.  

The bot checks the mailbox every 10 minutes, sends new messages **nicely formatted** with preview and timestamp, and supports management via Telegram commands.  

💡 This project is intended for personal use and learning. Licensed under MIT – it can be used freely, but the authorship remains with me.

---

## 🚀 Main Features

### 1️⃣ Gmail Checking
- Checks only **unread (UNSEEN) emails**  
- Retrieves **From**, **Subject**, **Preview**, and **Timestamp**  
- Sends messages in Telegram with **HTML formatting** and **inline button**  
- Marks email as **read** after sending ✅  
- Stores the last email (`last_email.json`)  
- Updates statistics (`stats.json`)  

---

### 2️⃣ Telegram Bot 🤖

**Supported commands:**

| Command       | Description |
|---------------|-------------|
| `/start`      | ▶ Enables email notifications |
| `/stop`       | ⏸ Stops email notifications |
| `/status`     | 📬 Shows whether notifications are enabled and the check interval |
| `/test`       | ✅ Sends a test message |
| `/menu`       | 📋 Shows all commands |
| `/last`       | 📨 Shows the last received email |
| `/stats`      | 📊 Shows statistics |

**Example of a received message:**


📬 NEW EMAIL RECEIVED

👤 From:  
Amazon

📌 Subject:  
Your order shipped

⏰ Received:  
14:32

📝 Preview:  
Your order has been shipped and will arrive tomorrow.

**Inline button:**  
📬 [Open Gmail](https://mail.google.com)

---

### 3️⃣ JSON Files 📂

- `bot_status.json` – stores whether the bot is active (`True/False`)  
- `stats.json` – stores statistics about processed emails  
- `last_email.json` – stores the last email for `/last` command  

---

## ⚙️ Project Files

| File | Description |
|------|-------------|
| `main.py` | Starts the Telegram bot and email checking loop |
| `telegram_bot.py` | Handles Telegram commands and messages |
| `gmail_service.py` | Connects to Gmail, checks for new emails, and sends them to Telegram |
| `config.py` | Loads configuration and tokens from `.env` |
| `.env` | Stores BOT_TOKEN, CHAT_ID, EMAIL_ADDRESS, EMAIL_PASSWORD |
| `bot_status.json` | Stores bot status |
| `stats.json` | Stores statistics |
| `last_email.json` | Stores the last email |

---

## 💻 Installation and Running

### 1️⃣ Install Python 🐍

Make sure you have **Python 3.10+** installed  

```bash
python --version
```

### 2️⃣ Clone the Project 📂

```bash
git clone https://github.com/username/TV-Robot.git
cd TV-Robot
```

### 3️⃣ Create Virtual Environment (recommended) 🌱

```bash
python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 4️⃣ Install Dependencies 📦

```bash
pip install -r requirements.txt
```

requirements.txt contains:

```bash
requests
python-dotenv
```

#### 5️⃣ Configure .env 🔐
Create a .env file in the root folder:

```
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
CHAT_ID=YOUR_CHAT_ID
EMAIL_ADDRESS=your.email@gmail.com
EMAIL_PASSWORD=your_app_password
```

⚠️ For Gmail, an App password is required if you have two-factor authentication enabled.

#### 6️⃣ Run the Bot ▶️
```bash
python main.py
```

The bot runs in parallel:

- Telegram bot (listens for commands)  
- Gmail loop (checks new emails every 10 minutes)  

---

## 📜 License & Authorship

This project is personal, developed by [KristiyanGeorgiev1996].  

Licensed under MIT – can be used freely, but always credit the author.  

All tokens and passwords are stored in `.env` and **should not be pushed to GitHub**.

---

## ⚡ Notes

- On Windows, use `python -m pip` instead of just `pip`.  
- GitHub `.gitignore` should include:

```
.env
pycache/
*.pyc
bot_status.json
stats.json
last_email.json
```


- The Telegram bot and Gmail checker run in parallel threads so they do not block each other.
