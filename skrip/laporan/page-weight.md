# 📊 Laporan Audit Bobot Statik & Performa Halaman (Page Weight)

> Tanggal Audit: 2026-10-18 | Total Halaman: **34 halaman HTML**
> Standar Kinerja: Evaluasi beban awal (HTML, CSS, JS, initial dataset) raw bytes & estimasi transfer Gzip.

---

## 🏆 Ringkasan Target & Hasil Optimasi Kamus

| Metrik Kinerja | Target Pengguna | Hasil Aktual (Raw) | Hasil Aktual (Gzip) | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Beban Data Kamus Awal** (`kanji-index.json` + `stroke-data.js` Kana) | ≤ 700 KB | **388.5 KB** | **66.4 KB** | ✅ Lolos Target |
| **Total Transfer Jaringan Kamus** (HTML + CSS + JS + Data Awal, Gzip) | ≤ 700 KB | **1829.9 KB (raw)** | **337.8 KB** | ✅ Lolos Target |
| **Beban Kanji N5 Pertama Dibuka** (detail teks `data/kanji/n5.json`) | ≤ +60 KB | **+50.3 KB** | **+10.5 KB** | ✅ Lolos Target |
| **Beban Vektor Goresan N5 Pertama Dibuka** (KanjiVG `data/strokes/n5.json`) | On-demand chunk | **+59.1 KB** | **+20.8 KB** | ✅ Modular |
| **Panggilan Jaringan Eksternal** (KanjiAPI / MyMemory) | 0 panggilan | **0 KB (100% Offline)** | **0 KB** | ✅ Local-First |

---

## 🔬 Rincian Arsitektur Data Kamus (Sebelum vs Sesudah)

```
SEBELUM (Muat Penuh di Awal):
  ├── js/stroke-data.js        : 4.200 KB
  ├── js/kanji-data.js         : 1.800 KB
  └── fetch data/kanji.json    : 2.400 KB
  ---------------------------------------------
  Total Beban Awal Data        : 8.400 KB (~8,4 MB)  💥 Lambat di HP/Wifi sekolah

SESUDAH (Modular Index & On-Demand Chunks):
  ├── js/stroke-data.js (Kana) :     71.9 KB  (Gzip:  17.9 KB)
  └── data/kanji-index.json    :   316.6 KB  (Gzip:  48.4 KB)
  ---------------------------------------------
  Total Beban Awal Data        :   388.5 KB  (Gzip:  66.4 KB)  🚀 Pemangkasan 95,4%!
```

### On-Demand Chunks (Dimuat hanya saat pengguna memilih/membuka karakter):
- **Level N5**: Detail Kanji: `58.3 KB` (Gzip: `10.6 KB`) | Goresan: `59.5 KB` (Gzip: `20.9 KB`)
- **Level N4**: Detail Kanji: `135.3 KB` (Gzip: `24.3 KB`) | Goresan: `175.3 KB` (Gzip: `60.0 KB`)
- **Level N3**: Detail Kanji: `320.0 KB` (Gzip: `57.6 KB`) | Goresan: `439.6 KB` (Gzip: `148.6 KB`)
- **Level N2**: Detail Kanji: `279.9 KB` (Gzip: `50.1 KB`) | Goresan: `451.8 KB` (Gzip: `152.8 KB`)
- **Level N1**: Detail Kanji: `733.8 KB` (Gzip: `132.6 KB`) | Goresan: `1.709.5 KB` (Gzip: `572.3 KB`)

---

## 📋 Tabel Audit Bobot Seluruh Halaman (Terberat ke Teringan)

