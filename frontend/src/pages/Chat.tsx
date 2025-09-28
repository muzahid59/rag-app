import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { queryRag, QueryResponse } from '../api/endpoints'

function SourceItem({ s }: { s: QueryResponse['sources'][number] }) {
  return (
    <div style={{ border: '1px solid #eee', borderRadius: 6, padding: 8 }}>
      <div style={{ fontSize: 12, color: '#666' }}>
        Doc: {s.docId} • Page {s.page} • Score {s.score.toFixed(2)}
      </div>
      <div style={{ marginTop: 4, whiteSpace: 'pre-wrap' }}>{s.snippet}</div>
    </div>
  )
}

export default function Chat() {
  const [query, setQuery] = useState('Explain reinforcement learning')
  const [response, setResponse] = useState<QueryResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const { mutate, isPending } = useMutation({
    mutationFn: queryRag,
    onSuccess: (data) => {
      setResponse(data)
      setError(null)
    },
    onError: (err: any) => {
      setError(err?.response?.data?.detail || 'Query failed')
      setResponse(null)
    },
  })

  function onAsk() {
    const q = query.trim()
    if (!q) return
    mutate({ query: q, topK: 5 })
  }

  return (
    <div>
      <h2>Chat / Ask a question</h2>
      <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask about your PDFs..."
          style={{ flex: 1, padding: '8px 10px', borderRadius: 6, border: '1px solid #ccc' }}
        />
        <button onClick={onAsk} disabled={isPending}>
          {isPending ? 'Asking…' : 'Ask'}
        </button>
      </div>

      {error && <div style={{ color: 'crimson', marginTop: 12 }}>{error}</div>}

      {response && (
        <div style={{ marginTop: 16 }}>
          <h3>Answer</h3>
          <div style={{ padding: 12, border: '1px solid #eee', borderRadius: 6, whiteSpace: 'pre-wrap' }}>
            {response.answer}
          </div>
          <h3 style={{ marginTop: 16 }}>Sources</h3>
          <div style={{ display: 'grid', gap: 8 }}>
            {response.sources.map((s, i) => (
              <SourceItem key={i} s={s} />
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
