from typing import List, Dict, Optional
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from loguru import logger
from ..config import settings

_embeddings = None
_vector_store = None


def get_embeddings():
    global _embeddings
    if _embeddings is None:
        logger.info(f"Loading embeddings model: {settings.embedding_model}")
        _embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)
    return _embeddings


def get_vector_store() -> Chroma:
    global _vector_store
    if _vector_store is None:
        _vector_store = Chroma(
            embedding_function=get_embeddings(),
            persist_directory=settings.chroma_dir,
        )
    return _vector_store


def add_texts(texts: List[str], metadatas: List[Dict[str, str]]):
    vs = get_vector_store()
    vs.add_texts(texts=texts, metadatas=metadatas)
    vs.persist()


def similarity_search(query: str, k: int = 5, doc_ids: Optional[List[str]] = None):
    vs = get_vector_store()
    where = {"doc_id": {"$in": doc_ids}} if doc_ids else None
    return vs.similarity_search(query, k=k, filter=where)


def similarity_search_with_scores(query: str, k: int = 5, doc_ids: Optional[List[str]] = None):
    """Return a list of (Document, score) pairs for a query.

    Score semantics are vector-store specific; for Chroma (via LangChain), this
    is typically a distance metric where lower is better. We surface it directly.
    """
    vs = get_vector_store()
    where = {"doc_id": {"$in": doc_ids}} if doc_ids else None
    return vs.similarity_search_with_score(query, k=k, filter=where)
