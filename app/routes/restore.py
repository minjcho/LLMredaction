from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException

from app.config import settings
from app.masker import decrypt_envelope, restore_text
from app.schemas import RestoreResponse
from app.storage import get

router = APIRouter()


@router.post("/restore/{doc_id}", response_model=RestoreResponse)
async def restore(
    doc_id: str,
    x_admin_key: str = Header(..., alias="X-ADMIN-KEY"),
):
    if x_admin_key != settings.ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Invalid admin key")

    entry = get(doc_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Document not found or expired")

    if not entry.get("envelope_encrypted"):
        raise HTTPException(status_code=400, detail="No envelope stored for this document")

    envelope = decrypt_envelope(entry["envelope_encrypted"])
    restored = restore_text(entry["masked_text"], envelope.token_map)

    return RestoreResponse(doc_id=doc_id, restored_text=restored)
