# 🛠️ Kumpulan Skrip Utilitas Pemeliharaan (Mirai No Webu)

Folder ini berisi 5 skrip utilitas pemeliharaan utama berbasis Python (`.py`) yang digunakan oleh pengembang dan AI asisten untuk pemeliharaan performa, data, dan arsitektur kode:

## 📋 5 Skrip Utilitas Utama:

1. **`skrip/optimasi-performa.py`**
   - Kompresi gambar WebP/PNG secara fisik.
   - Preload aset Hero & prioritas tinggi di seluruh halaman web.
   - Sinkronisasi version hash aset (`?v=...`) ke seluruh file HTML & `service-worker.js`.

2. **`skrip/rapikan-kode.py`**
   - Formatter multi-line CSS/JS & pembersih trailing whitespace.
   - Pembersihan otomatis cache `__pycache__` dan file temporer `.pyc`.
   - Pengecekan keseimbangan kurung & delimiter di seluruh kode JavaScript.

3. **`skrip/validasi-goresan.py`**
   - Validator independen data urutan goresan KanjiVG (`js/stroke-data.js` & `data/strokes/*.json`).
   - Memeriksa keabsahan path SVG, format viewBox (0..109), dan urutan goresan karakter.
   - Menghasilkan manifest cakupan data di `data/stroke-coverage-manifest.json`.

4. **`skrip/sinkron-data-kamus.py`**
   - Sinkronisasi master data `data/kanji.json` ke indeks ramping `data/kanji-index.json`.
   - Pemecahan data kamus & koordinat goresan menjadi chunk on-demand per level JLPT (N5–N1).
   - Memastikan initial load kamus tetap ringan (<= 700 KB).

5. **`skrip/cek-ukuran-web.py`**
   - Audit beban statik ukuran seluruh halaman web dan aset lokal (HTML, CSS, JS, data JSON).
   - Menghitung ukuran mentah (*raw bytes*) dan estimasi transfer terkompresi (*gzip*).
   - Menulis laporan terstruktur ke `skrip/laporan/page-weight.md`.

---

> [!NOTE]
> **Catatan Pengembang**: Skrip-skrip ini **hanya dijalankan di terminal lokal saat proses pengembangan**, dan **TIDAK dijalankan di peramban pengguna** (website berjalan mandiri dengan HTML, CSS, dan JavaScript).
