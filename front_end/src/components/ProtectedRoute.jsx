import { useEffect, useState } from 'react'
import { Navigate } from 'react-router-dom'
import client from '../api/client'

export default function ProtectedRoute({ children }) {
  const [status, setStatus] = useState('checking') // 'checking' | 'ok' | 'redirect'

  useEffect(() => {
    client
      .get('/user/me')
      .then(() => setStatus('ok'))
      .catch(() => setStatus('redirect'))
  }, [])

  if (status === 'checking') return null
  if (status === 'redirect') return <Navigate to="/login" replace />
  return children
}
