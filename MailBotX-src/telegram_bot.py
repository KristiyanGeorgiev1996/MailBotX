import requests
import time
import json
import config


def send_message(chat_id, message):

    url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }

    requests.post(url, data=payload)


def set_status(value):

    with open("bot_status.json", "w") as f:
        json.dump({"running": value}, f)


def get_status():

    try:
        with open("bot_status.json") as f:
            data = json.load(f)
            return data["running"]
    except:
        return True


def get_stats():

    try:
        with open("stats.json") as f:
            return json.load(f)
    except:
        return {"processed": 0, "sent": 0, "ignored": 0}


def get_last_email():

    try:
        with open("last_email.json") as f:
            return json.load(f)
    except:
        return None


def handle_command(command, chat_id):

    if command == "/stop":

        set_status(False)
        send_message(chat_id, "⏸ Email notifications stopped")

    elif command == "/start":

        set_status(True)
        send_message(chat_id, "▶ Email notifications resumed")

    elif command == "/status":

        status = "ON" if get_status() else "OFF"

        message = f"""
📬 <b>Email notifier status</b>

Notifications: <b>{status}</b>
Check interval: {config.CHECK_INTERVAL // 60} minutes
"""

        send_message(chat_id, message)

    elif command == "/test":

        send_message(chat_id, "✅ Bot is working correctly")

    elif command == "/menu":

        message = """
📬 <b>Email Bot Menu</b>

/start – start notifications
/stop – stop notifications
/status – bot status
/test – test bot
/last – last email received
/stats – bot statistics
"""

        send_message(chat_id, message)

    elif command == "/last":

        email_data = get_last_email()

        if not email_data:
            send_message(chat_id, "No emails processed yet.")
            return

        message = f"""
📧 <b>Last email</b>

👤 From:
{email_data["from"]}

📌 Subject:
{email_data["subject"]}

⏰ Received:
{email_data["time"]}
"""

        send_message(chat_id, message)

    elif command == "/stats":

        stats = get_stats()

        message = f"""
📊 <b>Bot statistics</b>

Emails processed: {stats["processed"]}
Emails sent to Telegram: {stats["sent"]}
Ignored emails: {stats["ignored"]}
"""

        send_message(chat_id, message)


def run_bot():

    last_update_id = None

    while True:

        url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/getUpdates"

        try:

            r = requests.get(url)
            data = r.json()

            if not data["ok"]:
                continue

            for result in data["result"]:

                update_id = result["update_id"]

                if last_update_id and update_id <= last_update_id:
                    continue

                message = result.get("message")

                if message:

                    chat_id = message["chat"]["id"]
                    text = message.get("text", "")

                    handle_command(text.strip(), chat_id)

                last_update_id = update_id

        except Exception as e:

            print("Telegram bot error:", e)

        time.sleep(2)
