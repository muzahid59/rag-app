from pydantic import BaseModel
from typing import List, Optional, Dict

class UploadResponse(BaseModel):
    docId: str
    fileName: str
    pages: int
    chunks: int
    status: str = "ready"

class DocumentMeta(BaseModel):
    docId: str
    fileName: str
    filePath: str
    sizeBytes: int
    pages: int
    chunks: int
    status: str
    createdAt: str

class QueryRequest(BaseModel):
    query: str
    docIds: Optional[List[str]] = None
    topK: int = 5
    stream: bool = False

class SourceChunk(BaseModel):
    docId: str
    page: int
    score: float
    snippet: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]
    usage: Dict[str, int]


class SearchResponse(BaseModel):
    results: List[SourceChunk]
    usage: Dict[str, int]


class BulkUploadRequest(BaseModel):
    directory_path: str


class BulkUploadResult(BaseModel):
    file_name: str
    doc_id: Optional[str] = None
    status: str  # "success", "error", "skipped"
    error_message: Optional[str] = None
    pages: Optional[int] = None
    chunks: Optional[int] = None


class BulkUploadResponse(BaseModel):
    total_files: int
    processed_files: int
    successful_uploads: int
    failed_uploads: int
    skipped_files: int
    results: List[BulkUploadResult]
