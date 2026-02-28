from __future__ import annotations

import re

from app.schemas import Span

# ---------- Korean RRN (주민등록번호) ----------
# Format: 6 digits - 7 digits (YYMMDD-GNNNNNN)
_RRN_RE = re.compile(r"\b(\d{6})-?([1-4]\d{6})\b")

# RRN checksum weights
_RRN_WEIGHTS = [2, 3, 4, 5, 6, 7, 8, 9, 2, 3, 4, 5]


def _valid_rrn(digits: str) -> bool:
    if len(digits) != 13 or not digits.isdigit():
        return False
    total = sum(int(d) * w for d, w in zip(digits[:12], _RRN_WEIGHTS))
    check = (11 - total % 11) % 10
    return check == int(digits[12])


# ---------- Korean BRN (사업자등록번호) ----------
# Format: 3 digits - 2 digits - 5 digits
_BRN_RE = re.compile(r"\b(\d{3})-?(\d{2})-?(\d{5})\b")
_BRN_WEIGHTS = [1, 3, 7, 1, 3, 7, 1, 3, 5]


def _valid_brn(digits: str) -> bool:
    if len(digits) != 10 or not digits.isdigit():
        return False
    total = sum(int(d) * w for d, w in zip(digits[:9], _BRN_WEIGHTS))
    total += (int(digits[8]) * 5) // 10
    check = (10 - total % 10) % 10
    return check == int(digits[9])


# ---------- Other patterns ----------
_PHONE_RE = re.compile(
    r"\b(01[016789]-?\d{3,4}-?\d{4}|0[2-6][0-9]-?\d{3,4}-?\d{4})\b"
)
_PLATE_RE = re.compile(r"\b\d{2,3}[가-힣]\s?\d{4}\b")
_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_BANK_ACCOUNT_RE = re.compile(r"\b\d{3,4}-\d{2,6}-\d{2,6}\b")
_API_KEY_RE = re.compile(
    r"(?i)\b(?:api[_-]?key|token|secret)[\"']?\s*[:=]\s*[\"']?([A-Za-z0-9_\-]{20,})[\"']?"
)

PATTERNS: list[tuple[str, re.Pattern, str | None]] = [
    ("RRN_KR", _RRN_RE, "rrn"),
    ("BRN_KR", _BRN_RE, "brn"),
    ("PHONE_KR", _PHONE_RE, None),
    ("PLATE_KR", _PLATE_RE, None),
    ("EMAIL", _EMAIL_RE, None),
    ("BANK_ACCOUNT", _BANK_ACCOUNT_RE, None),
    ("API_KEY", _API_KEY_RE, None),
]


def detect(text: str) -> list[Span]:
    spans: list[Span] = []

    for pii_type, pattern, validator in PATTERNS:
        for m in pattern.finditer(text):
            # For patterns with groups, we validate the full concatenated digits
            if validator == "rrn":
                digits = m.group(1) + m.group(2)
                if not _valid_rrn(digits):
                    continue
            elif validator == "brn":
                digits = m.group(1) + m.group(2) + m.group(3)
                if not _valid_brn(digits):
                    continue

            # For API_KEY pattern, the span is the captured key group
            if pii_type == "API_KEY" and m.lastindex and m.lastindex >= 1:
                start, end = m.start(1), m.end(1)
            else:
                start, end = m.start(), m.end()

            spans.append(
                Span(
                    start=start,
                    end=end,
                    type=pii_type,
                    text=text[start:end],
                    source="regex",
                    confidence=1.0,
                )
            )

    return spans
