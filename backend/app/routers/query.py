from fastapi import APIRouter, HTTPException
from ..models.schemas import QueryRequest, QueryResponse, SourceChunk
from ..services.rag import answer_query

router = APIRouter()

@router.post("", response_model=QueryResponse)
async def query_rag(body: QueryRequest):
    if not body.query or not body.query.strip():
        raise HTTPException(status_code=400, detail="Query must not be empty")

    answer, sources, usage = await answer_query(body.query, top_k=body.topK, doc_ids=body.docIds)
    source_models = [SourceChunk(**s) for s in sources]
    return QueryResponse(answer=answer, sources=source_models, usage=usage)
