<!-- cspell:disable -->
# <font color="#ff4f91">MIRAI NO WEBU</font> — Pedoman & Karakter Desain

> Catatan pegangan buat AI dan pengembang saat mengerjakan website Mirai no Webu (Klub Jepang Mirai no Hana). Ditulis simpel, manusiawi, dan langsung ke intinya.

---

## 1. Siapa Kita & Karakter Website

- <font color="#ff4f91">Nama Website:</font> Mirai No Webu
- <font color="#a855f7">Organisasi:</font> Mirai no Hana Nihongo Kurabu (SMASYIMDUTA Sidoarjo)
- <font color="#38bdf8">Jiwa Klub:</font> Komunitas pelajar mandiri yang santai, kreatif, hangat, dan estetik. Bukan website sekolah formal yang kaku.
- <font color="#10b981">Teknologi:</font> Vanilla web murni (HTML5, CSS di style.css, JavaScript modular di js/). Tanpa framework berat supaya loading instan dan mudah diedit langsung.
- <font color="#f59e0b">Nuansa Warna:</font> Dominan tema gelap modern dengan aksen pendaran pink sakura (#ff4f91), diselingi seksi putih bersih yang kontras dan elegan di bagian filosofi.

---

## 2. Bedah 3 Halaman Utama

### A. Beranda (index.html)
Pintu masuk utama pengunjung. Kesan pertama harus langsung memikat:
- Bagian atas (Hero) langsung menampilkan judul tegas, tipografi berani, dan tombol aksi ke materi.
- Ada ringkasan profil klub dengan kartu bertekstur halus khas Jepang.
- Menghubungkan langsung ke modul belajar, interaksi maskot Sora, hingga form saran.

### B. Hub Kelas Belajar (kelas.html)
Pusat pembelajaran bahasa Jepang dari nol sampai mahir:
- Setiap kartu modul dihiasi stiker chibi Genshin di pojok kanan atas supaya suasana belajar terasa santai dan imut.
- Alur belajarnya terarah: Huruf Dasar (Hiragana dan Katakana) → Tata Bahasa (Bunpou) → Aksara Kanji → Percakapan Sehari-hari.
- Tulisannya ramah pelajar SMA, tidak berbelit-belit, dan bikin semangat belajar.

### C. Profil Klub (tentang.html)
Wajah sejarah, nilai, dan kepengurusan klub:
- Konsep selang-seling warna: Seksi hitam untuk cerita sejarah dan prestasi, seksi putih untuk bendera resmi, filosofi nama, makna logo, dan pengurus.
- Garis waktu sejarah: Menceritakan perjalanan komunitas perintis sejak 2018, sempat jadi ekstrakurikuler sekolah, lalu mandiri, dan fleksibel ke depannya.
- Susunan Pengurus Kabinet Clover: 11 kartu pengurus yang rapi dan simetris, di mana 3 kartu di baris terakhir berada tepat di tengah tanpa keterangan kelas.

---

## 3. Filosofi Desain Pengguna (Wajib Dipatuhi)

Berikut aturan penting yang harus selalu diingat setiap kali mengerjakan prompt:

### <font color="#ef4444">1. Buatan Manusia Asli (Anti AI Slop)</font>
- <font color="#ef4444">Haram angka berawalan nol (01, 02, 03):</font> Manusia biasa menulis nomor urut langsung 1, 2, 3. Jangan pakai format kaku mesin.
- <font color="#ef4444">Haram garis miring kaku (/):</font> Jangan pakai garis miring untuk pemisah tanggal atau status. Gunakan tanda hubung (–), titik tengah (·), atau susun kalimat mengalir.
- <font color="#10b981">Bahasa Manusiawi:</font> Hindari kata-kata robot seperti "menjelajahi holistik" atau "sinergi mendalam". Gunakan kalimat yang hangat, akrab, dan wajar seperti anak muda Indonesia.

### <font color="#a855f7">2. Aturan Pola Wagara (Pattern)</font>
- <font color="#ef4444">Maksimal 1 pola per kartu:</font> Jangan pernah menumpuk 2 motif pattern dalam 1 kartu karena hasilnya terlihat tabrakan dan kotor.
- <font color="#10b981">Transparansi super halus:</font> Pattern hanya berfungsi sebagai tekstur mewah, bukan menutupi teks:
  - Seksi Gelap: Pola w1b.jpeg dengan opacity sekitar 0.045 (layar) sampai 0.08 saat disentuh.
  - Seksi Terang: Pola w1w.jpeg dengan opacity sekitar 0.035 sampai 0.045 (multiply).

### <font color="#38bdf8">3. Tata Letak Laptop (Anti Ruang Hampa)</font>
- <font color="#ef4444">Dilarang ada ruang kosong melompong:</font> Di layar laptop, kartu tidak boleh punya ruang bolong besar di tengah antara judul dan tombol bawah. Isi secara proporsional.
- <font color="#10b981">Urutan isi kartu yang rapi:</font>
  Label Kategori → Judul & Penyelenggara → Deskripsi/Caption Ringkas → Kotak Informasi (2 Kolom) → Tombol Juknis.
- <font color="#ff4f91">Poster Wajib Carousel Hemat Ruang:</font>
  Jika ada 2 poster, jangan ditumpuk ke bawah sampai kartu melar 700 piksel. Jadikan 1 frame carousel:
  - Bisa digeser dengan jari (touch swipe) di layar sentuh.
  - Bisa diklik tombol panah kiri dan kanan (‹ dan ›).
  - Bisa digeser dengan drag mouse di laptop.
  - Bisa diklik untuk melihat gambar ukuran penuh (lightbox).
  - Ada angka halaman yang jelas (contoh: 1 dari 2).

### <font color="#f59e0b">4. Standar Foto & Avatar: Chibi Genshin</font>
- Gunakan foto ikon chibi Genshin Impact resmi dari folder `images/mirai/icon/` (Hu Tao, Alhaitham, Furina, Kazuha, Zhongli, Raiden, Nahida, Venti, dsb).
- Lingkaran avatar wajib berlatar putih (#ffffff) dengan object-fit contain dan sedikit padding, supaya chibi berlatar transparan maupun putih tidak terpotong telinga atau topinya.
- Jangan gunakan stiker meme acak yang merusak estetika klub.

### <font color="#10b981">5. Susunan Kartu Ganjil Selalu di Tengah</font>
- Jika ada kartu berjumlah ganjil (seperti 11 pengurus), baris terakhir tidak boleh menjorok ke kiri sendirian.
- Tiga kartu terakhir wajib otomatis berada di posisi tengah agar komposisi tetap seimbang dan enak dipandang.

### <font color="#38bdf8">6. Kebersihan Teks & Data</font>
- Tulis nama pengurus atau anggota secara bersih tanpa keterangan kelas jika diminta.
- Hapus kalimat pengantar klise jika dirasa hanya membuat halaman terlalu panjang tanpa menambah keindahan.

---

## 4. Standar Teknis Kode

1. <font color="#ff4f91">Keseimbangan Kurung CSS:</font> Selalu periksa jumlah kurung kurawal buka dan tutup di style.css agar tidak ada error styling terputus.
2. <font color="#10b981">Jaga Fitur Lama:</font> Jangan pernah menghapus fungsi JavaScript yang sudah berjalan (modal juknis, lightbox gambar, kuis, canvas kanji, atau menu sidebar).
3. <font color="#38bdf8">Solusi Nyata Langsung Selesai:</font> Langsung terapkan perubahan di file yang bersangkutan dan berikan laporan ringkas yang enak dibaca.
