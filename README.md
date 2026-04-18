# 🛒 Katalog Harga Publik ILMIGROSIR

> **Developed by NOPAL TECH**

Aplikasi katalog harga produk grosir berbasis Streamlit, mobile-friendly, dan siap deploy ke Streamlit Cloud.

---

## 📂 Struktur File

```
ilmigrosir_katalog/
├── app.py                                   # Aplikasi utama Streamlit
├── requirements.txt                         # Dependensi Python
├── logo.jpg                                 # Logo ILMIGROSIR
├── UPDATE PERJUMLAH IPOS 5.xlsx - Sheet.csv # Database produk (dari iPOS 5)
└── README.md
```

---

## 🚀 Cara Deploy ke Streamlit Cloud

1. **Upload ke GitHub**
   - Buat repository baru di GitHub (bisa private)
   - Upload semua file di folder ini ke repo tersebut

2. **Deploy di Streamlit Cloud**
   - Buka [share.streamlit.io](https://share.streamlit.io)
   - Login dengan akun GitHub
   - Klik **New app** → pilih repo → pilih `app.py`
   - Klik **Deploy** → tunggu beberapa menit

3. **Selesai!** App siap disebarkan via link publik.

---

## ⚙️ Konfigurasi Awal

Sebelum deploy, edit baris berikut di `app.py`:

```python
WA_NUMBER = "6281234567890"  # ← Ganti dengan nomor WhatsApp admin (format: 62xxx)
```

---

## 🔐 Menu Admin

- Klik expander **"⚙️ Menu Admin (tersembunyi)"** di bagian bawah halaman
- Masukkan password: `nopal123`
- Upload ulang CSV database tanpa perlu deploy ulang

---

## 📊 Format CSV Database (iPOS 5)

File CSV harus memiliki kolom berikut:

| Kolom | Keterangan |
|---|---|
| Kode Item | Kode unik produk |
| Nama Item | Nama produk |
| Jenis | Kategori produk |
| Konversi | Jumlah isi per satuan |
| Satuan | PCS / PAK / DUS / dll |
| Harga Retail | Harga jual eceran |
| Harga Grosir | Harga grosir (0 jika tidak ada) |

---

## ✨ Fitur

- 🔍 Pencarian real-time nama barang
- 📂 Filter per kategori (Jenis)
- 📦 Grouping otomatis PCS/PAK/DUS dalam satu kartu
- 💛 Badge "Grosir (>3)" + tampilkan penghematan
- 💬 Tombol Cek Stok → WhatsApp otomatis dengan nama barang
- 📱 Mobile-first UI
- 🔒 Admin panel tersembunyi dengan password

---

*© 2025 ILMIGROSIR · Jual Lagi, Untung Kembali*
