from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import PlainTextResponse, JSONResponse

from app.storage import get

router = APIRouter()


@router.get("/download/{doc_id}")
async def download(
    doc_id: str,
    format: str = Query("masked", description="'masked' or 'audit'"),
):
    entry = get(doc_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Document not found or expired")

    if format == "masked":
        return PlainTextResponse(
            content=entry["masked_text"],
            headers={"Content-Disposition": f'attachment; filename="{doc_id}_masked.txt"'},
        )
    elif format == "audit":
        return JSONResponse(
            content=entry["audit"].model_dump(),
            headers={"Content-Disposition": f'attachment; filename="{doc_id}_audit.json"'},
        )
    else:
        raise HTTPException(status_code=400, detail="format must be 'masked' or 'audit'")
