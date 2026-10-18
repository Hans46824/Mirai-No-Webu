#!/usr/bin/env python3
"""
File: skrip/arsip/add_meta_tags.py
Fungsi: Menambahkan metadata SEO, Open Graph, Twitter Cards, theme-color, manifest,
        canonical URL, skip-link aksesibilitas, lang="ja" pada teks Jepang,
        dan menghasilkan robots.txt serta sitemap.xml.
Aturan: Idempoten (tanpa menggandakan tag jika dijalankan berulang kali).
"""

import os
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
BASE_URL = "https://hans46824.github.io/Mirai-No-Webu/"
DEFAULT_OG_IMAGE = "https://hans46824.github.io/Mirai-No-Webu/images/mirai/logo/bendera.jpeg"

# Metadata unik terkurasi per halaman
PAGE_METADATA = {
    "index.html": {
        "title": "MIRAI NO HANA — Website Resmi Klub Bahasa & Budaya Jepang SMAWH2",
        "desc": "Website Resmi Klub Bahasa & Kebudayaan Jepang MIRAI NO HANA SMA Wachid Hasyim 2 Taman Sidoarjo. Jelajahi kurikulum berjenjang, kamus kanji & kana mandiri, kegiatan budaya, dan fasilitas anggota."
    },
    "404.html": {
        "title": "Halaman Tidak Ditemukan — MIRAI NO HANA",
        "desc": "Halaman yang kamu tuju tidak ditemukan atau telah dipindahkan. Kembali ke beranda resmi Klub Bahasa Jepang MIRAI NO HANA SMA Wachid Hasyim 2 Taman."
    },
    "offline.html": {
        "title": "Mode Offline — MIRAI NO HANA",
        "desc": "Kamu sedang dalam mode offline. Seluruh kamus kanji, aksara kana, dan progres belajar tetap aman dan dapat diakses tanpa koneksi internet."
    },
    "kamus/index.html": {
        "title": "Kamus Aksara & Kosakata Jepang — MIRAI NO HANA",
        "desc": "Kamus Aksara & Kosakata Jepang Terpadu MIRAI NO HANA. Pelajari Hiragana, Katakana, dan ribuan kanji Joyo lengkap dengan audio pelafalan asli."
    },
    "kamus/kanji.html": {
        "title": "Kamus Kanji Interaktif & Urutan Goresan — MIRAI NO HANA",
        "desc": "Kamus Kanji Interaktif MIRAI NO HANA. Eksplorasi 2.211 Joyo Kanji lengkap dengan animasi urutan goresan baku KanjiVG, onyomi, kunyomi, dan contoh kata."
    },
    "kelas/index.html": {
        "title": "Kelas & Kurikulum Pembelajaran — MIRAI NO HANA",
        "desc": "Kelas & Kurikulum Pembelajaran Bahasa Jepang MIRAI NO HANA. Panduan alur belajar berjenjang, modul Mirai no Buuku, silabus pengajaran, dan latihan mandiri."
    },
    "kelas/latihan.html": {
        "title": "Latihan Kana Quest & Kuis Interaktif — MIRAI NO HANA",
        "desc": "Kana Quest & Latihan Kuis Interaktif MIRAI NO HANA. Latih penguasaan aksara Jepang, tebak suara choukai, balik kartu memori, dan evaluasi capaian belajar."
    },
    "kelas/motivasi.html": {
        "title": "Kata Mutiara & Motivasi Anime — MIRAI NO HANA",
        "desc": "Kata Motivasi & Inspirasi Bahasa Jepang MIRAI NO HANA. Kutipan penuh makna dari anime dan tokoh Jepang populer untuk membakar semangat belajarmu."
    },
    "materi/dasar/index.html": {
        "title": "Mirai no Buuku Dasar — MIRAI NO HANA",
        "desc": "Mirai no Buuku Dasar — Kumpulan modul pondasi aksara Hiragana, Katakana, kosakata esensial, dan tata cara salam perkenalan mandiri."
    },
    "materi/dasar/hiragana.html": {
        "title": "Langkah 1: Huruf Hiragana — Mirai no Buuku",
        "desc": "Modul 01 Mirai no Buuku: Pengenalan 46 Huruf Pokok Hiragana, variasi bunyi Dakuon/Handakuon, diftong Yoon, dan aturan pemanjangan vokal."
    },
    "materi/dasar/katakana.html": {
        "title": "Langkah 2: Huruf Katakana — Mirai no Buuku",
        "desc": "Modul 02 Mirai no Buuku: Aksara Katakana untuk kata serapan asing (gairaigo), nama luar negeri, istilah modern, dan onomatope."
    },
    "materi/dasar/kosakata.html": {
        "title": "Langkah 3: Kosakata Dasar — Mirai no Buuku",
        "desc": "Modul 03 Mirai no Buuku: Perbendaharaan kata konkret sehari-hari meliputi bilangan, nama hari, waktu, benda kelas, dan kata sifat dasar."
    },
    "materi/dasar/jikoshokai.html": {
        "title": "Langkah 4: Salam & Jikoshokai — Mirai no Buuku",
        "desc": "Modul 04 Mirai no Buuku: Ungkapan salam harian (aisatsu), tata cara perkenalan diri mandiri yang santun (jikoshoukai), dan etika ojigi."
    },
    "materi/lanjutan/index.html": {
        "title": "Mirai no Buuku Lanjutan — MIRAI NO HANA",
        "desc": "Mirai no Buuku Lanjutan — Kumpulan materi tata bahasa tingkat menengah, aksara kanji JLPT N5, dan pemahaman membaca kalimat paragraf."
    },
    "materi/lanjutan/grammar.html": {
        "title": "Langkah 5: Tata Bahasa & Partikel — Mirai no Buuku",
        "desc": "Modul 05 Mirai no Buuku: Logika tata bahasa kalimat bahasa Jepang (SOV) dan penguasaan 7 partikel esensial (wa, o, ni, de, no, to, ka)."
    },
    "materi/lanjutan/kanji.html": {
        "title": "Langkah 6: Aksara Kanji & JLPT — Mirai no Buuku",
        "desc": "Modul 06 Mirai no Buuku: Karakter logografis Kanji, aturan bacaan Onyomi vs Kunyomi, radikal bushu, dan kanji standar JLPT N5."
    },
    "materi/lanjutan/kalimat.html": {
        "title": "Langkah 7: Membaca Kalimat Sederhana — Mirai no Buuku",
        "desc": "Modul 07 Mirai no Buuku: Latihan membaca kalimat dan paragraf utuh tanpa spasi bertema kegiatan harian dan kafe dengan panduan furigana."
    },
    "divisi/index.html": {
        "title": "Struktur 4 Divisi Resmi — MIRAI NO HANA",
        "desc": "Struktur 4 Divisi Resmi Klub MIRAI NO HANA: Bahasa & Sastra, Seni & Desain, Cosplay & Budaya Populer, serta Kewirausahaan."
    },
    "divisi/bahasa.html": {
        "title": "Divisi Bahasa & Kebudayaan — MIRAI NO HANA",
        "desc": "Divisi Bahasa & Kebudayaan MIRAI NO HANA: Pembinaan kompetisi pidato bahasa Jepang, olimpiade kanji, penerjemahan, dan bimbingan JLPT."
    },
    "divisi/desain.html": {
        "title": "Divisi Seni & Desain Kreatif — MIRAI NO HANA",
        "desc": "Divisi Seni & Desain Kreatif MIRAI NO HANA: Pembuatan ilustrasi anime/manga, desain merchandise klub, poster event, dan identitas visual."
    },
    "divisi/cosplay.html": {
        "title": "Divisi Cosplay & Budaya Populer — MIRAI NO HANA",
        "desc": "Divisi Cosplay & Kebudayaan Populer MIRAI NO HANA: Pendalaman kostum karakter, tata panggung cosplay, pembuatan properti, dan etika berbusana."
    },
    "divisi/kewirausahaan.html": {
        "title": "Divisi Kewirausahaan & Konbini — MIRAI NO HANA",
        "desc": "Divisi Kewirausahaan & Konbini MIRAI NO HANA: Pengelolaan etalase atribut klub, bazaar festival, F&B khas Jepang, dan pendanaan mandiri."
    },
    "kegiatan/index.html": {
        "title": "Program Kerja & Fasilitas Klub — MIRAI NO HANA",
        "desc": "Program Kerja & Fasilitas Klub MIRAI NO HANA: Jelajahi 5 agenda tahunan unggulan serta fasilitas pendukung pembelajaran anggota."
    },
    "kegiatan/kimi-to-nippon.html": {
        "title": "Kimi to Nippon: Festival Budaya — MIRAI NO HANA",
        "desc": "Kimi to Nippon — Festival kebudayaan Jepang tahunan SMA Wachid Hasyim 2 Taman persembahan klub MIRAI NO HANA."
    },
    "kegiatan/konbini.html": {
        "title": "Mirai no Konbini: Kewirausahaan — MIRAI NO HANA",
        "desc": "Mirai no Konbini — Program kewirausahaan siswa penyedia camilan, minuman khas Jepang, dan merchandise resmi klub."
    },
    "kegiatan/nihon-go-rajio.html": {
        "title": "Nihon-go Rajio: Siaran Podcast — MIRAI NO HANA",
        "desc": "Nihon-go Rajio — Program podcast audio dan siaran radio belajar bahasa Jepang interaktif klub MIRAI NO HANA."
    },
    "kegiatan/ramadhan.html": {
        "title": "Pondok Ramadhan & Bakti Sosial — MIRAI NO HANA",
        "desc": "Pondok Ramadhan & Bakti Sosial — Kegiatan sosial keagamaan dan kepedulian sesama anggota klub MIRAI NO HANA di bulan suci."
    },
    "kegiatan/tomodachi.html": {
        "title": "Tomodachi Gathering: Temu Keakraban — MIRAI NO HANA",
        "desc": "Tomodachi Gathering — Ajang temu keakraban, inaugurasi anggota baru, dan penguatan persaudaraan klub MIRAI NO HANA."
    },
    "peringkat/index.html": {
        "title": "Papan Peringkat & Prestasi — MIRAI NO HANA",
        "desc": "Papan Peringkat & Prestasi MIRAI NO HANA: Leaderboard keaktifan siaran radio, presensi anggota, dan galeri piala prestasi klub."
    },
    "lomba/index.html": {
        "title": "Papan Informasi Lomba & Acara — MIRAI NO HANA",
        "desc": "Papan Informasi Lomba & Festival Jejepangan: Katalog 18 kompetisi akademik, seni, dan cosplay SMA se-Jawa Timur & Nasional."
    },
    "rekomendasi/index.html": {
        "title": "Rekomendasi Pop Culture & Media Belajar — MIRAI NO HANA",
        "desc": "Rekomendasi Pop Culture & Media Belajar: Pilihan anime bermakna, film budaya, musik, dan panduan platform legal MIRAI NO HANA."
    },
    "sora/index.html": {
        "title": "Chat Asora Aokita (Sora AI) — MIRAI NO HANA",
        "desc": "Asora Aokita (Sora) — Asisten AI Cerdas Pendamping Belajar Bahasa & Kebudayaan Jepang Klub MIRAI NO HANA."
    },
    "tentang/index.html": {
        "title": "Tentang Klub & Kepengurusan — MIRAI NO HANA",
        "desc": "Tentang MIRAI NO HANA: Sejarah berdirinya klub sejak angkatan 1 hingga 8, filosofi nama, bendera, makna logo, dan struktur pengurus."
    },
    "toko/index.html": {
        "title": "Toko Resmi & Konbini — MIRAI NO HANA",
        "desc": "Toko Resmi & Konbini MIRAI NO HANA: Etalase pembelian atribut seragam, haori resmi, KTA anggota, dan cinderamata klub."
    }
}

