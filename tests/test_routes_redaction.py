"""Tests for POST /redaction/{model}."""

import json
from unittest.mock import MagicMock, patch

import pytest


class TestModelValidation:
    def test_invalid_model(self, client):
        resp = client.post(
            "/redaction/invalid",
            files={"file": ("test.txt", b"hello", "text/plain")},
        )
        assert resp.status_code == 400

    def test_regex_model_accepted(self, client):
        resp = client.post(
            "/redaction/regex",
            files={"file": ("test.txt", b"no pii here", "text/plain")},
        )
        assert resp.status_code == 200

    def test_ner_model_accepted(self, client):
        resp = client.post(
            "/redaction/ner",
            files={"file": ("test.txt", b"no pii here", "text/plain")},
        )
        assert resp.status_code == 200


class TestRegexRedaction:
    def test_pii_text_masked(self, client):
        resp = client.post(
            "/redaction/regex",
            files={"file": ("test.txt", "이메일 user@example.com".encode(), "text/plain")},
        )
        data = resp.json()
        assert resp.status_code == 200
        assert "user@example.com" not in data["masked_text"]
        assert data["audit"]["total_found"] >= 1
        assert "regex" in data["audit"]["sources_used"]

    def test_no_pii_text(self, client):
        resp = client.post(
            "/redaction/regex",
            files={"file": ("test.txt", "안녕하세요".encode(), "text/plain")},
        )
        data = resp.json()
        assert data["audit"]["total_found"] == 0
        assert data["masked_text"] == "안녕하세요"


class TestGeminiRedaction:
    def test_gemini_disabled(self, client):
        with patch("app.routes.redaction.settings") as mock_settings:
            mock_settings.ALLOW_REMOTE_LLM = False
            resp = client.post(
                "/redaction/gemini",
                files={"file": ("test.txt", b"hello", "text/plain")},
            )
        assert resp.status_code == 403

    def test_gemini_enabled_with_mock(self, client):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = json.dumps([
            {"start": 0, "end": 3, "type": "PERSON", "text": "홍길동", "confidence": 0.9}
        ])
        mock_client.models.generate_content.return_value = mock_response

        with (
            patch("app.routes.redaction.settings") as mock_settings,
            patch("app.detectors.llm_detector.settings") as mock_llm_settings,
            patch("app.detectors.llm_detector.genai.Client", return_value=mock_client),
        ):
            mock_settings.ALLOW_REMOTE_LLM = True
            mock_llm_settings.GEMINI_API_KEY = "test-key"
            resp = client.post(
                "/redaction/gemini",
                files={"file": ("test.txt", "홍길동은 학생입니다".encode(), "text/plain")},
            )
        assert resp.status_code == 200
        assert "llm" in resp.json()["audit"]["sources_used"]


class TestHybridRedaction:
    def test_hybrid_disabled(self, client):
        with patch("app.routes.redaction.settings") as mock_settings:
            mock_settings.ALLOW_REMOTE_LLM = False
            resp = client.post(
                "/redaction/hybrid",
                files={"file": ("test.txt", b"hello", "text/plain")},
            )
        assert resp.status_code == 403

    def test_hybrid_enabled(self, client):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "[]"
        mock_client.models.generate_content.return_value = mock_response

        with (
            patch("app.routes.redaction.settings") as mock_settings,
            patch("app.detectors.llm_detector.settings") as mock_llm_settings,
            patch("app.detectors.llm_detector.genai.Client", return_value=mock_client),
        ):
            mock_settings.ALLOW_REMOTE_LLM = True
            mock_llm_settings.GEMINI_API_KEY = "test-key"
            resp = client.post(
                "/redaction/hybrid",
                files={"file": ("test.txt", "email user@test.com".encode(), "text/plain")},
            )
        data = resp.json()
        assert resp.status_code == 200
        sources = data["audit"]["sources_used"]
        assert "regex" in sources
        assert "ner" in sources
        assert "llm" in sources


class TestEnvelope:
    def test_include_envelope_true(self, client):
        resp = client.post(
            "/redaction/regex?include_envelope=true",
            files={"file": ("test.txt", "user@test.com".encode(), "text/plain")},
        )
        data = resp.json()
        assert data["envelope"] is not None
        assert "token_map" in data["envelope"]

    def test_include_envelope_false(self, client):
        resp = client.post(
            "/redaction/regex?include_envelope=false",
            files={"file": ("test.txt", "user@test.com".encode(), "text/plain")},
        )
        data = resp.json()
        assert data["envelope"] is None

    def test_store_envelope_false(self, client):
        resp = client.post(
            "/redaction/regex?store_envelope=false",
            files={"file": ("test.txt", "user@test.com".encode(), "text/plain")},
        )
        data = resp.json()
        doc_id = data["doc_id"]
        # Restore should fail because envelope not stored
        restore_resp = client.post(
            f"/restore/{doc_id}",
            headers={"X-ADMIN-KEY": "changeme"},
        )
        assert restore_resp.status_code == 400


class TestMissingFile:
    def test_no_file_422(self, client):
        resp = client.post("/redaction/regex")
        assert resp.status_code == 422


class TestE2E:
    def test_upload_redact_download_restore(self, client):
        original = "홍길동의 이메일은 hong@example.com 입니다"
        # 1. Upload and redact
        resp = client.post(
            "/redaction/regex",
            files={"file": ("test.txt", original.encode(), "text/plain")},
        )
        assert resp.status_code == 200
        data = resp.json()
        doc_id = data["doc_id"]
        assert "hong@example.com" not in data["masked_text"]

        # 2. Download masked
        dl_resp = client.get(f"/download/{doc_id}?format=masked")
        assert dl_resp.status_code == 200
        assert "hong@example.com" not in dl_resp.text

        # 3. Download audit
        audit_resp = client.get(f"/download/{doc_id}?format=audit")
        assert audit_resp.status_code == 200

        # 4. Restore
        restore_resp = client.post(
            f"/restore/{doc_id}",
            headers={"X-ADMIN-KEY": "changeme"},
        )
        assert restore_resp.status_code == 200
        assert restore_resp.json()["restored_text"] == original
