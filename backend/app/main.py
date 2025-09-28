from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import os

from .config import settings
from .routers.upload import router as upload_router
from .routers.query import router as query_router
from .routers.bulk_upload import router as bulk_upload_router

app = FastAPI(title="PDF RAG API", version="0.1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure storage directories exist
for path in [settings.documents_dir, settings.chroma_dir, settings.meta_dir]:
    os.makedirs(path, exist_ok=True)

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "models": {
            "embedding": settings.embedding_model,
            "llm": settings.llm_model,
        },
        "storage": {
            "documents_dir": settings.documents_dir,
            "chroma_dir": settings.chroma_dir,
            "meta_dir": settings.meta_dir,
        },
    }

app.include_router(upload_router, prefix="/upload", tags=["upload"])
app.include_router(bulk_upload_router, prefix="/bulk-upload", tags=["bulk-upload"])
app.include_router(query_router, prefix="/query", tags=["query"])
