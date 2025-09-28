from typing import List, Dict, Optional
import httpx
from ..config import settings

async def ollama_chat(messages: List[Dict[str, str]], model: Optional[str] = None) -> str:
    model = model or settings.llm_model
    url = f"{settings.ollama_base_url}/api/chat"
    payload = {"model": model, "messages": messages, "stream": False}
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(url, json=payload)
        r.raise_for_status()
        data = r.json()
        return data.get("message", {}).get("content", "")
