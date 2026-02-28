"""Tests for app.detectors.llm_detector."""

import json
from unittest.mock import MagicMock, patch

from app.detectors.llm_detector import detect


def _mock_genai_response(text: str):
    """Create a mock genai Client that returns the given text."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = text
    mock_client.models.generate_content.return_value = mock_response
    return mock_client


class TestLLMDetector:
    def test_no_api_key_returns_empty(self):
        with patch("app.detectors.llm_detector.settings") as mock_settings:
            mock_settings.GEMINI_API_KEY = ""
            result = detect("some text")
        assert result == []

    def test_valid_json_response(self):
        items = [
            {"start": 0, "end": 3, "type": "PERSON", "text": "홍길동", "confidence": 0.95}
        ]
        mock_client = _mock_genai_response(json.dumps(items))
        with (
            patch("app.detectors.llm_detector.settings") as mock_settings,
            patch("app.detectors.llm_detector.genai.Client", return_value=mock_client),
        ):
            mock_settings.GEMINI_API_KEY = "test-key"
            result = detect("홍길동은 학생입니다")
        assert len(result) == 1
        assert result[0].type == "PERSON"
        assert result[0].source == "llm"

    def test_markdown_fence_stripped(self):
        items = [{"start": 0, "end": 3, "type": "PERSON", "text": "홍길동", "confidence": 0.9}]
        raw = f"```json\n{json.dumps(items)}\n```"
        mock_client = _mock_genai_response(raw)
        with (
            patch("app.detectors.llm_detector.settings") as mock_settings,
            patch("app.detectors.llm_detector.genai.Client", return_value=mock_client),
        ):
            mock_settings.GEMINI_API_KEY = "test-key"
            result = detect("홍길동은 학생입니다")
        assert len(result) == 1

    def test_text_mismatch_falls_back_to_substring_search(self):
        """When text[start:end] doesn't match, detector searches for substring."""
        items = [{"start": 99, "end": 102, "type": "PERSON", "text": "홍길동", "confidence": 0.9}]
        mock_client = _mock_genai_response(json.dumps(items))
        with (
            patch("app.detectors.llm_detector.settings") as mock_settings,
            patch("app.detectors.llm_detector.genai.Client", return_value=mock_client),
        ):
            mock_settings.GEMINI_API_KEY = "test-key"
            result = detect("홍길동은 학생입니다")
        assert len(result) == 1
        assert result[0].start == 0
        assert result[0].end == 3

    def test_text_not_found_skips_span(self):
        items = [{"start": 0, "end": 5, "type": "PERSON", "text": "없는텍스트", "confidence": 0.9}]
        mock_client = _mock_genai_response(json.dumps(items))
        with (
            patch("app.detectors.llm_detector.settings") as mock_settings,
            patch("app.detectors.llm_detector.genai.Client", return_value=mock_client),
        ):
            mock_settings.GEMINI_API_KEY = "test-key"
            result = detect("홍길동은 학생입니다")
        assert len(result) == 0

    def test_empty_response(self):
        mock_client = _mock_genai_response("[]")
        with (
            patch("app.detectors.llm_detector.settings") as mock_settings,
            patch("app.detectors.llm_detector.genai.Client", return_value=mock_client),
        ):
            mock_settings.GEMINI_API_KEY = "test-key"
            result = detect("some text")
        assert result == []

    def test_invalid_json_returns_empty(self):
        mock_client = _mock_genai_response("not valid json")
        with (
            patch("app.detectors.llm_detector.settings") as mock_settings,
            patch("app.detectors.llm_detector.genai.Client", return_value=mock_client),
        ):
            mock_settings.GEMINI_API_KEY = "test-key"
            result = detect("some text")
        assert result == []

    def test_default_confidence(self):
        """When confidence is not provided, default to 0.8."""
        items = [{"start": 0, "end": 3, "type": "PERSON", "text": "홍길동"}]
        mock_client = _mock_genai_response(json.dumps(items))
        with (
            patch("app.detectors.llm_detector.settings") as mock_settings,
            patch("app.detectors.llm_detector.genai.Client", return_value=mock_client),
        ):
            mock_settings.GEMINI_API_KEY = "test-key"
            result = detect("홍길동은 학생입니다")
        assert len(result) == 1
        assert result[0].confidence == 0.8

    def test_none_response_text(self):
        mock_client = _mock_genai_response(None)
        # response.text returns None → raw should become "[]"
        mock_resp = MagicMock()
        mock_resp.text = None
        mock_client.models.generate_content.return_value = mock_resp
        with (
            patch("app.detectors.llm_detector.settings") as mock_settings,
            patch("app.detectors.llm_detector.genai.Client", return_value=mock_client),
        ):
            mock_settings.GEMINI_API_KEY = "test-key"
            result = detect("some text")
        assert result == []

    def test_multiple_spans(self):
        items = [
            {"start": 0, "end": 3, "type": "PERSON", "text": "홍길동", "confidence": 0.9},
            {"start": 5, "end": 7, "type": "ORG", "text": "삼성", "confidence": 0.85},
        ]
        mock_client = _mock_genai_response(json.dumps(items))
        with (
            patch("app.detectors.llm_detector.settings") as mock_settings,
            patch("app.detectors.llm_detector.genai.Client", return_value=mock_client),
        ):
            mock_settings.GEMINI_API_KEY = "test-key"
            result = detect("홍길동은 삼성에 다닙니다")
        assert len(result) == 2
        assert result[0].type == "PERSON"
        assert result[1].type == "ORG"
