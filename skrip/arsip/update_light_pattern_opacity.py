#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: skrip/arsip/update_light_pattern_opacity.py
Deskripsi:
  Menurunkan transparansi/opacity untuk seluruh pattern cerah (light pattern w1w & c1w)
  menjadi 0.015 (hover: 0.03) agar sangat halus, samar, dan tidak mengganggu keterbacaan teks
  di atas kartu putih/terang, sementara pattern gelap tetap dipertahankan pada 0.045 (hover: 0.07).
"""

import os
import re
import glob

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CSS_PAGES_DIR = os.path.join(BASE_DIR, "css", "pages")

def update_global_css():
    file_path = os.path.join(CSS_PAGES_DIR, "global.css")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    orig = content

    # 1. Tambah variabel master transparansi di :root jika belum ada
    if "--pattern-opacity-light:" not in content:
        content = content.replace(
            "  --pattern-size: 200px auto;\n",
            "  --pattern-size: 200px auto;\n  --pattern-opacity-light: 0.015;\n  --pattern-opacity-light-hover: 0.03;\n  --pattern-opacity-dark: 0.045;\n  --pattern-opacity-dark-hover: 0.07;\n"
        )

    # 2. .mirai-card-light::after
    content = re.sub(
        r'(\.mirai-card-light::after\s*\{[\s\S]*?opacity:\s*)0\.045(\s*!important;)',
        r'\g<1>0.015\2',
        content
    )

    # 3. .section-quote-slider.quote-theme-white .quote-card::after
    content = re.sub(
        r'(\.section-quote-slider\.quote-theme-white\s+\.quote-card::after\s*\{[\s\S]*?opacity:\s*)0\.045(\s*!important;)',
        r'\g<1>0.015\2',
        content
    )

    if content != orig:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(" [OK] css/pages/global.css diperbarui.")
    else:
        print(" [INFO] css/pages/global.css tidak berubah.")

def update_tentang_css():
    file_path = os.path.join(CSS_PAGES_DIR, "tentang.css")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    orig = content

    # Kartu putih tentang (.flag-feature-card, .logo-meaning-card, dll.)
    content = re.sub(
        r'(\.flag-feature-card::after[\s\S]*?opacity:\s*)0\.045(\s*!important;)',
        r'\g<1>0.015\2',
        content
    )
    content = re.sub(
        r'(\.flag-feature-card:hover::after[\s\S]*?opacity:\s*)0\.07(\s*!important;)',
        r'\g<1>0.03\2',
        content
    )

    # .page-kegiatan .program-card::after
    content = re.sub(
        r'(\.page-kegiatan\s+\.program-card::after\s*\{[\s\S]*?opacity:\s*)0\.045(\s*!important;)',
        r'\g<1>0.015\2',
        content
    )
    content = re.sub(
        r'(\.page-kegiatan\s+\.program-card:hover::after[\s\S]*?opacity:\s*)0\.07(\s*!important;)',
        r'\g<1>0.03\2',
        content
    )

    # .page-lomba .lomba-detail-card::after
    content = re.sub(
        r'(\.page-lomba\s+\.lomba-detail-card::after\s*\{[\s\S]*?opacity:\s*)0\.045(\s*!important;)',
        r'\g<1>0.015\2',
        content
    )
    content = re.sub(
        r'(\.page-lomba\s+\.lomba-detail-card:hover::after\s*\{[\s\S]*?opacity:\s*)0\.07(\s*!important;)',
        r'\g<1>0.03\2',
        content
    )

    if content != orig:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(" [OK] css/pages/tentang.css diperbarui.")
    else:
        print(" [INFO] css/pages/tentang.css tidak berubah.")

def update_beranda_css():
    file_path = os.path.join(CSS_PAGES_DIR, "beranda.css")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    orig = content

    # .start-card::after, .curriculum-cards a::after
    content = re.sub(
        r'(\.start-card::after,\s*\.curriculum-cards\s+a::after\s*\{[\s\S]*?opacity:\s*)0\.045(\s*!important;)',
        r'\g<1>0.015\2',
        content
    )
    content = re.sub(
        r'(\.start-card:hover::after,\s*\.curriculum-cards\s+a:hover::after\s*\{[\s\S]*?opacity:\s*)0\.07(\s*!important;)',
        r'\g<1>0.03\2',
        content
    )

    # .activity-start-card::after (terang)
    content = re.sub(
        r'(body:not\(\.dark-mode\):not\(\.theme-dark\)[\s\S]*?\.activity-start-card::after\s*\{[\s\S]*?opacity:\s*)0\.045(\s*!important;)',
        r'\g<1>0.015\2',
        content
    )

    # .feedback-feature-card::after (terang)
    content = re.sub(
        r'(\.feedback-theme-white\s+\.feedback-feature-card::after[\s\S]*?opacity:\s*)0\.045(\s*!important;)',
        r'\g<1>0.015\2',
        content
    )
    content = re.sub(
        r'(\.feedback-theme-white\s+\.feedback-feature-card:hover::after[\s\S]*?opacity:\s*)0\.07(\s*!important;)',
        r'\g<1>0.03\2',
        content
    )

    if content != orig:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(" [OK] css/pages/beranda.css diperbarui.")
    else:
        print(" [INFO] css/pages/beranda.css tidak berubah.")

def update_kelas_materi_css():
    file_path = os.path.join(CSS_PAGES_DIR, "kelas-materi.css")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    orig = content

    # doc-big-card
    content = re.sub(
        r'(\.page-kelas\s+#kurikulum\s+\.doc-big-card::after\s*\{[\s\S]*?opacity:\s*)0\.045(\s*!important;)',
        r'\g<1>0.015\2',
        content
    )
    content = re.sub(
        r'(\.page-kelas\s+#kurikulum\s+\.doc-big-card:hover::after\s*\{[\s\S]*?opacity:\s*)0\.15(\s*!important;)',
        r'\g<1>0.03\2',
        content
    )

    # #dasar .course-card::after
    content = re.sub(
        r'(#dasar\s+\.course-card::after\s*\{[\s\S]*?opacity:\s*)0\.045(\s*!important;)',
        r'\g<1>0.015\2',
        content
    )
    content = re.sub(
        r'(#dasar\s+\.course-card:hover::after\s*\{[\s\S]*?opacity:\s*)0\.07(\s*!important;)',
        r'\g<1>0.03\2',
        content
    )

    # .page-kelas-dasar .roadmap article::after
    content = re.sub(
        r'(\.page-kelas-dasar\s+\.roadmap\s+article::after\s*\{[\s\S]*?opacity:\s*)0\.045(\s*!important;)',
        r'\g<1>0.015\2',
        content
    )

    # Hiragana mode-card light
    content = re.sub(
        r'(\.learning-app\s+\.mode-card--hiragana::after[\s\S]*?opacity:\s*)0\.045(\s*!important;)',
        r'\g<1>0.015\2',
        content
    )
    content = re.sub(
        r'(\.learning-app\s+\.mode-card--hiragana:hover::after[\s\S]*?opacity:\s*)0\.07(\s*!important;)',
        r'\g<1>0.03\2',
        content
    )

    # Katakana mode-card light invert
    content = re.sub(
        r'(body:not\(\.theme-dark\):not\(\.dark-mode\)[\s\S]*?\.mode-card--katakana::after\s*\{[\s\S]*?opacity:\s*)0\.045(\s*!important;)',
        r'\g<1>0.015\2',
        content
    )
    content = re.sub(
        r'(body:not\(\.theme-dark\):not\(\.dark-mode\)[\s\S]*?\.mode-card--katakana:hover::after\s*\{[\s\S]*?opacity:\s*)0\.07(\s*!important;)',
        r'\g<1>0.03\2',
        content
    )

    if content != orig:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(" [OK] css/pages/kelas-materi.css diperbarui.")
    else:
        print(" [INFO] css/pages/kelas-materi.css tidak berubah.")

def update_other_css_files():
    # toko.css
    toko_path = os.path.join(CSS_PAGES_DIR, "toko.css")
    if os.path.exists(toko_path):
        with open(toko_path, "r", encoding="utf-8") as f:
            c = f.read()
        orig = c
        c = re.sub(r'(background-image:\s*url\("[^"]*c1w\.jpeg"\)\s*!important;[\s\S]*?opacity:\s*)0\.045(\s*!important;)', r'\g<1>0.015\2', c)
        if c != orig:
            with open(toko_path, "w", encoding="utf-8") as f:
                f.write(c)
            print(" [OK] css/pages/toko.css diperbarui.")

    # lomba.css
    lomba_path = os.path.join(CSS_PAGES_DIR, "lomba.css")
    if os.path.exists(lomba_path):
        with open(lomba_path, "r", encoding="utf-8") as f:
            c = f.read()
        orig = c
        c = re.sub(r'(background-image:\s*url\("[^"]*c1w\.jpeg"\)\s*!important;[\s\S]*?opacity:\s*)0\.045(\s*!important;)', r'\g<1>0.015\2', c)
        if c != orig:
            with open(lomba_path, "w", encoding="utf-8") as f:
                f.write(c)
            print(" [OK] css/pages/lomba.css diperbarui.")

    # rekomendasi-motivasi.css
    rek_path = os.path.join(CSS_PAGES_DIR, "rekomendasi-motivasi.css")
    if os.path.exists(rek_path):
        with open(rek_path, "r", encoding="utf-8") as f:
            c = f.read()
        orig = c
        c = re.sub(r'(background-image:\s*url\("[^"]*w1w\.jpeg"\)\s*!important;[\s\S]*?opacity:\s*)0\.045(\s*!important;)', r'\g<1>0.015\2', c)
        if c != orig:
            with open(rek_path, "w", encoding="utf-8") as f:
                f.write(c)
            print(" [OK] css/pages/rekomendasi-motivasi.css diperbarui.")

    # kamus.css
    kamus_path = os.path.join(CSS_PAGES_DIR, "kamus.css")
    if os.path.exists(kamus_path):
        with open(kamus_path, "r", encoding="utf-8") as f:
            c = f.read()
        orig = c
        c = re.sub(r'(\.dictionary-practice-link::after\s*\{[\s\S]*?opacity:\s*)0\.045(\s*!important;)', r'\g<1>0.015\2', c)
        if c != orig:
            with open(kamus_path, "w", encoding="utf-8") as f:
                f.write(c)
            print(" [OK] css/pages/kamus.css diperbarui.")

def update_agent_md():
    agent_path = os.path.join(BASE_DIR, "panduan", "agent.md")
    if os.path.exists(agent_path):
        with open(agent_path, "r", encoding="utf-8") as f:
            c = f.read()
        orig = c
        target = "2. **Kunci Transparansi Watermark Sangat Lembut (Maksimal Keterbacaan Teks)**:\n   - Pola Terang & Gelap: Dikunci pada **`opacity: 0.045 !important`** (hover: `0.07 !important`) dan gradien penutup master di `:root` sebesar `0.95`–`0.97` agar teks kartu sangat jernih, tajam, dan tidak terganggu oleh garis gelombang latar."
        replacement = "2. **Kunci Transparansi Watermark Sangat Lembut (Maksimal Keterbacaan Teks)**:\n   - Pola Terang (Light Pattern): Dikunci ekstra lembut pada **`opacity: 0.015 !important`** (hover: `0.03 !important`) agar latar putih bersih tetap jernih dan teks berkontras tajam tanpa gangguan garis motif.\n   - Pola Gelap (Dark Pattern): Tetap pada **`opacity: 0.045 !important`** (hover: `0.07 !important`) dengan `mix-blend-mode: screen` pada kartu gelap."
        c = c.replace(target, replacement)
        if c != orig:
            with open(agent_path, "w", encoding="utf-8") as f:
                f.write(c)
            print(" [OK] panduan/agent.md diperbarui dengan standar transparansi baru.")

def main():
    print("=== MIRAI NO HANA: Penyesuaian Transparansi Pattern Cerah ===")
    update_global_css()
    update_tentang_css()
    update_beranda_css()
    update_kelas_materi_css()
    update_other_css_files()
    update_agent_md()
    print("=== Selesai dengan sukses ===")

if __name__ == "__main__":
    main()

