import streamlit as st
import pandas as pd
import base64, os, urllib.parse

# ══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="ILMIGROSIR – Katalog Harga",
    page_icon="🛒",
    layout="centered",
    initial_sidebar_state="collapsed",
)

ADMIN_PASSWORD = "nopal123"
CSV_PATH       = "UPDATE PERJUMLAH IPOS 5.xlsx - Sheet.csv"
LOGO_PATH      = "logo.jpg"
WA_NUMBER      = "6281234567890"   # ← Ganti nomor WhatsApp admin

# ══════════════════════════════════════════════════════════════
# DESIGN SYSTEM – Luxury Retail Theme
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Sora:wght@700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background: #F0F4FF !important;
}
.block-container {
    padding: 0 !important;
    max-width: 480px !important;
    margin: 0 auto !important;
}
#MainMenu, footer, header, .stDeployButton { display: none !important; }
.stAppHeader { display: none !important; }

.hero {
    background: linear-gradient(160deg, #0A1628 0%, #0D2461 55%, #1545A8 100%);
    padding: 24px 20px 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content:'';position:absolute;top:-40px;right:-40px;
    width:200px;height:200px;border-radius:50%;
    background:radial-gradient(circle,rgba(255,215,0,.12) 0%,transparent 70%);
}
.hero::after {
    content:'';position:absolute;bottom:-30px;left:-30px;
    width:160px;height:160px;border-radius:50%;
    background:radial-gradient(circle,rgba(37,99,235,.25) 0%,transparent 70%);
}
.hero-logo {
    max-width:220px;border-radius:12px;
    box-shadow:0 8px 32px rgba(0,0,0,.4);
    position:relative;z-index:1;margin-bottom:12px;
}
.hero-tagline {
    color:#FFD700;font-size:11px;font-weight:700;
    letter-spacing:2.5px;text-transform:uppercase;
    position:relative;z-index:1;
}
.hero-sub {
    color:rgba(255,255,255,.5);font-size:10px;
    margin-top:4px;position:relative;z-index:1;letter-spacing:.5px;
}

.stats-bar {
    display:flex;background:#fff;
    border-bottom:1px solid #E8EDF8;padding:10px 0;
}
.stat-item {
    flex:1;text-align:center;border-right:1px solid #E8EDF8;
}
.stat-item:last-child{border-right:none;}
.stat-num{font-size:17px;font-weight:800;color:#0D2461;display:block;line-height:1;}
.stat-label{font-size:9px;color:#94A3B8;font-weight:700;text-transform:uppercase;letter-spacing:.8px;display:block;margin-top:2px;}

.stTextInput > div > div > input {
    border:2px solid #E2E8F8 !important;border-radius:12px !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
    font-size:14px !important;font-weight:500 !important;
    color:#0D2461 !important;padding:10px 14px !important;
    background:#F8FAFF !important;box-shadow:none !important;
}
.stTextInput > div > div > input:focus {
    border-color:#1545A8 !important;background:#fff !important;
    box-shadow:0 0 0 3px rgba(21,69,168,.1) !important;
}
.stTextInput > label,.stSelectbox > label {
    font-size:11px !important;font-weight:700 !important;
    color:#64748B !important;letter-spacing:.8px !important;
    text-transform:uppercase !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
}
.stSelectbox > div > div {
    border:2px solid #E2E8F8 !important;border-radius:12px !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
    font-size:13px !important;font-weight:600 !important;
    color:#0D2461 !important;background:#F8FAFF !important;
    box-shadow:none !important;
}

.result-strip {
    display:flex;align-items:center;justify-content:space-between;
    padding:10px 16px;background:#EEF2FF;border-bottom:1px solid #DDE5FF;
}
.result-count{font-size:12px;font-weight:700;color:#1545A8;}
.result-hint{font-size:10px;color:#94A3B8;font-weight:500;}

.catalog-feed{padding:12px 14px 0;background:#F0F4FF;}

.pcard {
    background:#fff;border-radius:16px;margin-bottom:12px;overflow:hidden;
    box-shadow:0 1px 4px rgba(13,36,97,.06),0 4px 16px rgba(13,36,97,.04);
    border:1px solid #E8EDF8;
}
.pcard-header {
    padding:14px 16px 10px;border-bottom:1px solid #F1F5FD;
    background:linear-gradient(135deg,#F8FAFF 0%,#fff 100%);
}
.pcard-badges{display:flex;align-items:center;gap:6px;margin-bottom:8px;flex-wrap:wrap;}
.badge-jenis {
    font-size:9px;font-weight:800;letter-spacing:1.2px;text-transform:uppercase;
    color:#1545A8;background:#EEF2FF;border:1px solid #C7D4FF;
    border-radius:6px;padding:3px 8px;
}
.badge-grosir {
    font-size:9px;font-weight:800;letter-spacing:.8px;text-transform:uppercase;
    color:#92400E;background:linear-gradient(90deg,#FEF3C7,#FDE68A);
    border:1px solid #F59E0B;border-radius:6px;padding:3px 8px;
}
.pcard-name{font-size:14px;font-weight:700;color:#0A1628;line-height:1.35;letter-spacing:-.1px;}
.pcard-kode{font-size:10px;color:#94A3B8;font-weight:500;margin-top:3px;}

.price-row {
    display:flex;align-items:center;
    padding:12px 16px;border-bottom:1px solid #F8FAFF;
}
.price-row:last-child{border-bottom:none;}
.price-row:nth-child(even){background:#FAFCFF;}
.price-row-left{flex:1;}
.satuan-pill {
    display:inline-flex;align-items:center;gap:5px;
    background:#0D2461;color:#fff;
    font-size:11px;font-weight:700;border-radius:8px;
    padding:4px 10px;letter-spacing:.5px;margin-bottom:3px;
}
.isi-label{font-size:10px;color:#94A3B8;font-weight:500;}
.price-row-right{text-align:right;}
.price-retail {
    font-size:19px;font-weight:800;color:#0D2461;
    font-family:'Sora',sans-serif;line-height:1;letter-spacing:-.5px;
}
.price-grosir-wrap{margin-top:4px;}
.price-grosir{font-size:15px;font-weight:800;color:#DC2626;font-family:'Sora',sans-serif;}
.grosir-pill {
    font-size:8px;font-weight:800;color:#92400E;
    background:#FEF3C7;border:1px solid #F59E0B;
    border-radius:4px;padding:2px 5px;margin-left:4px;letter-spacing:.5px;
}
.hemat-pill {
    display:inline-block;font-size:9px;font-weight:700;
    color:#065F46;background:#ECFDF5;border:1px solid #6EE7B7;
    border-radius:4px;padding:2px 6px;margin-top:3px;
}

.wa-btn-wrap{padding:12px 14px;background:#F8FAFF;border-top:1px solid #EEF2FF;}
.wa-btn {
    display:flex;align-items:center;justify-content:center;gap:8px;
    background:linear-gradient(135deg,#22C55E 0%,#16A34A 100%);
    color:#fff !important;text-decoration:none !important;
    border-radius:12px;padding:13px 16px;font-size:13px;font-weight:700;
    font-family:'Plus Jakarta Sans',sans-serif;letter-spacing:.2px;
    box-shadow:0 4px 14px rgba(22,163,74,.28);
}

.empty-state{text-align:center;padding:48px 24px;color:#94A3B8;}
.empty-icon{font-size:48px;margin-bottom:12px;display:block;}
.empty-title{font-size:16px;font-weight:700;color:#475569;}
.empty-sub{font-size:13px;margin-top:6px;line-height:1.6;}

.section-divider{height:6px;background:#F0F4FF;border-top:1px solid #E8EDF8;border-bottom:1px solid #E8EDF8;}

.app-footer{text-align:center;padding:20px 16px 28px;background:#fff;border-top:1px solid #E8EDF8;margin-top:8px;}
.footer-brand{font-size:13px;font-weight:800;color:#0D2461;letter-spacing:1px;text-transform:uppercase;}
.footer-tagline{font-size:11px;color:#94A3B8;margin-top:3px;}
.footer-dev{font-size:10px;color:#CBD5E1;margin-top:8px;letter-spacing:.5px;}
.footer-dev span{color:#1545A8;font-weight:700;}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════
def fmt_price(v):
    return "Rp {:,}".format(int(round(v))).replace(",", ".")

def wa_link(product_name):
    msg = ("Halo Kak, saya mau tanya stok barang ini di ILMIGROSIR:\n\n"
           f"* {product_name} *\n\nApakah tersedia? Berapa minimum ordernya? Terima kasih")
    return f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(msg)}"

@st.cache_data(show_spinner=False)
def load_data(path):
    df = pd.read_csv(path)
    for col in ["Harga Retail", "Harga Grosir", "Harga Pokok"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    df["Konversi"] = pd.to_numeric(df["Konversi"], errors="coerce").fillna(1)
    for col in ["Nama Item", "Jenis", "Satuan", "Kode Item"]:
        df[col] = df[col].astype(str).str.strip()
    return df

def get_logo_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

def build_card(kode, nama, jenis, group_df):
    rows_html = ""
    has_grosir = False

    for _, row in group_df.iterrows():
        satuan   = row["Satuan"]
        konversi = int(row["Konversi"])
        retail   = row["Harga Retail"]
        grosir   = row["Harga Grosir"]
        isi      = f"Isi {konversi} pcs" if konversi > 1 else "Satuan terkecil"
        r_str    = fmt_price(retail) if retail > 0 else "–"

        g_html = ""
        if grosir > 0 and grosir < retail:
            has_grosir = True
            selisih = retail - grosir
            pct     = round(selisih / retail * 100, 1)
            g_html  = (
                f'<div class="price-grosir-wrap">'
                f'<span class="price-grosir">{fmt_price(grosir)}</span>'
                f'<span class="grosir-pill">GROSIR &gt;3</span>'
                f'<br><span class="hemat-pill">Hemat {fmt_price(selisih)} ({pct}%)</span>'
                f'</div>'
            )

        rows_html += (
            f'<div class="price-row">'
            f'<div class="price-row-left">'
            f'<div class="satuan-pill">📦 {satuan}</div>'
            f'<div class="isi-label">{isi}</div>'
            f'</div>'
            f'<div class="price-row-right">'
            f'<div class="price-retail">{r_str}</div>'
            f'{g_html}'
            f'</div>'
            f'</div>'
        )

    gb = '<span class="badge-grosir">⭐ Harga Grosir</span>' if has_grosir else ""
    link = wa_link(nama)

    return (
        f'<div class="pcard">'
        f'<div class="pcard-header">'
        f'<div class="pcard-badges"><span class="badge-jenis">{jenis}</span>{gb}</div>'
        f'<div class="pcard-name">{nama}</div>'
        f'<div class="pcard-kode">Kode: {kode}</div>'
        f'</div>'
        f'<div class="pcard-prices">{rows_html}</div>'
        f'<div class="wa-btn-wrap">'
        f'<a class="wa-btn" href="{link}" target="_blank">'
        f'💬&nbsp; Tanya Stok &amp; Order via WhatsApp'
        f'</a>'
        f'</div>'
        f'</div>'
    )


# ══════════════════════════════════════════════════════════════
# LOAD DATA
# ══════════════════════════════════════════════════════════════
df = pd.DataFrame()
if os.path.exists(CSV_PATH):
    df = load_data(CSV_PATH)

total_produk   = df.groupby("Kode Item").ngroups if not df.empty else 0
total_kategori = df["Jenis"].nunique()            if not df.empty else 0
total_grosir   = int((df["Harga Grosir"] > 0).sum()) if not df.empty else 0


# ══════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════
logo_b64 = get_logo_b64(LOGO_PATH)
logo_tag  = (
    f'<img class="hero-logo" src="data:image/jpeg;base64,{logo_b64}" alt="ILMIGROSIR"/>'
    if logo_b64 else
    '<div style="font-size:28px;font-weight:900;color:#fff;font-family:Sora,sans-serif;">ILMIGROSIR</div>'
)

st.html(f"""
<div class="hero">
  {logo_tag}
  <div class="hero-tagline">✦ CATALOG HARGA ILMIGROSIR ✦</div>
  <div class="hero-sub">PEMBELIAN DI ATAS 3 UNTUK MENDAPATKAN HARGA GROSIR</div>
</div>
<div class="stats-bar">
  <div class="stat-item">
        <span class="stat-num">{total_produk:,}</span>
        <span class="stat-label">Produk</span>
  </div>
  <div class="stat-item">
    <span class="stat-num">{total_kategori}</span>
    <span class="stat-label">Kategori</span>
  </div>
  <div class="stat-item">
    <span class="stat-num">{total_grosir:,}</span>
    <span class="stat-label">Ada Grosir</span>
  </div>
</div>
""")


# ══════════════════════════════════════════════════════════════
# SEARCH & FILTER
# ══════════════════════════════════════════════════════════════
if df.empty:
    st.error("Database tidak ditemukan. Upload lewat Menu Admin.")
else:
    col1, col2 = st.columns([3, 2])
    with col1:
        keyword = st.text_input("🔍 Cari Barang", placeholder="Ketik nama barang…")
    with col2:
        cats = ["Semua Kategori"] + sorted(df["Jenis"].unique().tolist())
        selected_cat = st.selectbox("📂 Kategori", cats)

    filtered = df.copy()
    if keyword.strip():
        filtered = filtered[filtered["Nama Item"].str.contains(keyword.strip(), case=False, na=False)]
    if selected_cat != "Semua Kategori":
        filtered = filtered[filtered["Jenis"] == selected_cat]

    groups          = filtered.groupby(["Kode Item", "Nama Item", "Jenis"], sort=False)
    unique_products = list(groups)
    n               = len(unique_products)

    hint = "Coba kata lain" if n == 0 else "Scroll untuk lihat semua"
    st.html(f"""
    <div class="result-strip">
      <span class="result-count">{'Tidak ada' if n == 0 else f'{n:,}'} produk ditemukan</span>
      <span class="result-hint">{hint}</span>
    </div>
    """)

    if n == 0:
        st.html("""
        <div class="empty-state">
          <span class="empty-icon">🔍</span>
          <div class="empty-title">Produk tidak ditemukan</div>
          <div class="empty-sub">Coba gunakan kata kunci berbeda<br>atau pilih kategori lain.</div>
        </div>
        """)
    else:
        parts = ['<div class="catalog-feed">']
        for (kode, nama, jenis), gdf in unique_products:
            parts.append(build_card(kode, nama, jenis, gdf))
        parts.append('</div>')
        st.html("".join(parts))


# ══════════════════════════════════════════════════════════════
# ADMIN
# ══════════════════════════════════════════════════════════════
st.html('<div class="section-divider"></div>')
with st.expander("⚙️ Menu Admin"):
    pw = st.text_input("Password", type="password", key="admin_pw",
                       placeholder="Masukkan password admin…")
    if pw == ADMIN_PASSWORD:
        st.success("✅ Login berhasil!")
        up = st.file_uploader("Upload Database CSV (dari iPOS 5)", type=["csv"])
        if up:
            try:
                new_df = pd.read_csv(up)
                req = {"Kode Item","Nama Item","Jenis","Konversi","Satuan","Harga Retail","Harga Grosir"}
                if not req.issubset(set(new_df.columns)):
                    st.error(f"Kolom tidak lengkap. Dibutuhkan: {req}")
                else:
                    new_df.to_csv(CSV_PATH, index=False)
                    st.cache_data.clear()
                    st.success(f"✅ Database diperbarui! {len(new_df):,} baris tersimpan.")
                    st.rerun()
            except Exception as e:
                st.error(f"Gagal: {e}")
        st.info(f"📱 Nomor WA Admin: `{WA_NUMBER}` — Edit di baris 21 file `app.py`")
    elif pw:
        st.error("❌ Password salah.")


# ══════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════
st.html("""
<div class="app-footer">
  <div class="footer-brand">ILMIGROSIR</div>
  <div class="footer-tagline">JUAL KEMBALI UNTUNG BERKALI</div>
  <div class="footer-dev"><span>Developed with by NOPAL TECH</span></div>
</div>
""")
