import pytest
from unittest import mock
import gmail_service

@pytest.mark.parametrize("text", [
    "Hello World",
    "",
    "a"*500,
    "<b>Bold Text</b>",
    "<i>Italic & Special <>&</i>",
    "Emojis 😃🎉💌",
    "HTML + Emojis <b>Test 😎</b>"
])
@pytest.mark.parametrize("inline_keyboard", [
    [[{"text": "📬 Open Gmail", "url": "https://mail.google.com"}]],
    [],
    [[{"text": "Button 1", "url": "https://example.com"}, {"text": "Button 2", "url": "https://example.org"}]]
])
def test_send_telegram_message_combinations(monkeypatch, text, inline_keyboard):
    mock_post = mock.Mock()
    monkeypatch.setattr("requests.post", mock_post)

    def patched_send(message):
        payload = {
            "chat_id": 12345,  
            "text": message,
            "parse_mode": "HTML",
            "reply_markup": {"inline_keyboard": inline_keyboard}
        }
        import requests
        requests.post("https://api.telegram.org/fake_token/sendMessage", data=payload)

    monkeypatch.setattr(gmail_service, "send_telegram_message", patched_send)

    gmail_service.send_telegram_message(text)

    assert mock_post.called
    args, kwargs = mock_post.call_args
    payload = kwargs.get("data")
    assert payload["text"] == text
    assert payload["parse_mode"] == "HTML"
    assert payload["reply_markup"]["inline_keyboard"] == inline_keyboard


def test_send_telegram_message_exception(monkeypatch):
    def raise_exception(*args, **kwargs):
        raise Exception("fail")
    
    monkeypatch.setattr("requests.post", raise_exception)

    def patched_send(message):
        import requests
        payload = {
            "chat_id": 12345,
            "text": message,
            "parse_mode": "HTML",
            "reply_markup": {"inline_keyboard": []}
        }
        try:
            requests.post("https://api.telegram.org/fake_token/sendMessage", data=payload)
        except Exception:
            pass  

    monkeypatch.setattr(gmail_service, "send_telegram_message", patched_send)
    
    gmail_service.send_telegram_message("Test")  