import json
import os
import time
from typing import Dict, List, Optional
from loguru import logger

from ..config import settings

META_PATH = os.path.join(settings.meta_dir, "docs.json")

class DocStore:
    def __init__(self, path: str = META_PATH):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump({"documents": {}}, f)

    def _read(self) -> Dict:
        with open(self.path, "r") as f:
            return json.load(f)

    def _write(self, data: Dict):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def upsert(self, meta: Dict):
        data = self._read()
        data["documents"][meta["docId"]] = meta
        self._write(data)

    def get(self, doc_id: str) -> Optional[Dict]:
        return self._read()["documents"].get(doc_id)

    def list(self) -> List[Dict]:
        return list(self._read()["documents"].values())

    def delete(self, doc_id: str):
        data = self._read()
        if doc_id in data["documents"]:
            del data["documents"][doc_id]
            self._write(data)

store = DocStore()
