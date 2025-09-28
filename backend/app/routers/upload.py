from fastapi import APIRouter, UploadFile, File, HTTPException
from loguru import logger
import os
import time
import uuid

from ..config import settings
from ..models.schemas import UploadResponse
from ..stores.doc_store import store
from ..services.ingestion import ingest_document

router = APIRouter()

ALLOWED_CONTENT_TYPES = {"application/pdf", "text/markdown", "text/plain"}

@router.post("")
async def upload_document(file: UploadFile = File(...)) -> UploadResponse:
    file_ext = file.filename.lower().split('.')[-1] if file.filename else ""
    allowed_extensions = {"pdf", "md", "markdown"}
    
    if file.content_type not in ALLOWED_CONTENT_TYPES and file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Only PDF and Markdown files are allowed")

    file_bytes = await file.read()
    max_bytes = settings.max_upload_mb * 1024 * 1024
    if len(file_bytes) > max_bytes:
        raise HTTPException(status_code=400, detail=f"File too large. Max {settings.max_upload_mb}MB")

    doc_id = str(uuid.uuid4())
    file_name = file.filename
    file_ext = file.filename.lower().split('.')[-1] if file.filename else "txt"
    save_path = os.path.join(settings.documents_dir, f"{doc_id}.{file_ext}")
    with open(save_path, "wb") as f:
        f.write(file_bytes)

    try:
        pages, chunks = ingest_document(save_path, file_name, doc_id, file_ext)
        meta = {
            "docId": doc_id,
            "fileName": file_name,
            "filePath": save_path,
            "sizeBytes": len(file_bytes),
            "pages": pages,
            "chunks": chunks,
            "status": "ready",
            "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        store.upsert(meta)
        return UploadResponse(docId=doc_id, fileName=file_name, pages=pages, chunks=chunks, status="ready")
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Failed to ingest PDF")
