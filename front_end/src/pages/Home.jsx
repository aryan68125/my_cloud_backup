import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import client from '../api/client'

export default function Home() {
  const [user, setUser] = useState(null)
  const [helloMsg, setHelloMsg] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    client.get('/user/me').then((res) => setUser(res.data))
  }, [])

  function displayName() {
    const p = user?.profile
    if (p?.first_name && p?.last_name) return `${p.first_name} ${p.last_name}`
    return user?.email ?? ''
  }

  async function handleHello() {
    const res = await client.get('/hello')
    setHelloMsg(res.data.message)
  }

  async function handleLogout() {
    await client.post('/auth/logout')
    navigate('/login')
  }

  if (!user) return <p style={{ fontFamily: 'sans-serif', padding: 40 }}>Loading…</p>

  return (
    <div style={{ maxWidth: 600, margin: '80px auto', fontFamily: 'sans-serif' }}>
      <h2>Welcome, {displayName()}</h2>
      <p style={{ color: '#555' }}>Signed in as {user.email}</p>

      <div style={{ marginTop: 24 }}>
        <button onClick={handleHello} style={{ padding: '10px 20px', marginRight: 12 }}>
          Say Hello
        </button>
        {helloMsg && <span style={{ fontWeight: 'bold', color: '#333' }}>{helloMsg}</span>}
      </div>

      <div style={{ marginTop: 32 }}>
        <button
          onClick={handleLogout}
          style={{ padding: '8px 16px', color: 'red', background: 'none', border: '1px solid red', cursor: 'pointer' }}
        >
          Log Out
        </button>
      </div>
    </div>
  )
}
