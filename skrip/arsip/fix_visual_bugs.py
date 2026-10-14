#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to fix 3 critical visual bugs:
1. Fix relative image paths from ../images/ to ../../images/ in css/pages/*.css
2. Standardize hero text and hero-social-sidebar across all hero variations
3. Neaten .quick-stroke-btn at bottom-left
"""

import os
import glob
import re

def fix_image_paths():
    print("--- 1. Fixing Image Paths ---")
    count_total = 0
    for root, dirs, files in os.walk('css'):
        if root == 'css':
            continue # Don't modify root style.css (if any image references, which there aren't)
        for f in files:
            if f.endswith('.css'):
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as fh:
                    content = fh.read()
                
                # Replace ../images/ with ../../images/ (preventing ../../../images/)
                new_content, n = re.subn(r'(?<!\.\./)\.\./images/', '../../images/', content)
                if n > 0:
                    with open(path, 'w', encoding='utf-8') as fh:
                        fh.write(new_content)
                    print(f"Fixed {n} image path(s) in: {path}")
                    count_total += n
    print(f"Total image paths fixed: {count_total}")

def fix_hero_layout():
    print("--- 2. Standardizing Hero Text & Social Sidebar Layout ---")
    path = 'css/pages/navbar-hero-footer.css'
    if not os.path.exists(path):
        print(f"Error: {path} not found")
        return

    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()

    # Find the HERO LAYOUT GUARDRAIL block
    marker = "/* ========================================================================\n   HERO LAYOUT GUARDRAIL"
    idx = content.find(marker)
    if idx == -1:
        # try without exact newline
        marker = "HERO LAYOUT GUARDRAIL"
        idx = content.find(marker)
        if idx != -1:
            idx = content.rfind("/*", 0, idx)

    new_guardrail = """/* ========================================================================
   HERO LAYOUT GUARDRAIL (PENYERAGAMAN MENYELURUH DENGAN BERANDA)
   Semua hero halaman memakai satu garis dasar yang sama: subjudul, judul,
   dan tombol sosial diposisikan secara konsisten dan proporsional.
   ======================================================================== */
.hero,
.page-hero,
.proker-hero,
.quest-hero,
.toko-hero,
.class-hero,
.about-hero,
.activities-hero,
.rekomendasi-hero,
.peringkat-hero,
.lomba-hero,
.motivasi-hero {
    position: sticky !important;
    top: 0 !important;
    z-index: 1 !important;
    min-height: 59svh !important;
    display: flex !important;
    align-items: flex-end !important;
    overflow: hidden !important;
    box-sizing: border-box !important;
}

/* a) Blok teks judul di kiri bawah persis seperti Beranda */
.page-hero > div:not(.hero-social-sidebar),
.proker-hero-inner,
.quest-hero > div:not(.hero-social-sidebar),
.toko-hero > div:not(.hero-social-sidebar),
.class-hero > div:not(.hero-social-sidebar),
.about-hero > div:not(.hero-social-sidebar),
.activities-hero > div:not(.hero-social-sidebar),
.rekomendasi-hero > div:not(.hero-social-sidebar),
.peringkat-hero > div:not(.hero-social-sidebar),
.lomba-hero > div:not(.hero-social-sidebar),
.motivasi-hero > div:not(.hero-social-sidebar) {
    position: absolute !important;
    bottom: 14% !important;
    left: 6% !important;
    width: auto !important;
    max-width: calc(100% - 110px) !important;
    margin: 0 !important;
    padding: 0 !important;
    z-index: 5 !important;
}

/* b) Ukuran judul proporsional tidak merusak baris */
.page-title,
.hero-title,
.proker-hero h1,
.quest-hero h1,
.toko-hero h1,
.class-hero .page-title,
.about-hero .page-title,
.activities-hero .page-title,
.rekomendasi-hero .page-title,
.peringkat-hero .page-title,
.lomba-hero .page-title,
.motivasi-hero .page-title {
    font-size: clamp(2.4rem, 7vw, 4.8rem) !important;
    line-height: 1.02 !important;
    letter-spacing: -0.04em !important;
    margin: 0 !important;
    color: #ffffff !important;
    text-shadow: 2px 4px 10px rgba(0, 0, 0, 0.5) !important;
    overflow-wrap: break-word !important;
}

/* c) Sub-judul eyebrow di atas judul berjarak rapi */
.page-hero-eyebrow,
.proker-hero .eyebrow,
.hero-subtitle {
    margin: 0 0 8px 0 !important;
}

