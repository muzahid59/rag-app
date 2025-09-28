from typing import List, Dict, Optional
from ..stores.vector_store import similarity_search
from ..config import settings
from ..utils.llm import ollama_chat

SYSTEM_PROMPT = (
    "You are a helpful assistant. Use only the provided context to answer. "
    "If the answer is not in the context, say you don't know. Cite sources with page numbers."
)


def build_prompt(context_snippets: List[str], question: str) -> list[dict]:
    context = "\n\n".join(context_snippets)
    user = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user},
    ]


async def answer_query(query: str, top_k: int = 5, doc_ids: Optional[List[str]] = None):
    results = similarity_search(query, k=top_k, doc_ids=doc_ids)
    snippets = [r.page_content for r in results]

    msgs = build_prompt(snippets, query)
    answer = await ollama_chat(msgs)

    sources = []
    for r in results:
        md = r.metadata or {}
        sources.append({
            "docId": md.get("doc_id", ""),
            "page": int(md.get("page", 0)),
            "score": float(md.get("score", 0.0)) if "score" in md else 0.0,
            "snippet": r.page_content[:300],
        })

    return answer, sources, {"retrieved": len(results)}
