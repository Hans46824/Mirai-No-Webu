<!-- cspell:disable -->
# Panduan Utama & Aturan Kerja Mirai No Webu

Dokumen ini adalah pegangan resmi bagi pengembang dan AI asisten untuk merawat, memperbarui, serta mengembangkan website **Mirai no Webu** (Klub Bahasa & Kebudayaan Jepang MIRAI NO HANA SMASYIMDUTA Sidoarjo). 

Gunakan bahasa yang sederhana, manusiawi, dan langsung ke intinya. Hindari penulisan kode rumit di dokumen ini supaya nyaman dibaca oleh siapa pun.

---

## 1. Aturan Wajib: Pembaruan Mandiri Dokumentasi
- Setiap kali ada halaman baru, file script baru, atau aset gambar baru yang diunggah ke proyek, AI WAJIB langsung memperbarui dokumen **agent.md** dan **tree.md**.
- Jangan hanya mengubah kode web tanpa mencatat perubahannya di dokumentasi. Struktur direktori dan aturan desain harus selalu selaras dengan kondisi web terkini.

### A. Arsitektur Folder Modular (Clean Root Standard)
Seluruh berkas website Mirai no Webu dikelompokkan secara terstruktur ke dalam folder tematik:
- **Root (`/`)**: Berisi **index.html** (gerbang utama Beranda), **404.html** (halaman penanganan error ramah pengunjung bertema Mirai no Hana), dan **README.md** (etalase profil repositori GitHub dan dokumentasi kredit).
- **`css/`**: Berisi master stylesheet antarmuka (`css/style.css`).
- **`js/`**: Berisi seluruh logika JavaScript modular (`main.js`, `script.js`, `kanji.js`, `kana.js`, `stroke.js`, `stroke-data.js`, `sora.js`, dll.).
- **`panduan/`**: Berisi dokumentasi arsitektur proyek (`panduan/tree.md`, `panduan/agent.md`).
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
- **`skrip/`**: Kumpulan skrip otomasi & pemeliharaan kode Python.
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

---

## 2. Inventaris Sumber Daya Gambar & Berkas (Colocation & Shared)

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

## 3. Aturan Desain & Tampilan Visual

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

### B. Aturan Latar Belakang Hero (Clean Hero & Sticky Curtain Reveal Rule)
- **Aturan Judul Bersih Hero (Clean Hero Rule)**:
  - Pada halaman yang memiliki gambar latar maskot Sora (`background-image: url("../images/mirai/background/Sora.png")`), area hero **HANYA BOLEH menampilkan judul halaman murni (`<h1>`)** tanpa teks kicker/eyebrow, tanpa subjudul, dan tanpa paragraf pengantar.
  - Tujuannya agar visual ilustrasi karakter Sora tampil megah, bersih, lapang, dan tidak tertutup tumpukan teks yang berantakan.
  - Contoh: Pada halaman Toko, judul hero murni berupa `<h1 class="page-title">Toko</h1>` tanpa embel-embel teks lainnya.
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

### D. Penggunaan Ikon Chibi: Jangan Sampai Mendominasi
- Ikon chibi diletakkan di sudut kartu (.card-corner-chibi) atau avatar peringkat sebagai aksen pemanis desain saja.
- Ikon chibi **TIDAK BOLEH mendominasi tampilan kartu**.
- Tidak masalah jika stiker atau elemen lain menimpa bagian chibi. Yang paling utama adalah **isi teks dan fungsi web**.
- Jangan pernah mengorbankan keterbacaan materi atau tatanan tata letak hanya demi memperlihatkan gambar chibi.

