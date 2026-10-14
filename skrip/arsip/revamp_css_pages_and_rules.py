#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to revamp CSS architecture into css/pages/ (11 files),
update css/style.css, remove css/modules/, and install Workspace Rules
into panduan/CONTEKAN-TAG.md, .cursorrules, .github/copilot-instructions.md,
panduan/agent.md, and panduan/tree.md.
"""

import os
import shutil

def step1_split_css():
    print("--- STEP 1: Splitting CSS into css/pages/ ---")
    with open('css/modules/01-base-theme.css', 'r', encoding='utf-8') as f: c1 = f.read()
    with open('css/modules/02-header-hero-footer.css', 'r', encoding='utf-8') as f: c2 = f.read()
    with open('css/modules/03-kelas-kamus-latihan.css', 'r', encoding='utf-8') as f: c3 = f.read()
    with open('css/modules/04-proker-tentang.css', 'r', encoding='utf-8') as f: c4 = f.read()
    with open('css/modules/05-fitur-ekstra.css', 'r', encoding='utf-8') as f: c5 = f.read()

    pages_dir = 'css/pages'
    os.makedirs(pages_dir, exist_ok=True)

    page_slices = {
        'global.css': [
            "/* ==========================================================================\n   GLOBAL CSS — Mirai no Webu\n   Variabel :root, reset, sistem background selang-seling, tombol standar,\n   dark mode master, 404 estetik, dan sistem animasi reveal.\n   ========================================================================== */\n\n",
            c1,
            "\n\n/* Master Dark Mode System */\n",
            c3[70668:90332],
            "\n\n/* Efek Sinar Pink & Lightbox */\n",
            c4[141575:150953],
            "\n\n/* Motion Engine & 404 */\n",
            c5[153054:164859],
            c5[181346:181982]
        ],
        'navbar-hero-footer.css': [
            "/* ==========================================================================\n   NAVBAR, HERO & FOOTER — Mirai no Webu\n   Navbar melayang, off-canvas sidebar drawer, hero sticky curtain reveal,\n   hero-social-sidebar, three-tier header, hero guardrail, dan global footer.\n   ========================================================================== */\n\n",
            c2,
            "\n\n/* Mobile Menu Dark Mode */\n",
            c4[59219:59491],
            "\n\n/* Page Hero Chibi Styling */\n",
            c4[70085:73583],
            "\n\n/* Drawer Sora Widget */\n",
            c5[31974:32758],
            "\n\n/* Hero Layout Guardrail */\n",
            c5[228533:]
        ],
        'beranda.css': [
            "/* ==========================================================================\n   BERANDA (HOME) — Mirai no Webu\n   Seksi Apa itu Web, start-grid, aktivitas beranda (2 kartu besar),\n   masukan & saran (feedback preview), dan section quote slider.\n   ========================================================================== */\n\n",
            c4[59491:70085],
            "\n\n/* Nomor & Arrow Lingkaran Kartu Beranda */\n",
            c4[121900:126558],
            "\n\n/* Feature Card: Apa Itu Mirai no Webu */\n",
            c5[0:10505],
            "\n\n/* Feedback Preview Card */\n",
            c5[10505:28194]
        ],
        'kelas-materi.css': [
            "/* ==========================================================================\n   KELAS & MATERI — Mirai no Webu\n   class-overview, #dasar, #lanjutan, course-card, buuku-lesson, lesson-article,\n   #kurikulum, doc-big-card, learning-app, quest-hero, practice-view, result-view,\n   level-card, dan mode-card latihan kana.\n   ========================================================================== */\n\n",
            c3[0:70668],
            "\n\n/* Kana Practice Enhancements */\n",
            c3[90332:97001],
            "\n\n/* Chibi Placement & Contrast Guardrail */\n",
            c3[103302:],
            "\n\n/* Nomor & Chibi Kartu Kelas/Kurikulum */\n",
            c4[126558:127747],
            "\n\n/* Kurikulum & Tata Cara Mengajar */\n",
            c4[150953:196151],
            "\n\n/* Jalur Belajar & Kelas Dasar */\n",
            c4[198996:211082],
            "\n\n/* Kartu Alur Belajar */\n",
            c4[222747:],
            "\n\n/* Modal Latihan & Hasil Kana */\n",
            c5[164859:181346],
            "\n\n/* Pola Pattern Kartu Latihan Kana */\n",
            c5[181982:190364]
        ],
        'kamus.css': [
            "/* ==========================================================================\n   KAMUS & ENSIKLOPEDIA AKSARA — Mirai no Webu\n   dictionary-section, kana-card, kanji-card, stroke-stage, kanjivg,\n   quick-stroke-btn, script-intro-card, kanvas goresan Yoon, dan practice banner.\n   ========================================================================== */\n\n",
            c3[97001:103302],
            "\n\n/* Urutan Goresan KanjiVG & Karakter Yoon */\n",
            c4[73583:77503],
            "\n\n/* Kamus Jepang Exclusive Clean White Theme & Practice Banner */\n",
            c4[127747:141575],
            "\n\n/* Respacing Kamus */\n",
            c4[196151:196494],
            "\n\n/* Quick Floating Button Goresan */\n",
            c5[28194:31974]
        ],
        'kegiatan-divisi.css': [
            "/* ==========================================================================\n   KEGIATAN & DIVISI — Mirai no Webu\n   division-grid, program-grid, proker-hero, proker-section, njr-slider,\n   facility-section (kartu landscape), dan independent documentation slider.\n   ========================================================================== */\n\n",
            c4[0:22086],
            "\n\n/* Dokumentasi Slider Independen */\n",
            c4[77503:80799],
            "\n\n/* Respacing Kegiatan */\n",
            c4[196494:196990],
            "\n\n/* Seksi Fasilitas Mirai no Hana */\n",
            c5[144165:153054]
        ],
        'tentang.css': [
            "/* ==========================================================================\n   TENTANG (ABOUT) KLUB — Mirai no Webu\n   about-intro-section, about-flag-section, about-filosofi-section, logo-meaning-section,\n   slogan-section, vision-mission-section, timeline-section, sora-profile-section,\n   wall-of-fame-section, prestasi, haori-section, accessories-section, management-section, FAQ.\n   ========================================================================== */\n\n",
            c4[22086:59219],
            "\n\n/* Sejarah, Timeline, Sora RPG, Prestasi & FAQ */\n",
            c4[80799:121900],
            "\n\n/* Respacing Tentang */\n",
            c4[196990:197342],
            "\n\n/* Pattern w1b & w1w Halaman Tentang */\n",
            c4[211082:222747],
            "\n\n/* Penetapan Tema Warna Per Seksi Tentang */\n",
            c5[133667:144165]
        ],
        'rekomendasi-motivasi.css': [
            "/* ==========================================================================\n   REKOMENDASI & MOTIVASI — Mirai no Webu\n   motivasi-section, quote-card (3 box), rekomendasi-section, rek-card,\n   hero rekomendasi dua warna, media-rekomendasi-page, dan quote banner.\n   ========================================================================== */\n\n",
            c4[198384:198996],
            "\n\n/* Halaman Motivasi & Rekomendasi Media */\n",
            c5[32758:71911],
            "\n\n/* Section Kata Motivasi di Atas Disclaimer */\n",
            c5[130422:133667]
        ],
        'peringkat.css': [
            "/* ==========================================================================\n   PERINGKAT (LEADERBOARD) — Mirai no Webu\n   peringkat-section, leaderboard-tabs, podium-card (1, 2, 3), lb-table-card (4-10),\n   dan lb-modal-backdrop riwayat prestasi/siaran.\n   ========================================================================== */\n\n",
            c4[197802:198384],
            "\n\n/* Multi-Leaderboard, Podium & Modal Detail */\n",
            c5[71911:95351]
        ],
        'lomba.css': [
            "/* ==========================================================================\n   LOMBA & ACARA — Mirai no Webu\n   lomba-upcoming-section, lomba-catalog-section, event-card (vertical stacked),\n   poster full view carousel, tombol samping panah, spesifikasi 4 kolom, dan juknis-modal.\n   ========================================================================== */\n\n",
            c4[197342:197802],
            "\n\n/* Halaman Lomba & Acara, Katalog & Poster Carousel */\n",
            c5[95351:130422]
        ],
        'toko.css': [
            "/* ==========================================================================\n   TOKO & MIRAI NO KONBINI — Mirai no Webu\n   toko-hero, toko-catalog-section, toko-card (Shopee-style 185px), poster carousel\n   (Haori & KTA), toko-guide-white-section, toko-kwu-dark-section, toko-faq-white-section,\n   toko-cart-drawer & floating cart button.\n   ========================================================================== */\n\n",
            c5[190364:228533]
        ]
    }

    for fname, parts in page_slices.items():
        out_path = os.path.join(pages_dir, fname)
        with open(out_path, 'w', encoding='utf-8') as out_f:
            for part in parts:
                out_f.write(part)
        print(f"Created: {out_path} ({os.path.getsize(out_path)} bytes)")

def step2_update_style_css():
    print("--- STEP 2: Updating css/style.css and removing css/modules/ ---")
    style_content = """/* cspell:disable */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Noto+Serif+JP:wght@600;700;800;900&family=Noto+Sans+JP:wght@500;700;800;900&display=swap');

