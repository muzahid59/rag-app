import os
import uuid
import time
from typing import Tuple
from loguru import logger

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

from ..config import settings
from ..stores.vector_store import add_texts


def ingest_document(file_path: str, file_name: str, doc_id: str, file_ext: str) -> Tuple[int, int]:
    """Ingest a document (PDF or Markdown) into the vector store."""
    
    if file_ext.lower() == "pdf":
        loader = PyPDFLoader(file_path)
        documents = loader.load()
    elif file_ext.lower() in ["md", "markdown"]:
        loader = TextLoader(file_path, encoding='utf-8')
        documents = loader.load()
        # For markdown files, we'll treat the entire file as one "page"
        for doc in documents:
            doc.metadata["page"] = 0
    else:
        # Fallback for other text files
        loader = TextLoader(file_path, encoding='utf-8')
        documents = loader.load()
        for doc in documents:
            doc.metadata["page"] = 0

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    texts = [c.page_content for c in chunks]
    metadatas = []
    for idx, c in enumerate(chunks):
        page = c.metadata.get("page", 0)
        metadatas.append({
            "doc_id": doc_id,
            "page": page,
            "chunk_index": idx,
            "source": file_name,
            "file_type": file_ext,
        })

    logger.info(f"Adding {len(texts)} chunks for {file_ext.upper()} doc {doc_id}")
    add_texts(texts, metadatas)

    # For PDFs, calculate actual pages; for markdown, it's always 1
    if file_ext.lower() == "pdf":
        pages = max((c.metadata.get("page", 0) for c in chunks), default=-1) + 1
    else:
        pages = 1
    
    return pages, len(chunks)


# Keep the old function for backward compatibility
def ingest_pdf(file_path: str, file_name: str, doc_id: str) -> Tuple[int, int]:
    """Legacy function for PDF ingestion."""
    return ingest_document(file_path, file_name, doc_id, "pdf")
