import { Link, Route, Routes, Navigate } from 'react-router-dom'
import Upload from './pages/Upload'
import BulkUpload from './pages/BulkUpload'
import Chat from './pages/Chat'

export default function App() {
  return (
    <div style={{ fontFamily: 'system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, Helvetica Neue, Arial, sans-serif' }}>
      <header style={{ padding: '12px 16px', borderBottom: '1px solid #eee', display: 'flex', gap: 16, alignItems: 'center' }}>
        <h1 style={{ margin: 0, fontSize: 18 }}>Document RAG</h1>
        <nav style={{ display: 'flex', gap: 12 }}>
          <Link to="/upload">Upload</Link>
          <Link to="/bulk-upload">Bulk Upload</Link>
          <Link to="/chat">Chat</Link>
        </nav>
      </header>
      <main style={{ padding: 16, maxWidth: 900, margin: '0 auto' }}>
        <Routes>
          <Route path="/" element={<Navigate to="/upload" replace />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/bulk-upload" element={<BulkUpload />} />
          <Route path="/chat" element={<Chat />} />
        </Routes>
      </main>
    </div>
  )
}
