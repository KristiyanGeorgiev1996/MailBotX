import imaplib
import email
import requests
import json
from email.header import decode_header
from datetime import datetime
import html
import config

def bot_is_running():
    try:
        with open("bot_status.json") as f:
            data = json.load(f)
        return data["running"]
    except:
        return True

def update_stats(processed=0, sent=0, ignored=0):
    try:
        with open("stats.json") as f:
            stats = json.load(f)
    except:
        stats = {"processed": 0, "sent": 0, "ignored": 0}
    stats["processed"] += processed
    stats["sent"] += sent
    stats["ignored"] += ignored
    with open("stats.json", "w") as f:
        json.dump(stats, f)

def save_last_email(from_, subject):
    data = {
        "from": from_,
        "subject": subject,
        "time": datetime.now().strftime("%H:%M")
    }
    with open("last_email.json", "w") as f:
        json.dump(data, f)

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": config.CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "reply_markup": json.dumps({
            "inline_keyboard": [
                [{"text": "📬 Open Gmail", "url": "https://mail.google.com"}]
            ]
        })
    }
    try:
        r = requests.post(url, data=payload)
        print("DEBUG: Sending to Telegram...")
        print("DEBUG: Telegram status code:", r.status_code)
        print("DEBUG: Telegram response:", r.text)
    except Exception as e:
        print("Telegram error:", e)

def check_email():
    try:
        mail = imaplib.IMAP4_SSL(config.IMAP_SERVER)
        mail.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)
        mail.select("inbox")
        result, data = mail.search(None, "UNSEEN")
        email_ids = data[0].split()
        print(f"DEBUG: UNSEEN emails found: {len(email_ids)}")
        for num in email_ids:
            print(f"DEBUG: Fetching email ID {num.decode()}")
            update_stats(processed=1)
            result, msg_data = mail.fetch(num, "(RFC822)")
            raw_email = msg_data[0][1]
            message = email.message_from_bytes(raw_email)
            subject, encoding = decode_header(message["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")
            from_ = message.get("From")
            body = ""
            if message.is_multipart():
                for part in message.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            else:
                body = message.get_payload(decode=True).decode(errors="ignore")

            # 🔹 Escape HTML characters to prevent Telegram 400 error
            from_escaped = html.escape(from_)
            subject_escaped = html.escape(subject)
            preview_escaped = html.escape(body[:300])

            timestamp = datetime.now().strftime("%H:%M")
            text = f""" 📬 <b>NEW EMAIL RECEIVED</b>
👤 <b>From:</b> {from_escaped}
📌 <b>Subject:</b> {subject_escaped}
⏰ <b>Received:</b> {timestamp}
📝 <b>Preview:</b> {preview_escaped} """
            print(f"DEBUG: Sending email -> From: {from_escaped}, Subject: {subject_escaped}")
            send_telegram_message(text)
            save_last_email(from_, subject)
            update_stats(sent=1)
            mail.store(num, '+FLAGS', '\\Seen')
        mail.logout()
    except Exception as e:
        print("Email check error:", e)
