# Contekan Cepat Peta Halaman & Berkas (Otak Otomatis)

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
