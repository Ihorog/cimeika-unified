'use client'
import { useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import { useRouter } from 'next/navigation'

export default function AuthPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [mode, setMode] = useState<'login'|'register'>('login')
  const [msg, setMsg] = useState('')
  const [loading, setLoading] = useState(false)
  const router = useRouter()
  const sb = createClient()

  async function handle() {
    setLoading(true)
    setMsg('')
    if (mode === 'login') {
      const { error } = await sb.auth.signInWithPassword({ email, password })
      if (error) setMsg(error.message)
      else router.push('/ci')
    } else {
      const { error } = await sb.auth.signUp({ email, password })
      if (error) setMsg(error.message)
      else setMsg('Перевір пошту — посилання для підтвердження надіслано.')
    }
    setLoading(false)
  }

  return (
    <main style={{
      minHeight: '100dvh', display: 'flex', alignItems: 'center', justifyContent: 'center',
      background: '#080910', fontFamily: 'Onest, sans-serif', color: '#DDE0EA'
    }}>
      <div style={{
        width: 360, padding: 40, background: '#0F1018',
        border: '1px solid #1F2333', borderRadius: 16
      }}>
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <img src="https://raw.githubusercontent.com/Ihorog/media/main/Ci.png"
               alt="Ci" style={{ width: 56, marginBottom: 12 }} />
          <h1 style={{ fontSize: 22, color: '#C8A84B', fontFamily: 'Cormorant Garamond, serif' }}>
            Cimeika
          </h1>
          <p style={{ color: '#5A6077', fontSize: 13, marginTop: 4 }}>
            {mode === 'login' ? 'Вхід у простір' : 'Реєстрація'}
          </p>
        </div>

        <input
          type="email" placeholder="Email"
          value={email} onChange={e => setEmail(e.target.value)}
          style={inputStyle}
        />
        <input
          type="password" placeholder="Пароль"
          value={password} onChange={e => setPassword(e.target.value)}
          style={{...inputStyle, marginTop: 12}}
          onKeyDown={e => e.key === 'Enter' && handle()}
        />

        {msg && (
          <p style={{ marginTop: 12, fontSize: 13, color: '#D44A4A', textAlign: 'center' }}>
            {msg}
          </p>
        )}

        <button onClick={handle} disabled={loading} style={btnStyle}>
          {loading ? '...' : mode === 'login' ? 'Увійти' : 'Зареєструватись'}
        </button>

        <p style={{ textAlign: 'center', marginTop: 20, fontSize: 13, color: '#5A6077' }}>
          {mode === 'login' ? 'Немає акаунту? ' : 'Вже є акаунт? '}
          <span
            onClick={() => setMode(mode === 'login' ? 'register' : 'login')}
            style={{ color: '#C8A84B', cursor: 'pointer' }}
          >
            {mode === 'login' ? 'Реєстрація' : 'Вхід'}
          </span>
        </p>
      </div>
    </main>
  )
}

const inputStyle: React.CSSProperties = {
  width: '100%', padding: '12px 16px',
  background: '#161922', border: '1px solid #1F2333', borderRadius: 8,
  color: '#DDE0EA', fontSize: 14, outline: 'none', boxSizing: 'border-box'
}
const btnStyle: React.CSSProperties = {
  width: '100%', marginTop: 20, padding: '13px 0',
  background: '#C8A84B', color: '#080910', border: 'none',
  borderRadius: 8, fontSize: 15, fontWeight: 600, cursor: 'pointer'
}