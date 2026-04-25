import { Link, useLocation } from 'react-router-dom'
import { ShoppingBag, MessageCircle, LayoutGrid, Shield } from 'lucide-react'

export default function Navbar() {
  const location = useLocation()

  return (
    <header style={{
      position: 'sticky', top: 0, zIndex: 100,
      background: 'white',
      borderBottom: '3px solid var(--yellow)',
      boxShadow: '0 2px 12px rgba(0,0,0,0.08)'
    }}>
      <div className="container" style={{
        display: 'flex', alignItems: 'center',
        justifyContent: 'space-between',
        height: 'var(--nav-height)', gap: 16
      }}>
        {/* Logo */}
        <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: 8, flexShrink: 0 }}>
          <div style={{
            background: 'var(--yellow)',
            borderRadius: 8, padding: '4px 8px',
            border: '2px solid var(--red)',
            display: 'flex', alignItems: 'center'
          }}>
            <span style={{
              fontFamily: "'Bebas Neue', sans-serif",
              fontSize: 18, color: 'var(--red)', letterSpacing: 1
            }}>ilmi</span>
            <span style={{
              fontFamily: "'Bebas Neue', sans-serif",
              fontSize: 18, color: 'var(--blue)', letterSpacing: 1
            }}>grosir</span>
          </div>
          <span className="hide-mobile" style={{
            fontSize: 11, color: 'var(--gray-500)', fontWeight: 700,
            textTransform: 'uppercase', letterSpacing: 0.5
          }}>Jual Kembali Untung Berkali</span>
        </Link>

        {/* Desktop Nav */}
        <nav className="hide-mobile" style={{ display: 'flex', gap: 4 }}>
          {[
            { to: '/', label: 'Beranda', icon: ShoppingBag },
            { to: '/catalog', label: 'Katalog', icon: LayoutGrid },
            { to: '/chat', label: 'Tanya AI', icon: MessageCircle },
          ].map(({ to, label, icon: Icon }) => (
            <Link key={to} to={to} style={{
              display: 'flex', alignItems: 'center', gap: 6,
              padding: '8px 16px', borderRadius: 'var(--radius-sm)',
              fontWeight: 700, fontSize: 14,
              color: location.pathname === to ? 'var(--red)' : 'var(--gray-700)',
              background: location.pathname === to ? 'var(--red-light)' : 'transparent',
              transition: 'all 0.2s'
            }}>
              <Icon size={16} />
              {label}
            </Link>
          ))}
        </nav>

        {/* Right side */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <a
            href="https://wa.me/6285373373233"
            target="_blank" rel="noopener noreferrer"
            className="btn btn-yellow btn-sm hide-mobile"
          >
            📱 WhatsApp
          </a>
          <Link to="/admin" style={{
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            width: 36, height: 36, borderRadius: 8,
            background: 'var(--gray-100)', color: 'var(--gray-500)',
            transition: 'all 0.2s'
          }}>
            <Shield size={16} />
          </Link>
        </div>
      </div>
    </header>
  )
}
