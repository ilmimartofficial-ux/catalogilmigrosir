import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom'
import Navbar from './components/Navbar.jsx'
import BottomNav from './components/BottomNav.jsx'
import Home from './pages/Home.jsx'
import Catalog from './pages/Catalog.jsx'
import Chat from './pages/Chat.jsx'
import Admin from './pages/Admin.jsx'

function Layout() {
  const location = useLocation()
  const isAdmin = location.pathname === '/admin'

  return (
    <div style={{ paddingBottom: isAdmin ? 0 : 'var(--bottom-nav)' }}>
      {!isAdmin && <Navbar />}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/catalog" element={<Catalog />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/admin" element={<Admin />} />
      </Routes>
      {!isAdmin && <BottomNav />}
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <Layout />
    </BrowserRouter>
  )
}