def get_rel_root_prefix(rel_path):
    parts = rel_path.split("/")
    depth = len(parts) - 1
    return "../" * depth if depth > 0 else "./"

def process_html_file(file_path):
    rel_path = file_path.relative_to(ROOT_DIR).as_posix()
    if rel_path.startswith("skrip/"):
        return

    meta = PAGE_METADATA.get(rel_path, {
        "title": "MIRAI NO HANA — SMA Wachid Hasyim 2 Taman",
        "desc": "Website Resmi Klub Bahasa & Kebudayaan Jepang MIRAI NO HANA SMA Wachid Hasyim 2 Taman Sidoarjo."
    })

    content = file_path.read_text(encoding="utf-8")
    original = content

    root_prefix = get_rel_root_prefix(rel_path)
    canonical_url = f"{BASE_URL}{rel_path}"

    # 1. Bersihkan meta tags SEO lama yang berpotensi duplikat
    content = re.sub(r'\s*<meta\s+name=["\']description["\'][^>]*>', '', content, flags=re.I)
    content = re.sub(r'\s*<meta\s+name=["\']theme-color["\'][^>]*>', '', content, flags=re.I)
    content = re.sub(r'\s*<link\s+rel=["\']canonical["\'][^>]*>', '', content, flags=re.I)
    content = re.sub(r'\s*<link\s+rel=["\']manifest["\'][^>]*>', '', content, flags=re.I)
    content = re.sub(r'\s*<meta\s+property=["\']og:[^"\']+["\'][^>]*>', '', content, flags=re.I)
    content = re.sub(r'\s*<meta\s+name=["\']twitter:[^"\']+["\'][^>]*>', '', content, flags=re.I)

    # 2. Buat blok meta terintegrasi
    manifest_href = f"{root_prefix}manifest.webmanifest"
    seo_block = f"""    <meta name="description" content="{meta['desc']}">
    <meta name="theme-color" content="#141018">
    <link rel="canonical" href="{canonical_url}">
    <link rel="manifest" href="{manifest_href}">

    <!-- Open Graph (Facebook / WhatsApp / Discord) -->
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="MIRAI NO HANA">
    <meta property="og:title" content="{meta['title']}">
    <meta property="og:description" content="{meta['desc']}">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:image" content="{DEFAULT_OG_IMAGE}">

    <!-- Twitter Cards -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{meta['title']}">
    <meta name="twitter:description" content="{meta['desc']}">
    <meta name="twitter:image" content="{DEFAULT_OG_IMAGE}">"""

    # Sisipkan di dalam <head> setelah <title>...</title>
    title_match = re.search(r'(<title>[^<]*</title>)', content, flags=re.I)
    if title_match:
        content = content[:title_match.end()] + "\n" + seo_block + content[title_match.end():]
    else:
        # Fallback setelah <meta name="viewport"...>
        vp_match = re.search(r'(<meta\s+name=["\']viewport["\'][^>]*>)', content, flags=re.I)
        if vp_match:
            content = content[:vp_match.end()] + "\n" + seo_block + content[vp_match.end():]

    # 3. Tambahkan Skip-Link Aksesibilitas di awal <body>
    content = re.sub(r'\s*<a\s+class=["\']skip-link["\'][^>]*>.*?</a>', '', content, flags=re.I)
    skip_link = '\n    <a class="skip-link" href="#main-content">Lewati ke konten utama</a>'
    body_match = re.search(r'(<body[^>]*>)', content, flags=re.I)
    if body_match:
        content = content[:body_match.end()] + skip_link + content[body_match.end():]

    # 4. Pastikan <main> memiliki id="main-content"
    content = re.sub(r'<main(?![^>]*\bid=["\']main-content["\'])', '<main id="main-content"', content, flags=re.I)

    # 5. Tambahkan lang="ja" pada elemen teks Jepang (.jp-kanji, .card-sub-jp, .course-kana, .doc-kana) jika belum ada
    def add_lang_ja(match):
        tag = match.group(0)
        if 'lang=' not in tag:
            return tag[:-1] + ' lang="ja">'
        return tag

    content = re.sub(r'<span\s+class=["\'][^"\']*\b(jp-kanji|card-sub-jp|course-kana|doc-kana)\b[^"\']*["\']>', add_lang_ja, content)

    # 6. Pastikan seluruh input memiliki aria-label jika belum ada
    def ensure_input_label(match):
        input_tag = match.group(0)
        if 'aria-label' not in input_tag and 'id=' in input_tag:
            # Beri label dari placeholder atau id
            ph_match = re.search(r'placeholder=["\']([^"\']+)["\']', input_tag)
            id_match = re.search(r'id=["\']([^"\']+)["\']', input_tag)
            label = ph_match.group(1) if ph_match else (id_match.group(1).replace("-", " ") if id_match else "Input teks")
            return input_tag[:-1] + f' aria-label="{label}">'
        return input_tag

    content = re.sub(r'<input\s+[^>]+>', ensure_input_label, content)

    if content != original:
        file_path.write_text(content, encoding="utf-8")
        print(f"✔ Metadata & Aksesibilitas diperbarui: {rel_path}")

