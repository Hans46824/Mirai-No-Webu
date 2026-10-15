#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skrip Otomasi Pembaruan Dokumentasi & Panduan Developer
Mirai No Webu — Klub Bahasa & Kebudayaan Jepang MIRAI NO HANA
"""

import os
import shutil

print("=== MEMULAI PEMBARUAN DOKUMENTASI MIRAI NO WEBU ===")

# -------------------------------------------------------------
# 1. Bersihkan Root & ai-configs
# -------------------------------------------------------------
os.makedirs("panduan/ai-configs", exist_ok=True)

if os.path.exists(".cursorrules"):
    shutil.move(".cursorrules", "panduan/ai-configs/.cursorrules")
    print("[1] .cursorrules dipindahkan ke panduan/ai-configs/.cursorrules")

if os.path.exists(".github/copilot-instructions.md"):
    shutil.move(".github/copilot-instructions.md", "panduan/ai-configs/copilot-instructions.md")
    print("[1] copilot-instructions.md dipindahkan ke panduan/ai-configs/copilot-instructions.md")

if os.path.exists(".github"):
    try:
        os.rmdir(".github")
        print("[1] Folder .github berhasil dihapus")
    except OSError:
        shutil.rmtree(".github")
        print("[1] Folder .github berhasil dibersihkan")

# Hapus sisa file py di luar skrip/arsip/
for f in ["skrip/build_kanji_database.py", "skrip/apply_latihan_fullscreen_nav.py"]:
    if os.path.exists(f):
        os.remove(f)
        print(f"[1] Menghapus file skrip temporer: {f}")

# Pastikan css/modules dan css/style.css.bak bersih
if os.path.exists("css/modules"):
    shutil.rmtree("css/modules")
    print("[1] Menghapus css/modules")
if os.path.exists("css/style.css.bak"):
    os.remove("css/style.css.bak")
    print("[1] Menghapus css/style.css.bak")

# Buat panduan/ai-configs/README.md jika belum ada
ai_readme_content = """# Konfigurasi AI Assistant (Cursor, Copilot, Claude, Codex)

Folder ini menyimpan berkas aturan instruksi otomatis (*AI rules & system prompts*) untuk editor dan asisten cerdas yang digunakan oleh pengembang Mirai no Webu:

## Berkas yang Tersedia:
1. **`.cursorrules`**: Konfigurasi otomatis untuk editor **Cursor AI**. Jika Anda menggunakan Cursor, salin berkas ini ke *root* direktori proyek atau ke `.cursor/rules/`.
2. **`copilot-instructions.md`**: Konfigurasi instruksi sistem untuk **GitHub Copilot**. Jika Anda menggunakan ekstensi Copilot di VS Code atau GitHub, salin berkas ini ke `.github/copilot-instructions.md`.
3. **Claude Code / CLAUDE.md**: Jika menggunakan Claude Code CLI, Anda dapat merujuk atau menautkan aturan dari `panduan/agent.md` atau berkas ini.
4. **Antigravity AI**: Pengguna Google Antigravity secara otomatis membaca `panduan/agent.md` dan `panduan/CONTEKAN-TAG.md` sebagai sumber kebenaran tunggal (*Single Source of Truth*).

> [!NOTE]
> Berkas-berkas ini disimpan di folder `panduan/ai-configs/` agar *root* direktori proyek tetap bersih (*Clean Root Standard*) dan memudahkan pengurus klub dalam memelihara struktur repositori.
"""
with open("panduan/ai-configs/README.md", "w", encoding="utf-8") as f:
    f.write(ai_readme_content)
print("[1] Berkas panduan/ai-configs/README.md siap")

# -------------------------------------------------------------
# 2. Sempurnakan panduan/agent.md
# -------------------------------------------------------------
with open("panduan/agent.md", "r", encoding="utf-8") as f:
    agent_text = f.read()

# Perbarui deskripsi panduan/ di Bab 2.A
old_p = "- **`panduan/`**: Berisi dokumentasi arsitektur proyek (`panduan/tree.md`, `panduan/agent.md`)."
new_p = "- **`panduan/`**: Berisi dokumentasi arsitektur proyek (`panduan/tree.md`, `panduan/agent.md`, `panduan/CONTEKAN-TAG.md`, `panduan/PANDUAN-DEVELOPER.md`, dan folder konfigurasi AI `panduan/ai-configs/`)."
if old_p in agent_text:
    agent_text = agent_text.replace(old_p, new_p)

# Tambahkan Bagian 13: Panduan Lokasi Data Dinamis
section_13_text = """

