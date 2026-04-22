import streamlit as st
import pandas as pd
import base64, os, urllib.parse, datetime, html as htmllib

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
WA_NUMBER      = "6285373373233"

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

def cat_icon(j):
    return CATEGORY_ICONS.get(str(j).upper(), "📦")

# ══════════════════════════════════════════════════════════════
# SESSION STATE & QUERY PARAMS — baca di awal
# ══════════════════════════════════════════════════════════════
if "page" not in st.session_state:
    st.session_state.page = "home"
if "admin_auth" not in st.session_state:
    st.session_state.admin_auth = False

qp = st.query_params
if "page" in qp and qp["page"] in ("home", "catalog", "admin"):
    st.session_state.page = qp["page"]

page = st.session_state.page

# ══════════════════════════════════════════════════════════════
# GLOBAL CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Barlow+Condensed:wght@600;700;800;900&display=swap');

/* ── SEMBUNYIKAN BRANDING STREAMLIT ── */
#MainMenu          { visibility: hidden !important; }
footer             { visibility: hidden !important; }
header             { visibility: hidden !important; }
.stDeployButton    { display: none !important; }
[data-testid="stDecoration"]   { display: none !important; }
[data-testid="stToolbar"]      { display: none !important; }
[data-testid="stStatusWidget"] { display: none !important; }
.viewerBadge_container__1QSob  { display: none !important; }
.st-emotion-cache-1dp5vir      { display: none !important; }
.st-emotion-cache-zq5wmm       { display: none !important; }
[class*="viewerBadge"]         { display: none !important; }
[class*="StatusWidget"]        { display: none !important; }
[class*="DeployButton"]        { display: none !important; }

/* ── CSS VARIABLES ── */
:root {
    --red:    #E31E24; --red-dk: #B01519; --red-lt:    #FFF0F0;
    --blue:   #1B3FA0; --blue-md:#2554C7; --blue-lt:   #EBF0FB;
    --yellow: #F5C400; --ydk:    #C49A00; --yellow-lt: #FFFBEA;
    --white:  #FFFFFF; --bg:     #F0F4FB; --border:    #DDE3F0;
    --text:   #0E1B3D; --muted:  #6B7A99;
    --green:  #15803D; --green-lt:#DCFCE7;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif !important;
    background: #B8C5DF !important;
}

