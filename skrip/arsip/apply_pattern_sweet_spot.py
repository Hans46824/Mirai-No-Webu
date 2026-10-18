#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: skrip/arsip/apply_pattern_sweet_spot.py
Deskripsi:
  Mengunci "Titik Emas (Sweet Spot)" transparansi untuk ke-4 pattern master:
  1. Kartu Terang (c1w.jpeg)       -> Opacity 15% (--opacity-c1w: 0.15, overlay putih 85%)
  2. Kartu Gelap (c1b.jpeg)        -> Opacity 11% (--opacity-c1b: 0.11, overlay obsidian 89%)
  3. Section/Kartu Terang (w1w.jpeg) -> Opacity 10% (--opacity-w1w: 0.10, overlay putih 90%)
  4. Section Gelap & Footer (w1b.jpeg) -> Opacity 13% (--opacity-w1b: 0.13, overlay obsidian 87%)
  Serta menambahkan text-shadow halus pada seluruh teks kartu gelap agar 100% tajam & nyaman dibaca.
"""

import os
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
CSS_DIR = ROOT_DIR / "css" / "pages"
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

def update_global_css():
    file_path = CSS_DIR / "global.css"
    content = file_path.read_text(encoding="utf-8")
    orig = content

    # 1. Update :root dengan 4 variabel spesifik Titik Emas
    root_pattern_block = """  /* 4 Variabel Transparansi Spesifik Titik Emas (Sweet Spot) */
  --opacity-c1w: 0.15;
  --overlay-card-light: linear-gradient(135deg, rgba(255, 250, 252, 0.85), rgba(255, 245, 249, 0.85));

  --opacity-c1b: 0.11;
  --overlay-card-dark: linear-gradient(155deg, rgba(16, 12, 24, 0.89), rgba(11, 9, 17, 0.89));

  --opacity-w1w: 0.10;
  --overlay-section-light: linear-gradient(180deg, rgba(255, 255, 255, 0.90), rgba(255, 250, 252, 0.90));

  --opacity-w1b: 0.13;
  --overlay-section-dark: linear-gradient(180deg, rgba(14, 11, 18, 0.87), rgba(14, 11, 18, 0.87));

  /* Proportional Hover Opacities */
  --opacity-c1w-hover: 0.22;
  --opacity-c1b-hover: 0.16;
  --opacity-w1w-hover: 0.15;
  --opacity-w1b-hover: 0.18;

  /* Backward Compatibility */
  --pattern-opacity-light: var(--opacity-c1w);
  --pattern-opacity-light-hover: var(--opacity-c1w-hover);
  --pattern-opacity-dark: var(--opacity-c1b);
  --pattern-opacity-dark-hover: var(--opacity-c1b-hover);"""

    # Ganti blok lama di :root
    content = re.sub(
        r'  --pattern-opacity-light:[\s\S]*?--overlay-section-dark:[^\n]+;',
        root_pattern_block,
        content
    )

    # 2. .mirai-card-light::after -> --opacity-c1w
    content = re.sub(
        r'(\.mirai-card-light::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1w)\2',
        content
    )

    # 3. .mirai-card-dark::after -> --opacity-c1b
    content = re.sub(
        r'(\.mirai-card-dark::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1b)\2',
        content
    )

    # 4. .section-quote-slider.quote-theme-white .quote-card::after -> --opacity-w1w
    content = re.sub(
        r'(\.section-quote-slider\.quote-theme-white\s+\.quote-card::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1w)\2',
        content
    )

    # 5. .quote-card:not(.quote-theme-white)::after -> --opacity-c1b
    content = re.sub(
        r'(\.quote-card:not\(\.quote-theme-white\)::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1b)\2',
        content
    )

    # 6. .proker-hero ~ section:nth-of-type(even) ... ::after -> --opacity-w1b
    content = re.sub(
        r'(\.proker-hero\s*~[^{}]*::after\s*\{[^{}]*opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1b)\2',
        content
    )

    # 7. Tambahkan Text Shadow Halus pada Teks Kartu Gelap jika belum ada
    dark_text_shadow_rule = """
