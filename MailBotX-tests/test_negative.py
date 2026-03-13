import pytest
from unittest import mock
import gmail_service
import telegram_bot

def test_check_email_exception(monkeypatch):
    monkeypatch.setattr("imaplib.IMAP4_SSL", lambda server: (_ for _ in ()).throw(Exception("fail")))
    gmail_service.check_email()  # Should not raise exception

def test_send_telegram_message_exception(monkeypatch):
    monkeypatch.setattr("requests.post", lambda *a, **k: (_ for _ in ()).throw(Exception("fail")))
    gmail_service.send_telegram_message("test")  # Should not raise exception

def test_handle_command_invalid(monkeypatch):
    chat_id = 1
    mock_send = mock.Mock()
    monkeypatch.setattr(telegram_bot, "send_message", mock_send)
    telegram_bot.handle_command("/invalid", chat_id)
    assert not mock_send.called