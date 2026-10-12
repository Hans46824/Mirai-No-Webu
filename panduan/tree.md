# Struktur Direktori Proyek Mirai no Webu

Dokumen ini memetakan seluruh susunan berkas, folder, halaman web, aset gambar, basis data, dan logika skrip yang aktif di website **Mirai no Webu**.
Struktur direktori menerapkan standar **Feature-Based Asset Colocation** dan **Clean Root Architecture**, di mana berkas/foto yang spesifik berkaitan dengan halaman tertentu berada di dalam folder halaman tersebut:

```text
Mirai-No-Webu/
├── index.html                      # Gerbang utama website (Beranda)
├── 404.html                        # Halaman penanganan tautan salah / tidak ditemukan
├── README.md                       # Profil utama repositori & dokumentasi Sources & Credits
│
├── css/                            # Master Stylesheet (Gaya & Desain Antarmuka)
│   └── style.css                   # Master CSS (Tema gelap, terang, kartu wagara, tipografi, & komponen)
│
├── js/                             # Logika JavaScript Modular
│   ├── main.js                     # Logika navbar, sidebar mobile, launcher Sora, dan tema
│   ├── script.js                   # Master interaksi kuis, kartu, & efek interaktif global
│   ├── leaderboard-data.js         # Master data profil peringkat & prestasi
│   ├── sora.js                     # Logika bot obrolan & fallback jawaban cerdas Sora
│   ├── kanji.js                    # Mesin pencari & filter ensiklopedia Kanji
│   ├── kana.js                     # Logika audio pelafalan & kartu Kana
│   ├── stroke.js                   # Animasi kanvas urutan goresan Yoon & kanji
│   ├── stroke-data.js              # Vektor koordinat garis KanjiVG terkurasi
│   ├── carousel.js                 # Logika slider / carousel umum
│   ├── proker-slider.js            # Slider khusus halaman kegiatan & proker
│   ├── translator.js               # Mesin bantu terjemahan
│   └── api.js                      # Koneksi endpoint data
│
├── panduan/                        # Dokumentasi & Panduan Proyek
│   ├── tree.md                     # Peta struktur direktori lengkap proyek ini
│   └── agent.md                    # Pedoman aturan desain, fungsi, dan persona AI asisten
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
│       └── identitas/              # Foto Haori resmi, kartu tanda anggota (IDC), lanyard, & pin
│
├── lomba/                          # Halaman Informasi Kompetisi & Matsuri
│   ├── index.html                  # Informasi 18 lomba & festival jejepangan
│   └── images/                     # Poster resmi lomba (ITS, UNAIR, UNESA)
│       ├── its1.jpeg
│       ├── its2.jpeg
│       ├── una.jpeg
│       ├── une1.jpeg
│       └── une2.jpeg
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
├── kelas/                          # Halaman Modul & Pembelajaran Mandiri
│   ├── index.html                  # Hub utama Kelas (Pilihan level, modul, kurikulum, latihan)
│   ├── dasar.html                  # Modul Kelas Dasar (Hiragana & Katakana)
│   ├── lanjutan.html               # Modul Kelas Lanjutan (Kanji & Tata Bahasa)
│   ├── kurikulum.html              # Peta belajar kurikulum terstruktur & panduan mengajar
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
├── skrip/                          # Kumpulan Skrip Otomasi Pemeliharaan Kode (.py)
│   └── README.md                   # Panduan & daftar fungsi skrip otomasi pengembang
│
└── images/mirai/                   # Aset Bersama (Shared Global Assets)
    ├── background/                 # Pola Wagara master CSS (w1b, w1w, c1b, c1w, Sora.png, chat.jpeg)
    ├── logo/                       # Logo resmi klub (MNH1.png, MNH1-nav.png, NK.png, comingsoon.jpg)
    ├── icon/                       # Ikon chibi Genshin Impact (Al, Ay, Chi, Fa, Fu, Hu, Ka, Ki, Lo, dll.)
    └── stiker/                     # 28 stiker komunitas ekspresi karakter anime
```