def generate_robots_and_sitemap():
    # 1. Buat sitemap.xml
    sitemap_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]

    for rel_path in sorted(PAGE_METADATA.keys()):
        if rel_path == "404.html" or rel_path == "offline.html":
            continue
        url = f"{BASE_URL}{rel_path}"
        priority = "1.0" if rel_path == "index.html" else ("0.9" if "kamus" in rel_path or "kelas" in rel_path else "0.8")
        sitemap_lines.append("  <url>")
        sitemap_lines.append(f"    <loc>{url}</loc>")
        sitemap_lines.append("    <changefreq>weekly</changefreq>")
        sitemap_lines.append(f"    <priority>{priority}</priority>")
        sitemap_lines.append("  </url>")

    sitemap_lines.append("</urlset>")
    sitemap_file = ROOT_DIR / "sitemap.xml"
    sitemap_file.write_text("\n".join(sitemap_lines) + "\n", encoding="utf-8")
    print(f"✔ sitemap.xml berhasil dibuat ({len(PAGE_METADATA) - 2} URL terdaftar)")

    # 2. Buat robots.txt
    robots_content = f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}sitemap.xml
"""
    robots_file = ROOT_DIR / "robots.txt"
    robots_file.write_text(robots_content, encoding="utf-8")
    print("✔ robots.txt berhasil dibuat")

def run():
    print("=== PENAMBAHAN METADATA SEO, SOCIAL SHARING & AKSESIBILITAS ===")
    html_files = sorted(ROOT_DIR.rglob("*.html"))
    for hf in html_files:
        process_html_file(hf)
    generate_robots_and_sitemap()
    print("=== SELESAI DENGAN SUKSES ===")

if __name__ == "__main__":
    run()