---

## 13. Panduan Lokasi Data Dinamis (Pembaruan Rutin Pengurus)

Website Mirai no Webu mengadopsi arsitektur *Zero-Framework* yang mengelompokkan data dinamis ke dalam berkas-berkas spesifik agar pengurus klub mudah melakukan pembaruan konten secara teratur tanpa merusak struktur visual halaman:

### 1. Skor & Riwayat Peringkat (`js/leaderboard-data.js`)
- **Tujuan**: Memperbarui peringkat keaktifan siaran Nihon Go Rajio (NJR), presensi kehadiran rapat klub, dan rekam jejak juara siswa.
- **Cara Update**: Buka `js/leaderboard-data.js`, sesuaikan array data:
  - `RAJIO_LEADERBOARD`: Nama siswa, avatar chibi (`Al`, `Ay`, `Hu`, dll.), kelas, poin keaktifan, dan status siaran.
  - `ATTENDANCE_LEADERBOARD`: Persentase presensi dan akumulasi kehadiran per semester.
  - `ACHIEVEMENT_DATA`: Riwayat medali dan kejuaraan perlombaan eksternal.
- **Dampak Visual**: Otomatis memperbarui podium Rank 1–3, tabel peringkat di `peringkat/index.html`, serta galeri prestasi di `tentang/index.html`.

### 2. Data Kamus, Karakter & Goresan (`data/kana.json`, `data/kanji.json`, `js/stroke-data.js`)
- **Tujuan**: Menambah kosakata baru, melengkapi arti kanji bahasa Indonesia, atau memperbarui koordinat animasi goresan kuas.
- **Berkas Terkait**:
  - `data/kana.json`: Inventaris aksara Hiragana & Katakana beserta audio pelafalan.
  - `data/kanji.json` & `data/kanji-meta.json`: Basis data lengkap 2.136 Joyo Kanji (N5–N1), level JLPT, jumlah goresan, arti Bahasa Indonesia, On'yomi, Kun'yomi, dan contoh kosakata.
  - `js/stroke-data.js`: Koordinat vektor goresan KanjiVG terkurasi untuk kanvas interaktif.
- **Catatan Penting**: Pastikan struktur JSON valid (tanpa koma berlebih di elemen terakhir). Jika menambah kanji baru, pastikan koordinat goresannya terdaftar di `js/stroke-data.js` agar animasi goresan tidak kosong.

### 3. Katalog Lomba & Acara (`lomba/index.html`)
- **Tujuan**: Menambah informasi lomba jejepangan tingkat kota/provinsi/nasional atau pengumuman festival matsuri terbaru.
- **Cara Update**: Tambahkan kartu `<article class="event-card" data-event-type="..." data-event-region="...">` baru di dalam kontainer `.lomba-grid`.
- **Komponen Wajib**:
  - Poster resmi beresolusi jelas di `lomba/images/` dalam kontainer carousel `[data-event-carousel]`.
  - Grid spesifikasi: Pelaksanaan, Biaya Pendaftaran, Lokasi/Platform, dan Cabang Lomba.
  - Tombol aksi tautan pendaftaran atau informasi Instagram resmi (`target="_blank"`).

### 4. Katalog Toko / Mirai no Konbini (`toko/index.html`)
- **Tujuan**: Menambah atau memperbarui atribut resmi klub (Haori, KTA, lanyard) serta menu kuliner/minuman Jepang bazaar Konbini.
- **Cara Update**: Tambahkan kartu produk `<div class="toko-card" data-category="...">` di dalam grid `.toko-grid`.
- **Standar Format Produk**:
  - Foto Shopee-style 185px (makanan cover penuh di `images/mirai/produk/`, atribut berlatar putih bersih).
  - Jika produk memiliki tampak depan & belakang (seperti Haori / KTA), gunakan komponen carousel `[data-product-carousel]`.
  - Spesifikasi bahan, status ketersediaan (Tersedia / Pra-Pesan PO), dan harga rupiah yang jelas.

