<!-- cspell:disable -->
# Panduan Utama & Aturan Kerja Mirai No Webu

Dokumen ini adalah pegangan resmi bagi pengembang dan AI asisten untuk merawat, memperbarui, serta mengembangkan website **Mirai no Webu** (Klub Bahasa & Kebudayaan Jepang MIRAI NO HANA SMASYIMDUTA Sidoarjo). 

Gunakan bahasa yang sederhana, manusiawi, dan langsung ke intinya. Hindari penulisan kode rumit di dokumen ini supaya nyaman dibaca oleh siapa pun.

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

## 1. Protokol Eksekusi Cepat (Fast-Execution Protocol)

Setiap AI asisten atau pengembang yang bekerja pada repositori ini **WAJIB mematuhi 4 aturan inti eksekusi cepat** berikut tanpa kecuali:

### 1. Peta CSS Halaman Intuitif (DILARANG Membaca style.css Utuh)
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
  - **`css/pages/toko.css`**: Toko Resmi & Konbini (`toko/index.html`), etalase 12 produk atribut & F&B, Shopee-style thumb 185px, carousel geser Haori & KTA, drawer keranjang belanja, dan panduan PO.

### 2. Peta JavaScript (`js/`)
Akses logika interaktif langsung ke berkas terkait tanpa membaca seluruh folder:
- **Logika UI global & navigasi**: `js/main.js` (header scroll, hero motion, launcher) dan `js/script.js` (master interaksi kuis, kartu, & efek global).
- **Chatbot Sora & Studio Bahasa**: `js/sora.js` (logika chatbot offline & UI), `js/api.js` (endpoint data), `js/translator.js` (mesin bantu terjemahan & generator nama/KTA), dan `js/quiz-divisi.js` (kuis kepribadian tes kecocokan divisi).
- **Kamus, Kana, Kanji & Goresan**: `js/kana.js` (kartu & audio pelafalan), `js/kanji.js` (ensiklopedia & filter kanji), `js/kanji-data.js` (dataset 2.211 Joyo Kanji), dan `js/stroke.js` (animasi kanvas goresan). Catatan: `js/stroke-data.js` berisi vektor koordinat garis besar dan dikecualikan dari pemindaian.
- **Slider & Carousel**: `js/carousel.js` (carousel umum & produk) dan `js/proker-slider.js` (slider khusus proker kegiatan).

### 3. Larangan Menyalakan Server & Screenshot Otomatis
- **DILARANG KERAS** menyalakan/merestart HTTP server lokal (`python3 -m http.server`, live-server, dll.) atau mengambil screenshot otomatis via browser/tool kecuali diminta secara eksplisit oleh user.
- Fokus langsung pada eksekusi cepat kode dan pembaruan dokumentasi.

### 4. Eksekusi Batch HTML Berulang Wajib Skrip Python Terminal
- Jika diminta mengubah elemen HTML yang berulang di banyak halaman (seperti navbar, sidebar, hero, atau footer di 26+ file HTML), **WAJIB menggunakan satu script Python singkat via terminal**.
- **DILARANG KERAS** mengedit file HTML satu per satu secara manual dengan tool pengedit teks yang lambat dan membebani konteks percakapan.

---

## 2. Aturan Wajib: Pembaruan Mandiri Dokumentasi
- Setiap kali ada halaman baru, file script baru, atau aset gambar baru yang diunggah ke proyek, AI WAJIB langsung memperbarui dokumen **agent.md** dan **tree.md**.
- Jangan hanya mengubah kode web tanpa mencatat perubahannya di dokumentasi. Struktur direktori dan aturan desain harus selalu selaras dengan kondisi web terkini.

### A. Arsitektur Folder Modular (Clean Root Standard)
Seluruh berkas website Mirai no Webu dikelompokkan secara terstruktur ke dalam folder tematik:
- **Root (`/`)**: Berisi **index.html** (gerbang utama Beranda), **404.html** (halaman penanganan error ramah pengunjung bertema Mirai no Hana), **README.md** (etalase profil repositori GitHub dan dokumentasi kredit), **cspell.json** (konfigurasi spell checker bilingual), dan folder **`.vscode/`** (`settings.json` konfigurasi workspace, `extensions.json` rekomendasi ekstensi resmi).
- **`css/`**: Berisi master stylesheet antarmuka (`css/style.css`) yang memanggil 11 berkas CSS berbasis halaman di sub-folder `css/pages/` (`global.css`, `navbar-hero-footer.css`, `beranda.css`, `kelas-materi.css`, `kamus.css`, `kegiatan-divisi.css`, `tentang.css`, `rekomendasi-motivasi.css`, `peringkat.css`, `lomba.css`, `toko.css`).
- **`js/`**: Berisi seluruh logika JavaScript modular (`main.js`, `script.js`, `kanji.js`, `kana.js`, `stroke.js`, `stroke-data.js`, `sora.js`, dll.).
- **`panduan/`**: Berisi dokumentasi arsitektur proyek (`panduan/tree.md`, `panduan/agent.md`, `panduan/CONTEKAN-TAG.md`, `panduan/PANDUAN-DEVELOPER.md`, dan folder konfigurasi AI `panduan/ai-configs/`).
- **`data/`**: Berisi basis data lokal JSON (`kana.json`, `kanji.json`, `kanji-meta.json`) yang menyuplai data untuk Kamus dan Latihan Kana/Kanji.
- **`tentang/`**: Profil lengkap klub Mirai No Hana (`index.html`).
- **`lomba/`**: Informasi 18 lomba & festival jejepangan (`index.html`).
- **`peringkat/`**: Papan peringkat keaktifan, presensi, & galeri prestasi (`index.html`).
- **`rekomendasi/`**: Rekomendasi media belajar anime, film, dan musik (`index.html`).
- **`kelas/`**: Hub pembelajaran mandiri (`index.html`, `latihan.html`, `motivasi.html`, dan folder PDF `kurikulum/`). Modul materi kelas dasar, kelas lanjutan, serta dokumen kurikulum & tata cara pengajaran kini terpadu langsung di `index.html`.
- **`divisi/`**: Struktur 4 divisi resmi klub (`index.html`, `bahasa.html`, `cosplay.html`, `desain.html`, `kewirausahaan.html`).
- **`kegiatan/`**: Hub program kerja & fasilitas (`index.html`), `kimi-to-nippon.html` (orientasi KTN), `nihon-go-rajio.html` (siaran NJR), `konbini.html`, `ramadhan.html`, dan `tomodachi.html`.
- **`toko/`**: Toko resmi klub & stan Mirai no Konbini (`index.html`) untuk atribut Haori, cinderamata kreatif, kuliner Jepang, simulasi keranjang belanja melayang, dan pemesanan via Google Form.
- **`kamus/`**: Kamus interaktif pencarian Kana & Kanji (`index.html`) dan Ensiklopedia Kanji (`kanji.html`).
- **`materi/`**: Modul pembelajaran terperinci (`materi/dasar/` dan `materi/lanjutan/`).
- **`sora/`**: Playground bot obrolan maskot Sora (`index.html`).
- **`skrip/`**: Kumpulan skrip otomasi & pemeliharaan kode Python, serta sub-folder `skrip/arsip/` untuk menyimpan arsip skrip sekali-pakai.
- **Folder `video/` telah dihapus** agar repositori bersih dari berkas rekaman lokal yang tidak terpakai.

### B. Aturan Wajib: Pembaruan Mandiri Sumber Daya & Kredit (Sources & Credits)
- Setiap kali pengembang atau AI asisten mengintegrasikan API eksternal baru, menambahkan dependensi baru, menyematkan dataset, atau menggunakan aset eksternal (font, library, icon):
  - **WAJIB langsung memperbarui tabel "Sources & Credits" di berkas `README.md`** di root repositori.
  - Catat nama penyedia, jenis lisensi, dan fungsi komponen tersebut pada website agar rekam jejak hak cipta dan atribusi selalu akurat dan teratur (*always up-to-date*).

### C. Standar Penamaan Berkas & Aset (URL-Safe Filenames)
- Seluruh penamaan file dan folder baru **WAJIB menggunakan huruf kecil (*lowercase*) dan tanda hubung (*kebab-case*)**, contoh: `idc-front.jpeg`, `kimi-to-nippon.html`.
- **Dilarang keras menggunakan spasi pada nama file atau folder** karena akan dikonversi menjadi `%20` oleh peramban dan rawan menimbulkan tautan rusak (*broken link*) pada server web.

### D. Protokol Nol Tautan Rusak (Zero Broken Links Rule)
- Setiap kali pengembang atau AI asisten memindahkan file, mengganti nama file, atau menyunting tautan navigasi:
  - **WAJIB menjalankan skrip validasi tautan Python sebelum commit** untuk memindai seluruh berkas HTML dan memastikan jumlah tautan rusak adalah **0 (nol)**.
  - Dilarang membuat commit jika masih ditemukan broken link internal.

### E. Prinsip Proaktif Pengembangan Ide Mentah & Copywriting Orisinal (Proactive Idea Refinement & Anti-Plagiarism Rule)
- **Mandat Proaktif AI sebagai Partner Kreatif**:
  - AI asisten **wajib proaktif mengolah, menyempurnakan, dan mengembangkan ide mentah pengguna** menjadi solusi yang matang, elegan, dan berkelas, tanpa sekadar menjiplak draf kasar.
- **Copywriting Orisinal & Anti-Plagiarisme (Tone of Voice Eksklusif Mirai No Webu)**:
  - Dilarang meniru mentah-mentah (*copy-paste*) struktur kalimat dari website eksternal (seperti web Tengoku).
  - Teks deskripsi, legalitas, narasi kegiatan, dan penamaan wajib disusun ulang secara orisinal dengan gaya bahasa yang santun, profesional, bangga, dan mencerminkan prestise **Klub Bahasa & Kebudayaan Jepang MIRAI NO HANA SMA Wachid Hasyim 2 Taman Sidoarjo**.
- **Standar Narasi Independensi & Hak Cipta**:
  - **Klarifikasi Independensi Klub (Sidebar Footer)**: Menghindari kata-kata kaku/defensif (seperti "tidak ada campur tangan pihak sekolah"), digantikan dengan narasi berwibawa: *Situs web ini dirancang dan dikembangkan secara independen oleh kepengurusan siswa Klub Jepang MIRAI NO HANA sebagai sarana belajar bahasa Jepang, informasi kegiatan klub, dan fasilitas digital anggota.*
  - **Disclaimer & Atribusi (Global Footer)**: Menggunakan standar *educational fair-use*: *Seluruh karya seni visual, materi budaya, dan karakter dalam situs ini merupakan hak cipta dari masing-masing kreator aslinya. Website ini dihadirkan murni sebagai media pembelajaran kreatif non-komersial bagi anggota dan sahabat pecinta bahasa Jepang.*
  - **Copyright Bottom Bar**: Diseragamkan menjadi: *© 2026 MIRAI NO HANA — SMA Wachid Hasyim 2 Taman | Kabinet Sora | Ditenagai oleh GitHub Pages*.

---

## 3. Inventaris Sumber Daya Gambar & Berkas (Colocation & Shared)

Aset visual dikelompokkan berdasarkan halaman yang menggunakannya:

