import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getStats, getCategories, getProducts } from '../api/client'
import ProductCard from '../components/ProductCard.jsx'
import { Package, Tag, Star, ArrowRight, ChevronRight, MessageCircle } from 'lucide-react'

const formatRp = (n) => 'Rp ' + Number(n || 0).toLocaleString('id-ID')

export default function Home() {
  const [stats, setStats] = useState(null)
  const [categories, setCategories] = useState([])
  const [featured, setFeatured] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      getStats(),
      getCategories(),
      getProducts({ limit: 8 })
    ]).then(([s, c, p]) => {
      setStats(s.data.data)
      setCategories(c.data.data.slice(0, 8))
      setFeatured(p.data.data)
    }).catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  return (
    <main>
      {/* Hero Banner */}
      <section style={{
        background: 'linear-gradient(135deg, var(--yellow) 0%, #FFB300 50%, var(--yellow-dark) 100%)',
        padding: '32px 0 28px',
        position: 'relative', overflow: 'hidden'
      }}>
        {/* Decorative circles */}
        <div style={{
          position: 'absolute', top: -40, right: -40,
          width: 200, height: 200,
          borderRadius: '50%', background: 'rgba(255,255,255,0.15)'
        }} />
        <div style={{
          position: 'absolute', bottom: -60, left: -30,
          width: 150, height: 150,
          borderRadius: '50%', background: 'rgba(211,47,47,0.15)'
        }} />

        <div className="container" style={{ position: 'relative' }}>
          <div style={{
            border: '3px solid var(--red)',
            borderRadius: 4, padding: '4px 12px',
            display: 'inline-block', marginBottom: 12,
            background: 'white'
          }}>
            <span style={{
              fontFamily: "'Bebas Neue', sans-serif",
              fontSize: 28, letterSpacing: 2,
              color: 'var(--red)'
            }}>ilmi</span>
            <span style={{
              fontFamily: "'Bebas Neue', sans-serif",
              fontSize: 28, letterSpacing: 2,
              color: 'var(--blue)'
            }}>grosir</span>
          </div>

          <h1 style={{
            fontSize: 'clamp(22px, 5vw, 36px)',
            fontWeight: 900, color: 'var(--gray-900)',
            lineHeight: 1.2, marginBottom: 8
          }}>
            Jual Kembali,<br />
            <span style={{ color: 'var(--red)' }}>Untung Berkali-Kali! 📦</span>
          </h1>
          <p style={{
            fontSize: 14, color: 'var(--gray-700)',
            fontWeight: 600, marginBottom: 20, maxWidth: 400
          }}>
            Ribuan produk grosir dengan harga terbaik. Stok selalu update, pesan mudah via WhatsApp.
          </p>

          <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
            <Link to="/catalog" className="btn btn-primary btn-lg">
              🛒 Lihat Katalog
            </Link>
            <Link to="/chat" className="btn btn-blue btn-lg">
              🤖 Tanya AI
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Bar */}
      <section style={{
        background: 'var(--red)', padding: '14px 0'
      }}>
        <div className="container">
          {loading ? (
            <div style={{ display: 'flex', gap: 24 }}>
              {[1,2,3].map(i => (
                <div key={i} className="skeleton" style={{ height: 40, width: 120 }} />
              ))}
            </div>
          ) : (
            <div style={{
              display: 'flex', gap: 12, flexWrap: 'wrap',
              justifyContent: 'space-around'
            }}>
              {[
                { icon: Package, label: 'Total Produk', value: stats?.total_products?.toLocaleString('id-ID') || '0' },
                { icon: Tag, label: 'Kategori', value: stats?.total_categories || '0' },
                { icon: Star, label: 'Harga Grosir', value: stats?.total_grosir?.toLocaleString('id-ID') || '0' },
              ].map(({ icon: Icon, label, value }) => (
                <div key={label} style={{
                  display: 'flex', alignItems: 'center', gap: 10, color: 'white'
                }}>
                  <Icon size={20} style={{ opacity: 0.8 }} />
                  <div>
                    <div style={{ fontSize: 18, fontWeight: 900, lineHeight: 1 }}>{value}</div>
                    <div style={{ fontSize: 11, opacity: 0.8, fontWeight: 600 }}>{label}</div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Categories */}
      {categories.length > 0 && (
        <section style={{ padding: '24px 0 16px' }}>
          <div className="container">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 }}>
              <h2 style={{ fontSize: 18, fontWeight: 900 }}>📂 Kategori Produk</h2>
              <Link to="/catalog" style={{ fontSize: 13, color: 'var(--red)', fontWeight: 700, display: 'flex', alignItems: 'center', gap: 4 }}>
                Semua <ChevronRight size={14} />
              </Link>
            </div>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(100px, 1fr))',
              gap: 10
            }}>
              {categories.map((cat) => (
                <Link
                  key={cat.jenis}
                  to={`/catalog?category=${cat.jenis}`}
                  style={{
                    background: 'white',
                    borderRadius: 12, padding: '12px 8px',
                    textAlign: 'center',
                    boxShadow: 'var(--shadow-sm)',
                    border: '2px solid transparent',
                    transition: 'all 0.2s'
                  }}
                  onMouseEnter={e => e.currentTarget.style.borderColor = 'var(--yellow)'}
                  onMouseLeave={e => e.currentTarget.style.borderColor = 'transparent'}
                >
                  <div style={{ fontSize: 22, marginBottom: 4 }}>{catEmoji(cat.jenis)}</div>
                  <div style={{ fontSize: 11, fontWeight: 800, color: 'var(--gray-900)', lineHeight: 1.2 }}>
                    {cat.jenis}
                  </div>
                  <div style={{ fontSize: 10, color: 'var(--gray-500)', marginTop: 2 }}>
                    {cat.count} item
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Featured Products */}
      <section style={{ padding: '16px 0 24px' }}>
        <div className="container">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 }}>
            <h2 style={{ fontSize: 18, fontWeight: 900 }}>🔥 Produk Pilihan</h2>
            <Link to="/catalog" style={{ fontSize: 13, color: 'var(--red)', fontWeight: 700, display: 'flex', alignItems: 'center', gap: 4 }}>
              Lihat Semua <ArrowRight size={14} />
            </Link>
          </div>

          {loading ? (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(160px, 1fr))', gap: 12 }}>
              {[...Array(8)].map((_, i) => (
                <div key={i} className="skeleton" style={{ height: 200, borderRadius: 12 }} />
              ))}
            </div>
          ) : (
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(160px, 1fr))',
              gap: 12
            }}>
              {featured.map(p => <ProductCard key={p.id} product={p} />)}
            </div>
          )}
        </div>
      </section>

      {/* AI Chat CTA */}
      <section style={{
        background: 'linear-gradient(135deg, var(--blue-dark), var(--blue))',
        padding: '24px 0', margin: '0 0 8px'
      }}>
        <div className="container" style={{ textAlign: 'center' }}>
          <MessageCircle size={36} style={{ color: 'var(--yellow)', margin: '0 auto 12px' }} />
          <h2 style={{ fontSize: 20, fontWeight: 900, color: 'white', marginBottom: 8 }}>
            Mau Tanya Harga? Tanya AI Kami!
          </h2>
          <p style={{ color: 'rgba(255,255,255,0.8)', fontSize: 13, marginBottom: 16, fontWeight: 600 }}>
            AI kami mengakses database produk secara real-time. Tanya apa saja tentang produk kami!
          </p>
          <Link to="/chat" className="btn btn-yellow btn-lg">
            🤖 Chat Sekarang — Gratis!
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer style={{
        background: 'var(--gray-900)', color: 'white',
        padding: '20px 0', textAlign: 'center'
      }}>
        <div className="container">
          <div style={{
            fontFamily: "'Bebas Neue', sans-serif",
            fontSize: 24, letterSpacing: 2, marginBottom: 4
          }}>
            <span style={{ color: 'var(--red)' }}>ILMI</span>
            <span style={{ color: 'var(--yellow)' }}>GROSIR</span>
          </div>
          <p style={{ fontSize: 12, color: 'rgba(255,255,255,0.5)', marginBottom: 12 }}>
            Jual Kembali Untung Berkali
          </p>
          <a
            href="https://wa.me/6285373373233"
            target="_blank" rel="noopener noreferrer"
            style={{
              display: 'inline-flex', alignItems: 'center', gap: 8,
              background: '#25D366', color: 'white',
              padding: '8px 20px', borderRadius: 99,
              fontWeight: 700, fontSize: 13
            }}
          >
            📱 085373373233
          </a>
          <p style={{ fontSize: 11, color: 'rgba(255,255,255,0.3)', marginTop: 16 }}>
            © 2024 ILMIGROSIR. All rights reserved.
          </p>
        </div>
      </footer>
    </main>
  )
}

function catEmoji(jenis) {
  if (!jenis) return '📦'
  const j = jenis.toUpperCase()
  if (j.includes('SNACK') || j.includes('MAKANAN')) return '🍪'
  if (j.includes('MINUMAN') || j.includes('AIR')) return '🥤'
  if (j.includes('SABUN') || j.includes('DETERGEN')) return '🧴'
  if (j.includes('ROKOK')) return '🚬'
  if (j.includes('SEMBAKO') || j.includes('BERAS')) return '🌾'
  if (j.includes('KOPI')) return '☕'
  if (j.includes('TEH')) return '🍵'
  if (j.includes('MINYAK')) return '🫙'
  if (j.includes('SUSU')) return '🥛'
  if (j.includes('BUMBU')) return '🌶️'
  return '📦'
}
