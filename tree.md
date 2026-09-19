# Struktur Direktori Proyek Mirai no Webu

Dokumen ini memetakan susunan file dan folder setelah proses pembersihan dan pengorganisasian (*cleanup & reorganization*).

```text
Mirai-No-Webu/
├── ai_scripts/                     # Skrip otomasi & manipulasi agen AI (.py)
│   ├── add_nametag.py
│   ├── fix_heroes.py
│   ├── fix_index_links.py
│   ├── fix_japanese.py
│   ├── fix_sora.py
│   ├── fix_sora2.py
│   ├── move_menu_btn.py
│   ├── replace_cards.py
│   ├── replace_cards_revert.py
│   ├── replace_sidebar_text.py
│   ├── replace_sora_grid.py
│   ├── update_carousel.py
│   ├── update_carousel_js.py
│   ├── update_index_hero.py
│   └── update_kelas.py
│
├── archive/                        # Arsip file pengujian & halaman cadangan lama
│   ├── advance.html                # (Placeholder materi lanjutan lama)
│   ├── reguler.html                # (Placeholder materi reguler lama)
│   ├── test-card.html              # (File uji coba komponen CSS)
│   ├── proker-gathering.html       # (Arsip layout proker lama)
│   ├── proker-konbini.html         # (Arsip layout proker lama)
│   ├── proker-matsuri.html         # (Arsip layout proker lama)
│   └── proker-rajio.html           # (Arsip layout proker lama)
│
├── data/                           # Data JSON kamus & aksara Jepang
│   ├── kana.json
│   ├── kanji.json
│   ├── kanji-meta.json
│   └── STROKES-LICENSE.md
│
├── images/                         # Aset visual (logo, karakter, icon, background)
│   ├── mirai/
│   │   ├── background/
│   │   ├── banner/
│   │   ├── haori/
│   │   ├── icon/
│   │   ├── logo/
│   │   ├── profil/
│   │   └── stiker/
│   └── ...
│
├── js/                             # Logika interaktif & clientside JavaScript
│   ├── api.js
│   ├── carousel.js
│   ├── kana.js
│   ├── kanji.js
│   ├── main.js
│   ├── proker-slider.js
│   ├── sora.js
│   ├── stroke.js
│   ├── stroke-data.js
│   └── translator.js
│
├── materi/                         # Modul pembelajaran Mirai no Buuku
│   ├── dasar/
│   │   ├── index.html              # Daftar isi Mirai no Buuku Dasar
│   │   ├── hiragana.html           # Panduan Aksara Hiragana (Dasar 10)
│   │   ├── katakana.html           # Panduan Aksara Katakana (Dasar 11)
│   │   └── jikoshokai.html         # Modul Perkenalan Diri (Dasar 01)
│   └── lanjutan/
│       ├── index.html              # Daftar isi Mirai no Buuku Lanjutan
│       ├── kanji.html              # Panduan Aksara Kanji & JLPT (Lanjutan 02)
│       └── grammar.html            # Modul Tata Bahasa Lanjutan (Lanjutan 01)
│
├── sora/                           # Ruang eksplorasi maskot Sora
│   └── index.html
│
├── video/                          # Aset media video
│
├── [HALAMAN UTAMA WEBSITE]
│   ├── index.html                  # Beranda / Homepage utama
│   ├── tentang.html                # Profil, sejarah, dan makna klub
│   ├── kegiatan.html               # Halaman kegiatan (Divisi & Program Kerja)
│   ├── kelas.html                  # Hub kelas belajar (Dasar, Lanjutan, Kurikulum)
│   ├── kamus.html                  # Kamus interaktif Hiragana, Katakana, dan Kanji
│   ├── kanji.html                  # Kamus Kanji lengkap (2.136+ Jōyō Kanji)
│   ├── latihan.html                # Modul latihan kuis Kana interaktif
│   ├── kurikulum.html              # Peta belajar kurikulum
│   ├── kelas-dasar.html            # Ikhtisar materi kelas dasar
│   ├── kelas-lanjutan.html         # Ikhtisar materi kelas lanjutan
│   │
│   ├── [Halaman Divisi]
│   ├── divisi-bahasa.html          # Divisi Bahasa & Budaya
│   ├── divisi-cosplay.html         # Divisi Cosplay & Seni Peran
│   ├── divisi-desain.html          # Divisi Desain & Kreatif
│   ├── divisi-kewirausahaan.html   # Divisi Kewirausahaan
│   │
│   ├── [Halaman Program Kerja]
│   ├── ktn.html                    # 01. Kimi To Nippon (Orientasi)
│   ├── njr.html                    # 02. Nihon Go Rajio (Radio Sekolah)
│   ├── konbini.html                # 03. Mirai no Konbini (Kewirausahaan)
│   ├── ramadhan.html               # 04. Mirai no Ramadhan (Bulan Puasa)
│   │
│   ├── [Halaman Redirect / Kompatibilitas]
│   ├── about.html                  # Pengalihan ke tentang.html
│   ├── hiragana.html               # Pengalihan ke kamus.html?tab=hiragana
│   ├── katakana.html               # Pengalihan ke kamus.html?tab=katakana
│   └── masukan.html                # Pengalihan ke Google Form
│
├── [ASSET INTI GLOBAL]
│   ├── style.css                   # Master stylesheet (termasuk Dark Mode & Sora)
│   └── script.js                   # Master script interaktif global
└── tree.md                         # Dokumentasi struktur direktori ini
```

