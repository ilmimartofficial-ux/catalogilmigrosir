import streamlit as st
import pandas as pd
import base64, os, urllib.parse, datetime

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

def cat_icon(j): return CATEGORY_ICONS.get(j.upper(), "📦")

# ══════════════════════════════════════════════════════════════
# GLOBAL CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900;1000&family=Barlow+Condensed:wght@500;600;700;800;900&display=swap');

:root {
    --red:       #E31E24;
    --red-dark:  #B01519;
    --red-light: #FFF0F0;
    --blue:      #1B3FA0;
    --blue-mid:  #2554C7;
    --blue-light:#EBF0FB;
    --yellow:    #F5C400;
    --yellow-dk: #C49A00;
    --yellow-lt: #FFFBEA;
    --white:     #FFFFFF;
    --bg:        #F2F5FC;
    --surface:   #FFFFFF;
    --border:    #DDE3F0;
    --text:      #0E1B3D;
    --muted:     #6B7A99;
    --success:   #15803D;
    --success-lt:#DCFCE7;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif !important;
    background: #C9D3E8 !important;
}

.block-container {
    padding: 0 !important;
    max-width: 480px !important;
    margin: 0 auto !important;
    background: var(--bg) !important;
    min-height: 100vh;
    position: relative;
    overflow-x: hidden;
    box-shadow: 0 0 80px rgba(27,63,160,0.18);
    padding-bottom: 80px !important;
}

#MainMenu, footer, header, .stDeployButton, .stAppHeader { display: none !important; }

/* ── BOTTOM NAV BAR ── */
.bottom-nav {
    position: fixed;
    bottom: 0; left: 50%;
    transform: translateX(-50%);
    width: 100%; max-width: 480px;
    background: var(--white);
    border-top: 2px solid var(--border);
    display: flex; z-index: 9999;
    box-shadow: 0 -4px 24px rgba(27,63,160,0.10);
}
.nav-btn {
    flex: 1; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 10px 0 12px;
    cursor: pointer; border: none; background: none;
    gap: 4px; transition: all 0.2s;
    font-family: 'Nunito', sans-serif;
}
.nav-btn .nav-icon { font-size: 22px; line-height: 1; transition: transform 0.2s; }
.nav-btn .nav-label { font-size: 10px; font-weight: 800; color: var(--muted); letter-spacing: 0.3px; }
.nav-btn.active .nav-label { color: var(--blue); }
.nav-btn.active .nav-icon { transform: translateY(-2px); }
.nav-btn.admin-btn.active .nav-label { color: var(--red); }

/* Active indicator pill */
.nav-btn.active::before {
    content: '';
    position: absolute;
    top: 0;
    width: 36px; height: 3px;
    background: var(--blue);
    border-radius: 0 0 4px 4px;
}
.nav-btn.admin-btn.active::before { background: var(--red); }

/* ═══ PAGE: HOME ═══ */
.home-hero {
    background: linear-gradient(160deg, var(--blue) 0%, #112880 60%, #0A1F6B 100%);
    padding: 0;
    position: relative;
    overflow: hidden;
}
.home-hero-topbar {
    height: 5px;
    background: linear-gradient(90deg, var(--red) 0%, var(--yellow) 50%, var(--red) 100%);
}
.home-hero-content {
    padding: 28px 24px 80px;
    position: relative; z-index: 2;
}
.home-hero-deco1 {
    position: absolute; width: 220px; height: 220px; border-radius: 50%;
    background: radial-gradient(circle, rgba(245,196,0,0.12) 0%, transparent 70%);
    top: -60px; right: -60px; pointer-events: none; z-index: 1;
}
.home-hero-deco2 {
    position: absolute; width: 140px; height: 140px; border-radius: 50%;
    background: radial-gradient(circle, rgba(227,30,36,0.15) 0%, transparent 70%);
    bottom: 10px; left: -30px; pointer-events: none; z-index: 1;
}
.home-hero-deco3 {
    position: absolute; width: 60px; height: 60px;
    border: 2px solid rgba(245,196,0,0.15); border-radius: 12px;
    bottom: 40px; right: 30px; transform: rotate(20deg);
    pointer-events: none; z-index: 1;
}

.home-logo-wrap {
    background: var(--white);
    border-radius: 16px;
    padding: 10px 18px;
    border: 3px solid var(--yellow);
    display: inline-block;
    box-shadow: 0 6px 20px rgba(0,0,0,0.25);
    margin-bottom: 20px;
}
.home-logo-img { height: 46px; display: block; }
.home-logo-text {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 30px; font-weight: 900;
    color: var(--red);
}

.home-greeting {
    font-size: 13px; font-weight: 700;
    color: rgba(255,255,255,0.6);
    letter-spacing: 1px; text-transform: uppercase;
    margin-bottom: 4px;
}
.home-headline {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 30px; font-weight: 900;
    color: var(--white); line-height: 1.15;
    margin-bottom: 8px;
}
.home-headline span { color: var(--yellow); }
.home-subline {
    font-size: 13px; color: rgba(255,255,255,0.65);
    font-weight: 600; line-height: 1.6;
    margin-bottom: 22px;
}

/* CTA Buttons */
.home-cta-row { display: flex; gap: 10px; }
.cta-primary {
    flex: 1; background: var(--yellow);
    color: var(--blue) !important; text-decoration: none !important;
    padding: 13px 16px; border-radius: 12px;
    font-size: 13px; font-weight: 900;
    text-align: center; display: block;
    box-shadow: 0 4px 16px rgba(245,196,0,0.35);
    letter-spacing: 0.3px;
}
.cta-secondary {
    flex: 1; background: rgba(255,255,255,0.12);
    color: var(--white) !important; text-decoration: none !important;
    padding: 13px 16px; border-radius: 12px;
    font-size: 13px; font-weight: 800;
    text-align: center; display: block;
    border: 1.5px solid rgba(255,255,255,0.25);
    backdrop-filter: blur(8px);
}

/* Stats band */
.home-stats-band {
    background: var(--white);
    margin: 0 16px;
    border-radius: 20px;
    margin-top: -36px;
    position: relative; z-index: 10;
    display: flex;
    box-shadow: 0 8px 32px rgba(27,63,160,0.12);
    border: 1.5px solid var(--border);
    overflow: hidden;
}
.home-stat {
    flex: 1; text-align: center; padding: 18px 8px;
    border-right: 1.5px solid var(--border);
    position: relative;
}
.home-stat:last-child { border-right: none; }
.home-stat-num {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 26px; font-weight: 900;
    color: var(--blue); display: block; line-height: 1;
    margin-bottom: 4px;
}
.home-stat-label {
    font-size: 10px; font-weight: 800;
    color: var(--muted); text-transform: uppercase; letter-spacing: 0.5px;
}
.stat-dot {
    width: 6px; height: 6px; border-radius: 50%;
    margin: 0 auto 6px;
}

/* Section headers */
.sec-head {
    display: flex; align-items: center; justify-content: space-between;
    padding: 22px 20px 12px;
}
.sec-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 20px; font-weight: 800; color: var(--text);
    letter-spacing: 0.3px;
}
.sec-title span { color: var(--red); }
.sec-more {
    font-size: 12px; font-weight: 800; color: var(--blue);
    text-decoration: none; cursor: pointer;
    background: var(--blue-light); padding: 5px 12px;
    border-radius: 100px;
}

