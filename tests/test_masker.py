"""Tests for app.masker."""

import re
from unittest.mock import patch

from cryptography.fernet import Fernet

from app.masker import (
    decrypt_envelope,
    encrypt_envelope,
    mask_text,
    restore_text,
)
from app.schemas import Envelope, Span


def _span(start, end, type_="EMAIL", text=""):
    return Span(start=start, end=end, type=type_, text=text, source="regex", confidence=1.0)


# ── mask_text ───────────────────────────────────────────────────

class TestMaskText:
    def test_single_span(self):
        text = "email is user@test.com here"
        span = _span(9, 22, text="user@test.com")
        masked, token_map = mask_text(text, [span])
        assert "user@test.com" not in masked
        assert "[[PII:EMAIL:" in masked
        assert len(token_map) == 1

    def test_multiple_spans(self):
        text = "aaa bbb ccc"
        spans = [
            _span(0, 3, text="aaa"),
            _span(4, 7, text="bbb"),
        ]
        masked, token_map = mask_text(text, spans)
        assert "aaa" not in masked
        assert "bbb" not in masked
        assert len(token_map) == 2

    def test_empty_spans(self):
        text = "no pii here"
        masked, token_map = mask_text(text, [])
        assert masked == text
        assert token_map == {}

    def test_token_format(self):
        text = "user@test.com"
        span = _span(0, 13, text="user@test.com")
        masked, _ = mask_text(text, [span])
        assert re.match(r"\[\[PII:EMAIL:[a-f0-9]{8}\]\]", masked)

    def test_adjacent_spans(self):
        text = "aabbcc"
        spans = [
            _span(0, 2, text="aa", type_="PHONE_KR"),
            _span(2, 4, text="bb", type_="EMAIL"),
            _span(4, 6, text="cc", type_="RRN_KR"),
        ]
        masked, token_map = mask_text(text, spans)
        assert "aa" not in masked
        assert "bb" not in masked
        assert "cc" not in masked
        assert len(token_map) == 3

    def test_preserves_surrounding_text(self):
        text = "before user@test.com after"
        span = _span(7, 20, text="user@test.com")
        masked, _ = mask_text(text, [span])
        assert masked.startswith("before ")
        assert masked.endswith(" after")


# ── restore_text ────────────────────────────────────────────────

class TestRestoreText:
    def test_single_token(self):
        text = "email is user@test.com here"
        span = _span(9, 22, text="user@test.com")
        masked, token_map = mask_text(text, [span])
        restored = restore_text(masked, token_map)
        assert restored == text

    def test_multiple_tokens(self):
        text = "aaa and bbb"
        spans = [_span(0, 3, text="aaa"), _span(8, 11, text="bbb")]
        masked, token_map = mask_text(text, spans)
        restored = restore_text(masked, token_map)
        assert restored == text

    def test_empty_map(self):
        text = "no tokens here"
        assert restore_text(text, {}) == text


# ── round-trip ──────────────────────────────────────────────────

class TestRoundTrip:
    def test_mask_restore_roundtrip(self):
        text = "홍길동의 이메일은 hong@example.com입니다"
        span = _span(10, 26, text="hong@example.com")
        masked, token_map = mask_text(text, [span])
        restored = restore_text(masked, token_map)
        assert restored == text

    def test_korean_text_roundtrip(self):
        text = "전화번호는 010-1234-5678이고 이메일은 a@b.com입니다"
        spans = [
            _span(6, 19, text="010-1234-5678", type_="PHONE_KR"),
            _span(27, 34, text="a@b.com"),
        ]
        masked, token_map = mask_text(text, spans)
        restored = restore_text(masked, token_map)
        assert restored == text


# ── encrypt/decrypt ─────────────────────────────────────────────

class TestEncryptDecrypt:
    def test_roundtrip(self):
        envelope = Envelope(token_map={"abc12345": "user@test.com"})
        encrypted = encrypt_envelope(envelope)
        decrypted = decrypt_envelope(encrypted)
        assert decrypted.token_map == envelope.token_map

    def test_encrypted_is_string(self):
        envelope = Envelope(token_map={"abc12345": "hello"})
        encrypted = encrypt_envelope(envelope)
        assert isinstance(encrypted, str)

    def test_different_envelopes_different_ciphertext(self):
        e1 = Envelope(token_map={"a": "1"})
        e2 = Envelope(token_map={"b": "2"})
        assert encrypt_envelope(e1) != encrypt_envelope(e2)

    def test_token_map_preserved(self):
        original = {"id1": "홍길동", "id2": "010-1234-5678", "id3": "user@test.com"}
        envelope = Envelope(token_map=original)
        decrypted = decrypt_envelope(encrypt_envelope(envelope))
        assert decrypted.token_map == original

    def test_empty_token_map(self):
        envelope = Envelope(token_map={})
        decrypted = decrypt_envelope(encrypt_envelope(envelope))
        assert decrypted.token_map == {}

    def test_invalid_token_raises(self):
        import pytest

        with pytest.raises(Exception):
            decrypt_envelope("not-valid-fernet-token")
