# AGENT INSTRUCTION & GUIDELINES — MIRAI NO WEBU
> Dokumen panduan kerja, persona, dan standar desain AI Agent untuk pengembangan website **MIRAI NO WEBU** (未來の花日本語クラブ / Mirai no Hana Nihongo Kurabu).
> Dokumen ini dirumuskan berdasarkan analisis mendalam terhadap halaman **Beranda (`index.html`)**, **Kelas (`kelas.html`)**, **Tentang (`tentang.html`)**, serta rekam jejak preferensi, kritik, dan filosofi desain pengguna.

---

## 1. Identitas & Persona Proyek

- **Nama Proyek**: Mirai No Webu
- **Organisasi**: Klub Bahasa & Kebudayaan Jepang **MIRAI NO HANA** (SMASYIMDUTA Sidoarjo)
- **Karakter & Visi**: Komunitas pelajar mandiri yang berjiwa muda, dinamis, kreatif, hangat, dan estetik. Website ini bukan sekadar portal informasi sekolah yang kaku, melainkan wadah interaktif komunitas jejepangan (edukasi aksara, kebudayaan, cosplay, festival, dan kepengurusan).
- **Arsitektur Teknis**:
  - Multi-Page Vanilla Web (HTML5 Semantic, CSS3 Modern di `style.css`, JavaScript modular di `js/`).
  - Tidak menggunakan framework JavaScript berat (React/Vue/Tailwind) agar performa tetap instan, ringan, dan mudah dikelola langsung.
  - Dark Mode dominan dengan aksen Pink Sakura (`#ff4f91`, `#e91e63`), dipadukan dengan bagian terang (putih bersih) pada seksi filosofi tertentu secara harmonis.

---

## 2. Analisis Halaman Utama

### A. Beranda (`index.html`)
- **Fungsi**: Gerbang utama visual dan etalase ekosistem Mirai No Webu.
- **Komponen Kunci**:
  - **Hero Section**: Tipografi berani, animasi mengalir, tombol navigasi langsung ke kelas dan kegiatan.
  - **About Preview**: Ringkasan klub dengan kartu fitur bertekstur Wagara.
  - **Journey / Learning Modules**: Akses langsung ke modul dasar, lanjutan, kamus, dan latihan.
  - **Aktivitas & Maskot Sora**: Interaksi asisten AI / maskot Sora yang ramah.
  - **Feedback & Footer**: Penyangkalan hak cipta edukasi dan tautan media sosial resmi.

### B. Hub Kelas Belajar (`kelas.html`, `kelas-dasar.html`, `kelas-lanjutan.html`)
- **Fungsi**: Pusat edukasi bahasa Jepang dari nol hingga tingkat mahir.
- **Komponen Kunci**:
  - **Kartu Modul Visual**: Setiap kartu kelas dihiasi ikon chibi Genshin Impact di pojok kanan atas (`.card-corner-chibi`) agar suasana belajar terasa santai dan menyenangkan.
  - **Struktur Kurikulum**: Jalur belajar terarah (Hiragana &rarr; Katakana &rarr; Bunpou &rarr; Kanji &rarr; Percakapan).
  - **Bahasa Ramah Pelajar**: Penjelasan materi dibuat mudah dimengerti siswa SMA tanpa istilah linguistik yang membingungkan.

### C. Profil Klub (`tentang.html`)
- **Fungsi**: Ensiklopedia sejarah, nilai luhur, filosofi identitas, dan struktur organisasi klub.
- **Komponen Kunci**:
  - **Sistem Selang-Seling Hitam & Putih**:
    - **Hitam**: Seksi Pengenalan, Slogan, Sejarah (Timeline), Wall of Fame / Prestasi, Aksesori / Merchandise.
    - **Putih**: Bendera Resmi NK, Filosofi Nama, Makna Logo NK, Visi & Misi, Profil Sora, Etalase Haori, Kepengurusan.
  - **Timeline Sejarah Transformasi**: Perjalanan dari komunitas perintis (2018), menjadi ekstrakurikuler, beralih ke komunitas mandiri, dan fleksibel kembali.
  - **Susunan Pengurus Kabinet Clover**: 11 kartu pengurus dengan tata letak simetris di mana 3 kartu baris terakhir diletakkan di tengah secara elegan tanpa embel-embel kelas.

---

## 3. Analisis Preferensi & Kebiasaan Pengguna (User Design Philosophy)

*Bagian ini merangkum aturan mutlak yang wajib dipatuhi setiap kali menerima prompt atau instruksi dari pengguna:*

### 1. Anti "AI-Slop" (Buatan Manusia Tulen, Bukan Cetakan Mesin)
- **Larangan Leading Zeros (`01`, `02`, `03`)**:
  - Manusia normal tidak menulis nomor urut biasa dengan angka nol di depan.
  - Selalu gunakan penomoran langsung: `1`, `2`, `3`, `4`, dst.
- **Larangan Karakter Slash (`/`) yang Kaku**:
  - Jangan gunakan tanda `/` yang lazim dicetak otomatis oleh template AI (seperti pada tanggal `10/10/2026`, status `Aktif/Nonaktif`, atau pemisah teks).
  - Gunakan pemisah alami seperti tanda hubung (`–`), titik tengah (`·`), atau susun kalimat bahasa Indonesia yang mengalir.