/* Feature cards row */
.feature-row {
    display: flex; gap: 12px; padding: 0 16px 20px; overflow-x: auto;
    scrollbar-width: none;
}
.feature-row::-webkit-scrollbar { display: none; }
.feature-card {
    flex: 0 0 140px; background: var(--white);
    border-radius: 18px; padding: 18px 14px;
    border: 1.5px solid var(--border);
    box-shadow: 0 4px 16px rgba(27,63,160,0.05);
    display: flex; flex-direction: column; gap: 10px;
    cursor: pointer; transition: all 0.2s;
}
.feature-card:active { transform: scale(0.97); }
.fc-icon {
    width: 48px; height: 48px; border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 24px;
}
.fc-icon.red { background: var(--red-light); }
.fc-icon.blue { background: var(--blue-light); }
.fc-icon.yellow { background: var(--yellow-lt); }
.fc-title { font-size: 13px; font-weight: 900; color: var(--text); }
.fc-sub { font-size: 11px; color: var(--muted); font-weight: 600; line-height: 1.4; }

/* Popular category grid */
.cat-grid {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 10px; padding: 0 16px 20px;
}
.cat-item {
    display: flex; flex-direction: column; align-items: center; gap: 6px;
    background: var(--white); border-radius: 16px; padding: 14px 8px;
    border: 1.5px solid var(--border);
    box-shadow: 0 2px 8px rgba(27,63,160,0.04);
    cursor: pointer; transition: all 0.15s;
}
.cat-item:active { transform: scale(0.96); background: var(--blue-light); }
.cat-item-icon { font-size: 24px; }
.cat-item-name {
    font-size: 9px; font-weight: 800; color: var(--text);
    text-align: center; line-height: 1.3;
    text-transform: uppercase; letter-spacing: 0.3px;
}

/* WA Banner */
.wa-banner {
    margin: 4px 16px 24px;
    background: linear-gradient(135deg, #128C4F 0%, #075E54 100%);
    border-radius: 20px; padding: 20px;
    display: flex; gap: 16px; align-items: center;
    box-shadow: 0 6px 20px rgba(7,94,84,0.25);
    text-decoration: none !important;
}
.wa-banner-icon { font-size: 40px; flex-shrink: 0; }
.wa-banner-text .wb-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 18px; font-weight: 800; color: var(--white);
    margin-bottom: 3px;
}
.wa-banner-text .wb-sub {
    font-size: 12px; color: rgba(255,255,255,0.75); font-weight: 600;
}
.wa-banner-arrow {
    margin-left: auto; font-size: 20px; color: rgba(255,255,255,0.6);
}

/* ═══ PAGE: CATALOG ═══ */
.cat-page-hero {
    background: var(--blue);
    padding: 0;
    position: relative;
    overflow: hidden;
}
.cat-page-topbar {
    height: 5px;
    background: linear-gradient(90deg, var(--red), var(--yellow), var(--red));
}
.cat-page-inner {
    padding: 22px 20px 28px;
    position: relative; z-index: 2;
}
.cat-page-deco {
    position: absolute; width: 160px; height: 160px; border-radius: 50%;
    background: rgba(245,196,0,0.08);
    top: -40px; right: -40px; pointer-events: none;
}
.cat-page-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 28px; font-weight: 900; color: var(--white);
    letter-spacing: 0.5px; margin-bottom: 4px;
}
.cat-page-title span { color: var(--yellow); }
.cat-page-sub {
    font-size: 12px; color: rgba(255,255,255,0.6); font-weight: 700;
    text-transform: uppercase; letter-spacing: 1px;
}

