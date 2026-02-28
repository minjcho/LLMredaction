"""Tests for GET /download/{doc_id}."""

from app import storage
from app.schemas import Audit


def _store_doc(masked="masked text", envelope="enc"):
    audit = Audit(spans=[], total_found=0, sources_used=["regex"])
    return storage.store(masked, audit, envelope)


class TestDownloadMasked:
    def test_masked_format(self, client):
        doc_id = _store_doc(masked="hello masked")
        resp = client.get(f"/download/{doc_id}?format=masked")
        assert resp.status_code == 200
        assert resp.text == "hello masked"
        assert "text/plain" in resp.headers["content-type"]

    def test_content_disposition(self, client):
        doc_id = _store_doc()
        resp = client.get(f"/download/{doc_id}?format=masked")
        assert f"{doc_id}_masked.txt" in resp.headers["content-disposition"]


class TestDownloadAudit:
    def test_audit_format(self, client):
        doc_id = _store_doc()
        resp = client.get(f"/download/{doc_id}?format=audit")
        assert resp.status_code == 200
        data = resp.json()
        assert "total_found" in data
        assert "application/json" in resp.headers["content-type"]

    def test_audit_content_disposition(self, client):
        doc_id = _store_doc()
        resp = client.get(f"/download/{doc_id}?format=audit")
        assert f"{doc_id}_audit.json" in resp.headers["content-disposition"]


class TestDownloadErrors:
    def test_invalid_format(self, client):
        doc_id = _store_doc()
        resp = client.get(f"/download/{doc_id}?format=invalid")
        assert resp.status_code == 400

    def test_nonexistent_doc(self, client):
        resp = client.get("/download/nonexistent1?format=masked")
        assert resp.status_code == 404

    def test_default_format_is_masked(self, client):
        doc_id = _store_doc(masked="default test")
        resp = client.get(f"/download/{doc_id}")
        assert resp.status_code == 200
        assert resp.text == "default test"