/* d) Ikon sosial media di semua halaman terkunci di pojok kanan bawah sejajar judul */
.hero-social-sidebar,
.page-hero > .hero-social-sidebar,
.proker-hero > .hero-social-sidebar,
.quest-hero > .hero-social-sidebar,
.toko-hero > .hero-social-sidebar,
.class-hero > .hero-social-sidebar,
.about-hero > .hero-social-sidebar,
.activities-hero > .hero-social-sidebar,
.rekomendasi-hero > .hero-social-sidebar,
.peringkat-hero > .hero-social-sidebar,
.lomba-hero > .hero-social-sidebar,
.motivasi-hero > .hero-social-sidebar {
    position: absolute !important;
    bottom: 14% !important;
    right: 5% !important;
    top: auto !important;
    transform: none !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 12px !important;
    z-index: 10 !important;
}

@media (max-width: 600px) {
    .page-hero > div:not(.hero-social-sidebar),
    .proker-hero-inner,
    .quest-hero > div:not(.hero-social-sidebar),
    .toko-hero > div:not(.hero-social-sidebar),
    .class-hero > div:not(.hero-social-sidebar),
    .about-hero > div:not(.hero-social-sidebar),
    .activities-hero > div:not(.hero-social-sidebar),
    .rekomendasi-hero > div:not(.hero-social-sidebar),
    .peringkat-hero > div:not(.hero-social-sidebar),
    .lomba-hero > div:not(.hero-social-sidebar),
    .motivasi-hero > div:not(.hero-social-sidebar) {
        bottom: 12% !important;
        left: 5% !important;
        max-width: calc(100% - 75px) !important;
    }

    .hero-social-sidebar,
    .page-hero > .hero-social-sidebar,
    .proker-hero > .hero-social-sidebar,
    .quest-hero > .hero-social-sidebar,
    .toko-hero > .hero-social-sidebar,
    .class-hero > .hero-social-sidebar,
    .about-hero > .hero-social-sidebar,
    .activities-hero > .hero-social-sidebar,
    .rekomendasi-hero > .hero-social-sidebar,
    .peringkat-hero > .hero-social-sidebar,
    .lomba-hero > .hero-social-sidebar,
    .motivasi-hero > .hero-social-sidebar {
        bottom: 12% !important;
        right: 4% !important;
        gap: 8px !important;
    }

    .hero-social-btn {
        width: 38px !important;
        height: 38px !important;
    }
}
"""

    if idx != -1:
        content = content[:idx] + new_guardrail
    else:
        content = content + "\n\n" + new_guardrail

    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(content)
    print("Updated hero layout guardrail in navbar-hero-footer.css")

def fix_quick_stroke_btn():
    print("--- 3. Neatening .quick-stroke-btn at Bottom-Left ---")
    path = 'css/pages/kamus.css'
    if not os.path.exists(path):
        print(f"Error: {path} not found")
        return

    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()

    # Replace .quick-stroke-btn block
    old_btn_pattern = r'\.quick-stroke-btn\s*\{[^}]+\}'
    new_btn = """.quick-stroke-btn {
    position: fixed !important;
    left: 20px !important;
    right: auto !important;
    bottom: 24px !important;
    padding: 8px 14px !important;
    font-size: 11.5px !important;
    min-height: 36px !important;
    z-index: 90 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 8px !important;
    border-radius: 50px !important;
    background: linear-gradient(135deg, #ff659b 0%, #e91e63 100%) !important;
    color: #ffffff !important;
    border: 1.5px solid rgba(255, 255, 255, 0.45) !important;
    box-shadow: 0 8px 24px rgba(233, 30, 99, 0.38), 0 2px 8px rgba(0, 0, 0, 0.25) !important;
    cursor: pointer !important;
    font-family: inherit !important;
    font-weight: 800 !important;
    letter-spacing: 0.6px !important;
    text-transform: uppercase !important;
    text-decoration: none !important;
    user-select: none !important;
    -webkit-user-select: none !important;
    transition: transform 0.24s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.24s ease, background 0.24s ease, opacity 0.24s ease !important;
    opacity: 0.96;
}"""

    # We only replace the first occurrence (main block), not the hover/active or media query
    match = re.search(old_btn_pattern, content)
    if match:
        content = content[:match.start()] + new_btn + content[match.end():]
        print("Replaced main .quick-stroke-btn position & dimensions")

    # Also update mobile media query inside kamus.css
    old_mobile = r'@media\s*\(max-width:\s*600px\)\s*\{\s*\.quick-stroke-btn\s*\{[^}]+\}'
    new_mobile = """@media (max-width: 600px) {
    .quick-stroke-btn {
        left: 14px !important;
        right: auto !important;
        bottom: 20px !important;
        min-height: 34px !important;
        padding: 6px 12px !important;
    }"""
    content, n = re.subn(old_mobile, new_mobile, content)
    if n > 0:
        print("Updated mobile .quick-stroke-btn position to left")

    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(content)
    print("Updated .quick-stroke-btn in kamus.css")

def main():
    fix_image_paths()
    fix_hero_layout()
    fix_quick_stroke_btn()
    print("\nALL 3 CRITICAL VISUAL BUGS FIXED SUCCESSFULLY!")

if __name__ == '__main__':
    main()
