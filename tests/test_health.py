"""Tests for GET /health."""


class TestHealth:
    def test_health_200(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}

    def test_health_content_type(self, client):
        resp = client.get("/health")
        assert "application/json" in resp.headers["content-type"]