/* ==========================================================================
   MIRAI NO WEBU — Master Modular Stylesheet Index
   Sistem Desain: Obsidian Gelap & Putih Bersih, Pola Wagara, Responsif
   Arsitektur Berbasis Halaman 100% Intuitif (css/pages/)
   Urutan Cascade Dipertahankan Sempurna (100% Identik & Zero Conflict)
   ========================================================================== */

/* 1. Global: Variabel root, reset, background selang-seling, tombol dasar, dark mode, 404, animasi */
@import url('pages/global.css');

/* 2. Navbar, Hero, & Footer: Navbar melayang, off-canvas sidebar, hero banners, guardrail, & footer */
@import url('pages/navbar-hero-footer.css');

/* 3. Beranda: Seksi apa itu web, kisi fitur awal, aktivitas beranda, masukan & saran, quote slider */
@import url('pages/beranda.css');

/* 4. Kelas & Materi: Alur kelas, kelas dasar, kelas lanjutan, buuku lesson, kurikulum, & latihan quest */
@import url('pages/kelas-materi.css');

/* 5. Kamus & Aksara: Kamus kanji/kana, stroke order kanjivg, kanvas goresan, & quick button */
@import url('pages/kamus.css');

/* 6. Kegiatan & Divisi: Struktur 4 divisi, program kerja tahunan, fasilitas klub, & galeri slider */
@import url('pages/kegiatan-divisi.css');

