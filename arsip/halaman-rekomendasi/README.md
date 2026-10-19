# 🌸 Arsip Fitur & Ide: Halaman Rekomendasi Pop Culture (Anime, Manga, Musik)

> **Status:** Diarsipkan dari antarmuka web aktif atas permintaan pengguna (19 Oktober 2026).  
> **Berkas Cadangan Lengkap:** [`rekomendasi.archive.html`](rekomendasi.archive.html)  
> **Skrip Pemulihan Cepat (1-Klik):** `python3 skrip/arsip/restore_rekomendasi.py`

---

## 1. Latar Belakang & Konsep Ide
Halaman **Rekomendasi Pop Culture & Media Belajar** (`rekomendasi/index.html`) dirancang sebagai sarana edukatif interaktif bagi anggota klub **MIRAI NO HANA** SMA Wachid Hasyim 2 Taman. 

Filosofi di balik halaman ini adalah:
* Belajar bahasa Jepang (*Nihongo*) menjadi jauh lebih cepat, alami, dan menyenangkan apabila dipadukan dengan media pop culture yang disukai generasi muda (Anime, Manga, dan Musik).
* Melatih kepekaan mendengar (*Choukai / 聴解*) melalui dialog karakter anime dan lirik lagu J-Pop/J-Rock.
* Memperkaya kosakata (*Goi / 語彙*) dan kanji kontekstual melalui komik/manga bertakarir *furigana*.
* Mendorong budaya literasi digital yang sehat dengan mengampanyekan **platform streaming dan bacaan legal/resmi** (anti-bajakan).

---

## 2. Struktur Komponen & Fitur Halaman

Halaman ini mengusung sistem visual khas Mirai no Webu:
1. **Hero Header Dual-Color**: Eyebrow kanji `おすすめ作品`, judul besar `Rekomendasi Anime Manga Musik`, dan pintasan media sosial resmi.
2. **Tab Kategori Interaktif (Filter Tabs)**:
   - 🌟 **Semua Kategori** (`data-category="all"`)
   - 🎬 **Anime** (`data-category="anime"`)
   - 📖 **Manga dan Komik** (`data-category="manga"`)
   - 🎵 **Musik (J-Pop, J-Rock, Vocaloid)** (`data-category="musik"`)
3. **Dynamic Explanation Card (`#rekCatExplainCard`)**:
   Kotak edukasi yang teksnya berubah otomatis sesuai kategori yang aktif untuk memandu siswa memahami relevansi media tersebut dalam pembelajaran bahasa.
4. **Katalog Kartu Rekomendasi (`.rek-card`)**:
   Setiap kartu dilengkapi:
   - Sampul thumbnail & badge tipe media.
   - Judul Romaji & Judul Asli Aksara Jepang (Kanji/Kana).
   - Info episode / volume / artis & studio.
   - Sinopsis singkat berbahasa Indonesia.
   - **Karakter Utama / Artis** berserta pengisi suara (Seiyuu / 声優).
   - **Nilai Edukasi Bahasa & Budaya** (*Key takeaway* untuk pembelajar).
   - Tags genre / tema (misal: *School Life, Slice of Life, Seiyuu Listening, Kanji Furigana*).
5. **Sistem Paginasi Berbasis Klien (`.rekomendasi-pagination`)**:
   Menampilkan kartu secara bertahap (3 kartu per halaman) dengan transisi animasi halus dan tombol navigasi halaman.
6. **Seksi Platform & Layanan Legal (`#mediaRekomendasi`)**:
   Panduan direktori 3 kolom:
   - **Nonton Anime:** Bstation (Bilibili), Muse Indonesia & Ani-One Asia (YouTube Resmi), Crunchyroll.
   - **Baca Manga Resmi:** MANGA Plus by SHUEISHA, BookWalker Global, Comic Days / Shonen Jump+.
   - **Dengar Musik:** Spotify Japan, Apple Music, YouTube Music.
7. **Quote Inspiratif & Form Masukan:**
   Integrasi quote slider motivasi dan formulir kritik/saran klub.

---

## 3. Ringkasan Data Kurasi Karya

