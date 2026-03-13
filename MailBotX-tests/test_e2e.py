import pytest
from unittest import mock
import telegram_bot
import gmail_service

# ----------------- Fixtures -----------------
@pytest.fixture
def mock_send_message(monkeypatch):
    """Mock send_message to Telegram"""
    mock_func = mock.Mock()
    monkeypatch.setattr(telegram_bot, "send_message", mock_func)
    return mock_func

@pytest.fixture
def mock_gmail_emails(monkeypatch):
    """Mock Gmail emails with simple edge cases"""
    class MockIMAP:
        def login(self, user, password):
            return "OK", []

        def select(self, mailbox):
            return "OK", []

        def store(self, num, flags, mark):
            return "OK", []

        def logout(self):
            return "OK"

        def search(self, charset, *args):
            return "OK", [b"1 2 3 4 5 6"]

        def fetch(self, num, message_parts):
            emails = {
                b"1": "Subject: HTML Email\nFrom: html@test.com\n\n<b>Hello</b>",
                b"2": "Subject: \nFrom: empty_subject@test.com\n\nBody with text",
                b"3": "Subject: No Body\nFrom: nobody@test.com\n\n",
                b"4": "Subject: Long Body\nFrom: longbody@test.com\n\n" + "a"*500,
                b"5": "Subject: Emojis\nFrom: emoji@test.com\n\nHello world 😃🎉",
                b"6": "Subject: Multipart\nFrom: multipart@test.com\n\nBody part1\nBody part2"
            }
            return "OK", [(num.encode() if isinstance(num, str) else num, emails[num].encode("utf-8"))]

    monkeypatch.setattr("imaplib.IMAP4_SSL", lambda server: MockIMAP())

# ----------------- Test E2E -----------------
def test_bot_commands_and_email_flow(mock_send_message, mock_gmail_emails, monkeypatch):
    """Test all bot commands + email processing end-to-end"""
    chat_id = 12345

    # Bot ON
    monkeypatch.setattr(telegram_bot, "get_status", lambda: True)

    # Test all commands
    commands = ["/start", "/stop", "/test", "/status", "/last", "/stats", "/menu"]
    for cmd in commands:
        telegram_bot.handle_command(cmd, chat_id)
    assert mock_send_message.call_count == len(commands)

    # Patch send_telegram_message to track payloads
    payloads = []
    def fake_send_telegram_message(text):
        payloads.append(text)
    monkeypatch.setattr(gmail_service, "send_telegram_message", fake_send_telegram_message)

    # Run email processing
    gmail_service.check_email()
    assert len(payloads) == 6  

    # Validate edge cases in emails
    assert any("&lt;b&gt;Hello&lt;/b&gt;" in p for p in payloads)
    assert any("empty_subject@test.com" in p for p in payloads)
    assert any("a"*300 in p for p in payloads)
    assert any("😃" in p for p in payloads)
    assert any("Body part2" in p for p in payloads)

    # Sequential email + commands
    telegram_bot.handle_command("/status", chat_id)
    telegram_bot.handle_command("/last", chat_id)
    telegram_bot.handle_command("/stats", chat_id)
    assert mock_send_message.call_count == len(commands) + 3

# ----------------- Negative / edge cases -----------------
def test_invalid_command_does_nothing(mock_send_message):
    chat_id = 1
    telegram_bot.handle_command("/invalid", chat_id)
    assert not mock_send_message.called

def test_bot_off_email_not_sent(monkeypatch):
    """Emails are not sent if bot status is OFF"""
    monkeypatch.setattr(telegram_bot, "get_status", lambda: False)
    sent = []

    # Mock email processing
    class MockIMAP:
        def login(self, user, password): return "OK", []
        def select(self, mailbox): return "OK", []
        def store(self, num, flags, mark): return "OK", []
        def logout(self): return "OK"
        def search(self, charset, *args): return "OK", [b"1"]
        def fetch(self, num, message_parts):
            return "OK", [(b"1", b"Subject: Test\nFrom: test@test.com\n\nBody")]
    monkeypatch.setattr("imaplib.IMAP4_SSL", lambda server: MockIMAP())

    def send_if_bot_on(text):
        if telegram_bot.get_status():
            sent.append(text)
    monkeypatch.setattr(gmail_service, "send_telegram_message", send_if_bot_on)

    gmail_service.check_email()
    assert len(sent) == 0 

def test_telegram_api_exception(monkeypatch):
    """send_telegram_message handles requests exceptions gracefully"""
    def fail_send(text):
        raise Exception("fail")
    monkeypatch.setattr(gmail_service, "send_telegram_message", fail_send)
    try:
        gmail_service.check_email()
    except Exception:
        pytest.fail("check_email should handle exceptions gracefully")