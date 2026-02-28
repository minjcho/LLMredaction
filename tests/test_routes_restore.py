"""Tests for POST /restore/{doc_id}."""

from app import storage
from app.masker import encrypt_envelope, mask_text
from app.schemas import Audit, Envelope, Span


def _store_with_envelope(original_text="user@test.com"):
    span = Span(start=0, end=len(original_text), type="EMAIL", text=original_text, source="regex")
    masked, token_map = mask_text(original_text, [span])
    envelope = Envelope(token_map=token_map)
    encrypted = encrypt_envelope(envelope)
    audit = Audit(spans=[span], total_found=1, sources_used=["regex"])
    doc_id = storage.store(masked, audit, encrypted)
    return doc_id


class TestRestore:
    def test_valid_restore(self, client):
        doc_id = _store_with_envelope("user@test.com")
        resp = client.post(
            f"/restore/{doc_id}",
            headers={"X-ADMIN-KEY": "changeme"},
        )
        assert resp.status_code == 200
        assert resp.json()["restored_text"] == "user@test.com"

    def test_wrong_admin_key(self, client):
        doc_id = _store_with_envelope()
        resp = client.post(
            f"/restore/{doc_id}",
            headers={"X-ADMIN-KEY": "wrong-key"},
        )
        assert resp.status_code == 403

    def test_missing_admin_key(self, client):
        doc_id = _store_with_envelope()
        resp = client.post(f"/restore/{doc_id}")
        assert resp.status_code == 422

    def test_nonexistent_doc(self, client):
        resp = client.post(
            "/restore/nonexistent1",
            headers={"X-ADMIN-KEY": "changeme"},
        )
        assert resp.status_code == 404

    def test_no_envelope_stored(self, client):
        audit = Audit(spans=[], total_found=0, sources_used=["regex"])
        doc_id = storage.store("masked text", audit, None)
        resp = client.post(
            f"/restore/{doc_id}",
            headers={"X-ADMIN-KEY": "changeme"},
        )
        assert resp.status_code == 400

    def test_restore_returns_doc_id(self, client):
        doc_id = _store_with_envelope()
        resp = client.post(
            f"/restore/{doc_id}",
            headers={"X-ADMIN-KEY": "changeme"},
        )
        assert resp.json()["doc_id"] == doc_id
