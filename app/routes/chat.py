from __future__ import annotations

from fastapi import APIRouter, HTTPException

from google import genai
from google.genai import types

from app.config import settings
from app.schemas import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not settings.GEMINI_API_KEY:
        raise HTTPException(status_code=503, detail="GEMINI_API_KEY not configured")

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    # Build conversation contents
    contents: list[types.Content] = []
    for msg in req.history:
        role = "user" if msg.get("role") == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part(text=msg["content"])]))
    contents.append(types.Content(role="user", parts=[types.Part(text=req.message)]))

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
    )

    return ChatResponse(reply=response.text or "")
