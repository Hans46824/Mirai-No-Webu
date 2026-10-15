# Workspace Rules & Otak Otomatis — Mirai No Webu

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
