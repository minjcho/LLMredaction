from __future__ import annotations

from unittest.mock import patch

import pytest
from cryptography.fernet import Fernet
from starlette.testclient import TestClient

# Fixed Fernet key for deterministic encrypt/decrypt in tests
_TEST_FERNET_KEY = Fernet.generate_key()


@pytest.fixture(scope="session", autouse=True)
def patch_masker_fernet():
    """Pin the Fernet key so encrypt/decrypt round-trips are deterministic."""
    with patch("app.masker._fernet_key", _TEST_FERNET_KEY):
        yield


@pytest.fixture(autouse=True)
def clear_storage():
    """Clear the in-memory store before every test."""
    import app.storage as _st

    _st._store.clear()
    yield
    _st._store.clear()


@pytest.fixture()
def client():
    from app.main import app

    with TestClient(app) as c:
        yield c


@pytest.fixture()
def sample_text_with_pii() -> str:
    """Korean text containing known PII for integration tests."""
    return (
        "홍길동의 주민번호는 900101-1234567이고, "
        "전화번호는 010-1234-5678입니다. "
        "이메일은 hong@example.com이며, "
        "차량번호는 12가1234입니다."
    )
