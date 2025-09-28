from pydantic_settings import BaseSettings
from pydantic import Field
import os

class Settings(BaseSettings):
    embedding_model: str = Field(default="sentence-transformers/all-MiniLM-L6-v2")
    llm_model: str = Field(default="llama3.2")
    ollama_base_url: str = Field(default="http://localhost:11434")

    storage_root: str = Field(default=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "storage")))

    @property
    def pdf_dir(self) -> str:
        return os.path.join(self.storage_root, "documents")
    
    @property
    def documents_dir(self) -> str:
        return os.path.join(self.storage_root, "documents")

    @property
    def chroma_dir(self) -> str:
        return os.path.join(self.storage_root, "chroma")

    @property
    def meta_dir(self) -> str:
        return os.path.join(self.storage_root, "meta")

    cors_allow_origins: list[str] = Field(default_factory=lambda: [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ])

    max_upload_mb: int = Field(default=50)

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
