from fastapi import APIRouter, HTTPException
from loguru import logger
import os
import time
import uuid
from typing import List
from pathlib import Path

from ..config import settings
from ..models.schemas import BulkUploadRequest, BulkUploadResponse, BulkUploadResult
from ..stores.doc_store import store
from ..services.ingestion import ingest_document

router = APIRouter()

ALLOWED_EXTENSIONS = {".pdf", ".md", ".markdown"}

def is_valid_file(file_path: Path) -> bool:
    """Check if file has a valid extension for processing."""
    return file_path.suffix.lower() in ALLOWED_EXTENSIONS

def get_files_from_directory(directory_path: str) -> List[Path]:
    """Get all valid files from directory and subdirectories."""
    directory = Path(directory_path)
    if not directory.exists():
        raise HTTPException(status_code=400, detail=f"Directory does not exist: {directory_path}")
    
    if not directory.is_dir():
        raise HTTPException(status_code=400, detail=f"Path is not a directory: {directory_path}")
    
    valid_files = []
    for file_path in directory.rglob("*"):
        if file_path.is_file() and is_valid_file(file_path):
            valid_files.append(file_path)
    
    return valid_files

@router.post("")
async def bulk_upload(request: BulkUploadRequest) -> BulkUploadResponse:
    """Upload all PDF and Markdown files from a directory."""
    logger.info(f"Starting bulk upload from directory: {request.directory_path}")
    
    try:
        files = get_files_from_directory(request.directory_path)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scanning directory: {str(e)}")
    
    if not files:
        return BulkUploadResponse(
            total_files=0,
            processed_files=0,
            successful_uploads=0,
            failed_uploads=0,
            skipped_files=0,
            results=[]
        )
    
    results = []
    successful_uploads = 0
    failed_uploads = 0
    skipped_files = 0
    
    for file_path in files:
        result = BulkUploadResult(file_name=file_path.name, status="processing")
        
        try:
            # Check file size
            file_size = file_path.stat().st_size
            max_bytes = settings.max_upload_mb * 1024 * 1024
            
            if file_size > max_bytes:
                result.status = "skipped"
                result.error_message = f"File too large. Max {settings.max_upload_mb}MB"
                skipped_files += 1
                results.append(result)
                continue
            
            # Check if file already exists (by name)
            existing_docs = store.list()
            if any(doc.get("fileName") == file_path.name for doc in existing_docs):
                result.status = "skipped"
                result.error_message = "File with same name already exists"
                skipped_files += 1
                results.append(result)
                continue
            
            # Process the file
            doc_id = str(uuid.uuid4())
            file_ext = file_path.suffix[1:].lower()  # Remove the dot
            
            # Copy file to documents directory
            dest_path = os.path.join(settings.documents_dir, f"{doc_id}.{file_ext}")
            with open(file_path, "rb") as src, open(dest_path, "wb") as dst:
                dst.write(src.read())
            
            # Ingest the document
            pages, chunks = ingest_document(dest_path, file_path.name, doc_id, file_ext)
            
            # Store metadata
            meta = {
                "docId": doc_id,
                "fileName": file_path.name,
                "filePath": dest_path,
                "sizeBytes": file_size,
                "pages": pages,
                "chunks": chunks,
                "status": "ready",
                "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
            store.upsert(meta)
            
            result.doc_id = doc_id
            result.status = "success"
            result.pages = pages
            result.chunks = chunks
            successful_uploads += 1
            
            logger.info(f"Successfully processed {file_path.name}: {chunks} chunks, {pages} pages")
            
        except Exception as e:
            logger.error(f"Error processing {file_path.name}: {str(e)}")
            result.status = "error"
            result.error_message = str(e)
            failed_uploads += 1
            
            # Clean up partial files if they exist
            try:
                if result.doc_id:
                    dest_path = os.path.join(settings.documents_dir, f"{result.doc_id}.{file_ext}")
                    if os.path.exists(dest_path):
                        os.remove(dest_path)
            except:
                pass
        
        results.append(result)
    
    response = BulkUploadResponse(
        total_files=len(files),
        processed_files=len(results),
        successful_uploads=successful_uploads,
        failed_uploads=failed_uploads,
        skipped_files=skipped_files,
        results=results
    )
    
    logger.info(f"Bulk upload completed: {successful_uploads} successful, {failed_uploads} failed, {skipped_files} skipped")
    return response