/* Search box in catalog */
div[data-testid="stTextInput"] {
    padding: 0 16px !important; margin: 0 !important;
}
.stTextInput > div > div > input {
    border: none !important; border-radius: 14px !important;
    font-size: 14px !important; font-weight: 700 !important;
    color: var(--text) !important; padding: 14px 18px !important;
    background: var(--white) !important;
    box-shadow: 0 4px 16px rgba(27,63,160,0.10) !important;
    border: 1.5px solid transparent !important;
    font-family: 'Nunito', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--blue-mid) !important;
    box-shadow: 0 0 0 3px rgba(27,63,160,0.12) !important;
}
.stTextInput > div > div > input::placeholder { color: #9AA4C0 !important; font-weight: 600 !important; }
.stTextInput > label { display: none !important; }

/* Search container floating */
.search-float {
    background: transparent;
    padding: 0 0 16px;
    margin-top: -24px;
    position: relative; z-index: 5;
}

/* Category chips */
div[data-testid="stRadio"] { padding: 0 !important; }
div[data-testid="stRadio"] > label { display: none !important; }
div[data-testid="stRadio"] div[role="radiogroup"] {
    display: flex !important; flex-wrap: nowrap !important;
    overflow-x: auto !important; gap: 8px !important;
    padding: 4px 16px 16px !important;
    scrollbar-width: none !important;
}
div[data-testid="stRadio"] div[role="radiogroup"]::-webkit-scrollbar { display: none !important; }
div[data-testid="stRadio"] div[role="radiogroup"] > label {
    flex: 0 0 auto !important; display: inline-flex !important;
    align-items: center !important; padding: 9px 16px !important;
    border-radius: 100px !important; background: var(--white) !important;
    border: 1.5px solid var(--border) !important; cursor: pointer !important;
    transition: all .2s ease !important;
    box-shadow: 0 2px 8px rgba(27,63,160,0.04) !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input[type="radio"]:checked) {
    background: var(--blue) !important; border-color: var(--blue) !important;
    box-shadow: 0 4px 14px rgba(27,63,160,0.28) !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child { display: none !important; }
div[data-testid="stRadio"] div[role="radiogroup"] > label p {
    font-size: 12px !important; font-weight: 800 !important;
    color: var(--muted) !important; margin: 0 !important;
    font-family: 'Nunito', sans-serif !important; white-space: nowrap !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input[type="radio"]:checked) p {
    color: var(--white) !important;
}

/* Result strip */
.result-strip {
    padding: 4px 16px 12px;
    display: flex; align-items: center; justify-content: space-between;
}
.result-label { font-size: 13px; font-weight: 800; color: var(--text); }
.result-count {
    background: var(--blue); color: var(--white);
    padding: 4px 14px; border-radius: 100px;
    font-size: 11px; font-weight: 900;
}

/* Product cards */
.catalog-feed { padding: 0 16px 24px; }
.m-card {
    background: var(--white); border-radius: 20px; margin-bottom: 14px;
    box-shadow: 0 2px 16px rgba(27,63,160,0.07);
    border: 1.5px solid var(--border); overflow: hidden;
}
.m-card-stripe {
    height: 4px;
    background: linear-gradient(90deg, var(--blue) 0%, var(--red) 50%, var(--yellow) 100%);
}
.m-card-body {
    display: flex; padding: 14px 16px; gap: 14px;
    border-bottom: 1.5px dashed var(--border); align-items: flex-start;
}
.m-card-icon {
    width: 58px; height: 58px; background: var(--blue-light);
    border-radius: 15px; display: flex; align-items: center; justify-content: center;
    font-size: 28px; flex-shrink: 0; border: 1.5px solid var(--border);
}
.m-card-info { flex: 1; min-width: 0; }
.m-badges { display: flex; gap: 6px; margin-bottom: 7px; flex-wrap: wrap; }
.badge {
    font-size: 9px; font-weight: 900; padding: 3px 8px;
    border-radius: 6px; text-transform: uppercase; letter-spacing: 0.5px;
}
.badge-jenis { background: var(--blue-light); color: var(--blue); border: 1px solid #C0D0F0; }
.badge-grosir { background: var(--yellow-lt); color: var(--yellow-dk); border: 1px solid #F0D060; }
.m-title { font-size: 14px; font-weight: 900; color: var(--text); line-height: 1.3; margin-bottom: 5px; }
.m-kode {
    font-size: 10px; color: var(--muted); font-weight: 700;
    background: var(--bg); padding: 2px 8px; border-radius: 6px; display: inline-block;
}
.m-card-variants { background: #FAFBFF; }
.v-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 11px 16px; border-bottom: 1px solid var(--border);
}
.v-row:last-child { border-bottom: none; }
.v-left { display: flex; flex-direction: column; gap: 3px; }
.v-satuan { font-size: 13px; font-weight: 800; color: var(--text); display: flex; align-items: center; gap: 5px; }
.v-isi { font-size: 10px; color: var(--muted); font-weight: 700; }
.v-right { text-align: right; display: flex; flex-direction: column; align-items: flex-end; gap: 5px; }
.v-retail {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 20px; font-weight: 800; color: var(--text); line-height: 1;
}
.v-grosir-box {
    display: flex; align-items: center; gap: 5px;
    background: var(--red-light); padding: 4px 8px;
    border-radius: 8px; border: 1px solid #FFCCCC;
}
.vg-label { font-size: 9px; font-weight: 900; color: var(--red); text-transform: uppercase; }
.vg-val {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 14px; font-weight: 800; color: var(--red-dark);
}
.vg-hemat { font-size: 9px; color: var(--success); font-weight: 800; background: var(--success-lt); padding: 2px 6px; border-radius: 5px; }
.m-card-action { padding: 12px 16px; background: var(--white); }
.btn-wa {
    display: flex; align-items: center; justify-content: center; gap: 8px; width: 100%;
    background: linear-gradient(135deg, #22C55E 0%, #15803D 100%);
    color: var(--white) !important; text-decoration: none !important;
    padding: 13px; border-radius: 13px; font-size: 13px; font-weight: 800;
    box-shadow: 0 4px 16px rgba(21,128,61,0.25); font-family: 'Nunito', sans-serif;
    transition: all 0.2s;
}
.btn-wa:active { transform: scale(0.98); }

/* Empty state */
.m-empty { text-align: center; padding: 60px 20px; }
.m-empty-icon { font-size: 64px; margin-bottom: 16px; display: block; opacity: 0.35; }
.m-empty-title { font-size: 18px; font-weight: 900; color: var(--text); margin-bottom: 8px; }
.m-empty-sub { font-size: 13px; color: var(--muted); line-height: 1.6; font-weight: 600; }

/* ═══ PAGE: ADMIN ═══ */
.admin-hero {
    background: linear-gradient(135deg, var(--red-dark) 0%, var(--red) 50%, #F04040 100%);
    padding: 0;
    position: relative; overflow: hidden;
}
.admin-hero-topbar {
    height: 5px;
    background: linear-gradient(90deg, var(--yellow), var(--white), var(--yellow));
}
.admin-hero-inner { padding: 28px 24px 36px; position: relative; z-index: 2; }
.admin-hero-deco {
    position: absolute; width: 200px; height: 200px; border-radius: 50%;
    background: rgba(255,255,255,0.06);
    top: -60px; right: -60px; pointer-events: none;
}
.admin-hero-deco2 {
    position: absolute; width: 80px; height: 80px;
    border: 2px solid rgba(255,255,255,0.1); border-radius: 20px;
    bottom: 20px; left: 20px; transform: rotate(15deg); pointer-events: none;
}
.admin-badge-row { display: flex; align-items: center; gap: 10px; margin-bottom: 14px; }
.admin-badge {
    background: rgba(255,255,255,0.15); backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.25);
    padding: 6px 14px; border-radius: 100px;
    font-size: 11px; font-weight: 800; color: var(--white);
    letter-spacing: 1px; text-transform: uppercase;
}
.admin-badge-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: var(--yellow); display: inline-block;
    box-shadow: 0 0 0 3px rgba(245,196,0,0.3);
    margin-right: 4px;
}
.admin-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 32px; font-weight: 900; color: var(--white);
    line-height: 1.1; margin-bottom: 6px;
}
.admin-title span { color: var(--yellow); }
.admin-subtitle { font-size: 13px; color: rgba(255,255,255,0.65); font-weight: 600; }

/* Admin cards */
.admin-body { padding: 20px 16px 32px; }
.admin-card {
    background: var(--white); border-radius: 20px; margin-bottom: 16px;
    border: 1.5px solid var(--border);
    box-shadow: 0 4px 20px rgba(27,63,160,0.07); overflow: hidden;
}
.admin-card-head {
    padding: 16px 20px; display: flex; align-items: center; gap: 12px;
    border-bottom: 1.5px solid var(--border);
}
.admin-card-head-icon {
    width: 42px; height: 42px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
}
.ach-red { background: var(--red-light); }
.ach-blue { background: var(--blue-light); }
.ach-yellow { background: var(--yellow-lt); }
.admin-card-head-text .acht { font-size: 14px; font-weight: 900; color: var(--text); }
.admin-card-head-text .achs { font-size: 11px; color: var(--muted); font-weight: 700; }
.admin-card-body { padding: 16px 20px; }

/* Info row */
.info-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 10px 0; border-bottom: 1px solid var(--border);
}
.info-row:last-child { border-bottom: none; }
.info-label { font-size: 12px; font-weight: 700; color: var(--muted); }
.info-value { font-size: 13px; font-weight: 900; color: var(--text); }
.info-value.green { color: var(--success); }
.info-value.red { color: var(--red); }
.info-value.blue { color: var(--blue); }

/* Status pill */
.status-pill {
    padding: 4px 12px; border-radius: 100px;
    font-size: 11px; font-weight: 900;
}
.sp-green { background: var(--success-lt); color: var(--success); }
.sp-red { background: var(--red-light); color: var(--red); }
.sp-blue { background: var(--blue-light); color: var(--blue); }

/* Admin stats grid */
.admin-stats-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 12px; margin-bottom: 16px;
}
.admin-stat-card {
    background: var(--white); border-radius: 18px; padding: 18px;
    border: 1.5px solid var(--border);
    box-shadow: 0 2px 12px rgba(27,63,160,0.05);
}
.asc-icon { font-size: 24px; margin-bottom: 10px; }
.asc-num {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 28px; font-weight: 900; display: block; line-height: 1;
}
.asc-label { font-size: 11px; font-weight: 800; color: var(--muted); text-transform: uppercase; letter-spacing: 0.5px; }

/* Streamlit widget overrides for admin */
.stTextInput > div > div > input { margin-bottom: 8px !important; }
.stFileUploader { border-radius: 14px !important; }
.stAlert { border-radius: 12px !important; }

/* Override for stExpander hide */
.stExpander { display: none !important; }

/* Streamlit button */
div[data-testid="stButton"] button {
    border-radius: 12px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
}

/* Section divider */
.sec-divider {
    display: flex; align-items: center; gap: 12px; padding: 4px 0 16px;
}
.sec-divider-line { flex: 1; height: 1.5px; background: var(--border); }
.sec-divider-label {
    font-size: 11px; font-weight: 800; color: var(--muted);
    text-transform: uppercase; letter-spacing: 1px;
}

/* Footer */
.app-footer {
    background: var(--white); border-top: 1.5px solid var(--border);
    padding: 20px; text-align: center;
}
.af-brand {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 18px; font-weight: 900; color: var(--blue); letter-spacing: 1px;
}
.af-brand span { color: var(--red); }
.af-tag { font-size: 10px; color: var(--muted); font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 3px; }
.af-divider {
    width: 36px; height: 3px; margin: 10px auto 8px;
    background: linear-gradient(90deg, var(--red), var(--yellow));
    border-radius: 2px;
}
.af-dev { font-size: 11px; color: var(--muted); font-weight: 700; }
.af-dev strong { color: var(--blue); font-weight: 900; }
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

def wa_link_general():
    msg = "Halo Kak, saya mau tanya-tanya produk di ILMIGROSIR. Boleh dibantu? 😊"
    return f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(msg)}"