### 5. Kepengurusan, Sejarah & Prestasi (`tentang/index.html`)
- **Tujuan**: Melakukan pembaruan struktur organisasi saat Serah Terima Jabatan (Sertijab) tahunan, penambahan timeline sejarah angkatan baru, dan wall of fame prestasi siswa.
- **Komponen Terkait**:
  - Slider Kepengurusan: Tambahkan slide kabinet baru atau perbarui kartu pengurus di `tentang/index.html` (foto potret anggota di `tentang/images/anggota/`, nama lengkap, jabatan tunggal di `.member-label`, dan kutipan moto).
  - Garis Waktu Angkatan (Timeline): Tambahkan balok angkatan baru di seksi sejarah klub (`#sejarah`).
  - Dinding Prestasi (Wall of Fame): Tambahkan kartu piala dan piagam penghargaan anggota di seksi `#prestasi`.
"""

if "## 13. Panduan Lokasi Data Dinamis" not in agent_text:
    agent_text = agent_text.rstrip() + section_13_text + "\n"
    print("[2] Menambahkan Bab 13 ke panduan/agent.md")

with open("panduan/agent.md", "w", encoding="utf-8") as f:
    f.write(agent_text)
print("[2] panduan/agent.md berhasil disimpan")

# -------------------------------------------------------------
# 3. Buat panduan/PANDUAN-DEVELOPER.md
# -------------------------------------------------------------
developer_guide_content = """# 🌸 Buku Panduan Serah-Terima Pengembang & Pengurus
## Website Resmi Mirai no Webu — MIRAI NO HANA SMA Wachid Hasyim 2 Taman Sidoarjo

Selamat datang, Pengurus dan Pengembang Generasi Penerus Klub Bahasa & Kebudayaan Jepang **MIRAI NO HANA**! 🎌

Dokumen ini disusun sebagai **Buku Saku Serah-Terima Jabatan (Sertijab)** untuk memandu Anda memahami, merawat, dan mengembangkan website **Mirai no Webu**. Website ini dirancang 100% mandiri oleh siswa anggota klub sebagai ruang berkarya, wadah belajar interaktif, dan etalase kebanggaan ekstrakurikuler kita.

---

