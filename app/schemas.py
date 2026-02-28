from __future__ import annotations

from pydantic import BaseModel


class Span(BaseModel):
    start: int
    end: int
    type: str
    text: str
    source: str  # "regex" | "ner" | "llm"
    confidence: float = 1.0


class Audit(BaseModel):
    spans: list[Span]
    total_found: int
    sources_used: list[str]


class Envelope(BaseModel):
    token_map: dict[str, str]  # token_id -> original text


class RedactionResponse(BaseModel):
    doc_id: str
    masked_text: str
    audit: Audit
    envelope: Envelope | None = None


class RestoreRequest(BaseModel):
    envelope_encrypted: str | None = None


class RestoreResponse(BaseModel):
    doc_id: str
    restored_text: str


class ChatRequest(BaseModel):
    message: str
    history: list[dict[str, str]] = []


class ChatResponse(BaseModel):
    reply: str