/* 7. Tentang Klub: Profil klub, bendera, filosofi, logo, slogan, visi-misi, sejarah, haori, pengurus, FAQ */
@import url('pages/tentang.css');

/* 8. Rekomendasi & Motivasi: Kata motivasi anime, rekomendasi karya, & media legal */
@import url('pages/rekomendasi-motivasi.css');

/* 9. Papan Peringkat: Leaderboard keaktifan rajio, presensi, tabel skor, & modal prestasi */
@import url('pages/peringkat.css');

/* 10. Lomba & Acara: Papan info kompetisi, katalog lomba jejepangan, poster carousel, & modal */
@import url('pages/lomba.css');

/* 11. Toko & Konbini: Etalase atribut & F&B konbini, poster carousel produk, panduan PO, drawer keranjang */
@import url('pages/toko.css');
"""
    with open('css/style.css', 'w', encoding='utf-8') as f:
        f.write(style_content)
    print("Updated css/style.css with 11 page imports")

    if os.path.exists('css/modules'):
        shutil.rmtree('css/modules')
        print("Deleted legacy css/modules/ directory")

def step3_create_contekan_tag():
    print("--- STEP 3: Creating panduan/CONTEKAN-TAG.md ---")
    contekan_content = """# Contekan Cepat Peta Halaman & Berkas (Otak Otomatis)

Dokumen ini adalah acuan cepat (*cheat sheet*) satu pintu untuk memetakan setiap halaman web Mirai no Webu ke berkas CSS modular (`css/pages/`) dan berkas JavaScript (`js/`) yang bersangkutan.

> [!IMPORTANT]
> **Protokol Eksekusi Cepat (Fast-Execution Protocol)**:
> 1. **DILARANG** membaca `css/style.css` secara penuh atau memindai seluruh folder CSS sekaligus. Buka **hanya file CSS spesifik** di kolom tabel berikut.
> 2. **DILARANG** menyalakan/merestart HTTP server lokal (`python3 -m http.server`, live-server, dll.) atau mengambil screenshot otomatis via browser/tool kecuali diminta eksplisit oleh user.
> 3. Jika diminta mengubah elemen HTML yang berulang di banyak halaman (navbar, sidebar, hero, footer di 26+ file HTML), **WAJIB gunakan script terminal Python**, dilarang mengedit file satu per satu secara manual.

---

## Tabel Pemetaan Lengkap Halaman, CSS, & JS

