# 📊 Laporan Audit Bobot Statik & Performa Halaman (Page Weight)

> Tanggal Audit: 2026-10-18 | Total Halaman: **33 halaman HTML**
> Standar Kinerja: Evaluasi beban awal (HTML, CSS, JS, initial dataset) raw bytes & estimasi transfer Gzip.

---

## 🏆 Ringkasan Target & Hasil Optimasi Kamus

| Metrik Kinerja | Target Pengguna | Hasil Aktual (Raw) | Hasil Aktual (Gzip) | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Beban Data Kamus Awal** (`kanji-index.json` + `stroke-data.js` Kana) | ≤ 700 KB | **388.5 KB** | **66.4 KB** | ✅ Lolos Target |
| **Total Transfer Jaringan Kamus** (HTML + CSS + JS + Data Awal, Gzip) | ≤ 700 KB | **1614.2 KB (raw)** | **301.7 KB** | ✅ Lolos Target |
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
| 1 | `kamus/index.html` | 43.3k / 9.9k | 879.5k / 138.3k | 374.7k / 105.1k | 316.6k / 48.4k | **1614.2 KB** | **301.7 KB** |
| 2 | `kamus/kanji.html` | 12.8k / 3.9k | 879.5k / 138.3k | 374.7k / 105.1k | 316.6k / 48.4k | **1583.7 KB** | **295.7 KB** |
| 3 | `kelas/latihan.html` | 122.5k / 21.6k | 879.5k / 138.3k | 364.6k / 91.9k | — | **1366.6 KB** | **251.8 KB** |
| 4 | `lomba/index.html` | 146.4k / 21.4k | 879.5k / 138.3k | 265.1k / 64.9k | — | **1291.0 KB** | **224.6 KB** |
| 5 | `rekomendasi/index.html` | 93.1k / 15.9k | 879.5k / 138.3k | 265.1k / 64.9k | — | **1237.6 KB** | **219.1 KB** |
| 6 | `toko/index.html` | 71.2k / 13.2k | 879.5k / 138.3k | 265.1k / 64.9k | — | **1215.7 KB** | **216.4 KB** |
| 7 | `peringkat/index.html` | 35.7k / 7.9k | 879.5k / 138.3k | 296.6k / 70.7k | — | **1211.8 KB** | **216.9 KB** |
| 8 | `tentang/index.html` | 62.0k / 13.3k | 879.5k / 138.3k | 132.7k / 33.8k | — | **1074.1 KB** | **185.4 KB** |
| 9 | `index.html` | 68.5k / 15.5k | 879.5k / 138.3k | 103.4k / 29.3k | — | **1051.5 KB** | **183.1 KB** |
| 10 | `kegiatan/nihon-go-rajio.html` | 35.6k / 8.1k | 879.5k / 138.3k | 106.4k / 29.7k | — | **1021.5 KB** | **176.1 KB** |
| 11 | `kegiatan/index.html` | 31.8k / 7.2k | 879.5k / 138.3k | 106.4k / 29.7k | — | **1017.7 KB** | **175.2 KB** |
| 12 | `kelas/motivasi.html` | 30.2k / 7.1k | 879.5k / 138.3k | 103.4k / 29.3k | — | **1013.2 KB** | **174.7 KB** |
| 13 | `kelas/index.html` | 27.2k / 5.0k | 879.5k / 138.3k | 103.4k / 29.3k | — | **1010.1 KB** | **172.6 KB** |
| 14 | `materi/lanjutan/kanji.html` | 24.6k / 6.2k | 879.5k / 138.3k | 103.4k / 29.3k | — | **1007.5 KB** | **173.8 KB** |
| 15 | `materi/lanjutan/grammar.html` | 24.6k / 6.1k | 879.5k / 138.3k | 103.4k / 29.3k | — | **1007.5 KB** | **173.7 KB** |
| 16 | `divisi/index.html` | 13.2k / 3.9k | 879.5k / 138.3k | 114.5k / 32.9k | — | **1007.2 KB** | **175.2 KB** |
| 17 | `materi/lanjutan/kalimat.html` | 23.5k / 5.9k | 879.5k / 138.3k | 103.4k / 29.3k | — | **1006.4 KB** | **173.5 KB** |
| 18 | `kegiatan/ramadhan.html` | 18.7k / 4.7k | 879.5k / 138.3k | 106.4k / 29.7k | — | **1004.6 KB** | **172.7 KB** |
| 19 | `kegiatan/konbini.html` | 18.7k / 4.8k | 879.5k / 138.3k | 106.4k / 29.7k | — | **1004.5 KB** | **172.8 KB** |
| 20 | `kegiatan/kimi-to-nippon.html` | 18.6k / 4.7k | 879.5k / 138.3k | 106.4k / 29.7k | — | **1004.5 KB** | **172.7 KB** |
| 21 | `kegiatan/tomodachi.html` | 18.6k / 4.7k | 879.5k / 138.3k | 106.4k / 29.7k | — | **1004.5 KB** | **172.7 KB** |
| 22 | `materi/dasar/kosakata.html` | 21.0k / 5.6k | 879.5k / 138.3k | 103.4k / 29.3k | — | **1003.9 KB** | **173.2 KB** |
| 23 | `materi/dasar/jikoshokai.html` | 20.3k / 5.3k | 879.5k / 138.3k | 103.4k / 29.3k | — | **1003.3 KB** | **172.9 KB** |
| 24 | `materi/dasar/hiragana.html` | 19.7k / 5.4k | 879.5k / 138.3k | 103.4k / 29.3k | — | **1002.6 KB** | **173.0 KB** |
| 25 | `materi/dasar/katakana.html` | 19.5k / 5.4k | 879.5k / 138.3k | 103.4k / 29.3k | — | **1002.4 KB** | **173.0 KB** |
| 26 | `materi/dasar/index.html` | 16.8k / 4.1k | 879.5k / 138.3k | 103.4k / 29.3k | — | **999.7 KB** | **171.7 KB** |
| 27 | `materi/lanjutan/index.html` | 13.0k / 3.6k | 879.5k / 138.3k | 103.4k / 29.3k | — | **995.9 KB** | **171.2 KB** |
| 28 | `divisi/cosplay.html` | 14.9k / 4.5k | 879.5k / 138.3k | 101.1k / 28.0k | — | **995.5 KB** | **170.8 KB** |
| 29 | `divisi/kewirausahaan.html` | 14.9k / 4.5k | 879.5k / 138.3k | 101.1k / 28.0k | — | **995.5 KB** | **170.8 KB** |
| 30 | `divisi/bahasa.html` | 14.8k / 4.5k | 879.5k / 138.3k | 101.1k / 28.0k | — | **995.4 KB** | **170.8 KB** |
| 31 | `divisi/desain.html` | 14.8k / 4.5k | 879.5k / 138.3k | 101.1k / 28.0k | — | **995.4 KB** | **170.8 KB** |
| 32 | `404.html` | 13.0k / 3.9k | 879.5k / 138.3k | 101.1k / 28.0k | — | **993.5 KB** | **170.2 KB** |
| 33 | `sora/index.html` | 49.4k / 11.0k | 0.0k / 0.0k | 0.0k / 0.0k | — | **49.4 KB** | **11.0 KB** |

