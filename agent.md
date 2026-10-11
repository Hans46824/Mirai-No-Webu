<!-- cspell:disable -->
# Panduan Desain & Aturan Web Mirai No Webu

Dokumen ini rangkuman aturan desain, fungsi, dan gaya web Mirai no Webu yang disukai dan sudah diterapkan. Gunakan panduan ini setiap kali membuat atau mengubah halaman web. Penjelasannya singkat, padat, dan langsung ke intinya.

---

## 1. Konsep Halaman & Warna Selang-Seling Hitam Putih
- Web menerapkan konsep selang-seling seksi hitam dan putih (terutama di halaman Tentang dan penjelasan profil).
- Tujuannya supaya mata pengunjung tidak jenuh saat scroll ke bawah.
- Seksi hitam memakai warna dasar gelap (#111111 / #0e0d13) dengan teks putih.
- Seksi putih memakai latar putih bersih (#ffffff) dengan teks gelap (#18151b).

## 2. Background Hero Tiap Halaman
- Tidak semua halaman harus punya background hero gambar besar.
- Halaman utama (Beranda, Tentang, Kegiatan, Papan Peringkat) punya hero visual dengan nuansa tegas.
- Halaman materi dan modul (Kelas Dasar, Kelas Lanjutan, Kamus) memakai hero minimalis tanpa gambar berat, supaya pengunjung langsung fokus ke materi belajar.

## 3. Aturan Pattern (Pola Wagara) & Transparansi
- Aturan mutlak: Hanya 1 pattern dalam satu kartu. Dilarang menumpuk pattern di dalam kartu yang sama karena hasilnya tabrakan dan kotor.
- Transparansi pattern harus sangat halus (tipis saja sebagai tekstur mewah, bukan menutupi teks):
  - Kartu gelap: Memakai w1b.jpeg dengan transparansi sekitar 4.5% (opacity: 0.045), saat hover naik sedikit ke 8% (opacity: 0.08).
  - Kartu terang: Memakai w1w.jpeg dengan transparansi sekitar 3.5% sampai 4.5% (opacity: 0.035 - 0.045).

## 4. Penggunaan Ikon Chibi
- Ikon chibi (Genshin / maskot) ditaruh di pojok kartu atau avatar sebagai pemanis visual saja.
- Ikon chibi TIDAK BOLEH mendominasi tampilan kartu.
- Tidak masalah kalau chibi kena timpa stiker atau elemen lain. Yang paling utama adalah teks dan fungsi web.
- Jangan sampai keberadaan chibi merusak tata letak, menutupi info penting, atau bikin tulisan susah dibaca.

## 5. Skema Warna Web (Pink, Putih, Hitam + Multi-Color)
- Warna dominan: Pink sakura (#ff4f91 dan #e91e63), putih (#ffffff), dan hitam (#09090d / #111115).
- Warna pelengkap (multi-color) wajib ada pada badge, tag status, dan level agar web tidak monoton:
  - Biru: Wilayah Sidoarjo, tingkat Jatim, dan info teknis.
  - Hijau: Wilayah Surabaya, status pendaftaran buka, presensi hadir.
  - Oranye / Emas: Tingkat provinsi, juara perunggu/emas, status peringatan.
  - Merah: Tingkat nasional, status tutup, deadline penting.
  - Ungu: Kategori acara festival, cosplay, dan ruang Sora.

## 6. Aturan Judul Tiap Halaman (Heading)
- Gunakan gaya Two-Tone: Gabungan teks putih/hitam biasa dengan kata aksen pink yang dibungkus tag span.
- Judul harus tegas, bold, dan proporsional di layar laptop maupun ponsel.
- Dilarang keras memakai angka berawalan nol (01, 02) atau garis miring (/) yang kaku.

## 7. Aturan Deskripsi & Tulisan
- Deskripsi harus ringkas dan padat (cukup 2 sampai 3 baris saja).
- Warna teks deskripsi di tema gelap memakai abu-abu lembut (#cbd5e1 atau #94a3b8), bukan putih murni 100%, agar nyaman dibaca lama.
- Gunakan bahasa manusia yang ramah, santai, dan akrab khas pelajar/komunitas. Hindari bahasa kaku robot atau istilah klise AI.

## 8. Aturan Tombol
- Bentuk tombol memiliki sudut melengkung halus (border-radius: 12px), bukan kotak kaku dan bukan lonjong oval.
- Warna gradien pink sakura (#ff4f91 ke #e91e63) dengan bayangan pendar lembut (box-shadow).
- Saat disorot mouse (hover), tombol naik sedikit (translateY -2px) dan pendaran lebih terang.
- Ukuran tombol harus pas dan proporsional, tidak boleh melar memenuhi seluruh kartu.

## 9. Aturan Foto, Poster, & Avatar
- Jika ada 2 poster dalam satu kartu acara, jangan ditumpuk vertikal ke bawah yang membuat kartu melar tinggi.
- Gabungkan dalam 1 frame carousel hemat ruang:
  - Bisa digeser dengan swipe jari di HP/tablet.
  - Bisa digeser dengan tombol panah kiri-kanan (‹ dan ›).
  - Bisa digeser dengan drag mouse di laptop.
  - Bisa diklik untuk melihat foto ukuran penuh (popup lightbox).
  - Ada indikator halaman yang jelas (contoh: 1 dari 2).
- Avatar anggota/juara lingkaran harus berlatar putih (#ffffff) dengan gambar contain dan sedikit padding, supaya telinga atau topi karakter tidak terpotong garis tepi lingkaran.

## 10. Aturan Spasi & Tata Letak (Layout)
- Anti ruang hampa: Di layar laptop, dilarang ada ruang hitam/putih kosong melompong di tengah kartu. Isi secara padat dan seimbang dari atas ke bawah.
- Susunan kartu berjumlah ganjil: Jika jumlah kartu ganjil (seperti 11 kartu pengurus), baris terakhir wajib ditaruh di posisi tengah (rata tengah), tidak boleh jomplang sendirian di kiri.
- Format nama pengurus/anggota ditulis bersih tanpa embel-embel kelas jika diminta.
