# 🌸 MIRAI NO WEBU (未来のウェブ)

> **Website Resmi & Platform Edukasi Terpadu Klub Bahasa & Kebudayaan Jepang MIRAI NO HANA**  
> SMA Wachid Hasyim 2 (SMASYIMDUTA) Taman, Sidoarjo, Jawa Timur.

[![Status](https://img.shields.io/badge/Status-Aktif-success.svg)](#)
[![Tampilan](https://img.shields.io/badge/Desain-Clean%20Root%20%7C%20Motion%20Engine-e91e63.svg)](#)
[![Hosting](https://img.shields.io/badge/Hosting-GitHub%20Pages-181717.svg)](#)
[![Bahasa](https://img.shields.io/badge/Bahasa-Indonesia%20%7C%20%E6%97%A5%E6%9C%AC%E8%AA%9E-blue.svg)](#)

---

## 📌 Tentang Proyek

**Mirai no Webu** adalah portal pembelajaran dan informasi terpadu yang dirancang dan dikembangkan secara mandiri oleh kepengurusan **Klub Jepang MIRAI NO HANA**. Website ini menjadi sarana belajar bahasa Jepang interaktif, dokumentasi kegiatan, katalog prestasi, informasi matsuri/lomba, serta pusat komunikasi bagi seluruh anggota klub dan siswa pecinta budaya Jepang.

---

## ✨ Fitur Unggulan

1. **⛩️ Gerbang Utama (Beranda)**
   * Showcase kegiatan unggulan, filosofi klub, kutipan inspiratif, dan peluncur asisten interaktif Sora.
2. **📖 Modul Pembelajaran Terpadu (`kelas/`)**
   * **Kelas Dasar**: Pengenalan aksara Hiragana & Katakana beserta latihan audio pelafalan.
   * **Kelas Lanjutan**: Kosakata tematik, tata bahasa, partikel, pola kalimat, dan budaya kerja Jepang.
   * **Latihan Mandiri Interaktif**: Bank soal 20 kuis acak mencakup pilihan ganda, tebak kosakata, pasangan kata, dan **Tantangan Menulis Goresan Kana Ala Duolingo (Stroke Tracing)** dengan panduan garis berpresisi tinggi.
   * **Kurikulum & Silabus**: Silabus resmi terstruktur per semester dalam format digital dan unduhan PDF.
3. **🔍 Kamus Interaktif & Ensiklopedia Kanji (`kamus/`)**
   * Pencarian cepat ribuan kosakata Kana dan karakter Jōyō Kanji.
   * Visualisasi animasi urutan goresan (*stroke order animation*) interaktif berbasis data vektor KanjiVG.
   * Detail radikal, jumlah goresan, level JLPT (N5 - N1), bacaan On'yomi & Kun'yomi, serta contoh kalimat aplikatif.
4. **🎏 Program Kerja & Fasilitas (`kegiatan/`)**
   * Dokumentasi dan portal pendaftaran 5 Program Kerja Utama:
     * *Kimi to Nippon (KTN)* — Orientasi dan penyambutan anggota baru.
     * *Nihon Go Rajio (NJR)* — Siaran radio sekolah bertema Jepang.
     * *Mirai no Konbini* — Bazaar merchandise kreatif & kewirausahaan.
     * *Mirai no Ramadhan* — Bakti sosial & festival berbagi takjil ramadhan.
     * *Tomodachi* — Forum jejaring, diskusi, & malam keakraban.
   * Galeri fasilitas: Haori resmi, Happi, pin identitas, perpustakaan komik/modul, dan inventaris klub.
5. **🏆 Papan Peringkat & Galeri Prestasi (`peringkat/`)**
   * Rekapitulasi poin keaktifan anggota, presensi kegiatan, podium 3 besar, dan etalase piala kejuaraan.
6. **🎌 Kalender Lomba & Matsuri (`lomba/`)**
   * Papan informasi resmi seputar 18 kompetisi jejepangan dan festival budaya di tingkat Jawa Timur dan Nasional (ITS, UNAIR, UNESA, dll.).
7. **🤖 Asisten Virtual Sora (`sora/` & Floating Chat)**
   * Chatbot maskot klub *Asora Aokita* dengan respon ramah, ceria, sistem pencarian materi cerdas, dan generator stiker ekspresi.
8. **💫 Sistem Motion & Animasi Masuk (Native Motion Engine)**
   * **View Transitions API (W3C)**: Transisi halaman tanpa jeda putih (*cross-document smooth fade*).
   * **Page Entrance Motion**: Efek kemunculan halaman dan komponen secara mengalir (*cascading reveal*).
   * **Scroll Motion Reveal**: Animasi halus saat kartu dan seksi memasuki layar menggunakan native `IntersectionObserver`.
   * **Aksesibilitas Tinggi**: Menghormati pengaturan pengguna via `@media (prefers-reduced-motion: reduce)`.

---

## 📂 Struktur Direktori (Clean Root Standard)

```text
Mirai-No-Webu/
├── index.html              # Gerbang utama website (Beranda)
├── 404.html                # Halaman penanganan tautan salah / tidak ditemukan
├── README.md               # Dokumentasi utama repositori & kredit
│
├── css/                    # Master stylesheet (Gaya antarmuka & motion)
│   └── style.css           # Desain hitam-putih obsidian wagara, responsif & animasi
│
├── js/                     # Logika modular JavaScript (Vanilla JS)
│   ├── main.js             # Navigasi, sidebar mobile, reveal scroll, & inisialisasi
│   ├── script.js           # Mesin interaksi kartu wagara & animasi global
│   ├── kanji.js            # Mesin pencari ensiklopedia Kanji
│   ├── kana.js             # Logika kartu alfabet Kana & pelafalan audio
│   ├── stroke.js           # Mesin animasi urutan goresan kanji & yoon
│   ├── stroke-data.js      # Basis data vektor koordinat KanjiVG terkurasi
│   └── sora.js             # Logika respon offline maskot Sora
│
├── kelas/                  # Modul pembelajaran & latihan mandiri
│   ├── index.html          # Hub kelas
│   ├── dasar.html          # Kelas dasar
│   ├── lanjutan.html       # Kelas lanjutan
│   ├── kurikulum.html      # Silabus kurikulum
│   ├── latihan.html        # Latihan mandiri 20 soal acak & stroke tracing
│   └── motivasi.html       # Artikel motivasi belajar
│
├── kamus/                  # Kamus kosakata & ensiklopedia kanji
│   ├── index.html          # Kamus interaktif
│   └── kanji.html          # Detail karakter kanji
│
├── kegiatan/               # Program kerja & fasilitas
│   ├── index.html          # Hub proker & galeri fasilitas
│   ├── kimi-to-nippon.html # Proker 1: KTN
│   ├── nihon-go-rajio.html # Proker 2: NJR
│   ├── konbini.html        # Proker 3: Mirai no Konbini
│   ├── ramadhan.html       # Proker 4: Mirai no Ramadhan
│   └── tomodachi.html      # Proker 5: Tomodachi
│
├── tentang/                # Profil lengkap klub & kepengurusan
│   ├── index.html          # Sejarah, filosofi, bendera, Haori, & 11 pengurus
│   └── images/             # Dokumentasi foto anggota & busana identitas
│
├── divisi/                 # Struktur 4 divisi resmi klub
├── lomba/                  # Informasi matsuri & kompetisi (dengan poster lomba)
├── peringkat/              # Papan peringkat poin keaktifan & piala lomba
├── rekomendasi/            # Rekomendasi media belajar anime, film, & musik
├── data/                   # Basis data JSON lokal (kana.json, kanji.json, kanji-meta.json)
├── docs/                   # Pedoman kerja (agent.md, tree.md) & silabus PDF
├── skrip/                  # Skrip pemeliharaan kode & otomasi Python
└── images/                 # Aset grafis global (logo, pola wagara, stiker chibi)
```

---

## 📜 Sumber Daya, API, & Kredit (Sources & Credits)

Sebagai wujud integritas keterbukaan dan penghargaan hak cipta, seluruh sumber daya, pustaka, dan aset yang digunakan di website ini didokumentasikan secara transparan:

| Komponen | Sumber / Penyedia | Lisensi / Keterangan | Fungsi di Website |
| :--- | :--- | :--- | :--- |
| **Data Goresan Huruf** | [KanjiVG Project](https://kanjivg.tagaini.net) | [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/) | Vektor koordinat langkah goresan Kanji, Hiragana, Katakana, dan kombinasi Yoon pada fitur Kamus dan Latihan Menulis. |
| **Tipografi Jepang** | [Noto Sans JP](https://fonts.google.com/specimen/Noto+Sans+JP) (Google Fonts) | SIL Open Font License 1.1 | Tipografi utama karakter kanji, hiragana, dan katakana. |
| **Tipografi Latin** | [Plus Jakarta Sans](https://fonts.google.com/specimen/Plus+Jakarta+Sans) & [Nunito](https://fonts.google.com/specimen/Nunito) | SIL Open Font License 1.1 | Tipografi antarmuka teks bahasa Indonesia dan Romaji. |
| **Tipografi Aksen** | [M PLUS Rounded 1c](https://fonts.google.com/specimen/M+PLUS+Rounded+1c) | SIL Open Font License 1.1 | Tipografi badge angka, romaji kana, dan judul playful. |
| **Ikon Antarmuka** | [Font Awesome 6](https://fontawesome.com) | CC BY 4.0 / SIL OFL | Ikon navigasi, media sosial, dan penunjuk status. |
| **Mesin Gerak (Motion Engine)** | Native CSS3 & W3C View Transitions API | Standar Web Native (Zero-Dependency) | Animasi masuk halaman, efek cascade komponen hero, dan scroll-reveal. |
| **Observer Gulir** | Native JavaScript `IntersectionObserver` | Standar Web Browser | Pemicu kemunculan kartu otomatis saat memasuki layar tanpa beban library luar. |
| **Markdown Parser** | [Marked.js](https://marked.js.org) | MIT License | Pengurai sintaks markdown pada obrolan asisten Sora. |
| **Sanitasi HTML** | [DOMPurify](https://github.com/cure53/DOMPurify) | Apache-2.0 / MPL-2.0 | Pengaman pencegah celah injeksi XSS pada obrolan Sora. |
| **Aset Ilustrasi & Foto** | Dokumentasi Internal Klub & Komunitas Jepang | Fair Use / Edukasi Non-Komersial | Foto kegiatan, desain Haori, stiker maskot Sora, dan poster lomba. |

---

## 🚀 Menjalankan Website secara Lokal

Karena website ini berarsitektur murni **Static Web Application (HTML, CSS, Vanilla JS)**, Anda dapat menjalankannya dengan mudah tanpa perlu instalasi `npm` atau kompilasi rumit:

### Opsi 1: Menggunakan Python (Direkomendasikan)
Buka terminal di dalam folder proyek, lalu jalankan:
```bash
python3 -m http.server 8000
```
Buka peramban (browser) dan akses: `http://localhost:8000`

### Opsi 2: Menggunakan Ekstensi VS Code
1. Pasang ekstensi **Live Server** di Visual Studio Code.
2. Klik kanan pada berkas `index.html` dan pilih **Open with Live Server**.

---

## 🌸 Kontak & Media Sosial

* **Instagram Resmi**: [@mirainohana_smawh2](https://www.instagram.com/mirainohana_smawh2?utm_source=ig_web_button_share_sheet&stkn=ZDNlZDc0MzIxNw==)
* **Organisasi**: Ekstrakurikuler Bahasa & Kebudayaan Jepang SMASYIMDUTA Sidoarjo
* **Tahun Operasional**: 2026 (Kabinet Sora)
* **Lisensi Kode**: Didedikasikan untuk tujuan edukasi dan pengembangan klub.
