"""Tests for app.storage."""

import re
from unittest.mock import patch

from app.schemas import Audit, Span
from app import storage


def _make_audit() -> Audit:
    return Audit(spans=[], total_found=0, sources_used=["regex"])


class TestStore:
    def test_returns_hex_id(self):
        doc_id = storage.store("masked", _make_audit())
        assert re.match(r"^[a-f0-9]{12}$", doc_id)

    def test_store_get_roundtrip(self):
        doc_id = storage.store("hello", _make_audit(), "enc-data")
        entry = storage.get(doc_id)
        assert entry is not None
        assert entry["masked_text"] == "hello"
        assert entry["envelope_encrypted"] == "enc-data"

    def test_unique_ids(self):
        ids = {storage.store("t", _make_audit()) for _ in range(100)}
        assert len(ids) == 100


class TestGet:
    def test_nonexistent_returns_none(self):
        assert storage.get("nonexistent123") is None

    def test_ttl_expired_returns_none(self):
        doc_id = storage.store("text", _make_audit())
        # Simulate time passing beyond TTL
        with patch("app.storage.time.time", return_value=storage._store[doc_id]["created_at"] + 99999):
            result = storage.get(doc_id)
        assert result is None

    def test_ttl_within_returns_entry(self):
        doc_id = storage.store("text", _make_audit())
        created = storage._store[doc_id]["created_at"]
        # Simulate time within TTL (1 second after creation)
        with patch("app.storage.time.time", return_value=created + 1):
            result = storage.get(doc_id)
        assert result is not None

    def test_expired_entry_removed_from_store(self):
        doc_id = storage.store("text", _make_audit())
        with patch("app.storage.time.time", return_value=storage._store[doc_id]["created_at"] + 99999):
            storage.get(doc_id)
        assert doc_id not in storage._store


class TestCleanup:
    def test_removes_expired(self):
        doc_id = storage.store("text", _make_audit())
        created = storage._store[doc_id]["created_at"]
        with patch("app.storage.time.time", return_value=created + 99999):
            removed = storage.cleanup()
        assert removed == 1
        assert doc_id not in storage._store

    def test_no_expired_returns_zero(self):
        storage.store("text", _make_audit())
        removed = storage.cleanup()
        assert removed == 0
