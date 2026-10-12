# Basis Data Lokal Aksara & Kamus (JSON Data)

Folder ini berfungsi sebagai **penyimpan data lokal offline (Database JSON)** yang digunakan langsung oleh aplikasi interaktif di website:

## Berkas & Relasi Penggunaannya:
- **`kana.json`**:
  - Berisi daftar karakter Hiragana & Katakana, romaji, pelafalan, dan contoh kata.
  - **Terhubung ke**: [kelas/latihan.html](file:///home/hans/Mirai-No-Webu/kelas/latihan.html) (bank soal kuis latihan aksara) dan modul pelafalan audio kana.
- **`kanji.json`**:
  - Berisi 2.136 karakter Jōyō Kanji lengkap dengan arti bahasa Indonesia, onyomi, kunyomi, level JLPT, dan contoh kosakata.
  - **Terhubung ke**: [kamus/index.html](file:///home/hans/Mirai-No-Webu/kamus/index.html) dan [kamus/kanji.html](file:///home/hans/Mirai-No-Webu/kamus/kanji.html) sebagai basis data pencarian offline instan.
- **`kanji-meta.json`**:
  - Berisi metadata indeks radikal, jumlah goresan (stroke count), dan grade kurikulum sekolah Jepang.
  - **Terhubung ke**: Mesin penyortiran cepat kamus kanji (`js/kanji.js`).
- **`STROKES-LICENSE.md`**:
  - Dokumen lisensi resmi data vektor urutan goresan KanjiVG.
