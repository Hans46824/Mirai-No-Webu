# Struktur Direktori Proyek Mirai no Webu

Dokumen ini memetakan seluruh susunan file, folder, halaman web, aset gambar, data, dan logika skrip yang aktif di website **Mirai no Webu**.

```text
Mirai-No-Webu/
├── agent.md                        # Pedoman aturan desain, fungsi, dan persona AI
├── tree.md                         # Peta lengkap struktur direktori proyek ini
├── style.css                       # Master stylesheet CSS (Tema gelap, terang, & komponen)
├── script.js                       # Master JavaScript interaktif global
│
├── [HALAMAN UTAMA WEBSITE]
│   ├── index.html                  # Beranda utama (Hero, modul, maskot Sora, feedback)
│   ├── tentang.html                # Profil klub (Sejarah, filosofi, bendera, Haori, 11 pengurus)
│   ├── kegiatan.html               # Hub Program & Fasilitas (4 Divisi, 5 Program Kerja, & Fasilitas Sekolah/Web)
│   ├── kelas.html                  # Hub kelas belajar (Kelas Dasar, Lanjutan, Kurikulum)
│   ├── kelas-dasar.html            # Modul Kelas Dasar (Hiragana & Katakana)
│   ├── kelas-lanjutan.html         # Modul Kelas Lanjutan (Kanji & Tata Bahasa)
│   ├── kurikulum.html              # Peta belajar kurikulum terstruktur
│   ├── latihan.html                # Kuis interaktif aksara Kana (Hiragana & Katakana)
│   ├── kamus.html                  # Kamus interaktif pencarian Kana & Kanji
│   ├── kanji.html                  # Ensiklopedia lengkap 2.136+ Jōyō Kanji
│   ├── peringkat.html              # Papan peringkat (Leaderboard Rajio, Kehadiran, Prestasi)
│   ├── lomba.html                  # Informasi 18 lomba & festival jejepangan (Carousel poster 1-view & link kegiatan)
│   ├── motivasi.html               # Kumpulan kata motivasi & mutiara bahasa Jepang
│   ├── rekomendasi.html            # Rekomendasi media belajar (Anime, musik, dorama)
│   ├── tomodachi.html              # Forum perkenalan & jejaring teman belajar
│   ├── masukan.html                # Halaman aspirasi & form kritik saran
│   │
│   ├── [Halaman 4 Divisi Resmi]
│   ├── divisi-bahasa.html          # Divisi Bahasa & Budaya
│   ├── divisi-cosplay.html         # Divisi Cosplay & Seni Peran
│   ├── divisi-desain.html          # Divisi Desain & Kreatif
│   ├── divisi-kewirausahaan.html   # Divisi Kewirausahaan
│   │
│   ├── [Halaman 4 Program Kerja Unggulan]
│   ├── ktn.html                    # 1. Kimi To Nippon (Orientasi anggota baru)
│   ├── njr.html                    # 2. Nihon Go Rajio (Siaran radio mingguan sekolah)
│   ├── konbini.html                # 3. Mirai no Konbini (Bazaar & merchandise klub)
│   ├── ramadhan.html               # 4. Mirai no Ramadhan (Bakti sosial & matsuri puasa)
│   │
│   ├── [Halaman Pengalihan / Redirect]
│   ├── about.html                  # Pengalihan ke tentang.html
│   ├── hiragana.html               # Pengalihan ke kamus.html?tab=hiragana
│   └── katakana.html               # Pengalihan ke kamus.html?tab=katakana
│
├── sora/                           # Ruang obrolan interaktif maskot Sora
│   └── index.html                  # Halaman playground chat Sora
│
├── materi/                         # Buku modul pembelajaran terperinci
│   ├── dasar/
│   │   ├── index.html              # Daftar isi materi dasar
│   │   ├── hiragana.html           # Modul lengkap aksara Hiragana
│   │   ├── katakana.html           # Modul lengkap aksara Katakana
│   │   └── jikoshokai.html         # Modul perkenalan diri (Jikoshoukai)
│   └── lanjutan/
│       ├── index.html              # Daftar isi materi lanjutan
│       ├── kanji.html              # Panduan aksara Kanji & JLPT
│       └── grammar.html            # Panduan tata bahasa (Bunpou) lanjutan
│
├── data/                           # Database JSON aksara & kamus
│   ├── kana.json                   # Data huruf Hiragana & Katakana
│   ├── kanji.json                  # Data 2.136 karakter Kanji
│   ├── kanji-meta.json             # Metadata radikal & urutan goresan
│   └── STROKES-LICENSE.md          # Lisensi data urutan goresan KanjiVG
│
├── js/                             # File logika JavaScript modular
│   ├── main.js                     # Logika navbar, sidebar mobile, tema, & launcher Sora
│   ├── leaderboard-data.js         # Master data 30 profil peringkat & prestasi
│   ├── sora.js                     # Logika bot obrolan & fallback jawaban Sora
│   ├── kanji.js                    # Mesin pencari & filter kamus Kanji
│   ├── kana.js                     # Logika kartu & audio pelafalan Kana
│   ├── stroke.js                   # Visualisasi urutan goresan kanvas Kanji & Kana (Animasi Yoon proporsional)
│   ├── stroke-data.js              # Vektor koordinat garis KanjiVG
│   ├── carousel.js                 # Logika slider / carousel umum
│   ├── proker-slider.js            # Slider khusus halaman kegiatan proker
│   ├── translator.js               # Mesin bantu terjemahan
│   └── api.js                      # Koneksi endpoint data
│
├── images/mirai/                   # Seluruh aset visual klub
│   ├── background/                 # Pola wagara & wallpaper latar
│   │   ├── c1b.jpeg                # Pola awan kumo gelap (kartu menu ganjil: Beranda, Kamus, Rekomendasi, Lomba)
│   │   ├── c1w.jpeg                # Pola awan kumo terang (kartu menu ganjil: Beranda, Kamus, Rekomendasi, Lomba)
│   │   ├── w1b.jpeg                # Pola ombak wagara gelap (kartu menu genap: Kelas, Kegiatan, Peringkat, Tentang)
│   │   ├── w1w.jpeg                # Pola ombak wagara terang (kartu menu genap: Kelas, Kegiatan, Peringkat, Tentang)
│   │   ├── w2w.jpeg                # Pola tekstil wagara terang cadangan
│   │   ├── chat.jpeg               # Wallpaper latar ruang obrolan
│   │   └── Sora.png                # Artwork gambar maskot Sora
│   │
│   ├── logo/                       # Logo resmi klub & program kerja
│   │   ├── MNH1.png                # Logo utama Mirai No Hana
│   │   ├── MNH1-nav.png            # Logo Mirai No Hana versi navbar
│   │   ├── NK.png                  # Logo Nihongo Kurabu
│   │   ├── NGR.png                 # Logo Nihon Go Rajio
│   │   ├── KTN.png                 # Logo Kimi To Nippon
│   │   ├── Mirainokonbini.png       # Logo Mirai no Konbini
│   │   ├── Miraimatsuri.png        # Logo Miraimatsuri
│   │   ├── Ramadhan.jpeg           # Logo Mirai no Ramadhan
│   │   └── comingsoon.jpg          # Placeholder acara mendatang
│   │
│   ├── icon/                       # Ikon chibi Genshin & simbol
│   │   ├── Al.png                  # Chibi Alhaitham (PNG transparan)
│   │   ├── Ay.png                  # Chibi Kamisato Ayato (PNG transparan)
│   │   ├── Chi.png                 # Chibi Tartaglia Childe (PNG transparan)
│   │   ├── Fa.png                  # Chibi Faruzan (PNG transparan)
│   │   ├── Fli.png                 # Chibi Fischl (PNG transparan)
│   │   ├── Fu.png                  # Chibi Furina (PNG transparan)
│   │   ├── Hu.png                  # Chibi Hu Tao (PNG transparan)
│   │   ├── Ka.png                  # Chibi Kaedehara Kazuha (PNG transparan)
│   │   ├── Ki.png                  # Chibi Kirara (PNG transparan)
│   │   ├── Lo.png                  # Chibi Layla (PNG transparan)
│   │   ├── Wa.png                  # Chibi Wanderer Scaramouche (PNG transparan)
│   │   ├── ang.jpeg                # Chibi Venti
│   │   ├── bal.jpeg                # Chibi Raiden Shogun Ei
│   │   ├── bul.jpeg                # Chibi Columbina
│   │   ├── chi.jpeg                # Chibi Yanfei
│   │   ├── cil.jpeg                # Chibi Xiao
│   │   ├── dil.jpeg                # Chibi Diluc
│   │   ├── nah.jpeg                # Chibi Nahida
│   │   ├── sar.jpeg                # Chibi Kujou Sara
│   │   ├── zho.jpeg                # Chibi Zhongli
│   │   └── chat.jpeg               # Ikon balon obrolan
│   │
│   ├── identitas/                  # Aset atribut resmi & merchandise klub
│   │   ├── haori-depan-new.png     # Tampak depan Haori resmi klub
│   │   ├── haori-belakang-new.png  # Tampak belakang Haori resmi klub
│   │   ├── happi.jpeg              # Foto jubah festival Happi
│   │   ├── idc front.jpeg          # Desain depan kartu tanda anggota (ID Card)
│   │   ├── idc back.jpeg           # Desain belakang kartu tanda anggota
│   │   ├── lanyard.jpeg            # Foto tali lanyard klub
│   │   ├── lanyard-horizontal.png  # Mockup lanyard horizontal
│   │   ├── lanyard-horizontal-ccw.png # Mockup lanyard rotasi
│   │   ├── nametag-katakana.jpeg   # Tanda pengenal bertuliskan Katakana
│   │   ├── pin.jpeg                # Foto pin lencana klub
│   │   └── pin-clean.png           # Render transparan pin lencana
│   │
│   ├── Lomba & Acara/              # Poster resmi kompetisi & matsuri
│   │   ├── its1.jpeg               # Poster INOCHI ITS (Akademik)
│   │   ├── its2.jpeg               # Poster INOCHI ITS (Kreatif & Cosplay)
│   │   ├── una.jpeg                # Poster JWC UNAIR
│   │   ├── une1.jpeg               # Poster JPC UNESA (Lomba Umum)
│   │   └── une2.jpeg               # Poster JPC UNESA (Lomba Akademik)
│   │
│   ├── sora/                       # Aset khusus maskot Sora
│   │   ├── soracarousel.png        # Banner showcase maskot Sora
│   │   └── sorachat.jpeg           # Avatar maskot di kotak obrolan
│   │
│   ├── stiker/                     # 28 stiker komunitas (ada, aku, ala, be, dst.)
│   ├── anggota/                    # 8 foto dokumentasi anggota (1.jpg s.d. 8.jpg)
│   └── dokumentasi/                # path_to_landscape.jpg & path_to_portrait.jpg
│
├── ai_scripts/                     # Koleksi skrip otomasi & pemeliharaan kode (.py)
├── docs/                           # Dokumentasi pendukung proyek
└── video/                          # Aset berkas video kegiatan
```