@st.cache_data(show_spinner=False)
def load_data(path):
    df = pd.read_csv(path)
    price_cols = ["Harga Retail", "Harga Grosir", "Harga Pokok"]
    for col in price_cols:
        df[col] = df[col].astype(str)
        df[col] = df[col].str.replace('Rp', '', case=False, regex=False)
        df[col] = df[col].str.replace('.', '', regex=False)
        df[col] = df[col].str.replace(',', '', regex=False)
        df[col] = df[col].str.replace(' ', '', regex=False)
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
    icon = cat_icon(jenis)
    has_grosir = any((row["Harga Grosir"] > 0 and row["Harga Grosir"] < row["Harga Retail"]) for _, row in group_df.iterrows())
    rows_html = ""
    for _, row in group_df.iterrows():
        satuan   = row["Satuan"]
        konversi = int(row["Konversi"])
        retail   = row["Harga Retail"]
        grosir   = row["Harga Grosir"]
        isi_text = f"Isi {konversi} pcs" if konversi > 1 else "Satuan terkecil"
        r_str    = fmt_price(retail) if retail > 0 else "–"
        g_html = ""
        if grosir > 0 and grosir < retail:
            selisih = retail - grosir
            g_html = (
                f'<div class="v-grosir-box">'
                f'<span class="vg-label">Grosir</span>'
                f'<span class="vg-val">{fmt_price(grosir)}</span>'
                f'<span class="vg-hemat">Hemat {fmt_price(selisih)}</span>'
                f'</div>'
            )
        rows_html += (
            f'<div class="v-row">'
            f'<div class="v-left"><span class="v-satuan">📦 {satuan}</span>'
            f'<span class="v-isi">{isi_text}</span></div>'
            f'<div class="v-right"><span class="v-retail">{r_str}</span>{g_html}</div>'
            f'</div>'
        )
    gb = '<span class="badge badge-grosir">⭐ Harga Grosir</span>' if has_grosir else ""
    link = wa_link(nama)
    return (
        f'<div class="m-card"><div class="m-card-stripe"></div>'
        f'<div class="m-card-body">'
        f'<div class="m-card-icon">{icon}</div>'
        f'<div class="m-card-info">'
        f'<div class="m-badges"><span class="badge badge-jenis">{jenis}</span>{gb}</div>'
        f'<div class="m-title">{nama}</div>'
        f'<div class="m-kode">Kode: {kode}</div>'
        f'</div></div>'
        f'<div class="m-card-variants">{rows_html}</div>'
        f'<div class="m-card-action">'
        f'<a class="btn-wa" href="{link}" target="_blank">'
        f'<svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.888-.788-1.487-1.761-1.66-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413"/></svg>'
        f'Tanya Stok & Pesan</a>'
        f'</div></div>'
    )