### E. Skema Warna Web (Pink, Putih, Hitam + Multi-Color)
- Warna pondasi klub: Pink sakura (#ff4f91 dan #e91e63), putih (#ffffff), dan hitam gelap (#09090d / #111115).
- Warna aksen (multi-color) wajib digunakan pada lencana, label tingkat, dan status agar tampilan tidak monoton:
  - Biru (#38bdf8 / #0284c7): Tingkat Sidoarjo, Jawa Timur, status Segar & Hangat kuliner, dan informasi teknis.
  - Hijau (#10b981 / #34d399): Tingkat Surabaya, status Tersedia produk, status pendaftaran buka, presensi hadir.
  - Oranye / Emas (#f97316 / #f59e0b): Tingkat provinsi, status Pra-Pesan (PO), juara perunggu dan emas, status perhatian.
  - Merah (#f43f5e / #e11d48): Tingkat nasional, status pendaftaran ditutup, batas akhir waktu.
  - Ungu (#a855f7 / #c084fc): Kategori acara festival cosplay dan ruang maskot Sora.

### F. Aturan Judul Bersih Tanpa Deskripsi Pengantar (Clean Standalone Headings Rule)
- **Aturan Mutlak: Pengguna Tidak Menyukai Judul yang Diberi Deskripsi Pengantar**:
  - Dilarang keras menaruh teks deskripsi, subjudul, atau paragraf pengantar (`<p class="section-desc">...`) tepat di bawah judul hero halaman maupun di bawah judul seksi (`.section-intro .heading`).
  - Judul wajib tampil bersih, percaya diri, elegan, dan mandiri (*clean standalone heading*).
  - Contoh penerapannya:
    - Judul hero hanya menampilkan judul halaman murni: `<h1 class="page-title">Toko</h1>`.
    - Judul seksi hanya menampilkan heading two-tone murni: `<h2 class="heading">Etalase <span>Koleksi Produk</span></h2>`, `<h2 class="heading">Cara <span>Pemesanan</span></h2>`, dll., **tanpa ada `<p class="section-desc">` di bawahnya**.
- **Judul Hero Halaman (Hero Title)**:
  - Bersih mandiri, tegas, berbobot tebal (`font-weight: 800 - 900`, `letter-spacing: -0.08em`, `font-size: clamp(58px, 8vw, 116px)`).
  - Pada halaman Toko, judul hero adalah murni **"Toko"** (`<h1 class="page-title">Toko</h1>`).
- **Judul Seksi Halaman (Section Heading)**:
  - Gaya Two-Tone: Warna dasar (putih di seksi gelap / `#18151b` di seksi terang) dipadukan dengan kata kunci penting berwarna pink sakura di dalam tag `<span>`.
  - Format rata kiri seragam (`.heading`), tanpa penomoran angka 01/02, dan tanpa garis miring (/) yang kaku.
- **Judul pada Kartu (Card Title)**:
  - Berukuran proporsional (`16px` - `18px`, `font-weight: 800`).
  - Langsung menamai entitas produk/fitur/materi secara spesifik, padat, dan tidak berulang.
  - Didukung metadata tipografi aksara Jepang jika relevan (`.toko-jp-name` bergaya *Noto Serif JP* warna pink).

### G. Aturan Bahasa Antarmuka (Pemberantasan Bahasa Inggris yang Tidak Perlu)
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
- Gunakan bahasa manusia yang hangat, santai, dan bersahabat seperti gaya komunikasi anak muda sekolah. Hindari istilah kaku buatan mesin AI.

### H. Aturan Deskripsi dan Teks Pendukung (Card & Page Description Rule)
- **Etalase Produk Toko Bersih & Ringkas**:
  - Pada kartu produk Toko, dilarang menaruh deskripsi produk panjang (`.toko-card-desc`) dan dilarang menampilkan rating bintang ulasan (`.toko-rating`) agar kartu tampil bersih, rapi, dan berfokus pada foto produk, nama produk, spesifikasi teknis penting, harga, dan tombol aksi.
  - Pada halaman lain yang memerlukan deskripsi materi, deskripsi harus padat, informatif, dan ringkas (maksimal 2 sampai 3 baris kalimat).
- **Kontras Warna Teks**:
  - Di latar gelap: Warna teks menggunakan abu-abu lembut (`#cbd5e1` atau `#94a3b8`), bukan putih murni 100%, agar kontrasnya nyaman di mata dan tidak silau.
  - Di latar putih/terang: Warna teks menggunakan abu gelap pekat (`#554857` atau `#475569`), bukan hitam murni tajam, untuk kenyamanan membaca optimal.
- Dilarang membuat kalimat deskripsi bertele-tele, klise, atau membuang ruang visual kartu.

### I. Aturan Tombol
- Sudut tombol melengkung halus dan modern (border-radius: 12px), bukan kotak kaku dan bukan oval lonjong.
- Memakai warna gradien pink sakura dengan bayangan berpendar lembut (glow).
- Saat disorot mouse (hover), tombol naik sedikit (translateY -2px) dan pendaran warnanya semakin menyala.
- Ukuran tombol harus pas dan proporsional dengan isi teksnya (tidak boleh melar memenuhi seluruh kartu).

### J. Aturan Penataan Foto, Poster, dan Avatar
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

### K. Aturan Kanvas Display Putih untuk Produk Toko (White Product Canvas Rule)
- **Wadah Kanvas Display Putih (`.toko-thumb-canvas`)**:
  - Seluruh produk pada etalase Toko wajib menggunakan wadah/kartu alas display putih solid (`background: #ffffff; border-radius: 12px; box-shadow: ...`).
  - Tujuannya agar produk hasil potong latar belakang (seperti Lanyard, ID Card, Nametag, Pin, dan Cinderamata Akrilik) tidak memperlihatkan artefak tepian kasar atau halo putih saat diletakkan di kartu bernuansa gelap. Dengan kanvas putih, foto produk tampil bersih, estetik, dan tampak profesional layaknya pemotretan studio katalog.
- **Tampilan Khusus Haori (Duo View Depan & Belakang)**:
  - Pada produk Haori Resmi Klub, kanvas display menampilkan dua sudut pandang sekaligus: Tampak Depan (`haori-depan-new.png`) dan Tampak Belakang (`haori-belakang-new.png`) berdampingan dengan label indikator pill (`Depan` dan `Belakang`). Hal ini penting agar kaligrafi kanji punggung [未来の花] dan detail bordir depan terlihat jelas tanpa perlu berpindah halaman.
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

### L. Aturan Spasi dan Tata Letak (Layout)
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
  - **Sistem Modal Viewport-Fixed Mengikuti Pengguna**:
    - Tampilan latihan (`.practice-view`) dan hasil latihan (`.result-view`) wajib berposisi `fixed` viewport (`top: 0; left: 0; width: 100vw; height: 100vh; z-index: 99999; overflow-y: auto; display: flex; align-items: center; justify-content: flex-start`).
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

## 4. Perawatan & Pengelolaan Fitur Chat Sora

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

## 5. Sistem Motion & Animasi Masuk Halaman (Native Motion Engine)

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

## 6. Standar Halaman Penanganan Error 404 Kustom (404.html)

Halaman penanganan tautan salah (`404.html`) di root repositori wajib mempertahankan identitas khas Mirai no Hana dan dilarang disederhanakan menjadi teks polos kaku:
1. **Efek Kelopak Sakura Melayang (`.sakura-field`)**: Menggunakan animasi murni CSS3 untuk menghadirkan atmosfer visual jejepangan yang anggun di latar belakang kartu error.
2. **Maskot Sora & Gelembung Dialog Senpai**: Menampilkan avatar maskot Asora Aokita dengan animasi mengapung lembut (`mascotFloat`) dan gelembung pesan ramah yang menyapa senpai.
3. **Pencarian Cepat Cerdas (*Smart Quick Finder*)**: Menyediakan input teks pencarian instan yang cerdas mendeteksi kata kunci (*kanji, kelas, proker, lomba, tentang, sora*) dan otomatis mengarahkan pengunjung ke halaman yang tepat.
4. **4 Kartu Destinasi Berpendar Wagara**: Menyediakan tombol kartu mini menuju **Beranda**, **Kelas Belajar**, **Kamus Kanji**, dan **Tanya Sora**.

---

## 7. Pengelolaan Basis Data Offline JSON & Vektor KanjiVG (Folder data/)

Seluruh data karakter, kosakata, dan goresan di website beroperasi murni secara offline melalui berkas lokal:
- **`data/kana.json`**: Menyimpan seluruh inventaris karakter Hiragana dan Katakana (Gojūon, Dakuon, Handakuon, Yōon, Sokuon).
- **`data/kanji.json`**: Menyimpan basis data lengkap 2.136 karakter Jōyō Kanji, terjemahan Bahasa Indonesia, serta bacaan On'yomi dan Kun'yomi.
- **`data/kanji-meta.json`**: Menyimpan metadata radikal, jumlah goresan (*stroke count*), dan tingkatan JLPT (N5 s.d N1).
- **`js/stroke-data.js`**: Menyimpan vektor koordinat kurva KanjiVG terkurasi untuk animasi goresan.
- **Aturan Sinkronisasi**: Jika ada penambahan kanji atau kosakata baru pada Kamus maupun Latihan Mandiri, pengembang **WAJIB memastikan keselarasan data** antara berkas JSON di `data/` dan pustaka goresan di `js/stroke-data.js` agar fitur pencarian dan animasi goresan tetap akurat.

---

## 8. Standar Keamanan Siber & Sanitasi Input

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

## 9. Konvensi Pesan Git Commit (Conventional Commits)

Seluruh riwayat commit repositori wajib rapi dan seragam menggunakan bahasa Indonesia dengan format baku:
- **`feat:`** — Penambahan fitur atau halaman baru (contoh: `feat: buat halaman 404 estetik`).
- **`fix:`** — Perbaikan kesalahan kode atau bug (contoh: `fix: perbaiki toleransi goresan kana`).
- **`docs:`** — Pembaruan berkas dokumentasi markdown (contoh: `docs: perbarui agent.md dan README`).
- **`refactor:`** — Penataan ulang folder, pembersihan, atau perapian nama file tanpa mengubah fungsi web (contoh: `refactor: ganti nama berkas idc tanpa spasi`).
- **`style:`** — Perubahan gaya visual CSS atau tipografi tanpa mengubah logika skrip.
- **`chore:`** — Pemeliharaan konfigurasi perkakas atau skrip otomasi Python.

---

## 10. Protokol Universal Anti-Halangan Kontrol Mengambang (Floating Controls Auto-Hide)

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

## 11. Protokol Dokumentasi Hidup Terpadu (Living Documentation & Auto-Sync Protocol)

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



