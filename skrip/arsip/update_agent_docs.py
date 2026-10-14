#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to update panduan/agent.md with Fast-Execution Protocol
and current modular CSS & scripts structure.
"""

def main():
    path = 'panduan/agent.md'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    fast_protocol = '''## 1. Protokol Eksekusi Cepat (Fast-Execution Protocol)

Setiap AI asisten atau pengembang yang bekerja pada repositori ini **WAJIB mematuhi 4 aturan inti eksekusi cepat** berikut tanpa kecuali:

### 1. Peta Modul CSS (DILARANG Membaca style.css Utuh)
- **DILARANG KERAS** membaca `css/style.css` secara keseluruhan atau memindai semua modul CSS sekaligus ke dalam konteks percakapan.
- `css/style.css` kini murni berfungsi sebagai master index pengimpor (`@import`) 5 modul terpisah.
- Untuk membaca atau mengedit aturan CSS, **hanya buka modul spesifik yang relevan** sesuai peta berikut:
  - **`css/modules/01-base-theme.css`**: Variabel warna root, CSS reset, sistem selang-seling background ganjil/genap, dan tombol dasar.
  - **`css/modules/02-header-hero-footer.css`**: Floating navbar, off-canvas sidebar menu, banner hero section semua halaman, global footer, dan three-tier header.
  - **`css/modules/03-kelas-kamus-latihan.css`**: Halaman Kelas (`kelas/*`), Materi (`materi/*`), Kamus (`kamus/*`), kuis Latihan Kana, kanvas urutan goresan (stroke order), dan kurikulum.
  - **`css/modules/04-proker-tentang.css`**: Halaman Kegiatan/Proker (`kegiatan/*`), Divisi (`divisi/*`), Tentang Klub (`tentang/index.html`), filosofi, logo, slogan, visi misi, haori, kepengurusan, timeline, sora profile, prestasi, dan FAQ.
  - **`css/modules/05-fitur-ekstra.css`**: Komponen Beranda (`index.html`), Rekomendasi (`rekomendasi/index.html`), Peringkat (`peringkat/index.html`), Lomba (`lomba/index.html`), Toko (`toko/index.html`), 404 (`404.html`), animasi umum, dan Hero Guardrail.

### 2. Peta JavaScript (`js/`)
Akses logika interaktif langsung ke berkas terkait tanpa membaca seluruh folder:
- **Logika UI global & navigasi**: `js/main.js` (header scroll, hero motion, launcher) dan `js/script.js` (master interaksi kuis, kartu, & efek global).
- **Chatbot Sora**: `js/sora.js` (logika chatbot offline & UI), `js/api.js` (endpoint data), dan `js/translator.js` (mesin bantu terjemahan).
- **Kamus, Kana, Kanji & Goresan**: `js/kana.js` (kartu & audio pelafalan), `js/kanji.js` (ensiklopedia & filter kanji), dan `js/stroke.js` (animasi kanvas goresan). Catatan: `js/stroke-data.js` berisi vektor koordinat garis besar dan dikecualikan dari pemindaian.
- **Slider & Carousel**: `js/carousel.js` (carousel umum & produk) dan `js/proker-slider.js` (slider khusus proker kegiatan).

### 3. Larangan Menyalakan Server & Screenshot Otomatis
- **DILARANG KERAS** menyalakan/merestart HTTP server lokal (`python3 -m http.server`, live-server, dll.) atau mengambil screenshot otomatis via browser/tool kecuali diminta secara eksplisit oleh user.
- Fokus langsung pada eksekusi cepat kode dan pembaruan dokumentasi.

### 4. Eksekusi Batch HTML Berulang Wajib Skrip Python Terminal
- Jika diminta mengubah elemen HTML yang berulang di banyak halaman (seperti navbar, sidebar, hero, atau footer di 26+ file HTML), **WAJIB menggunakan satu script Python singkat via terminal**.
- **DILARANG KERAS** mengedit file HTML satu per satu secara manual dengan tool pengedit teks yang lambat dan membebani konteks percakapan.

---

'''

    # Update css and skrip description under section 1.A
    old_css_desc = '- **`css/`**: Berisi master stylesheet antarmuka (`css/style.css`).'
    new_css_desc = '- **`css/`**: Berisi master stylesheet antarmuka (`css/style.css`) yang memanggil 5 modul terpisah di `css/modules/` (`01-base-theme.css` s.d. `05-fitur-ekstra.css`).'

    old_skrip_desc = '- **`skrip/`**: Kumpulan skrip otomasi & pemeliharaan kode Python.'
    new_skrip_desc = '- **`skrip/`**: Kumpulan skrip otomasi & pemeliharaan kode Python, serta sub-folder `skrip/arsip/` untuk menyimpan arsip skrip sekali-pakai.'

    if old_css_desc not in content:
        print("ERROR: old_css_desc not found")
        return
    if old_skrip_desc not in content:
        print("ERROR: old_skrip_desc not found")
        return

    content = content.replace(old_css_desc, new_css_desc)
    content = content.replace(old_skrip_desc, new_skrip_desc)

    # Renumber sections 11 down to 1
    for n in range(11, 0, -1):
        content = content.replace(f'## {n}. ', f'## {n+1}. ')

    target = '## 2. Aturan Wajib: Pembaruan Mandiri Dokumentasi'
    if target not in content:
        print("ERROR: target not found")
        return

    content = content.replace(target, fast_protocol + target)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: panduan/agent.md updated successfully")

if __name__ == '__main__':
    main()