# ══════════════════════════════════════════════════════════════
# LOAD DATA & STATE
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

logo_b64  = get_logo_b64(LOGO_PATH)
logo_html = (
    f'<img class="home-logo-img" src="data:image/jpeg;base64,{logo_b64}" alt="Logo"/>'
    if logo_b64 else '<div class="home-logo-text">ILMIGROSIR</div>'
)

# Session state
if "page" not in st.session_state:
    st.session_state.page = "home"
if "catalog_cat" not in st.session_state:
    st.session_state.catalog_cat = None
if "admin_auth" not in st.session_state:
    st.session_state.admin_auth = False


# ══════════════════════════════════════════════════════════════
# BOTTOM NAV — rendered as HTML + JS
# ══════════════════════════════════════════════════════════════
page = st.session_state.page

home_active  = "active" if page == "home"    else ""
cat_active   = "active" if page == "catalog" else ""
admin_active = "active" if page == "admin"   else ""

st.html(f"""
<div class="bottom-nav" style="position:fixed;">
  <button class="nav-btn {home_active}" onclick="window.location.href='?page=home'">
    <span class="nav-icon">🏠</span>
    <span class="nav-label">Beranda</span>
  </button>
  <button class="nav-btn {cat_active}" onclick="window.location.href='?page=catalog'">
    <span class="nav-icon">🛒</span>
    <span class="nav-label">Katalog</span>
  </button>
  <button class="nav-btn admin-btn {admin_active}" onclick="window.location.href='?page=admin'">
    <span class="nav-icon">⚙️</span>
    <span class="nav-label">Admin</span>
  </button>
</div>
""")

