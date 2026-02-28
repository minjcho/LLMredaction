from fastapi import HTTPException, UploadFile
from pypdf import PdfReader
import io


async def extract_text(file: UploadFile) -> tuple[str, str]:
    """Extract text from an uploaded TXT or PDF file.

    Returns (text, kind) where kind is "txt" or "pdf".
    """
    filename = (file.filename or "").lower()
    raw = await file.read()

    if filename.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(raw))
        pages = [page.extract_text() or "" for page in reader.pages]
        text = "\n".join(pages).strip()
        if not text:
            raise HTTPException(status_code=400, detail="PDF contains no extractable text")
        return text, "pdf"

    # Default: treat as plain text
    text = raw.decode("utf-8", errors="replace")
    return text, "txt"
