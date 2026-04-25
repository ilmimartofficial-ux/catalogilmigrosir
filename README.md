# 📦 ILMIGROSIR — Website Toko Grosir Online

**JUAL KEMBALI UNTUNG BERKALI** — Website toko grosir dengan AI Chat, upload Excel, dan catalog produk lengkap.

---

## 🏗️ Struktur Proyek

```
ilmigrosir/
├── frontend/          ← React (deploy ke Vercel — GRATIS)
│   ├── src/
│   │   ├── api/client.js
│   │   ├── components/
│   │   ├── pages/
│   │   └── styles/
│   ├── package.json
│   └── vercel.json
│
└── backend/           ← Express + SQLite (deploy ke Railway — GRATIS)
    ├── server.js
    ├── src/
    │   ├── db/database.js
    │   └── routes/
    └── package.json
```

---

## 🚀 PANDUAN DEPLOY LENGKAP (Gratis 100%)

### Bagian 1 — Upload ke GitHub

1. Buat akun di [github.com](https://github.com) jika belum punya
2. Buat **2 repository baru**:
   - `ilmigrosir-backend`
   - `ilmigrosir-frontend`
3. Upload file backend ke repo `ilmigrosir-backend`
4. Upload file frontend ke repo `ilmigrosir-frontend`

**Cara upload via GitHub web (tanpa Git):**
- Buka repo → klik **"Add file"** → **"Upload files"**
- Drag & drop semua file, klik **"Commit changes"**

---

### Bagian 2 — Deploy Backend ke Railway

**Railway = hosting backend GRATIS (500 jam/bulan)**

#### Langkah-langkah:

1. Buka [railway.app](https://railway.app) → Login dengan GitHub
2. Klik **"New Project"** → **"Deploy from GitHub repo"**
3. Pilih repo `ilmigrosir-backend`
4. Tunggu deploy selesai (biasanya 2-3 menit)
5. Klik tab **"Variables"** → tambahkan environment variables:

```
ANTHROPIC_API_KEY    = (isi API key Anthropic kamu — lihat cara dapat di bawah)
ADMIN_PASSWORD       = nopal123
JWT_SECRET           = ilmigrosir_s3cr3t_k3y_2024
DB_DIR               = /data
FRONTEND_URL         = (kosongkan dulu, isi setelah frontend deploy)
```

6. Klik tab **"Settings"** → **"Volumes"** → **"New Volume"**
   - Mount path: `/data`
   - Ini agar database tidak hilang saat restart!

7. Catat **URL backend** kamu (contoh: `https://ilmigrosir-backend.up.railway.app`)

---

### Bagian 3 — Cara Dapat API Key Anthropic (GRATIS)

1. Buka [console.anthropic.com](https://console.anthropic.com)
2. Daftar akun baru (gratis, pakai email)
3. Klik **"API Keys"** → **"Create Key"**
4. Copy API key (format: `sk-ant-...`)
5. Paste ke Railway di variable `ANTHROPIC_API_KEY`

> **Catatan:** Akun baru dapat $5 credit gratis ≈ ribuan percakapan dengan model Haiku!

---

### Bagian 4 — Deploy Frontend ke Vercel

**Vercel = hosting frontend GRATIS (unlimited)**

#### Langkah-langkah:

1. Buka [vercel.com](https://vercel.com) → Login dengan GitHub
2. Klik **"New Project"** → Import repo `ilmigrosir-frontend`
3. Di bagian **"Environment Variables"**, tambahkan:

```
VITE_API_URL = https://ilmigrosir-backend.up.railway.app
```
(Ganti dengan URL Railway kamu dari Bagian 2)

4. Klik **"Deploy"** → tunggu 1-2 menit
5. Catat URL frontend kamu (contoh: `https://ilmigrosir.vercel.app`)

---

### Bagian 5 — Sambungkan Frontend & Backend

1. Kembali ke Railway
2. Di tab **Variables**, update:
```
FRONTEND_URL = https://ilmigrosir.vercel.app
```
(Ganti dengan URL Vercel kamu)

3. Railway akan auto-restart backend
4. Website siap digunakan! ✅

---

## 📊 Upload Data Produk (Excel)

### Format Kolom Excel yang Didukung:

| Kolom | Wajib | Keterangan |
|-------|-------|------------|
| Nama Item | ✅ | Nama produk |
| Kode Item | ❌ | Kode/SKU produk |
| Jenis | ❌ | Kategori (SNACK, MINUMAN, dll) |
| Satuan | ❌ | KARTON, LUSIN, PCS, dll |
| ISI | ❌ | Jumlah isi per satuan |
| Stok | ❌ | Jumlah stok |
| Harga Retail | ❌ | Harga eceran |
| Harga Grosir | ❌ | Harga grosir |
| DASAR | ❌ | Satuan dasar (PCS, dll) |
| Pokok | ❌ | Harga pokok (tidak ditampilkan) |

### Cara Upload:
1. Buka website → scroll ke bawah → klik **Admin** (ikon gembok di navbar)
2. Atau langsung ke: `https://website-kamu.vercel.app/admin`
3. Login dengan password: `nopal123`
4. Drag & drop file Excel atau klik "Pilih File"
5. Data langsung tersinkron ke semua perangkat!

---

## ⚙️ Konfigurasi Lokal (untuk testing)

### Backend:
```bash
cd backend
npm install
cp .env.example .env
# Edit .env, isi ANTHROPIC_API_KEY
npm run dev
# Running di http://localhost:3001
```

### Frontend:
```bash
cd frontend
npm install
cp .env.example .env
# Edit .env: VITE_API_URL=http://localhost:3001
npm run dev
# Running di http://localhost:5173
```

---

## 🔧 Fitur Lengkap

| Fitur | Keterangan |
|-------|------------|
| 📦 Katalog Produk | Grid produk dengan search & filter kategori |
| 🔍 Pencarian Real-time | Cari nama, kode, atau kategori produk |
| 🤖 Chat AI | Asisten AI akses database real-time |
| 📊 Upload Excel | Sinkron database dari file .xlsx |
| 📱 Mobile-First | Responsive semua perangkat |
| 🛒 Order via WA | Tombol pesan langsung ke WhatsApp |
| 🔐 Admin Panel | Login aman, upload, riwayat |
| 💾 Database Persisten | SQLite dengan volume Railway |

---

## 🆘 Troubleshooting

**Q: Chat AI tidak merespons?**
- Cek ANTHROPIC_API_KEY sudah diisi di Railway
- Pastikan format key benar: `sk-ant-...`

**Q: Data produk hilang setelah restart Railway?**
- Pastikan sudah buat Volume di Railway dengan mount path `/data`
- Pastikan variable `DB_DIR=/data` sudah diset

**Q: Gambar tidak muncul / website error?**
- Cek variable `VITE_API_URL` di Vercel sudah mengarah ke URL Railway yang benar
- Pastikan URL Railway tidak ada trailing slash `/`

**Q: Upload Excel gagal?**
- Pastikan kolom "Nama Item" ada di file Excel
- Cek ukuran file tidak melebihi 50MB
- Coba format file .xlsx (bukan .xls lama)

---

## 📞 Kontak

WhatsApp: **085373373233**

---

*Dibuat dengan ❤️ untuk ILMIGROSIR*