# Read page from query params
qp = st.query_params
if "page" in qp:
    st.session_state.page = qp["page"]
    page = st.session_state.page


# ══════════════════════════════════════════════════════════════
# ═══ PAGE: HOME ═══
# ══════════════════════════════════════════════════════════════
if page == "home":

    now = datetime.datetime.now()
    hour = now.hour
    if hour < 11:   greeting = "Selamat Pagi"
    elif hour < 15: greeting = "Selamat Siang"
    elif hour < 18: greeting = "Selamat Sore"
    else:           greeting = "Selamat Malam"

    st.html(f"""
    <div class="home-hero">
        <div class="home-hero-topbar"></div>
        <div class="home-hero-deco1"></div>
        <div class="home-hero-deco2"></div>
        <div class="home-hero-deco3"></div>
        <div class="home-hero-content">
            <div class="home-logo-wrap">{logo_html}</div>
            <div class="home-greeting">{greeting}, Selamat Datang 👋</div>
            <div class="home-headline">Grosir Terlengkap,<br>Harga <span>Terjangkau</span></div>
            <div class="home-subline">
                Temukan ribuan produk kebutuhan sehari-hari dengan harga grosir terbaik langsung dari distributor.
            </div>
            <div class="home-cta-row">
                <a class="cta-primary" href="?page=catalog">🛒 Lihat Katalog</a>
                <a class="cta-secondary" href="https://wa.me/{WA_NUMBER}?text={urllib.parse.quote('Halo ILMIGROSIR, saya mau tanya produk.')}" target="_blank">💬 Hubungi WA</a>
            </div>
        </div>
    </div>
    """)

    # Stats band
    st.html(f"""
    <div class="home-stats-band">
        <div class="home-stat">
            <div class="stat-dot" style="background:#1B3FA0;"></div>
            <span class="home-stat-num">{total_produk:,}</span>
            <span class="home-stat-label">Produk</span>
        </div>
        <div class="home-stat">
            <div class="stat-dot" style="background:#E31E24;"></div>
            <span class="home-stat-num">{total_kategori}</span>
            <span class="home-stat-label">Kategori</span>
        </div>
        <div class="home-stat">
            <div class="stat-dot" style="background:#F5C400;"></div>
            <span class="home-stat-num">{total_grosir:,}</span>
            <span class="home-stat-label">Harga Grosir</span>
        </div>
    </div>
    <div style="height:24px;"></div>
    """)

    # Feature cards
    st.html("""
    <div class="sec-head">
        <div class="sec-title">Layanan <span>Kami</span></div>
    </div>
    <div class="feature-row">
        <div class="feature-card" onclick="window.location.href='?page=catalog'">
            <div class="fc-icon blue">🛍️</div>
            <div>
                <div class="fc-title">Katalog Lengkap</div>
                <div class="fc-sub">Ribuan produk siap dipesan</div>
            </div>
        </div>
        <div class="feature-card">
            <div class="fc-icon red">💰</div>
            <div>
                <div class="fc-title">Harga Grosir</div>
                <div class="fc-sub">Lebih hemat untuk pembelian banyak</div>
            </div>
        </div>
        <div class="feature-card">
            <div class="fc-icon yellow">🚚</div>
            <div>
                <div class="fc-title">Pengiriman Cepat</div>
                <div class="fc-sub">Langsung ke lokasi Anda</div>
            </div>
        </div>
        <div class="feature-card">
            <div class="fc-icon blue">📱</div>
            <div>
                <div class="fc-title">Order via WA</div>
                <div class="fc-sub">Mudah & cepat via WhatsApp</div>
            </div>
        </div>
    </div>
    """)

    # Popular categories (show first 8)
    if all_cats:
        cats_to_show = all_cats[:8]
        cat_items_html = ""
        for c in cats_to_show:
            icon = cat_icon(c)
            short = c[:9] + "…" if len(c) > 9 else c
            cat_items_html += f"""
            <div class="cat-item" onclick="window.location.href='?page=catalog'">
                <div class="cat-item-icon">{icon}</div>
                <div class="cat-item-name">{short}</div>
            </div>
            """
        st.html(f"""
        <div class="sec-head">
            <div class="sec-title">Kategori <span>Produk</span></div>
            <a class="sec-more" href="?page=catalog">Semua →</a>
        </div>
        <div class="cat-grid">{cat_items_html}</div>
        """)

    # WA banner
    wa_url = wa_link_general()
    st.html(f"""
    <a class="wa-banner" href="{wa_url}" target="_blank">
        <div class="wa-banner-icon">
            <svg width="44" height="44" viewBox="0 0 24 24" fill="white"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.888-.788-1.487-1.761-1.66-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413"/></svg>
        </div>
        <div class="wa-banner-text">
            <div class="wb-title">Hubungi Kami via WhatsApp</div>
            <div class="wb-sub">Tanya harga, stok, & minimum order</div>
        </div>
        <div class="wa-banner-arrow">›</div>
    </a>
    """)

    # Footer
    st.html("""
    <div class="app-footer">
        <div class="af-brand">ILMI<span>GROSIR</span></div>
        <div class="af-tag">Jual Kembali · Untung Berkali</div>
        <div class="af-divider"></div>
        <div class="af-dev">Developed by <strong>NAUFAL TECH</strong></div>
    </div>
    """)