### A. Aset Bersama / Global (Folder images/mirai/)
- **background/**: Pola Wagara master CSS (`w1b.jpeg`, `w1w.jpeg`, `c1b.jpeg`, `c1w.jpeg`, `w2w.jpeg`, `chat.jpeg`, `Sora.png`).
- **logo/**: Logo resmi klub (`MNH1.png`, `MNH1-nav.png`, `NK.png`, `comingsoon.jpg`).
- **icon/**: Koleksi 20 stiker chibi resmi Genshin Impact untuk profil anggota, papan peringkat, dan dekorasi kartu modul (Al, Ay, Chi, Fa, Fli, Fu, Hu, Ka, Ki, Lo, Wa, ang, bal, bul, chi, cil, dil, nah, sar, zho).
- **karakter/**: Foto potret karakter anime untuk kartu kutipan motivasi (`luf.jpeg`, `ere.jpeg`, `nar.jpeg`, `dek.jpeg`, `tan.jpeg`).
- **produk/**: Foto produk kuliner & minuman asli Mirai no Konbini (`oni.jpeg`, `tak.jpeg`, `dan.jpeg`, `mat.jpeg`, `teh.jpeg`).
- **stiker/**: Berisi 28 stiker komunitas ekspresi anime untuk asisten Sora dan materi pendukung.

### B. Aset Spesifik per Halaman (Co-located Assets)
- **tentang/images/**:
  - **anggota/**: Berisi 8 dokumentasi foto anggota kepengurusan (1.jpg sampai 8.jpg).
  - **identitas/**: Busana Haori resmi (depan & belakang), jubah Happi, kartu tanda anggota (IDC depan & belakang), lanyard, pin lencana, dan nametag Katakana.
- **lomba/images/**:
  - Poster resmi kompetisi & matsuri (ITS 1 & 2, UNAIR, UNESA 1 & 2).
- **kegiatan/images/**:
  - Logo resmi program kerja (`KTN.png`, `NGR.png`, `Mirainokonbini.png`, `Ramadhan.jpeg`, `Miraimatsuri.png`).
  - **dokumentasi/**: Foto lanskap dan potret kegiatan klub.
- **sora/images/**:
  - Banner etalase profil Asora Aokita (`soracarousel.png`) dan avatar obrolan (`sorachat.jpeg`).
- **kelas/kurikulum/**:
  - Berkas silabus kurikulum pembelajaran dan panduan mengajar resmi klub (PDF).

---

## 4. Aturan Desain & Tampilan Visual

### A. Konsep Selang-Seling Hitam dan Putih (Universal Section Alternation)
- Seluruh halaman web (Beranda, Tentang, Program & Fasilitas, serta Toko) menggunakan sistem seksi warna selang-seling antara hitam (#0e0b12 atau #111115) dan putih murni (#ffffff).
- Tujuannya menjaga ritme membaca pengunjung agar mata tidak cepat lelah saat menggulir halaman panjang.
- **Seksi Hitam / Gelap**:
  - Warna latar belakang solid `#0e0b12` atau `#111115` selebar 100% layar (*full width*).
  - Teks judul putih bersih `#ffffff` dipadukan aksen pink sakura `<span>...</span>`.
  - Teks deskripsi menggunakan abu-abu lembut (`#cbd5e1` atau `#94a3b8`) agar kontrasnya nyaman di mata.
  - Kartu komponen menggunakan permukaan gelap gradasi (`linear-gradient(160deg, #1a1424, #120e19)`) dengan pola gelap (`c1b.jpeg` atau `w1b.jpeg`) transparansi 4.5% (`mix-blend-mode: screen`).
- **Seksi Putih / Terang**:
  - Warna latar belakang putih murni solid `#ffffff` selebar 100% layar (*full width*).
  - Teks judul menggunakan warna hitam pekat `#18151b` dipadukan aksen pink sakura `<span>...</span>`.
  - Teks deskripsi dan paragraf menggunakan abu gelap pekat (`#554857` atau `#475569`) dengan standar kontras tinggi WCAG AAA.
  - Kartu komponen menggunakan permukaan putih bersih (`#ffffff`) dengan border pink pastel (`#ffccd9` / `#ebd0dc`) dan pola terang (`c1w.jpeg` atau `w1w.jpeg`) transparansi 10% (`mix-blend-mode: multiply`).
- **Perlindungan Lebar Penuh (Anti-Bleed Background Rule)**: Setiap seksi wajib membentang penuh 100% lebar layar (`width: 100%`), sedangkan isi konten di dalamnya dibatasi dalam kontainer tengah (`max-width: 1200px` - `1240px; margin: 0 auto;`), sehingga tidak terjadi kebocoran latar belakang (*background bleed*) di layar monitor lebar.

### B. Aturan Latar Belakang Judul Hero & Standar Sub-Judul Jepang (Pill Kanji)
- **Aturan Hero Ber-Background (Background Judul)**:
  - Pada area hero yang memiliki gambar latar belakang (ilustrasi maskot Sora, wagara, atau latar tematik):
    - **HANYA BOLEH menampilkan sub-judul (bahasa Jepang murni dari kata judul halaman tersebut) dan judul utama (`<h1>`), TANPA deskripsi**.
    - **Deskripsi Dihilangkan**: Dilarang menampilkan paragraf deskripsi (`.page-hero-desc` / `.hero-desc`) di area hero ber-background. Hal ini bertujuan agar tampilan visual ilustrasi Sora dan judul halaman tampak megah, bersih, lapang, dan tidak tertutup tumpukan teks panjang.
    - **Sub-judul HANYA Bahasa Jepang Murni**: Sub-judul berupa terjemahan/istilah asli bahasa Jepang dari kata judul halaman tersebut yang dibungkus tag `<span class="jp-kanji">...</span>` (contoh: `<p class="page-hero-eyebrow"><span class="jp-kanji">公式ショップ</span></p>`). Dilarang menambahkan embel-embel teks bahasa Indonesia di sampingnya.
- **Standar Sub-Judul Jepang Menyeluruh (Pill Kanji: Wajib Pink, Lebih Besar, & Seragam Noto Serif JP)**:
  - **1. Konsistensi Warna Pink Seluruh Sub-Judul**: Seluruh sub-judul Jepang pada header hero maupun sub-judul seksi (`.jp-kanji`) **WAJIB menggunakan teks warna pink sakura yang seragam**, bukan teks putih atau hitam:
    - **Di Latar Gelap / Hero Banner**: Teks berwarna pink sakura cerah berpendar (`color: #ff659b !important; text-shadow: 0 0 10px rgba(255, 101, 155, 0.45);`) dengan latar pill transparan anggun (`background: rgba(255, 79, 145, 0.18); border: 1.5px solid rgba(255, 101, 155, 0.45);`).
    - **Di Latar Terang / Putih**: Teks berwarna pink tua berry tegas (`color: #e91e63 !important;`) dengan kontras tinggi standar WCAG AAA di atas latar putih (`background: rgba(233, 30, 99, 0.08); border: 1.5px solid rgba(233, 30, 99, 0.28);`).
  - **2. Ukuran Lebih Besar & Proporsional Agar Guratan Kanji Jelas**:
    - Guratan aksara Kanji yang kompleks membutuhkan ukuran yang cukup agar tidak tampak rapat atau buram:
      - **Mode Laptop / Desktop**: `14.5px - 15px` (`font-weight: 700; padding: 5px 15px; border-radius: 99px;`).
      - **Mode HP (Mobile)**: `13px` (`font-weight: 700; padding: 3.5px 12px; border-radius: 99px;`).
  - **3. Keseragaman Font Jepang Murni (100% Noto Serif JP)**:
    - Dilarang keras membiarkan halaman merender font sistem bawaan (*system fallback*) yang membuat aksara kanji berbeda-beda bentuknya di tiap komputer/perangkat.
    - Seluruh berkas HTML proyek wajib menyematkan tautan Google Fonts resmi (`Noto Serif JP` & `Plus Jakarta Sans`).
    - Stylesheet master `css/style.css` menyertakan `@import` font di baris teratas sebagai jaminan ganda (*fail-safe*) bahwa seluruh sub-judul Jepang di seluruh halaman terjamin 100% menggunakan font yang sama persis.
- **Ikon Media Sosial Resmi di Hero (`.hero-social-sidebar`)**:
  - Setiap background hero yang memiliki judul teks halaman **WAJIB menyematkan sidebar ikon media sosial vertikal** berisi tautan Instagram resmi (`@mirainohana_smawh2`) dan TikTok resmi (`@nihongo.kurabu.wh2`).
  - **Peletakan Presisi Identik dengan Beranda**: Posisi tombol media sosial ini dikunci pada sisi kanan bawah hero (`position: absolute; bottom: 15%; right: 5%;` di desktop, `bottom: 12%; right: 6%;` di mobile) di samping karakter maskot Sora, persis seperti tata letak foto Beranda.
  - Tombol medsos hero secara otomatis disembunyikan halus ketika panel navigasi samping (sidebar menu), modal dialog, latihan interaktif, atau lightbox gambar aktif.
- **Sub-Judul Khusus Hero Beranda (`.hero-yokoso-kanji`)**:
  - Khusus pada Beranda (`index.html`), sub-judul hero tidak menggunakan badge pill pink nama klub, melainkan secara spesifik menggunakan kata sambutan **"ようこそ"** (Yokoso) berukuran besar (`clamp(26px, 3.8vw, 44px)`), berbobot tebal (`font-weight: 800`), font aksara Jepang murni (`Noto Serif JP`), dan berwarna **putih bersih `#ffffff`** dengan bayangan pendaran lembut.
  - Tampilan ini sengaja dibuat berbeda dari halaman lain sebagai ucapan selamat datang utama yang megah dan berwibawa di atas judul `MIRAI NO WEBU`.
- **Arsitektur Sticky Curtain Reveal**:
  - Hero menerapkan `position: sticky; top: 0; z-index: 1; min-height: 59svh; display: flex; align-items: flex-end;`.
  - Gambar latar Sora menetap diam di layar saat halaman digulir (*parallax-free clean anchor*).
  - Seksi pertama di bawah hero (`.page-hero + section`) wajib memiliki elevasi bayangan tebal meluncur naik (`box-shadow: 0 -35px 85px rgba(0, 0, 0, 0.98); z-index: 12; position: relative;`) berlatar solid untuk menutup / "memakan" hero secara fisik dan mulus saat digulir.
  - Dilarang keras menimpa `.page-hero` dengan warna radial gradient kusam atau background solid lokal yang menghilangkan karakter Sora.

### C. Aturan Pola Background (Pattern) & Selang-Seling Tiap Halaman Menu
- **Aturan Selang-Seling 9 Halaman Menu Utama**: Motif pola pada tiap kartu diatur berselang-seling mengikuti urutan menu navigasi dari awal sampai akhir:
  1. **Beranda**: Menggunakan Pola Awan Kumo — **c1b.jpeg** (kartu seksi gelap) & **c1w.jpeg** (kartu seksi terang).
  2. **Kelas & Kurikulum**: Menggunakan Pola Ombak Wagara Seigaiha — **w1b.jpeg** (kartu seksi gelap) & **w1w.jpeg** (kartu seksi terang).
  3. **Kamus**: Menggunakan Pola Awan Kumo — **c1b.jpeg** (kartu seksi gelap) & **c1w.jpeg** (kartu seksi terang).
  4. **Program & Fasilitas**: Menggunakan Pola Ombak Wagara Seigaiha — **w1b.jpeg** (kartu divisi & seksi fasilitas kelas/gelap) & **w1w.jpeg** (kartu program kerja/terang).
  5. **Toko**: Menggunakan Pola Awan Kumo — **c1b.jpeg** (kartu seksi gelap) & **c1w.jpeg** (kartu seksi terang).
  6. **Rekomendasi**: Menggunakan Pola Awan Kumo — **c1b.jpeg** (kartu seksi gelap) & **c1w.jpeg** (kartu seksi terang).
  7. **Papan Peringkat**: Menggunakan Pola Ombak Wagara Seigaiha — **w1b.jpeg** (kartu podium & tabel gelap) & **w1w.jpeg** (kartu terang).
  8. **Lomba & Acara**: Menggunakan Pola Awan Kumo — **c1b.jpeg** (kartu acara gelap) & **c1w.jpeg** (kartu detail terang).
  9. **Tentang**: Menggunakan Pola Ombak Wagara Seigaiha — **w1b.jpeg** (kartu seksi gelap) & **w1w.jpeg** (kartu seksi terang).
- **Aturan Mutlak Anti-Tumpuk**: Hanya boleh ada 1 pola pattern dalam satu kartu. Dilarang keras menumpuk pattern di dalam kartu yang sudah memiliki pattern karena motifnya akan saling bertabrakan dan terlihat kotor.
- **Tingkat Transparansi Wajib Tipis & Halus (Agar Teks Tetap Jelas)**:
  - Kartu Gelap (c1b / w1b): Transparansi sekitar 4.5% (opacity: 0.045, mix-blend-mode: screen). Saat disorot mouse (hover) naik halus ke 8% (opacity: 0.08).
  - Kartu Terang (c1w / w1w): Transparansi sekitar 10% (opacity: 0.10, mix-blend-mode: multiply). Saat disorot mouse naik ke 16% (opacity: 0.16).

### D. Penggunaan Ikon Chibi: Jangan Sampai Mendominasi & Konsistensi Kartu Kelas
- Ikon chibi diletakkan di sudut kartu (.card-corner-chibi) atau avatar peringkat sebagai aksen pemanis desain saja.
- Ikon chibi **TIDAK BOLEH mendominasi tampilan kartu**.
- Tidak masalah jika stiker atau elemen lain menimpa bagian chibi. Yang paling utama adalah **isi teks dan fungsi web**.
- Jangan pernah mengorbankan keterbacaan materi atau tatanan tata letak hanya demi memperlihatkan gambar chibi.
- **Konsistensi Ikon Chibi pada Seluruh Kartu Pembelajaran & Dokumen Hub Kelas (`kelas/index.html`)**:
  - Untuk menjaga keharmonisan dan konsistensi visual di halaman Kelas (`kelas/index.html`), seluruh kartu modul dan kartu dokumen wajib dilengkapi stiker maskot chibi Genshin Impact di sudut kanan bawah (`.card-corner-chibi`):
    - **Kelas Dasar**: Hu Tao (`Hu.png`), Kazuha (`Ka.png`), Faruzan (`Fa.png`), Freminet (`Fli.png`).
    - **Kelas Lanjutan**: Chiori (`Chi.png`), Wanderer (`Wa.png`).
    - **Kurikulum Pembelajaran**: Alhaitham (`Al.png` — cendekiawan analitis yang selaras dengan acuan kurikulum & silabus materi).
    - **Tata Cara Mengajar**: Furina (`Fu.png` — sosok pemandu & instruktur ekspresif yang serasi untuk panduan pengajaran tutor).
- **Prinsip Desain Kartu Dokumen: Mode HP (Mobile-First) Utama & Mode Laptop Presentasi**:
  - **Prioritas Utama Mode HP (Smartphone-First)**:
    - Mayoritas pengunjung mengakses web via ponsel cerdas (*handphone*), sehingga kenyamanan genggaman layar sentuh menjadi prioritas nomor satu.
    - **Bebas Blok Kaku 100%**: Dilarang membuat tombol aksi kartu dokumen berjejer vertikal selebar 100% kartu yang membuat kartu terlalu tinggi dan menabrak maskot chibi.
    - **Tombol Ringkas Berdampingan (Side-by-Side Ergonomics)**: Tombol aksi primer ("Unduh PDF") dan sekunder ("Buka") ditata berdampingan dengan pembatas lebar aman (`max-width: calc(100% - 70px)`). Hal ini memastikan tombol mudah dijangkau sentuhan jempol dan maskot chibi di pojok kanan bawah memiliki ruang lega tanpa tumpang tindih.
    - **Label Responsif Adaptif**: Pada mode HP gunakan label ringkas (`.doc-btn-label-short` contoh: "Buka"), sedangkan pada layar desktop laptop tampil penuh (`.doc-btn-label-full` contoh: "Buka Dokumen").
    - **Lencana Aksara Kanji Sejajar**: Bagian header kartu dokumen dilengkapi lencana kanji tematik (`教本` untuk Kurikulum, `指導` untuk Tata Cara Mengajar) dengan `white-space: nowrap` agar konsisten dengan kartu modul di atasnya dan tidak terpecah baris di layar sempit.
    - **Permukaan Kartu Menyatu (Seamless Texture)**: Hindari penggunaan kotak footer putih kaku terpisah. Permukaan kartu menyatu utuh dengan tekstur pola ombak Wagara Seigaiha (`w1w.jpeg` / `w1b.jpeg`) bergradasi lembut.
  - **Kerapian Mode Laptop (Presentation-Ready Standard)**:
    - Pada layar laptop/desktop, kartu tampil proporsional dalam grid 2 kolom simetris dengan jarak lapang, tipografi seimbang, dan efek interaksi hover halus (`translateY(-5px) scale(1.08) rotate(-3deg)` pada chibi) yang rapi, mewah, dan siap dipresentasikan di hadapan guru pembina maupun anggota klub.

### E. Skema Warna Web (Pink, Putih, Hitam + Multi-Color)
- Warna pondasi klub: Pink sakura (#ff4f91 dan #e91e63), putih (#ffffff), dan hitam gelap (#09090d / #111115).
- Warna aksen (multi-color) wajib digunakan pada lencana, label tingkat, dan status agar tampilan tidak monoton:
  - Biru (#38bdf8 / #0284c7): Tingkat Sidoarjo, Jawa Timur, status Segar & Hangat kuliner, dan informasi teknis.
  - Hijau (#10b981 / #34d399): Tingkat Surabaya, status Tersedia produk, status pendaftaran buka, presensi hadir.
  - Oranye / Emas (#f97316 / #f59e0b): Tingkat provinsi, status Pra-Pesan (PO), juara perunggu dan emas, status perhatian.
  - Merah (#f43f5e / #e11d48): Tingkat nasional, status pendaftaran ditutup, batas akhir waktu.
  - Ungu (#a855f7 / #c084fc): Kategori acara festival cosplay dan ruang maskot Sora.

### F. Sistem Tipografi Judul Tiga Lapis pada Seluruh Seksi Halaman (Three-Tier Japanese Header System)
- **Hierarki Wajib Tiga Lapis pada Setiap Judul Seksi Halaman**:
  Seluruh seksi konten di Mirai no Webu (termasuk Kelas, Tentang, Program, Fasilitas, Toko, Lomba, Peringkat, Rekomendasi, Kamus, Divisi, dan Beranda) **WAJIB menerapkan sistem tiga lapis**:
  1. **Lapisan 1 — Sub-judul / Kicker Bahasa Jepang Murni di Atas Judul (`.section-eyebrow`)**:
     - Terletak tepat di atas judul seksi.
     - **HANYA memuat aksara Jepang murni (Kanji / Katakana / Hiragana)** dari kata kunci judul seksi tersebut dalam tag `<span class="jp-kanji">...</span>`.
     - **Dilarang keras menambahkan teks bahasa Indonesia di sampingnya** (tanpa embel-embel atau label bahasa Indonesia).
  2. **Lapisan 2 — Judul Seksi Heading Tebal (`.heading` / `<h2>`)**:
     - Tipografi tegas, berbobot tebal (`font-weight: 800 - 900`).
     - Menggunakan gaya Two-Tone: Warna solid teks dipadukan aksen pink sakura di dalam tag `<span>`.
  3. **Lapisan 3 — Deskripsi Singkat Elegan di Bawah Judul (`.section-desc`)**:
     - Terletak tepat di bawah judul seksi dengan panjang 1–2 kalimat ringkas, padat, dan informatif.
     - Menerangkan maksud dan isi konten dari seksi tersebut secara jelas dan mudah dipahami.
- **Daftar Baku Sub-Judul Jepang Murni untuk Halaman & Seksi**:
  - **Beranda**: Hero: `<span class="jp-kanji hero-yokoso-kanji">ようこそ</span>` (Besar & Putih Bersih) | Apa itu Web: `<span class="jp-kanji">ウェブについて</span>` | Belajar Digital: `<span class="jp-kanji">デジタル学習</span>` | Lainnya: `<span class="jp-kanji">その他の活動</span>`
  - **Kelas & Kurikulum**: Hero: `<span class="jp-kanji">クラス＆カリキュラム</span>` | Kelas Dasar: `<span class="jp-kanji">基礎クラス</span>` | Kelas Lanjutan: `<span class="jp-kanji">上級クラス</span>` | Kurikulum: `<span class="jp-kanji">カリキュラムと指導法</span>`
  - **Tentang Klub**: Hero: `<span class="jp-kanji">日本語クラブについて</span>` | Profil: `<span class="jp-kanji">クラブ概要</span>` | Bendera: `<span class="jp-kanji">公式旗</span>` | Nama: `<span class="jp-kanji">名前の由来</span>` | Logo NK: `<span class="jp-kanji">ロゴの意味</span>` | Slogan: `<span class="jp-kanji">合言葉</span>` | Visi & Misi: `<span class="jp-kanji">ビジョン＆ミッション</span>` | Sejarah: `<span class="jp-kanji">クラブの歴史</span>` | Prestasi: `<span class="jp-kanji">実績と表彰</span>` | Haori: `<span class="jp-kanji">公式羽織</span>` | Aksesoris: `<span class="jp-kanji">アクセサリー</span>` | Kepengurusan: `<span class="jp-kanji">役員構成</span>`
  - **Program & Fasilitas**: Hero: `<span class="jp-kanji">プログラム＆施設</span>` | Divisi: `<span class="jp-kanji">専門部門</span>` | Program Kerja: `<span class="jp-kanji">主要年間プログラム</span>` | Fasilitas: `<span class="jp-kanji">クラブ施設と備品</span>`
  - **Toko**: Hero: `<span class="jp-kanji">公式ショップ</span>` | Katalog Produk: `<span class="jp-kanji">商品カタログ</span>`
  - **Lomba & Acara**: Hero: `<span class="jp-kanji">大会＆イベント</span>` | Info Lomba: `<span class="jp-kanji">大会とイベント情報</span>`
  - **Papan Peringkat**: Hero: `<span class="jp-kanji">ランキングボード</span>` | Papan Peringkat: `<span class="jp-kanji">栄誉ランキング</span>`
  - **Rekomendasi**: Hero: `<span class="jp-kanji">おすすめ作品</span>` | Rekomendasi Media: `<span class="jp-kanji">人気メディア作品</span>`
  - **Kamus**: Hero: `<span class="jp-kanji">日本語辞書</span>` | Pencarian: `<span class="jp-kanji">文字と語彙検索</span>`
  - **Kamus Kanji**: Hero: `<span class="jp-kanji">漢字辞典</span>` | Pencarian Kanji: `<span class="jp-kanji">漢字検索</span>`
  - **Kata Motivasi**: Hero: `<span class="jp-kanji">名言集</span>` | Koleksi: `<span class="jp-kanji">名言コレクション</span>`
  - **Divisi**: Hub Divisi Hero: `<span class="jp-kanji">公式部門</span>` | Seksi: `<span class="jp-kanji">部門一覧</span>` | Bahasa: `<span class="jp-kanji">言語部門</span>` | Cosplay: `<span class="jp-kanji">コスプレ部門</span>` | Desain: `<span class="jp-kanji">デザイン部門</span>` | KWU: `<span class="jp-kanji">起業部門</span>`
  - **Latihan Kana**: Hero: `<span class="jp-kanji">仮名練習</span>` | Materi: `<span class="jp-kanji">教材選択</span>` | Campuran: `<span class="jp-kanji">総合練習</span>` | Hasil: `<span class="jp-kanji">学習完了</span>`
  - **Materi Buuku Dasar**: Hub Dasar Hero: `<span class="jp-kanji">基礎学習</span>` | Hiragana: `<span class="jp-kanji">平仮名入門</span>` | Katakana: `<span class="jp-kanji">片仮名入門</span>` | Jikoshokai: `<span class="jp-kanji">自己紹介</span>`
  - **Materi Buuku Lanjutan**: Hub Lanjutan Hero: `<span class="jp-kanji">上級学習</span>` | Grammar: `<span class="jp-kanji">応用文法</span>` | Kanji JLPT: `<span class="jp-kanji">漢字学習＆JLPT</span>`
  - **Proker Spesifik**: KTN: `<span class="jp-kanji">君と日本</span>` | NJR: `<span class="jp-kanji">日本語ラジオ</span>` | Konbini: `<span class="jp-kanji">未来のコンビニ</span>` | Ramadhan: `<span class="jp-kanji">ラマダン祝福</span>` | Tomodachi: `<span class="jp-kanji">日本友達</span>` | Dokumentasi: `<span class="jp-kanji">活動記録</span>`

### G. Arsitektur Komposisi Warna Teks Anti-Nabrak (Color Contrast Architecture Rule)
- **PRINSIP MUTLAK & ZERO-TOLERANCE: DILARANG KERAS TEKS MENABRAK BACKGROUND**:
  Jangan pernah meletakkan teks gelap di halaman/seksi gelap, dan JANGAN PERNAH meletakkan teks terang/pudar di halaman/seksi putih/terang! Seluruh kombinasi warna teks, paragraf, deskripsi seksi, judul, dan isi kartu WAJIB lolos uji kontras tinggi WCAG AAA.

- **1. Pada Seksi Berlatar Terang / Putih Solid (`#ffffff`, `#dasar`, `#kurikulum`, `.lomba-catalog-section`, `.toko-guide-white-section`, dll)**:
  - **DILARANG KERAS** teks putih atau abu-abu terang/pudar (`#ffffff`, `#cbd5e1`, `#d5ccd3`, `#94a3b8`, dsb.) di atas latar putih. Ini membuat teks tidak terlihat / harus diblok mouse baru terbaca.
  - **Teks Deskripsi Seksi (`.section-desc`, `p.section-desc`, `.copy`, `.lead`, `.doc-desc`)**: WAJIB menggunakan warna **abu-abu gelap slate pekat** (`color: #475569 !important;` atau `#334155 !important;` atau `#554857 !important;`), font-weight 500, tanpa bayangan teks kabur (`text-shadow: none !important;`).
  - **Judul Heading (`.heading`, `h2`)**: Menggunakan warna hitam arang pekat (`#18151b !important;` / `#1a151e !important;`) dipadukan aksen pink berry/sakura pada `<span>` (`color: var(--pink, #e91e63) !important;`).
  - **Sub-judul / Kanji (`.section-eyebrow`, `.section-eyebrow .jp-kanji`)**: Menggunakan teks *deep berry pink* (`color: #c2185b !important;` / `#e91e63 !important;`), latar belakang semi-transparan pink lembut `rgba(233, 30, 99, 0.08)`, dan border tegas `1.5px solid rgba(233, 30, 99, 0.28)`. Teks terbaca tajam dan tidak pudar.
  - **Kartu Komponen & Deskripsi Kartu (`.course-card`, `.doc-big-card`, dsb.)**: Latar putih solid dengan border pink lembut (`#ffccd9` / `rgba(255, 101, 155, 0.35)`), judul kartu hitam pekat (`#18151b !important;`), dan deskripsi kartu abu-abu gelap (`#475569 !important;` / `#554857 !important;`).

- **2. Pada Seksi Berlatar Gelap / Hitam Solid (`#0e0b12`, `#111111`, `.soft-section`, `#lanjutan`, `.facility-section`, `.toko-catalog-section`, dll)**:
  - **DILARANG KERAS** teks hitam atau abu-abu gelap pekat (`#18151b`, `#333333`, `#475569`, `#554e57`, dsb.) di atas latar gelap. Ini membuat teks tenggelam ke dalam latar hitam.
  - **Teks Deskripsi Seksi (`.section-desc`, `p.section-desc`, `.copy`, `.lead`)**: WAJIB menggunakan warna **abu-abu terang bersih** (`color: #cbd5e1 !important;` atau `#e2e8f0 !important;`), nyaman di mata, kontras tinggi, dengan `text-shadow: 0 1px 6px rgba(0, 0, 0, 0.5) !important;`.
  - **Judul Heading (`.heading`, `h2`)**: Menggunakan warna putih murni (`#ffffff !important;`) dipadukan aksen pink bercahaya pada `<span>` (`color: var(--pink, #e91e63) !important;`).
  - **Sub-judul / Kanji (`.section-eyebrow`, `.section-eyebrow .jp-kanji`)**: Menggunakan teks pink cerah berpendar (`color: #ff659b !important;`) berbalut pil semi-transparan pink `rgba(255, 79, 145, 0.18)` dengan border pendar pink `rgba(255, 101, 155, 0.45)`.
  - **Kartu Komponen & Deskripsi Kartu**: Permukaan gelap gradasi obsidian (`#1d1624` -> `#130f18`), border pink halus, judul kartu putih bersih (`#ffffff !important;`), dan deskripsi kartu abu-abu terang (`#cbd5e1 !important;` / `#d5ccd3 !important;`).

- **3. Larangan Keras Selector CSS Brittle (`:nth-of-type(even/odd)`) Tanpa Pengecualian**:
  - Dilarang keras mengandalkan selector global `main > section:nth-of-type(even) p` atau `main > section:nth-of-type(odd) p` untuk mengatur warna teks deskripsi secara buta.
  - Mengapa? Karena keberadaan `<section class="page-hero">` menggeser urutan ganjil-genap sehingga seksi terang `#dasar` dan `#kurikulum` menjadi genap (terkena warna teks putih/terang), sedangkan seksi gelap `#lanjutan` menjadi ganjil (terkena warna teks gelap pekat).
  - Setiap seksi yang memiliki tema spesifik (seperti `.learning-path`, `#dasar`, `#lanjutan`, `#kurikulum`, `.facility-section`, `.division-section`) WAJIB dikecualikan dari selector nth-of-type global (`:not(...)`) dan WAJIB diberikan aturan warna teks eksplisit dengan selector berbobot spesifisitas tinggi (`!important`).

- **4. Pada Hero Banner Ber-Background Ilustrasi Karakter (Sora / Header Utama)**:
  - **Sub-judul / Kanji Hero Banner (`.page-hero-eyebrow .jp-kanji`, `.hero-eyebrow .jp-kanji`)**:
    - **DILARANG MENGGUNAKAN PILL / BADGE KOTAK/OVAL** pada background banner hero (background: `transparent`, border: `none`, padding: `0`, border-radius: `0`, box-shadow: `none`).
    - Warna sub-judul Jepang pada background banner hero **WAJIB PINK GLOWING** (`#ff659b !important`) dengan text-shadow bayangan gelap dan pendaran pink halus agar terbaca jelas dan menyatu artistik dengan ilustrasi.
    - Sub-judul Beranda (`ようこそ`): Huruf Jepang Noto Serif JP besar berukuran jelas, berwarna pink glowing (`#ff659b !important`) tanpa badge box.
  - **Judul Utama Hero Beranda (`.hero-title`)**:
    - Format dwinafas: kata pertama/kedua putih, kata penutup pink (`MIRAI NO` berwarna putih `#ffffff`, `<span>WEBU</span>` berwarna pink sakura `var(--pink)`).
  - **Tata Letak Hero & Ikon Sosial Media (Harmonis Seperti Beranda)**:
    - Seluruh halaman inner hero (`.page-hero`, `.proker-hero`, `.quest-hero`, `.toko-hero`) wajib memiliki perataan bawah (*grounded baseline*) yang sama dengan Beranda: blok teks berada di kiri bawah (`bottom: 14%`, `left: 5%` atau `6%`) dan sidebar ikon sosial media (`.hero-social-sidebar`) berada di kanan bawah (`bottom: 14%`, `right: 5%` atau `6%`), tidak mengambang canggung di tengah badan ilustrasi karakter.
  - **Tanpa Deskripsi di Hero**: Hero banner berlatar gambar ilustrasi hanya memuat Sub-judul Jepang dan Judul Utama agar tidak menutupi visual karakter Sora.

### H. Aturan Bahasa Antarmuka (Pemberantasan Bahasa Inggris yang Tidak Perlu)
- Seluruh teks tampilan website (judul, deskripsi, tombol, menu navigasi, badge, filter, dan pesan) **WAJIB murni menggunakan Bahasa Indonesia** sebagai bahasa pengantar dan **Bahasa Jepang** (Kanji, Hiragana, Katakana, dan Romaji) untuk materi pembelajaran klub.
- **Dilarang keras memakai Bahasa Inggris yang tidak perlu** pada teks yang dilihat pengunjung web.
- **Kamus Standar Padanan Istilah UI/UX**:
  - *Pre-Order (PO)* &rarr; **Pra-Pesan (PO)**
  - *Ready Stock* &rarr; **Tersedia**
  - *Best Seller* &rarr; **Paling Laris**
  - *Fresh* &rarr; **Segar & Hangat**
  - *Custom* &rarr; **Kustom / Pesan Khusus**
  - *All Size / Oversized* &rarr; **Semua Ukuran / Longgar Nyaman**
  - *Sticker Pack* &rarr; **Paket Stiker**
  - *Totebag* &rarr; **Tas Jinjing (Totebag)**
  - *Cart* &rarr; **Keranjang Belanja**
  - *Add to Cart* &rarr; **+ Keranjang**
  - *Checkout* &rarr; **Pesan via Google Form**
  - *Clear Cart* &rarr; **Kosongkan Keranjang**
  - *Search* &rarr; **Cari Produk / Materi**
  - *Level / Challenge* &rarr; **Tingkat / Tantangan**
- **Gaya Bahasa & Nada Bicara (Tone of Voice Anak SMA)**:
  - Setiap teks, deskripsi, pesan sambutan, maupun pengantar konten **WAJIB ditulis dengan gaya bahasa anak SMA yang semi-formal, santun, hangat, dan bersahabat**.
  - Bawa vibes organisasi/ekskul sekolah yang aktif dan guyub: komunikatif, menghargai sesama teman (*"kalian", "sahabat", "bareng-bareng"*), tidak birokratis kaku seperti instansi pemerintah, dan tidak dibuat-buat seperti bot robot AI.
  - Untuk bagian feedback/kritik & saran: ajak audiens secara terbuka bila menemukan kendala tampilan/bug di Mirai no Webu maupun ide kegiatan kreatif untuk klub Mirai no Hana.

### I. Aturan Deskripsi dan Teks Pendukung (Card & Page Description Rule)
- **Etalase Produk Toko Bersih & Ringkas**:
  - Pada kartu produk Toko, dilarang menaruh deskripsi produk panjang (`.toko-card-desc`) dan dilarang menampilkan rating bintang ulasan (`.toko-rating`) agar kartu tampil bersih, rapi, dan berfokus pada foto produk, nama produk, spesifikasi teknis penting, harga, dan tombol aksi.
  - Pada halaman lain yang memerlukan deskripsi materi, deskripsi harus padat, informatif, dan ringkas (maksimal 2 sampai 3 baris kalimat).
- **Kontras Warna Teks**:
  - Di latar gelap: Warna teks menggunakan abu-abu lembut (`#cbd5e1` atau `#94a3b8`), bukan putih murni 100%, agar kontrasnya nyaman di mata dan tidak silau.
  - Di latar putih/terang: Warna teks menggunakan abu gelap pekat (`#554857` atau `#475569`), bukan hitam murni tajam, untuk kenyamanan membaca optimal.
- Dilarang membuat kalimat deskripsi bertele-tele, klise, atau membuang ruang visual kartu.

### J. Aturan Tombol
- Sudut tombol melengkung halus dan modern (border-radius: 12px), bukan kotak kaku dan bukan oval lonjong.
- Memakai warna gradien pink sakura dengan bayangan berpendar lembut (glow).
- Saat disorot mouse (hover), tombol naik sedikit (translateY -2px) dan pendaran warnanya semakin menyala.
- Ukuran tombol harus pas dan proporsional dengan isi teksnya (tidak boleh melar memenuhi seluruh kartu).

### K. Aturan Penataan Foto, Poster, dan Avatar
- **Format Kartu Lomba (Poster Utuh di Atas & Teks Info di Bawah)**:
  - Kartu event/lomba (`.event-card`) ditata secara bertumpuk vertikal (**Vertical Stacked Layout**):
    - **Sisi Atas (Poster Display)**: Menampilkan poster lomba secara utuh, lengkap, dan proporsional tanpa terpotong (`object-fit: contain`) dengan rasio tinggi yang lapang (tinggi 540px di desktop, 460px di tablet, 380px di mobile) serta latar belakang gelap netral (`#08080c`).
    - **Sisi Bawah (Informasi Teks & Aksi)**: Menampung header badge (kategori lomba/acara, level wilayah, status tanggal), judul lomba tebal, tag penyelenggara, deskripsi singkat, grid spesifikasi 4 kolom (Pelaksanaan, Biaya, Lokasi, Cabang), dan tombol aksi lebar penuh.
- **Frame 1 Poster & Carousel Geser Mandiri**: Wadah poster di kartu event wajib berukuran 1 poster tunggal yang utuh (Single Poster View), tidak boleh menampilkan poster bertumpuk vertikal ataupun berdampingan terpotong:
  - Jika event memiliki lebih dari 1 poster/halaman (seperti ITS & UNESA), gunakan carousel horizontal yang bisa digeser dengan panah, drag mouse di desktop, atau swipe jari di HP.
  - **Tombol Panah Navigasi**: Wajib berada tepat di **bagian tengah samping kiri (‹) dan kanan (›)** poster dengan gaya semi-transparan ber-blur dan efek pendar pink saat disorot. Jika poster hanya ada 1 lembar, tombol panah otomatis disembunyikan.
  - **Tanpa Keterangan Counter Angka & Tag Watermark**: Dilarang menampilkan teks counter angka (seperti "1 dari 2") serta label tag watermark institusi/univ (seperti "POSTER RESMI ITS", dll).
  - **Tombol Aksi Semantik & Navigasi Langsung (Tanpa Pop-up Juknis)**:
    - Tombol aksi kartu dibedakan secara tegas: **"🔗 Buka Link Lomba"** untuk kategori lomba, dan **"🔗 Buka Link Acara Jejepangan"** untuk kategori festival/acara.
    - **Langsung Mengarah ke Tautan Eksternal**: Tombol langsung membuka tautan tujuan di tab baru (`target="_blank" rel="noopener noreferrer"`). Untuk sementara seluruh tombol diarahkan ke Instagram resmi Nihongo Kurabu Mirai No Hana (`https://www.instagram.com/mirainohana_smawh2`), bukan membuka pop-up modal juknis internal.
  - **Bebas Interaksi Tanpa Jebakan (No Lock-In)**: Poster murni menjadi visual kartu yang aman disentuh, di-drag, atau di-scroll tanpa memicu modal lightbox yang mengunci scroll layar (`overflow: hidden`). Navigasi halaman poster kedua dilakukan murni via tombol panah tengah samping atau swipe.
- **Avatar Lingkaran**: Wadah avatar profil atau juara wajib memiliki latar belakang putih (#ffffff) dengan gambar berukuran contain dan sedikit padding, agar bagian telinga, rambut, atau topi chibi tidak terpotong garis tepi lingkaran.

### L. Aturan Format Foto Produk Toko Ringkas (Shopee Style) & Carousel Geser Mandiri
- **Format Ukuran Foto Ringkas & Kanvas Seamless (Shopee-Style Display)**:
  - Header kartu produk toko menggunakan format ringkas dan bersih (`.toko-card-thumb` dengan tinggi 185px di desktop, 155px di HP) tanpa canvas kotak ganda berspasi tebal yang menyisakan terlalu banyak ruang putih kosong.
  - Kanvas foto menyatu langsung dengan bagian atas kartu produk (`border-radius: 14px 14px 0 0; background: #ffffff; border-bottom: 1px solid rgba(255, 79, 145, 0.18)`).
  - Foto makanan & minuman asli (`oni.jpeg`, `tak.jpeg`, `dan.jpeg`, `mat.jpeg`, `teh.jpeg`) tampil penuh (`object-fit: cover`) layaknya etalase Shopee tanpa margin kosong berlebih.
  - Produk cinderamata/atribut berbasis potong latar belakang tampil proporsional (`object-fit: contain; max-width: 88%; max-height: 86%`) di tengah kanvas putih bersih.
- **Carousel Geser Kiri-Kanan utk Produk Lebih dari 1 Foto (Haori & Kartu Tanda Anggota)**:
  - Jika produk memiliki lebih dari 1 foto/sudut pandang (seperti **Haori**: tampak depan `haori-depan-new.png` & belakang `haori-belakang-new.png`; serta **Kartu Tanda Anggota**: tampak depan `idc-front.jpeg` & belakang `idc-back.jpeg`), gunakan sistem carousel horizontal (`.toko-poster-carousel` [data-product-carousel]):
    - Menampilkan **1 sudut pandang penuh** per slide dengan label badge pill indikator posisi (`Depan` / `Belakang`).
    - Dilengkapi tombol panah geser melayang di samping kiri (`‹`) dan kanan (`›`) dengan gaya semi-transparan ber-blur dan efek pendar pink saat disentuh/di-hover.
    - Mendukung navigasi tombol klik, swipe jari di HP, dan mouse drag di desktop dengan scroll-snapping halus (`scroll-snap-type: x mandatory`).
- **Keterangan Bahan & Spesifikasi Wajib Dipertahankan**:
  - Seluruh informasi bahan, ukuran, porsi, dan dimensi teknis pada kotak spesifikasi (`.toko-card-specs`) wajib dipertahankan secara utuh dan jelas di bawah nama produk.
- **Katalog Produk Terkurasi (12 Item Aktif) & Aturan Penamaan Lugas (Anti-Fluff Naming Rule)**:
  - **Nama Produk Wajib Lugas & Langsung ke Inti**: Dilarang menambahkan kata-kata hiasan/pemasaran berlebihan pada nama produk (misalnya: dilarang memakai "Resmi Klub", "Personal", "Spesial", dsb). Nama produk harus to the point:
    - Atribut Mirai no Hana (5): `Haori`, `Kartu Tanda Anggota`, `Lanyard`, `Pin`, `Nametag`.
    - Makanan Konbini (3): `Onigiri Segitiga`, `Takoyaki`, `Dango`.
    - Minuman Konbini (2): `Matcha Latte`, `Es Teh` (Rp 5.000).
    - Cinderamata (2): `Stiker`, `Gantungan Kunci`.
  - Produk Ramune Soda dan Dorayaki telah dihapus permanen.
  - Foto produk kuliner & minuman asli dipasang dari `images/mirai/produk/` (`oni.jpeg`, `tak.jpeg`, `dan.jpeg`, `mat.jpeg`, `teh.jpeg`) pada alas kanvas putih solid.
- **Standar 5 Toko Karakter Kutipan Motivasi (Halaman Motivasi)**:
  - Kutipan motivasi anime di `kelas/motivasi.html` dan slider kutipan footer `js/main.js` dikurasi menjadi **5 tokoh ikonik** dengan foto potret karakter asli dari folder `images/mirai/karakter/`:
    1. Monkey D. Luffy (`luf.jpeg`) · One Piece
    2. Eren Yeager (`ere.jpeg`) · Attack on Titan
    3. Uzumaki Naruto (`nar.jpeg`) · Naruto Shippuden
    4. Midoriya Izuku / Deku (`dek.jpeg`) · My Hero Academia
    5. Tanjiro Kamado (`tan.jpeg`) · Demon Slayer
  - Tokoh Asta (Black Clover) dan Kageyama/Hinata (Haikyuu!!) telah dihapus.

### M. Aturan Spasi dan Tata Letak (Layout)
- **Menu Navigasi Parsial (Non-Fullscreen Off-Canvas Drawer di HP & Laptop)**:
  - Menu navigasi (`.sidebar-nav`) **dilarang keras membuka secara layar penuh (fullscreen 100% width)** baik di HP maupun di laptop.
  - Pada perangkat seluler/HP (`max-width: 600px`), menu harus muncul **sebagian dari sisi kanan** layaknya mode laptop (`width: 78%`, `max-width: 310px`, `min-width: 250px`), dengan sisi kiri (~22%) tetap memperlihatkan latar belakang halaman yang diredupkan oleh `.sidebar-overlay`.
  - Mengetuk/mengklik area redup di sebelah kiri wajib langsung menutup menu secara instan.
  - Menu memiliki scrollbar halus bertema pink gelap (`scrollbar-width: thin; scrollbar-color: rgba(255, 79, 145, 0.35) transparent`) tanpa menampilkan scrollbar default abu-abu/putih sistem operasi.
  - Saat menu aktif, scroll halaman latar belakang dikunci via `body.sidebar-open { overflow: hidden !important; }`.
- **Navigasi Halaman Ringkas & Pintar (Smart Pagination with Ellipsis & Arrow-Only)**:
  - Tombol navigasi halaman (`Sebelumnya` dan `Selanjutnya`) **dilarang memuat teks panjang** yang menyebabkan pematahan baris (*line wrap*) di layar HP. Wajib hanya menampilkan simbol panah ringkas (`←` dan `→`) dalam wadah bujur sangkar/lingkaran kompak (42px di desktop, 38px di HP) lengkap dengan `aria-label` semantik.
  - Penomoran halaman wajib menggunakan sistem **Smart Ellipsis (`...`)**:
    - Jika total halaman > 5, tampilkan halaman pertama, jendela halaman aktif, titik tiga (`...`), dan halaman terakhir (contoh: pada halaman 1 dari 6 tampil `[←] [1] [2] [...] [6] [→]`).
    - Memastikan seluruh kontrol navigasi pagination tertata rapi dalam 1 baris tunggal (*single horizontal row*) tanpa terpotong atau turun ke baris berikutnya di perangkat seluler.
- **Anti Ruang Hampa**: Di layar laptop, kartu tidak boleh menyisakan ruang kosong hitam atau putih yang melompong di tengah antara judul dan tombol bawah. Susun elemen secara padat dan seimbang.
- **Pemusatan Kartu Ganjil**: Jika jumlah kartu dalam satu seksi berjumlah ganjil (seperti 11 kartu pengurus Kabinet Clover), kartu pada baris terakhir diletakkan tepat di posisi tengah (rata tengah), tidak boleh miring sendirian di sebelah kiri.
- **Keseragaman Kartu Program Kerja & Divisi**: Ukuran kartu Program Kerja (tinggi, padding, border-radius, font judul, dan posisi tombol) wajib disamaratakan persis dengan kartu Divisi agar tampilan sejajar dan rapi.
- **Format Kartu Fasilitas Landscape**: Fasilitas Mirai no Hana menggunakan format kartu Landscape memanjang (2 kartu: Ruang Pertemuan dan Mirai no Webu). Deskripsi kartu Mirai no Webu diselaraskan dengan teks Beranda, dan tombol aksi di bawah digantikan oleh badge status resmi.
- **Grid Penelusuran Beranda (7 Kartu)**: Menu kartu beranda menyusun 7 kartu seimbang (1. Struktur Divisi, 2. Program Kerja, 3. Fasilitas, 4. Toko & Konbini, 5. Rekomendasi, 6. Papan Peringkat, 7. Lomba & Acara).
- **Format Nama Bersih & Tunggal Jabatan**:
  - Jabatan pengurus **hanya muncul 1 kali saja** di atas nama pengurus (`.member-label`). Dilarang menduplikasi nama jabatan di bawah nama pengurus.
  - Nama anggota atau pengurus ditulis rapi tanpa embel-embel keterangan kelas jika diminta.
  - **Profil Pembina Klub**: Kartu Pembina berformat bersih, padat, dan elegan tanpa deskripsi panjang yang mengulang kata "Pembina". Cukup memuat avatar dengan badge peran, kicker pembina, lencana periode masa pengabdian, nama lengkap guru, dan instansi sekolah.
- **Scroll Vertikal Kepengurusan (Anti Gap Space Slider)**:
  - Pada slider multi-periode kepengurusan (Kabinet Sora 8 kartu vs Kabinet Clover 11 kartu), tinggi area kartu dikunci pas setinggi 2 baris kartu (tinggi Kabinet Sora).
  - Kabinet Clover (11 orang) dibuat *scrollable* atas-bawah (vertikal) di dalam gridnya, sehingga 3 orang di baris ketiga dapat dilihat dengan menggulir ke bawah tanpa membuat Slide 1 melar dan menyisakan ruang kosong putih aneh di bawahnya.
- **Proporsi Kanvas Urutan Menulis Yoon (Kombinasi 2 Huruf)**:
  - Karakter kombinasi Yoon (seperti `ひゃ`, `きゅ`, `しょ`, dll) wajib ditampilkan **berukuran besar dan proporsional** seimbang dengan kana tunggal (tinggi ~185px dibandingkan kana tunggal 200px), agar tidak tampak kerdil atau timpang di dalam kanvas latihan.
  - Setiap karakter wajib berdiri di dalam kotak kisi Genkouyoushi tersendiri (`.yoon-char`) secara berdampingan dengan jarak rapat rapi (`gap: 14px`). **Dilarang menyatukan atau menabrakkan kedua huruf ke dalam satu koordinat kotak**, sehingga huruf utama dan huruf kecil (sutegana) tetap terpisah bersih tanpa tumpang tindih.
  - Di layar HP kecil (mobile), ukuran kotak otomatis fleksibel (`clamp(140px, 42vw, 185px)`) agar tetap berdampingan horizontal tanpa patah ke bawah.
- **Galeri Kumpulan-Kumpulan Foto & Dokumentasi**:
  - Judul seksi galeri foto ("Kumpulan-Kumpulan Foto") wajib berformat **rata kiri** (`.heading`) seragam dengan seksi lainnya, bukan rata tengah.
  - Tampilan slider galeri murni berfokus visual: dilarang menampilkan teks subjudul berulang seperti "Potret Keseruan" maupun "Momen Bersama".
  - Foto dokumentasi disusun dalam 2 baris slider independen (baris 1 portrait, baris 2 landscape) dengan wadah luas 1100px, efek elevasi hover lembut (`translateY(-8px)`), border-radius 18px, dan bayangan berpendar pink khas Mirai no Hana.
- **Format Bersih Badge Podium Papan Peringkat**:
  - Pada 3 kartu podium teratas di halaman `peringkat.html`, label badge medali hanya mencantumkan nomor peringkat ringkas: **"PERINGKAT 1"**, **"PERINGKAT 2"**, dan **"PERINGKAT 3"**.
  - Dilarang menambahkan embel-embel teks predikat logam (seperti "· JUARA EMAS", "· PERAK", atau "· PERUNGGU") agar lencana tetap bersih, minimalis, dan proporsional.
- **Latihan Mandiri Kana Interaktif (20 Soal Acak, Tata Letak Minim Space & Duolingo-Style Stroke Tracing)**:
  - Total kuis latihan mandiri berjumlah **20 soal**, terdiri dari **10 soal pilihan ganda huruf biasa** (kana → romaji dan romaji → kana) + **5 soal tantangan interaktif menulis goresan kana** yang posisinya **diacak secara random** (tidak berselang-seling kaku), ditambah 4 soal kosakata dan 1 soal pasangkan kata.
  - **Petunjuk Tunggal Romaji Saja pada Soal Goresan**: Pada soal interaktif goresan kana, petunjuk yang muncul di bagian atas kanvas **HANYA menampilkan Romaji saja** (misalnya `a`, `i`, `u`, `e`, `o`, `ka`, `ki`, dst.), dilarang menampilkan karakter Kana di atas kanvas agar melatih daya ingat aktif pengguna dalam merecall bentuk karakter kana secara mandiri.
  - **Karakter Goresan Eksklusif Sesuai Level Terpilih**: Karakter pada soal goresan kana **WAJIB murni dan eksklusif berasal dari level materi yang sedang dipilih oleh pengguna** (misalnya jika memilih level 1 `a i u e o`, maka 5 soal goresan hanya boleh memunculkan huruf `あ`, `い`, `う`, `え`, `お` tanpa ada huruf dari level lain yang menyusup). Begitu pula untuk setiap level materi lainnya.
  - **Tata Letak Minim Space & Fokus Fitur Fungsional**: Dilarang menampilkan tombol "Ulangi Goresan" yang memakan ruang atau teks baris petunjuk panjang di bawah kanvas. Subtitle soal disembunyikan dan indikator langkah disederhanakan menjadi deretan *pills* bulat kompak (1, 2, 3) tepat di atas kanvas. Ukuran kanvas proporsional (`min(240px, 52vmin)`) sehingga seluruh antarmuka muat 1 layar penuh (*no-scroll viewport*) di HP maupun laptop *split-view*.
  - **Kanvas Bersih Tanpa Bantuan di Awal**: Kanvas hanya menampilkan kisi Genkouyoushi dan goresan langkah sebelumnya yang sudah selesai. Garis panduan putus-putus dan titik awal lingkaran **HANYA muncul saat pengguna membuat goresan keliru** untuk memandu gerakan yang benar. Begitu berhasil dan pindah ke langkah berikutnya, garis panduan kembali bersih.
  - **Ketebalan Garis Proporsional Selaras Kamus**: Garis kanvas tulisan tangan menggunakan rasio ketebalan `4.4` unit (`4.4 * rect.width / 109`), garis goresan selesai `4.4` unit, bayangan huruf `4.2` unit, dan panduan putus-putus `3.8` unit. Ketebalan ini selaras penuh dengan kuas Kamus (`4.2px` - `4.4px`), memberikan sapuan visual yang rapi, elegan, tidak terlalu tebal/gemuk, dan nyaman ditiru pengguna di berbagai resolusi layar.
  - **Akurasi Bentuk Kana Standar Terkurasi (Ko, Fu, Katakana Ko, dll.)**: Path SVG goresan kana diselaraskan secara presisi dengan bentuk glif buku teks resmi bahasa Jepang. Karakter `こ` (dan `ご`) menggunakan goresan horizontal pertama yang bersih dan tegas tanpa bengkokan kail aneh di ujung; Katakana `コ` (dan `ゴ`) menggunakan sudut siku-siku tegak 90° yang tegas; serta Hiragana `ふ` (dan `ぶ`, `ぷ`) disusun menggunakan 4 goresan kurva natural (titik atas, kurva sapuan tengah yang lembut tanpa gembungan balon terbalik, titik kiri, dan titik kanan) sehingga 100% konsisten dengan gambar visual huruf di kamus.
  - **Toleransi Keakuratan Bersahabat (Menceng Dikit Tetap Benar)**: Validasi memeriksa kedekatan titik awal (≤21.5 unit), titik akhir (≤22.5 unit), panjang goresan (≥44%), cakupan kurva (coverage ≥52%), deviasi rata-rata (≤16.8 unit), deviasi maksimal (≤29.5 unit), dan arah progresif. Tetap menolak sentuhan/geseran mini tanpa bentuk dan arah terbalik, namun memberikan toleransi ekstra ramah sentuhan untuk menoleransi sedikit deviasi bentuk antara gambar huruf dan goresan kanvas (*menceng dikit ada koreksi benarnya*).
  - **Sistem Modal Viewport-Fixed & Scroll Bebas Terpotong (Anti-Clipping Protocol)**:
    - Tampilan latihan (`.practice-view`) dan hasil latihan (`.result-view`) wajib berposisi `fixed` viewport (`position: fixed !important; inset: 0 !important; width: 100vw !important; width: 100% !important; height: 100vh !important; height: 100dvh !important; max-height: none !important; z-index: 99999 !important; overflow-y: auto !important; overflow-x: hidden !important; -webkit-overflow-scrolling: touch !important; overscroll-behavior: contain !important; display: flex !important; flex-direction: column !important; align-items: center !important; justify-content: flex-start !important; padding: clamp(24px, 4vh, 48px) clamp(14px, 3vw, 24px) clamp(44px, 6vh, 68px) !important;`).
    - **Kartu Modal Wajib Anti-Shrink (`flex-shrink: 0 !important`) & `overflow: visible !important`**: Wadah kartu (`.practice-shell` dan `.result-card`) dilarang keras memiliki `overflow: hidden` atau membiarkan default flex shrinking aktif. Wajib eksplisit `flex-shrink: 0 !important; flex-grow: 0 !important; max-height: none !important; overflow: visible !important; width: min(660px, 100%) !important; margin: 0 auto !important;` agar seluruh konten (termasuk daftar panjang Review Kesalahan) tidak terpotong dan dapat digulir bebas dari atas sampai bawah di layar HP, tablet, maupun desktop *split-view*.
    - **Scrollbar Elegan**: Modal dilengkapi scrollbar pink halus (`scrollbar-width: thin; scrollbar-color: var(--pink) rgba(255, 255, 255, 0.08);`) yang mudah dilihat dan diinteraksikan.
    - **Desain Visual Kartu Hasil Elevated**:
      - Kartu hasil berlatar putih bersih (atau `#211925` tema gelap), sudut melengkung `18px`, bayangan melayang elegan, dan aksen garis pink halus.
      - Header kicker menggunakan pil modern `SESI SELESAI · セッション完了`, judul `🎉 Latihan selesai!` serif tegas, streak pil oranye hangat `🔥 Runtunan terbaik: X`.
      - 4 Kartu statistik interaktif berbingkai lembut (Akurasi, Benar, Salah, Waktu) dengan respons hover micro-elevasi.
      - Tombol aksi: `↻ Coba Lagi` dengan gradient pink cerah menonjol dan `Tinjau Kesalahan (X)` yang dinamis menampilkan jumlah kesalahan (atau `Nilai Sempurna 🎉` jika 100% benar) dengan aksi *smooth scroll* langsung ke target review.
      - **Review Kesalahan Komprehensif**: Kartu kesalahan memiliki lencana nomor, tipe kesalahan, huruf kana raksasa anggun (38px serif), dua kotak komparasi jelas (Jawaban Kamu ❌ vs Jawaban Benar ✅), kotak tips penjelasan 💡, serta tombol suara interaktif `🔊 Dengarkan` langsung di setiap kartu kesalahan untuk melatih pendengaran native pengguna.
      - Teks deskripsi review kesalahan (`.mistake-review-header p`) wajib `display: block !important; width: 100% !important;` agar bebas dari bug wrapping sempit 38px legacy grid.
    - Dilarang keras menerapkan CSS `transform` maupun `animation` dengan `animation-fill-mode: both` yang mengubah `transform` pada tag `body` atau class `body.learning-app` (agar tidak membajak CSS Containing Block elemen fixed).
    - Saat modal terbuka, halaman latar belakang dikunci scroll-nya via `body.is-practicing { overflow: hidden !important; }`, dan posisi scroll modal (`scrollTop`) otomatis di-reset ke 0 setiap kali sesi latihan atau hasil dibuka sehingga modal selalu muncul tepat di depan mata pengguna dan mengikuti posisi layar secara konsisten.
    - Elemen di dalam `.practice-view` dan `.result-view` dikecualikan dari `setupReveal()` motion-reveal agar tidak mengalami jeda transisi atau distorsi layout saat dimunculkan.
- **Pola Motif Kartu & Tipografi Latihan Kana (`latihan.html`)**:
  - **Pola Motif Kartu Level (Hiragana vs Katakana)**:
    - Kartu Hiragana menggunakan motif awan Kumo gelap (`images/mirai/background/c1b.jpeg`) via `.level-card--hiragana::after` / `[data-script="hiragana"] .level-card::after`.
    - Kartu Katakana menggunakan motif Wagara ombak gelap (`images/mirai/background/w1b.jpeg`) via `.level-card--katakana::after` / `[data-script="katakana"] .level-card::after`.
    - Keduanya menggunakan `mix-blend-mode: screen` dengan opacity halus (0.045 hingga 0.08 saat hover) agar menyatu anggun di atas kartu tanpa mengganggu keterbacaan teks.
  - **Pola Motif Kartu Latihan Gabungan (`.mode-card`)**:
    - Kartu mode campuran bersifat adaptif dan dinamis berganti sesuai skrip kana yang sedang aktif:
      - **Saat membuka Hiragana**: Menggunakan motif awan Kumo terang (`images/mirai/background/c1w.jpeg`) dengan `mix-blend-mode: multiply` dan opacity 0.10 (0.16 saat hover) pada tema terang, serta opacity 0.08 (0.14 saat hover) pada tema gelap (`body.theme-dark`).
      - **Saat membuka Katakana**: Menggunakan motif Wagara ombak gelap (`images/mirai/background/w1b.jpeg`) dengan `mix-blend-mode: screen` dan opacity 0.045 (0.08 saat hover) pada tema gelap, serta filter invert pada tema terang.
  - **Tipografi Bersih & Bebas Teks Redundan**:
    - Hero banner dilarang menampilkan eyebrow teks redundan "Kelas Dasar · Latihan Mandiri".
    - Seksi Latihan Gabungan menggunakan judul utama Two-Tone yang kokoh: `<h2>Latihan <span>Gabungan</span></h2>` tanpa teks kicker. Dilarang menampilkan teks usang seperti "MODE TANTANGAN", "Campur materi", maupun kalimat deskripsi panjang "Pilih cakupan latihan. Materi yang terkunci tidak akan masuk ke soal." agar layout tetap bersih, minimalis, dan seragam.
  - **Badge Informasi Isi Latihan Berada di Bawah Judul Materi (Bukan di Dalam Kartu)**:
    - Deretan badge informasi komposisi latihan (`.script-overview-badges` / `[data-script-badges]`) ditempatkan **tepat di bawah judul materi** (`Hiragana ひらがな` atau `Katakana カタカナ`), bukan di dalam kartu-kartu level:
      - **Desain Seragam 1 Jenis**: Seluruh badge menggunakan desain pil aksen pink seragam yang estetik persis seperti desain badge "20 Soal" (latar belakang semi-transparan pink, border pink halus, dan teks pink cerah `#ff659b` / `var(--pink)`).
      - **Daftar Lencana Lengkap (6 Item)**:
        1. **20 Soal**: Total jumlah soal latihan.
        2. **Kana → Romaji**: Dinamis sesuai alfabet (`Hiragana → Romaji` atau `Katakana → Romaji`).
        3. **Romaji → Kana**: Dinamis sesuai alfabet (`Romaji → Hiragana` atau `Romaji → Katakana`).
        4. **Goresan**: Menandai soal interaktif menulis goresan kana ala Duolingo (tanpa emoji).
        5. **Kosakata**: Menandai soal latihan tebak kata.
        6. **Pasangkan Kata**: Menandai soal pencocokan pasangan kata.
    - **Kartu Level Tetap Bersih & Proporsional**: Dilarang menaruh deretan badge isi soal tersebut di dalam masing-masing kartu level (`level-card`), sehingga kartu level bebas dari repetisi elemen redundan, memiliki ketinggian kompak (`min-height: 230px`), dan fokus menampilkan nomor level, karakter kana, serta tombol aksi.
    - **Dilarang Keras**: Menampilkan teks basi/usang seperti "Mulai dari sini" atau kalimat teks bantuan panjang di kartu level.

---

### N. Standar Kartu Expandable Beranda & Tentang (Tap-to-Expand Standard)
- **Arsitektur Tap-to-Expand**:
  - Kartu navigasi Beranda (`.start-card`, `.activity-start-card`) dan kartu fitur besar (`.about-feature-card`, `.feedback-feature-card`) menggunakan tag `<div>` dengan atribut `[data-expand-card]`, BUKAN tag link pembungkus `<a>`.
  - **Kondisi Awal (Collapsed)**: Hanya menampilkan nomor urut (`.card-step-num`), judul (`<h3>` atau `<h2>`), maskot chibi di pojok kanan bawah, tombol aksi CTA, dan tombol panah buka-tutup (`.card-toggle`). Deskripsi disembunyikan.
  - **Kondisi Terbuka (`.is-expanded`)**: Mengetuk kartu atau tombol panah membuka deskripsi menggunakan transisi CSS Grid modern `grid-template-rows: 0fr -> 1fr` (`.card-collapsible-content > .card-collapsible-inner`) tanpa `display: none` agar animasi berjalan mulus.
  - **Perilaku Tombol Aksi (`[data-expand-cta]`)**:
    * Jika tombol ditekan saat kartu masih tertutup: kartu membuka terlebih dahulu, tidak langsung berpindah halaman.
    * Jika tombol ditekan saat kartu sudah terbuka: berpindah ke halaman tujuan.
    * Kombinasi Ctrl/Cmd/Shift/Alt klik dibiarkan membuka tab baru secara normal.
  - **Format Tombol Seragam**: Seluruh tombol aksi kartu berformat kotak agak bundar (`border-radius: 12px`).
  - **Ikon Panah Toggle (`.card-toggle`)**: Menggunakan chevron CSS murni di sudut kanan atas dengan atribut `aria-expanded` dan styling `:focus-visible`.
  - **Laci Logo NK (`#mnhAboutDrawerCard`)**: Tampil di seluruh ukuran layar (desktop, tablet, mobile). Saat kartu diekspansi (`.is-expanded` / `.is-pulled`), laci logo NK meluncur keluar dari kanan (`transform: translateX(0)`) melahap/memakan sisi kanan kartu tanpa menggeser teks, disertai animasi rotasi spring/elastic logo NK (`rotate(-180deg) scale(0.4) -> rotate(0deg) scale(1)`).
  - **Tata Letak Responsif**:
    * `.start-grid`: 2 kolom di tablet/desktop, 4 kolom di layar lebar `>= 1400px`, 1 kolom di HP `<= 600px`.
    * `.activities-two-grid`: 2 kolom di tablet/desktop (kartu ganjil terakhir span penuh), 12 kolom di `>= 1400px` (4 kartu span 3, 3 kartu span 4), 1 kolom di HP `<= 600px`.
    * HP (`<= 600px`): Nomor urut, judul, dan panah tertata dalam 1 baris, tombol `max-width: calc(100% - 76px)` dan maskot chibi 62px di pojok kanan bawah.


---

## 5. Perawatan & Pengelolaan Fitur Chat Sora

Fitur bot obrolan maskot Sora beroperasi melalui berkas **js/sora.js** dan halaman **sora/index.html**:

### A. Logika Balasan Lokal (Mode Offline)
- Sora memiliki fungsi balasan lokal (fallbackReply) di berkas js/sora.js yang bekerja tanpa memerlukan koneksi server internet.
- Jawaban dipicu oleh pola kata kunci (regex). Cara merawat dan menambah wawasan Sora:
  - Tambahkan pengenalan pola kata baru di fungsi fallbackReply (misalnya pertanyaan tata bahasa, kanji, salam, atau info klub).
  - Tulis balasan Sora dengan kepribadian khasnya: ceria, ramah, senang menyemangati (Ganbatte!, Yatta! ✨), dan selalu membantu mengarahkan pengunjung ke halaman web terkait (seperti Kelas Dasar, Kelas Lanjutan, atau Kamus Kanji).

### B. Koneksi API Eksternal
- Jika di masa depan Sora dihubungkan dengan kecerdasan buatan luar (AI Server), koneksi dilakukan melalui variabel global window.SORA_API_ENDPOINT.
- **Aturan Keamanan**: Kunci rahasia API (API key) tidak boleh ditulis langsung di dalam kode JavaScript frontend ini demi menjaga keamanan sistem.

---

## 6. Sistem Motion & Animasi Masuk Halaman (Native Motion Engine)

Website Mirai no Webu menerapkan animasi masuk (*page entrance motion*) dan scroll reveal yang anggun, modern, dan ringan tanpa dependensi pustaka berat:

### A. Standar Native Web (Zero External Dependency)
- Seluruh animasi memanfaatkan **CSS3 Keyframes** teroptimasi dan standar W3C **Cross-Document View Transitions API** (`@view-transition { navigation: auto; }`).
- **Animasi Masuk (`pageFadeIn` & `contentSlideIn`)**:
  - Halaman dimuat dengan transisi lembut ke atas (`translateY(16px)` ke `translateY(0)`) dan opacity `0` ke `1` menggunakan kurva easing perlambatan halus `cubic-bezier(0.16, 1, 0.3, 1)`.
  - Komponen hero, judul (`h1`), subjudul (`p`), dan kartu aksi mengalir berjenjang (*staggered reveal*) dengan jeda `0.06s` - `0.16s`.
- **Scroll Motion Reveal Per Seksi Halaman (`setupReveal`)**:
  - Animasi masuk tidak hanya berlaku saat pertama kali membuka halaman (di hero atas), melainkan **berlaku aktif saat pengunjung menggulir layar (*scrolling*) dan tiba di setiap seksi/bagian halaman baru**:
  - Seluruh seksi konten (`main > section`, `.section`, `.proker-section`, dll.) otomatis didaftarkan sebagai `.section-reveal` ke pipeline `IntersectionObserver` di `js/main.js`.
  - Ketika suatu seksi tiba/masuk ke dalam layar, seksi tersebut baru memicu animasi masuknya (`translateY(28px)` ke `0`), disusul judul seksi (`.heading`/`h2` jeda `0.06s`) dan subjudul (`p` jeda `0.14s`).
  - Seluruh kartu komponen (`article`, `[class*='-card']`, dll.) di dalam seksi tersebut mengalir muncul bertahap (*staggered reveal: 0.06s s.d 0.46s*), menghidupkan suasana website seolah konten baru menyambut pengunjung saat tiba di tiap bagian halaman.
- **Aksesibilitas & Kepatuhan Gerak**:
  - Wajib menghormati preferensi pengguna dengan `@media (prefers-reduced-motion: reduce)`. Pengguna yang mematikan efek motion pada sistem operasi tidak akan dipaksa melihat animasi yang mengganggu kenyamanan mata.

---

## 7. Standar Halaman Penanganan Error 404 Kustom (404.html)

Halaman penanganan tautan salah (`404.html`) di root repositori wajib mempertahankan identitas khas Mirai no Hana dan dilarang disederhanakan menjadi teks polos kaku:
1. **Efek Kelopak Sakura Melayang (`.sakura-field`)**: Menggunakan animasi murni CSS3 untuk menghadirkan atmosfer visual jejepangan yang anggun di latar belakang kartu error.
2. **Maskot Sora & Gelembung Dialog Senpai**: Menampilkan avatar maskot Asora Aokita dengan animasi mengapung lembut (`mascotFloat`) dan gelembung pesan ramah yang menyapa senpai.
3. **Pencarian Cepat Cerdas (*Smart Quick Finder*)**: Menyediakan input teks pencarian instan yang cerdas mendeteksi kata kunci (*kanji, kelas, proker, lomba, tentang, sora*) dan otomatis mengarahkan pengunjung ke halaman yang tepat.
4. **4 Kartu Destinasi Berpendar Wagara**: Menyediakan tombol kartu mini menuju **Beranda**, **Kelas Belajar**, **Kamus Kanji**, dan **Tanya Sora**.

---

## 8. Pengelolaan Basis Data Offline JSON & Vektor KanjiVG (Folder data/)

Seluruh data karakter, kosakata, dan goresan di website beroperasi murni secara offline melalui berkas lokal:
- **`data/kana.json`**: Menyimpan seluruh inventaris karakter Hiragana dan Katakana (Gojūon, Dakuon, Handakuon, Yōon, Sokuon).
- **`data/kanji.json`**: Menyimpan basis data lengkap 2.136 karakter Jōyō Kanji, terjemahan Bahasa Indonesia, serta bacaan On'yomi dan Kun'yomi.
- **`data/kanji-meta.json`**: Menyimpan metadata radikal, jumlah goresan (*stroke count*), dan tingkatan JLPT (N5 s.d N1).
- **`js/stroke-data.js`**: Menyimpan vektor koordinat kurva KanjiVG terkurasi (viewBox: `0 0 109 109`) untuk animasi goresan kanvas.
- **`data/stroke-coverage-manifest.json`**: Laporan cakupan status validasi goresan, sampel pengujian, dan catatan diskrepansi metadata.
- **Skrip Pemeliharaan & Validasi**:
  - `python3 skrip/arsip/validate_stroke_data.py`: Memvalidasi kelengkapan, viewBox, kurva path SVG, koordinat, dan konsistensi metadata tanpa mengubah berkas.
  - `python3 skrip/arsip/fetch_kanjivg_strokes.py --staging-only`: Menyiapkan pembaruan data ke berkas pementasan `js/stroke-data.tmp.js`.
  - `python3 skrip/arsip/fetch_kanjivg_strokes.py --apply`: Menerapkan pembaruan data secara atomik setelah validasi 100% lolos.
- **Aturan Sinkronisasi**: Jika ada penambahan kanji atau kosakata baru pada Kamus maupun Latihan Mandiri, pengembang **WAJIB menjalankan validator** untuk memastikan keselarasan data antara berkas JSON di `data/` dan pustaka goresan di `js/stroke-data.js` agar fitur pencarian dan animasi goresan tetap akurat.

---

## 9. Standar Keamanan Siber & Sanitasi Input

Untuk menjaga keamanan pengunjung dan integritas website:
1. **Pencegahan Celah XSS (Cross-Site Scripting)**:
   - Setiap teks dari pengguna yang dirender ke antarmuka (terutama obrolan bot Sora dan pesan masukan) **WAJIB disanitasi menggunakan DOMPurify**:
     ```javascript
     const cleanHTML = DOMPurify.sanitize(marked.parse(userInput));
     ```
   - Dilarang memasukkan teks mentah langsung ke `innerHTML` tanpa proses sanitasi.
2. **Kerahasiaan Kredensial & Kunci API**:
   - Dilarang keras menyimpan kunci rahasia (*API Key*), token autentikasi, atau kredensial berbayar di dalam berkas JavaScript frontend publik. Seluruh komunikasi AI luar wajib melalui gateway proxy aman.

---

## 10. Konvensi Pesan Git Commit (Conventional Commits)

Seluruh riwayat commit repositori wajib rapi dan seragam menggunakan bahasa Indonesia dengan format baku:
- **`feat:`** — Penambahan fitur atau halaman baru (contoh: `feat: buat halaman 404 estetik`).
- **`fix:`** — Perbaikan kesalahan kode atau bug (contoh: `fix: perbaiki toleransi goresan kana`).
- **`docs:`** — Pembaruan berkas dokumentasi markdown (contoh: `docs: perbarui agent.md dan README`).
- **`refactor:`** — Penataan ulang folder, pembersihan, atau perapian nama file tanpa mengubah fungsi web (contoh: `refactor: ganti nama berkas idc tanpa spasi`).
- **`style:`** — Perubahan gaya visual CSS atau tipografi tanpa mengubah logika skrip.
- **`chore:`** — Pemeliharaan konfigurasi perkakas atau skrip otomasi Python.

---

## 11. Protokol Universal Anti-Halangan Kontrol Mengambang (Floating Controls Auto-Hide)

Website Mirai no Hana memiliki elemen kontrol mengambang global yang selalu menempel di layar (*fixed overlay*), yaitu:
- **Tombol Menu Navigasi** (`.menu-btn`) di pojok kanan atas.
- **Tombol Launcher Chat Sora** (`#launcher` & `.sora-widget`) di pojok kanan bawah.
- **Tombol Kembali ke Atas** (`.to-top`) di pojok kanan bawah.
- **Sidebar Ikon Media Sosial Hero** (`.hero-social-sidebar`) di pojok kanan hero (sejajar horizontal dengan judul hero).

### Aturan Wajib Anti-Halangan (Sekarang & Fitur Mendatang):
1. **Otomatis Bersembunyi Saat Ada Fitur/Modal yang Dibuka**:
   Setiap kali ada fitur interaktif yang menutupi layar atau memerlukan fokus pengguna sedang berjalan/dibuka, seluruh tombol kontrol mengambang di atas **WAJIB otomatis bersembunyi / tertutup** (`opacity: 0 !important; visibility: hidden !important; pointer-events: none !important; transform: translateY(12px) scale(0.88) !important;`):
   - **Latihan Mandiri Kana** (`.practice-view`, `.result-view`, `body.is-practicing`).
   - **Chatbot Asora Aokita (Sora)** (`#drawer.open`, `#drawer.fullscreen`, `body.sora-drawer-open`, `body.sora-fullscreen-active`, `.sora-panel`).
   - **Sidebar Navigasi Menu** (`.sidebar-nav.active`, `body.sidebar-open`).
   - **Lightbox Peninjau Foto** (`.img-lightbox.is-open`, `.lightbox.active`, `body.lightbox-open`).
   - **Seluruh Modal & Dialog Masa Depan** (`.modal.is-open`, `.modal.active`, `dialog[open]`, `[role="dialog"].is-open`).
2. **Pemulihan Otomatis Saat Ditutup**:
   Begitu jendela/modal/chat/latihan tersebut ditutup, seluruh kontrol mengambang **wajib otomatis muncul kembali** secara mulus tanpa memerlukan tindakan manual dari pengunjung (`transition: opacity 0.25s ease, visibility 0.25s ease, transform 0.25s ease`).
3. **Pemberlakuan CSS & JS Dual-Layer**:
   - Lapisan CSS menggunakan selector canggih `body:has(...)` untuk deteksi otomatis tanpa bergantung penuh pada JS.
   - Lapisan JavaScript menyediakan penanda kelas status di `document.body` (`.is-practicing`, `.sora-drawer-open`, `.sora-fullscreen-active`, `.sidebar-open`, `.lightbox-open`) untuk kompatibilitas mutlak 100% di semua peramban.
   - Setiap penambahan fitur overlay atau modal baru di masa depan **WAJIB mematuhi protokol ini**.

### Media Sosial Resmi & Efek Hero Parallax:
1. **Dua Saluran Komunikasi Resmi Klub**:
   - **Instagram**: `https://www.instagram.com/mirainohana_smawh2?utm_source=ig_web_button_share_sheet&stkn=ZDNlZDc0MzIxNw==` (`@mirainohana_smawh2`).
   - **TikTok**: `https://www.tiktok.com/@nihongo.kurabu.wh2?is_from_webapp=1&sender_device=pc` (`@nihongo.kurabu.wh2`).
2. **Hero Sticky Curtain Reveal & Scroll-Ascending Content (Universal 100% di Seluruh 29 Halaman Hero)**:
   - Seluruh banner hero di website (`.hero`, `.page-hero`, `.proker-hero`, `.quest-hero`, `.about-hero`, `.activities-hero`, `.class-hero`, `.motivasi-hero`, `.rekomendasi-hero`, `.peringkat-hero`, `.lomba-hero`, `.buuku-hero`, `.toko-hero`) **WAJIB menerapkan arsitektur *Sticky Curtain Reveal*** (`position: sticky !important; top: 0 !important; z-index: 1 !important;`).
   - Dilarang keras menimpa hero dengan `position: relative !important`, agar gambar latar Sora selalu **ketinggal dan menetap diam di layar** tanpa pergeseran background (bebas 100% dari celah hitam), sementara seksi materi/konten di bawahnya meluncur naik dengan elevasi bayangan tebal (`box-shadow: 0 -35px 85px rgba(0, 0, 0, 0.98); z-index: 12;`) dan background solid padat menutupi / "memakan" hero secara fisik saat di-scroll.
   - **Teks Judul & Tombol Medsos Bergerak Naik Tanpa Transparansi**: Melalui `setupHeroContentScroll()` di `main.js`, teks judul (baik di Beranda maupun subhalaman) dan tombol medsos bergerak naik ke atas secara proporsional (`translate3d(0, -scrollY, 0)`) mengikuti scroll halaman. Seluruh style transparansi/opacity dihapus total (`color: #ffffff; opacity: 1 !important;`), sehingga teks tetap tajam, padat, dan solid saat naik.
   - **Protokol Visibilitas Seketika Tirai Pertama (Above-the-Fold Instant Visibility)**:
     - Seksi pertama tepat di bawah hero (`.hero + section, .page-hero + section, .proker-hero + section, .quest-hero + section, .toko-catalog-section`) dan seluruh elemen di dalamnya (judul, filter tab, kartu di viewport awal) **DILARANG disembunyikan dengan `opacity: 0`**.
     - Seksi tersebut wajib memiliki status visibilitas langsung (`opacity: 1 !important; transform: none !important; visibility: visible !important;`) agar saat halaman pertama kali dibuka, tidak ada kekosongan/ruang hitam kosong (*black void gap*), dan langsung menampilkan konten etalase/katalog secara utuh layaknya halaman lainnya.
   - Ikon media sosial di pojok kanan hero Beranda berdesain lingkaran kaca Tengoku style (`backdrop-filter: blur(8px)`, pendar pink saat disentuh mouse), posisinya sejajar vertikal dengan teks judul hero (`bottom: 15%` pada desktop, `bottom: 12%` pada mobile).

---

## 12. Protokol Dokumentasi Hidup Terpadu (Living Documentation & Auto-Sync Protocol)

Seluruh berkas dokumentasi di repositori Mirai-No-Webu berprinsip sebagai **Dokumentasi Hidup (*Living Documentation*)** yang wajib selalu mutakhir (*up-to-date*) dan sinkron dengan kondisi kode riil saat ini.

### Kewajiban Sinkronisasi Otomatis Setiap Ada Perubahan:
Setiap kali Agent atau pengembang melakukan modifikasi kode, penambahan fitur, pemindahan/penghapusan berkas, atau penyesuaian aturan, **WAJIB langsung memperbarui berkas dokumentasi terkait secara serentak**:

1. **Pembaruan `panduan/agent.md`**:
   - Wajib mencatat aturan desain baru, parameter teknis (misal: rasio kuas, toleransi algoritma, selector CSS, class JS), atau keputusan arsitektur yang disepakati bersama pengguna.
   - Menjadi sumber kebenaran tunggal (*Single Source of Truth*) bagi perilaku AI dan standar kualitas kode.

2. **Pembaruan `panduan/tree.md`**:
   - Wajib langsung menyinkronkan diagram pohon direktori jika ada penambahan berkas baru, penghapusan berkas, pemindahan folder, atau perubahan struktur sub-direktori.
   - Diagram direktori dilarang usang atau memuat berkas yang sudah dihapus/dipindahkan.

3. **Pembaruan `README.md` (Root Repositori)**:
   - Wajib memperbarui ringkasan fitur jika ada fitur baru yang ditambahkan ke website.
   - Wajib memperbarui bagan direktori ringkas di Bab 4 agar selalu selaras dengan `panduan/tree.md`.
   - Wajib memperbarui tabel **Sources & Credits** (Bab 5) jika ada pustaka eksternal, font, aset, atau API baru yang mulai digunakan dalam proyek.

4. **Pembaruan Sub-Dokumentasi Tematik**:
   - **`data/README.md`**: Wajib diperbarui jika ada berkas JSON baru, perubahan skema kolom, atau penambahan dataset offline.
   - **`skrip/README.md`**: Wajib diperbarui jika ada skrip Python otomasi baru yang ditambahkan atau skrip usang yang dibersihkan.

5. **Prinsip Satu Kesatuan Komit (*Atomic Documentation Commits*)**:
   - Pembaruan dokumentasi harus dilakukan bersamaan dengan kode perubahannya (atau dalam commit dokumentasi lanjutan langsung) agar tidak pernah ada jeda waktu di mana dokumentasi tertinggal dari implementasi kode (*zero documentation drift*).

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

