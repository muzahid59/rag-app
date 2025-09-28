# Document Search & Q&A (RAG) App

This is a full-stack app to upload documents (PDFs and Markdown files) and query them using Retrieval-Augmented Generation (RAG).

## Stack
- Frontend: React (Vite + TypeScript)
- Backend: FastAPI
- Embeddings: HuggingFace `sentence-transformers/all-MiniLM-L6-v2`
- Vector DB: Chroma
- LLM: Ollama (local) using `llama3.2` by default

## Prerequisites
- Python 3.9+
- Node 18+
- Ollama running locally (`brew install ollama && ollama serve`) and pull a model:
  ```bash
  ollama pull llama3.2
  ```

## Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8001
```

Health check: http://localhost:8001/health

## Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Visit: http://localhost:5173

## Project Structure
```
backend/
  app/
    main.py
    config.py
    models/
      schemas.py
    routers/
      upload.py
      query.py
    services/
      ingestion.py
      rag.py
    stores/
      doc_store.py
      vector_store.py
    utils/
      llm.py
  requirements.txt
  .env.example
frontend/
  src/
    pages/
      Upload.tsx
      Chat.tsx
    api/
      client.ts
      endpoints.ts
    App.tsx
    main.tsx
  package.json
  vite.config.ts
  tsconfig.json
  .env.example
storage/
  documents/
  chroma/
  meta/
```

## Usage
1. **Upload**: Go to `/upload`, select a PDF or Markdown file, and click Upload. The system will process it into chunks and store embeddings.
2. **Bulk Upload**: Go to `/bulk-upload`, enter a directory path, and upload all PDF and Markdown files from that directory (including subdirectories) at once.
3. **Chat**: Go to `/chat`, enter a question about your uploaded documents, and get AI-generated answers with source citations.

## API Endpoints
- `GET /health` - Health check
- `POST /upload` - Upload document (PDF or Markdown, multipart form field `file`)
- `POST /bulk-upload` - Bulk upload documents from directory with `{ directory_path }`
- `POST /query` - Query documents with `{ query, docIds?, topK? }`

## Notes
- Documents and embeddings are stored under `storage/`.
- The system uses 500-character chunks with 50-character overlap.
- Supports querying across all documents or filtering by specific document IDs.
- Returns answers with source citations including page numbers and snippets.
- Bulk upload scans directories recursively and skips files that already exist (by filename).
- Bulk upload provides detailed progress tracking with success/error/skip status for each file.

## Next Steps
- Add document management (list/delete endpoints)
- Implement streaming answers (SSE)
- Add authentication and multi-user support
