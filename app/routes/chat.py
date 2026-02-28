from __future__ import annotations

from fastapi import APIRouter, HTTPException

from google import genai
from google.genai import types

from app.config import settings
from app.masker import decrypt_envelope, restore_text
from app.schemas import ChatRequest, ChatResponse
from app.storage import get as get_doc

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not settings.GEMINI_API_KEY:
        raise HTTPException(status_code=503, detail="GEMINI_API_KEY not configured")

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    # Build system instruction from masked document if doc_id is provided
    config = None
    if req.doc_id:
        doc = get_doc(req.doc_id)
        if doc:
            system_instruction = (
                "아래는 PII가 마스킹된 문서입니다. "
                "질문에 답변할 때 마스킹된 토큰(예: [[PII:TYPE:id]])을 그대로 포함하여 답변하세요. "
                "토큰은 나중에 자동으로 원래 값으로 복원됩니다.\n\n"
                f"{doc['masked_text']}"
            )
            config = types.GenerateContentConfig(system_instruction=system_instruction)

    # Build conversation contents
    contents: list[types.Content] = []
    for msg in req.history:
        role = "user" if msg.get("role") == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part(text=msg["content"])]))
    contents.append(types.Content(role="user", parts=[types.Part(text=req.message)]))

    kwargs = dict(model="gemini-3.1-pro-preview", contents=contents)
    if config:
        kwargs["config"] = config

    response = client.models.generate_content(**kwargs)

    reply = response.text or ""
    reply_masked = None

    # Restore masked tokens in LLM response using the encrypted token map
    if req.doc_id:
        doc = get_doc(req.doc_id)
        if doc and doc.get("envelope_encrypted"):
            envelope = decrypt_envelope(doc["envelope_encrypted"])
            reply_masked = reply
            reply = restore_text(reply, envelope.token_map)

    return ChatResponse(reply=reply, reply_masked=reply_masked)