---

## 🛠️ Optimasi yang Telah Diterapkan
1. **Local-First & Single Source of Truth**: Seluruh kanjiJoyo & JLPT (2.211 karakter) bersumber dari `data/kanji.json`. Panggilan jaringan luar ke `kanjiapi.dev` dan `mymemory.translated.net` telah 100% ditiadakan.
2. **Modular Chunking**: Dataset kamus dipecah menjadi indeks ramping (`data/kanji-index.json`, 316 KB) dan chunk per level JLPT (`data/kanji/<jlpt>.json` & `data/strokes/<jlpt>.json`).
3. **Non-Blocking Font Rendering**: Menghapus `@import url('https://fonts.googleapis.com/...')` dari `css/style.css`. Browser langsung mengunduh font secara konkuren lewat `<link rel="preconnect">` dan `<link rel="stylesheet">` di `<head>`.
4. **Script Deferring**: Seluruh tag `<script src="...">` dilengkapi atribut `defer` agar proses parsing dan render DOM tidak terblokir eksekusi JavaScript.
5. **CLS Prevention & Image Lazy Loading**: Seluruh 444 tag `<img>` di bawah layar awal telah dilengkapi `loading="lazy" decoding="async"` serta dimensi eksplisit `width` dan `height` yang dihitung otomatis dari dimensi file aset asli.
6. **Automated Content-Hash Versioning**: Skrip `skrip/arsip/stamp_asset_versions.py` otomatis menghitung hash konten SHA-256 (8 karakter) untuk seluruh CSS dan JS lokal (`?v=<hash>`), memaksimalkan cache browser.