/* ==========================================================================
   TEXT-SHADOW HALUS TEKS KARTU GELAP (100% KETASTISAN & KETERBACAAN TEKS)
   ========================================================================== */
.mirai-card-dark,
.mirai-card-dark h1, .mirai-card-dark h2, .mirai-card-dark h3, .mirai-card-dark h4, .mirai-card-dark h5, .mirai-card-dark h6,
.mirai-card-dark p, .mirai-card-dark span, .mirai-card-dark a,
.quote-card:not(.quote-theme-white),
.timeline-content, .about-intro-card, .about-name-card, .history-origin-card,
.slogan-hero-card, .slogan-card, .achievement-card, .accessory-card,
.accessory-banner-card, .prestasi-stat-box, .podium-card, .lb-category-desc-card,
.lb-table-card, .lb-system-info-card, .event-card, .rek-card, .toko-card,
.doc-big-card, .kurikulum-page-section .doc-big-card,
#lanjutan .course-card, .facility-card,
body.dark-mode .program-card, body.theme-dark .program-card,
body.dark-mode .start-card, body.theme-dark .start-card,
body.dark-mode .lomba-detail-card, body.theme-dark .lomba-detail-card,
body.dark-mode .dictionary-practice-link, body.theme-dark .dictionary-practice-link {
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.65);
}
"""
    if "/* TEXT-SHADOW HALUS TEKS KARTU GELAP" not in content:
        content = content.rstrip() + "\n" + dark_text_shadow_rule

    if content != orig:
        file_path.write_text(content, encoding="utf-8")
        print("  ✔ css/pages/global.css berhasil diperbarui dengan 4 variabel titik emas & text-shadow.")
    else:
        print("  ℹ css/pages/global.css tidak berubah.")


def update_navbar_hero_footer():
    file_path = CSS_DIR / "navbar-hero-footer.css"
    content = file_path.read_text(encoding="utf-8")
    orig = content

    # .global-footer::before -> --opacity-c1b (0.11)
    content = re.sub(
        r'(\.global-footer::before\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1b)\2',
        content
    )

    if content != orig:
        file_path.write_text(content, encoding="utf-8")
        print("  ✔ css/pages/navbar-hero-footer.css diperbarui.")
    else:
        print("  ℹ css/pages/navbar-hero-footer.css tidak berubah.")


def update_beranda_css():
    file_path = CSS_DIR / "beranda.css"
    content = file_path.read_text(encoding="utf-8")
    orig = content

    # .start-card::after, .curriculum-cards a::after (c1w) -> --opacity-c1w
    content = re.sub(
        r'(\.start-card::after,\s*\.curriculum-cards\s+a::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1w)\2',
        content
    )
    # hover -> --opacity-c1w-hover
    content = re.sub(
        r'(\.start-card:hover::after,\s*\.curriculum-cards\s+a:hover::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1w-hover)\2',
        content
    )

    # dark-mode .start-card::after (c1b) -> --opacity-c1b
    content = re.sub(
        r'(body\.dark-mode\s+\.start-card::after[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1b)\2',
        content
    )

    # .activity-start-card::after (c1b) -> --opacity-c1b
    content = re.sub(
        r'(\.activity-start-card::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1b)\2',
        content
    )
    # light .activity-start-card::after (c1w) -> --opacity-c1w
    content = re.sub(
        r'(body:not\(\.dark-mode\):not\(\.theme-dark\)[\s\S]*?\.activity-start-card::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1w)\2',
        content
    )

    # .class-card::after (w1b) -> --opacity-w1b
    content = re.sub(
        r'(\.class-card::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1b)\2',
        content
    )

    # .division-card::after (w1b) -> --opacity-w1b
    content = re.sub(
        r'(\.division-card::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1b)\2',
        content
    )

    # .program-card::after (w1w) -> --opacity-w1w
    content = re.sub(
        r'(\.program-card::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1w)\2',
        content
    )
    # hover -> --opacity-w1w-hover
    content = re.sub(
        r'(\.program-card:hover::after,\s*\.program-card-link:hover\s+\.program-card::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1w-hover)\2',
        content
    )

    # dark-mode .program-card::after (w1b) -> --opacity-w1b
    content = re.sub(
        r'(body\.dark-mode\s+\.program-card::after,\s*body\.theme-dark\s+\.program-card::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1b)\2',
        content
    )
    # hover dark -> --opacity-w1b-hover
    content = re.sub(
        r'(body\.dark-mode\s+\.program-card:hover::after,\s*body\.theme-dark\s+\.program-card:hover::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1b-hover)\2',
        content
    )

    # .feedback-theme-white .feedback-feature-card::after (c1w) -> --opacity-c1w
    content = re.sub(
        r'(\.feedback-theme-white\s+\.feedback-feature-card::after[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1w)\2',
        content
    )
    content = re.sub(
        r'(\.feedback-theme-white\s+\.feedback-feature-card:hover::after[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1w-hover)\2',
        content
    )

    # .feedback-theme-dark (c1b) -> --opacity-c1b
    content = re.sub(
        r'(\.feedback-theme-dark\s+\.feedback-feature-card::after[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1b)\2',
        content
    )
    content = re.sub(
        r'(\.feedback-theme-dark\s+\.feedback-feature-card:hover::after[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1b-hover)\2',
        content
    )

    if content != orig:
        file_path.write_text(content, encoding="utf-8")
        print("  ✔ css/pages/beranda.css diperbarui.")
    else:
        print("  ℹ css/pages/beranda.css tidak berubah.")


def update_tentang_css():
    file_path = CSS_DIR / "tentang.css"
    content = file_path.read_text(encoding="utf-8")
    orig = content

    # .timeline-content::after (w1b) -> --opacity-w1b
    content = re.sub(
        r'(\.timeline-content::after[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1b)\2',
        content
    )
    content = re.sub(
        r'(\.timeline-node:hover\s+\.timeline-content::after,\s*\.timeline-content:hover::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1b-hover)\2',
        content
    )

    # .about-intro-card::after, .about-name-card::after, ... (w1b) -> --opacity-w1b
    content = re.sub(
        r'(\.about-intro-card::after,\s*\.about-name-card::after[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1b)\2',
        content
    )
    content = re.sub(
        r'(\.about-intro-card:hover::after,\s*\.about-name-card:hover::after[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1b-hover)\2',
        content
    )

    # .event-card::after, .rek-cat-explain-card::after, ... (c1b) -> --opacity-c1b
    content = re.sub(
        r'(\.event-card::after,\s*\.rek-cat-explain-card::after[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1b)\2',
        content
    )
    content = re.sub(
        r'(\.event-card:hover::after,\s*\.rek-cat-explain-card:hover::after[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1b-hover)\2',
        content
    )

    # .flag-mockup-frame::after (w1w) -> --opacity-w1w
    content = re.sub(
        r'(\.flag-mockup-frame::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1w)\2',
        content
    )
    content = re.sub(
        r'(\.flag-feature-card:hover\s+\.flag-mockup-frame::after,\s*\.flag-mockup-frame:hover::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1w-hover)\2',
        content
    )

    # dark-mode .flag-mockup-frame::after (w1b) -> --opacity-w1b
    content = re.sub(
        r'(body\.theme-dark\s+\.flag-mockup-frame::after,\s*body\.dark-mode\s+\.flag-mockup-frame::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1b)\2',
        content
    )
    content = re.sub(
        r'(body\.theme-dark\s+\.flag-mockup-frame:hover::after,\s*body\.dark-mode\s+\.flag-mockup-frame:hover::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1b-hover)\2',
        content
    )

    # .flag-feature-card::after, .logo-meaning-badge-col::after, ... (w1w) -> --opacity-w1w
    content = re.sub(
        r'(\.flag-feature-card::after,\s*\.logo-meaning-badge-col::after[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1w)\2',
        content
    )
    content = re.sub(
        r'(\.flag-feature-card:hover::after,\s*\.logo-meaning-badge-col:hover::after[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1w-hover)\2',
        content
    )

    # .page-kegiatan .program-card::after (w1w) -> --opacity-w1w
    content = re.sub(
        r'(\.page-kegiatan\s+\.program-card::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1w)\2',
        content
    )
    content = re.sub(
        r'(\.page-kegiatan\s+\.program-card:hover::after[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1w-hover)\2',
        content
    )

    # dark-mode .page-kegiatan .program-card::after (w1b) -> --opacity-w1b
    content = re.sub(
        r'(body\.dark-mode\s+\.page-kegiatan\s+\.program-card::after[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1b)\2',
        content
    )
    content = re.sub(
        r'(body\.dark-mode\s+\.page-kegiatan\s+\.program-card:hover::after[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1b-hover)\2',
        content
    )

    # .page-lomba .lomba-detail-card::after (c1w) -> --opacity-c1w
    content = re.sub(
        r'(\.page-lomba\s+\.lomba-detail-card::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1w)\2',
        content
    )
    content = re.sub(
        r'(\.page-lomba\s+\.lomba-detail-card:hover::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1w-hover)\2',
        content
    )

    # dark-mode .page-lomba .lomba-detail-card::after (c1b) -> --opacity-c1b
    content = re.sub(
        r'(body\.dark-mode\s+\.page-lomba\s+\.lomba-detail-card::after[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1b)\2',
        content
    )
    content = re.sub(
        r'(body\.dark-mode\s+\.page-lomba\s+\.lomba-detail-card:hover::after[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1b-hover)\2',
        content
    )

    if content != orig:
        file_path.write_text(content, encoding="utf-8")
        print("  ✔ css/pages/tentang.css diperbarui.")
    else:
        print("  ℹ css/pages/tentang.css tidak berubah.")


def update_kelas_materi_css():
    file_path = CSS_DIR / "kelas-materi.css"
    content = file_path.read_text(encoding="utf-8")
    orig = content

    # .kurikulum-page-section .doc-big-card::after, .doc-big-card::after (c1b) -> --opacity-c1b
    content = re.sub(
        r'(\.kurikulum-page-section\s+\.doc-big-card::after,\s*\.doc-big-card::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1b)\2',
        content
    )
    content = re.sub(
        r'(\.kurikulum-page-section\s+\.doc-big-card:hover::after,\s*\.doc-big-card:hover::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1b-hover)\2',
        content
    )

    # #lanjutan .course-card::after (w1b) -> --opacity-w1b
    content = re.sub(
        r'(#lanjutan\s+\.course-card::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1b)\2',
        content
    )
    content = re.sub(
        r'(#lanjutan\s+\.course-card:hover::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1b-hover)\2',
        content
    )

    # .page-kelas #kurikulum .doc-big-card::after (w1w) -> --opacity-w1w
    content = re.sub(
        r'(\.page-kelas\s+#kurikulum\s+\.doc-big-card::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1w)\2',
        content
    )
    content = re.sub(
        r'(\.page-kelas\s+#kurikulum\s+\.doc-big-card:hover::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1w-hover)\2',
        content
    )

    # dark-mode .page-kelas #kurikulum .doc-big-card::after (w1b) -> --opacity-w1b
    content = re.sub(
        r'(body\.dark-mode\s+\.page-kelas\s+#kurikulum\s+\.doc-big-card::after[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1b)\2',
        content
    )

    # .class-card::after (w1b) -> --opacity-w1b
    content = re.sub(
        r'(\.class-card::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1b)\2',
        content
    )
    content = re.sub(
        r'(\.class-card:hover::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1b-hover)\2',
        content
    )

    # #dasar .course-card::after (w1w) -> --opacity-w1w
    content = re.sub(
        r'(#dasar\s+\.course-card::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1w)\2',
        content
    )
    content = re.sub(
        r'(#dasar\s+\.course-card:hover::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1w-hover)\2',
        content
    )

    # .page-kelas-dasar .roadmap article::after (w1w) -> --opacity-w1w
    content = re.sub(
        r'(\.page-kelas-dasar\s+\.roadmap\s+article::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1w)\2',
        content
    )

    # .learning-app .mode-card--hiragana::after (c1w) -> --opacity-c1w
    content = re.sub(
        r'(\.learning-app\s+\.mode-card--hiragana::after[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1w)\2',
        content
    )
    content = re.sub(
        r'(\.learning-app\s+\.mode-card--hiragana:hover::after[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1w-hover)\2',
        content
    )

    # dark-mode .learning-app .mode-card--hiragana::after (c1b) -> --opacity-c1b
    content = re.sub(
        r'(body\.theme-dark\s+\.learning-app\s+\.mode-card--hiragana::after[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1b)\2',
        content
    )
    content = re.sub(
        r'(body\.theme-dark\s+\.learning-app\s+\.mode-card--hiragana:hover::after[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1b-hover)\2',
        content
    )

    # .mode-card--katakana::after (w1b) -> --opacity-w1b
    content = re.sub(
        r'(\.learning-app\s+\.mode-card--katakana::after[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1b)\2',
        content
    )
    content = re.sub(
        r'(\.learning-app\s+\.mode-card--katakana:hover::after[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1b-hover)\2',
        content
    )
    content = re.sub(
        r'(body:not\(\.theme-dark\):not\(\.dark-mode\)[\s\S]*?\.mode-card--katakana::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1b)\2',
        content
    )
    content = re.sub(
        r'(body:not\(\.theme-dark\):not\(\.dark-mode\)[\s\S]*?\.mode-card--katakana:hover::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1b-hover)\2',
        content
    )

    if content != orig:
        file_path.write_text(content, encoding="utf-8")
        print("  ✔ css/pages/kelas-materi.css diperbarui.")
    else:
        print("  ℹ css/pages/kelas-materi.css tidak berubah.")


def update_rekomendasi_motivasi_css():
    file_path = CSS_DIR / "rekomendasi-motivasi.css"
    content = file_path.read_text(encoding="utf-8")
    orig = content

    # .motivasi-spotlight-card::before (c1b) -> --opacity-c1b
    content = re.sub(
        r'(\.motivasi-spotlight-card::before\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1b)\2',
        content
    )

    # .rek-card::after (c1b) -> --opacity-c1b
    content = re.sub(
        r'(\.rek-card::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1b)\2',
        content
    )
    content = re.sub(
        r'(\.rek-card:hover::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1b-hover)\2',
        content
    )

    # .section-quote-slider.quote-theme-dark .quote-card::after (c1b) -> --opacity-c1b
    content = re.sub(
        r'(\.section-quote-slider\.quote-theme-dark\s+\.quote-card::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1b)\2',
        content
    )
    content = re.sub(
        r'(\.section-quote-slider\.quote-theme-dark\s+\.quote-card:hover::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1b-hover)\2',
        content
    )

    # .section-quote-slider.quote-theme-white .quote-card::after (w1w) -> --opacity-w1w
    content = re.sub(
        r'(\.section-quote-slider\.quote-theme-white\s+\.quote-card::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1w)\2',
        content
    )

    if content != orig:
        file_path.write_text(content, encoding="utf-8")
        print("  ✔ css/pages/rekomendasi-motivasi.css diperbarui.")
    else:
        print("  ℹ css/pages/rekomendasi-motivasi.css tidak berubah.")


def update_other_css():
    # kamus.css
    kamus_path = CSS_DIR / "kamus.css"
    content = kamus_path.read_text(encoding="utf-8")
    orig = content
    content = re.sub(
        r'(\.dictionary-practice-link::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1w)\2',
        content
    )
    content = re.sub(
        r'(body\.theme-dark\s+\.dictionary-practice-link::after,\s*body\.dark-mode\s+\.dictionary-practice-link::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1b)\2',
        content
    )
    if content != orig:
        kamus_path.write_text(content, encoding="utf-8")
        print("  ✔ css/pages/kamus.css diperbarui.")

    # kegiatan-divisi.css
    kg_path = CSS_DIR / "kegiatan-divisi.css"
    content = kg_path.read_text(encoding="utf-8")
    orig = content
    content = re.sub(
        r'(\.facility-card::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1b)\2',
        content
    )
    content = re.sub(
        r'(\.facility-card:hover::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-w1b-hover)\2',
        content
    )
    if content != orig:
        kg_path.write_text(content, encoding="utf-8")
        print("  ✔ css/pages/kegiatan-divisi.css diperbarui.")

    # lomba.css
    lomba_path = CSS_DIR / "lomba.css"
    content = lomba_path.read_text(encoding="utf-8")
    orig = content
    content = re.sub(
        r'(\.lomba-detail-card::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1w)\2',
        content
    )
    content = re.sub(
        r'(body\.dark-mode\s+\.lomba-detail-card::after,\s*body\.theme-dark\s+\.lomba-detail-card::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1b)\2',
        content
    )
    content = re.sub(
        r'(\.lomba-detail-card:hover::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1w-hover)\2',
        content
    )
    if content != orig:
        lomba_path.write_text(content, encoding="utf-8")
        print("  ✔ css/pages/lomba.css diperbarui.")

    # toko.css
    toko_path = CSS_DIR / "toko.css"
    content = toko_path.read_text(encoding="utf-8")
    orig = content
    # .toko-card::after (c1b)
    content = re.sub(
        r'(\.toko-card::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1b)\2',
        content
    )
    content = re.sub(
        r'(\.toko-card:hover::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1b-hover)\2',
        content
    )
    # .toko-step-card-white::after (c1w)
    content = re.sub(
        r'(\.toko-step-card-white::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1w)\2',
        content
    )
    content = re.sub(
        r'(\.toko-step-card-white:hover::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1w-hover)\2',
        content
    )
    # .toko-kwu-card::after (c1b)
    content = re.sub(
        r'(\.toko-kwu-card::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1b)\2',
        content
    )
    # .toko-faq-item-white::after (c1w)
    content = re.sub(
        r'(\.toko-faq-item-white::after\s*\{[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1w)\2',
        content
    )
    # seksi panduan pemesanan & FAQ white (c1w)
    content = re.sub(
        r'(background-image:\s*url\("[^"]*c1w\.jpeg"\)\s*!important;[\s\S]*?opacity:\s*)[^;]+(\s*!important;)',
        r'\g<1>var(--opacity-c1w)\2',
        content
    )
    if content != orig:
        toko_path.write_text(content, encoding="utf-8")
        print("  ✔ css/pages/toko.css diperbarui.")


def update_agent_md():
    agent_path = ROOT_DIR / "panduan" / "agent.md"
    content = agent_path.read_text(encoding="utf-8")
    orig = content

    pattern_spec_doc = """1. **Master Variabel Pattern & Gradien Terpusat di `:root` (`css/pages/global.css`)**:
   - `--pattern-c1w: url("../../images/mirai/background/c1w.jpeg");` (Kumo/Awan Terang)
   - `--pattern-c1b: url("../../images/mirai/background/c1b.jpeg");` (Kumo/Awan Gelap)
   - `--pattern-w1w: url("../../images/mirai/background/w1w.jpeg");` (Wagara/Ombak Terang)
   - `--pattern-w1b: url("../../images/mirai/background/w1b.jpeg");` (Wagara/Ombak Gelap)
   - `--opacity-c1w: 0.15;` (Kartu Terang: Kelihatan 15%, Overlay Putih 85%)
   - `--overlay-card-light: linear-gradient(135deg, rgba(255, 250, 252, 0.85), rgba(255, 245, 249, 0.85));`
   - `--opacity-c1b: 0.11;` (Kartu Gelap: Kelihatan 11%, Overlay Obsidian 89%)
   - `--overlay-card-dark: linear-gradient(155deg, rgba(16, 12, 24, 0.89), rgba(11, 9, 17, 0.89));`
   - `--opacity-w1w: 0.10;` (Section Terang: Kelihatan 10%, Overlay Putih 90%)
   - `--overlay-section-light: linear-gradient(180deg, rgba(255, 255, 255, 0.90), rgba(255, 250, 252, 0.90));`
   - `--opacity-w1b: 0.13;` (Section Gelap & Footer: Kelihatan 13%, Overlay Obsidian 87%)
   - `--overlay-section-dark: linear-gradient(180deg, rgba(14, 11, 18, 0.87), rgba(14, 11, 18, 0.87));`

