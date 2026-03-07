# Installation

1. **Clone the repository**
```bash
git clone https://github.com/username/MailBotX.git
cd MailBotX
```

2. **Create a virtual environment**
```
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

3. **Install dependencies**
```
pip install -r requirements.txt
```

4. **Set up your .env** (see env.md)
```

### **env.md**

```markdown
# Environment Variables (.env)

Create a `.env` file in the root folder:


- `BOT_TOKEN` – Your Telegram bot token  
- `CHAT_ID` – Your personal chat ID  
- `EMAIL_ADDRESS` – Gmail account for notifications  
- `EMAIL_PASSWORD` – Gmail App Password (required if 2FA is enabled)

> Never upload `.env` to GitHub.
```
