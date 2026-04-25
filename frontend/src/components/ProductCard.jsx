const formatRp = (n) =>
  'Rp ' + Number(n || 0).toLocaleString('id-ID')

export default function ProductCard({ product }) {
  const { nama_item, jenis, harga_retail, harga_grosir, satuan, isi, kode_item } = product
  const hasGrosir = harga_grosir > 0
  const waText = encodeURIComponent(
    `Halo kak, saya mau tanya/pesan:\n*${nama_item}*\nKode: ${kode_item || '-'}\nHarga Retail: ${formatRp(harga_retail)}\n\nMohon info ketersediaan stok ya 🙏`
  )

  return (
    <div className="card" style={{
      display: 'flex', flexDirection: 'column',
      transition: 'transform 0.2s, box-shadow 0.2s',
      cursor: 'default'
    }}
      onMouseEnter={e => {
        e.currentTarget.style.transform = 'translateY(-4px)'
        e.currentTarget.style.boxShadow = 'var(--shadow-md)'
      }}
      onMouseLeave={e => {
        e.currentTarget.style.transform = ''
        e.currentTarget.style.boxShadow = ''
      }}
    >
      {/* Color accent top bar based on category */}
      <div style={{
        height: 4,
        background: categoryColor(jenis)
      }} />

      <div style={{ padding: '12px 14px', flex: 1, display: 'flex', flexDirection: 'column', gap: 8 }}>
        {/* Category badge */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 6 }}>
          <span style={{
            fontSize: 10, fontWeight: 700, letterSpacing: 0.5,
            background: 'var(--yellow-light)', color: '#7B6000',
            padding: '2px 8px', borderRadius: 99,
            textTransform: 'uppercase', flexShrink: 0
          }}>{jenis || 'UMUM'}</span>
          {kode_item && (
            <span style={{ fontSize: 10, color: 'var(--gray-500)', fontWeight: 600 }}>
              #{kode_item}
            </span>
          )}
        </div>

        {/* Name */}
        <p style={{
          fontSize: 13, fontWeight: 800, color: 'var(--gray-900)',
          lineHeight: 1.35, flex: 1
        }}>{nama_item}</p>

        {/* Satuan */}
        {isi > 1 && (
          <span style={{ fontSize: 11, color: 'var(--gray-500)', fontWeight: 600 }}>
            Isi {isi} {satuan}
          </span>
        )}

        {/* Prices */}
        <div style={{
          background: 'var(--gray-50)', borderRadius: 8,
          padding: '8px 10px', display: 'flex', flexDirection: 'column', gap: 4
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: 11, color: 'var(--gray-500)', fontWeight: 600 }}>Retail</span>
            <span style={{ fontSize: 14, fontWeight: 900, color: 'var(--red)' }}>
              {formatRp(harga_retail)}
            </span>
          </div>
          {hasGrosir && (
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: 11, color: 'var(--blue)', fontWeight: 700 }}>Grosir</span>
              <span style={{ fontSize: 14, fontWeight: 900, color: 'var(--blue)' }}>
                {formatRp(harga_grosir)}
              </span>
            </div>
          )}
        </div>

        {/* WA button */}
        <a
          href={`https://wa.me/6285373373233?text=${waText}`}
          target="_blank" rel="noopener noreferrer"
          className="btn btn-yellow btn-sm"
          style={{ width: '100%', fontSize: 12, gap: 6 }}
        >
          📱 Pesan via WA
        </a>
      </div>
    </div>
  )
}

function categoryColor(jenis) {
  if (!jenis) return 'var(--gray-200)'
  const j = jenis.toUpperCase()
  if (j.includes('SNACK') || j.includes('MAKANAN')) return 'var(--yellow)'
  if (j.includes('MINUMAN') || j.includes('AIR')) return 'var(--blue)'
  if (j.includes('SABUN') || j.includes('DETERGEN') || j.includes('PEMBERSIH')) return '#4CAF50'
  if (j.includes('ROKOK')) return 'var(--red)'
  if (j.includes('SEMBAKO') || j.includes('BERAS')) return '#FF9800'
  if (j.includes('KOPI') || j.includes('TEH')) return '#795548'
  return '#9C27B0'
}
