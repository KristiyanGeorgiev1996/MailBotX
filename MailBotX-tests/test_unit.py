import pytest
import json
from unittest import mock
from datetime import datetime
import builtins
import gmail_service
import telegram_bot

# ----------------- Mock datetime -----------------
class MockDateTime:
    @classmethod
    def now(cls):
        return datetime(2026, 3, 13, 12, 0)

@pytest.fixture(autouse=True)
def patch_datetime(monkeypatch):
    monkeypatch.setattr(gmail_service, "datetime", MockDateTime)
    yield

# ----------------- Helper to mock open -----------------
class DummyFile:
    def __init__(self, initial_content=""):
        self.content = initial_content
        self.written = ""
        self.read_pointer = 0

    def __enter__(self):
        from io import StringIO
        self.io = StringIO(self.content)
        return self.io

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.written = self.io.getvalue()

# ----------------- bot_is_running -----------------
def test_bot_is_running_existing_file(monkeypatch):
    dummy_file = DummyFile(json.dumps({"running": False}))
    monkeypatch.setattr(builtins, "open", lambda *a, **k: dummy_file)
    assert gmail_service.bot_is_running() is False

def test_bot_is_running_no_file(monkeypatch):
    def raise_fn(*a, **k):
        raise FileNotFoundError()
    monkeypatch.setattr(builtins, "open", raise_fn)
    assert gmail_service.bot_is_running() is True

# ----------------- update_stats -----------------
def test_update_stats_creates_file(monkeypatch):
    dummy_file = DummyFile()
    monkeypatch.setattr(builtins, "open", lambda *a, **k: dummy_file)
    gmail_service.update_stats(processed=2, sent=1, ignored=0)
    written = dummy_file.written
    data = json.loads(written)
    assert data["processed"] == 2
    assert data["sent"] == 1
    assert data["ignored"] == 0

def test_update_stats_existing_file(monkeypatch):
    dummy_file = DummyFile(json.dumps({"processed": 5, "sent": 3, "ignored": 1}))
    monkeypatch.setattr(builtins, "open", lambda *a, **k: dummy_file)
    gmail_service.update_stats(processed=2, sent=1, ignored=0)
    data = json.loads(dummy_file.written)
    assert data["processed"] == 7
    assert data["sent"] == 4
    assert data["ignored"] == 1

# ----------------- save_last_email -----------------
def test_save_last_email(monkeypatch):
    dummy_file = DummyFile()
    monkeypatch.setattr(builtins, "open", lambda *a, **k: dummy_file)
    gmail_service.save_last_email("from@test.com", "Subject")
    written = json.loads(dummy_file.written)
    assert written["from"] == "from@test.com"
    assert written["subject"] == "Subject"
    assert written["time"] == "12:00"

# ----------------- send_telegram_message -----------------
def test_send_telegram_message_payload(monkeypatch):
    mock_post = mock.Mock()
    monkeypatch.setattr("requests.post", mock_post)

    gmail_service.send_telegram_message("Hello")

    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args

    assert args[0].startswith("https://api.telegram.org/bot")
    assert args[0].endswith("/sendMessage")
    assert kwargs["data"]["text"] == "Hello"

def test_send_telegram_message_exception(monkeypatch):
    def fail_post(*a, **k):
        raise Exception("fail")
    monkeypatch.setattr("requests.post", fail_post)
    gmail_service.send_telegram_message("Test")

# ----------------- telegram_bot helpers -----------------
def test_get_status_default(monkeypatch):
    monkeypatch.setattr(builtins, "open", lambda *a, **k: (_ for _ in ()).throw(FileNotFoundError()))
    assert telegram_bot.get_status() is True

def test_get_status_existing_file(monkeypatch):
    dummy_file = DummyFile(json.dumps({"running": False}))
    monkeypatch.setattr(builtins, "open", lambda *a, **k: dummy_file)
    assert telegram_bot.get_status() is False

def test_get_last_email_none(monkeypatch):
    monkeypatch.setattr(builtins, "open", lambda *a, **k: (_ for _ in ()).throw(FileNotFoundError()))
    assert telegram_bot.get_last_email() is None

def test_get_last_email_existing(monkeypatch):
    dummy_file = DummyFile(json.dumps({"from": "user@test.com", "subject": "Hi", "time": "12:00"}))
    monkeypatch.setattr(builtins, "open", lambda *a, **k: dummy_file)
    data = telegram_bot.get_last_email()
    assert data["from"] == "user@test.com"
    assert data["subject"] == "Hi"

def test_get_stats_default(monkeypatch):
    monkeypatch.setattr(builtins, "open", lambda *a, **k: (_ for _ in ()).throw(FileNotFoundError()))
    stats = telegram_bot.get_stats()
    assert stats == {"processed": 0, "sent": 0, "ignored": 0}

def test_get_stats_existing(monkeypatch):
    dummy_file = DummyFile(json.dumps({"processed": 5, "sent": 3, "ignored": 1}))
    monkeypatch.setattr(builtins, "open", lambda *a, **k: dummy_file)
    stats = telegram_bot.get_stats()
    assert stats["processed"] == 5
    assert stats["sent"] == 3
    assert stats["ignored"] == 1

def test_set_status(monkeypatch):
    dummy_file = DummyFile()
    monkeypatch.setattr(builtins, "open", lambda *a, **k: dummy_file)
    telegram_bot.set_status(True)
    data = json.loads(dummy_file.written)
    assert data["running"] is True

# ----------------- handle_command basic coverage -----------------
def test_handle_command_start_stop(monkeypatch):
    calls = []
    monkeypatch.setattr(telegram_bot, "send_message", lambda chat_id, msg: calls.append(msg))
    monkeypatch.setattr(telegram_bot, "set_status", lambda value: calls.append(f"status:{value}"))
    telegram_bot.handle_command("/start", 1)
    telegram_bot.handle_command("/stop", 1)
    assert "status:True" in calls
    assert "status:False" in calls

def test_handle_command_test(monkeypatch):
    calls = []
    monkeypatch.setattr(telegram_bot, "send_message", lambda chat_id, msg: calls.append(msg))
    telegram_bot.handle_command("/test", 1)
    assert any("✅ Bot is working correctly" in c for c in calls)

def test_handle_command_unknown(monkeypatch):
    calls = []
    monkeypatch.setattr(telegram_bot, "send_message", lambda chat_id, msg: calls.append(msg))
    telegram_bot.handle_command("/unknown", 1)
    # Unknown commands should not send anything
    assert calls == []