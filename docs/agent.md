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
- **Root (`/`)**: Hanya menyisakan **index.html** sebagai gerbang utama Beranda.
- **`css/`**: Berisi master stylesheet antarmuka (`css/style.css`).
- **`js/`**: Berisi seluruh logika JavaScript modular (`main.js`, `script.js`, `kanji.js`, `kana.js`, `stroke.js`, `stroke-data.js`, `sora.js`, dll.).
- **`docs/`**: Berisi dokumentasi arsitektur proyek (`docs/tree.md`, `docs/agent.md`) dan pedoman PDF (`docs/kurikulum/`).
- **`data/`**: Berisi basis data lokal JSON (`kana.json`, `kanji.json`, `kanji-meta.json`) yang menyuplai data untuk Kamus dan Latihan Kana/Kanji.
- **`tentang/`**: Profil lengkap klub Mirai No Hana (`index.html`).
- **`lomba/`**: Informasi 18 lomba & festival jejepangan (`index.html`).
- **`peringkat/`**: Papan peringkat keaktifan, presensi, & galeri prestasi (`index.html`).
- **`rekomendasi/`**: Rekomendasi media belajar anime, film, dan musik (`index.html`).
- **`kelas/`**: Hub pembelajaran mandiri (`index.html`, `dasar.html`, `lanjutan.html`, `kurikulum.html`, `latihan.html`, `motivasi.html`).
- **`divisi/`**: Struktur 4 divisi resmi klub (`index.html`, `bahasa.html`, `cosplay.html`, `desain.html`, `kewirausahaan.html`).
- **`kegiatan/`**: Hub program kerja & fasilitas (`index.html`), `kimi-to-nippon.html` (orientasi KTN), `nihon-go-rajio.html` (siaran NJR), `konbini.html`, `ramadhan.html`, dan `tomodachi.html`.
- **`kamus/`**: Kamus interaktif pencarian Kana & Kanji (`index.html`) dan Ensiklopedia Kanji (`kanji.html`).
- **`materi/`**: Modul pembelajaran terperinci (`materi/dasar/` dan `materi/lanjutan/`).
- **`sora/`**: Playground bot obrolan maskot Sora (`index.html`).
- **`skrip/`**: Kumpulan skrip otomasi & pemeliharaan kode Python.
- **Folder `video/` telah dihapus** agar repositori bersih dari berkas rekaman lokal yang tidak terpakai.

---

## 2. Inventaris Sumber Daya Gambar & Berkas (Colocation & Shared)

Aset visual dikelompokkan berdasarkan halaman yang menggunakannya:

### A. Aset Bersama / Global (Folder images/mirai/)
- **background/**: Pola Wagara master CSS (`w1b.jpeg`, `w1w.jpeg`, `c1b.jpeg`, `c1w.jpeg`, `w2w.jpeg`, `chat.jpeg`, `Sora.png`).
- **logo/**: Logo resmi klub (`MNH1.png`, `MNH1-nav.png`, `NK.png`, `comingsoon.jpg`).
- **icon/**: Koleksi 20 stiker chibi resmi Genshin Impact untuk profil anggota, papan peringkat, dan dekorasi kartu modul (Al, Ay, Chi, Fa, Fli, Fu, Hu, Ka, Ki, Lo, Wa, ang, bal, bul, chi, cil, dil, nah, sar, zho).
- **stiker/**: Berisi 28 stiker komunitas ekspresi anime untuk kutipan dan asisten Sora.

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

### A. Konsep Selang-Seling Hitam dan Putih
- Halaman web (terutama halaman profil Tentang dan penjelasan proker) menggunakan sistem seksi warna selang-seling antara hitam dan putih.
- Tujuannya menjaga ritme membaca pengunjung agar mata tidak cepat lelah saat menggulir halaman panjang.
- Seksi hitam memakai warna latar gelap (#111111 atau #0e0d13) dengan teks putih bersih.
- Seksi putih memakai latar putih murni (#ffffff) dengan teks warna abu gelap pekat (#18151b).

### B. Background Hero Tiap Halaman
- Tidak semua halaman wajib memiliki background hero gambar besar.
- Halaman utama (Beranda, Tentang, Kegiatan, Papan Peringkat, Lomba) memiliki hero visual yang menonjol dan menarik perhatian.
- Halaman fokus materi (Kelas Dasar, Kelas Lanjutan, Kamus, Kurikulum) memakai hero minimalis tanpa gambar berat, agar pengguna langsung fokus ke modul pembelajaran.

### C. Aturan Pola Background (Pattern) & Selang-Seling Tiap Halaman Menu
- **Aturan Selang-Seling 8 Halaman Menu Utama**: Motif pola pada tiap kartu diatur berselang-seling mengikuti urutan menu navigasi dari awal sampai akhir:
  1. **Beranda**: Menggunakan Pola Awan Kumo — **c1b.jpeg** (kartu seksi gelap) & **c1w.jpeg** (kartu seksi terang).
  2. **Kelas**: Menggunakan Pola Ombak Wagara Seigaiha — **w1b.jpeg** (kartu seksi gelap) & **w1w.jpeg** (kartu seksi terang).
  3. **Kamus**: Menggunakan Pola Awan Kumo — **c1b.jpeg** (kartu seksi gelap) & **c1w.jpeg** (kartu seksi terang).
  4. **Program & Fasilitas**: Menggunakan Pola Ombak Wagara Seigaiha — **w1b.jpeg** (kartu divisi & seksi fasilitas kelas/gelap) & **w1w.jpeg** (kartu program kerja/terang).
  5. **Rekomendasi**: Menggunakan Pola Awan Kumo — **c1b.jpeg** (kartu seksi gelap) & **c1w.jpeg** (kartu seksi terang).
  6. **Papan Peringkat**: Menggunakan Pola Ombak Wagara Seigaiha — **w1b.jpeg** (kartu podium & tabel gelap) & **w1w.jpeg** (kartu terang).
  7. **Lomba & Acara**: Menggunakan Pola Awan Kumo — **c1b.jpeg** (kartu acara gelap) & **c1w.jpeg** (kartu detail terang).
  8. **Tentang**: Menggunakan Pola Ombak Wagara Seigaiha — **w1b.jpeg** (kartu seksi gelap) & **w1w.jpeg** (kartu seksi terang).
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
  - Biru (#38bdf8 / #0284c7): Tingkat Sidoarjo, Jawa Timur, dan informasi teknis.
  - Hijau (#10b981 / #34d399): Tingkat Surabaya, status pendaftaran buka, presensi hadir.
  - Oranye / Emas (#f97316 / #f59e0b): Tingkat provinsi, juara perunggu dan emas, status perhatian.
  - Merah (#f43f5e / #e11d48): Tingkat nasional, status pendaftaran ditutup, batas akhir waktu.
  - Ungu (#a855f7 / #c084fc): Kategori acara festival cosplay dan ruang maskot Sora.

### F. Aturan Judul Tiap Halaman (Heading)
- Gunakan gaya Two-Tone: Teks judul berwarna putih atau hitam dipadukan dengan kata kunci penting berwarna pink sakura di dalam tag span.
- Judul harus berbobot tegas (font-weight 800 ke atas) dan proporsional di layar laptop maupun ponsel.
- Dilarang memakai penomoran angka berawalan nol (seperti 01 atau 02) dan dilarang memakai garis miring (/) yang kaku.
- **Judul Bersih Mandiri**: Pada seksi spesifik seperti Fasilitas, judul dibuat mandiri tanpa kicker/sub-judul atau deskripsi bertele-tele yang membuang ruang.

### G. Aturan Bahasa Antarmuka (Hanya Bahasa Indonesia & Bahasa Jepang)
- Seluruh teks tampilan website (judul, deskripsi, tombol, menu navigasi, badge, petunjuk kuis, dan pesan) **WAJIB murni menggunakan Bahasa Indonesia** sebagai bahasa pengantar dan **Bahasa Jepang** (Kanji, Hiragana, Katakana, dan Romaji) untuk materi pembelajaran klub.
- **Dilarang keras memakai Bahasa Inggris yang tidak perlu** pada teks yang dilihat pengunjung web. Selalu gunakan padanan Bahasa Indonesia yang luwes (misalnya: hindari *Level*, *Challenge*, *Overview*, *Coming Soon* jika ada padanan tepat seperti *Tingkat/Level*, *Tantangan*, *Ringkasan*, *Segera Hadir*).
- Gunakan bahasa manusia yang hangat, santai, dan bersahabat seperti gaya komunikasi anak muda sekolah. Hindari istilah kaku buatan mesin AI.

### H. Aturan Deskripsi dan Teks Pendukung
- Deskripsi harus padat dan ringkas (cukup 2 sampai 3 baris kalimat).
- Di latar gelap, warna teks deskripsi menggunakan abu-abu lembut (#cbd5e1 atau #94a3b8), bukan putih murni 100%, agar kontrasnya nyaman di mata.

### H. Aturan Tombol
- Sudut tombol melengkung halus dan modern (border-radius: 12px), bukan kotak kaku dan bukan oval lonjong.
- Memakai warna gradien pink sakura dengan bayangan berpendar lembut (glow).
- Saat disorot mouse (hover), tombol naik sedikit (translateY -2px) dan pendaran warnanya semakin menyala.
- Ukuran tombol harus pas dan proporsional dengan isi teksnya (tidak boleh melar memenuhi seluruh kartu).

### I. Aturan Penataan Foto, Poster, dan Avatar
- **Frame 1 Poster & Carousel Geser Mandiri**: Wadah poster di kartu event wajib berukuran 1 poster tunggal yang utuh (Single Poster View), tidak boleh menampilkan poster bertumpuk vertikal ataupun berdampingan terpotong:
  - Jika event memiliki lebih dari 1 poster/halaman (seperti ITS & UNESA), gunakan carousel horizontal yang bisa digeser dengan panah, drag mouse di desktop, atau swipe jari di HP.
  - **Tombol Panah Navigasi**: Wajib berada tepat di **bagian tengah samping kiri (‹) dan kanan (›)** poster dengan gaya semi-transparan ber-blur dan efek pendar pink saat disorot. Jika poster hanya ada 1 lembar, tombol panah otomatis disembunyikan.
  - **Tanpa Keterangan Counter Angka & Tag Watermark**: Dilarang menampilkan teks counter angka (seperti "1 dari 2") serta label tag watermark institusi/univ (seperti "POSTER RESMI ITS", dll).
  - **Tombol Aksi Semantik & Navigasi Langsung (Tanpa Pop-up Juknis)**:
    - Tombol aksi kartu dibedakan secara tegas: **"🔗 Buka Link Lomba"** untuk kategori lomba, dan **"🔗 Buka Link Acara Jejepangan"** untuk kategori festival/acara.
    - **Langsung Mengarah ke Tautan Eksternal**: Tombol langsung membuka tautan tujuan di tab baru (`target="_blank" rel="noopener noreferrer"`). Untuk sementara seluruh tombol diarahkan ke Instagram resmi Nihongo Kurabu Mirai No Hana (`https://www.instagram.com/mirainohana_smawh2`), bukan membuka pop-up modal juknis internal.
  - **Bebas Interaksi Tanpa Jebakan (No Lock-In)**: Poster murni menjadi visual kartu yang aman disentuh, di-drag, atau di-scroll tanpa memicu modal lightbox yang mengunci scroll layar (`overflow: hidden`). Navigasi halaman poster kedua dilakukan murni via tombol panah tengah samping atau swipe.
- **Avatar Lingkaran**: Wadah avatar profil atau juara wajib memiliki latar belakang putih (#ffffff) dengan gambar berukuran contain dan sedikit padding, agar bagian telinga, rambut, atau topi chibi tidak terpotong garis tepi lingkaran.

### J. Aturan Spasi dan Tata Letak (Layout)
- **Anti Ruang Hampa**: Di layar laptop, kartu tidak boleh menyisakan ruang kosong hitam atau putih yang melompong di tengah antara judul dan tombol bawah. Susun elemen secara padat dan seimbang.
- **Pemusatan Kartu Ganjil**: Jika jumlah kartu dalam satu seksi berjumlah ganjil (seperti 11 kartu pengurus Kabinet Clover), kartu pada baris terakhir diletakkan tepat di posisi tengah (rata tengah), tidak boleh miring sendirian di sebelah kiri.
- **Keseragaman Kartu Program Kerja & Divisi**: Ukuran kartu Program Kerja (tinggi, padding, border-radius, font judul, dan posisi tombol) wajib disamaratakan persis dengan kartu Divisi agar tampilan sejajar dan rapi.
- **Format Kartu Fasilitas Landscape**: Fasilitas Mirai no Hana menggunakan format kartu Landscape memanjang (2 kartu: Ruang Pertemuan dan Mirai no Webu). Deskripsi kartu Mirai no Webu diselaraskan dengan teks Beranda, dan tombol aksi di bawah digantikan oleh badge status resmi.
- **Grid Penelusuran Beranda (6 Kartu)**: Menu kartu beranda menyusun 6 kartu seimbang (1. Struktur Divisi, 2. Program Kerja, 3. Fasilitas, 4. Rekomendasi, 5. Papan Peringkat, 6. Lomba & Acara).
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
  - **Ketebalan Garis Lebih Nyata & Nyaman**: Garis kanvas tulisan tangan dinaikkan ke ketebalan `17px` (rasio kanvas), garis goresan selesai `17px`, dan panduan putus-putus `15.5px` (pada animasi kamus dinaikkan menjadi `4.2px` untuk kuas tebal), memberikan sapuan visual yang tegas, tebal, dan mudah terlihat jelas di berbagai layar.
  - **Akurasi Bentuk Kana Standar Terkurasi (Ko, Fu, Katakana Ko, dll.)**: Path SVG goresan kana diselaraskan secara presisi dengan bentuk glif buku teks resmi bahasa Jepang. Karakter `こ` (dan `ご`) menggunakan goresan horizontal pertama yang bersih dan tegas tanpa bengkokan kail aneh di ujung; Katakana `コ` (dan `ゴ`) menggunakan sudut siku-siku tegak 90° yang tegas; serta Hiragana `ふ` (dan `ぶ`, `ぷ`) disusun menggunakan 4 goresan kurva natural (titik atas, kurva sapuan tengah yang lembut tanpa gembungan balon terbalik, titik kiri, dan titik kanan) sehingga 100% konsisten dengan gambar visual huruf di kamus.
  - **Toleransi Keakuratan Bersahabat (Menceng Dikit Tetap Benar)**: Validasi memeriksa kedekatan titik awal (≤21.5 unit), titik akhir (≤22.5 unit), panjang goresan (≥44%), cakupan kurva (coverage ≥52%), deviasi rata-rata (≤16.8 unit), deviasi maksimal (≤29.5 unit), dan arah progresif. Tetap menolak sentuhan/geseran mini tanpa bentuk dan arah terbalik, namun memberikan toleransi ekstra ramah sentuhan untuk menoleransi sedikit deviasi bentuk antara gambar huruf dan goresan kanvas (*menceng dikit ada koreksi benarnya*).
- **Pola Motif Kartu & Tipografi Latihan Kana (`latihan.html`)**:
  - **Pola Motif Kartu Level (Hiragana vs Katakana)**:
    - Kartu Hiragana menggunakan motif Wagara ombak gelap (`images/mirai/background/w1b.jpeg`) via `.level-card--hiragana::after` / `[data-script="hiragana"] .level-card::after`.
    - Kartu Katakana menggunakan motif awan Kumo gelap (`images/mirai/background/c1b.jpeg`) via `.level-card--katakana::after` / `[data-script="katakana"] .level-card::after`.
    - Keduanya menggunakan `mix-blend-mode: screen` dengan opacity halus (0.045 hingga 0.08 saat hover) agar menyatu anggun di atas kartu tanpa mengganggu keterbacaan teks.
  - **Pola Motif Kartu Latihan Gabungan (`.mode-card`)**:
    - Kartu mode campuran bersifat adaptif terhadap skrip kana yang sedang aktif:
      - **Saat membuka Hiragana**: Menggunakan motif Wagara ombak terang (`images/mirai/background/w1w.jpeg`) dengan `mix-blend-mode: multiply` dan opacity 0.10 (0.16 saat hover) pada tema terang, dan berganti ke `w1b.jpeg` pada tema gelap (`body.theme-dark`).
      - **Saat membuka Katakana**: Menggunakan motif Kumo awan terang (`images/mirai/background/c1w.jpeg`) dengan `mix-blend-mode: multiply` dan opacity 0.10 (0.16 saat hover) pada tema terang, dan berganti ke `c1b.jpeg` pada tema gelap (`body.theme-dark`).
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
