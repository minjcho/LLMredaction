from __future__ import annotations

import time
import uuid

from app.config import settings
from app.schemas import Audit


_store: dict[str, dict] = {}


def store(masked_text: str, audit: Audit, envelope_encrypted: str | None = None) -> str:
    doc_id = uuid.uuid4().hex[:12]
    _store[doc_id] = {
        "masked_text": masked_text,
        "audit": audit,
        "envelope_encrypted": envelope_encrypted,
        "created_at": time.time(),
    }
    return doc_id


def get(doc_id: str) -> dict | None:
    entry = _store.get(doc_id)
    if entry is None:
        return None
    if time.time() - entry["created_at"] > settings.DOC_TTL_SEC:
        _store.pop(doc_id, None)
        return None
    return entry


def cleanup() -> int:
    now = time.time()
    expired = [k for k, v in _store.items() if now - v["created_at"] > settings.DOC_TTL_SEC]
    for k in expired:
        del _store[k]
    return len(expired)
