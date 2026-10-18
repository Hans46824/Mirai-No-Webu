# Basis Data Lokal Aksara & Kamus (JSON Data)

Folder ini berfungsi sebagai **penyimpan basis data lokal offline (Database JSON)** yang menyuplai kamus interaktif, modul kelas, latihan mandiri, dan kanvas goresan di website **Mirai no Webu**:

## 📚 Berkas & Relasi Penggunaannya:
- **`kanji.json`** *(Single Source of Truth)*:
  - Basis data master berisi 2.211 karakter Jōyō Kanji dan JLPT N5–N1 lengkap dengan arti bahasa Indonesia terkurasi, bacaan Onyomi/Kunyomi, level JLPT, jumlah goresan, contoh kosakata (`words`), kalimat contoh (`sentence`), penanda template (`sentence_is_template`), serta kata contoh terbaik (`example_word`).
  - Menjadi sumber utama untuk menghasilkan berkas artefak `data/kanji-index.json`, chunk `data/kanji/*.json`, dan `js/kanji-data.js`.
- **`kanji-index.json`**:
  - Indeks data kanji super-ringkas (~316 KB) untuk pencarian instan berbobot (Ranked Search), penyaringan level JLPT, dan pagination tanpa membebani kuota awal.
- **`kanji/`** (`n5.json`, `n4.json`, `n3.json`, `n2.json`, `n1.json`):
  - Chunk modular data detail kanji (kosakata lengkap & contoh kalimat) yang dimuat secara *on-demand* saat kanji pertama dari level terkait dibuka oleh pengguna.
- **`stroke-master.json`** *(Single Source of Truth Goresan)*:
  - Basis data master 2.375 karakter vektor koordinat goresan KanjiVG terkalibrasi.
- **`strokes/`** (`n5.json`, `n4.json`, `n3.json`, `n2.json`, `n1.json`):
  - Chunk modular vektor goresan SVG kanji per level JLPT yang dimuat secara *on-demand*.
- **`kana.json`**:
  - Berisi daftar karakter Hiragana & Katakana, romaji, pelafalan audio, dan contoh kata untuk kuis latihan aksara di `kelas/latihan.html`.
- **`kanji-meta.json`**:
  - Berisi metadata indeks radikal, jumlah goresan (*stroke count*), dan *grade* kurikulum sekolah Jepang.
- **`stroke-overrides.json`**:
  - Lapisan override pelindung perbaikan manual goresan dan varian buku teks (*kyōkasho*) agar tidak pernah tertimpa pipeline otomatis.
- **`stroke-coverage-manifest.json`**:
  - Laporan validasi cakupan integritas data goresan (100% karakter terverifikasi).
- **`STROKES-LICENSE.md`**:
  - Dokumen lisensi resmi data vektor urutan goresan KanjiVG.

---

## ⚖️ Sumber Data & Lisensi Terbuka (Open Data Attribution):
Seluruh data kamus dan aksara dalam direktori ini berasal dari proyek komunitas terbuka internasional dan **BUKAN merupakan karya cipta mandiri klub Mirai no Hana**:
1. **KANJIDIC2 & JMdict**:
   - Hak Cipta © *Electronic Dictionary Research and Development Group (EDRDG)* — Jim Breen dkk ([https://www.edrdg.org](https://www.edrdg.org)).
   - Dilisensikan di bawah [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).
2. **KanjiVG**:
   - Hak Cipta © Ulrich Apel dan kontributor ([https://kanjivg.tagaini.net](https://kanjivg.tagaini.net)).
   - Dilisensikan di bawah [Creative Commons Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)](https://creativecommons.org/licenses/by-sa/3.0/).