.block-container {
    padding: 0 !important;
    max-width: 480px !important;
    margin: 0 auto !important;
    background: var(--bg) !important;
    min-height: 100vh;
    overflow-x: hidden;
    box-shadow: 0 0 80px rgba(27,63,160,.20);
    padding-bottom: 86px !important;
}
.main .block-container { padding-top: 0 !important; }
[data-testid="stAppViewContainer"] { background: #B8C5DF !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }
[data-testid="stVerticalBlock"] > div { padding: 0 !important; margin: 0 !important; }

/* ══ BOTTOM NAV ══ */
.bnav {
    position: fixed; bottom: 0; left: 50%;
    transform: translateX(-50%);
    width: 100%; max-width: 480px;
    background: rgba(255,255,255,.97);
    backdrop-filter: blur(16px);
    border-top: 1.5px solid var(--border);
    display: flex; z-index: 9999;
    box-shadow: 0 -4px 20px rgba(27,63,160,.10);
}
.bnav-a {
    flex: 1; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 10px 0 13px; gap: 3px;
    text-decoration: none !important;
    position: relative;
    -webkit-tap-highlight-color: transparent;
}
.bnav-a .ni { font-size: 22px; line-height: 1; transition: transform .2s; }
.bnav-a .nl { font-size: 10px; font-weight: 800; color: var(--muted); font-family: 'Nunito', sans-serif; transition: color .2s; }
.bnav-a.on  .nl { color: var(--blue); }
.bnav-a.on  .ni { transform: translateY(-2px); }
.bnav-a.adm.on .nl { color: var(--red); }
.bnav-a.on::after {
    content: ''; position: absolute;
    top: 0; left: 50%; transform: translateX(-50%);
    width: 36px; height: 3px;
    background: var(--blue); border-radius: 0 0 4px 4px;
    animation: barIn .25s ease;
}
.bnav-a.adm.on::after { background: var(--red); }
@keyframes barIn { from{width:0;opacity:0} to{width:36px;opacity:1} }

/* ══ TOMBOL KEMBALI ══ */
.back-btn {
    position: fixed; top: 14px; left: 14px;
    z-index: 9998;
    width: 42px; height: 42px; border-radius: 50%;
    background: rgba(255,255,255,.93);
    border: 1.5px solid var(--border);
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 3px 14px rgba(27,63,160,.14);
    text-decoration: none !important;
    font-size: 20px; color: var(--blue) !important;
    font-weight: 900; line-height: 1;
    -webkit-tap-highlight-color: transparent;
}
.back-btn:active { opacity: .8; }

/* ══ STRIPE ANIMASI ══ */
.stripe {
    height: 4px;
    background: linear-gradient(90deg, var(--red) 0%, var(--yellow) 50%, var(--red) 100%);
    background-size: 200%;
    animation: stripeMove 3s linear infinite;
}
@keyframes stripeMove { 0%{background-position:0%} 100%{background-position:200%} }

/* ══ HERO (HOME) ══ */
.hero {
    background: linear-gradient(155deg, #0D2785 0%, #1B3FA0 45%, #0A1E6B 100%);
    position: relative; overflow: hidden;
}
.hero-in { padding: 26px 22px 84px; position: relative; z-index: 2; }
.hero::before {
    content:''; position:absolute; width:260px; height:260px; border-radius:50%;
    background:radial-gradient(circle,rgba(245,196,0,.09) 0%,transparent 65%);
    top:-70px; right:-70px; pointer-events:none;
}
.hero::after {
    content:''; position:absolute; width:140px; height:140px; border-radius:50%;
    background:radial-gradient(circle,rgba(227,30,36,.10) 0%,transparent 65%);
    bottom:10px; left:-40px; pointer-events:none;
}
.logo-box {
    display: inline-block; background: #fff; border-radius: 14px;
    padding: 9px 16px; border: 3px solid var(--yellow);
    box-shadow: 0 6px 22px rgba(0,0,0,.22), 0 0 0 6px rgba(245,196,0,.12);
    margin-bottom: 20px;
}
.logo-box img  { height: 44px; display: block; }
.logo-box span { font-family:'Barlow Condensed',sans-serif; font-size:28px; font-weight:900; color:var(--red); }
.hero-greet { font-size:11px; font-weight:800; color:rgba(255,255,255,.55); letter-spacing:1.5px; text-transform:uppercase; margin-bottom:6px; }
.hero-h1    { font-family:'Barlow Condensed',sans-serif; font-size:34px; font-weight:900; color:#fff; line-height:1.1; margin-bottom:10px; }
.hero-h1 em { color:var(--yellow); font-style:normal; }
.hero-sub   { font-size:13px; color:rgba(255,255,255,.58); font-weight:600; line-height:1.65; margin-bottom:24px; max-width:300px; }
.cta-row    { display:flex; gap:10px; }
.cta-a {
    flex:1.2; background:var(--yellow); color:var(--blue) !important;
    text-decoration:none !important; padding:13px 16px; border-radius:13px;
    font-size:13px; font-weight:900; text-align:center;
    box-shadow:0 5px 18px rgba(245,196,0,.38);
    -webkit-tap-highlight-color:transparent;
}
.cta-b {
    flex:1; background:rgba(255,255,255,.10); color:#fff !important;
    text-decoration:none !important; padding:13px 16px; border-radius:13px;
    font-size:13px; font-weight:800; text-align:center;
    border:1.5px solid rgba(255,255,255,.20);
    -webkit-tap-highlight-color:transparent;
}

/* Stats band */
.stats-band {
    background:#fff; margin:-38px 16px 0; border-radius:20px;
    position:relative; z-index:10; display:flex;
    box-shadow:0 10px 36px rgba(27,63,160,.12); border:1.5px solid var(--border); overflow:hidden;
}
.stat-item { flex:1; text-align:center; padding:18px 8px; border-right:1.5px solid var(--border); }
.stat-item:last-child { border-right:none; }
.stat-num  { font-family:'Barlow Condensed',sans-serif; font-size:26px; font-weight:900; display:block; line-height:1; margin-bottom:4px; }
.stat-lbl  { font-size:9.5px; font-weight:800; color:var(--muted); text-transform:uppercase; letter-spacing:.6px; }
.dot       { width:5px; height:5px; border-radius:50%; margin:0 auto 5px; }

/* Section head */
.sec-hd { display:flex; align-items:center; justify-content:space-between; padding:22px 18px 12px; }
.sec-ttl { font-family:'Barlow Condensed',sans-serif; font-size:22px; font-weight:800; color:var(--text); }
.sec-ttl em { color:var(--red); font-style:normal; }
.sec-more {
    font-size:11px; font-weight:800; color:var(--blue);
    background:var(--blue-lt); padding:5px 14px; border-radius:100px;
    text-decoration:none !important; -webkit-tap-highlight-color:transparent;
}

/* Feature cards */
.feat-row { display:flex; gap:12px; padding:0 16px 22px; overflow-x:auto; scrollbar-width:none; }
.feat-row::-webkit-scrollbar { display:none; }
.feat-card {
    flex:0 0 144px; background:#fff; border-radius:18px; padding:16px 14px;
    border:1.5px solid var(--border); box-shadow:0 2px 10px rgba(27,63,160,.05);
    display:flex; flex-direction:column; gap:10px; text-decoration:none !important;
    -webkit-tap-highlight-color:transparent;
}
.fi    { width:48px; height:48px; border-radius:14px; display:flex; align-items:center; justify-content:center; font-size:24px; }
.fi-b  { background:var(--blue-lt); }   .fi-r { background:var(--red-lt); }
.fi-y  { background:var(--yellow-lt); } .fi-g { background:var(--green-lt); }
.ft    { font-size:13px; font-weight:900; color:var(--text); margin-bottom:2px; }
.fs    { font-size:11px; color:var(--muted); font-weight:600; line-height:1.45; }

/* Cat grid */
.cat-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:10px; padding:0 16px 22px; }
.cat-box  {
    display:flex; flex-direction:column; align-items:center; gap:6px;
    background:#fff; border-radius:16px; padding:13px 6px;
    border:1.5px solid var(--border); text-decoration:none !important;
    -webkit-tap-highlight-color:transparent;
}
.cat-box:active { background:var(--blue-lt); }
.cat-em { font-size:24px; }
.cat-nm { font-size:9px; font-weight:900; color:var(--text); text-align:center; line-height:1.3; text-transform:uppercase; letter-spacing:.3px; }

/* WA Banner */
.wa-ban {
    margin:4px 16px 26px;
    background:linear-gradient(135deg,#22C55E 0%,#128C4F 50%,#075E54 100%);
    border-radius:20px; padding:18px; display:flex; gap:14px; align-items:center;
    box-shadow:0 7px 24px rgba(7,94,84,.25); text-decoration:none !important;
    -webkit-tap-highlight-color:transparent;
}
.wa-ban:active { opacity:.92; }
.wa-ico { font-size:40px; flex-shrink:0; }
.wa-ttl { font-family:'Barlow Condensed',sans-serif; font-size:18px; font-weight:800; color:#fff; margin-bottom:2px; }
.wa-sub { font-size:12px; color:rgba(255,255,255,.70); font-weight:600; }
.wa-arr { margin-left:auto; font-size:22px; color:rgba(255,255,255,.50); flex-shrink:0; }

/* ══ CATALOG HERO ══ */
.cat-hero { background:linear-gradient(150deg,#1B3FA0 0%,#0D2785 100%); position:relative; overflow:hidden; }
.cat-hero-in { padding:22px 20px 32px; position:relative; z-index:2; }
.cat-hero::before {
    content:''; position:absolute; width:180px; height:180px; border-radius:50%;
    background:rgba(245,196,0,.07); top:-50px; right:-50px; pointer-events:none;
}
.cat-lbl  { font-size:10px; font-weight:800; color:rgba(255,255,255,.50); text-transform:uppercase; letter-spacing:2px; margin-bottom:4px; }
.cat-ttl  { font-family:'Barlow Condensed',sans-serif; font-size:32px; font-weight:900; color:#fff; }
.cat-ttl em { color:var(--yellow); font-style:normal; }

/* Search */
div[data-testid="stTextInput"] { padding:0 14px !important; margin:0 !important; }
.stTextInput > div > div > input {
    border:none !important; border-radius:14px !important;
    font-size:14px !important; font-weight:700 !important;
    color:var(--text) !important; padding:14px 18px !important;
    background:#fff !important;
    box-shadow:0 5px 20px rgba(27,63,160,.11) !important;
    border:1.5px solid transparent !important;
    font-family:'Nunito',sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color:var(--blue-md) !important;
    box-shadow:0 0 0 3px rgba(27,63,160,.10),0 5px 20px rgba(27,63,160,.08) !important;
}
.stTextInput > div > div > input::placeholder { color:#9AA4C0 !important; font-weight:600 !important; }
.stTextInput > label { display:none !important; }
.search-wrap { margin-top:-24px; position:relative; z-index:5; padding-bottom:14px; }

/* Radio chips */
div[data-testid="stRadio"] { padding:0 !important; }
div[data-testid="stRadio"] > label { display:none !important; }
div[data-testid="stRadio"] div[role="radiogroup"] {
    display:flex !important; flex-wrap:nowrap !important;
    overflow-x:auto !important; gap:8px !important;
    padding:2px 14px 16px !important; scrollbar-width:none !important;
}
div[data-testid="stRadio"] div[role="radiogroup"]::-webkit-scrollbar { display:none !important; }
div[data-testid="stRadio"] div[role="radiogroup"] > label {
    flex:0 0 auto !important; display:inline-flex !important; align-items:center !important;
    padding:8px 16px !important; border-radius:100px !important;
    background:#fff !important; border:1.5px solid var(--border) !important;
    cursor:pointer !important; transition:all .18s !important;
    -webkit-tap-highlight-color:transparent !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
    background:var(--blue) !important; border-color:var(--blue) !important;
    box-shadow:0 4px 14px rgba(27,63,160,.28) !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child { display:none !important; }
div[data-testid="stRadio"] div[role="radiogroup"] > label p {
    font-size:12px !important; font-weight:800 !important; color:var(--muted) !important;
    margin:0 !important; font-family:'Nunito',sans-serif !important; white-space:nowrap !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) p { color:#fff !important; }

/* Result strip */
.res-strip { padding:4px 14px 12px; display:flex; align-items:center; justify-content:space-between; }
.res-lbl   { font-size:13px; font-weight:800; color:var(--text); }
.res-cnt   { background:var(--blue); color:#fff; padding:4px 14px; border-radius:100px; font-size:11px; font-weight:900; box-shadow:0 3px 10px rgba(27,63,160,.24); }

/* ══ PRODUCT CARD ══ */
.feed { padding:0 12px 28px; }
.pcard { background:#fff; border-radius:20px; margin-bottom:13px; box-shadow:0 2px 14px rgba(27,63,160,.07); border:1.5px solid var(--border); overflow:hidden; }
.pstripe { height:4px; background:linear-gradient(90deg,var(--blue) 0%,var(--red) 50%,var(--yellow) 100%); }
.pbody   { display:flex; padding:14px; gap:13px; border-bottom:1.5px dashed rgba(221,227,240,.7); align-items:flex-start; }
.picon   { width:58px; height:58px; background:var(--blue-lt); border-radius:15px; display:flex; align-items:center; justify-content:center; font-size:28px; flex-shrink:0; border:1.5px solid rgba(221,227,240,.6); }
.pinfo   { flex:1; min-width:0; }
.pbadges { display:flex; gap:6px; margin-bottom:7px; flex-wrap:wrap; }
.bdg     { font-size:9px; font-weight:900; padding:3px 8px; border-radius:6px; text-transform:uppercase; letter-spacing:.4px; }
.bdg-j   { background:var(--blue-lt); color:var(--blue); border:1px solid #C0D0F0; }
.bdg-g   { background:var(--yellow-lt); color:var(--ydk); border:1px solid #EED080; }
.ptitle  { font-size:14px; font-weight:900; color:var(--text); line-height:1.35; margin-bottom:5px; word-break:break-word; }
.pkode   { font-size:10px; color:var(--muted); font-weight:700; background:var(--bg); padding:2px 8px; border-radius:6px; display:inline-block; border:1px solid var(--border); }
.pvars   { background:#FAFBFF; }
.vrow    { display:flex; justify-content:space-between; align-items:center; padding:11px 14px; border-bottom:1px solid rgba(221,227,240,.6); }
.vrow:last-child { border-bottom:none; }
.vleft   { display:flex; flex-direction:column; gap:3px; }
.vsat    { font-size:13px; font-weight:800; color:var(--text); }
.visi    { font-size:10px; color:var(--muted); font-weight:700; }
.vright  { text-align:right; display:flex; flex-direction:column; align-items:flex-end; gap:5px; }
.vret    { font-family:'Barlow Condensed',sans-serif; font-size:22px; font-weight:800; color:var(--text); line-height:1; }
.vgbox   { display:flex; align-items:center; gap:5px; background:var(--red-lt); padding:4px 8px; border-radius:8px; border:1px solid #FFCCCC; }
.vglbl   { font-size:9px; font-weight:900; color:var(--red); text-transform:uppercase; }
.vgval   { font-family:'Barlow Condensed',sans-serif; font-size:14px; font-weight:800; color:var(--red-dk); }
.vghem   { font-size:9px; color:var(--green); font-weight:800; background:var(--green-lt); padding:2px 6px; border-radius:5px; }
.paction { padding:11px 13px; background:#fff; }
.btn-wa  {
    display:flex; align-items:center; justify-content:center; gap:8px; width:100%;
    background:linear-gradient(135deg,#22C55E 0%,#15803D 100%);
    color:#fff !important; text-decoration:none !important;
    padding:13px; border-radius:13px; font-size:13px; font-weight:800;
    box-shadow:0 4px 16px rgba(21,128,61,.25); font-family:'Nunito',sans-serif;
    -webkit-tap-highlight-color:transparent;
}
.btn-wa:active { opacity:.92; }

/* Empty state */
.empty     { text-align:center; padding:60px 20px; }
.empty-ico { font-size:64px; display:block; opacity:.28; margin-bottom:14px; }
.empty-ttl { font-size:18px; font-weight:900; color:var(--text); margin-bottom:8px; }
.empty-sub { font-size:13px; color:var(--muted); font-weight:600; line-height:1.6; }

/* ══ ADMIN ══ */
.admin-hero { background:linear-gradient(135deg,var(--red-dk) 0%,var(--red) 55%,#F04040 100%); position:relative; overflow:hidden; }
.admin-hero::before { content:''; position:absolute; width:220px; height:220px; border-radius:50%; background:rgba(255,255,255,.06); top:-65px; right:-65px; pointer-events:none; }
.admin-hero::after  { content:''; position:absolute; width:80px; height:80px; border:2px solid rgba(255,255,255,.08); border-radius:20px; bottom:16px; left:18px; transform:rotate(14deg); pointer-events:none; }
.admin-in  { padding:26px 22px 36px; position:relative; z-index:2; }
.adm-badge { display:inline-flex; align-items:center; gap:7px; background:rgba(255,255,255,.13); border:1px solid rgba(255,255,255,.22); padding:5px 15px; border-radius:100px; font-size:10px; font-weight:900; color:#fff; letter-spacing:1.2px; text-transform:uppercase; margin-bottom:14px; }
.adm-dot   { width:8px; height:8px; border-radius:50%; background:var(--yellow); box-shadow:0 0 0 3px rgba(245,196,0,.28); animation:pls 2s ease-in-out infinite; }
@keyframes pls { 0%,100%{box-shadow:0 0 0 3px rgba(245,196,0,.28)} 50%{box-shadow:0 0 0 6px rgba(245,196,0,.12)} }
.adm-ttl   { font-family:'Barlow Condensed',sans-serif; font-size:32px; font-weight:900; color:#fff; line-height:1.05; margin-bottom:6px; }
.adm-ttl em{ color:var(--yellow); font-style:normal; }
.adm-sub   { font-size:13px; color:rgba(255,255,255,.58); font-weight:600; line-height:1.55; }

.admin-body{ padding:18px 14px 36px; }
.acard     { background:#fff; border-radius:20px; margin-bottom:14px; border:1.5px solid var(--border); box-shadow:0 3px 16px rgba(27,63,160,.07); overflow:hidden; }
.ahead     { padding:15px 18px; display:flex; align-items:center; gap:13px; border-bottom:1.5px solid var(--border); background:rgba(242,245,252,.6); }
.ahead-ico { width:44px; height:44px; border-radius:13px; display:flex; align-items:center; justify-content:center; font-size:21px; flex-shrink:0; }
.ico-r { background:var(--red-lt); } .ico-b { background:var(--blue-lt); } .ico-y { background:var(--yellow-lt); }
.ahead-t   { font-size:14px; font-weight:900; color:var(--text); }
.ahead-s   { font-size:11px; color:var(--muted); font-weight:700; margin-top:2px; }
.abody     { padding:15px 18px; }
.irow      { display:flex; align-items:center; justify-content:space-between; padding:10px 0; border-bottom:1px solid rgba(221,227,240,.7); }
.irow:last-child { border-bottom:none; }
.ilbl      { font-size:12px; font-weight:700; color:var(--muted); }
.ival      { font-size:13px; font-weight:900; color:var(--text); }
.ival-b    { color:var(--blue); }
.pill      { padding:4px 13px; border-radius:100px; font-size:11px; font-weight:900; }
.pill-g    { background:var(--green-lt); color:var(--green); }
.pill-r    { background:var(--red-lt); color:var(--red); }
.pill-b    { background:var(--blue-lt); color:var(--blue); }

.agrid     { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:14px; }
.astat     { background:#fff; border-radius:18px; padding:16px; border:1.5px solid var(--border); box-shadow:0 2px 10px rgba(27,63,160,.05); }
.astat-ico { font-size:24px; margin-bottom:8px; }
.astat-num { font-family:'Barlow Condensed',sans-serif; font-size:28px; font-weight:900; display:block; line-height:1; margin-bottom:4px; }
.astat-lbl { font-size:10px; font-weight:900; color:var(--muted); text-transform:uppercase; letter-spacing:.5px; }

.divdr     { display:flex; align-items:center; gap:10px; padding:6px 0 16px; }
.divdr-l   { flex:1; height:1.5px; background:var(--border); }
.divdr-t   { font-size:10px; font-weight:900; color:var(--muted); text-transform:uppercase; letter-spacing:1px; padding:3px 12px; background:var(--bg); border-radius:100px; border:1px solid var(--border); white-space:nowrap; }

/* Streamlit widgets */
div[data-testid="stButton"] > button {
    border-radius:13px !important; font-family:'Nunito',sans-serif !important;
    font-weight:900 !important; padding:13px 20px !important; font-size:14px !important;
}
.stAlert  { border-radius:13px !important; }
.stFileUploader { border-radius:14px !important; }

/* Footer */
.footer      { background:linear-gradient(180deg,var(--bg) 0%,#fff 100%); border-top:1.5px solid var(--border); padding:22px 18px 26px; text-align:center; }
.footer-brand{ font-family:'Barlow Condensed',sans-serif; font-size:20px; font-weight:900; color:var(--blue); letter-spacing:1.5px; }
.footer-brand em { color:var(--red); font-style:normal; }
.footer-tag  { font-size:10px; color:var(--muted); font-weight:800; text-transform:uppercase; letter-spacing:1.8px; margin-top:3px; }
.footer-line { width:36px; height:3px; margin:10px auto 8px; background:linear-gradient(90deg,var(--red),var(--yellow)); border-radius:2px; }
.footer-dev  { font-size:11px; color:var(--muted); font-weight:700; }
.footer-dev strong { color:var(--blue); font-weight:900; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════
def fmt_price(v):
    try:
        return "Rp {:,}".format(int(round(float(v)))).replace(",", ".")
    except Exception:
        return "–"

def wa_link(nama):
    msg = (f"Halo Kak, saya mau tanya stok barang ini di ILMIGROSIR:\n\n"
           f"*{nama}*\n\nApakah tersedia? Berapa minimum ordernya? Terima kasih")
    return f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(msg)}"

def wa_general():
    msg = "Halo Kak, saya mau tanya-tanya produk di ILMIGROSIR. Boleh dibantu?"
    return f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(msg)}"

@st.cache_data(show_spinner=False)
def load_data(path):
    df = pd.read_csv(path)
    for col in ["Harga Retail", "Harga Grosir", "Harga Pokok"]:
        if col in df.columns:
            df[col] = (df[col].astype(str)
                       .str.replace("Rp", "", case=False, regex=False)
                       .str.replace(".", "", regex=False)
                       .str.replace(",", "", regex=False)
                       .str.replace(" ", "", regex=False))
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    if "Konversi" in df.columns:
        df["Konversi"] = pd.to_numeric(df["Konversi"], errors="coerce").fillna(1)
    for col in ["Nama Item", "Jenis", "Satuan", "Kode Item"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    return df

def get_logo_b64():
    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# SVG WhatsApp icon (inline, satu kali definisi)
_WA_SVG = (
    '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">'
    '<path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15'
    '-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475'
    '-.888-.788-1.487-1.761-1.66-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52'
    '.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207'
    '-.242-.579-.487-.5-.669-.51a12.8 12.8 0 0 0-.57-.01c-.198 0-.52.074-.792.372'
    '-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2'
    ' 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118'
    '.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347'
    'm-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374'
    'a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898'
    'a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884'
    'm8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892'
    'c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005'
    'c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413"/></svg>'
)

def build_card(kode, nama, jenis, group_df):
    # Escape semua teks dinamis — ini fix utama agar nama produk muncul
    n  = htmllib.escape(str(nama))
    k  = htmllib.escape(str(kode))
    j  = htmllib.escape(str(jenis))
    ic = cat_icon(jenis)

    has_g = any(
        float(r.get("Harga Grosir", 0)) > 0
        and float(r.get("Harga Grosir", 0)) < float(r.get("Harga Retail", 0))
        for _, r in group_df.iterrows()
    )

    vrows = []
    for _, r in group_df.iterrows():
        sat  = htmllib.escape(str(r.get("Satuan", "-")))
        try:  konv = int(float(r.get("Konversi", 1)))
        except: konv = 1
        ret  = float(r.get("Harga Retail", 0))
        grs  = float(r.get("Harga Grosir", 0))
        isi  = f"Isi {konv} pcs" if konv > 1 else "Satuan terkecil"
        rstr = fmt_price(ret) if ret > 0 else "–"

        g_html = ""
        if grs > 0 and grs < ret:
            hem = ret - grs
            g_html = (
                f'<div class="vgbox">'
                f'<span class="vglbl">Grosir</span>'
                f'<span class="vgval">{fmt_price(grs)}</span>'
                f'<span class="vghem">Hemat {fmt_price(hem)}</span>'
                f'</div>'
            )
        vrows.append(
            f'<div class="vrow">'
            f'<div class="vleft"><span class="vsat">&#128230; {sat}</span>'
            f'<span class="visi">{isi}</span></div>'
            f'<div class="vright"><span class="vret">{rstr}</span>{g_html}</div>'
            f'</div>'
        )

    badge_g = '<span class="bdg bdg-g">&#11088; Harga Grosir</span>' if has_g else ""
    url = wa_link(nama)

    return (
        f'<div class="pcard">'
        f'<div class="pstripe"></div>'
        f'<div class="pbody">'
        f'<div class="picon">{ic}</div>'
        f'<div class="pinfo">'
        f'<div class="pbadges"><span class="bdg bdg-j">{j}</span>{badge_g}</div>'
        f'<div class="ptitle">{n}</div>'
        f'<div class="pkode">Kode: {k}</div>'
        f'</div></div>'
        f'<div class="pvars">{"".join(vrows)}</div>'
        f'<div class="paction">'
        f'<a class="btn-wa" href="{url}" target="_blank">'
        f'{_WA_SVG} Tanya Stok &amp; Pesan</a>'
        f'</div></div>'
    )


# ══════════════════════════════════════════════════════════════
# LOAD DATA
# ══════════════════════════════════════════════════════════════
df = pd.DataFrame()
if os.path.exists(CSV_PATH):
    try:
        df = load_data(CSV_PATH)
        if not df.empty and "Jenis" in df.columns:
            df["Jenis"] = df["Jenis"].astype(str).str.strip()
    except Exception:
        df = pd.DataFrame()

has_kode = not df.empty and "Kode Item" in df.columns
has_jen  = not df.empty and "Jenis"     in df.columns
has_grs  = not df.empty and "Harga Grosir" in df.columns

total_produk   = df.groupby("Kode Item").ngroups if has_kode else 0
total_kategori = df["Jenis"].nunique()             if has_jen  else 0
total_grosir   = int((df["Harga Grosir"] > 0).sum()) if has_grs else 0
all_cats       = sorted(df["Jenis"].unique().tolist()) if has_jen else []

logo_b64  = get_logo_b64()
logo_html = (
    f'<img src="data:image/jpeg;base64,{logo_b64}" style="height:44px;display:block;" alt="Logo"/>'
    if logo_b64 else
    '<span style="font-family:\'Barlow Condensed\',sans-serif;font-size:26px;font-weight:900;color:#E31E24;">ILMIGROSIR</span>'
)


# ══════════════════════════════════════════════════════════════
# BOTTOM NAV — pakai <a href> biasa, tanpa JavaScript
# ══════════════════════════════════════════════════════════════
on_h = "on" if page == "home"    else ""
on_c = "on" if page == "catalog" else ""
on_a = "on" if page == "admin"   else ""

st.markdown(f"""
<div class="bnav">
  <a class="bnav-a {on_h}" href="?page=home">
    <span class="ni">&#127968;</span>
    <span class="nl">Beranda</span>
  </a>
  <a class="bnav-a {on_c}" href="?page=catalog">
    <span class="ni">&#128722;</span>
    <span class="nl">Katalog</span>
  </a>
  <a class="bnav-a adm {on_a}" href="?page=admin">
    <span class="ni">&#9881;&#65039;</span>
    <span class="nl">Admin</span>
  </a>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# TOMBOL KEMBALI — hanya di halaman selain beranda
# ══════════════════════════════════════════════════════════════
if page != "home":
    st.markdown(
        '<a class="back-btn" href="?page=home" title="Kembali ke Beranda">&#8592;</a>',
        unsafe_allow_html=True
    )


# ══════════════════════════════════════════════════════════════
# PAGE: BERANDA
# ══════════════════════════════════════════════════════════════
if page == "home":
    hour = datetime.datetime.now().hour
    if   hour < 11: grt, gem = "Selamat Pagi",  "&#127796;"
    elif hour < 15: grt, gem = "Selamat Siang", "&#9728;&#65039;"
    elif hour < 18: grt, gem = "Selamat Sore",  "&#127751;"
    else:           grt, gem = "Selamat Malam", "&#127769;"

    wa_cta = f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote('Halo ILMIGROSIR, saya mau tanya produk.')}"

    st.markdown(f"""
<div class="hero">
  <div class="stripe"></div>
  <div class="hero-in">
    <div class="logo-box">{logo_html}</div>
    <div class="hero-greet">{gem} {grt}, Selamat Datang</div>
    <div class="hero-h1">Grosir Terlengkap,<br>Harga <em>Terjangkau</em></div>
    <div class="hero-sub">Ribuan produk kebutuhan sehari-hari dengan harga grosir terbaik langsung dari distributor.</div>
    <div class="cta-row">
      <a class="cta-a" href="?page=catalog">&#128722; Lihat Katalog</a>
      <a class="cta-b" href="{wa_cta}" target="_blank">&#128172; WhatsApp</a>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown(f"""
<div class="stats-band">
  <div class="stat-item">
    <div class="dot" style="background:#1B3FA0;"></div>
    <span class="stat-num" style="color:#1B3FA0;">{total_produk:,}</span>
    <span class="stat-lbl">Produk</span>
  </div>
  <div class="stat-item">
    <div class="dot" style="background:#E31E24;"></div>
    <span class="stat-num" style="color:#E31E24;">{total_kategori}</span>
    <span class="stat-lbl">Kategori</span>
  </div>
  <div class="stat-item">
    <div class="dot" style="background:#C49A00;"></div>
    <span class="stat-num" style="color:#C49A00;">{total_grosir:,}</span>
    <span class="stat-lbl">Harga Grosir</span>
  </div>
</div>
<div style="height:22px;"></div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="sec-hd"><div class="sec-ttl">Layanan <em>Kami</em></div></div>
<div class="feat-row">
  <a class="feat-card" href="?page=catalog">
    <div class="fi fi-b">&#128717;</div>
    <div><div class="ft">Katalog Lengkap</div><div class="fs">Ribuan produk siap dipesan</div></div>
  </a>
  <div class="feat-card">
    <div class="fi fi-r">&#128176;</div>
    <div><div class="ft">Harga Grosir</div><div class="fs">Lebih hemat beli banyak</div></div>
  </div>
  <div class="feat-card">
    <div class="fi fi-y">&#128666;</div>
    <div><div class="ft">Pengiriman Cepat</div><div class="fs">Langsung ke lokasi Anda</div></div>
  </div>
  <div class="feat-card">
    <div class="fi fi-g">&#128241;</div>
    <div><div class="ft">Order via WA</div><div class="fs">Mudah lewat WhatsApp</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

    if all_cats:
        items = ""
        for c in all_cats[:8]:
            ic = cat_icon(c)
            nm = htmllib.escape((c[:8] + "…") if len(c) > 8 else c)
            items += (
                f'<a class="cat-box" href="?page=catalog">'
                f'<span class="cat-em">{ic}</span>'
                f'<span class="cat-nm">{nm}</span>'
                f'</a>'
            )
        st.markdown(f"""
<div class="sec-hd">
  <div class="sec-ttl">Kategori <em>Produk</em></div>
  <a class="sec-more" href="?page=catalog">Semua &#8594;</a>
</div>
<div class="cat-grid">{items}</div>
""", unsafe_allow_html=True)

    st.markdown(f"""
<a class="wa-ban" href="{wa_general()}" target="_blank">
  <div class="wa-ico">
    <svg width="40" height="40" viewBox="0 0 24 24" fill="white">
      <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.888-.788-1.487-1.761-1.66-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413"/>
    </svg>
  </div>
  <div>
    <div class="wa-ttl">Hubungi Kami via WhatsApp</div>
    <div class="wa-sub">Tanya harga, stok &amp; minimum order</div>
  </div>
  <div class="wa-arr">&#8250;</div>
</a>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="footer">
  <div class="footer-brand">ILMI<em>GROSIR</em></div>
  <div class="footer-tag">Jual Kembali &middot; Untung Berkali</div>
  <div class="footer-line"></div>
  <div class="footer-dev">Developed by <strong>NAUFAL TECH</strong></div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE: KATALOG
# ══════════════════════════════════════════════════════════════
elif page == "catalog":

    st.markdown("""
<div class="cat-hero">
  <div class="stripe"></div>
  <div class="cat-hero-in">
    <div class="cat-lbl">ILMIGROSIR</div>
    <div class="cat-ttl">Katalog <em>Produk</em></div>
  </div>
</div>
<div class="search-wrap">
""", unsafe_allow_html=True)

    keyword = st.text_input("Cari", placeholder="🔍Cari nama barang… (mie, gula, kopi)", key="kw")

    st.markdown("</div>", unsafe_allow_html=True)

    if df.empty:
        st.error("&#128237; Database belum ada. Silakan upload via halaman Admin.")
        st.stop()

    cat_list    = ["Semua"] + all_cats
    cat_display = ["&#128722; Semua"] + [f"{cat_icon(c)} {c}" for c in all_cats]

    st.markdown(
        '<div style="padding:0 14px 4px;">'
        '<span style="font-size:11px;font-weight:900;color:#6B7A99;'
        'text-transform:uppercase;letter-spacing:1.2px;">Filter Kategori</span></div>',
        unsafe_allow_html=True
    )

    chosen   = st.radio("Kategori", options=cat_display, horizontal=True,
                        label_visibility="collapsed", key="cat_radio")
    selected = cat_list[cat_display.index(chosen)]

    filtered = df.copy()
    if selected != "Semua":
        filtered = filtered[
            filtered["Jenis"].str.strip().str.lower() == selected.strip().lower()
        ]
    kw = keyword.strip()
    if kw:
        filtered = filtered[
            filtered["Nama Item"].str.contains(kw, case=False, na=False)
        ]

    groups   = filtered.groupby(["Kode Item", "Nama Item", "Jenis"], sort=False)
    products = list(groups)
    n        = len(products)

    cat_lbl = f"{cat_icon(selected)} {htmllib.escape(selected)}" if selected != "Semua" else "&#128722; Semua Kategori"
    st.markdown(f"""
<div class="res-strip">
  <span class="res-lbl">{cat_lbl}</span>
  <span class="res-cnt">{n:,} Item</span>
</div>
""", unsafe_allow_html=True)

    if n == 0:
        st.markdown("""
<div class="empty">
  <span class="empty-ico">&#128230;</span>
  <div class="empty-ttl">Produk Tidak Ditemukan</div>
  <div class="empty-sub">Coba kata kunci lain atau pilih kategori berbeda.</div>
</div>
""", unsafe_allow_html=True)
    else:
        # Render semua kartu dalam SATU blok st.markdown
        parts = ['<div class="feed">']
        for (kode, nama, jenis), gdf in products:
            parts.append(build_card(kode, nama, jenis, gdf))
        parts.append('</div>')
        st.markdown("".join(parts), unsafe_allow_html=True)

    st.markdown("""
<div class="footer">
  <div class="footer-brand">ILMI<em>GROSIR</em></div>
  <div class="footer-tag">Jual Kembali &middot; Untung Berkali</div>
  <div class="footer-line"></div>
  <div class="footer-dev">Developed by <strong>NAUFAL TECH</strong></div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE: ADMIN
# ══════════════════════════════════════════════════════════════
elif page == "admin":

    st.markdown("""
<div class="admin-hero">
  <div class="stripe" style="background:linear-gradient(90deg,#F5C400,#fff,#F5C400);"></div>
  <div class="admin-in">
    <div class="adm-badge"><span class="adm-dot"></span>Panel Kontrol</div>
    <div class="adm-ttl">Admin <em>Dashboard</em></div>
    <div class="adm-sub">Kelola database produk, pantau statistik, dan konfigurasi sistem ILMIGROSIR</div>
  </div>
</div>
<div class="admin-body">
""", unsafe_allow_html=True)

    # ── LOGIN ──
    if not st.session_state.admin_auth:
        st.markdown("""
<div class="acard">
  <div class="ahead">
    <div class="ahead-ico ico-r">&#128272;</div>
    <div><div class="ahead-t">Autentikasi Admin</div><div class="ahead-s">Masukkan password untuk melanjutkan</div></div>
  </div>
  <div class="abody">
""", unsafe_allow_html=True)

        pw = st.text_input("Password Admin", type="password",
                           key="pw_in", placeholder="Masukkan password rahasia…")
        if pw == ADMIN_PASSWORD:
            st.session_state.admin_auth = True
            st.rerun()
        elif pw:
            st.error("&#10060; Password salah. Coba lagi.")

        st.markdown("</div></div>", unsafe_allow_html=True)
        st.markdown("""
<div style="text-align:center;padding:28px 20px;">
  <div style="font-size:50px;margin-bottom:12px;">&#128274;</div>
  <div style="font-size:15px;font-weight:900;color:#0E1B3D;margin-bottom:8px;">Area Terbatas</div>
  <div style="font-size:12px;color:#6B7A99;font-weight:600;line-height:1.65;">
    Halaman ini hanya untuk administrator resmi ILMIGROSIR.<br>
    Masukkan password yang benar untuk mengakses panel kontrol.
  </div>
</div>
""", unsafe_allow_html=True)

    # ── DASHBOARD ──
    else:
        last_upd = "–"
        if os.path.exists(CSV_PATH):
            ts = os.path.getmtime(CSV_PATH)
            last_upd = datetime.datetime.fromtimestamp(ts).strftime("%d %b %Y, %H:%M")
        db_ok = not df.empty
        pill_db = ('<span class="pill pill-g">&#10003; Aktif</span>'
                   if db_ok else '<span class="pill pill-r">&#10007; Tidak Ada</span>')

        st.markdown(f"""
<div class="divdr"><div class="divdr-l"></div><div class="divdr-t">Statistik Database</div><div class="divdr-l"></div></div>
<div class="agrid">
  <div class="astat"><div class="astat-ico">&#128230;</div><span class="astat-num" style="color:#1B3FA0;">{total_produk:,}</span><span class="astat-lbl">Total Produk</span></div>
  <div class="astat"><div class="astat-ico">&#128193;</div><span class="astat-num" style="color:#E31E24;">{total_kategori}</span><span class="astat-lbl">Kategori</span></div>
  <div class="astat"><div class="astat-ico">&#11088;</div><span class="astat-num" style="color:#C49A00;">{total_grosir:,}</span><span class="astat-lbl">Item Grosir</span></div>
  <div class="astat"><div class="astat-ico">&#128336;</div><span class="astat-num" style="color:#1B3FA0;font-size:13px;line-height:1.6;">{last_upd}</span><span class="astat-lbl">Update Terakhir</span></div>
</div>
<div class="divdr"><div class="divdr-l"></div><div class="divdr-t">Status Sistem</div><div class="divdr-l"></div></div>
<div class="acard">
  <div class="ahead">
    <div class="ahead-ico ico-b">&#128202;</div>
    <div><div class="ahead-t">Informasi Database</div><div class="ahead-s">Status dan konfigurasi sistem</div></div>
  </div>
  <div class="abody">
    <div class="irow"><span class="ilbl">Status Database</span>{pill_db}</div>
    <div class="irow"><span class="ilbl">Nomor WhatsApp</span><span class="ival ival-b">+{htmllib.escape(WA_NUMBER)}</span></div>
    <div class="irow"><span class="ilbl">Total Baris Data</span><span class="ival ival-b">{len(df):,} baris</span></div>
    <div class="irow"><span class="ilbl">Versi Aplikasi</span><span class="pill pill-b">v3.0.0</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="divdr"><div class="divdr-l"></div><div class="divdr-t">Kelola Database</div><div class="divdr-l"></div></div>
<div class="acard">
  <div class="ahead">
    <div class="ahead-ico ico-y">&#128228;</div>
    <div><div class="ahead-t">Upload Database Baru</div><div class="ahead-s">Format CSV dari ekspor iPOS 5</div></div>
  </div>
  <div class="abody">
    <div style="background:#FFFBEA;border:1.5px solid #F5C400;border-radius:12px;padding:12px 14px;margin-bottom:14px;font-size:12px;font-weight:700;color:#7A5E00;line-height:1.7;">
      &#9888;&#65039; <strong>Kolom wajib:</strong><br>
      Kode Item &middot; Nama Item &middot; Jenis &middot; Konversi &middot; Satuan &middot; Harga Retail &middot; Harga Grosir
    </div>
""", unsafe_allow_html=True)

        up = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")
        if up is not None:
            try:
                new_df  = pd.read_csv(up)
                req     = {"Kode Item","Nama Item","Jenis","Konversi","Satuan","Harga Retail","Harga Grosir"}
                missing = req - set(new_df.columns)
                if missing:
                    st.error(f"Kolom kurang: {', '.join(missing)}")
                else:
                    new_df.to_csv(CSV_PATH, index=False)
                    st.cache_data.clear()
                    st.success(f"Berhasil! {len(new_df):,} baris data tersimpan.")
                    st.rerun()
            except Exception as e:
                st.error(f"Gagal memproses: {e}")

        st.markdown("</div></div>", unsafe_allow_html=True)

        st.markdown("""
<div class="acard" style="margin-top:14px;">
  <div class="ahead">
    <div class="ahead-ico ico-b">&#128161;</div>
    <div><div class="ahead-t">Tips Penggunaan</div><div class="ahead-s">Panduan untuk administrator</div></div>
  </div>
  <div class="abody" style="font-size:12px;color:#6B7A99;font-weight:700;line-height:1.9;">
    <div>&#128204; Export data dari iPOS 5 dalam format CSV</div>
    <div>&#128204; Pastikan semua kolom wajib ada sebelum upload</div>
    <div>&#128204; Data lama digantikan otomatis setelah upload berhasil</div>
    <div>&#128204; Gunakan tombol &#8592; di pojok kiri atas untuk kembali ke Beranda</div>
  </div>
</div>
<div style="height:14px;"></div>
""", unsafe_allow_html=True)

        if st.button("&#128682; Keluar dari Admin Panel", use_container_width=True):
            st.session_state.admin_auth = False
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)  # tutup admin-body

    st.markdown("""
<div class="footer">
  <div class="footer-brand">ILMI<em>GROSIR</em></div>
  <div class="footer-tag">Admin Panel &middot; Akses Terbatas</div>
  <div class="footer-line"></div>
  <div class="footer-dev">Developed by <strong>NAUFAL TECH</strong></div>
</div>
""", unsafe_allow_html=True)
