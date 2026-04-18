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
WA_NUMBER      = "6282278891186"  # ← Ganti nomor WhatsApp admin

CATEGORY_ICONS = {
    "MIE INSTANT":"🍜","MIE CUP":"🍜","MIE OLAH":"🍜",
    "BERAS":"🌾","GULA":"🍚","MINYAK":"🫙",
    "KOPI":"☕","TEH":"🍵","SIRUP":"🧃",
    "SUSU UHT":"🥛","SUSU SKM":"🥛","SUSU FORMULA":"🍼",
    "SNACK":"🍿","CANDY":"🍬","CKLT BTG":"🍫",
    "SARDEN":"🐟","SAOS":"🫙","KECAP":"🫙",
    "BUMBU INSTANT":"🧂","MICIN":"🧂","GARAM":"🧂",
    "TERIGU":"🌾","BHN KUE":"🧁","BIHUN":"🍝",
    "ROKOK":"🚬","BHN ROKOK":"🚬",
    "DETERJEN":"🧺","RINSO BUBUK":"🧺","RINSO CAIR":"🧴",
    "SHAMPO":"🧴","SBN MANDI BTG":"🧼","REFIL/SBN MNDI":"🧴",
    "PSTA/SKT GIGI":"🪥","SABUN COLEK":"🧼","SBN LANTAI":"🫧",
    "TISU":"🧻","PEMBALUT":"🩹","POPOK":"👶",
    "OBAT":"💊","OBAT NYAMUK":"🦟",
    "COSMETIC":"💄","PRFM":"🌸",
    "PEWANGI RUANGAN":"🌺","MOLTO REF":"🌸","MOLTO RCG":"🌸","SOKLIN RCG":"🧴",
    "MNM":"🥤","MNM 1000":"💧","MNM RCG":"🥤",
    "MKAN":"🍱","MKCG":"🍱","MKN BYI":"🍱",
    "CUCI MULUT":"🍮","KEJU/MNTGA":"🧈",
    "GAS":"🔵","PLASTIK":"🛍️","KERTAS NASI":"📄",
    "ATK":"✏️","ALT":"🔧","ALT BYI":"🔧",
    "BAHAN DAPUR":"🥘","KATEMBAT":"🌿",
    "KRPK":"🥨","TERASI":"🦐","MAYONIES":"🥣","ACI":"🌽",
    "CURAH":"⚖️","SBN ALT MKN":"🍽️",
}

def cat_icon(j): return CATEGORY_ICONS.get(j.upper(), "📦")

# ══════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Sora:wght@700;800&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html,body,[class*="css"]{
    font-family:'Plus Jakarta Sans',sans-serif !important;
    background:#F0F4FF !important;
}
.block-container{padding:0 !important;max-width:480px !important;margin:0 auto !important;}
#MainMenu,footer,header,.stDeployButton{display:none !important;}
.stAppHeader{display:none !important;}

