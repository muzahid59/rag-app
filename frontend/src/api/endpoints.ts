import { api } from './client'

export type UploadResponse = {
  docId: string
  fileName: string
  pages: number
  chunks: number
  status: string
}

export async function uploadDocument(file: File): Promise<UploadResponse> {
  const form = new FormData()
  form.append('file', file)
  const { data } = await api.post<UploadResponse>('/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

// Keep the old function for backward compatibility
export const uploadPdf = uploadDocument

export type QueryRequest = {
  query: string
  docIds?: string[]
  topK?: number
  stream?: boolean
}

export type SourceChunk = {
  docId: string
  page: number
  score: number
}

export type QueryResponse = {
  answer: string
  sources: SourceChunk[]
  usage: { retrieved: number }
}

export type BulkUploadRequest = {
  directory_path: string
}

export type BulkUploadResult = {
  file_name: string
  doc_id?: string
  status: 'success' | 'error' | 'skipped'
  error_message?: string
  pages?: number
  chunks?: number
}

export type BulkUploadResponse = {
  total_files: number
  processed_files: number
  successful_uploads: number
  failed_uploads: number
  skipped_files: number
  results: BulkUploadResult[]
}

export async function queryRag(req: QueryRequest): Promise<QueryResponse> {
  const { data } = await api.post<QueryResponse>('/query', req)
  return data
}

export async function bulkUpload(req: BulkUploadRequest): Promise<BulkUploadResponse> {
  const { data } = await api.post<BulkUploadResponse>('/bulk-upload', req)
  return data
}
