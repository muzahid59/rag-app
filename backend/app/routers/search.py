from fastapi import APIRouter, HTTPException
from typing import List

from ..models.schemas import QueryRequest, SearchResponse, SourceChunk
from ..stores.vector_store import similarity_search_with_scores

router = APIRouter()


def _make_snippet(text: str, max_len: int = 280) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


@router.post("")
async def search(req: QueryRequest) -> List[str]:
    if not req.query or not req.query.strip():
        raise HTTPException(status_code=400, detail="Query must not be empty")

    results = similarity_search_with_scores(req.query, k=req.topK, doc_ids=req.docIds)

    # Return only the content of each chunk
    return [doc.page_content for doc, score in results]
