from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, Query, UploadFile

from app.config import settings
from app.detectors import ner_detector, regex_detector, llm_detector
from app.ingest import extract_text
from app.masker import encrypt_envelope, mask_text
from app.merger import merge_spans
from app.schemas import Audit, Envelope, RedactionResponse
from app.storage import store

router = APIRouter()


@router.post("/redaction/{model}", response_model=RedactionResponse)
async def redact(
    model: str,
    file: UploadFile = File(...),
    policy: str = Query("mask", description="Redaction policy"),
    store_envelope: bool = Query(True, description="Store envelope for later restore"),
    include_envelope: bool = Query(False, description="Include envelope in response"),
):
    # Validate model
    valid_models = {"regex", "ner", "gemini", "hybrid"}
    if model not in valid_models:
        raise HTTPException(status_code=400, detail=f"Invalid model. Choose from: {valid_models}")

    if model == "gemini" and not settings.ALLOW_REMOTE_LLM:
        raise HTTPException(status_code=403, detail="Remote LLM calls disabled (ALLOW_REMOTE_LLM=false)")

    # Extract text
    text, kind = await extract_text(file)

    # Detect spans
    all_spans = []
    sources_used = []

    if model in ("regex", "hybrid"):
        all_spans.extend(regex_detector.detect(text))
        sources_used.append("regex")

    if model in ("ner", "hybrid"):
        all_spans.extend(ner_detector.detect(text))
        sources_used.append("ner")

    if model in ("gemini", "hybrid"):
        if not settings.ALLOW_REMOTE_LLM:
            raise HTTPException(status_code=403, detail="Remote LLM calls disabled (ALLOW_REMOTE_LLM=false)")
        llm_spans = llm_detector.detect(text, pre_masked_spans=all_spans)
        all_spans.extend(llm_spans)
        sources_used.append("llm")

    # Merge overlapping spans
    merged = merge_spans(all_spans)

    # Mask
    masked_text, token_map = mask_text(text, merged)

    # Build audit
    audit = Audit(spans=merged, total_found=len(merged), sources_used=sources_used)

    # Build envelope
    envelope = Envelope(token_map=token_map)
    envelope_encrypted = encrypt_envelope(envelope) if store_envelope else None

    # Store
    doc_id = store(masked_text, audit, envelope_encrypted)

    return RedactionResponse(
        doc_id=doc_id,
        masked_text=masked_text,
        audit=audit,
        envelope=envelope if include_envelope else None,
    )