# ══════════════════════════════════════════════════════════════
# ═══ PAGE: CATALOG ═══
# ══════════════════════════════════════════════════════════════
elif page == "catalog":

    st.html("""
    <div class="cat-page-hero">
        <div class="cat-page-topbar"></div>
        <div class="cat-page-deco"></div>
        <div class="cat-page-inner">
            <div class="cat-page-sub">ILMIGROSIR</div>
            <div class="cat-page-title">Katalog <span>Produk</span></div>
        </div>
    </div>
    <div class="search-float">
    """)

    keyword = st.text_input(
        "Cari",
        placeholder="🔍 Cari nama barang… (mie, gula, kopi)",
        key="kw",
    )

    st.html('</div>')

    if df.empty:
        st.error("Database belum ada. Silakan upload via halaman Admin.")
        st.stop()

    cat_list    = ["Semua"] + all_cats
    cat_display = ["🛒 Semua"] + [f"{cat_icon(c)} {c}" for c in all_cats]

    st.html('<div style="padding:0 16px 4px;"><span style="font-size:12px;font-weight:800;color:#6B7A99;text-transform:uppercase;letter-spacing:1px;">Filter Kategori</span></div>')

    chosen_display = st.radio(
        "Kategori",
        options=cat_display,
        horizontal=True,
        label_visibility="collapsed",
        key="cat_radio",
    )
    chosen_idx = cat_display.index(chosen_display)
    selected   = cat_list[chosen_idx]

    filtered = df.copy()
    if selected != "Semua":
        mask     = df["Jenis"].str.strip().str.lower() == selected.strip().lower()
        filtered = filtered[mask]
    kw = keyword.strip()
    if kw:
        filtered = filtered[filtered["Nama Item"].str.contains(kw, case=False, na=False)]

    groups          = filtered.groupby(["Kode Item", "Nama Item", "Jenis"], sort=False)
    unique_products = list(groups)
    n               = len(unique_products)

    cat_label = f'{cat_icon(selected)} {selected}' if selected != 'Semua' else '🛒 Semua Kategori'
    st.html(f"""
    <div class="result-strip">
        <span class="result-label">{cat_label}</span>
        <span class="result-count">{n:,} Item</span>
    </div>
    """)

    if n == 0:
        st.html("""
        <div class="m-empty">
            <span class="m-empty-icon">📦</span>
            <div class="m-empty-title">Produk Tidak Ditemukan</div>
            <div class="m-empty-sub">Coba kata kunci lain atau pilih kategori yang berbeda.</div>
        </div>
        """)
    else:
        parts = ['<div class="catalog-feed">']
        for (kode, nama, jenis), gdf in unique_products:
            parts.append(build_card(kode, nama, jenis, gdf))
        parts.append("</div>")
        st.html("".join(parts))

    st.html("""
    <div class="app-footer">
        <div class="af-brand">ILMI<span>GROSIR</span></div>
        <div class="af-tag">Jual Kembali · Untung Berkali</div>
        <div class="af-divider"></div>
        <div class="af-dev">Developed by <strong>NAUFAL TECH</strong></div>
    </div>
    """)