- **Diksi Alami & Teks Hangat**:
  - Hindari kata-kata klise robotik seperti *"menjelajahi holistik"*, *"sinergi komprehensif"*, *"eksplorasi mendalam"*.
  - Gunakan kalimat yang terasa ditulis oleh anak muda kreatif Indonesia: ringkas, jelas, menarik, dan berjiwa manusia.

### 2. Aturan Pola Wagara & Transparansi (Pattern Integrity)
- **Maksimal 1 Pola per Kartu**:
  - DILARANG KERAS menumpuk dua motif pattern dalam satu kartu (misalnya container kartu sudah punya pattern, lalu elemen di dalamnya diberi pattern lagi). Ini menyebabkan visual *tabrakan* (*pattern clash*) yang terlihat kotor.
- **Tingkat Transparansi yang Sangat Halus**:
  - Pattern hanya berfungsi sebagai tekstur halus berkelas, bukan penghalang teks.
  - **Seksi Gelap/Hitam**: Menggunakan `w1b.jpeg` dengan `mix-blend-mode: screen; opacity: 0.045` (maksimal `0.08` saat hover).
  - **Seksi Terang/Putih**: Menggunakan `w1w.jpeg` dengan `mix-blend-mode: multiply; opacity: 0.035` sampai `0.045`.

### 3. Proporsi Tata Letak & Pemanfaatan Ruang (Anti Ruang Kosong Melompong)
- **Larangan Ruang Hitam/Putih Hampa**:
  - Jangan biarkan kartu di tampilan laptop/desktop memiliki ruang kosong besar yang memisahkan judul dan informasi bawah.
  - Gunakan ritme vertikal yang padat dan seimbang:
    `Header Badges` &rarr; `Judul & Penyelenggara` &rarr; `Deskripsi/Caption` &rarr; `Meta Grid (2 Kolom)` &rarr; `Tombol Aksi`.
- **Hemat Ruang Poster dengan Carousel / Slider**:
  - Jika terdapat lebih dari 1 poster atau gambar dalam satu kartu, **JANGAN ditumpuk vertikal ke bawah** yang membuat kartu melar hingga ratusan piksel.
  - Satukan dalam frame carousel 1 poster yang hemat ruang:
    - Bisa digeser dengan sentuhan jari (*touch swipe*) di layar ponsel/tablet.
    - Bisa digeser dengan tombol panah melayang kiri dan kanan (`‹` dan `›`).
    - Bisa digeser dengan *mouse drag* di laptop.
    - Bisa diklik untuk melihat resolusi penuh via popup *lightbox*.
    - Memiliki indikator nomor halaman yang jelas (misal: `1 dari 2`).

### 4. Standar Aset Visual: Ikon Chibi Genshin Impact
- **Avatar & Maskot**:
  - Untuk foto profil anggota, papan peringkat, maupun dekorasi sudut modul belajar, gunakan koleksi resmi **ikon chibi Genshin Impact** dari folder `images/mirai/icon/` (contoh: Hu Tao, Alhaitham, Furina, Kazuha, Zhongli, Raiden, Nahida, Venti, Xiao, dsb).
  - **Frame Avatar Bulat**: Kontainer avatar (`.podium-avatar-wrap` dan modal) wajib memiliki `background: #ffffff` dan gambar ber-`object-fit: contain` dengan sedikit padding. Hal ini memastikan baik file PNG transparan maupun JPEG putih tampil bulat sempurna tanpa ada telinga, topi, atau aksesoris karakter yang terpotong garis tepi.
  - Hindari penggunaan stiker meme acak yang tidak selaras dengan tema estetika jejepangan klub.

### 5. Penataan Grid Simetris (Kasus Jumlah Ganjil)
- Jika komponen kartu memiliki jumlah ganjil (seperti 11 pengurus), baris terakhir tidak boleh dibiarkan timpang di sisi kiri.
- Terapkan teknik pemusatan otomatis (misalnya 4 kolom di baris 1 & 2, lalu 3 kartu di baris ke-3 berada tepat di posisi tengah / *centered*) untuk menciptakan komposisi visual yang seimbang dan sedap dipandang.

### 6. Kebersihan Teks & Format Nama
- Jika pengguna meminta perubahan data pengurus atau anggota, cantumkan nama secara bersih tanpa embel-embel keterangan kelas jika diminta.
- Hapus teks pengantar atau *subtitle* klise jika pengguna merasa teks tersebut memperpanjang halaman tanpa memberi nilai tambah visual.

---

## 4. Pedoman Teknis Modifikasi Kode

1. **Integritas CSS**:
   - Selalu cek keseimbangan kurung kurawal penutup (`{}` balance) di `style.css` setelah melakukan penambahan atau penyuntingan aturan baru.
   - Hindari aturan `!important` berlebihan yang dapat menimpa media query responsif di tablet (`max-width: 820px`) dan mobile (`max-width: 600px`).
2. **Preservasi Fitur yang Berjalan**:
   - Jangan pernah merusak atau menghapus fungsi interaktif yang sudah ada (seperti modal Juknis, lightbox poster, audio pronunciation, kanji canvas, atau toggle sidebar).
3. **Eksekusi Langsung & Solutif**:
   - Pengguna menyukai eksekusi yang langsung tuntas ke sasaran, menjelaskan poin perubahan secara konkret, dan menyertakan referensi file yang dapat diklik.

---

*Dokumen ini bersifat terbuka untuk dikoreksi, ditambah, dan disempurnakan sesuai kebutuhan pengembangan masa depan Mirai No Webu.*
