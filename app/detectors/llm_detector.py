from __future__ import annotations

import json
import logging

from google import genai
from google.genai import types

from app.config import settings
from app.schemas import Span

log = logging.getLogger(__name__)

_SYSTEM_PROMPT = """\
You are a PII detection engine. Given a text, find all personally identifiable information spans.
Return a JSON array of objects with these fields:
- "start": integer character offset (0-based)
- "end": integer character offset (exclusive)
- "type": PII category (e.g. PERSON, ORG, LOCATION, PHONE, EMAIL, ADDRESS, DATE_OF_BIRTH, etc.)
- "text": the exact substring from the input
- "confidence": float 0-1

Return ONLY the JSON array, no other text.
"""


def detect(text: str, pre_masked_spans: list[Span] | None = None) -> list[Span]:
    """Use Gemini API to detect PII spans in text."""
    if not settings.GEMINI_API_KEY:
        log.warning("GEMINI_API_KEY not set, skipping LLM detection")
        return []

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=text,
        config=types.GenerateContentConfig(
            system_instruction=_SYSTEM_PROMPT,
            temperature=0,
            response_mime_type="application/json",
        ),
    )

    raw = response.text or "[]"
    # Strip markdown code fences if present
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
    if raw.endswith("```"):
        raw = raw.rsplit("```", 1)[0]
    raw = raw.strip()

    try:
        items = json.loads(raw)
    except json.JSONDecodeError:
        log.error("LLM returned invalid JSON: %s", raw[:200])
        return []

    spans: list[Span] = []
    for item in items:
        start = item.get("start", 0)
        end = item.get("end", 0)
        expected_text = item.get("text", "")

        # Verify text[start:end] matches, attempt substring search if not
        if text[start:end] != expected_text and expected_text:
            idx = text.find(expected_text)
            if idx >= 0:
                start = idx
                end = idx + len(expected_text)
            else:
                log.warning("LLM span text not found in source: %s", expected_text[:50])
                continue

        spans.append(
            Span(
                start=start,
                end=end,
                type=item.get("type", "UNKNOWN"),
                text=text[start:end],
                source="llm",
                confidence=float(item.get("confidence", 0.8)),
            )
        )

    return spans
