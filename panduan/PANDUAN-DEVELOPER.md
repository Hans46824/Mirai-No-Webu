# 🌸 Buku Panduan Serah-Terima Pengembang & Pengurus
## Website Resmi Mirai no Webu — MIRAI NO HANA SMA Wachid Hasyim 2 Taman Sidoarjo

Selamat datang, Pengurus dan Pengembang Generasi Penerus Klub Bahasa & Kebudayaan Jepang **MIRAI NO HANA**! 🎌

Dokumen ini disusun sebagai **Buku Saku Serah-Terima Jabatan (Sertijab)** untuk memandu Anda memahami, merawat, dan mengembangkan website **Mirai no Webu**. Website ini dirancang 100% mandiri oleh siswa anggota klub sebagai ruang berkarya, wadah belajar interaktif, dan etalase kebanggaan ekstrakurikuler kita.

---

## 📑 Daftar Isi
0. [Bab 0: Persiapan Awal & Instalasi Tools (Wajib untuk Pengurus/Developer Baru)](#-bab-0-persiapan-awal--instalasi-tools-wajib-untuk-pengurusdeveloper-baru)
   - [Langkah 1: Instalasi Code Editor & Tools Dasar](#langkah-1-instalasi-code-editor--tools-dasar)
   - [Langkah 2: Instalasi AI Coding Agent di VS Code](#langkah-2-instalasi-ai-coding-agent-di-vs-code)
   - [Langkah 3: Daftar Ekstensi VS Code Wajib & Fungsinya](#langkah-3-daftar-ekstensi-vs-code-wajib--fungsinya)
   - [Langkah 4: Cara Mengatur VS Code (Settings & Extensions)](#langkah-4-cara-mengatur-vs-code-settings--extensions)
   - [Langkah 5: Cara Memakai Utility Class Universal (Anti-Rusak)](#langkah-5-cara-memakai-utility-class-universal-anti-rusak)
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

## 🎨 7 Sistem Visual & Transparansi Pattern Universal (Master Design Standard)

Seluruh pengembang dan AI asisten **WAJIB mematuhi 7 Aturan Visual Universal** ini untuk menjaga konsistensi, estetika, dan keterbacaan (WCAG AAA) di seluruh halaman Mirai no Webu:

1. **Master Variabel Pattern & Gradien Terpusat di `:root` (`css/pages/global.css`)**:
   - `--pattern-c1w: url("../../images/mirai/background/c1w.jpeg");` (Kumo/Awan Terang)
   - `--pattern-c1b: url("../../images/mirai/background/c1b.jpeg");` (Kumo/Awan Gelap)
   - `--pattern-w1w: url("../../images/mirai/background/w1w.jpeg");` (Wagara/Ombak Terang)
   - `--pattern-w1b: url("../../images/mirai/background/w1b.jpeg");` (Wagara/Ombak Gelap)
   - `--overlay-card-light: linear-gradient(135deg, rgba(255, 255, 255, 0.96), rgba(255, 252, 254, 0.96));` (Gradien penutup terang untuk watermark 4.5% kartu)
   - `--overlay-card-dark: linear-gradient(155deg, rgba(16, 12, 22, 0.96), rgba(10, 8, 14, 0.97));` (Gradien penutup gelap untuk watermark 4.5% kartu)
   - `--overlay-section-dark: linear-gradient(180deg, rgba(14, 11, 18, 0.95), rgba(14, 11, 18, 0.96));`

2. **Kunci Transparansi Watermark Sangat Lembut (Maksimal Keterbacaan Teks)**:
   - Pola Terang & Gelap: Dikunci pada **`opacity: 0.045 !important`** (hover: `0.07 !important`) dan gradien penutup master di `:root` sebesar `0.95`–`0.97` agar teks kartu sangat jernih, tajam, dan tidak terganggu oleh garis gelombang latar.

3. **Seksi Selang-Seling Bersih & Polos (Pattern HANYA pada Kartu, DILARANG pada Halaman/Seksi)**:
   - Semua `<section>` konten setelah Hero wajib memiliki latar belakang solid yang 100% bersih, polos, dan bebas dari pattern gambar latar (`background-image: none !important;`):
     - Seksi Ganjil (`nth-of-type(odd)`): Putih Bersih (`#ffffff`) polos dengan teks kontras tinggi (`#18151b` / `#554e57`).
     - Seksi Genap (`nth-of-type(even)`): Hitam Obsidian (`#111111`) polos dengan teks kontras terang (`#ffffff` / `#d5ccd3`).
   - Gunakan utility class `.mirai-section-light` dan `.mirai-section-dark` saat membuat seksi baru.

4. **Sistem Whitelist & Utility Class Kartu Resmi (Anti-Wildcard Rusak)**:
   - **DILARANG KERAS** memakai selector wildcard agresif seperti `[class*="-card"]` atau `[class*="-box"]` yang memaksa sub-elemen mewarisi border/background.
   - Gunakan utility class resmi `.mirai-card-light` dan `.mirai-card-dark` yang sudah dibekali guard `:not()` otomatis untuk seluruh elemen anak (`*-head`, `*-header`, `*-point-card`, `*-badge`, dll.).

5. **Aturan Anti-Double-Pattern pada Sub-Kartu (Inner Boxes)**:
   - Semua kotak/panel anak di dalam kartu utama (seperti `.quote-char-box`, `.quote-speech-box`, `.quote-meaning-box`, profile box, badge box, dll.) WAJIB menggunakan latar solid/glass (`background: rgba(255, 255, 255, 0.94) !important;` di kartu terang, `background: rgba(24, 19, 34, 0.90) !important;` di kartu gelap) TANPA pattern gambar (`background-image: none !important`), memastikan teks 100% bersih, jernih, dan tidak bertabrakan dengan background.

6. **Harmoni Motif Berbasis Karakter Halaman**:
   - Halaman Interaktif & Dinamis (Beranda, Kamus, Rekomendasi, Lomba, Toko): Menggunakan motif Kumo Awan (`--pattern-c1w` / `--pattern-c1b`).
   - Halaman Kurikulum & Prestasi (Kelas, Kegiatan, Peringkat, Tentang): Menggunakan motif Ombak Seigaiha (`--pattern-w1w` / `--pattern-w1b`).

7. **Standar Kontras & Aksesibilitas WCAG AAA**:
   - Di seksi terang: Heading berwarna `#18151b`, paragraf `#554e57`, aksen pink `#e91e63`.
   - Di seksi gelap: Heading berwarna `#ffffff`, paragraf `#d5ccd3`, aksen pink `#ff4f91` atau `#ff659b`.

---

## 🚀 Bab 0: Persiapan Awal & Instalasi Tools (Wajib untuk Pengurus/Developer Baru)

Selamat datang di tim pengembang **Mirai no Webu**! Bagian ini disusun khusus secara ramah pemula agar siapa pun pengurus atau anggota klub yang baru ditunjuk dapat menyiapkan perangkat komputer/laptopnya dari nol hingga siap mengedit website dengan nyaman, rapi, dan bebas error.

---

### Langkah 1: Instalasi Code Editor & Tools Dasar
Sebelum membuka proyek, pastikan Anda telah memasang 3 perangkat lunak esensial berikut:
1. **Visual Studio Code (VS Code)** *(Wajib)*:
   - Unduh gratis di situs resmi: [code.visualstudio.com](https://code.visualstudio.com/).
   - Editor kode standar industri yang sangat ringan, cepat, dan memiliki ekosistem ekstensi terlengkap.
2. **Git Version Control** *(Wajib)*:
   - Unduh di: [git-scm.com](https://git-scm.com/).
   - Digunakan untuk mencatat riwayat perubahan kode (commit) dan menyinkronkan website ke GitHub Pages.
3. **Python 3 (v3.10+)** *(Sangat Dianjurkan)*:
   - Unduh di: [python.org](https://www.python.org/).
   - **PENTING saat instalasi di Windows**: Centang opsi **"Add python.exe to PATH"** agar perintah `python` dapat dipanggil langsung dari terminal VS Code untuk menjalankan skrip automasi pengurus di folder `skrip/arsip/`.

---

### Langkah 2: Instalasi AI Coding Agent di VS Code
Website ini dirancang agar sangat mudah dikembangkan bersama asisten kecerdasan buatan (AI Pair Programming). Anda dapat memasang salah satu ekstensi AI berikut di VS Code:
- **Google Antigravity / Gemini CLI**: Asisten AI resmi berkonteks besar.
- **GitHub Copilot**: Ekstensi resmi dari GitHub (`GitHub.copilot`).
- **Cline / Claude Code**: Asisten AI agentic untuk VS Code.
- **Cursor IDE**: Editor fork VS Code dengan AI bawaan.

#### Cara Menyuapi Konteks ke AI (Context Feeding Wajib):
Setiap kali Anda memberikan instruksi baru kepada AI, **SELALU sertakan mention berkas konteks** berikut di awal percakapan:
```text
@panduan/agent.md @panduan/CONTEKAN-TAG.md
Tolong bantu saya menambahkan [sebutkan tugas Anda di sini]...
```
*Dengan menyuapi kedua file panduan ini, AI akan otomatis tahu letak CSS/JS yang tepat, mematuhi standar desain tanpa merusak layout, dan tidak akan mencoba membaca file CSS secara membabi-buta.*

---

### Langkah 3: Daftar Ekstensi VS Code Wajib & Fungsinya
Folder `.vscode/extensions.json` telah disiapkan di repositori ini. Berikut 9 ekstensi resmi yang wajib Anda pasang beserta fungsinya:

| Nama Ekstensi | Identifier | Fungsi Utama |
| :--- | :--- | :--- |
| **Prettier - Code formatter** | `esbenp.prettier-vscode` | Merapikan baris & indentasi HTML/CSS/JS secara otomatis setiap kali menekan `Ctrl + S`. |
| **Live Server** | `ritwickdey.LiveServer` | Menjalankan preview website di browser lokal dengan 1 klik ("Go Live" di status bar kanan bawah). |
| **Code Spell Checker** | `streetsidesoftware.code-spell-checker` | Mencegah salah ketik (typo) teks dan variabel kode, terhubung ke kamus proyek `cspell.json`. |
| **Python** | `ms-python.python` | Menjalankan skrip automasi pemeliharaan web di folder `skrip/arsip/` langsung dari editor. |
| **Auto Rename Tag** | `formulahendry.auto-rename-tag` | Otomatis mengubah tag penutup saat tag pembuka HTML diedit, mencegah bug tag tak seimbang. |
| **HTML CSS Support** | `ecmel.vscode-html-css` | Menampilkan rekomendasi nama class CSS saat mengetik di berkas HTML secara otomatis. |
| **Path Intellisense** | `christian-kohler.path-intellisense` | Membantu autocomplete path gambar atau file (misal `../../images/...`) tanpa takut salah ketik. |
| **Color Highlight** | `naumovs.color-highlight` | Menampilkan kotak warna visual langsung pada kode warna hex/RGBA di stylesheet CSS. |
| **VS Code Pets** | `tonybaloney.vscode-pets` | Menghadirkan hewan peliharaan animasi kecil lucu di panel editor untuk menemani Anda ngoding! 🐱🐶 |

---

### Langkah 4: Cara Mengatur VS Code (Settings & Extensions)
Proyek ini telah dilengkapi pengaturan otomatis di dalam folder `.vscode/`:
1. Buka folder proyek `Mirai-No-Webu` di VS Code (`File > Open Folder...`).
2. Buka tab Ekstensi (`Ctrl + Shift + X`), ketik `@recommended` di kolom pencarian atas.
3. Klik tombol **"Install Workspace Recommended Extensions"** untuk memasang seluruh paket ekstensi dalam 1 klik.
4. Berkas `.vscode/settings.json` telah otomatis mengunci:
   - `editor.formatOnSave: true` (merapikan kode otomatis saat simpan).
   - `editor.tabSize: 2` (standar spasi 2 karakter yang rapi).
   - Menyembunyikan folder besar seperti `.git`, `__pycache__`, dan berkas vektor besar `stroke-data.js` dari pencarian agar VS Code berjalan **sangat cepat dan ringan**.

---

### Langkah 5: Cara Memakai Utility Class Universal (Anti-Rusak)
Untuk memastikan siapa pun pengurus baru yang menambah konten tidak akan merusak layout atau membuat selector wildcard yang bentrok, gunakan **Utility Classes Resmi** yang sudah disediakan di `css/pages/global.css`:

1. **Membuat Seksi Halaman Baru**:
   - Seksi Tema Terang: `<section class="section mirai-section-light">`
   - Seksi Tema Gelap: `<section class="section mirai-section-dark">`
2. **Membuat Kartu Konten Baru**:
   - Kartu Cerah Berpola Halus:
     ```html
     <div class="mirai-card-light">
       <h3>Judul Kartu</h3>
       <p>Deskripsi konten kartu...</p>
     </div>
     ```
   - Kartu Gelap Berpola Halus:
     ```html
     <div class="mirai-card-dark">
       <h3>Judul Kartu</h3>
       <p>Deskripsi konten kartu...</p>
     </div>
     ```
3. **Mengapa Wajib Menggunakan Class Ini?**
   - Kartu otomatis memiliki sudut melengkung 18px, border beraksen pink lembut, dan watermark pattern halus (4.5% opacity).
   - Sudah terpasang **guard anti-double pattern**: elemen di dalam kartu (judul, header, icon, badge) diproteksi secara otomatis agar tidak memiliki kotak border ganda atau latar bertumpuk.

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
| **Kamus Kana, Kanji, & Goresan** | `kamus/index.html`<br>`kamus/kanji.html` | `css/pages/kamus.css` | `data/kanji-index.json`<br>`data/kanji/*.json`<br>`data/strokes/*.json` |
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
