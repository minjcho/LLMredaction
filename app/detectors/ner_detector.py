from __future__ import annotations

from app.schemas import Span


def detect(text: str) -> list[Span]:
    """Stub NER detector. Returns empty list.

    Replace with a HuggingFace NER model (e.g., klue/bert-base) in the future.
    """
    return []