# ══════════════════════════════════════════════════════════════
# ═══ PAGE: ADMIN ═══
# ══════════════════════════════════════════════════════════════
elif page == "admin":

    st.html("""
    <div class="admin-hero">
        <div class="admin-hero-topbar"></div>
        <div class="admin-hero-deco"></div>
        <div class="admin-hero-deco2"></div>
        <div class="admin-hero-inner">
            <div class="admin-badge-row">
                <span class="admin-badge"><span class="admin-badge-dot"></span>Panel Kontrol</span>
            </div>
            <div class="admin-title">Admin <span>Dashboard</span></div>
            <div class="admin-subtitle">Kelola database produk, pantau statistik, dan konfigurasi sistem ILMIGROSIR</div>
        </div>
    </div>
    <div class="admin-body">
    """)

    # ─── AUTH ───
    if not st.session_state.admin_auth:
        st.html("""
        <div class="admin-card">
            <div class="admin-card-head">
                <div class="admin-card-head-icon ach-red">🔐</div>
                <div class="admin-card-head-text">
                    <div class="acht">Autentikasi Admin</div>
                    <div class="achs">Masukkan password untuk melanjutkan</div>
                </div>
            </div>
            <div class="admin-card-body">
        """)
        pw = st.text_input("Password Admin", type="password", key="admin_pw_input",
                           placeholder="Masukkan password rahasia…")
        if pw == ADMIN_PASSWORD:
            st.session_state.admin_auth = True
            st.rerun()
        elif pw:
            st.error("❌ Password salah. Coba lagi.")
        st.html("</div></div>")

        st.html("""
        <div style="text-align:center;padding:20px;">
            <div style="font-size:48px;margin-bottom:12px;">🔒</div>
            <div style="font-size:14px;font-weight:800;color:#0E1B3D;margin-bottom:6px;">Area Terbatas</div>
            <div style="font-size:12px;color:#6B7A99;font-weight:600;line-height:1.6;">
                Halaman ini hanya untuk administrator resmi ILMIGROSIR.<br>
                Masukkan password untuk mengakses panel kontrol.
            </div>
        </div>
        """)

    else:
        # ─── STATS GRID ───
        db_status = "✅ Aktif" if not df.empty else "❌ Tidak Ada"
        last_update = "–"
        if os.path.exists(CSV_PATH):
            ts = os.path.getmtime(CSV_PATH)
            last_update = datetime.datetime.fromtimestamp(ts).strftime("%d %b %Y, %H:%M")

        st.html(f"""
        <div class="sec-divider">
            <div class="sec-divider-line"></div>
            <div class="sec-divider-label">Statistik Database</div>
            <div class="sec-divider-line"></div>
        </div>
        <div class="admin-stats-grid">
            <div class="admin-stat-card">
                <div class="asc-icon">📦</div>
                <span class="asc-num" style="color:#1B3FA0;">{total_produk:,}</span>
                <span class="asc-label">Total Produk</span>
            </div>
            <div class="admin-stat-card">
                <div class="asc-icon">🗂️</div>
                <span class="asc-num" style="color:#E31E24;">{total_kategori}</span>
                <span class="asc-label">Kategori</span>
            </div>
            <div class="admin-stat-card">
                <div class="asc-icon">⭐</div>
                <span class="asc-num" style="color:#C49A00;">{total_grosir:,}</span>
                <span class="asc-label">Item Grosir</span>
            </div>
            <div class="admin-stat-card">
                <div class="asc-icon">🕐</div>
                <span class="asc-num" style="color:#1B3FA0;font-size:16px;line-height:1.4;">{last_update}</span>
                <span class="asc-label">Update Terakhir</span>
            </div>
        </div>
        """)

        # ─── DB STATUS CARD ───
        st.html(f"""
        <div class="sec-divider">
            <div class="sec-divider-line"></div>
            <div class="sec-divider-label">Status Sistem</div>
            <div class="sec-divider-line"></div>
        </div>
        <div class="admin-card">
            <div class="admin-card-head">
                <div class="admin-card-head-icon ach-blue">📊</div>
                <div class="admin-card-head-text">
                    <div class="acht">Informasi Database</div>
                    <div class="achs">Status dan konfigurasi sistem</div>
                </div>
            </div>
            <div class="admin-card-body">
                <div class="info-row">
                    <span class="info-label">Status Database</span>
                    <span class="status-pill {'sp-green' if not df.empty else 'sp-red'}">{db_status}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">File Database</span>
                    <span class="info-value" style="font-size:11px;color:#6B7A99;">{CSV_PATH}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Nomor WhatsApp</span>
                    <span class="info-value blue">+{WA_NUMBER}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Total Baris Data</span>
                    <span class="info-value blue">{len(df):,} baris</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Versi Aplikasi</span>
                    <span class="status-pill sp-blue">v2.0.0</span>
                </div>
            </div>
        </div>
        """)

        # ─── UPLOAD CARD ───
        st.html(f"""
        <div class="sec-divider">
            <div class="sec-divider-line"></div>
            <div class="sec-divider-label">Kelola Database</div>
            <div class="sec-divider-line"></div>
        </div>
        <div class="admin-card">
            <div class="admin-card-head">
                <div class="admin-card-head-icon ach-yellow">📤</div>
                <div class="admin-card-head-text">
                    <div class="acht">Upload Database Baru</div>
                    <div class="achs">Format CSV dari ekspor iPOS 5</div>
                </div>
            </div>
            <div class="admin-card-body">
                <div style="background:#FFFBEA;border:1.5px solid #F5C400;border-radius:12px;padding:12px 14px;margin-bottom:14px;font-size:12px;font-weight:700;color:#7A5E00;line-height:1.6;">
                    ⚠️ <strong>Kolom wajib:</strong> Kode Item, Nama Item, Jenis, Konversi, Satuan, Harga Retail, Harga Grosir
                </div>
        """)

        up = st.file_uploader("Upload file CSV", type=["csv"], label_visibility="collapsed")
        if up:
            try:
                new_df = pd.read_csv(up)
                req = {"Kode Item","Nama Item","Jenis","Konversi","Satuan","Harga Retail","Harga Grosir"}
                if not req.issubset(set(new_df.columns)):
                    st.error(f"❌ Kolom tidak lengkap. Butuh: {req}")
                else:
                    new_df.to_csv(CSV_PATH, index=False)
                    st.cache_data.clear()
                    st.success(f"✅ {len(new_df):,} baris data berhasil disimpan!")
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Gagal memproses file: {e}")

        st.html("</div></div>")

        # ─── LOGOUT / TIPS ───
        st.html("""
        <div class="admin-card" style="margin-top:16px;">
            <div class="admin-card-head">
                <div class="admin-card-head-icon ach-red">💡</div>
                <div class="admin-card-head-text">
                    <div class="acht">Tips Penggunaan</div>
                    <div class="achs">Panduan untuk admin</div>
                </div>
            </div>
            <div class="admin-card-body" style="font-size:12px;color:#6B7A99;font-weight:700;line-height:1.8;">
                <div style="margin-bottom:6px;">📌 Export data dari iPOS 5 dalam format CSV</div>
                <div style="margin-bottom:6px;">📌 Pastikan semua kolom wajib tersedia sebelum upload</div>
                <div style="margin-bottom:6px;">📌 Data lama akan otomatis digantikan setelah upload</div>
                <div>📌 Refresh halaman setelah upload untuk melihat perubahan</div>
            </div>
        </div>
        """)

        if st.button("🚪 Keluar dari Admin Panel", use_container_width=True):
            st.session_state.admin_auth = False
            st.rerun()

    st.html("</div>")  # close admin-body

    st.html("""
    <div class="app-footer">
        <div class="af-brand">ILMI<span>GROSIR</span></div>
        <div class="af-tag">Admin Panel · Akses Terbatas</div>
        <div class="af-divider"></div>
        <div class="af-dev">Developed by <strong>NAUFAL TECH</strong></div>
    </div>
    """)