| No | Halaman HTML | HTML (Raw / Gz) | CSS Bundle (Raw / Gz) | JS Lokal (Raw / Gz) | Data Awal (Raw / Gz) | Total Raw | Transfer Gzip |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `kamus/index.html` | 54.4k / 11.5k | 1012.0k / 155.7k | 446.8k / 122.1k | 316.6k / 48.4k | **1829.9 KB** | **337.8 KB** |
| 2 | `kamus/kanji.html` | 14.7k / 4.3k | 1012.0k / 155.7k | 446.8k / 122.1k | 316.6k / 48.4k | **1790.2 KB** | **330.5 KB** |
| 3 | `kelas/latihan.html` | 124.9k / 22.1k | 1012.0k / 155.7k | 411.7k / 104.6k | — | **1548.7 KB** | **282.4 KB** |
| 4 | `lomba/index.html` | 110.5k / 19.4k | 1012.0k / 155.7k | 285.5k / 70.1k | — | **1408.0 KB** | **245.3 KB** |
| 5 | `arsip/halaman-rekomendasi/rekomendasi.archive.html` | 95.1k / 16.3k | 1012.0k / 155.7k | 285.5k / 70.1k | — | **1392.6 KB** | **242.2 KB** |
| 6 | `toko/index.html` | 74.0k / 14.0k | 1012.0k / 155.7k | 285.5k / 70.1k | — | **1371.5 KB** | **239.9 KB** |
| 7 | `peringkat/index.html` | 37.9k / 8.3k | 1012.0k / 155.7k | 317.0k / 76.0k | — | **1367.0 KB** | **240.1 KB** |
| 8 | `tentang/index.html` | 64.1k / 13.5k | 1012.0k / 155.7k | 149.9k / 38.3k | — | **1226.0 KB** | **207.6 KB** |
| 9 | `index.html` | 69.8k / 15.8k | 1012.0k / 155.7k | 120.7k / 33.8k | — | **1202.6 KB** | **205.3 KB** |
| 10 | `materi/lanjutan/grammar.html` | 30.1k / 7.0k | 1012.0k / 155.7k | 147.3k / 41.1k | — | **1189.4 KB** | **203.8 KB** |
| 11 | `materi/lanjutan/kanji.html` | 29.9k / 7.1k | 1012.0k / 155.7k | 147.3k / 41.1k | — | **1189.2 KB** | **203.9 KB** |
| 12 | `materi/lanjutan/kalimat.html` | 29.1k / 6.9k | 1012.0k / 155.7k | 147.3k / 41.1k | — | **1188.5 KB** | **203.7 KB** |
| 13 | `materi/dasar/kosakata.html` | 26.3k / 6.4k | 1012.0k / 155.7k | 147.3k / 41.1k | — | **1185.6 KB** | **203.2 KB** |
| 14 | `materi/dasar/jikoshokai.html` | 25.8k / 6.2k | 1012.0k / 155.7k | 147.3k / 41.1k | — | **1185.1 KB** | **203.0 KB** |
| 15 | `materi/dasar/hiragana.html` | 25.3k / 6.4k | 1012.0k / 155.7k | 147.3k / 41.1k | — | **1184.6 KB** | **203.2 KB** |
| 16 | `materi/dasar/katakana.html` | 25.0k / 6.3k | 1012.0k / 155.7k | 147.3k / 41.1k | — | **1184.3 KB** | **203.1 KB** |
| 17 | `materi/dasar/index.html` | 18.9k / 4.5k | 1012.0k / 155.7k | 147.3k / 41.1k | — | **1178.2 KB** | **201.3 KB** |
| 18 | `materi/lanjutan/index.html` | 15.1k / 4.0k | 1012.0k / 155.7k | 147.3k / 41.1k | — | **1174.4 KB** | **200.8 KB** |
| 19 | `kegiatan/nihon-go-rajio.html` | 36.7k / 8.4k | 1012.0k / 155.7k | 123.7k / 34.2k | — | **1172.4 KB** | **198.3 KB** |
| 20 | `kegiatan/index.html` | 30.2k / 6.9k | 1012.0k / 155.7k | 123.7k / 34.2k | — | **1165.9 KB** | **196.8 KB** |
| 21 | `kelas/motivasi.html` | 32.2k / 7.5k | 1012.0k / 155.7k | 120.7k / 33.8k | — | **1164.9 KB** | **197.0 KB** |
| 22 | `kelas/index.html` | 29.4k / 5.4k | 1012.0k / 155.7k | 120.7k / 33.8k | — | **1162.1 KB** | **194.9 KB** |
| 23 | `divisi/index.html` | 18.1k / 5.0k | 1012.0k / 155.7k | 131.8k / 37.4k | — | **1161.9 KB** | **198.1 KB** |
| 24 | `kegiatan/ramadhan.html` | 19.8k / 5.0k | 1012.0k / 155.7k | 123.7k / 34.2k | — | **1155.5 KB** | **194.8 KB** |
| 25 | `kegiatan/konbini.html` | 19.7k / 5.0k | 1012.0k / 155.7k | 123.7k / 34.2k | — | **1155.4 KB** | **194.9 KB** |
| 26 | `kegiatan/tomodachi.html` | 19.7k / 4.9k | 1012.0k / 155.7k | 123.7k / 34.2k | — | **1155.4 KB** | **194.8 KB** |
| 27 | `kegiatan/kimi-to-nippon.html` | 19.7k / 4.9k | 1012.0k / 155.7k | 123.7k / 34.2k | — | **1155.4 KB** | **194.8 KB** |
| 28 | `divisi/cosplay.html` | 16.8k / 4.9k | 1012.0k / 155.7k | 118.4k / 32.5k | — | **1147.2 KB** | **193.1 KB** |
| 29 | `divisi/kewirausahaan.html` | 16.7k / 4.8k | 1012.0k / 155.7k | 118.4k / 32.5k | — | **1147.2 KB** | **193.1 KB** |
| 30 | `divisi/desain.html` | 16.7k / 4.9k | 1012.0k / 155.7k | 118.4k / 32.5k | — | **1147.1 KB** | **193.1 KB** |
| 31 | `divisi/bahasa.html` | 16.7k / 4.8k | 1012.0k / 155.7k | 118.4k / 32.5k | — | **1147.1 KB** | **193.0 KB** |
| 32 | `404.html` | 14.8k / 4.2k | 1012.0k / 155.7k | 118.4k / 32.5k | — | **1145.2 KB** | **192.4 KB** |
| 33 | `offline.html` | 7.6k / 2.3k | 1012.0k / 155.7k | 0.0k / 0.0k | — | **1019.6 KB** | **158.0 KB** |
| 34 | `sora/index.html` | 51.2k / 11.4k | 0.0k / 0.0k | 0.0k / 0.0k | — | **51.2 KB** | **11.4 KB** |

