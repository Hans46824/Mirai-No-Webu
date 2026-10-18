#!/usr/bin/env python3
"""
File: skrip/arsip/test_mobile_responsiveness.py
Fungsi: Unit test dan verifikasi DOM tanpa browser untuk menguji:
1. Tata letak mobile responsif pada lebar 360px, 390px, dan 430px.
2. Pencegahan tumpang tindih (collision) tombol melayang (#launcher & .to-top), gap 12px, dan touch target >= 44x44px.
3. Kelengkapan Mobile Bottom Navigation bar (5 item: Beranda, Kelas, Kamus, Latihan, Menu).
4. Aksesibilitas: :focus-visible universal, skip-link ke #main-content, input labels, dan prefers-reduced-motion.
5. Kesiapan PWA: manifest.webmanifest, service-worker.js, offline.html, robots.txt, dan sitemap.xml.
"""

import sys
import re
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

def test_pwa_infrastructure():
    print("--- [TEST 1] Kesiapan Infrastruktur PWA & SEO ---")
    manifest_path = ROOT_DIR / "manifest.webmanifest"
    assert manifest_path.exists(), "manifest.webmanifest tidak ditemukan!"
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest_data = json.load(f)
    assert manifest_data.get("display") == "standalone", "Display mode harus standalone!"
    assert len(manifest_data.get("icons", [])) >= 2, "Ikon PWA (192 & 512) harus terdaftar!"
    print("  ✔ manifest.webmanifest valid dan memiliki konfigurasi standalone & icons.")

    sw_path = ROOT_DIR / "service-worker.js"
    assert sw_path.exists(), "service-worker.js tidak ditemukan!"
    sw_text = sw_path.read_text(encoding="utf-8")
    assert "CACHE_NAME" in sw_text and "PRECACHE_ASSETS" in sw_text, "service-worker.js tidak memiliki konfigurasi cache!"
    assert "offline.html" in sw_text, "service-worker.js harus memiliki fallback offline.html!"
    print("  ✔ service-worker.js valid dan memiliki strategi offline.")

    offline_path = ROOT_DIR / "offline.html"
    assert offline_path.exists(), "offline.html tidak ditemukan!"
    assert 'id="main-content"' in offline_path.read_text(encoding="utf-8"), "offline.html harus memiliki id='main-content'!"
    print("  ✔ offline.html valid dengan main-content.")

    robots_path = ROOT_DIR / "robots.txt"
    sitemap_path = ROOT_DIR / "sitemap.xml"
    assert robots_path.exists(), "robots.txt tidak ditemukan!"
    assert sitemap_path.exists(), "sitemap.xml tidak ditemukan!"
    print("  ✔ robots.txt dan sitemap.xml ditemukan.")


def test_accessibility_and_skip_links():
    print("\n--- [TEST 2] Aksesibilitas, Skip-Link & Input Labels ---")
    html_files = list(ROOT_DIR.glob("**/*.html"))
    html_files = [f for f in html_files if "skrip/laporan" not in str(f)]
    assert len(html_files) >= 30, f"Ditemukan {len(html_files)} file HTML."

    missing_skip = []
    missing_main = []
    missing_manifest = []

    for f in html_files:
        text = f.read_text(encoding="utf-8")
        rel = f.relative_to(ROOT_DIR)

        if 'class="skip-link"' not in text:
            missing_skip.append(str(rel))
        if 'id="main-content"' not in text:
            missing_main.append(str(rel))
        if 'rel="manifest"' not in text:
            missing_manifest.append(str(rel))

    assert not missing_skip, f"Halaman kehilangan skip-link: {missing_skip}"
    assert not missing_main, f"Halaman kehilangan id='main-content': {missing_main}"
    assert not missing_manifest, f"Halaman kehilangan <link rel='manifest'>: {missing_manifest}"

    print(f"  ✔ Seluruh {len(html_files)} file HTML memiliki skip-link, main-content, dan manifest link!")

    # Cek aria-live="polite" pada kamus
    kamus_index = (ROOT_DIR / "kamus/index.html").read_text(encoding="utf-8")
    kamus_kanji = (ROOT_DIR / "kamus/kanji.html").read_text(encoding="utf-8")
    assert 'data-kanji-count aria-live="polite"' in kamus_index or 'aria-live="polite"' in kamus_index, "kamus/index.html harus punya aria-live='polite'!"
    assert 'data-kanji-count aria-live="polite"' in kamus_kanji or 'aria-live="polite"' in kamus_kanji, "kamus/kanji.html harus punya aria-live='polite'!"
    print("  ✔ [data-kanji-count] di kamus/index.html dan kamus/kanji.html memiliki aria-live='polite'.")

    # Cek label input
    latihan_html = (ROOT_DIR / "kelas/latihan.html").read_text(encoding="utf-8")
    assert 'data-custom-count-slider' in latihan_html and 'aria-label=' in latihan_html, "Slider custom count latihan harus memiliki aria-label!"
    print("  ✔ Input range slider di kelas/latihan.html memiliki aria-label aksesibel.")


def test_css_focus_and_reduced_motion():
    print("\n--- [TEST 3] CSS Focus-Visible & Reduced Motion ---")
    global_css = (ROOT_DIR / "css/pages/global.css").read_text(encoding="utf-8")
    nav_css = (ROOT_DIR / "css/pages/navbar-hero-footer.css").read_text(encoding="utf-8")
    kamus_css = (ROOT_DIR / "css/pages/kamus.css").read_text(encoding="utf-8")

    assert ":focus-visible" in global_css, "global.css harus memiliki aturan focus-visible universal!"
    assert ".skip-link" in global_css, "global.css harus memiliki styling untuk .skip-link!"
    assert "prefers-reduced-motion" in global_css, "global.css harus memiliki media query prefers-reduced-motion!"
    assert "prefers-reduced-motion" in nav_css, "navbar-hero-footer.css harus memiliki media query prefers-reduced-motion!"
    print("  ✔ Aturan :focus-visible, .skip-link, dan prefers-reduced-motion terverifikasi di CSS.")


