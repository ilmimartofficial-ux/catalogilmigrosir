import { useState, useEffect, useCallback, useRef } from 'react'
import { useSearchParams } from 'react-router-dom'
import { getProducts, getCategories } from '../api/client'
import ProductCard from '../components/ProductCard.jsx'
import { Search, Filter, X, ChevronLeft, ChevronRight, Loader } from 'lucide-react'

export default function Catalog() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [products, setProducts] = useState([])
  const [categories, setCategories] = useState([])
  const [pagination, setPagination] = useState({})
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState(searchParams.get('search') || '')
  const [category, setCategory] = useState(searchParams.get('category') || 'all')
  const [page, setPage] = useState(1)
  const [showFilter, setShowFilter] = useState(false)
  const searchRef = useRef(null)
  const debounceRef = useRef(null)

  // Load categories once
  useEffect(() => {
    getCategories().then(r => setCategories(r.data.data)).catch(console.error)
  }, [])

  // Load products
  const loadProducts = useCallback((s, cat, p) => {
    setLoading(true)
    getProducts({ search: s, category: cat === 'all' ? '' : cat, page: p, limit: 60 })
      .then(r => {
        setProducts(r.data.data)
        setPagination(r.data.pagination)
      })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    clearTimeout(debounceRef.current)
    debounceRef.current = setTimeout(() => {
      setPage(1)
      loadProducts(search, category, 1)
      // Sync URL
      const p = {}
      if (search) p.search = search
      if (category !== 'all') p.category = category
      setSearchParams(p, { replace: true })
    }, 350)
    return () => clearTimeout(debounceRef.current)
  }, [search, category])

  useEffect(() => {
    loadProducts(search, category, page)
  }, [page])

  const clearSearch = () => { setSearch(''); searchRef.current?.focus() }

  return (
    <main style={{ minHeight: '100vh' }}>
      {/* Sticky search bar */}
      <div style={{
        position: 'sticky', top: 'var(--nav-height)', zIndex: 50,
        background: 'white',
        borderBottom: '2px solid var(--yellow)',
        padding: '10px 0'
      }}>
        <div className="container" style={{ display: 'flex', gap: 8 }}>
          {/* Search input */}
          <div style={{ flex: 1, position: 'relative' }}>
            <Search size={16} style={{
              position: 'absolute', left: 12, top: '50%',
              transform: 'translateY(-50%)', color: 'var(--gray-500)'
            }} />
            <input
              ref={searchRef}
              className="input"
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="Cari produk... (nama, kode, kategori)"
              style={{ paddingLeft: 36, paddingRight: search ? 36 : 14 }}
            />
            {search && (
              <button onClick={clearSearch} style={{
                position: 'absolute', right: 10, top: '50%',
                transform: 'translateY(-50%)',
                background: 'none', color: 'var(--gray-500)'
              }}>
                <X size={16} />
              </button>
            )}
          </div>
          {/* Filter button */}
          <button
            className="btn btn-outline btn-sm"
            onClick={() => setShowFilter(!showFilter)}
            style={{ flexShrink: 0, borderColor: showFilter ? 'var(--red)' : undefined, color: showFilter ? 'var(--red)' : undefined }}
          >
            <Filter size={16} />
            <span className="hide-mobile">Filter</span>
          </button>
        </div>

        {/* Category filter row */}
        {showFilter && (
          <div style={{
            padding: '8px 0 4px',
            borderTop: '1px solid var(--gray-100)',
            overflowX: 'auto',
            display: 'flex', gap: 6, paddingLeft: 16
          }}>
            {[{ jenis: 'all', count: pagination.total || 0 }, ...categories].map(cat => (
              <button
                key={cat.jenis}
                onClick={() => setCategory(cat.jenis)}
                style={{
                  flexShrink: 0,
                  padding: '5px 12px', borderRadius: 99,
                  fontSize: 12, fontWeight: 700,
                  border: '2px solid',
                  borderColor: category === cat.jenis ? 'var(--red)' : 'var(--gray-200)',
                  background: category === cat.jenis ? 'var(--red)' : 'white',
                  color: category === cat.jenis ? 'white' : 'var(--gray-700)',
                  cursor: 'pointer', transition: 'all 0.15s',
                  whiteSpace: 'nowrap'
                }}
              >
                {cat.jenis === 'all' ? 'Semua' : cat.jenis}
                <span style={{ marginLeft: 4, opacity: 0.7 }}>({cat.count})</span>
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="container" style={{ paddingTop: 16, paddingBottom: 16 }}>
        {/* Result info */}
        <div style={{
          display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          marginBottom: 14, flexWrap: 'wrap', gap: 8
        }}>
          <p style={{ fontSize: 13, color: 'var(--gray-500)', fontWeight: 600 }}>
            {loading ? 'Memuat...' : (
              <>
                Menampilkan <strong style={{ color: 'var(--gray-900)' }}>{products.length}</strong> dari{' '}
                <strong style={{ color: 'var(--gray-900)' }}>{(pagination.total || 0).toLocaleString('id-ID')}</strong> produk
                {category !== 'all' && <> · Kategori: <strong style={{ color: 'var(--red)' }}>{category}</strong></>}
              </>
            )}
          </p>
          {(search || category !== 'all') && (
            <button
              className="btn btn-outline btn-sm"
              onClick={() => { setSearch(''); setCategory('all') }}
              style={{ fontSize: 12 }}
            >
              <X size={14} /> Reset Filter
            </button>
          )}
        </div>

        {/* Products grid */}
        {loading ? (
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(160px, 1fr))',
            gap: 12
          }}>
            {[...Array(12)].map((_, i) => (
              <div key={i} className="skeleton" style={{ height: 220, borderRadius: 12 }} />
            ))}
          </div>
        ) : products.length === 0 ? (
          <div style={{
            textAlign: 'center', padding: '60px 20px'
          }}>
            <div style={{ fontSize: 48, marginBottom: 12 }}>🔍</div>
            <h3 style={{ fontSize: 18, fontWeight: 800, marginBottom: 8 }}>Produk Tidak Ditemukan</h3>
            <p style={{ color: 'var(--gray-500)', fontSize: 14, marginBottom: 20 }}>
              Coba kata kunci lain atau hubungi kami via WhatsApp
            </p>
            <a
              href="https://wa.me/6285373373233"
              target="_blank" rel="noopener noreferrer"
              className="btn btn-yellow"
            >
              📱 Tanya via WhatsApp
            </a>
          </div>
        ) : (
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(160px, 1fr))',
            gap: 12
          }}>
            {products.map(p => <ProductCard key={p.id} product={p} />)}
          </div>
        )}

        {/* Pagination */}
        {pagination.pages > 1 && !loading && (
          <div style={{
            display: 'flex', justifyContent: 'center', alignItems: 'center',
            gap: 8, marginTop: 28, flexWrap: 'wrap'
          }}>
            <button
              className="btn btn-outline btn-sm"
              onClick={() => { setPage(p => p - 1); window.scrollTo({ top: 0, behavior: 'smooth' }) }}
              disabled={page <= 1}
            >
              <ChevronLeft size={16} /> Prev
            </button>

            {/* Page numbers */}
            {pagesArr(pagination.pages, page).map((p, i) =>
              p === '...' ? (
                <span key={`e${i}`} style={{ color: 'var(--gray-500)', padding: '0 4px' }}>...</span>
              ) : (
                <button
                  key={p}
                  onClick={() => { setPage(p); window.scrollTo({ top: 0, behavior: 'smooth' }) }}
                  style={{
                    width: 36, height: 36, borderRadius: 8,
                    fontWeight: 800, fontSize: 13,
                    background: page === p ? 'var(--red)' : 'white',
                    color: page === p ? 'white' : 'var(--gray-700)',
                    border: `2px solid ${page === p ? 'var(--red)' : 'var(--gray-200)'}`,
                    cursor: 'pointer', transition: 'all 0.15s'
                  }}
                >
                  {p}
                </button>
              )
            )}

            <button
              className="btn btn-outline btn-sm"
              onClick={() => { setPage(p => p + 1); window.scrollTo({ top: 0, behavior: 'smooth' }) }}
              disabled={!pagination.has_next}
            >
              Next <ChevronRight size={16} />
            </button>
          </div>
        )}
      </div>
    </main>
  )
}

function pagesArr(total, current) {
  const pages = []
  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
    return pages
  }
  pages.push(1)
  if (current > 3) pages.push('...')
  for (let i = Math.max(2, current - 1); i <= Math.min(total - 1, current + 1); i++) pages.push(i)
  if (current < total - 2) pages.push('...')
  pages.push(total)
  return pages
}