/* HERO */
.hero{
    background:linear-gradient(160deg,#0A1628 0%,#0D2461 55%,#1545A8 100%);
    padding:24px 20px 20px;text-align:center;position:relative;overflow:hidden;
}
.hero::before{content:'';position:absolute;top:-40px;right:-40px;width:200px;height:200px;
    border-radius:50%;background:radial-gradient(circle,rgba(255,215,0,.12) 0%,transparent 70%);}
.hero::after{content:'';position:absolute;bottom:-30px;left:-30px;width:160px;height:160px;
    border-radius:50%;background:radial-gradient(circle,rgba(37,99,235,.25) 0%,transparent 70%);}
.hero-logo{max-width:220px;border-radius:12px;box-shadow:0 8px 32px rgba(0,0,0,.4);
    position:relative;z-index:1;margin-bottom:12px;}
.hero-tagline{color:#FFD700;font-size:11px;font-weight:700;letter-spacing:2.5px;
    text-transform:uppercase;position:relative;z-index:1;}
.hero-sub{color:rgba(255,255,255,.5);font-size:10px;margin-top:4px;
    position:relative;z-index:1;letter-spacing:.5px;}

/* STATS */
.stats-bar{display:flex;background:#fff;border-bottom:1px solid #E8EDF8;padding:10px 0;}
.stat-item{flex:1;text-align:center;border-right:1px solid #E8EDF8;}
.stat-item:last-child{border-right:none;}
.stat-num{font-size:17px;font-weight:800;color:#0D2461;display:block;line-height:1;}
.stat-label{font-size:9px;color:#94A3B8;font-weight:700;text-transform:uppercase;
    letter-spacing:.8px;display:block;margin-top:2px;}

/* SEARCH */
.search-wrap{background:#fff;padding:12px 14px 10px;border-bottom:1px solid #E8EDF8;}
.stTextInput>div>div>input{
    border:2px solid #E2E8F8 !important;border-radius:12px !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
    font-size:14px !important;font-weight:500 !important;
    color:#0D2461 !important;padding:10px 14px !important;
    background:#F8FAFF !important;box-shadow:none !important;
}
.stTextInput>div>div>input:focus{
    border-color:#1545A8 !important;background:#fff !important;
    box-shadow:0 0 0 3px rgba(21,69,168,.1) !important;
}
.stTextInput>label{
    font-size:11px !important;font-weight:700 !important;color:#64748B !important;
    letter-spacing:.8px !important;text-transform:uppercase !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
}

/* CATEGORY CHIPS — horizontal slide */
.chips-wrap{
    background:#fff;
    padding:10px 0 10px;
    border-bottom:5px solid #F0F4FF;
}
.chips-label{
    font-size:10px;font-weight:800;color:#94A3B8;
    letter-spacing:1px;text-transform:uppercase;
    padding:0 14px 8px;display:block;
}
.chips-scroll{
    display:flex;gap:8px;
    overflow-x:auto;padding:2px 14px 4px;
    scrollbar-width:none;-ms-overflow-style:none;
    -webkit-overflow-scrolling:touch;
}
.chips-scroll::-webkit-scrollbar{display:none;}
.chip{
    display:inline-flex;align-items:center;gap:6px;
    flex:0 0 auto;
    padding:8px 14px;
    border-radius:50px;
    font-size:12px;font-weight:700;
    cursor:pointer;
    white-space:nowrap;
    border:2px solid #E2E8F8;
    background:#F8FAFF;
    color:#475569;
    transition:all .18s cubic-bezier(.4,0,.2,1);
    user-select:none;
}
.chip:active{transform:scale(.96);}
.chip.active{
    background:linear-gradient(135deg,#0D2461 0%,#1545A8 100%);
    border-color:#0D2461;
    color:#fff;
    box-shadow:0 4px 14px rgba(13,36,97,.3);
}
.chip-icon{font-size:15px;line-height:1;}

/* RESULT STRIP */
.result-strip{
    display:flex;align-items:center;justify-content:space-between;
    padding:10px 16px;background:#EEF2FF;border-bottom:1px solid #DDE5FF;
}
.result-count{font-size:12px;font-weight:700;color:#1545A8;}
.result-hint{font-size:10px;color:#94A3B8;font-weight:500;}
.active-badge{
    display:inline-flex;align-items:center;gap:4px;
    font-size:10px;background:#0D2461;color:#fff;
    border-radius:6px;padding:2px 8px;font-weight:700;margin-left:6px;
}

/* CATALOG */
.catalog-feed{padding:12px 14px 0;background:#F0F4FF;}

/* PRODUCT CARD */
.pcard{
    background:#fff;border-radius:16px;margin-bottom:12px;overflow:hidden;
    box-shadow:0 1px 4px rgba(13,36,97,.06),0 4px 16px rgba(13,36,97,.04);
    border:1px solid #E8EDF8;
}
.pcard-header{
    padding:14px 16px 10px;border-bottom:1px solid #F1F5FD;
    background:linear-gradient(135deg,#F8FAFF 0%,#fff 100%);
}
.pcard-badges{display:flex;align-items:center;gap:6px;margin-bottom:8px;flex-wrap:wrap;}
.badge-jenis{
    font-size:9px;font-weight:800;letter-spacing:1.2px;text-transform:uppercase;
    color:#1545A8;background:#EEF2FF;border:1px solid #C7D4FF;border-radius:6px;padding:3px 8px;
}
.badge-grosir{
    font-size:9px;font-weight:800;letter-spacing:.8px;text-transform:uppercase;
    color:#92400E;background:linear-gradient(90deg,#FEF3C7,#FDE68A);
    border:1px solid #F59E0B;border-radius:6px;padding:3px 8px;
}
.pcard-name{font-size:14px;font-weight:700;color:#0A1628;line-height:1.35;letter-spacing:-.1px;}
.pcard-kode{font-size:10px;color:#94A3B8;font-weight:500;margin-top:3px;}

.price-row{display:flex;align-items:center;padding:12px 16px;border-bottom:1px solid #F8FAFF;}
.price-row:last-child{border-bottom:none;}
.price-row:nth-child(even){background:#FAFCFF;}
.price-row-left{flex:1;}
.satuan-pill{
    display:inline-flex;align-items:center;gap:5px;
    background:#0D2461;color:#fff;
    font-size:11px;font-weight:700;border-radius:8px;
    padding:4px 10px;letter-spacing:.5px;margin-bottom:3px;
}
.isi-label{font-size:10px;color:#94A3B8;font-weight:500;}
.price-row-right{text-align:right;}
.price-retail{
    font-size:19px;font-weight:800;color:#0D2461;
    font-family:'Sora',sans-serif;line-height:1;letter-spacing:-.5px;
}
.price-grosir-wrap{margin-top:4px;}
.price-grosir{font-size:15px;font-weight:800;color:#DC2626;font-family:'Sora',sans-serif;}
.grosir-pill{
    font-size:8px;font-weight:800;color:#92400E;
    background:#FEF3C7;border:1px solid #F59E0B;
    border-radius:4px;padding:2px 5px;margin-left:4px;letter-spacing:.5px;
}
.hemat-pill{
    display:inline-block;font-size:9px;font-weight:700;
    color:#065F46;background:#ECFDF5;border:1px solid #6EE7B7;
    border-radius:4px;padding:2px 6px;margin-top:3px;
}

.wa-btn-wrap{padding:12px 14px;background:#F8FAFF;border-top:1px solid #EEF2FF;}
.wa-btn{
    display:flex;align-items:center;justify-content:center;gap:8px;
    background:linear-gradient(135deg,#22C55E 0%,#16A34A 100%);
    color:#fff !important;text-decoration:none !important;
    border-radius:12px;padding:13px 16px;font-size:13px;font-weight:700;
    font-family:'Plus Jakarta Sans',sans-serif;
    box-shadow:0 4px 14px rgba(22,163,74,.28);
}

.empty-state{text-align:center;padding:48px 24px;color:#94A3B8;}
.empty-icon{font-size:48px;margin-bottom:12px;display:block;}
.empty-title{font-size:16px;font-weight:700;color:#475569;}
.empty-sub{font-size:13px;margin-top:6px;line-height:1.6;}

.section-divider{height:6px;background:#F0F4FF;border-top:1px solid #E8EDF8;border-bottom:1px solid #E8EDF8;}

.app-footer{text-align:center;padding:20px 16px 28px;background:#fff;
    border-top:1px solid #E8EDF8;margin-top:8px;}
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

def wa_link(name):
    msg = (f"Halo Kak, saya mau tanya stok barang ini di ILMIGROSIR:\n\n"
           f"* {name} *\n\nApakah tersedia? Berapa minimum ordernya? Terima kasih")
    return f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(msg)}"

@st.cache_data(show_spinner=False)
def load_data(path):
    df = pd.read_csv(path)
    for col in ["Harga Retail","Harga Grosir","Harga Pokok"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    df["Konversi"] = pd.to_numeric(df["Konversi"], errors="coerce").fillna(1)
    for col in ["Nama Item","Jenis","Satuan","Kode Item"]:
        df[col] = df[col].astype(str).str.strip()
    return df

def get_logo_b64(path):
    if os.path.exists(path):
        with open(path,"rb") as f: return base64.b64encode(f.read()).decode()
    return ""

def build_card(kode, nama, jenis, group_df):
    rows_html = ""; has_grosir = False
    for _, row in group_df.iterrows():
        satuan = row["Satuan"]; konversi = int(row["Konversi"])
        retail = row["Harga Retail"]; grosir = row["Harga Grosir"]
        isi    = f"Isi {konversi} pcs" if konversi > 1 else "Satuan terkecil"
        r_str  = fmt_price(retail) if retail > 0 else "–"
        g_html = ""
        if grosir > 0 and grosir < retail:
            has_grosir = True
            selisih = retail - grosir; pct = round(selisih/retail*100,1)
            g_html = (
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
            f'<div class="price-retail">{r_str}</div>{g_html}'
            f'</div></div>'
        )
    gb   = '<span class="badge-grosir">⭐ Harga Grosir</span>' if has_grosir else ""
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
        f'💬&nbsp; Tanya Stok &amp; Order via WhatsApp</a>'
        f'</div></div>'
    )


# ══════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════
qp = st.query_params
default_kw = qp.get("q", "")

if "cat" in qp:
    st.session_state.cat = qp["cat"]
elif "cat" not in st.session_state:
    st.session_state.cat = "Semua"

selected = st.session_state.cat

# ══════════════════════════════════════════════════════════════
# LOAD DATA
# ══════════════════════════════════════════════════════════════
df = pd.DataFrame()
if os.path.exists(CSV_PATH):
    df = load_data(CSV_PATH)
    if not df.empty:
        df["Jenis"] = df["Jenis"].astype(str).str.strip()

total_produk   = df.groupby("Kode Item").ngroups if not df.empty else 0
total_kategori = df["Jenis"].nunique()            if not df.empty else 0
total_grosir   = int((df["Harga Grosir"] > 0).sum()) if not df.empty else 0
all_cats       = sorted(df["Jenis"].unique().tolist()) if not df.empty else []

# ══════════════════════════════════════════════════════════════
# SEARCH
# ══════════════════════════════════════════════════════════════
keyword = st.text_input(
    "🔍 Cari Barang",
    value=default_kw,          # ← restore keyword setelah chip click (page reload)
    placeholder="Ketik nama barang… contoh: mie, gula, sabun",
    key="kw",                  # ← key stabil agar state tidak hilang saat rerun / Enter
)

# ══════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════
logo_b64 = get_logo_b64(LOGO_PATH)
logo_tag  = (
    f'<img class="hero-logo" src="data:image/jpeg;base64,{logo_b64}" alt="ILMIGROSIR"/>'
    if logo_b64 else
    '<div style="font-size:28px;font-weight:900;color:#fff;">ILMIGROSIR</div>'
)
st.html(f"""
<div class="hero">
  {logo_tag}
  <div class="hero-tagline">✦ Katalog Harga Publik ✦</div>
  <div class="hero-sub">Jual Lagi, Untung Kembali</div>
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


if df.empty:
    st.error("Database tidak ditemukan. Upload lewat Menu Admin.")
    st.stop()



# ══════════════════════════════════════════════════════════════
# CATEGORY CHIPS — pure HTML slide, JS sets query param → rerun
# ══════════════════════════════════════════════════════════════
selected = st.session_state.cat
cat_list = ["Semua"] + all_cats

chips_html = ""
for cat in cat_list:
    icon     = "🛒" if cat == "Semua" else cat_icon(cat)
    is_act   = "active" if cat == selected else ""
    # Escape for JS string (single-quote safe)
    cat_js   = cat.replace("'", "\\'")
    chips_html += (
        f'<div class="chip {is_act}" onclick="selectCat(\'{cat_js}\')">'
        f'<span class="chip-icon">{icon}</span>{cat}'
        f'</div>'
    )

st.html(f"""
<div class="chips-wrap">
  <span class="chips-label">📂 Pilih Kategori</span>
  <div class="chips-scroll" id="chipsScroll">
    {chips_html}
  </div>
</div>

<script>
function selectCat(cat) {{
  // ── PENTING: st.html() berjalan di dalam iframe.
  //    window.location = iframe itu sendiri (bukan Streamlit).
  //    Harus gunakan window.PARENT.location agar URL Streamlit berubah ──
  const url = new URL(window.parent.location.href);
  url.searchParams.set('cat', cat);

  // ── Baca nilai search dari parent Streamlit dan ikutkan ke URL ──
  var searchVal = '';
  try {{
    var inputs = window.parent.document.querySelectorAll('input[type="text"]');
    for (var i = 0; i < inputs.length; i++) {{
      var ph = inputs[i].placeholder || '';
      if (ph.indexOf('nama barang') !== -1 || ph.indexOf('Ketik') !== -1) {{
        searchVal = inputs[i].value || '';
        break;
      }}
    }}
  }} catch(e) {{}}

  if (searchVal.trim()) {{
    url.searchParams.set('q', searchVal.trim());
  }} else {{
    url.searchParams.delete('q');
  }}

  window.parent.location.href = url.toString();
}}

// Auto-scroll active chip into view
const active = document.querySelector('.chip.active');
if (active) {{
  setTimeout(() => active.scrollIntoView({{behavior:'smooth', block:'nearest', inline:'center'}}), 50);
}}
</script>
""")
# ══════════════════════════════════════════════════════════════
# FILTER PRODUCTS (PERBAIKAN)
# ══════════════════════════════════════════════════════════════
filtered = df.copy()

# 1. Filter Kategori (Rata Kiri)
if selected != "Semua":
    # Gunakan strip dan lower agar perbandingan teks akurat
    filtered = filtered[filtered["Jenis"].str.strip().str.lower() == selected.strip().lower()]

# 2. Filter Pencarian/Keyword (Rata Kiri)
if keyword.strip():
    filtered = filtered[filtered["Nama Item"].str.contains(keyword.strip(), case=False, na=False)]

# 3. Pengelompokan (Wajib Rata Kiri agar selalu jalan)
groups          = filtered.groupby(["Kode Item", "Nama Item", "Jenis"], sort=False)
unique_products = list(groups)
n               = len(unique_products)

# ══════════════════════════════════════════════════════════════
# RESULT STRIP & CARDS (LANJUTAN KE BAWAH)
# ══════════════════════════════════════════════════════════════
if selected != "Semua":
    badge = f'<span class="active-badge">{cat_icon(selected)} {selected}</span>'
else:
    badge = ""

hint = "Coba kata lain" if n == 0 else "Scroll untuk lihat semua"

st.html(f"""
<div class="result-strip">
  <span class="result-count">
    {'Tidak ada' if n == 0 else f'{n:,}'} produk {badge}
  </span>
  <span class="result-hint">{hint}</span>
</div>
""")

# Bagian Cards tetap seperti kode asli Anda
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
    parts.append("</div>")
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
        st.info(f"📱 Nomor WA: `{WA_NUMBER}` — Edit baris 18 file `app.py`")
    elif pw:
        st.error("❌ Password salah.")


# ══════════════════════════════════════════════════════════════
# FOOTERimport streamlit as st
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
WA_NUMBER      = "6281234567890"

CATEGORY_ICONS = {
    "MIE INSTANT":"🍜","MIE CUP":"🍜","MIE OLAH":"🍜",
    "BERAS":"🌾","GULA":"🍚","MINYAK":"🫙",
    "KOPI":"☕","TEH":"🍵","SIRUP":"🧃",
    "SUSU UHT":"🥛","SUSU SKM":"🥛","SUSU FORMULA":"🍼",
    "SNACK":"🍿","CANDY":"🍬","CKLT BTG":"🍫",
    "SARDEN":"🐟","SAOS":"🫙","KECAP":"🫙",
    "BUMBU INSTANT":"🧂","MICIN":"🧂","GARAM":"🧂",
    "TERIGU":"🌾","BHN KUE":"🧁","BIHUN":"🍝",
    "ROKOK":"🚬","BHN ROKOK":"🚬",
    "DETERJEN":"🧺","RINSO BUBUK":"🧺","RINSO CAIR":"🧴",
    "SHAMPO":"🧴","SBN MANDI BTG":"🧼","REFIL/SBN MNDI":"🧴",
    "PSTA/SKT GIGI":"🪥","SABUN COLEK":"🧼","SBN LANTAI":"🫧",
    "TISU":"🧻","PEMBALUT":"🩹","POPOK":"👶",
    "OBAT":"💊","OBAT NYAMUK":"🦟",
    "COSMETIC":"💄","PRFM":"🌸",
    "PEWANGI RUANGAN":"🌺","MOLTO REF":"🌸","MOLTO RCG":"🌸","SOKLIN RCG":"🧴",
    "MNM":"🥤","MNM 1000":"💧","MNM RCG":"🥤",
    "MKAN":"🍱","MKCG":"🍱","MKN BYI":"🍱",
    "CUCI MULUT":"🍮","KEJU/MNTGA":"🧈",
    "GAS":"🔵","PLASTIK":"🛍️","KERTAS NASI":"📄",
    "ATK":"✏️","ALT":"🔧","ALT BYI":"🔧",
    "BAHAN DAPUR":"🥘","KATEMBAT":"🌿",
    "KRPK":"🥨","TERASI":"🦐","MAYONIES":"🥣","ACI":"🌽",
    "CURAH":"⚖️","SBN ALT MKN":"🍽️",
}

def cat_icon(j): return CATEGORY_ICONS.get(j.upper(), "📦")

# ══════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Sora:wght@700;800&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html,body,[class*="css"]{
    font-family:'Plus Jakarta Sans',sans-serif !important;
    background:#F0F4FF !important;
}
.block-container{padding:0 !important;max-width:480px !important;margin:0 auto !important;}
#MainMenu,footer,header,.stDeployButton{display:none !important;}
.stAppHeader{display:none !important;}

/* HERO */
.hero{
    background:linear-gradient(160deg,#0A1628 0%,#0D2461 55%,#1545A8 100%);
    padding:24px 20px 20px;text-align:center;position:relative;overflow:hidden;
}
.hero::before{content:'';position:absolute;top:-40px;right:-40px;width:200px;height:200px;
    border-radius:50%;background:radial-gradient(circle,rgba(255,215,0,.12) 0%,transparent 70%);}
.hero::after{content:'';position:absolute;bottom:-30px;left:-30px;width:160px;height:160px;
    border-radius:50%;background:radial-gradient(circle,rgba(37,99,235,.25) 0%,transparent 70%);}
.hero-logo{max-width:220px;border-radius:12px;box-shadow:0 8px 32px rgba(0,0,0,.4);
    position:relative;z-index:1;margin-bottom:12px;}
.hero-tagline{color:#FFD700;font-size:11px;font-weight:700;letter-spacing:2.5px;
    text-transform:uppercase;position:relative;z-index:1;}
.hero-sub{color:rgba(255,255,255,.5);font-size:10px;margin-top:4px;
    position:relative;z-index:1;letter-spacing:.5px;}

/* STATS */
.stats-bar{display:flex;background:#fff;border-bottom:1px solid #E8EDF8;padding:10px 0;}
.stat-item{flex:1;text-align:center;border-right:1px solid #E8EDF8;}
.stat-item:last-child{border-right:none;}
.stat-num{font-size:17px;font-weight:800;color:#0D2461;display:block;line-height:1;}
.stat-label{font-size:9px;color:#94A3B8;font-weight:700;text-transform:uppercase;
    letter-spacing:.8px;display:block;margin-top:2px;}

/* SEARCH */
.stTextInput>div>div>input{
    border:2px solid #E2E8F8 !important;border-radius:12px !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
    font-size:14px !important;font-weight:500 !important;
    color:#0D2461 !important;padding:10px 14px !important;
    background:#F8FAFF !important;box-shadow:none !important;
}
.stTextInput>div>div>input:focus{
    border-color:#1545A8 !important;background:#fff !important;
    box-shadow:0 0 0 3px rgba(21,69,168,.1) !important;
}
.stTextInput>label{
    font-size:11px !important;font-weight:700 !important;color:#64748B !important;
    letter-spacing:.8px !important;text-transform:uppercase !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
}

/* ════════════════════════════════════════
   CHIPS via st.radio — NO JS, NO IFRAME
   ════════════════════════════════════════ */

/* Bungkus stRadio: styling kotak putih chip row */
div[data-testid="stRadio"]{
    background:#fff !important;
    padding:0 0 10px 0 !important;
    border-bottom:5px solid #F0F4FF !important;
    margin-bottom:0 !important;
}

/* Sembunyikan label bawaan ("Pilih Kategori") */
div[data-testid="stRadio"] > label{
    display:none !important;
}

/* Row chip: horizontal scroll tanpa wrap */
div[data-testid="stRadio"] div[role="radiogroup"]{
    display:flex !important;
    flex-wrap:nowrap !important;
    overflow-x:auto !important;
    gap:8px !important;
    padding:2px 14px 4px !important;
    scrollbar-width:none !important;
    -ms-overflow-style:none !important;
    -webkit-overflow-scrolling:touch !important;
    align-items:center !important;
}
div[data-testid="stRadio"] div[role="radiogroup"]::-webkit-scrollbar{
    display:none !important;
}

/* Setiap opsi (label wrapper) → tampak sebagai chip */
div[data-testid="stRadio"] div[role="radiogroup"] > label{
    flex:0 0 auto !important;
    display:inline-flex !important;
    align-items:center !important;
    gap:5px !important;
    padding:8px 14px !important;
    border-radius:50px !important;
    font-size:12px !important;
    font-weight:700 !important;
    white-space:nowrap !important;
    border:2px solid #E2E8F8 !important;
    background:#F8FAFF !important;
    color:#475569 !important;
    cursor:pointer !important;
    transition:all .18s cubic-bezier(.4,0,.2,1) !important;
    margin:0 !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
    user-select:none !important;
    min-height:unset !important;
    height:auto !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] > label:hover{
    border-color:#1545A8 !important;
    color:#1545A8 !important;
}

/* Chip AKTIF — :has() didukung Chrome 105+, Edge 105+, FF 121+, Safari 15.4+ */
div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input[type="radio"]:checked){
    background:linear-gradient(135deg,#0D2461 0%,#1545A8 100%) !important;
    border-color:#0D2461 !important;
    color:#fff !important;
    box-shadow:0 4px 14px rgba(13,36,97,.3) !important;
}

/* Sembunyikan radio circle bawaan Streamlit */
div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child{
    display:none !important;
}

/* Teks di dalam label chip */
div[data-testid="stRadio"] div[role="radiogroup"] > label > div:last-child,
div[data-testid="stRadio"] div[role="radiogroup"] > label > div:last-child p{
    font-size:12px !important;
    font-weight:700 !important;
    color:inherit !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
    margin:0 !important;
    line-height:1.2 !important;
}

/* chips header label */
.chips-header{
    background:#fff;
    padding:10px 14px 6px;
}
.chips-label{
    font-size:10px;font-weight:800;color:#94A3B8;
    letter-spacing:1px;text-transform:uppercase;display:block;
}

/* RESULT STRIP */
.result-strip{
    display:flex;align-items:center;justify-content:space-between;
    padding:10px 16px;background:#EEF2FF;border-bottom:1px solid #DDE5FF;
}
.result-count{font-size:12px;font-weight:700;color:#1545A8;}
.result-hint{font-size:10px;color:#94A3B8;font-weight:500;}
.active-badge{
    display:inline-flex;align-items:center;gap:4px;
    font-size:10px;background:#0D2461;color:#fff;
    border-radius:6px;padding:2px 8px;font-weight:700;margin-left:6px;
}

/* CATALOG */
.catalog-feed{padding:12px 14px 0;background:#F0F4FF;}

/* PRODUCT CARD */
.pcard{
    background:#fff;border-radius:16px;margin-bottom:12px;overflow:hidden;
    box-shadow:0 1px 4px rgba(13,36,97,.06),0 4px 16px rgba(13,36,97,.04);
    border:1px solid #E8EDF8;
}
.pcard-header{
    padding:14px 16px 10px;border-bottom:1px solid #F1F5FD;
    background:linear-gradient(135deg,#F8FAFF 0%,#fff 100%);
}
.pcard-badges{display:flex;align-items:center;gap:6px;margin-bottom:8px;flex-wrap:wrap;}
.badge-jenis{
    font-size:9px;font-weight:800;letter-spacing:1.2px;text-transform:uppercase;
    color:#1545A8;background:#EEF2FF;border:1px solid #C7D4FF;border-radius:6px;padding:3px 8px;
}
.badge-grosir{
    font-size:9px;font-weight:800;letter-spacing:.8px;text-transform:uppercase;
    color:#92400E;background:linear-gradient(90deg,#FEF3C7,#FDE68A);
    border:1px solid #F59E0B;border-radius:6px;padding:3px 8px;
}
.pcard-name{font-size:14px;font-weight:700;color:#0A1628;line-height:1.35;letter-spacing:-.1px;}
.pcard-kode{font-size:10px;color:#94A3B8;font-weight:500;margin-top:3px;}
.price-row{display:flex;align-items:center;padding:12px 16px;border-bottom:1px solid #F8FAFF;}
.price-row:last-child{border-bottom:none;}
.price-row:nth-child(even){background:#FAFCFF;}
.price-row-left{flex:1;}
.satuan-pill{
    display:inline-flex;align-items:center;gap:5px;
    background:#0D2461;color:#fff;
    font-size:11px;font-weight:700;border-radius:8px;
    padding:4px 10px;letter-spacing:.5px;margin-bottom:3px;
}
.isi-label{font-size:10px;color:#94A3B8;font-weight:500;}
.price-row-right{text-align:right;}
.price-retail{
    font-size:19px;font-weight:800;color:#0D2461;
    font-family:'Sora',sans-serif;line-height:1;letter-spacing:-.5px;
}
.price-grosir-wrap{margin-top:4px;}
.price-grosir{font-size:15px;font-weight:800;color:#DC2626;font-family:'Sora',sans-serif;}
.grosir-pill{
    font-size:8px;font-weight:800;color:#92400E;
    background:#FEF3C7;border:1px solid #F59E0B;
    border-radius:4px;padding:2px 5px;margin-left:4px;letter-spacing:.5px;
}
.hemat-pill{
    display:inline-block;font-size:9px;font-weight:700;
    color:#065F46;background:#ECFDF5;border:1px solid #6EE7B7;
    border-radius:4px;padding:2px 6px;margin-top:3px;
}
.wa-btn-wrap{padding:12px 14px;background:#F8FAFF;border-top:1px solid #EEF2FF;}
.wa-btn{
    display:flex;align-items:center;justify-content:center;gap:8px;
    background:linear-gradient(135deg,#22C55E 0%,#16A34A 100%);
    color:#fff !important;text-decoration:none !important;
    border-radius:12px;padding:13px 16px;font-size:13px;font-weight:700;
    font-family:'Plus Jakarta Sans',sans-serif;
    box-shadow:0 4px 14px rgba(22,163,74,.28);
}
.empty-state{text-align:center;padding:48px 24px;color:#94A3B8;}
.empty-icon{font-size:48px;margin-bottom:12px;display:block;}
.empty-title{font-size:16px;font-weight:700;color:#475569;}
.empty-sub{font-size:13px;margin-top:6px;line-height:1.6;}
.section-divider{height:6px;background:#F0F4FF;border-top:1px solid #E8EDF8;border-bottom:1px solid #E8EDF8;}
.app-footer{text-align:center;padding:20px 16px 28px;background:#fff;
    border-top:1px solid #E8EDF8;margin-top:8px;}
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

def wa_link(name):
    msg = (f"Halo Kak, saya mau tanya stok barang ini di ILMIGROSIR:\n\n"
           f"* {name} *\n\nApakah tersedia? Berapa minimum ordernya? Terima kasih")
    return f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(msg)}"

@st.cache_data(show_spinner=False)
def load_data(path):
    df = pd.read_csv(path)
    for col in ["Harga Retail","Harga Grosir","Harga Pokok"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    df["Konversi"] = pd.to_numeric(df["Konversi"], errors="coerce").fillna(1)
    for col in ["Nama Item","Jenis","Satuan","Kode Item"]:
        df[col] = df[col].astype(str).str.strip()
    return df

def get_logo_b64(path):
    if os.path.exists(path):
        with open(path,"rb") as f: return base64.b64encode(f.read()).decode()
    return ""

def build_card(kode, nama, jenis, group_df):
    rows_html = ""; has_grosir = False
    for _, row in group_df.iterrows():
        satuan   = row["Satuan"]; konversi = int(row["Konversi"])
        retail   = row["Harga Retail"]; grosir = row["Harga Grosir"]
        isi      = f"Isi {konversi} pcs" if konversi > 1 else "Satuan terkecil"
        r_str    = fmt_price(retail) if retail > 0 else "–"
        g_html   = ""
        if grosir > 0 and grosir < retail:
            has_grosir = True
            selisih    = retail - grosir
            pct        = round(selisih / retail * 100, 1)
            g_html = (
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
            f'<div class="price-retail">{r_str}</div>{g_html}'
            f'</div></div>'
        )
    gb   = '<span class="badge-grosir">⭐ Harga Grosir</span>' if has_grosir else ""
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
        f'💬&nbsp; Tanya Stok &amp; Order via WhatsApp</a>'
        f'</div></div>'
    )


# ══════════════════════════════════════════════════════════════
# LOAD DATA
# ══════════════════════════════════════════════════════════════
df = pd.DataFrame()
if os.path.exists(CSV_PATH):
    df = load_data(CSV_PATH)
    if not df.empty:
        df["Jenis"] = df["Jenis"].astype(str).str.strip()

total_produk   = df.groupby("Kode Item").ngroups if not df.empty else 0
total_kategori = df["Jenis"].nunique()            if not df.empty else 0
total_grosir   = int((df["Harga Grosir"] > 0).sum()) if not df.empty else 0
all_cats       = sorted(df["Jenis"].unique().tolist()) if not df.empty else []


# ══════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════
logo_b64 = get_logo_b64(LOGO_PATH)
logo_tag  = (
    f'<img class="hero-logo" src="data:image/jpeg;base64,{logo_b64}" alt="ILMIGROSIR"/>'
    if logo_b64 else
    '<div style="font-size:28px;font-weight:900;color:#fff;">ILMIGROSIR</div>'
)
st.html(f"""
<div class="hero">
  {logo_tag}
  <div class="hero-tagline">✦ Katalog Harga Publik ✦</div>
  <div class="hero-sub">Jual Lagi, Untung Kembali</div>
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

if df.empty:
    st.error("Database tidak ditemukan. Upload lewat Menu Admin.")
    st.stop()


# ══════════════════════════════════════════════════════════════
# SEARCH
# ══════════════════════════════════════════════════════════════
keyword = st.text_input(
    "🔍 Cari Barang",
    placeholder="Ketik nama barang… contoh: mie, gula, sabun",
    key="kw",
)


# ══════════════════════════════════════════════════════════════
# CATEGORY CHIPS — st.radio NATIVE (ZERO JS, ZERO IFRAME)
# ══════════════════════════════════════════════════════════════
# ✅ Kenapa ini bekerja 100%:
#    • st.radio adalah widget Streamlit asli (bukan HTML inject)
#    • Saat diklik → Streamlit langsung rerun Python → filter jalan
#    • Tidak ada iframe sandbox, tidak ada JS, tidak ada page reload
#    • State chip tersimpan otomatis oleh Streamlit via key="cat_radio"
#    • Search input tetap utuh karena hanya rerun (bukan page reload)
# ══════════════════════════════════════════════════════════════

cat_list    = ["Semua"] + all_cats
cat_display = ["🛒 Semua"] + [f"{cat_icon(c)} {c}" for c in all_cats]

# Header label chip (HTML statik, tanpa logika)
st.markdown(
    '<div class="chips-header"><span class="chips-label">📂 Pilih Kategori</span></div>',
    unsafe_allow_html=True,
)

# Pilihan kategori sebagai radio horizontal (ditampilkan sebagai chip via CSS)
chosen_display = st.radio(
    "Pilih Kategori",
    options=cat_display,
    horizontal=True,
    label_visibility="collapsed",
    key="cat_radio",
)

# Petakan label tampilan → nama kategori asli
chosen_idx = cat_display.index(chosen_display)
selected   = cat_list[chosen_idx]


# ══════════════════════════════════════════════════════════════
# FILTER PRODUK
# ══════════════════════════════════════════════════════════════
filtered = df.copy()

# 1. Filter kategori (case-insensitive, strip whitespace)
if selected != "Semua":
    mask     = df["Jenis"].str.strip().str.lower() == selected.strip().lower()
    filtered = filtered[mask]

# 2. Filter keyword pencarian
kw = keyword.strip()
if kw:
    filtered = filtered[
        filtered["Nama Item"].str.contains(kw, case=False, na=False)
    ]

# 3. Kelompokkan per produk unik
groups          = filtered.groupby(["Kode Item", "Nama Item", "Jenis"], sort=False)
unique_products = list(groups)
n               = len(unique_products)


# ══════════════════════════════════════════════════════════════
# RESULT STRIP
# ══════════════════════════════════════════════════════════════
badge = (
    f'<span class="active-badge">{cat_icon(selected)} {selected}</span>'
    if selected != "Semua" else ""
)
hint = "Coba kata lain" if n == 0 else "Scroll untuk lihat semua"

st.html(f"""
<div class="result-strip">
  <span class="result-count">
    {'Tidak ada' if n == 0 else f'{n:,}'} produk{badge}
  </span>
  <span class="result-hint">{hint}</span>
</div>
""")


# ══════════════════════════════════════════════════════════════
# PRODUCT CARDS
# ══════════════════════════════════════════════════════════════
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
    parts.append("</div>")
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
        st.info(f"📱 Nomor WA: `{WA_NUMBER}` — Edit variabel WA_NUMBER di file `app.py`")
    elif pw:
        st.error("❌ Password salah.")


# ══════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════
st.html("""
<div class="app-footer">
  <div class="footer-brand">ILMIGROSIR</div>
  <div class="footer-tagline">Jual Lagi, Untung Kembali</div>
  <div class="footer-dev">Developed with ❤️ by <span>NOPAL TECH</span></div>
</div>
""")

# ══════════════════════════════════════════════════════════════
st.html("""
<div class="app-footer">
  <div class="footer-brand">ILMIGROSIR</div>
  <div class="footer-tagline">Jual Lagi, Untung Kembali</div>
  <div class="footer-dev">Developed with ❤️ by <span>NOPAL TECH</span></div>
</div>
""")
