import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { uploadDocument, UploadResponse } from '../api/endpoints'

export default function Upload() {
  const [file, setFile] = useState<File | null>(null)
  const [result, setResult] = useState<UploadResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const { mutate, isPending } = useMutation({
    mutationFn: uploadDocument,
    onSuccess: (data) => {
      setResult(data)
      setError(null)
    },
    onError: (err: any) => {
      setError(err?.response?.data?.detail || 'Upload failed')
      setResult(null)
    },
  })

  function onSelect(e: React.ChangeEvent<HTMLInputElement>) {
    const f = e.target.files?.[0]
    if (!f) return
    const fileName = f.name.toLowerCase()
    const allowedExtensions = ['.pdf', '.md', '.markdown']
    const isValidFile = allowedExtensions.some(ext => fileName.endsWith(ext))
    
    if (!isValidFile) {
      setError('Please select a PDF or Markdown file')
      return
    }
    setError(null)
    setFile(f)
  }

  function onUpload() {
    if (!file) return
    mutate(file)
  }

  return (
    <div>
      <h2>Upload a Document</h2>
      <p>Select a PDF or Markdown file to ingest into the knowledge base.</p>

      <input type="file" accept="application/pdf,.pdf,.md,.markdown,text/markdown" onChange={onSelect} />
      <div style={{ marginTop: 12, display: 'flex', gap: 8 }}>
        <button onClick={onUpload} disabled={!file || isPending}>
          {isPending ? 'Uploading…' : 'Upload'}
        </button>
        {file && <span>{file.name} ({Math.round(file.size/1024)} KB)</span>}
      </div>

      {error && (
        <div style={{ color: 'crimson', marginTop: 12 }}>{error}</div>
      )}

      {result && (
        <div style={{ marginTop: 16, padding: 12, border: '1px solid #eee', borderRadius: 6 }}>
          <div><strong>Document ID:</strong> {result.docId}</div>
          <div><strong>File Name:</strong> {result.fileName}</div>
          <div><strong>Pages:</strong> {result.pages}</div>
          <div><strong>Chunks:</strong> {result.chunks}</div>
          <div><strong>Status:</strong> {result.status}</div>
        </div>
      )}
    </div>
  )
}
