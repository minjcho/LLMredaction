from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.routes import chat, download, redaction, restore
from app.storage import cleanup

import asyncio


async def _periodic_cleanup():
    while True:
        await asyncio.sleep(300)
        cleanup()


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(_periodic_cleanup())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(title="LLM Redaction API", version="0.1.0", lifespan=lifespan)

app.include_router(redaction.router)
app.include_router(download.router)
app.include_router(restore.router)
app.include_router(chat.router)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/")
async def serve_spa():
    return FileResponse("frontend/index.html")


app.mount("/static", StaticFiles(directory="frontend"), name="static")
