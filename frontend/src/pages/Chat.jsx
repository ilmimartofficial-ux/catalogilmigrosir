import { useState, useRef, useEffect } from 'react'
import { sendChat } from '../api/client'
import { Send, Bot, User, Loader, RefreshCw } from 'lucide-react'

const QUICK_QUESTIONS = [
  '🛒 Ada produk snack apa saja?',
  '💰 Berapa harga grosir minyak goreng?',
  '📦 Minimum order grosir berapa?',
  '🚀 Ada promo produk hari ini?',
  '☕ Ada kopi sachet apa saja?',
  '🧴 Produk sabun merk apa yang ada?',
]

export default function Chat() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: '👋 Halo! Saya asisten AI **ILMIGROSIR**.\n\nSaya bisa membantu Anda:\n• Cari produk & cek harga\n• Info harga grosir\n• Rekomendasi produk\n\nSilakan tanya apa saja! 😊'
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const send = async (text) => {
    const msg = text || input.trim()
    if (!msg || loading) return

    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: msg }])
    setLoading(true)

    try {
      const history = messages.slice(-10)
      const r = await sendChat(msg, history)
      setMessages(prev => [...prev, { role: 'assistant', content: r.data.reply }])
    } catch {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: '❌ Maaf, terjadi gangguan. Silakan hubungi WhatsApp kami di 085373373233 🙏'
      }])
    } finally {
      setLoading(false)
      inputRef.current?.focus()
    }
  }

  const reset = () => {
    setMessages([{
      role: 'assistant',
      content: '👋 Chat baru dimulai! Ada yang bisa saya bantu? 😊'
    }])
    setInput('')
  }

  return (
    <div style={{
      display: 'flex', flexDirection: 'column',
      height: 'calc(100vh - var(--nav-height) - var(--bottom-nav))',
      background: 'var(--gray-50)'
    }}>
      {/* Header */}
      <div style={{
        background: 'white',
        borderBottom: '2px solid var(--yellow)',
        padding: '12px 16px',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div style={{
            width: 40, height: 40, borderRadius: '50%',
            background: 'linear-gradient(135deg, var(--blue), var(--blue-dark))',
            display: 'flex', alignItems: 'center', justifyContent: 'center'
          }}>
            <Bot size={20} color="white" />
          </div>
          <div>
            <div style={{ fontWeight: 900, fontSize: 15 }}>AI Assistant ILMIGROSIR</div>
            <div style={{ fontSize: 11, color: '#25D366', fontWeight: 700, display: 'flex', alignItems: 'center', gap: 4 }}>
              <span style={{ width: 7, height: 7, borderRadius: '50%', background: '#25D366', display: 'inline-block' }} />
              Online — Akses Database Real-time
            </div>
          </div>
        </div>
        <button
          onClick={reset}
          style={{ background: 'none', color: 'var(--gray-500)', display: 'flex', alignItems: 'center', gap: 4, fontSize: 12, fontWeight: 700 }}
        >
          <RefreshCw size={14} /> Reset
        </button>
      </div>

      {/* Messages */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '16px', display: 'flex', flexDirection: 'column', gap: 12 }}>
        {messages.map((msg, i) => (
          <div key={i} style={{
            display: 'flex',
            justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
            gap: 8, alignItems: 'flex-end',
            animation: 'fadeIn 0.3s ease'
          }}>
            {msg.role === 'assistant' && (
              <div style={{
                width: 30, height: 30, borderRadius: '50%', flexShrink: 0,
                background: 'linear-gradient(135deg, var(--blue), var(--blue-dark))',
                display: 'flex', alignItems: 'center', justifyContent: 'center'
              }}>
                <Bot size={16} color="white" />
              </div>
            )}

            <div style={{
              maxWidth: '78%',
              padding: '10px 14px',
              borderRadius: msg.role === 'user'
                ? '18px 18px 4px 18px'
                : '18px 18px 18px 4px',
              background: msg.role === 'user'
                ? 'var(--red)'
                : 'white',
              color: msg.role === 'user' ? 'white' : 'var(--gray-900)',
              fontSize: 14, lineHeight: 1.55,
              fontWeight: 600,
              boxShadow: 'var(--shadow-sm)',
              whiteSpace: 'pre-wrap',
              wordBreak: 'break-word'
            }}>
              {formatMessage(msg.content)}
            </div>

            {msg.role === 'user' && (
              <div style={{
                width: 30, height: 30, borderRadius: '50%', flexShrink: 0,
                background: 'var(--yellow)',
                display: 'flex', alignItems: 'center', justifyContent: 'center'
              }}>
                <User size={16} color="var(--gray-900)" />
              </div>
            )}
          </div>
        ))}

        {/* Typing indicator */}
        {loading && (
          <div style={{ display: 'flex', gap: 8, alignItems: 'flex-end' }}>
            <div style={{
              width: 30, height: 30, borderRadius: '50%',
              background: 'linear-gradient(135deg, var(--blue), var(--blue-dark))',
              display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0
            }}>
              <Bot size={16} color="white" />
            </div>
            <div style={{
              background: 'white', padding: '12px 16px', borderRadius: '18px 18px 18px 4px',
              boxShadow: 'var(--shadow-sm)', display: 'flex', gap: 4, alignItems: 'center'
            }}>
              {[0, 0.2, 0.4].map((delay, i) => (
                <span key={i} style={{
                  width: 8, height: 8, borderRadius: '50%',
                  background: 'var(--gray-300)',
                  animation: `pulse 1.2s ${delay}s infinite`
                }} />
              ))}
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Quick questions (only at start) */}
      {messages.length <= 1 && (
        <div style={{
          padding: '8px 12px',
          display: 'flex', gap: 8, overflowX: 'auto',
          borderTop: '1px solid var(--gray-100)'
        }}>
          {QUICK_QUESTIONS.map(q => (
            <button
              key={q}
              onClick={() => send(q)}
              style={{
                flexShrink: 0, padding: '7px 12px',
                borderRadius: 99, border: '2px solid var(--blue-light)',
                background: 'var(--blue-light)', color: 'var(--blue-dark)',
                fontSize: 12, fontWeight: 700, cursor: 'pointer',
                transition: 'all 0.15s', whiteSpace: 'nowrap'
              }}
            >
              {q}
            </button>
          ))}
        </div>
      )}

      {/* Input bar */}
      <div style={{
        background: 'white',
        borderTop: '2px solid var(--yellow)',
        padding: '10px 12px',
        display: 'flex', gap: 8, alignItems: 'flex-end'
      }}>
        <textarea
          ref={inputRef}
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault()
              send()
            }
          }}
          placeholder="Tanya tentang produk, harga, stok..."
          rows={1}
          style={{
            flex: 1, padding: '10px 14px',
            border: '2px solid var(--gray-200)', borderRadius: 12,
            fontSize: 14, fontWeight: 600,
            resize: 'none', maxHeight: 100, overflowY: 'auto',
            fontFamily: "'Nunito', sans-serif", lineHeight: 1.4,
            transition: 'border-color 0.2s'
          }}
          onFocus={e => e.target.style.borderColor = 'var(--blue)'}
          onBlur={e => e.target.style.borderColor = 'var(--gray-200)'}
        />
        <button
          onClick={() => send()}
          disabled={!input.trim() || loading}
          style={{
            width: 42, height: 42, borderRadius: 12, flexShrink: 0,
            background: input.trim() && !loading ? 'var(--red)' : 'var(--gray-200)',
            color: input.trim() && !loading ? 'white' : 'var(--gray-500)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            transition: 'all 0.2s', cursor: input.trim() && !loading ? 'pointer' : 'default'
          }}
        >
          {loading ? <Loader size={18} style={{ animation: 'spin 1s linear infinite' }} /> : <Send size={18} />}
        </button>
      </div>
    </div>
  )
}

function formatMessage(text) {
  // Bold **text**
  return text.split(/(\*\*[^*]+\*\*)/).map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={i}>{part.slice(2, -2)}</strong>
    }
    return part
  })
}
