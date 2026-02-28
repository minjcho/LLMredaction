from __future__ import annotations

import re
import uuid

from cryptography.fernet import Fernet

from app.config import settings
from app.schemas import Envelope, Span

# Auto-generate a Fernet key if not configured
_fernet_key: bytes = (
    settings.FERNET_KEY.encode()
    if settings.FERNET_KEY
    else Fernet.generate_key()
)


def _get_fernet() -> Fernet:
    return Fernet(_fernet_key)


def mask_text(text: str, spans: list[Span]) -> tuple[str, dict[str, str]]:
    """Replace detected spans with tokens, returning masked text and token_map.

    Processes spans in reverse order to preserve indices.
    """
    token_map: dict[str, str] = {}
    sorted_spans = sorted(spans, key=lambda s: s.start, reverse=True)

    for span in sorted_spans:
        token_id = uuid.uuid4().hex[:8]
        token = f"[[PII:{span.type}:{token_id}]]"
        token_map[token_id] = span.text
        text = text[: span.start] + token + text[span.end :]

    return text, token_map


def restore_text(masked_text: str, token_map: dict[str, str]) -> str:
    """Restore original text by replacing tokens with their original values."""
    result = masked_text
    for token_id, original in token_map.items():
        pattern = rf"\[\[PII:[A-Z_]+:{re.escape(token_id)}\]\]"
        result = re.sub(pattern, original, result)
    return result


def encrypt_envelope(envelope: Envelope) -> str:
    return _get_fernet().encrypt(envelope.model_dump_json().encode()).decode()


def decrypt_envelope(encrypted: str) -> Envelope:
    raw = _get_fernet().decrypt(encrypted.encode())
    return Envelope.model_validate_json(raw)
