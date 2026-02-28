from __future__ import annotations

from app.schemas import Span

SOURCE_PRIORITY = {"regex": 0, "ner": 1, "llm": 2}

TYPE_SENSITIVITY = {
    "RRN_KR": 0,
    "BRN_KR": 1,
    "PHONE_KR": 2,
    "EMAIL": 3,
    "API_KEY": 4,
    "SECRET": 4,
    "BANK_ACCOUNT": 5,
    "PLATE_KR": 6,
    "PERSON": 7,
    "ORG": 8,
    "LOCATION": 9,
}


def _span_sort_key(span: Span) -> tuple:
    return (
        SOURCE_PRIORITY.get(span.source, 99),
        TYPE_SENSITIVITY.get(span.type, 99),
        -(span.end - span.start),
        -span.confidence,
    )


def merge_spans(spans: list[Span]) -> list[Span]:
    """Merge overlapping spans, keeping the higher-priority one."""
    if not spans:
        return []

    sorted_spans = sorted(spans, key=_span_sort_key)
    merged: list[Span] = []

    for candidate in sorted_spans:
        overlaps = False
        for existing in merged:
            if candidate.start < existing.end and candidate.end > existing.start:
                overlaps = True
                break
        if not overlaps:
            merged.append(candidate)

    merged.sort(key=lambda s: s.start)
    return merged