## 📑 Daftar Isi
1. [Pengenalan Arsitektur Web (Zero-Framework Architecture)](#1-pengenalan-arsitektur-web-zero-framework-architecture)
2. [Peta Berkas & Folder Lengkap (File Map)](#2-peta-berkas--folder-lengkap-file-map)
3. [Tutorial Langkah-demi-Langkah Update Konten Rutin](#3-tutorial-langkah-demi-langkah-update-konten-rutin)
   - [3.1 Tambah Info Lomba & Acara Baru](#31-tambah-info-lomba--acara-baru)
   - [3.2 Update Skor & Leaderboard Peringkat](#32-update-skor--leaderboard-peringkat)
   - [3.3 Tambah Produk Toko / Konbini](#33-tambah-produk-toko--konbini)
   - [3.4 Tambah Foto Dokumentasi Program Kerja](#34-tambah-foto-dokumentasi-program-kerja)
   - [3.5 Update Kepengurusan Baru saat Sertijab](#35-update-kepengurusan-baru-saat-sertijab)
4. [Standar Desain & Estetika Visual Wajib](#4-standar-desain--estetika-visual-wajib)
5. [Cara Menggunakan AI Assistant (Pair Programming)](#5-cara-menggunakan-ai-assistant-pair-programming)
6. [Panduan Alur Git & Deployment GitHub Pages](#6-panduan-alur-git--deployment-github-pages)
7. [Checklist Serah-Terima Jabatan & Kontak](#7-checklist-serah-terima-jabatan--kontak)

---

## 1. Pengenalan Arsitektur Web (Zero-Framework Architecture)

Website Mirai no Webu sengaja dibangun menggunakan prinsip **Zero-Framework Web Standards**:
- **HTML5 Semantik Murni**: Struktur halaman yang ramah mesin pencari, aksesibel, dan mudah dibaca tanpa sintaks JSX/template engine rumit.
- **Modular CSS Berbasis Halaman (`css/pages/`)**: Tidak ada file CSS monolitik raksasa yang membingungkan. Setiap halaman web memiliki file CSS tersendiri.
- **Vanilla JavaScript (ES6+)**: Logika interaktif berjalan murni tanpa dependensi Node.js, React, Vue, atau build tools seperti Webpack/Vite.

### Mengapa Pendekatan Ini Dipilih?
1. **Abadi & Bebas Kerusakan Dependensi**: Website tidak akan pernah rusak hanya karena ada versi `npm package` yang usang di masa depan.
2. **Bisa Langsung Dijalankan di Browser**: Cukup klik dua kali `index.html` di komputer Anda, dan web langsung terbuka sempurna tanpa install apa pun.
3. **Gratis Selamanya di GitHub Pages**: Hosting web statis ini sepenuhnya gratis, cepat, dan terhubung langsung dengan repositori GitHub klub.

### Arsitektur CSS Modular:
Berkas `css/style.css` murni berfungsi sebagai **Master Index** yang mengimpor 11 file spesifik di `css/pages/`:
```text
css/
├── style.css                   # Master Index (@import fonts & 11 sub-file)
└── pages/
    ├── global.css              # Variabel :root, reset, dark mode, tombol, 404
    ├── navbar-hero-footer.css  # Navbar floating, sidebar drawer, hero banners, footer
    ├── beranda.css             # Komponen Beranda (index.html)
    ├── kelas-materi.css        # Modul kelas, kurikulum, dan kuis latihan
    ├── kamus.css               # Kamus Kana, Joyo Kanji, dan kanvas goresan
    ├── kegiatan-divisi.css     # Hub kegiatan, 5 proker, 4 divisi, fasilitas
    ├── tentang.css             # Profil klub, bendera, timeline sejarah, pengurus
    ├── rekomendasi-motivasi.css# Motivasi anime & rekomendasi karya pop culture
    ├── peringkat.css           # Leaderboard keaktifan, presensi, dan podium
    ├── lomba.css               # Informasi lomba jejepangan & poster carousel
    └── toko.css                # Etalase produk atribut & F&B Mirai no Konbini
```
> [!IMPORTANT]
> **Aturan Emas Styling**: Jika Anda atau AI ingin mengubah tampilan halaman tertentu, **langsung buka berkas di `css/pages/*.css` terkait**. DILARANG mengedit atau membaca `css/style.css` secara utuh.

---

## 2. Peta Berkas & Folder Lengkap (File Map)

Gunakan tabel praktis ini untuk mengetahui berkas mana yang harus dibuka saat ingin melakukan perubahan:

| Kebutuhan Pengurus | Berkas HTML | Berkas CSS | Berkas Data / JS |
|---|---|---|---|
| **Beranda & Slogan Web** | `index.html` | `css/pages/beranda.css` | `js/main.js` |
| **Profil Klub, Sejarah, Pengurus** | `tentang/index.html` | `css/pages/tentang.css` | `tentang/images/anggota/` |
| **Info Lomba & Festival Matsuri** | `lomba/index.html` | `css/pages/lomba.css` | `lomba/images/` |
| **Katalog Produk Toko & Konbini** | `toko/index.html` | `css/pages/toko.css` | `images/mirai/produk/` |
| **Skor Keaktifan & Presensi Anggota** | `peringkat/index.html` | `css/pages/peringkat.css` | `js/leaderboard-data.js` |
| **Modul Pembelajaran & Kuis** | `kelas/index.html`<br>`kelas/latihan.html` | `css/pages/kelas-materi.css` | `js/script.js`<br>`js/kana.js` |
| **Kamus Kana, Kanji, & Goresan** | `kamus/index.html`<br>`kamus/kanji.html` | `css/pages/kamus.css` | `data/kanji.json`<br>`js/stroke-data.js` |
| **Program Kerja (KTN, NJR, dll.)** | `kegiatan/*.html` | `css/pages/kegiatan-divisi.css` | `js/proker-slider.js` |
| **Struktur 4 Divisi Resmi** | `divisi/*.html` | `css/pages/kegiatan-divisi.css` | `js/main.js` |
| **Rekomendasi Anime/Manga/Musik** | `rekomendasi/index.html` | `css/pages/rekomendasi-motivasi.css` | `js/main.js` |
| **Kutipan Motivasi Karakter** | `kelas/motivasi.html` | `css/pages/rekomendasi-motivasi.css` | `images/mirai/karakter/` |
| **Chatbot Maskot Sora** | `sora/index.html` | `css/pages/navbar-hero-footer.css` | `js/sora.js` |

---

## 3. Tutorial Langkah-demi-Langkah Update Konten Rutin

### 3.1 Tambah Info Lomba & Acara Baru
1. Siapkan file poster lomba (format `.jpg` atau `.png`, disarankan orientasi potret/vertikal).
2. Simpan file poster ke dalam folder `lomba/images/` (contoh: `lomba/images/poster-its-2026.jpg`).
3. Buka file `lomba/index.html`, cari kontainer `<div class="lomba-grid">`.
4. Tambahkan elemen kartu lomba baru menggunakan format standar berikut:
```html
<article class="event-card" data-event-type="lomba" data-event-region="jatim">
  <!-- Wadah Poster Single / Carousel -->
  <div class="event-poster-wrapper">
    <div class="event-poster-carousel" data-event-carousel>
      <div class="event-poster-slide is-active">
        <img src="images/poster-its-2026.jpg" alt="Poster Lomba Bunkasai ITS 2026" loading="lazy">
      </div>
    </div>
  </div>

  <!-- Detail Informasi Lomba -->
  <div class="event-info-wrapper">
    <div class="event-badges">
      <span class="event-badge event-badge--cat">Kompetisi Bahasa</span>
      <span class="event-badge event-badge--region">Jawa Timur</span>
      <span class="event-badge event-badge--status">Pendaftaran Dibuka</span>
    </div>

    <h3 class="event-title">Bunkasai ITS 2026</h3>
    <p class="event-organizer">Diselenggarakan oleh HMDJ Institut Teknologi Sepuluh Nopember</p>
    <p class="event-desc">Kompetisi bergengsi tahunan cabang Olimpiade Kanji, Cerdas Cermat, Pidato Bahasa Jepang, dan Cosplay Walk.</p>

    <div class="event-meta-grid">
      <div class="event-meta-item">
        <span class="meta-label">Pelaksanaan</span>
        <span class="meta-val">15 - 16 November 2026</span>
      </div>
      <div class="event-meta-item">
        <span class="meta-label">Biaya</span>
        <span class="meta-val">Rp 35.000 / Tim</span>
      </div>
      <div class="event-meta-item">
        <span class="meta-label">Lokasi</span>
        <span class="meta-val">Kampus ITS Sukolilo, Surabaya</span>
      </div>
      <div class="event-meta-item">
        <span class="meta-label">Cabang</span>
        <span class="meta-val">Kanji, Cerdas Cermat, Cosplay</span>
      </div>
    </div>

    <div class="event-actions">
      <a href="https://www.instagram.com/mirainohana_smawh2" target="_blank" rel="noopener noreferrer" class="btn btn-primary event-btn">
        🔗 Buka Link Pendaftaran
      </a>
    </div>
  </div>
</article>
```

---

### 3.2 Update Skor & Leaderboard Peringkat
1. Buka file `js/leaderboard-data.js`.
2. Di dalam file tersebut terdapat 3 array utama:
   - `RAJIO_LEADERBOARD`: Data keaktifan siswa pada siaran mingguan Nihon Go Rajio.
   - `ATTENDANCE_LEADERBOARD`: Rekapitulasi presensi kehadiran pertemuan rutin klub.
   - `ACHIEVEMENT_DATA`: Dinding prestasi kejuaraan siswa yang mengharumkan nama sekolah.
3. Contoh menambah atau memperbarui anggota di leaderboard:
```javascript
{
  rank: 1,
  name: "Ahmad Fauzi",
  kelas: "XI-MIPA 2",
  avatar: "Ka", // Kode avatar chibi di images/mirai/icon/ (contoh: Ka, Hu, Al, Ay, Fu, dll.)
  score: 980,
  broadcasts: 14,
  favoriteRole: "Penyiar Utama",
  badge: "Bintang Rajio",
  trend: "up"
}
```
4. Simpan file `js/leaderboard-data.js`. Perubahan otomatis tampil di podium dan tabel `peringkat/index.html` tanpa perlu mengedit HTML!

---

### 3.3 Tambah Produk Toko / Konbini
1. Siapkan foto produk:
   - Jika kuliner/minuman asli: Simpan di `images/mirai/produk/` (foto persegi, objek fokus).
   - Jika atribut resmi (Haori, nametag): Siapkan foto tampak depan dan belakang berlatar putih bersih.
2. Buka `toko/index.html`, cari kontainer `.toko-grid`.
3. Tambahkan kartu produk baru:
```html
<div class="toko-card" data-category="atribut">
  <div class="toko-card-thumb">
    <!-- Jika memiliki 2 sisi foto, gunakan data-product-carousel -->
    <div class="toko-poster-carousel" data-product-carousel>
      <div class="toko-poster-slide is-active">
        <img src="../tentang/images/identitas/pin-depan.png" alt="Pin Lencana Klub" loading="lazy">
        <span class="toko-view-pill">Tampak Depan</span>
      </div>
    </div>
  </div>

  <div class="toko-card-body">
    <div class="toko-card-header">
      <span class="toko-badge-status toko-badge-status--ready">Tersedia</span>
      <span class="toko-category-label">Atribut Resmi</span>
    </div>
    
    <h3 class="toko-card-title">Pin Lencana Klub</h3>
    <div class="toko-card-specs">
      <span class="toko-spec-item">Bahan: Logam Enamel Tebal</span>
      <span class="toko-spec-item">Ukuran: Diameter 4.5 cm</span>
    </div>

    <div class="toko-card-footer">
      <div class="toko-price-box">
        <span class="toko-price-label">Harga</span>
        <span class="toko-price-val">Rp 15.000</span>
      </div>
      <button type="button" class="btn btn-primary toko-buy-btn" data-add-to-cart="Pin Lencana Klub" data-price="15000">
        + Keranjang
      </button>
    </div>
  </div>
</div>
```

---

### 3.4 Tambah Foto Dokumentasi Program Kerja
1. Kompresi foto agar ukuran berkas tidak terlalu berat (disarankan di bawah 400 KB per foto).
2. Simpan foto ke dalam folder `kegiatan/images/dokumentasi/` (contoh: `kegiatan/images/dokumentasi/ktn-2026-1.jpg`).
3. Buka file kegiatan terkait (misalnya `kegiatan/kimi-to-nippon.html`), cari slider galeri:
```html
<div class="proker-gallery-track">
  <div class="proker-gallery-item">
    <img src="images/dokumentasi/ktn-2026-1.jpg" alt="Momen Orientasi KTN 2026" loading="lazy">
  </div>
</div>
```

---

### 3.5 Update Kepengurusan Baru saat Sertijab
Setiap pergantian periode pengurus (Sertijab tahunan):
1. Siapkan foto potret masing-masing pengurus baru (rasio kotak 1:1, pose rapi berjas/berbatik/berhaori).
2. Simpan di folder `tentang/images/anggota/` dengan penomoran rapi (`1.jpg`, `2.jpg`, dst.).
3. Buka `tentang/index.html`:
   - Pada bagian **Slider Kepengurusan**: Buat slide kabinet baru (misal: "Kabinet Sakura") dengan kartu anggota berisi avatar, nama lengkap, jabatan tunggal di `.member-label`, dan moto hidup.
   - Pada bagian **Garis Waktu Sejarah (`#sejarah`)**: Tambahkan balok timeline angkatan baru yang mencatat masa bakti kepengurusan Anda beserta capaian pentingnya.
   - Pada bagian **Wall of Fame (`#prestasi`)**: Masukkan prestasi juara yang diraih selama periode kepengurusan Anda.

---

## 4. Standar Desain & Estetika Visual Wajib

Untuk menjaga marwah dan estetika website Mirai no Webu, seluruh developer wajib mematuhi standar desain berikut:

### 1. Palet Warna Pondasi Klub
- **Obsidian Dark**: `#0e0b12` dan `#111115` (Latar belakang gelap berwibawa).
- **Sakura Pink**: `#ff4f91` (Aksen utama cerah berpendar) dan `#e91e63` (Aksen berry kontras tinggi untuk teks latar putih).
- **Putih Murni**: `#ffffff` (Latar seksi terang dan kartu putih bersih).
- **Multi-color Status**: Biru (Tingkat Kota / Segar), Hijau (Tersedia / Surabaya), Oranye (Provinsi / PO), Merah (Nasional / Ditutup).

### 2. Aturan Selang-Seling Seksi (Section Alternation) & Kontras WCAG AAA
- Halaman disusun berselang-seling antara seksi **Gelap** dan seksi **Terang (Putih)** untuk menjaga kesegaran mata pembaca.
- **DILARANG KERAS Teks Menabrak Background**:
  - Di seksi putih: Gunakan warna teks abu-abu gelap slate (`#475569` / `#554857`). **Dilarang** memakai teks putih atau abu terang!
  - Di seksi gelap: Gunakan warna teks abu-abu terang (`#cbd5e1` / `#e2e8f0`). **Dilarang** memakai teks hitam pekat!

### 3. Penggunaan Pola Tradisional Wagara (1 Kartu 1 Motif)
- Kartu gelap: `images/mirai/background/c1b.jpeg` (Kumo/Awan) atau `w1b.jpeg` (Seigaiha/Ombak) dengan transparansi tipis (~4.5%).
- Kartu terang: `images/mirai/background/c1w.jpeg` atau `w1w.jpeg` dengan transparansi ~10%.
- **Dilarang menumpuk pattern ganda** dalam satu elemen kartu.

### 4. Standar Sub-Judul Jepang Murni (`.jp-kanji`)
- Sub-judul seksi dan hero wajib berupa **aksara Jepang murni (Kanji/Kana)** menggunakan Google Fonts **Noto Serif JP** berwarna pink sakura.
- Dilarang menambahkan embel-embel atau terjemahan bahasa Indonesia di samping kanji tersebut.

### 5. Penempatan Maskot Chibi (`.card-corner-chibi`)
- Maskot chibi Genshin diletakkan di pojok kanan bawah kartu sebagai pemanis visual.
- Maskot chibi tidak boleh mengorbankan keterbacaan teks dan fungsionalitas tombol.

---

## 5. Cara Menggunakan AI Assistant (Pair Programming)

Website ini sangat ramah dikembangkan bersama AI coding asisten modern (**Google Antigravity**, **Cursor**, **GitHub Copilot**, **Claude Code**, atau **ChatGPT**).

### Di Mana Konfigurasi AI Disimpan?
Seluruh konfigurasi AI disimpan rapi di folder **`panduan/ai-configs/`**:
- **`.cursorrules`**: Aturan otomatis untuk Cursor AI.
- **`copilot-instructions.md`**: Instruksi sistem untuk GitHub Copilot.
- **`panduan/agent.md`**: Buku pedoman menyeluruh aturan desain dan arsitektur kode.
- **`panduan/CONTEKAN-TAG.md`**: Peta cepat pemetaan satu pintu file HTML -> CSS -> JS.

### 3 Aturan Emas saat Memberi Instruksi ke AI:
1. **Sebutkan File Spesifik**: Jangan biarkan AI membaca seluruh folder CSS. Katakan: *"Edit css/pages/lomba.css untuk memperbaiki kartu lomba"*.
2. **Larang Menyalakan Live Server**: Instruksikan AI untuk langsung mengubah kode tanpa membuang waktu menyalakan server lokal atau mengambil screenshot browser.
3. **Gunakan Python Script untuk Perubahan Berulang**: Jika ingin memperbarui elemen yang ada di 26+ file HTML sekaligus (seperti navbar atau footer), wajib minta AI membuat dan menjalankan script Python singkat di terminal.

---

## 6. Panduan Alur Git & Deployment GitHub Pages

Setiap kali Anda selesai melakukan perubahan atau update konten, publikasikan ke internet menggunakan Git:

### Langkah-demi-Langkah Komit:
1. Buka terminal di folder proyek (`/Mirai-No-Webu`).
2. Periksa file apa saja yang telah Anda modifikasi:
   ```bash
   git status
   ```
3. Tambahkan seluruh berkas perubahan ke staging area:
   ```bash
   git add .
   ```
4. Buat komit dengan pesan yang jelas menggunakan konvensi baku:
   ```bash
   git commit -m "feat: tambah poster lomba bunkasai its 2026"
   ```
   *Gunakan awalan: `feat:` (fitur baru), `fix:` (perbaikan bug), `docs:` (dokumentasi), `style:` (perubahan tampilan).*
5. Dorong (*push*) perubahan ke GitHub:
   ```bash
   git push origin main
   ```
6. **Selesai!** GitHub Pages akan otomatis memperbarui website dalam 1–2 menit. Anda bisa langsung membuka link website resmi untuk melihat hasilnya secara online.

---

## 7. Checklist Serah-Terima Jabatan & Kontak

### Checklist Wajib Pengurus Baru Setiap Tahun:
- [ ] Mengecek masa aktif pendaftaran lomba di `lomba/index.html`.
- [ ] Memperbarui foto dan susunan kepengurusan baru di `tentang/index.html`.
- [ ] Mereset atau memperbarui rekap keaktifan di `js/leaderboard-data.js`.
- [ ] Memeriksa stok produk dan harga merchandise di `toko/index.html`.
- [ ] Menambahkan dokumentasi program kerja yang baru saja terlaksana di `kegiatan/`.
- [ ] Menjalankan script validasi link internal agar **tautan rusak selalu 0 (nol)**.

### Saluran Komunikasi & Media Sosial Resmi Klub:
- **Instagram**: [@mirainohana_smawh2](https://www.instagram.com/mirainohana_smawh2)
- **TikTok**: [@nihongo.kurabu.wh2](https://www.tiktok.com/@nihongo.kurabu.wh2)
- **Sekretariat**: SMA Wachid Hasyim 2 Taman, Sidoarjo, Jawa Timur

*Selamat berkarya dan melanjutkan estafet perjuangan klub tercinta! Ganbatte kudasai! ✨🎌*
"""

with open("panduan/PANDUAN-DEVELOPER.md", "w", encoding="utf-8") as f:
    f.write(developer_guide_content)
print("[3] panduan/PANDUAN-DEVELOPER.md berhasil dibuat")

# -------------------------------------------------------------
# 4. Perbarui panduan/tree.md
# -------------------------------------------------------------
tree_content = """# Struktur Direktori Proyek Mirai no Webu

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
│
└── images/mirai/                   # Aset Bersama (Shared Global Assets)
    ├── background/                 # Pola Wagara master CSS (w1b, w1w, c1b, c1w, w2w, chat, Sora)
    ├── logo/                       # Logo resmi klub (MNH1.png, MNH1-nav.png, NK.png, comingsoon.jpg)
    ├── icon/                       # Ikon chibi Genshin Impact (Al, Ay, Chi, Fa, Fu, Hu, Ka, Ki, Lo, dll.)
    ├── karakter/                   # Foto karakter anime kutipan (luf, ere, nar, dek, tan)
    ├── produk/                     # Foto produk konbini (oni, tak, dan, mat, teh)
    └── stiker/                     # 28 stiker komunitas ekspresi karakter anime
```
"""

with open("panduan/tree.md", "w", encoding="utf-8") as f:
    f.write(tree_content)
print("[4] panduan/tree.md berhasil diperbarui")

# -------------------------------------------------------------
# 5. Perbarui README.md agar tree-nya selaras
# -------------------------------------------------------------
with open("README.md", "r", encoding="utf-8") as f:
    readme_text = f.read()

# Update panduan/ in README.md
old_rm_panduan = """├── panduan/                        # Dokumentasi Arsitektur & Panduan AI
│   ├── tree.md                     # Peta pohon direktori komprehensif
│   └── agent.md                    # Pedoman aturan desain, fungsi, dan persona asisten"""

new_rm_panduan = """├── panduan/                        # Dokumentasi Arsitektur & Panduan AI
│   ├── PANDUAN-DEVELOPER.md        # Buku panduan serah-terima pengurus & developer klub
│   ├── CONTEKAN-TAG.md             # Acuan cepat pemetaan halaman -> CSS -> JS
│   ├── tree.md                     # Peta pohon direktori komprehensif
│   ├── agent.md                    # Pedoman aturan desain, fungsi, dan persona asisten
│   └── ai-configs/                 # Konfigurasi AI Assistant (Cursor, Copilot, dll.)"""

if old_rm_panduan in readme_text:
    readme_text = readme_text.replace(old_rm_panduan, new_rm_panduan)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_text)
    print("[5] README.md pohon panduan berhasil diselaraskan")

print("=== SELURUH DOKUMENTASI & PANDUAN BERHASIL DIPERBARUI SECARA PURNA! ===")

