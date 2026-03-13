import pytest
import json
import builtins
import gmail_service
import telegram_bot

# ----------------- Fixtures -----------------

@pytest.fixture
def stats_file(tmp_path):
    file = tmp_path / "stats.json"
    file.write_text('{"processed":5,"sent":2,"ignored":1}')
    return file

@pytest.fixture
def last_email_file(tmp_path):
    file = tmp_path / "last_email.json"
    file.write_text(json.dumps({"from": "user@test.com", "subject": "Old", "time": "12:00"}))
    return file

@pytest.fixture
def bot_status_file(tmp_path):
    file = tmp_path / "bot_status.json"
    file.write_text(json.dumps({"running": True}))
    return file

# ----------------- Regression tests for update_stats -----------------

@pytest.mark.parametrize("processed,sent,ignored,expected", [
    (0,0,0,{"processed":5,"sent":2,"ignored":1}),
    (1,1,1,{"processed":6,"sent":3,"ignored":2}),
    (10,0,0,{"processed":15,"sent":2,"ignored":1}),
    (0,10,0,{"processed":5,"sent":12,"ignored":1}),
    (0,0,10,{"processed":5,"sent":2,"ignored":11}),
])
def test_update_stats_regression(stats_file, processed, sent, ignored, expected, monkeypatch):
    original_open = builtins.open

    def fake_open(filename, mode='r', *args, **kwargs):
        if filename == "stats.json":
            filename = str(stats_file)
        return original_open(filename, mode, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", fake_open)
    gmail_service.update_stats(processed, sent, ignored)
    data = json.loads(stats_file.read_text())
    assert data == expected

def test_update_stats_file_missing(tmp_path, monkeypatch):
    tmp_file = tmp_path / "stats.json"
    original_open = builtins.open

    def fake_open(filename, mode='r', *args, **kwargs):
        if 'r' in mode:
            raise FileNotFoundError()
        if filename == "stats.json":
            filename = str(tmp_file)
        return original_open(filename, mode, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", fake_open)
    gmail_service.update_stats(processed=1, sent=2, ignored=3)
    data = json.loads(tmp_file.read_text())
    assert data == {"processed":1,"sent":2,"ignored":3}

# ----------------- Regression tests for save_last_email -----------------

@pytest.mark.parametrize("from_,subject", [
    ("user1@test.com", "Hello"),
    ("", ""),
    ("user2@test.com", "Special chars <>&"),
    ("emoji@test.com", "Emojis 😃🎉"),
])
def test_save_last_email_regression(tmp_path, from_, subject, monkeypatch):
    file = tmp_path / "last_email.json"
    original_open = builtins.open

    def fake_open(filename, mode='w', *args, **kwargs):
        if filename == "last_email.json":
            filename = str(file)
        return original_open(filename, mode, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", fake_open)
    gmail_service.save_last_email(from_, subject)
    data = json.loads(file.read_text())
    assert data["from"] == from_
    assert data["subject"] == subject
    assert "time" in data

# ----------------- Regression tests for bot_is_running -----------------

def test_bot_is_running_file_exists(bot_status_file, monkeypatch):
    original_open = builtins.open

    def fake_open(filename, mode='r', *args, **kwargs):
        if filename == "bot_status.json":
            filename = str(bot_status_file)
        return original_open(filename, mode, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", fake_open)
    assert gmail_service.bot_is_running() is True

def test_bot_is_running_file_missing(monkeypatch):
    def fake_open(filename, mode='r', *args, **kwargs):
        raise FileNotFoundError()
    monkeypatch.setattr(builtins, "open", fake_open)
    assert gmail_service.bot_is_running() is True

# ----------------- Regression tests for telegram_bot helpers -----------------

def test_get_status_file_exists(bot_status_file, monkeypatch):
    original_open = builtins.open

    def fake_open(filename, mode='r', *args, **kwargs):
        if filename == "bot_status.json":
            filename = str(bot_status_file)
        return original_open(filename, mode, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", fake_open)
    assert telegram_bot.get_status() is True

def test_get_status_file_missing(monkeypatch):
    def fake_open(filename, mode='r', *args, **kwargs):
        raise FileNotFoundError()
    monkeypatch.setattr(builtins, "open", fake_open)
    assert telegram_bot.get_status() is True

def test_get_last_email_existing(last_email_file, monkeypatch):
    original_open = builtins.open

    def fake_open(filename, mode='r', *args, **kwargs):
        if filename == "last_email.json":
            filename = str(last_email_file)
        return original_open(filename, mode, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", fake_open)
    data = telegram_bot.get_last_email()
    assert data["from"] == "user@test.com"

def test_get_last_email_missing(monkeypatch):
    def fake_open(filename, mode='r', *args, **kwargs):
        raise FileNotFoundError()
    monkeypatch.setattr(builtins, "open", fake_open)
    assert telegram_bot.get_last_email() is None

def test_get_stats_existing(stats_file, monkeypatch):
    original_open = builtins.open

    def fake_open(filename, mode='r', *args, **kwargs):
        if filename == "stats.json":
            filename = str(stats_file)
        return original_open(filename, mode, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", fake_open)
    data = telegram_bot.get_stats()
    assert data["processed"] == 5
    assert data["sent"] == 2
    assert data["ignored"] == 1

def test_get_stats_missing(monkeypatch):
    def fake_open(filename, mode='r', *args, **kwargs):
        raise FileNotFoundError()
    monkeypatch.setattr(builtins, "open", fake_open)
    data = telegram_bot.get_stats()
    assert data == {"processed":0,"sent":0,"ignored":0}

def test_set_status_true(tmp_path, monkeypatch):
    file = tmp_path / "bot_status.json"
    original_open = builtins.open

    def fake_open(filename, mode='w', *args, **kwargs):
        if filename == "bot_status.json":
            filename = str(file)
        return original_open(filename, mode, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", fake_open)
    telegram_bot.set_status(True)
    data = json.loads(file.read_text())
    assert data["running"] is True

def test_set_status_false(tmp_path, monkeypatch):
    file = tmp_path / "bot_status.json"
    original_open = builtins.open

    def fake_open(filename, mode='w', *args, **kwargs):
        if filename == "bot_status.json":
            filename = str(file)
        return original_open(filename, mode, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", fake_open)
    telegram_bot.set_status(False)
    data = json.loads(file.read_text())
    assert data["running"] is False

# ----------------- Regression tests for handle_command -----------------

@pytest.mark.parametrize("command", ["/start", "/stop", "/test", "/status", "/last", "/stats", "/menu"])
def test_handle_command_calls(monkeypatch, command):
    calls = []
    monkeypatch.setattr(telegram_bot, "send_message", lambda chat_id, msg: calls.append(msg))
    monkeypatch.setattr(telegram_bot, "set_status", lambda value: calls.append(f"status:{value}"))
    telegram_bot.handle_command(command, 1)
    assert len(calls) > 0

def test_handle_command_unknown(monkeypatch):
    calls = []
    monkeypatch.setattr(telegram_bot, "send_message", lambda chat_id, msg: calls.append(msg))
    telegram_bot.handle_command("/unknown", 1)
    assert calls == []

# ----------------- Regression edge case: large numbers -----------------

def test_update_stats_large_numbers(tmp_path, monkeypatch):
    file = tmp_path / "stats.json"
    file.write_text(json.dumps({"processed": 999999, "sent": 999999, "ignored": 999999}))
    original_open = builtins.open

    def fake_open(filename, mode='r+', *args, **kwargs):
        if filename == "stats.json":
            filename = str(file)
        return original_open(filename, mode, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", fake_open)
    gmail_service.update_stats(processed=1, sent=1, ignored=1)
    data = json.loads(file.read_text())
    assert data["processed"] == 1000000
    assert data["sent"] == 1000000
    assert data["ignored"] == 1000000