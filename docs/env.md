# Environment Variables (.env)

Create a `.env` file in the root folder of the project:

```env
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
CHAT_ID=YOUR_CHAT_ID
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
```

# Environment Variables Description

- **BOT_TOKEN** – Your Telegram bot token  
- **CHAT_ID** – Your personal chat ID (where the bot sends notifications)  
- **EMAIL_ADDRESS** – Gmail account used for sending notifications  
- **EMAIL_PASSWORD** – Gmail App Password (required if 2FA is enabled)  

> ⚠️ Never upload your `.env` file to GitHub.  
> Use `.env.example` with placeholder values for the repository.
