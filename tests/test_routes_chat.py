"""Tests for POST /chat."""

from unittest.mock import MagicMock, patch


class TestChat:
    def test_no_api_key_503(self, client):
        with patch("app.routes.chat.settings") as mock_settings:
            mock_settings.GEMINI_API_KEY = ""
            resp = client.post("/chat", json={"message": "hello"})
        assert resp.status_code == 503

    def test_valid_chat(self, client):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "I'm an AI assistant"
        mock_client.models.generate_content.return_value = mock_response

        with (
            patch("app.routes.chat.settings") as mock_settings,
            patch("app.routes.chat.genai.Client", return_value=mock_client),
        ):
            mock_settings.GEMINI_API_KEY = "test-key"
            resp = client.post("/chat", json={"message": "hello"})
        assert resp.status_code == 200
        assert resp.json()["reply"] == "I'm an AI assistant"

    def test_chat_with_history(self, client):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "response"
        mock_client.models.generate_content.return_value = mock_response

        with (
            patch("app.routes.chat.settings") as mock_settings,
            patch("app.routes.chat.genai.Client", return_value=mock_client),
        ):
            mock_settings.GEMINI_API_KEY = "test-key"
            resp = client.post(
                "/chat",
                json={
                    "message": "follow up",
                    "history": [
                        {"role": "user", "content": "first message"},
                        {"role": "model", "content": "first reply"},
                    ],
                },
            )
        assert resp.status_code == 200

    def test_empty_reply(self, client):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = None
        mock_client.models.generate_content.return_value = mock_response

        with (
            patch("app.routes.chat.settings") as mock_settings,
            patch("app.routes.chat.genai.Client", return_value=mock_client),
        ):
            mock_settings.GEMINI_API_KEY = "test-key"
            resp = client.post("/chat", json={"message": "hello"})
        assert resp.status_code == 200
        assert resp.json()["reply"] == ""

    def test_missing_message_422(self, client):
        resp = client.post("/chat", json={})
        assert resp.status_code == 422

    def test_invalid_body_422(self, client):
        resp = client.post("/chat", json={"wrong_field": "value"})
        assert resp.status_code == 422
