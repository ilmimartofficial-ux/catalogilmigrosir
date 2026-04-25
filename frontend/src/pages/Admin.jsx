import { useState, useEffect, useRef } from 'react'
import { adminLogin, uploadExcel, getHistory, getStats } from '../api/client'
import { Lock, Upload, LogOut, CheckCircle, AlertCircle, Clock, Database, Package } from 'lucide-react'

export default function Admin() {
  const [token, setToken] = useState(() => sessionStorage.getItem('admin_token') || '')
  const [password, setPassword] = useState('')
  const [loginLoading, setLoginLoading] = useState(false)
  const [loginError, setLoginError] = useState('')
  const [stats, setStats] = useState(null)
  const [history, setHistory] = useState([])
  const [uploading, setUploading] = useState(false)
  const [uploadResult, setUploadResult] = useState(null)
  const [dragOver, setDragOver] = useState(false)
  const fileRef = useRef(null)

  const isLoggedIn = !!token

  useEffect(() => {
    if (isLoggedIn) loadData()
  }, [isLoggedIn])

  const loadData = async () => {
    try {
      const [s, h] = await Promise.all([getStats(), getHistory(token)])
      setStats(s.data.data)
      setHistory(h.data.data)
    } catch (e) {
      if (e.response?.status === 401) logout()
    }
  }

  const login = async (e) => {
    e.preventDefault()
    setLoginLoading(true)
    setLoginError('')
    try {
      const r = await adminLogin(password)
      const t = r.data.token
      setToken(t)
      sessionStorage.setItem('admin_token', t)
    } catch {
      setLoginError('❌ Password salah. Coba lagi.')
    } finally {
      setLoginLoading(false)
    }
  }

  const logout = () => {
    setToken('')
    sessionStorage.removeItem('admin_token')
    setStats(null)
    setHistory([])
  }

  const handleFile = async (file) => {
    if (!file) return
    if (!/\.(xlsx|xls|csv)$/i.test(file.name)) {
      setUploadResult({ success: false, message: '❌ Hanya file .xlsx, .xls, atau .csv' })
      return
    }
    setUploading(true)
    setUploadResult(null)
    try {
      const r = await uploadExcel(file, token)
      setUploadResult({ success: true, message: r.data.message, total: r.data.total })
      loadData()
    } catch (e) {
      setUploadResult({
        success: false,
        message: e.response?.data?.message || '❌ Upload gagal. Cek format file.'
      })
    } finally {
      setUploading(false)
      if (fileRef.current) fileRef.current.value = ''
    }
  }

  const onDrop = (e) => {
    e.preventDefault()
    setDragOver(false)
    handleFile(e.dataTransfer.files[0])
  }

  // ── LOGIN PAGE ──────────────────────────────────────────────
  if (!isLoggedIn) {
    return (
      <div style={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, var(--yellow) 0%, var(--yellow-dark) 100%)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        padding: 16
      }}>
        <div className="card" style={{ width: '100%', maxWidth: 380, padding: 32 }}>
          {/* Logo */}
          <div style={{ textAlign: 'center', marginBottom: 28 }}>
            <div style={{
              width: 64, height: 64, borderRadius: 16, margin: '0 auto 12px',
              background: 'var(--yellow)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              border: '3px solid var(--red)'
            }}>
              <Lock size={28} color="var(--red)" />
            </div>
            <h1 style={{ fontSize: 22, fontWeight: 900, marginBottom: 4 }}>Admin Panel</h1>
            <p style={{ fontSize: 13, color: 'var(--gray-500)', fontWeight: 600 }}>ILMIGROSIR Dashboard</p>
          </div>

          <form onSubmit={login} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            <div>
              <label style={{ display: 'block', fontSize: 13, fontWeight: 800, marginBottom: 6, color: 'var(--gray-700)' }}>
                Password Admin
              </label>
              <input
                type="password"
                className="input"
                value={password}
                onChange={e => setPassword(e.target.value)}
                placeholder="Masukkan password..."
                autoFocus
              />
            </div>

            {loginError && (
              <div style={{
                background: 'var(--red-light)', color: 'var(--red)',
                padding: '10px 14px', borderRadius: 8, fontSize: 13, fontWeight: 700,
                display: 'flex', alignItems: 'center', gap: 8
              }}>
                <AlertCircle size={16} /> {loginError}
              </div>
            )}

            <button
              type="submit"
              className="btn btn-primary"
              disabled={loginLoading || !password}
              style={{ width: '100%', padding: '12px' }}
            >
              {loginLoading ? '⏳ Masuk...' : '🔐 Login'}
            </button>
          </form>

          <p style={{ textAlign: 'center', marginTop: 20, fontSize: 12, color: 'var(--gray-500)' }}>
            Khusus Admin ILMIGROSIR
          </p>
        </div>
      </div>
    )
  }

  // ── ADMIN DASHBOARD ─────────────────────────────────────────
  return (
    <div style={{ minHeight: '100vh', background: 'var(--gray-50)' }}>
      {/* Top Bar */}
      <div style={{
        background: 'var(--gray-900)',
        borderBottom: '3px solid var(--yellow)',
        padding: '12px 16px',
        display: 'flex', justifyContent: 'space-between', alignItems: 'center'
      }}>
        <div style={{ color: 'white' }}>
          <div style={{
            fontFamily: "'Bebas Neue', sans-serif",
            fontSize: 20, letterSpacing: 2, lineHeight: 1
          }}>
            <span style={{ color: 'var(--red)' }}>ILMI</span>
            <span style={{ color: 'var(--yellow)' }}>GROSIR</span>
            <span style={{ color: 'rgba(255,255,255,0.5)', fontSize: 13, marginLeft: 8, fontFamily: "'Nunito', sans-serif" }}>
              Admin
            </span>
          </div>
        </div>
        <button
          onClick={logout}
          style={{
            display: 'flex', alignItems: 'center', gap: 6,
            background: 'rgba(255,255,255,0.1)', color: 'white',
            padding: '7px 14px', borderRadius: 8,
            fontSize: 13, fontWeight: 700, cursor: 'pointer', border: 'none'
          }}
        >
          <LogOut size={16} /> Logout
        </button>
      </div>

      <div className="container" style={{ padding: '20px 16px', maxWidth: 800 }}>
        {/* Stats */}
        {stats && (
          <div style={{
            display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)',
            gap: 12, marginBottom: 24
          }}>
            {[
              { icon: Package, label: 'Total Produk', value: stats.total_products?.toLocaleString('id-ID'), color: 'var(--blue)' },
              { icon: Database, label: 'Kategori', value: stats.total_categories, color: 'var(--red)' },
              { icon: CheckCircle, label: 'Ada Harga Grosir', value: stats.total_grosir?.toLocaleString('id-ID'), color: '#4CAF50' },
            ].map(({ icon: Icon, label, value, color }) => (
              <div key={label} className="card" style={{ padding: '14px', textAlign: 'center' }}>
                <Icon size={22} style={{ color, margin: '0 auto 6px' }} />
                <div style={{ fontSize: 22, fontWeight: 900, color }}>{value}</div>
                <div style={{ fontSize: 11, color: 'var(--gray-500)', fontWeight: 700 }}>{label}</div>
              </div>
            ))}
          </div>
        )}

        {/* Upload Section */}
        <div className="card" style={{ padding: 24, marginBottom: 24 }}>
          <h2 style={{ fontSize: 18, fontWeight: 900, marginBottom: 6, display: 'flex', alignItems: 'center', gap: 8 }}>
            <Upload size={20} color="var(--red)" /> Upload Data Produk
          </h2>
          <p style={{ fontSize: 13, color: 'var(--gray-500)', marginBottom: 16, fontWeight: 600 }}>
            Upload file Excel (.xlsx) untuk memperbarui seluruh database produk. Data lama akan diganti otomatis.
          </p>

          {/* Drop zone */}
          <div
            onDragOver={e => { e.preventDefault(); setDragOver(true) }}
            onDragLeave={() => setDragOver(false)}
            onDrop={onDrop}
            onClick={() => fileRef.current?.click()}
            style={{
              border: `3px dashed ${dragOver ? 'var(--blue)' : 'var(--gray-200)'}`,
              borderRadius: 16,
              padding: '36px 20px',
              textAlign: 'center',
              cursor: uploading ? 'default' : 'pointer',
              background: dragOver ? 'var(--blue-light)' : 'var(--gray-50)',
              transition: 'all 0.2s'
            }}
          >
            {uploading ? (
              <>
                <div style={{ fontSize: 40, marginBottom: 8 }}>⏳</div>
                <p style={{ fontWeight: 800, color: 'var(--blue)' }}>Sedang mengupload & memproses...</p>
                <p style={{ fontSize: 12, color: 'var(--gray-500)', marginTop: 4 }}>Mohon tunggu, jangan tutup halaman</p>
              </>
            ) : (
              <>
                <div style={{ fontSize: 40, marginBottom: 8 }}>📊</div>
                <p style={{ fontWeight: 800, fontSize: 15, marginBottom: 4 }}>
                  {dragOver ? 'Lepaskan file di sini!' : 'Drag & drop file, atau klik untuk pilih'}
                </p>
                <p style={{ fontSize: 12, color: 'var(--gray-500)', fontWeight: 600 }}>
                  Format: .xlsx, .xls, .csv · Max 50MB
                </p>
              </>
            )}
          </div>

          <input
            ref={fileRef}
            type="file"
            accept=".xlsx,.xls,.csv"
            style={{ display: 'none' }}
            onChange={e => handleFile(e.target.files[0])}
          />

          {!uploading && (
            <button
              className="btn btn-primary"
              onClick={() => fileRef.current?.click()}
              style={{ width: '100%', marginTop: 14, padding: 12 }}
            >
              <Upload size={18} /> Pilih File Excel
            </button>
          )}

          {/* Result */}
          {uploadResult && (
            <div style={{
              marginTop: 14,
              background: uploadResult.success ? '#E8F5E9' : 'var(--red-light)',
              color: uploadResult.success ? '#2E7D32' : 'var(--red)',
              padding: '14px 16px', borderRadius: 12,
              display: 'flex', alignItems: 'flex-start', gap: 10,
              fontWeight: 700, fontSize: 14
            }}>
              {uploadResult.success
                ? <CheckCircle size={20} style={{ flexShrink: 0, marginTop: 1 }} />
                : <AlertCircle size={20} style={{ flexShrink: 0, marginTop: 1 }} />
              }
              <div>
                <div>{uploadResult.message}</div>
                {uploadResult.total && (
                  <div style={{ fontSize: 12, fontWeight: 600, marginTop: 4, opacity: 0.8 }}>
                    Database diperbarui: {uploadResult.total.toLocaleString('id-ID')} produk aktif
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Column format guide */}
        <div className="card" style={{ padding: 20, marginBottom: 24 }}>
          <h3 style={{ fontSize: 15, fontWeight: 900, marginBottom: 12 }}>📋 Format Kolom Excel</h3>
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 12 }}>
              <thead>
                <tr style={{ background: 'var(--gray-100)' }}>
                  {['Kolom', 'Wajib?', 'Contoh'].map(h => (
                    <th key={h} style={{ padding: '8px 12px', textAlign: 'left', fontWeight: 800, color: 'var(--gray-700)' }}>
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {[
                  ['Nama Item', '✅ Wajib', 'Snack Chitato 68g'],
                  ['Kode Item', '⬜ Opsional', 'CHT001'],
                  ['Jenis', '⬜ Opsional', 'SNACK'],
                  ['Satuan', '⬜ Opsional', 'KARTON'],
                  ['ISI', '⬜ Opsional', '48'],
                  ['Stok', '⬜ Opsional', '100'],
                  ['Harga Retail', '⬜ Opsional', '4000'],
                  ['Harga Grosir', '⬜ Opsional', '3500'],
                ].map(([col, req, ex]) => (
                  <tr key={col} style={{ borderBottom: '1px solid var(--gray-100)' }}>
                    <td style={{ padding: '8px 12px', fontWeight: 700 }}>{col}</td>
                    <td style={{ padding: '8px 12px', color: req.includes('✅') ? '#2E7D32' : 'var(--gray-500)' }}>{req}</td>
                    <td style={{ padding: '8px 12px', color: 'var(--gray-500)' }}>{ex}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Upload history */}
        {history.length > 0 && (
          <div className="card" style={{ padding: 20 }}>
            <h3 style={{ fontSize: 15, fontWeight: 900, marginBottom: 14, display: 'flex', alignItems: 'center', gap: 8 }}>
              <Clock size={18} color="var(--gray-500)" /> Riwayat Upload
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {history.map(h => (
                <div key={h.id} style={{
                  display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                  padding: '10px 12px', background: 'var(--gray-50)', borderRadius: 8,
                  gap: 12, flexWrap: 'wrap'
                }}>
                  <div>
                    <div style={{ fontSize: 13, fontWeight: 800, color: 'var(--gray-900)' }}>{h.filename}</div>
                    <div style={{ fontSize: 11, color: 'var(--gray-500)' }}>{h.uploaded_at}</div>
                  </div>
                  <div className="badge badge-blue">
                    {h.total_rows?.toLocaleString('id-ID')} produk
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