---

## 🛠️ Optimasi yang Telah Diterapkan
1. **Local-First & Single Source of Truth**: Seluruh kanjiJoyo & JLPT (2.211 karakter) bersumber dari `data/kanji.json`. Panggilan jaringan luar ke `kanjiapi.dev` dan `mymemory.translated.net` telah 100% ditiadakan.
2. **Modular Chunking**: Dataset kamus dipecah menjadi indeks ramping (`data/kanji-index.json`, 316 KB) dan chunk per level JLPT (`data/kanji/<jlpt>.json` & `data/strokes/<jlpt>.json`).
3. **Non-Blocking Font Rendering**: Menghapus `@import url('https://fonts.googleapis.com/...')` dari `css/style.css`. Browser langsung mengunduh font secara konkuren lewat `<link rel="preconnect">` dan `<link rel="stylesheet">` di `<head>`.
4. **Script Deferring**: Seluruh tag `<script src="...">` dilengkapi atribut `defer` agar proses parsing dan render DOM tidak terblokir eksekusi JavaScript.
5. **CLS Prevention & Image Lazy Loading**: Seluruh 444 tag `<img>` di bawah layar awal telah dilengkapi `loading="lazy" decoding="async"` serta dimensi eksplisit `width` dan `height` yang dihitung otomatis dari dimensi file aset asli.
6. **Automated Content-Hash Versioning**: Skrip `skrip/arsip/stamp_asset_versions.py` otomatis menghitung hash konten SHA-256 (8 karakter) untuk seluruh CSS dan JS lokal (`?v=<hash>`), memaksimalkan cache browser.
