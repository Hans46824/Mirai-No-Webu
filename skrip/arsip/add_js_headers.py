#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to add documentation headers to all 11 js/*.js files
and remove duplicate event listeners between main.js and script.js.
"""

def update_main():
    path = 'js/main.js'
    header = '''/**
 * File: js/main.js
 * Fungsi: Pengendali UI global (navbar, sidebar drawer, hero sticky curtain, back-to-top, scroll reveal, dan tema).
 * Penggunaan: Universal di seluruh 30 halaman HTML website (index.html, tentang, kelas, kegiatan, divisi, lomba, toko, dll.).
 */

'''
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if not content.startswith('/**\n * File: js/main.js'):
        content = header + content
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated js/main.js")

def update_script():
    path = 'js/script.js'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find where const rows = [ begins
    marker = 'const rows = ['
    idx = content.find(marker)
    if idx == -1:
        print("ERROR: marker not found in js/script.js")
        return

    remaining = content[idx:]

    new_top = '''/**
 * File: js/script.js
 * Fungsi: Mesin kuis interaktif pembelajaran mandiri Kana Quest (20 soal adaptif, goresan kanvas, dan evaluasi hasil).
 * Penggunaan: Digunakan di kelas/latihan.html (serta modul interaktif lomba, peringkat, rekomendasi, dan toko).
 */

document.addEventListener("DOMContentLoaded", () => {
    const app = document.querySelector(".learning-app");
    if (app) {
        initKanaQuest();
    }
});

'''
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_top + remaining)
    print("Updated js/script.js (cleaned duplicate listeners and added header)")

def update_carousel():
    path = 'js/carousel.js'
    header = '''/**
 * File: js/carousel.js
 * Fungsi: Komponen slider horizontal utilitas [data-slider] dengan navigasi panah, pagination dots, dan touch swipe.
 * Penggunaan: Komponen mandiri untuk etalase slider benefit/fitur pada sub-halaman interaktif.
 */

'''
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if not content.startswith('/**\n * File: js/carousel.js'):
        content = header + content
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated js/carousel.js")

def update_proker_slider():
    path = 'js/proker-slider.js'
    header = '''/**
 * File: js/proker-slider.js
 * Fungsi: Pengendali interaktif slider galeri program kerja & dokumentasi kegiatan klub dengan touch swipe & tombol panah.
 * Penggunaan: kegiatan/index.html, kimi-to-nippon.html, konbini.html, nihon-go-rajio.html, ramadhan.html, tomodachi.html.
 */

'''
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove existing 2-line comment if present
    old_prefix = "// Shared Independent Documentation Slider (Portrait & Landscape)\n// Used in kegiatan.html and all proker pages (ktn.html, njr.html, konbini.html, ramadhan.html)\n"
    if content.startswith(old_prefix):
        content = content[len(old_prefix):]

    content = header + content.lstrip()
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated js/proker-slider.js")

def update_kana():
    path = 'js/kana.js'
    header = '''/**
 * File: js/kana.js
 * Fungsi: Pengelola modul tabel aksara Kana (Hiragana & Katakana), filter Gojuuon/Dakuon/Yoon, pencarian, dan audio pelafalan.
 * Penggunaan: kamus/index.html dan kamus/kanji.html.
 */

'''
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if not content.startswith('/**\n * File: js/kana.js'):
        content = header + content
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated js/kana.js")

def update_kanji():
    path = 'js/kanji.js'
    header = '''/**
 * File: js/kanji.js
 * Fungsi: Mesin pencarian dan ensiklopedia 2.136 karakter Joyo Kanji, filter tingkat JLPT/kelas, dan modal detail kanji.
 * Penggunaan: kamus/index.html dan kamus/kanji.html.
 */

'''
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove existing block comment at start if present
    if content.startswith('/**'):
        end_idx = content.find('*/')
        if end_idx != -1:
            content = content[end_idx+2:].lstrip()

    content = header + content
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated js/kanji.js")

def update_stroke():
    path = 'js/stroke.js'
    header = '''/**
 * File: js/stroke.js
 * Fungsi: Mesin animasi kanvas urutan goresan karakter Kanji dan kombinasi Kana Yoon di atas kisi Genkouyoushi.
 * Penggunaan: kamus/index.html dan kamus/kanji.html.
 */

'''
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if not content.startswith('/**\n * File: js/stroke.js'):
        content = header + content
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated js/stroke.js")

def update_sora():
    path = 'js/sora.js'
    header = '''/**
 * File: js/sora.js
 * Fungsi: Logika asisten chatbot maskot Asora Aokita (Sora), filter jawaban offline cerdas, saran halaman, dan drawer UI.
 * Penggunaan: 18 halaman yang menyematkan widget Sora (index.html, kelas/*, divisi/index.html, lomba, toko, kamus, materi).
 */

'''
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if not content.startswith('/**\n * File: js/sora.js'):
        content = header + content
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated js/sora.js")

def update_api():
    path = 'js/api.js'
    header = '''/**
 * File: js/api.js
 * Fungsi: Layanan terpadu API data kamus & karakter (MiraiData), caching localStorage, dan loader dataset data/kana.json.
 * Penggunaan: Modul penyedia data sentral untuk fitur kamus, pencarian kanji, dan pembelajaran aksara.
 */

'''
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove existing comment at start if present
    if content.startswith('/**'):
        end_idx = content.find('*/')
        if end_idx != -1:
            content = content[end_idx+2:].lstrip()

    content = header + content
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated js/api.js")

def update_translator():
    path = 'js/translator.js'
    header = '''/**
 * File: js/translator.js
 * Fungsi: Mesin penerjemah leksikal kamus (MiraiTranslator) dari makna bahasa Inggris ke padanan istilah Bahasa Indonesia.
 * Penggunaan: kamus/index.html dan kamus/kanji.html.
 */

'''
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if not content.startswith('/**\n * File: js/translator.js'):
        content = header + content
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated js/translator.js")

def update_leaderboard():
    path = 'js/leaderboard-data.js'
    header = '''/**
 * File: js/leaderboard-data.js
 * Fungsi: Master data terpusat untuk papan peringkat keaktifan, presensi kehadiran anggota, dan rekam jejak prestasi siswa.
 * Penggunaan: peringkat/index.html dan tentang/index.html.
 */

'''
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove existing comment at start if present
    if content.startswith('/**'):
        end_idx = content.find('*/')
        if end_idx != -1:
            content = content[end_idx+2:].lstrip()

    content = header + content
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated js/leaderboard-data.js")

def main():
    update_main()
    update_script()
    update_carousel()
    update_proker_slider()
    update_kana()
    update_kanji()
    update_stroke()
    update_sora()
    update_api()
    update_translator()
    update_leaderboard()
    print("ALL 11 JS FILES UPDATED!")

if __name__ == '__main__':
    main()