| No | Halaman Web | Berkas HTML | Berkas CSS (`css/pages/`) | Berkas JS (`js/`) | Komponen & Fitur Kunci |
|---|---|---|---|---|---|
| **1** | **Global / Seluruh Web** | *Semua 30 Halaman* | `css/pages/global.css`<br>`css/pages/navbar-hero-footer.css` | `js/main.js` | Reset CSS, variabel warna, sistem selang-seling, navbar, sidebar drawer, hero sticky curtain, back-to-top, scroll reveal, dark mode, 404 |
| **2** | **Beranda** | `index.html` | `css/pages/beranda.css` | `js/main.js`<br>`js/sora.js` | Apa itu Mirai no Webu, start-grid, 2 kartu kegiatan, masukan & saran, slider kutipan footer |
| **3** | **Kelas & Kurikulum** | `kelas/index.html` | `css/pages/kelas-materi.css` | `js/main.js`<br>`js/sora.js` | Hub kelas, jalur belajar, kelas dasar (#dasar), kelas lanjutan (#lanjutan), kartu kurikulum (#kurikulum), tombol unduh/buka |
| **4** | **Latihan Mandiri Kana** | `kelas/latihan.html` | `css/pages/kelas-materi.css` | `js/main.js`<br>`js/script.js` | Kana Quest, 20 soal adaptif acak, kanvas goresan Duolingo-style, mode campuran, review kesalahan modal |
| **5** | **Kata Motivasi** | `kelas/motivasi.html` | `css/pages/rekomendasi-motivasi.css` | `js/main.js`<br>`js/sora.js` | Koleksi kutipan 5 karakter anime (Luffy, Eren, Naruto, Deku, Tanjiro), filter chips, layout 3 box |
| **6** | **Modul Buuku Dasar** | `materi/dasar/index.html`<br>`materi/dasar/hiragana.html`<br>`materi/dasar/katakana.html`<br>`materi/dasar/jikoshokai.html` | `css/pages/kelas-materi.css` | `js/main.js`<br>`js/sora.js` | Silabus dasar, tabel gojuuon, dakuon, yoon, kartu panduan perkenalan diri (Jikoshoukai) |
| **7** | **Modul Buuku Lanjutan** | `materi/lanjutan/index.html`<br>`materi/lanjutan/grammar.html`<br>`materi/lanjutan/kanji.html` | `css/pages/kelas-materi.css` | `js/main.js`<br>`js/sora.js` | Silabus lanjutan, panduan tata bahasa (Bunpou), daftar kanji JLPT N5–N1, kisi chip JLPT |
| **8** | **Kamus Kana & Kanji** | `kamus/index.html` | `css/pages/kamus.css` | `js/main.js`<br>`js/kana.js`<br>`js/kanji.js`<br>`js/stroke.js`<br>`js/api.js`<br>`js/translator.js` | Pencarian kana/kanji, filter alfabet, stage goresan KanjiVG, kanvas Yoon berdampingan, quick floating button |
| **9** | **Ensiklopedia Kanji** | `kamus/kanji.html` | `css/pages/kamus.css` | `js/main.js`<br>`js/kanji.js`<br>`js/stroke.js`<br>`js/api.js`<br>`js/translator.js` | Basis data 2.136 Joyo Kanji, arti Indonesia, onyomi, kunyomi, filter tingkat sekolah & level JLPT |
| **10** | **Hub Program & Fasilitas** | `kegiatan/index.html` | `css/pages/kegiatan-divisi.css` | `js/main.js`<br>`js/proker-slider.js` | Hub 4 divisi, 5 program kerja unggulan, fasilitas klub (format landscape), slider galeri foto |
| **11** | **Proker: Kimi To Nippon** | `kegiatan/kimi-to-nippon.html` | `css/pages/kegiatan-divisi.css` | `js/main.js`<br>`js/proker-slider.js` | Orientasi anggota baru, filosofi KTN, slider dokumentasi foto kegiatan |
| **12** | **Proker: Nihon Go Rajio** | `kegiatan/nihon-go-rajio.html` | `css/pages/kegiatan-divisi.css` | `js/main.js`<br>`js/proker-slider.js` | Siaran radio mingguan sekolah, segmen siaran, slider dokumentasi siaran |
| **13** | **Proker: Mirai no Konbini** | `kegiatan/konbini.html` | `css/pages/kegiatan-divisi.css` | `js/main.js`<br>`js/proker-slider.js` | Stan bazaar kuliner & cinderamata kreatif, dokumentasi bazaar |
| **14** | **Proker: Ramadhan** | `kegiatan/ramadhan.html` | `css/pages/kegiatan-divisi.css` | `js/main.js`<br>`js/proker-slider.js` | Bakti sosial & takjil puasa, dokumentasi kegiatan baksos |
| **15** | **Proker: Tomodachi** | `kegiatan/tomodachi.html` | `css/pages/kegiatan-divisi.css` | `js/main.js`<br>`js/proker-slider.js` | Forum jejaring persahabatan, sesi tukar cerita, dokumentasi tomodachi |
| **16** | **Hub Divisi Resmi** | `divisi/index.html` | `css/pages/kegiatan-divisi.css` | `js/main.js`<br>`js/sora.js` | Ringkasan 4 divisi resmi klub Mirai no Hana |
| **17** | **Divisi Bahasa & Budaya** | `divisi/bahasa.html` | `css/pages/kegiatan-divisi.css` | `js/main.js` | Profil divisi bahasa, program pendalaman tata bahasa & kanji |
| **18** | **Divisi Cosplay & Peran** | `divisi/cosplay.html` | `css/pages/kegiatan-divisi.css` | `js/main.js` | Profil divisi cosplay, pembuatan kostum & aksi panggung |
| **19** | **Divisi Desain & Kreatif** | `divisi/desain.html` | `css/pages/kegiatan-divisi.css` | `js/main.js` | Profil divisi desain, ilustrasi digital, poster, dan dekorasi |
| **20** | **Divisi Kewirausahaan** | `divisi/kewirausahaan.html` | `css/pages/kegiatan-divisi.css` | `js/main.js` | Profil divisi KWU, produksi merchandise & kuliner konbini |
| **21** | **Tentang Klub** | `tentang/index.html` | `css/pages/tentang.css` | `js/main.js`<br>`js/leaderboard-data.js` | Profil klub, bendera resmi, filosofi nama, logo, slogan, visi misi, timeline sejarah angkatan 1–8, profil Sora RPG, wall of fame prestasi, haori, aksesoris, slider kepengurusan, FAQ |
| **22** | **Lomba & Acara** | `lomba/index.html` | `css/pages/lomba.css` | `js/main.js`<br>`js/script.js`<br>`js/sora.js` | Papan info 18 lomba/event jejepangan, kartu bertumpuk vertikal, poster carousel kiri-kanan, modal juknis |
| **23** | **Papan Peringkat** | `peringkat/index.html` | `css/pages/peringkat.css` | `js/main.js`<br>`js/script.js`<br>`js/leaderboard-data.js`<br>`js/sora.js` | Multi-leaderboard keaktifan rajio & presensi, podium rank 1-3, tabel peringkat 4-10, modal riwayat |
| **24** | **Rekomendasi Media** | `rekomendasi/index.html` | `css/pages/rekomendasi-motivasi.css` | `js/main.js`<br>`js/script.js`<br>`js/sora.js` | Rekomendasi anime, film, musik jejepangan, platform legal, tips edukatif |
| **25** | **Toko Resmi & Konbini** | `toko/index.html` | `css/pages/toko.css` | `js/main.js`<br>`js/script.js`<br>`js/carousel.js`<br>`js/sora.js` | Etalase 12 produk atribut (Haori, KTA) & F&B konbini, Shopee-style thumb 185px, carousel foto depan/belakang, panduan PO, keranjang belanja mengambang |
| **26** | **Ruang Chat Sora** | `sora/index.html` | `css/pages/navbar-hero-footer.css` | `js/main.js`<br>`js/sora.js` | Antarmuka obrolan interaktif maskot Asora Aokita, balasan lokal offline |
| **27** | **Error 404** | `404.html` | `css/pages/global.css` | `js/main.js` | Halaman penanganan tautan salah bertema sakura melayang, avatar Sora, pencarian pintar 404 |

---

## Peta Cepat Logika JavaScript (`js/`)

- **`js/main.js`**: Pengendali antarmuka global (navbar, sidebar drawer, hero sticky curtain reveal, back-to-top, scroll reveal, dan tema) &mdash; *dipakai di seluruh 30 halaman HTML*.
- **`js/script.js`**: Mesin kuis interaktif pembelajaran mandiri Kana Quest (20 soal adaptif acak, kanvas goresan Duolingo-style, dan evaluasi hasil) &mdash; *dipakai di `kelas/latihan.html`*.
- **`js/carousel.js`**: Komponen slider horizontal mandiri `[data-slider]` dengan navigasi panah, dots, dan touch swipe &mdash; *dipakai di komponen etalase/slider*.
- **`js/proker-slider.js`**: Pengendali interaktif slider galeri program kerja & dokumentasi kegiatan klub &mdash; *dipakai di 6 halaman kegiatan*.
- **`js/kana.js`**: Pengelola tabel karakter aksara Kana (Hiragana & Katakana), filter Gojuuon/Dakuon/Yoon, pencarian, dan audio pelafalan &mdash; *dipakai di `kamus/index.html` & `kamus/kanji.html`*.
- **`js/kanji.js`**: Mesin pencarian dan ensiklopedia 2.136 karakter Joyo Kanji, filter tingkat JLPT/kelas, dan modal detail kanji &mdash; *dipakai di `kamus/index.html` & `kamus/kanji.html`*.
- **`js/stroke.js`**: Mesin animasi kanvas urutan goresan karakter Kanji dan kombinasi Kana Yoon di atas kisi Genkouyoushi &mdash; *dipakai di `kamus/index.html` & `kamus/kanji.html`*.
- **`js/sora.js`**: Logika asisten chatbot maskot Asora Aokita (Sora), filter jawaban offline cerdas, saran halaman, dan drawer UI &mdash; *dipakai di 18 halaman*.
- **`js/api.js`**: Layanan terpadu API data kamus & karakter (`MiraiData`), caching localStorage, dan loader dataset `data/kana.json` &mdash; *modul penyedia data sentral*.
- **`js/translator.js`**: Mesin penerjemah leksikal kamus (`MiraiTranslator`) dari makna bahasa Inggris ke padanan istilah Bahasa Indonesia &mdash; *dipakai di `kamus/index.html` & `kamus/kanji.html`*.
- **`js/leaderboard-data.js`**: Master data terpusat untuk papan peringkat keaktifan, presensi kehadiran anggota, dan rekam jejak prestasi siswa &mdash; *dipakai di `peringkat/index.html` & `tentang/index.html`*.
"""
    with open('panduan/CONTEKAN-TAG.md', 'w', encoding='utf-8') as f:
        f.write(contekan_content)
    print("Created panduan/CONTEKAN-TAG.md")

def step4_create_ide_rules():
    print("--- STEP 4: Creating .cursorrules and .github/copilot-instructions.md ---")
    rules_content = """# Workspace Rules & Otak Otomatis — Mirai No Webu

Repositori ini adalah website resmi Klub Bahasa & Kebudayaan Jepang MIRAI NO HANA SMA Wachid Hasyim 2 Taman Sidoarjo.

## 1. Protokol Eksekusi Cepat (Fast-Execution Protocol)
- **DILARANG KERAS** membaca `css/style.css` secara penuh atau memindai seluruh folder CSS sekaligus.
- Seluruh stylesheet antarmuka diorganisir secara intuitif per-halaman di `css/pages/`.
- **DILARANG KERAS** menyalakan/merestart HTTP server lokal (`python3 -m http.server`, live-server, dll.) atau mengambil screenshot otomatis via browser/tool kecuali diminta secara eksplisit oleh user.
- Jika diminta mengubah elemen HTML yang berulang di banyak halaman (navbar, sidebar, hero, atau footer di 26+ file HTML), **WAJIB gunakan script terminal Python sekali-jalan**, dilarang mengedit file satu per satu secara manual.

## 2. Peta Cepat Halaman -> CSS (`css/pages/`) -> JS (`js/`)
Rujuk tabel berikut untuk langsung membuka file target yang benar tanpa perlu bertanya atau menebak:

| Kebutuhan Edit Halaman | Buka File CSS (`css/pages/`) | Buka File JS (`js/`) |
|---|---|---|
| Navbar, Sidebar Drawer, Hero Banner, Footer | `css/pages/navbar-hero-footer.css` | `js/main.js` |
| Reset, Variabel Warna Root, Background Selang-Seling, Tombol Standar, 404, Animasi | `css/pages/global.css` | `js/main.js` |
| Beranda (Apa itu web, fitur awal, masukan & saran, aktivitas) | `css/pages/beranda.css` | `js/main.js`, `js/sora.js` |
| Kelas, Kurikulum, Materi Buuku, Kana Quest (Latihan) | `css/pages/kelas-materi.css` | `js/main.js`, `js/script.js` |
| Kamus Kana, Ensiklopedia Kanji, Urutan Goresan KanjiVG | `css/pages/kamus.css` | `js/kana.js`, `js/kanji.js`, `js/stroke.js`, `js/api.js`, `js/translator.js` |
| Program Kerja (KTN, NJR, Konbini, Ramadhan, Tomodachi), 4 Divisi, Fasilitas | `css/pages/kegiatan-divisi.css` | `js/main.js`, `js/proker-slider.js` |
| Profil Klub Tentang, Bendera, Logo, Slogan, Visi Misi, Timeline Sejarah, Prestasi, Haori, Pengurus, FAQ | `css/pages/tentang.css` | `js/main.js`, `js/leaderboard-data.js` |
| Kata Motivasi & Rekomendasi Media Pop Culture | `css/pages/rekomendasi-motivasi.css` | `js/main.js`, `js/sora.js` |
| Papan Peringkat (Multi-Leaderboard, Podium, Tabel) | `css/pages/peringkat.css` | `js/main.js`, `js/leaderboard-data.js` |
| Lomba & Acara Jejepangan, Katalog Event, Poster | `css/pages/lomba.css` | `js/main.js`, `js/script.js` |
| Toko Resmi Mirai no Konbini, Keranjang Belanja | `css/pages/toko.css` | `js/main.js`, `js/carousel.js` |
| Chatbot Asora Aokita (Sora) | `css/pages/navbar-hero-footer.css` | `js/sora.js`, `js/api.js` |

Detail lengkap tersedia di `panduan/CONTEKAN-TAG.md` dan `panduan/agent.md`.
"""
    with open('.cursorrules', 'w', encoding='utf-8') as f:
        f.write(rules_content)
    print("Created .cursorrules")

    os.makedirs('.github', exist_ok=True)
    with open('.github/copilot-instructions.md', 'w', encoding='utf-8') as f:
        f.write(rules_content)
    print("Created .github/copilot-instructions.md")

def step5_update_agent_md():
    print("--- STEP 5: Updating panduan/agent.md ---")
    with open('panduan/agent.md', 'r', encoding='utf-8') as f:
        content = f.read()

    old_peta_css = """### 1. Peta Modul CSS (DILARANG Membaca style.css Utuh)
- **DILARANG KERAS** membaca `css/style.css` secara keseluruhan atau memindai semua modul CSS sekaligus ke dalam konteks percakapan.
- `css/style.css` kini murni berfungsi sebagai master index pengimpor (`@import`) 5 modul terpisah.
- Untuk membaca atau mengedit aturan CSS, **hanya buka modul spesifik yang relevan** sesuai peta berikut:
  - **`css/modules/01-base-theme.css`**: Variabel warna root, CSS reset, sistem selang-seling background ganjil/genap, dan tombol dasar.
  - **`css/modules/02-header-hero-footer.css`**: Floating navbar, off-canvas sidebar menu, banner hero section semua halaman, global footer, dan three-tier header.
  - **`css/modules/03-kelas-kamus-latihan.css`**: Halaman Kelas (`kelas/*`), Materi (`materi/*`), Kamus (`kamus/*`), kuis Latihan Kana, kanvas urutan goresan (stroke order), dan kurikulum.
  - **`css/modules/04-proker-tentang.css`**: Halaman Kegiatan/Proker (`kegiatan/*`), Divisi (`divisi/*`), Tentang Klub (`tentang/index.html`), filosofi, logo, slogan, visi misi, haori, kepengurusan, timeline, sora profile, prestasi, dan FAQ.
  - **`css/modules/05-fitur-ekstra.css`**: Komponen Beranda (`index.html`), Rekomendasi (`rekomendasi/index.html`), Peringkat (`peringkat/index.html`), Lomba (`lomba/index.html`), Toko (`toko/index.html`), 404 (`404.html`), animasi umum, dan Hero Guardrail."""

    new_peta_css = """### 1. Peta CSS Halaman Intuitif (DILARANG Membaca style.css Utuh)
- **DILARANG KERAS** membaca `css/style.css` secara keseluruhan atau memindai seluruh folder CSS sekaligus ke dalam konteks percakapan.
- `css/style.css` kini murni berfungsi sebagai master index pengimpor (`@import`) 11 file CSS berbasis halaman di `css/pages/`.
- Rujuk tabel di **`panduan/CONTEKAN-TAG.md`** atau peta berikut untuk langsung membuka file target:
  - **`css/pages/global.css`**: Variabel :root, CSS reset, sistem background selang-seling, tombol standar, dark mode master, 404 estetik, dan sistem animasi reveal.
  - **`css/pages/navbar-hero-footer.css`**: Floating navbar, off-canvas sidebar nav, banner hero section semua halaman, hero-social-sidebar, hero guardrail, dan global footer.
  - **`css/pages/beranda.css`**: Komponen Beranda (`index.html`), apa itu web (`.about-preview`, `.start-grid`), aktivitas beranda (2 kartu besar), masukan & saran (`.feedback-preview`), dan quote slider.
  - **`css/pages/kelas-materi.css`**: Hub Kelas (`kelas/index.html`), jalur belajar (`.class-overview`), kelas dasar (`#dasar`), kelas lanjutan (`#lanjutan`), buuku lesson (`materi/*`), kurikulum (`#kurikulum`, `.doc-big-card`), dan kuis Kana Quest (`kelas/latihan.html`, `.practice-view`, `.result-view`).
  - **`css/pages/kamus.css`**: Kamus Kana & Kanji (`kamus/index.html`, `kamus/kanji.html`), kartu karakter, stage urutan goresan KanjiVG, kanvas kombinasi Yoon, dan tombol quick stroke.
  - **`css/pages/kegiatan-divisi.css`**: Hub Kegiatan & Fasilitas (`kegiatan/index.html`), 5 halaman proker (`kegiatan/*`), 4 halaman divisi (`divisi/*`), dan fasilitas klub (format landscape).
  - **`css/pages/tentang.css`**: Halaman Profil Klub (`tentang/index.html`), bendera resmi, filosofi nama, makna logo, slogan, visi misi, timeline sejarah angkatan 1–8, profil Sora RPG, wall of fame prestasi, haori, aksesoris, slider kepengurusan, dan FAQ.
  - **`css/pages/rekomendasi-motivasi.css`**: Halaman Kata Motivasi (`kelas/motivasi.html`), quote-card 3 box, rekomendasi karya (`rekomendasi/index.html`), hero dua warna, dan media legal.
  - **`css/pages/peringkat.css`**: Halaman Papan Peringkat (`peringkat/index.html`), leaderboard-tabs, podium rank 1–3, tabel peringkat 4–10, dan modal riwayat keaktifan/prestasi.
  - **`css/pages/lomba.css`**: Halaman Lomba & Acara (`lomba/index.html`), kartu event vertikal bertumpuk, poster carousel utuh, navigasi panah tengah samping, dan modal juknis.
  - **`css/pages/toko.css`**: Toko Resmi & Konbini (`toko/index.html`), etalase 12 produk atribut & F&B, Shopee-style thumb 185px, carousel geser Haori & KTA, drawer keranjang belanja, dan panduan PO."""

    content = content.replace(old_peta_css, new_peta_css)

    old_css_root = "- **`css/`**: Berisi master stylesheet antarmuka (`css/style.css`) yang memanggil 5 modul terpisah di `css/modules/` (`01-base-theme.css` s.d. `05-fitur-ekstra.css`)."
    new_css_root = "- **`css/`**: Berisi master stylesheet antarmuka (`css/style.css`) yang memanggil 11 berkas CSS berbasis halaman di sub-folder `css/pages/` (`global.css`, `navbar-hero-footer.css`, `beranda.css`, `kelas-materi.css`, `kamus.css`, `kegiatan-divisi.css`, `tentang.css`, `rekomendasi-motivasi.css`, `peringkat.css`, `lomba.css`, `toko.css`)."
    content = content.replace(old_css_root, new_css_root)

    with open('panduan/agent.md', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated panduan/agent.md")

def step6_update_tree_md():
    print("--- STEP 6: Updating panduan/tree.md ---")
    with open('panduan/tree.md', 'r', encoding='utf-8') as f:
        tree = f.read()

    old_css_tree = """├── css/                            # Master & Arsitektur Stylesheet Modular
│   ├── style.css                   # Master CSS Index (Hanya memuat @import Google Fonts & 5 modul)
│   └── modules/                    # Sub-folder pecahan stylesheet modular (terisolasi & performan)
│       ├── 01-base-theme.css       # Variabel warna, CSS reset, tombol dasar, & sistem selang-seling
│       ├── 02-header-hero-footer.css # Floating navbar, off-canvas sidebar, hero banners, & footer
│       ├── 03-kelas-kamus-latihan.css # Modul pembelajaran kelas, kana quest, kamus, stroke order, & kurikulum
│       ├── 04-proker-tentang.css   # Divisi, proker, profil klub, filosofi, logo, slogan, visi misi, haori, FAQ
│       └── 05-fitur-ekstra.css     # Kartu beranda, kutipan motivasi, rekomendasi, peringkat, lomba, toko, animasi"""

    new_css_tree = """├── css/                            # Master & Arsitektur Stylesheet Berbasis Halaman
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
│       └── toko.css                # Etalase atribut & F&B konbini, Shopee-style 185px, poster carousel Haori/KTA, drawer keranjang"""

    tree = tree.replace(old_css_tree, new_css_tree)

    # Add .cursorrules, .github, and panduan/CONTEKAN-TAG.md
    old_root_files = """├── 404.html                        # Halaman penanganan tautan salah / tidak ditemukan bertema Sora
├── README.md                       # Profil utama repositori & dokumentasi Sources & Credits
├── cspell.json                     # Konfigurasi Code Spell Checker (kamus & ignorasi kata bilingual)
├── .vscode/                        # Konfigurasi workspace editor VS Code / Antigravity
│   └── settings.json               # Pengaturan workspace, search.exclude, & files.watcherExclude"""

    new_root_files = """├── 404.html                        # Halaman penanganan tautan salah / tidak ditemukan bertema Sora
├── README.md                       # Profil utama repositori & dokumentasi Sources & Credits
├── cspell.json                     # Konfigurasi Code Spell Checker (kamus & ignorasi kata bilingual)
├── .cursorrules                    # Aturan otomatis workspace editor Cursor (Otak Otomatis AI)
├── .github/                        # Konfigurasi integrasi GitHub
│   └── copilot-instructions.md     # Instruksi otomatis GitHub Copilot (Otak Otomatis AI)
├── .vscode/                        # Konfigurasi workspace editor VS Code / Antigravity
│   └── settings.json               # Pengaturan workspace, search.exclude, & files.watcherExclude"""

    tree = tree.replace(old_root_files, new_root_files)

    old_panduan = """├── panduan/                        # Dokumentasi & Panduan Proyek
│   ├── tree.md                     # Peta struktur direktori lengkap proyek ini
│   └── agent.md                    # Pedoman aturan desain, protokol eksekusi cepat, dan persona AI"""

    new_panduan = """├── panduan/                        # Dokumentasi & Panduan Proyek
│   ├── CONTEKAN-TAG.md             # Acuan cepat pemetaan halaman -> CSS -> JS (Otak Otomatis)
│   ├── tree.md                     # Peta struktur direktori lengkap proyek ini
│   └── agent.md                    # Pedoman aturan desain, protokol eksekusi cepat, dan persona AI"""

    tree = tree.replace(old_panduan, new_panduan)

    with open('panduan/tree.md', 'w', encoding='utf-8') as f:
        f.write(tree)
    print("Updated panduan/tree.md")

def main():
    step1_split_css()
    step2_update_style_css()
    step3_create_contekan_tag()
    step4_create_ide_rules()
    step5_update_agent_md()
    step6_update_tree_md()
    print("\nALL TASKS COMPLETED SUCCESSFULLY!")

if __name__ == '__main__':
    main()
