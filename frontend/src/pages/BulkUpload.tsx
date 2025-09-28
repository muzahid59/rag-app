import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { bulkUpload, BulkUploadResponse, BulkUploadResult } from '../api/endpoints'

export default function BulkUpload() {
  const [directoryPath, setDirectoryPath] = useState('')
  const [result, setResult] = useState<BulkUploadResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const { mutate, isPending } = useMutation({
    mutationFn: bulkUpload,
    onSuccess: (data) => {
      setResult(data)
      setError(null)
    },
    onError: (err: any) => {
      setError(err?.response?.data?.detail || 'Bulk upload failed')
      setResult(null)
    },
  })

  function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!directoryPath.trim()) {
      setError('Please enter a directory path')
      return
    }
    mutate({ directory_path: directoryPath.trim() })
  }

  function getStatusColor(status: string) {
    switch (status) {
      case 'success': return '#28a745'
      case 'error': return '#dc3545'
      case 'skipped': return '#ffc107'
      default: return '#6c757d'
    }
  }

  function getStatusIcon(status: string) {
    switch (status) {
      case 'success': return '✅'
      case 'error': return '❌'
      case 'skipped': return '⚠️'
      default: return '❓'
    }
  }

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <h2>Bulk Upload Documents</h2>
      <p>Upload all PDF and Markdown files from a directory (including subdirectories).</p>

      <form onSubmit={onSubmit} style={{ marginBottom: '20px' }}>
        <div style={{ marginBottom: '12px' }}>
          <label htmlFor="directory" style={{ display: 'block', marginBottom: '4px', fontWeight: 'bold' }}>
            Directory Path:
          </label>
          <input
            id="directory"
            type="text"
            value={directoryPath}
            onChange={(e) => setDirectoryPath(e.target.value)}
            placeholder="/path/to/your/documents"
            style={{
              width: '100%',
              padding: '8px',
              border: '1px solid #ccc',
              borderRadius: '4px',
              fontSize: '14px'
            }}
            disabled={isPending}
          />
          <small style={{ color: '#666', fontSize: '12px' }}>
            Enter the full path to the directory containing your PDF and Markdown files
          </small>
        </div>
        
        <button
          type="submit"
          disabled={isPending || !directoryPath.trim()}
          style={{
            padding: '10px 20px',
            backgroundColor: isPending ? '#ccc' : '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: isPending ? 'not-allowed' : 'pointer',
            fontSize: '14px'
          }}
        >
          {isPending ? 'Processing...' : 'Start Bulk Upload'}
        </button>
      </form>

      {error && (
        <div style={{
          color: '#dc3545',
          backgroundColor: '#f8d7da',
          border: '1px solid #f5c6cb',
          borderRadius: '4px',
          padding: '12px',
          marginBottom: '20px'
        }}>
          {error}
        </div>
      )}

      {result && (
        <div style={{ marginTop: '20px' }}>
          <h3>Upload Results</h3>
          
          {/* Summary */}
          <div style={{
            backgroundColor: '#f8f9fa',
            border: '1px solid #dee2e6',
            borderRadius: '4px',
            padding: '16px',
            marginBottom: '20px'
          }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))', gap: '12px' }}>
              <div>
                <strong>Total Files:</strong><br />
                <span style={{ fontSize: '18px', color: '#007bff' }}>{result.total_files}</span>
              </div>
              <div>
                <strong>Successful:</strong><br />
                <span style={{ fontSize: '18px', color: '#28a745' }}>{result.successful_uploads}</span>
              </div>
              <div>
                <strong>Failed:</strong><br />
                <span style={{ fontSize: '18px', color: '#dc3545' }}>{result.failed_uploads}</span>
              </div>
              <div>
                <strong>Skipped:</strong><br />
                <span style={{ fontSize: '18px', color: '#ffc107' }}>{result.skipped_files}</span>
              </div>
            </div>
          </div>

          {/* Detailed Results */}
          {result.results.length > 0 && (
            <div>
              <h4>File Details</h4>
              <div style={{ maxHeight: '400px', overflowY: 'auto', border: '1px solid #dee2e6', borderRadius: '4px' }}>
                {result.results.map((fileResult: BulkUploadResult, index: number) => (
                  <div
                    key={index}
                    style={{
                      padding: '12px',
                      borderBottom: index < result.results.length - 1 ? '1px solid #eee' : 'none',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '12px'
                    }}
                  >
                    <span style={{ fontSize: '16px' }}>
                      {getStatusIcon(fileResult.status)}
                    </span>
                    
                    <div style={{ flex: 1 }}>
                      <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>
                        {fileResult.file_name}
                      </div>
                      
                      {fileResult.status === 'success' && (
                        <div style={{ fontSize: '12px', color: '#666' }}>
                          {fileResult.pages} pages, {fileResult.chunks} chunks
                          {fileResult.doc_id && (
                            <span style={{ marginLeft: '8px', fontFamily: 'monospace' }}>
                              ID: {fileResult.doc_id.substring(0, 8)}...
                            </span>
                          )}
                        </div>
                      )}
                      
                      {fileResult.error_message && (
                        <div style={{ fontSize: '12px', color: '#dc3545', marginTop: '4px' }}>
                          {fileResult.error_message}
                        </div>
                      )}
                    </div>
                    
                    <div style={{
                      padding: '4px 8px',
                      borderRadius: '12px',
                      fontSize: '12px',
                      fontWeight: 'bold',
                      color: 'white',
                      backgroundColor: getStatusColor(fileResult.status)
                    }}>
                      {fileResult.status.toUpperCase()}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