### A. Kategori Anime (12 Karya)
| Judul Romaji | Judul Jepang | Studio / Info | Manfaat Belajar Bahasa & Budaya |
| :--- | :--- | :--- | :--- |
| **Yuru Camp△** | ゆるキャン△ | C-Station · 12 Ep | Kosakata alam bebas, percakapan santai sehari-hari (*Tameguchi*), dialek Yamanashi. |
| **Hyouka** | 氷菓 | Kyoto Animation · 22 Ep | Tata bahasa deduktif, ungkapan sastra formal, diksi klub budaya sekolah. |
| **Kimi no Na wa** | 君の名は。 | CoMix Wave Films · Film | Ragam bahasa maskulin vs feminin (*Ore* vs *Watashi*), dialek Hida, tradisi Shinto (*Musubi*). |
| **Shigatsu wa Kimi no Uso** | 四月は君の嘘 | A-1 Pictures · 22 Ep | Monolog puitis, ungkapan emosional mendalam, istilah musik klasik. |
| **Bakuman** | バクマン。 | J.C.Staff · 25 Ep | Kosakata industri kreatif Jepang, etos kerja profesional, proses produksi manga. |
| **Barakamon** | ばらかもん | Kinema Citrus · 12 Ep | Seni kaligrafi Jepang (*Shoudou*), dialek Kepulauan Goto, keramahan pedesaan. |
| **Koe no Katachi** | 聲の形 | Kyoto Animation · Film | Bahasa isyarat Jepang (JSL), etika komunikasi empati, interaksi kelas sekolah. |
| **Haikyuu!!** | ハイキュー!! | Production I.G · 25 Ep | Kosakata olahraga, seruan semangat tim (*Gambare, Ikimashou*), mentalitas pantang menyerah. |
| **Frieren: Beyond Journey's End** | 葬送のフリーレン | Madhouse · 28 Ep | Tempo bicara tenang, diksi sastra klasik, perenungan konsep waktu dan memori manusia. |
| **Bocchi the Rock!** | ぼっち・ざ・ろっく！ | CloverWorks · 12 Ep | Kosakata media sosial modern, bahasa gaul anak muda (*Wakamono Kotoba*), budaya live house. |
| **Violet Evergarden** | ヴァイオレット・エヴァーガーデン | Kyoto Animation · 13 Ep | Tingkat kesantunan tertinggi (*Keigo / Kenjougo / Sonkeigo*), etika korespondensi surat. |
| **Ghibli: Tonari no Totoro** | となりのトトロ | Studio Ghibli · Film | Tata bahasa dasar anak-anak yang ramah pemula, mitologi makhluk alam Jepang. |

### B. Kategori Manga (6 Karya)
| Judul Romaji | Judul Jepang | Mangaka / Penerbit | Manfaat Belajar Bahasa & Budaya |
| :--- | :--- | :--- | :--- |
| **Komi-san wa, Komyushou desu.** | 古見さんは、コミュ症です。 | Tomohito Oda · Shogakukan | Visualisasi onomatopoeia (*Gitaigo & Giongo*), tulisan di buku tulis, percakapan remaja. |
| **Blue Period** | ブルーピリオド | Tsubasa Yamaguchi · Kodansha | Istilah seni rupa, persiapan ujian masuk universitas Jepang, monolog motivasi diri. |
| **Yotsuba to!** | よつばと! | Kiyohiko Azuma · ASCII Media Works | Materi terbaik untuk pemula (N5-N4), kalimat pendek sederhana, kehidupan harian Jepang. |
| **Oishinbo** | 美味しんぼ | Tetsu Kariya · Shogakukan | Kosakata kuliner autentik (*Washoku*), kebiasaan makan tradisional, etika jamuan tamu. |
| **Chihayafuru** | ちはやふる | Yuki Suetsugu · Kodansha | Sastra puisi klasik kuno *Ogura Hyakunin Isshu*, olahraga tradisional *Karuta*. |
| **Spy x Family** | スパイファミリー | Tatsuya Endo · Shueisha | Pembedaan ragam bahasa: formal Anya (kekanak-kanakan), Loid (intelektual), Yor (sopan). |

