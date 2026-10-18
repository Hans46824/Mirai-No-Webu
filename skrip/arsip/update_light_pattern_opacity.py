#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: skrip/arsip/update_light_pattern_opacity.py
Deskripsi:
  Meningkatkan visibilitas seluruh pattern cerah (light pattern w1w & c1w)
  menjadi 0.085 (hover: 0.13) agar motif Wagara dan Kumo tampak lebih jelas, anggun,
  dan terlihat nyata di atas kartu putih/terang, dengan tetap menjaga kontras teks
  tinggi di atas 9:1 (WCAG AAA). Pattern gelap dipertahankan pada 0.045 (hover: 0.07).
"""

import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CSS_PAGES_DIR = os.path.join(BASE_DIR, "css", "pages")

NEW_LIGHT_OPACITY = "0.085"
NEW_LIGHT_HOVER = "0.13"
DARK_OPACITY = "0.045"
DARK_HOVER = "0.07"

def update_global_css():
    file_path = os.path.join(CSS_PAGES_DIR, "global.css")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    orig = content

    # 1. Update variabel master di :root
    content = re.sub(
        r'--pattern-opacity-light:\s*[\d\.]+;',
        f'--pattern-opacity-light: {NEW_LIGHT_OPACITY};',
        content
    )
    content = re.sub(
        r'--pattern-opacity-light-hover:\s*[\d\.]+;',
        f'--pattern-opacity-light-hover: {NEW_LIGHT_HOVER};',
        content
    )

    # 2. .mirai-card-light::after
    content = re.sub(
        r'(\.mirai-card-light::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{NEW_LIGHT_OPACITY}\2',
        content
    )

    # 3. .section-quote-slider.quote-theme-white .quote-card::after
    content = re.sub(
        r'(\.section-quote-slider\.quote-theme-white\s+\.quote-card::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{NEW_LIGHT_OPACITY}\2',
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

    # .flag-mockup-frame::after
    content = re.sub(
        r'(\.flag-mockup-frame::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{NEW_LIGHT_OPACITY}\2',
        content
    )
    content = re.sub(
        r'(\.flag-feature-card:hover\s+\.flag-mockup-frame::after,\s*\.flag-mockup-frame:hover::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{NEW_LIGHT_HOVER}\2',
        content
    )

    # dark-mode .flag-mockup-frame::after (gelap)
    content = re.sub(
        r'(body\.theme-dark\s+\.flag-mockup-frame::after,\s*body\.dark-mode\s+\.flag-mockup-frame::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{DARK_OPACITY}\2',
        content
    )
    content = re.sub(
        r'(body\.theme-dark\s+\.flag-mockup-frame:hover::after,\s*body\.dark-mode\s+\.flag-mockup-frame:hover::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{DARK_HOVER}\2',
        content
    )

    # .flag-feature-card::after, .logo-meaning-badge-col::after, etc.
    content = re.sub(
        r'(\.flag-feature-card::after,\s*\.logo-meaning-badge-col::after[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{NEW_LIGHT_OPACITY}\2',
        content
    )
    content = re.sub(
        r'(\.flag-feature-card:hover::after,\s*\.logo-meaning-badge-col:hover::after[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{NEW_LIGHT_HOVER}\2',
        content
    )

    # .page-kegiatan .program-card::after (terang)
    content = re.sub(
        r'(\.page-kegiatan\s+\.program-card::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{NEW_LIGHT_OPACITY}\2',
        content
    )
    content = re.sub(
        r'(\.page-kegiatan\s+\.program-card:hover::after,\s*\.page-kegiatan\s+\.program-card-link:hover\s+\.program-card::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{NEW_LIGHT_HOVER}\2',
        content
    )

    # dark-mode .page-kegiatan .program-card::after (gelap)
    content = re.sub(
        r'(body\.dark-mode\s+\.page-kegiatan\s+\.program-card::after,\s*body\.theme-dark\s+\.page-kegiatan\s+\.program-card::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{DARK_OPACITY}\2',
        content
    )
    content = re.sub(
        r'(body\.dark-mode\s+\.page-kegiatan\s+\.program-card:hover::after,\s*body\.theme-dark\s+\.page-kegiatan\s+\.program-card:hover::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{DARK_HOVER}\2',
        content
    )

    # .page-lomba .lomba-detail-card::after (terang)
    content = re.sub(
        r'(\.page-lomba\s+\.lomba-detail-card::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{NEW_LIGHT_OPACITY}\2',
        content
    )
    content = re.sub(
        r'(\.page-lomba\s+\.lomba-detail-card:hover::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{NEW_LIGHT_HOVER}\2',
        content
    )

    # dark-mode .page-lomba .lomba-detail-card::after (gelap)
    content = re.sub(
        r'(body\.dark-mode\s+\.page-lomba\s+\.lomba-detail-card::after,\s*body\.theme-dark\s+\.page-lomba\s+\.lomba-detail-card::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{DARK_OPACITY}\2',
        content
    )
    content = re.sub(
        r'(body\.dark-mode\s+\.page-lomba\s+\.lomba-detail-card:hover::after,\s*body\.theme-dark\s+\.page-lomba\s+\.lomba-detail-card:hover::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{DARK_HOVER}\2',
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
        r'(\.start-card::after,\s*\.curriculum-cards\s+a::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{NEW_LIGHT_OPACITY}\2',
        content
    )
    content = re.sub(
        r'(\.start-card:hover::after,\s*\.curriculum-cards\s+a:hover::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{NEW_LIGHT_HOVER}\2',
        content
    )

    # .program-card::after (terang)
    content = re.sub(
        r'(\.program-card::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{NEW_LIGHT_OPACITY}\2',
        content
    )
    content = re.sub(
        r'(\.program-card:hover::after,\s*\.program-card-link:hover\s+\.program-card::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{NEW_LIGHT_HOVER}\2',
        content
    )

    # dark-mode .program-card::after (gelap)
    content = re.sub(
        r'(body\.dark-mode\s+\.program-card::after,\s*body\.theme-dark\s+\.program-card::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{DARK_OPACITY}\2',
        content
    )
    content = re.sub(
        r'(body\.dark-mode\s+\.program-card:hover::after,\s*body\.theme-dark\s+\.program-card:hover::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{DARK_HOVER}\2',
        content
    )

    # .activity-start-card::after (terang)
    content = re.sub(
        r'(body:not\(\.dark-mode\):not\(\.theme-dark\)[\s\S]*?\.activity-start-card::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{NEW_LIGHT_OPACITY}\2',
        content
    )

    # .feedback-theme-white .feedback-feature-card::after (terang)
    content = re.sub(
        r'(\.feedback-theme-white\s+\.feedback-feature-card::after[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{NEW_LIGHT_OPACITY}\2',
        content
    )
    content = re.sub(
        r'(\.feedback-theme-white\s+\.feedback-feature-card:hover::after[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{NEW_LIGHT_HOVER}\2',
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

    # doc-big-card (terang)
    content = re.sub(
        r'(\.page-kelas\s+#kurikulum\s+\.doc-big-card::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{NEW_LIGHT_OPACITY}\2',
        content
    )
    content = re.sub(
        r'(\.page-kelas\s+#kurikulum\s+\.doc-big-card:hover::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{NEW_LIGHT_HOVER}\2',
        content
    )

    # dark-mode doc-big-card (gelap)
    content = re.sub(
        r'(body\.dark-mode\s+\.page-kelas\s+#kurikulum\s+\.doc-big-card::after,\s*body\.theme-dark\s+\.page-kelas\s+#kurikulum\s+\.doc-big-card::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{DARK_OPACITY}\2',
        content
    )

    # #dasar .course-card::after
    content = re.sub(
        r'(#dasar\s+\.course-card::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{NEW_LIGHT_OPACITY}\2',
        content
    )
    content = re.sub(
        r'(#dasar\s+\.course-card:hover::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{NEW_LIGHT_HOVER}\2',
        content
    )

    # .page-kelas-dasar .roadmap article::after
    content = re.sub(
        r'(\.page-kelas-dasar\s+\.roadmap\s+article::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{NEW_LIGHT_OPACITY}\2',
        content
    )

    # Hiragana mode-card light
    content = re.sub(
        r'(\.learning-app\s+\.mode-card--hiragana::after[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{NEW_LIGHT_OPACITY}\2',
        content
    )
    content = re.sub(
        r'(\.learning-app\s+\.mode-card--hiragana:hover::after[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{NEW_LIGHT_HOVER}\2',
        content
    )

    # dark mode Hiragana mode-card
    content = re.sub(
        r'(body\.theme-dark\s+\.learning-app\s+\.mode-card--hiragana::after[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{DARK_OPACITY}\2',
        content
    )

    # Katakana mode-card light
    content = re.sub(
        r'(body:not\(\.theme-dark\):not\(\.dark-mode\)[\s\S]*?\.mode-card--katakana::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{NEW_LIGHT_OPACITY}\2',
        content
    )
    content = re.sub(
        r'(body:not\(\.theme-dark\):not\(\.dark-mode\)[\s\S]*?\.mode-card--katakana:hover::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
        rf'\g<1>{NEW_LIGHT_HOVER}\2',
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
        c = re.sub(
            r'(background-image:\s*url\("[^"]*c1w\.jpeg"\)\s*!important;[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
            rf'\g<1>{NEW_LIGHT_OPACITY}\2',
            c
        )
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
        c = re.sub(
            r'(background-image:\s*url\("[^"]*c1w\.jpeg"\)\s*!important;[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
            rf'\g<1>{NEW_LIGHT_OPACITY}\2',
            c
        )
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
        c = re.sub(
            r'(background-image:\s*url\("[^"]*w1w\.jpeg"\)\s*!important;[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
            rf'\g<1>{NEW_LIGHT_OPACITY}\2',
            c
        )
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
        # light
        c = re.sub(
            r'(\.dictionary-practice-link::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
            rf'\g<1>{NEW_LIGHT_OPACITY}\2',
            c
        )
        # dark
        c = re.sub(
            r'(body\.theme-dark\s+\.dictionary-practice-link::after,\s*body\.dark-mode\s+\.dictionary-practice-link::after\s*\{[\s\S]*?opacity:\s*)[\d\.]+(\s*!important;)',
            rf'\g<1>{DARK_OPACITY}\2',
            c
        )
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
        
        # Pola Terang di section 7
        c = re.sub(
            r'- Pola Terang \(Light Pattern\):[^\n]+',
            f'- Pola Terang (Light Pattern): Disesuaikan lebih terlihat dan berkarakter pada **`opacity: {NEW_LIGHT_OPACITY} !important`** (hover: `{NEW_LIGHT_HOVER} !important`) agar motif Wagara dan Kumo tampak anggun, jelas, dan tetap menjamin kontras teks di atas 9:1 (WCAG AAA).',
            c
        )
        c = re.sub(
            r'- Pola Gelap \(Dark Pattern\):[^\n]+',
            f'- Pola Gelap (Dark Pattern): Tetap pada **`opacity: {DARK_OPACITY} !important`** (hover: `{DARK_HOVER} !important`) dengan `mix-blend-mode: screen` pada kartu gelap.',
            c
        )
        
        if c != orig:
            with open(agent_path, "w", encoding="utf-8") as f:
                f.write(c)
            print(" [OK] panduan/agent.md diperbarui dengan standar transparansi baru.")

def update_tree_md():
    tree_path = os.path.join(BASE_DIR, "panduan", "tree.md")
    if os.path.exists(tree_path):
        with open(tree_path, "r", encoding="utf-8") as f:
            c = f.read()
        orig = c
        
        c = re.sub(
            r'update_light_pattern_opacity\.py\s*#[^\n]+',
            f'update_light_pattern_opacity.py # Penyesuaian visibilitas pola motif cerah ({NEW_LIGHT_OPACITY}) agar lebih jelas & anggun',
            c
        )
        if c != orig:
            with open(tree_path, "w", encoding="utf-8") as f:
                f.write(c)
            print(" [OK] panduan/tree.md diperbarui.")

def main():
    print("=== MIRAI NO WEBU: Peningkatan Visibilitas Pattern Cerah (0.085) ===")
    update_global_css()
    update_tentang_css()
    update_beranda_css()
    update_kelas_materi_css()
    update_other_css_files()
    update_agent_md()
    update_tree_md()
    print("=== Selesai dengan sukses ===")

if __name__ == "__main__":
    main()
