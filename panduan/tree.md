# Struktur Direktori Proyek Mirai no Webu

Dokumen ini memetakan seluruh susunan berkas, folder, modul stylesheet, halaman web, aset gambar, basis data, dan logika skrip yang aktif di website **Mirai no Webu**.
Struktur direktori menerapkan standar **Feature-Based Asset Colocation**, **Modular CSS Architecture**, dan **Clean Root Standard**:

```text
Mirai-No-Webu/
├── index.html                      # Gerbang utama website (Beranda)
├── 404.html                        # Halaman penanganan tautan salah / tidak ditemukan bertema Sora
├── README.md                       # Profil utama repositori & dokumentasi Sources & Credits
├── cspell.json                     # Konfigurasi Code Spell Checker (kamus & ignorasi kata bilingual)
├── .vscode/                        # Konfigurasi workspace editor VS Code / Antigravity
│   └── settings.json               # Pengaturan workspace, search.exclude, & files.watcherExclude
│
├── css/                            # Master & Arsitektur Stylesheet Berbasis Halaman
│   ├── style.css                   # Master CSS Index (Memanggil @import Google Fonts & 11 file css/pages/)
│   └── pages/                      # Sub-folder stylesheet 100% intuitif per-halaman web
│       ├── global.css              # Variabel :root, reset, sistem background selang-seling, tombol dasar, dark mode, 404, animasi
│       ├── navbar-hero-footer.css  # Floating navbar, off-canvas sidebar nav, hero banners, hero guardrail, & footer
│       ├── beranda.css             # Apa itu web, start-grid, aktivitas beranda (2 kartu besar), masukan & saran, quote slider
│       ├── kelas-materi.css        # Alur kelas, kelas dasar (#dasar), kelas lanjutan (#lanjutan), buuku lesson, kurikulum, kuis latihan
│       ├── kamus.css               # Kamus kana & kanji, stage goresan KanjiVG, kanvas Yoon, quick stroke button
│       ├── kegiatan-divisi.css     # Hub kegiatan, 5 halaman proker, 4 divisi resmi, fasilitas klub (format landscape), slider galeri
│       ├── tentang.css             # Profil klub, bendera, logo, slogan, visi misi, timeline angkatan 1-8, Sora RPG, prestasi, haori, FAQ
│       ├── rekomendasi-motivasi.css # Kata motivasi anime (3 box), rekomendasi pop culture, & media legal
│       ├── peringkat.css           # Multi-leaderboard keaktifan rajio, presensi kehadiran, podium rank 1-3, tabel skor, modal riwayat
│       ├── lomba.css               # Papan info lomba/acara, kartu event bertumpuk vertikal, poster carousel kiri-kanan, modal juknis
│       └── toko.css                # Etalase atribut & F&B konbini, Shopee-style 185px, poster carousel Haori/KTA, drawer keranjang
│
├── js/                             # Logika JavaScript Modular
│   ├── main.js                     # Logika navbar, sidebar mobile, launcher Sora, dan tema
│   ├── script.js                   # Master interaksi kuis, kartu, & efek interaktif global
│   ├── leaderboard-data.js         # Master data profil peringkat & prestasi
│   ├── sora.js                     # Logika bot obrolan & fallback jawaban cerdas Sora
│   ├── kanji.js                    # Mesin pencari & filter ensiklopedia Kanji
│   ├── kana.js                     # Logika audio pelafalan & kartu Kana
│   ├── stroke.js                   # Animasi kanvas urutan goresan Yoon & kanji
│   ├── stroke-data.js              # Vektor koordinat garis KanjiVG terkurasi (dikecualikan dari watcher)
│   ├── carousel.js                 # Logika slider / carousel umum
│   ├── proker-slider.js            # Slider khusus halaman kegiatan & proker
│   ├── translator.js               # Mesin bantu terjemahan
│   └── api.js                      # Koneksi endpoint data
│
├── panduan/                        # Dokumentasi & Panduan Proyek
│   ├── PANDUAN-DEVELOPER.md        # Buku panduan serah-terima pengurus & developer klub
│   ├── CONTEKAN-TAG.md             # Acuan cepat pemetaan halaman -> CSS -> JS (Otak Otomatis)
│   ├── tree.md                     # Peta struktur direktori lengkap proyek ini
│   ├── agent.md                    # Pedoman aturan desain, protokol eksekusi cepat, dan persona AI
│   └── ai-configs/                 # Konfigurasi AI Assistant (Clean Root Standard)
│       ├── .cursorrules            # Aturan otomatis untuk Cursor AI
│       ├── copilot-instructions.md # Instruksi otomatis untuk GitHub Copilot
│       └── README.md               # Panduan penggunaan AI rules di berbagai editor
│
├── data/                           # Basis Data Lokal JSON (Menyuplai Kamus & Latihan)
│   ├── README.md                   # Dokumentasi relasi & fungsi basis data JSON
│   ├── kana.json                   # Database aksara Hiragana & Katakana
│   ├── kanji.json                  # Database lengkap 2.136 karakter Jōyō Kanji
│   ├── kanji-meta.json             # Metadata radikal, level JLPT, & jumlah goresan
│   └── STROKES-LICENSE.md          # Lisensi data urutan goresan KanjiVG
│
├── tentang/                        # Halaman Profil Lengkap Klub Mirai No Hana
│   ├── index.html                  # Sejarah klub, filosofi bunga, bendera, Haori, dan 11 profil pengurus
│   └── images/                     # Aset foto spesifik halaman Tentang
│       ├── anggota/                # Dokumentasi foto anggota kepengurusan (1.jpg - 8.jpg)
│       └── identitas/              # Foto Haori resmi (depan/belakang), IDC, lanyard, nametag, & pin
│
├── lomba/                          # Halaman Informasi Kompetisi & Matsuri
│   ├── index.html                  # Informasi 18 lomba & festival jejepangan
│   └── images/                     # Poster resmi lomba (ITS 1 & 2, UNAIR, UNESA 1 & 2)
│
├── kegiatan/                       # Halaman Program Kerja Unggulan & Fasilitas
│   ├── index.html                  # Hub Program & Fasilitas (4 Divisi, 5 Proker, Fasilitas, & Galeri Foto)
│   ├── kimi-to-nippon.html         # 1. Kimi To Nippon (Orientasi anggota baru klub)
│   ├── nihon-go-rajio.html         # 2. Nihon Go Rajio (Siaran radio mingguan sekolah)
│   ├── konbini.html                # 3. Mirai no Konbini (Bazaar & merchandise kreatif)
│   ├── ramadhan.html               # 4. Mirai no Ramadhan (Bakti sosial & takjil puasa)
│   ├── tomodachi.html              # 5. Tomodachi (Forum jejaring & perkenalan anggota)
│   └── images/                     # Aset spesifik program kerja & dokumentasi
│       ├── KTN.png                 # Logo Kimi To Nippon
│       ├── NGR.png                 # Logo Nihon Go Rajio
│       ├── Mirainokonbini.png       # Logo Mirai no Konbini
│       ├── Ramadhan.jpeg           # Logo Mirai no Ramadhan
│       ├── Miraimatsuri.png        # Logo Miraimatsuri
│       └── dokumentasi/            # Foto dokumentasi kegiatan landscape & portrait
│
├── toko/                           # Toko Resmi & Mirai no Konbini (Atribut, Cinderamata, & F&B)
│   └── index.html                  # Etalase produk Haori, merchandise, F&B konbini, keranjang, & GForm
│
├── kelas/                          # Halaman Modul Kelas & Kurikulum Pembelajaran Mandiri
│   ├── index.html                  # Hub utama terpadu (Kelas Dasar, Kelas Lanjutan, & Kurikulum Dokumen)
│   ├── latihan.html                # Kuis interaktif mandiri aksara Kana (20 soal & goresan kanvas)
│   ├── motivasi.html               # Kumpulan kata motivasi & mutiara bahasa Jepang
│   └── kurikulum/                  # Dokumen kurikulum & tata cara pengajaran (PDF)
│       ├── kurikulum-pembelajaran.pdf
│       ├── tata-cara-mengajar.pdf
│       └── README.txt
│
├── divisi/                         # Halaman 4 Divisi Resmi Klub
│   ├── index.html                  # Hub ringkasan struktur 4 divisi resmi
│   ├── bahasa.html                 # Divisi Bahasa & Budaya
│   ├── cosplay.html                # Divisi Cosplay & Seni Peran
│   ├── desain.html                 # Divisi Desain & Kreatif
│   └── kewirausahaan.html          # Divisi Kewirausahaan
│
├── kamus/                          # Kamus Interaktif & Ensiklopedia Aksara
│   ├── index.html                  # Kamus interaktif Kana (Hiragana & Katakana) serta pencarian Kanji
│   └── kanji.html                  # Ensiklopedia lengkap 2.136+ karakter Jōyō Kanji
│
├── peringkat/                      # Papan Peringkat (Leaderboard)
│   └── index.html                  # Leaderboard keaktifan Rajio, presensi kehadiran, & galeri prestasi siswa
│
├── rekomendasi/                    # Rekomendasi Media Belajar Budaya Jepang
│   └── index.html                  # Rekomendasi anime, film layar lebar, musik, dan konten kebudayaan
│
├── sora/                           # Ruang Asisten Obrolan Maskot Sora
│   ├── index.html                  # Halaman antarmuka obrolan interaktif Sora
│   └── images/                     # Aset khusus maskot Sora (soracarousel.png, sorachat.jpeg)
│
├── materi/                         # Buku Modul Pembelajaran Detail (Mirai no Buuku)
│   ├── dasar/
│   │   ├── index.html              # Daftar isi modul dasar
│   │   ├── hiragana.html           # Modul lengkap aksara Hiragana
│   │   ├── katakana.html           # Modul lengkap aksara Katakana
│   │   └── jikoshokai.html         # Modul perkenalan diri (Jikoshoukai)
│   └── lanjutan/
│       ├── index.html              # Daftar isi modul lanjutan
│       ├── kanji.html              # Panduan aksara Kanji & JLPT
│       └── grammar.html            # Panduan tata bahasa (Bunpou) lanjutan
│
├── skrip/                          # Pemeliharaan Kode Python
│   ├── README.md                   # Panduan skrip pengembang
│   └── arsip/                      # Arsip skrip perbaikan sekali-pakai (dikecualikan dari watcher)
│       ├── apply_card_expand.py
│
└── images/mirai/                   # Aset Bersama (Shared Global Assets)
    ├── background/                 # Pola Wagara master CSS (w1b, w1w, c1b, c1w, w2w, chat, Sora)
    ├── logo/                       # Logo resmi klub (MNH1.png, MNH1-nav.png, NK.png, comingsoon.jpg)
    ├── icon/                       # Ikon chibi Genshin Impact (Al, Ay, Chi, Fa, Fu, Hu, Ka, Ki, Lo, dll.)
    ├── karakter/                   # Foto karakter anime kutipan (luf, ere, nar, dek, tan)
    ├── produk/                     # Foto produk konbini (oni, tak, dan, mat, teh)
    └── stiker/                     # 28 stiker komunitas ekspresi karakter anime
```