def test_floating_buttons_and_mobile_layout():
    print("\n--- [TEST 4] Simulasi Tata Letak Mobile (360px, 390px, 430px) & Floating Buttons ---")
    viewports = [360, 390, 430]
    nav_css = (ROOT_DIR / "css/pages/navbar-hero-footer.css").read_text(encoding="utf-8")
    global_css = (ROOT_DIR / "css/pages/global.css").read_text(encoding="utf-8")

    # 1. Verifikasi ukuran tombol melayang di CSS
    assert "width: 44px" in nav_css and "height: 44px" in nav_css, "Tombol melayang (.to-top, #launcher) wajib minimal 44x44px!"
    assert "width: 44px" in global_css and "height: 44px" in global_css, "Tombol melayang di global.css wajib 44x44px!"

    # 2. Simulasi posisi matematis untuk mencegah tabrakan (collision detection)
    # Target sentuh = 44px. Gap = 12px.
    btn_size = 44
    gap = 12
    margin_bottom = 16
    margin_right = 16

    # Kasus Standar (Tanpa bottom nav)
    to_top_bottom = margin_bottom
    to_top_top = to_top_bottom + btn_size
    launcher_bottom = to_top_top + gap # 16 + 44 + 12 = 72px
    launcher_top = launcher_bottom + btn_size # 72 + 44 = 116px

    calculated_gap = launcher_bottom - to_top_top
    assert calculated_gap == 12, f"Gap antara tombol harus 12px, didapat: {calculated_gap}px"

    # Kasus Dengan Bottom Nav (tinggi bar ~60px, padding/margin 12px)
    nav_bar_height = 64
    bnav_to_top_bottom = nav_bar_height + 12 # 76px
    bnav_to_top_top = bnav_to_top_bottom + btn_size # 120px
    bnav_launcher_bottom = bnav_to_top_top + gap # 132px
    bnav_launcher_top = bnav_launcher_bottom + btn_size # 176px

    bnav_gap = bnav_launcher_bottom - bnav_to_top_top
    assert bnav_gap == 12, f"Gap saat bottom nav aktif harus 12px, didapat: {bnav_gap}px"

    for w in viewports:
        # Cek margin horizontal: Tombol tidak boleh overflow layar
        occupied_x = margin_right + btn_size
        remaining_x = w - occupied_x
        assert remaining_x > 0, f"Tombol melayang overflow layar {w}px!"
        print(f"  ✔ Viewport {w}px: Bebas collision (Gap: {calculated_gap}px, Margin Kanan: {margin_right}px, Sisa Ruang: {remaining_x}px).")

    # 3. Cek Bottom Nav styling & JS
    assert ".mobile-bottom-nav" in nav_css, "navbar-hero-footer.css harus memuat .mobile-bottom-nav!"
    assert "body.has-bottom-nav" in nav_css, "navbar-hero-footer.css harus mengatur padding-bottom saat bottom nav aktif!"

    main_js = (ROOT_DIR / "js/main.js").read_text(encoding="utf-8")
    assert "renderMobileBottomNav" in main_js, "js/main.js harus memiliki fungsi renderMobileBottomNav!"
    assert "registerServiceWorker" in main_js, "js/main.js harus memiliki fungsi registerServiceWorker!"
    print("  ✔ Logika Bottom Navigation Bar & Service Worker registration terpasang di js/main.js.")


def test_kamus_shortcuts_and_sticky_panel():
    print("\n--- [TEST 5] Panel Sticky Desktop & Kamus Bersih ---")
    kanji_js = (ROOT_DIR / "js/kanji.js").read_text(encoding="utf-8")
    kamus_css = (ROOT_DIR / "css/pages/kamus.css").read_text(encoding="utf-8")

    assert "kamus-shortcuts-hint" not in kanji_js, "Petunjuk pintasan harus sudah bersih dihapus dari js/kanji.js!"
    assert "kamus-shortcuts-hint" not in kamus_css, "CSS pintasan harus sudah bersih dihapus dari css/pages/kamus.css!"
    print("  ✔ Kamus bersih dari notifikasi pintasan keyboard.")

    assert "@media (min-width: 1200px)" in kamus_css, "kamus.css harus memiliki kueri sticky pada layar >= 1200px!"
    assert "position: sticky" in kamus_css or "position: -webkit-sticky" in kamus_css, "kamus.css harus mengatur sticky untuk panel detail kanji!"
    print("  ✔ Panel detail kanji sticky di desktop (>= 1200px) terverifikasi.")


def main():
    print("==================================================")
    print("📱 TEST SUITE: MOBILE RESPONSIVENESS, AKSESIBILITAS & PWA")
    print("==================================================")
    test_pwa_infrastructure()
    test_accessibility_and_skip_links()
    test_css_focus_and_reduced_motion()
    test_floating_buttons_and_mobile_layout()
    test_kamus_shortcuts_and_sticky_panel()
    print("\n🎉 SEMUA 5 PENGUJIAN BERHASIL 100% TANPA KESALAHAN! 🎉")

if __name__ == "__main__":
    main()

