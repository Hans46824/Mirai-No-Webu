# Peta Struktur Direktori Proyek — Mirai no Webu
**Website Resmi Klub Bahasa & Kebudayaan Jepang MIRAI NO HANA**  
*SMASYIMDUTA (SMA YPM 2 Sukodono, Sidoarjo)*

Dokumen ini memetakan seluruh susunan folder, file kode, aset visual, dan modul pembelajaran terkini dalam repositori `Mirai-No-Webu`.

---

```text
Mirai-No-Webu/
│
├── 📂 data/                                # Data kamus, metadata aksara, dan lisensi
│   ├── kana.json                           # Data aksara Hiragana & Katakana
│   ├── kanji.json                          # Database lokal karakter Kanji
│   ├── kanji-meta.json                     # Metadata jumlah goresan & grade Kanji
│   └── STROKES-LICENSE.md                  # Lisensi data goresan KanjiVG
│
├── 📂 docs/                                # Dokumen pedoman & kurikulum resmi
│   └── kurikulum/
│       ├── kurikulum-pembelajaran.pdf      # Silabus materi pembelajaran bertingkat
│       ├── tata-cara-mengajar.pdf          # Buku panduan tutor & metode pengajaran
│       └── README.txt                      # Catatan pembaruan berkas kurikulum
│
├── 📂 images/mirai/                        # Sentral aset grafis, foto, dan visual klub
│   ├── anggota/                            # Foto resmi ketua angkatan (Angkatan 1–8)
│   ├── background/                         # Ilustrasi latar belakang (Sora.png)
│   ├── dokumentasi/                        # Foto arsip dokumentasi kegiatan klub
│   ├── icon/                               # Ikon chibi maskot klub (Ay, Fa, Fu, Hu, Ka, Lo, dll.)
│   ├── identitas/                          # Atribut resmi (Haori, ID card, lanyard, nametag, pin)
│   ├── logo/                               # Logo resmi klub (MNH1, NK) & logo program kerja
│   ├── pattern/                            # Motif Wagara Jepang (w1b, w1w, w2w, c1b, c1w)
│   ├── sora/                               # Aset visual chatbot Asora Aokita
│   └── stiker/                             # Foto formal ketua angkatan & stiker klub
│
├── 📂 js/                                  # Modul logika JavaScript (Frontend & Client-side)
│   ├── api.js                              # Client API Kanji & Kana dengan sistem caching
│   ├── carousel.js                         # Handler carousel interaktif
│   ├── kana.js                             # Mesin pencarian, audio, & tabel aksara Kana
│   ├── kanji.js                            # Kamus Kanji lengkap (JLPT N5–N1) & stroke player
│   ├── main.js                             # Logika global (Navigasi sidebar, Back to Top, Lightbox, Reveal)
│   ├── proker-slider.js                    # Slider galeri untuk halaman kegiatan & proker
│   ├── sora.js                             # Modul AI Chatbot Sora & fallback respons lokal
│   ├── stroke.js                           # Mesin render animasi goresan SVG (KanjiVG)
│   ├── stroke-data.js                      # Vektor koordinat goresan stroke Hiragana & Kanji
│   └── translator.js                       # Terjemahan arti definisi Kanji (Inggris ke Indonesia)
│
├── 📂 materi/                              # Modul artikel pembelajaran digital (Mirai no Buuku)
│   ├── dasar/                              # Seri Buuku Kelas Dasar
│   │   ├── index.html                      # Daftar isi materi kelas dasar
│   │   ├── hiragana.html                   # Panduan Aksara Hiragana (Dasar 10)
│   │   ├── katakana.html                   # Panduan Aksara Katakana (Dasar 11)
│   │   └── jikoshokai.html                 # Panduan Perkenalan Diri (Dasar 01)
│   └── lanjutan/                           # Seri Buuku Kelas Lanjutan
│       ├── index.html                      # Daftar isi materi kelas lanjutan
│       ├── kanji.html                      # Panduan Aksara Kanji & JLPT (Lanjutan 02)
│       └── grammar.html                    # Panduan Pola Kalimat & Tata Bahasa (Lanjutan 01)
│
├── 📂 sora/                                # Antarmuka mandiri chatbot maskot
│   └── index.html                          # Kanvas mandiri chatbot Asora Aokita
│
├── 📂 video/                               # Aset media video
│   └── recording_20260822_19-15-48.mp4     # Rekaman dokumentasi klub
│
├── 📂 ai_scripts/                          # Skrip Python utilitas & otomasi pengembang
│
├── 📄 [HALAMAN UTAMA WEBSITE]
│   ├── index.html                          # Beranda utama (Hero, Tentang Card, Jalur Belajar, Kegiatan, Masukan)
│   ├── tentang.html                        # Profil lengkap klub, filosofi, visi-misi, sejarah, haori, & kepengurusan
│   ├── kegiatan.html                       # Hub aktivitas (Struktur 4 Divisi & Galeri 4 Program Kerja)
│   ├── kelas.html                          # Hub ruang belajar (Kelas Dasar, Kelas Lanjutan, & Kurikulum)
│   ├── kelas-dasar.html                    # Silabus & ringkasan materi kelas dasar
│   ├── kelas-lanjutan.html                 # Silabus & ringkasan materi kelas lanjutan
│   ├── kurikulum.html                      # Peta kurikulum pembelajaran & portal unduh dokumen PDF
│   ├── kamus.html                          # Kamus interaktif terpadu (Kanji, Hiragana, Katakana, Live Stroke)
│   └── latihan.html                        # Arena kuis latihan interaktif (KanaQuest)
│
├── 📄 [HALAMAN DIVISI KLUB]
│   ├── divisi-bahasa.html                  # Profil Divisi Bahasa & Kebudayaan Jepang
│   ├── divisi-cosplay.html                 # Profil Divisi Cosplay & Seni Peran
│   ├── divisi-desain.html                  # Profil Divisi Desain Grafis & Kreatif
│   └── divisi-kewirausahaan.html           # Profil Divisi Kewirausahaan
│
├── 📄 [HALAMAN PROGRAM KERJA]
│   ├── ktn.html                            # Proker 01: Kimi To Nippon (Orientasi Anggota Baru)
│   ├── njr.html                            # Proker 02: Nihon Go Rajio (Siaran Radio Jepang Sekolah)
│   ├── konbini.html                        # Proker 03: Mirai no Konbini (Kewirausahaan & Kuliner)
│   └── ramadhan.html                       # Proker 04: Mirai no Ramadhan (Bagi Takjil & Buka Puasa)
│
├── 📄 [HALAMAN PENGALIHAN / REDIRECT STUBS]
│   ├── about.html                          # Pengalihan otomatis (HTTP-Refresh) ke tentang.html
│   ├── hiragana.html                       # Pengalihan otomatis ke kamus.html?tab=hiragana
│   ├── katakana.html                       # Pengalihan otomatis ke kamus.html?tab=katakana
│   ├── kanji.html                          # Halaman cadangan/pengalihan ke kamus.html
│   └── masukan.html                        # Pengalihan langsung ke Google Form aspirasi
│
└── 📄 [BERKAS INTI GLOBAL]
    ├── style.css                           # Master stylesheet desain (Obsidian Dark, Wagara Patterns, Responsif)
    ├── script.js                           # Engine kuis latihan KanaQuest (latihan.html)
    └── tree.md                             # Dokumentasi peta struktur proyek (berkas ini)
```

---

## 📌 Ringkasan Pembaruan Terakhir

1. **Penghapusan Folder `archive/`:**  
   Folder `archive/` yang berisi draf uji coba lawas (`advance.html`, `reguler.html`, `test-card.html`, dan proker arsip) telah dihapus permanen dari proyek karena seluruh fiturnya sudah digantikan oleh halaman rilis resmi dan tidak terhubung lagi dengan navigasi situs aktif.
2. **Pembaruan Peta Aset `images/mirai/`:**  
   Struktur subdirektori diselaraskan dengan isi aktual repositori (`anggota/`, `background/`, `dokumentasi/`, `icon/`, `identitas/`, `logo/`, `pattern/`, `sora/`, `stiker/`).
3. **Pengelompokan Halaman Web:**  
   Pemisahan kategori secara sistematis antara Halaman Utama, Halaman Divisi, Program Kerja, Materi Pembelajaran (*Mirai no Buuku*), dan Halaman Pengalihan (*Redirect*).
