import threading
import time
import config
from gmail_service import check_email, bot_is_running
from telegram_bot import run_bot


def email_loop():

    while True:

        if bot_is_running():

            print("Checking email...")

            check_email()

        else:

            print("Email notifications paused")

        time.sleep(config.CHECK_INTERVAL)


telegram_thread = threading.Thread(target=run_bot)

telegram_thread.start()

email_loop()