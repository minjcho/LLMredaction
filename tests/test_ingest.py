"""Tests for app.ingest."""

import io
from unittest.mock import MagicMock, patch

import pytest
from fastapi import UploadFile

from app.ingest import extract_text


def _make_upload(content: bytes, filename: str) -> UploadFile:
    return UploadFile(file=io.BytesIO(content), filename=filename)


@pytest.mark.asyncio
class TestTXT:
    async def test_utf8_text(self):
        upload = _make_upload(b"hello world", "test.txt")
        text, kind = await extract_text(upload)
        assert text == "hello world"
        assert kind == "txt"

    async def test_korean_text(self):
        content = "안녕하세요 홍길동입니다".encode("utf-8")
        upload = _make_upload(content, "korean.txt")
        text, kind = await extract_text(upload)
        assert "홍길동" in text

    async def test_invalid_utf8_replaced(self):
        content = b"hello \xff\xfe world"
        upload = _make_upload(content, "bad.txt")
        text, kind = await extract_text(upload)
        assert "hello" in text
        assert "world" in text
        assert kind == "txt"


@pytest.mark.asyncio
class TestPDF:
    async def test_valid_pdf(self):
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "PDF content here"
        mock_reader = MagicMock()
        mock_reader.pages = [mock_page]

        with patch("app.ingest.PdfReader", return_value=mock_reader):
            upload = _make_upload(b"fake-pdf", "document.pdf")
            text, kind = await extract_text(upload)
        assert text == "PDF content here"
        assert kind == "pdf"

    async def test_empty_pdf_raises_400(self):
        mock_page = MagicMock()
        mock_page.extract_text.return_value = ""
        mock_reader = MagicMock()
        mock_reader.pages = [mock_page]

        with patch("app.ingest.PdfReader", return_value=mock_reader):
            upload = _make_upload(b"fake-pdf", "empty.pdf")
            with pytest.raises(Exception) as exc_info:
                await extract_text(upload)
            assert exc_info.value.status_code == 400


@pytest.mark.asyncio
class TestExtension:
    async def test_no_extension_treated_as_txt(self):
        upload = _make_upload(b"plain text", "noext")
        text, kind = await extract_text(upload)
        assert kind == "txt"
        assert text == "plain text"

    async def test_uppercase_pdf(self):
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "content"
        mock_reader = MagicMock()
        mock_reader.pages = [mock_page]

        with patch("app.ingest.PdfReader", return_value=mock_reader):
            upload = _make_upload(b"fake-pdf", "FILE.PDF")
            text, kind = await extract_text(upload)
        assert kind == "pdf"

    async def test_none_filename(self):
        upload = _make_upload(b"content", None)
        # filename defaults to "" when None
        upload.filename = None
        text, kind = await extract_text(upload)
        assert kind == "txt"