2. **Kunci Transparansi "Titik Emas (Sweet Spot)" & Keterbacaan Teks Mutlak**:
   - **Kartu Terang (c1w.jpeg)**: Dikunci pada **`opacity: var(--opacity-c1w) !important;`** (`0.15`, hover `0.22`) dengan gradien penutup 85% agar tekstur awan Kumo tampil anggun dan nyata.
   - **Kartu Gelap (c1b.jpeg)**: Dikunci pada **`opacity: var(--opacity-c1b) !important;`** (`0.11`, hover `0.16`) dengan `mix-blend-mode: screen` dan gradien penutup 89%.
   - **Section/Kartu Terang (w1w.jpeg)**: Dikunci pada **`opacity: var(--opacity-w1w) !important;`** (`0.10`, hover `0.15`) dengan gradien penutup 90% untuk motif gelombang ombak Seigaiha.
   - **Section Gelap & Footer (w1b.jpeg)**: Dikunci pada **`opacity: var(--opacity-w1b) !important;`** (`0.13`, hover `0.18`) dengan gradien penutup 87%.
   - **Perlindungan Ketajaman Huruf**: Seluruh teks pada kartu gelap dibekali `text-shadow: 0 1px 3px rgba(0, 0, 0, 0.65);` agar huruf putih tetap tajam 100% saat melintasi garis motif."""

    content = re.sub(
        r'1\. \*\*Master Variabel Pattern & Gradien Terpusat di `:root`[\s\S]*?2\. \*\*Kunci Transparansi Watermark Sangat Lembut[^\n]+(?:\n[ \t]*-[^\n]+)+',
        pattern_spec_doc,
        content
    )

    if content != orig:
        agent_path.write_text(content, encoding="utf-8")
        print("  ✔ panduan/agent.md diperbarui dengan dokumentasi Titik Emas.")


def update_tree_md():
    tree_path = ROOT_DIR / "panduan" / "tree.md"
    content = tree_path.read_text(encoding="utf-8")
    orig = content

    if "apply_pattern_sweet_spot.py" not in content:
        content = content.replace(
            "│       ├── update_light_pattern_opacity.py",
            "│       ├── apply_pattern_sweet_spot.py # Kunci Titik Emas 4 pattern (c1w 15%, c1b 11%, w1w 10%, w1b 13%)\n│       ├── update_light_pattern_opacity.py"
        )

    if content != orig:
        tree_path.write_text(content, encoding="utf-8")
        print("  ✔ panduan/tree.md diperbarui.")


def main():
    print("==================================================")
    print("✨ MIRAI NO WEBU — KUNCI TITIK EMAS 4 PATTERN")
    print("==================================================")
    update_global_css()
    update_navbar_hero_footer()
    update_beranda_css()
    update_tentang_css()
    update_kelas_materi_css()
    update_rekomendasi_motivasi_css()
    update_other_css()
    update_agent_md()
    update_tree_md()

    print("\n🏷️  Menjalankan Version Stamping & Precache Rebuild...")
    from stamp_asset_versions import main as stamp_main
    stamp_main()

    from build_precache_list import build_service_worker
    build_service_worker()

    print("\n🎉 SELURUH FILE CSS TELAH TERKUNCI PADA TITIK EMAS DENGAN SUKSES!")

if __name__ == "__main__":
    main()