### C. Kategori Musik (6 Artis / Grup)
| Nama Artis / Grup | Genre Populer | Lagu Rekomendasi | Manfaat Belajar Bahasa & Budaya |
| :--- | :--- | :--- | :--- |
| **YOASOBI** | Novel-into-Music / J-Pop | *Yoru ni Kakeru*, *Idol*, *Gunjou* | Memahami lirik yang diadaptasi langsung dari cerpen sastra Jepang, kecepatan artikulasi. |
| **Eve** | J-Rock / Alternative / Vocaloid | *Kaikai Kitan*, *Dramaturgy*, *Asyoulikeit* | Diksi metafora puitis, rima kalimat khas bahasa Jepang modern. |
| **RADWIMPS** | Alternative Rock / Film OST | *Zenzenzense*, *Sparkle*, *Nandemonaiya* | Struktur kalimat majemuk, ungkapan filosofis tentang kehidupan dan waktu. |
| **Official HIGE DANdism** | Piano Pop / Soul | *Pretender*, *I Love...*, *Subtitle* | Diksi melodi vokal yang jernih, kosakata cinta dan pertemanan yang elegan. |
| **Ado** | Utaite / J-Pop / Rock | *Usseewa*, *Gira Gira*, *Show* | Eksplorasi emosi vokal, ungkapan kritik sosial khas pemuda Jepang era modern. |
| **Kenshi Yonezu** | Art Pop / J-Rock / Vocaloid | *Lemon*, *KICK BACK*, *Uchiage Hanabi* | Kosakata sastra puitis tingkat lanjut (N2-N1), keindahan metafora musim dan memori. |

---

## 4. Panduan Memulihkan Kembali Halaman Ini (Restorasi)

Apabila di kemudian hari Anda memutuskan untuk mengaktifkan kembali halaman Rekomendasi ke situs utama, lakukan langkah berikut:

### Metode Otomatis (Direkomendasikan):
Jalankan skrip pemulihan instan di terminal proyek:
```bash
python3 skrip/arsip/restore_rekomendasi.py
```

### Metode Manual (Langkah demi Langkah):
1. **Salin Kembali Berkas HTML**:
   Buat folder `rekomendasi/` di root proyek dan salin berkas arsip:
   ```bash
   mkdir -p rekomendasi
   cp arsip/halaman-rekomendasi/rekomendasi.archive.html rekomendasi/index.html
   ```
2. **Aktifkan Link Menu Navigasi**:
   Tambahkan baris link berikut ke dalam elemen `<nav class="sidebar-links">` di seluruh berkas HTML:
   - Untuk halaman root (`index.html`, `404.html`):
     ```html
     <a href="rekomendasi/index.html">REKOMENDASI</a>
     ```
   - Untuk halaman sub-folder tingkat 1 (`kamus/`, `kegiatan/`, `kelas/`, dll.):
     ```html
     <a href="../rekomendasi/index.html">REKOMENDASI</a>
     ```
   - Untuk halaman sub-folder tingkat 2 (`materi/dasar/`, `materi/lanjutan/`):
     ```html
     <a href="../../rekomendasi/index.html">REKOMENDASI</a>
     ```
3. **Kembalikan Kartu Navigasi di `index.html`**:
   Sisipkan kembali kartu Rekomendasi pada seksi `.activities-two-grid` di `index.html`:
   ```html
   <div class="activity-start-card nav-card activity-card-active" data-expand-card>
       <img loading="lazy" decoding="async" class="card-corner-chibi" src="images/mirai/icon/Ki.png" alt="" aria-hidden="true" width="500" height="500">
       <span class="card-step-num">5</span>
       <span class="card-sub-jp" lang="ja">おすすめ</span>
       <h3>Rekomendasi</h3>
       <div class="card-collapsible-content">
           <div class="card-collapsible-inner">
               <p>Kumpulan rekomendasi anime, musik, dan konten kebudayaan Jepang pilihan.</p>
           </div>
       </div>
       <a class="card-go-btn" href="rekomendasi/index.html" data-expand-cta>Buka Rekomendasi →</a>
       <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
   </div>
   ```
4. **Daftarkan Kembali di `sitemap.xml`**:
   Tambahkan entri URL ke `sitemap.xml`:
   ```xml
   <url>
     <loc>https://hans46824.github.io/Mirai-No-Webu/rekomendasi/index.html</loc>
     <changefreq>weekly</changefreq>
     <priority>0.8</priority>
   </url>
   ```
5. **Perbarui Versi Aset & Precache**:
   Jalankan:
   ```bash
   python3 skrip/arsip/stamp_asset_versions.py && python3 skrip/arsip/build_precache_list.py
   ```

