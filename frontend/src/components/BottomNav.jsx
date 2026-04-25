import { Link, useLocation } from 'react-router-dom'
import { Home, LayoutGrid, MessageCircle, Phone } from 'lucide-react'

const navItems = [
  { to: '/', label: 'Beranda', icon: Home },
  { to: '/catalog', label: 'Katalog', icon: LayoutGrid },
  { to: '/chat', label: 'Tanya AI', icon: MessageCircle },
]

export default function BottomNav() {
  const location = useLocation()

  return (
    <>
      {/* Bottom Nav */}
      <nav style={{
        position: 'fixed', bottom: 0, left: 0, right: 0, zIndex: 100,
        background: 'white',
        borderTop: '3px solid var(--yellow)',
        boxShadow: '0 -4px 20px rgba(0,0,0,0.10)',
        display: 'flex', height: 'var(--bottom-nav)',
        paddingBottom: 'env(safe-area-inset-bottom)'
      }} className="hide-desktop">
        {navItems.map(({ to, label, icon: Icon }) => {
          const active = location.pathname === to
          return (
            <Link key={to} to={to} style={{
              flex: 1, display: 'flex', flexDirection: 'column',
              alignItems: 'center', justifyContent: 'center', gap: 3,
              color: active ? 'var(--red)' : 'var(--gray-500)',
              fontWeight: active ? 800 : 600,
              fontSize: 10,
              background: active ? 'var(--red-light)' : 'transparent',
              transition: 'all 0.2s',
              position: 'relative'
            }}>
              {active && (
                <span style={{
                  position: 'absolute', top: 0, left: '20%', right: '20%',
                  height: 3, background: 'var(--red)', borderRadius: '0 0 4px 4px'
                }} />
              )}
              <Icon size={20} strokeWidth={active ? 2.5 : 1.8} />
              {label}
            </Link>
          )
        })}
        {/* WA Button */}
        <a
          href="https://wa.me/6285373373233"
          target="_blank" rel="noopener noreferrer"
          style={{
            flex: 1, display: 'flex', flexDirection: 'column',
            alignItems: 'center', justifyContent: 'center', gap: 3,
            color: '#25D366', fontWeight: 700, fontSize: 10,
            textDecoration: 'none'
          }}
        >
          <Phone size={20} strokeWidth={1.8} />
          WA Order
        </a>
      </nav>
    </>
  )
}
