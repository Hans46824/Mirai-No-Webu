#!/usr/bin/env python3
"""
fix_missing_card_patterns.py
Memperbaiki 3 kartu yang belum memiliki background pattern sesuai laporan user & screenshot:
1. .about-name-card (Makna Nama Mirai no Hana Nihongo Kurabu di tentang/index.html):
   - Dipindahkan dari seksi putih (w1w multiply) ke seksi gelap (w1b screen, opacity 0.045)
   - Styling diselaraskan ke tema obsidian gelap dengan aksen pink
2. .flag-mockup-frame (Bendera Resmi Nihongo Kurabu di tentang/index.html):
   - Diberikan pattern w1w (opacity 0.015, multiply) di atas frame gradien bendera
   - Mode gelap w1b (opacity 0.045, screen)
3. .quote-card (Kutipan Inspiratif / Slider Motivasi di index.html & universal):
   - Diberikan pattern c1b (opacity 0.045, screen) untuk quote-theme-dark dan .quote-card
   - High-specificity rule untuk halaman Beranda (c1b) dan Tentang (w1b)
"""

import sys

def patch_tentang_css():
    path = "css/pages/tentang.css"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update (A-1) KARTU GELAP: Tambahkan .about-name-card dan .quote-card::after
    old_a1 = ".about-intro-card, .history-origin-card, .slogan-hero-card, .slogan-card, .achievement-card, .accessory-card, .accessory-banner-card, .timeline-content, .prestasi-stat-box, .podium-card, .lb-category-desc-card, .lb-table-card, .lb-system-info-card, .quote-card"
    new_a1 = ".about-intro-card, .about-name-card, .history-origin-card, .slogan-hero-card, .slogan-card, .achievement-card, .accessory-card, .accessory-banner-card, .timeline-content, .prestasi-stat-box, .podium-card, .lb-category-desc-card, .lb-table-card, .lb-system-info-card, .quote-card"

    old_a1_after = ".about-intro-card::after, .history-origin-card::after, .slogan-hero-card::after, .slogan-card::after, .achievement-card::after, .accessory-card::after, .accessory-banner-card::after, .timeline-content::after, .prestasi-stat-box::after, .podium-card::after, .lb-category-desc-card::after, .lb-table-card::after, .lb-system-info-card::after"
    new_a1_after = ".about-intro-card::after, .about-name-card::after, .history-origin-card::after, .slogan-hero-card::after, .slogan-card::after, .achievement-card::after, .accessory-card::after, .accessory-banner-card::after, .timeline-content::after, .prestasi-stat-box::after, .podium-card::after, .lb-category-desc-card::after, .lb-table-card::after, .lb-system-info-card::after, .quote-card::after"

    old_a1_hover = ".about-intro-card:hover::after, .history-origin-card:hover::after, .slogan-hero-card:hover::after, .slogan-card:hover::after, .achievement-card:hover::after, .accessory-card:hover::after, .accessory-banner-card:hover::after, .timeline-node:hover .timeline-content::after, .prestasi-stat-box:hover::after, .podium-card:hover::after, .lb-category-desc-card:hover::after, .lb-table-card:hover::after, .lb-system-info-card:hover::after, .quote-card:hover::after"
    new_a1_hover = ".about-intro-card:hover::after, .about-name-card:hover::after, .history-origin-card:hover::after, .slogan-hero-card:hover::after, .slogan-card:hover::after, .achievement-card:hover::after, .accessory-card:hover::after, .accessory-banner-card:hover::after, .timeline-node:hover .timeline-content::after, .prestasi-stat-box:hover::after, .podium-card:hover::after, .lb-category-desc-card:hover::after, .lb-table-card:hover::after, .lb-system-info-card:hover::after, .quote-card:hover::after"

    old_a1_child = ".about-intro-card > *, .history-origin-card > *, .slogan-hero-card > *, .slogan-card > *, .achievement-card > *, .accessory-card > *, .accessory-banner-card > *, .timeline-content > *, .prestasi-stat-box > *, .podium-card > *, .lb-category-desc-card > *, .lb-table-card > *, .lb-system-info-card > *, .quote-card > *"
    new_a1_child = ".about-intro-card > *, .about-name-card > *, .history-origin-card > *, .slogan-hero-card > *, .slogan-card > *, .achievement-card > *, .accessory-card > *, .accessory-banner-card > *, .timeline-content > *, .prestasi-stat-box > *, .podium-card > *, .lb-category-desc-card > *, .lb-table-card > *, .lb-system-info-card > *, .quote-card > *"

    if old_a1 in content:
        content = content.replace(old_a1, new_a1, 1)
    if old_a1_after in content:
        content = content.replace(old_a1_after, new_a1_after, 1)
    if old_a1_hover in content:
        content = content.replace(old_a1_hover, new_a1_hover, 1)
    if old_a1_child in content:
        content = content.replace(old_a1_child, new_a1_child, 1)

    # 2. Hapus .about-name-card dari (B) BAGIAN PUTIH
    old_b_comment = "/* (B) BAGIAN PUTIH: .flag-feature-card, .about-name-card,"
    new_b_comment = "/* (B) BAGIAN PUTIH: .flag-feature-card,"
    if old_b_comment in content:
        content = content.replace(old_b_comment, new_b_comment, 1)

    old_b_sel = ".flag-feature-card, .about-name-card, .logo-meaning-badge-col"
    new_b_sel = ".flag-feature-card, .logo-meaning-badge-col"
    if old_b_sel in content:
        content = content.replace(old_b_sel, new_b_sel, 1)

    old_b_after = ".flag-feature-card::after, .about-name-card::after, .logo-meaning-badge-col::after"
    new_b_after = ".flag-feature-card::after, .logo-meaning-badge-col::after"
    if old_b_after in content:
        content = content.replace(old_b_after, new_b_after, 1)

    old_b_hover = ".flag-feature-card:hover::after, .about-name-card:hover::after, .logo-meaning-badge-col:hover::after"
    new_b_hover = ".flag-feature-card:hover::after, .logo-meaning-badge-col:hover::after"
    if old_b_hover in content:
        content = content.replace(old_b_hover, new_b_hover, 1)

    old_b_child = ".flag-feature-card > *, .about-name-card > *, .logo-meaning-badge-col > *"
    new_b_child = ".flag-feature-card > *, .logo-meaning-badge-col > *"
    if old_b_child in content:
        content = content.replace(old_b_child, new_b_child, 1)

    # 3. Update styling .about-name-card ke dark obsidian & kontras tinggi
    old_name_card_block = """.about-name-card {
  background: #ffffff !important;
  border: 1.5px solid #ffccd9 !important;
  border-left: 5px solid var(--pink, #e91e63) !important;
  box-shadow: 0 8px 24px rgba(72, 32, 52, 0.05) !important;
  padding: 34px 30px !important;
  display: flex !important;
  flex-direction: column !important;
}

.about-name-card:hover {
  transform: translateY(-4px) !important;
  border-color: var(--pink, #e91e63) !important;
  box-shadow: 0 16px 34px rgba(233, 30, 99, 0.14) !important;
}

.about-name-badge {
  color: var(--pink, #e91e63) !important;
  font-size: 11px !important;
  font-weight: 800 !important;
  letter-spacing: 1.6px !important;
  margin-bottom: 12px !important;
  text-transform: uppercase !important;
  display: inline-block !important;
}

.about-name-card h3 {
  margin: 0 0 14px !important;
  font-size: 21px !important;
  line-height: 1.4 !important;
  color: #1a151e !important;
  font-weight: 800 !important;
}

.about-name-card p {
  color: #554857 !important;
  font-size: 14.5px !important;
  line-height: 1.75 !important;
  margin: 0 !important;
}"""

    new_name_card_block = """.about-name-card {
  background: linear-gradient(165deg, #1c1523 0%, #130f18 100%) !important;
  border: 1.5px solid rgba(255, 101, 155, 0.28) !important;
  border-left: 5px solid var(--pink, #e91e63) !important;
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.45) !important;
  padding: 34px 30px !important;
  display: flex !important;
  flex-direction: column !important;
}

.about-name-card:hover {
  transform: translateY(-4px) !important;
  border-color: var(--pink, #e91e63) !important;
  box-shadow: 0 16px 36px rgba(233, 30, 99, 0.22) !important;
}

.about-name-badge {
  color: var(--pink, #e91e63) !important;
  font-size: 11px !important;
  font-weight: 800 !important;
  letter-spacing: 1.6px !important;
  margin-bottom: 12px !important;
  text-transform: uppercase !important;
  display: inline-block !important;
}

.about-name-card h3 {
  margin: 0 0 14px !important;
  font-size: 21px !important;
  line-height: 1.4 !important;
  color: #ffffff !important;
  font-weight: 800 !important;
}

.about-name-card p {
  color: #d5ccd3 !important;
  font-size: 14.5px !important;
  line-height: 1.75 !important;
  margin: 0 !important;
}"""

    if old_name_card_block in content:
        content = content.replace(old_name_card_block, new_name_card_block, 1)

    # 4. Tambahkan pattern w1w pada .flag-mockup-frame
    flag_pattern_css = """/* Pattern Wagara Lembut Mockup Bendera */
.flag-mockup-frame {
  position: relative !important;
  overflow: hidden !important;
}

.flag-mockup-frame::after {
  content: "" !important;
  position: absolute !important;
  inset: 0 !important;
  background-image: url("../../images/mirai/background/w1w.jpeg") !important;
  background-size: 200px auto !important;
  background-repeat: repeat !important;
  background-position: center top !important;
  opacity: 0.015 !important;
  mix-blend-mode: multiply !important;
  pointer-events: none !important;
  z-index: 1 !important;
  border-radius: inherit !important;
  display: block !important;
  transition: opacity 0.3s ease, transform 0.3s ease !important;
}

.flag-feature-card:hover .flag-mockup-frame::after,
.flag-mockup-frame:hover::after {
  opacity: 0.03 !important;
  transform: scale(1.02) !important;
}

.flag-mockup-frame > * {
  position: relative !important;
  z-index: 2 !important;
}

body.theme-dark .flag-mockup-frame::after,
body.dark-mode .flag-mockup-frame::after {
  background-image: url("../../images/mirai/background/w1b.jpeg") !important;
  opacity: 0.045 !important;
  mix-blend-mode: screen !important;
}

body.theme-dark .flag-mockup-frame:hover::after,
body.dark-mode .flag-mockup-frame:hover::after {
  opacity: 0.07 !important;
}

"""
    if "/* Pattern Wagara Lembut Mockup Bendera */" not in content:
        content = content.replace("/* (B) BAGIAN PUTIH: .flag-feature-card", flag_pattern_css + "/* (B) BAGIAN PUTIH: .flag-feature-card", 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ [tentang.css] Berhasil diperbarui (.about-name-card w1b, .flag-mockup-frame w1w, .quote-card::after)")


def patch_global_css():
    path = "css/pages/global.css"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    marker = ".section-quote-slider.quote-theme-white .quote-card > *"
    dark_quote_pattern_css = """/* Proteksi & Tampilan Pattern Quote Card Seksi Gelap (Beranda & Universal) */
.section-quote-slider.quote-theme-dark .quote-card,
.quote-card:not(.quote-theme-white) {
  position: relative !important;
  overflow: hidden !important;
}

.section-quote-slider.quote-theme-dark .quote-card::after,
.quote-card:not(.quote-theme-white)::after {
  content: "" !important;
  position: absolute !important;
  inset: 0 !important;
  background-image: var(--pattern-c1b, url("../../images/mirai/background/c1b.jpeg")) !important;
  background-size: 200px auto !important;
  background-repeat: repeat !important;
  background-position: center top !important;
  opacity: 0.045 !important;
  mix-blend-mode: screen !important;
  pointer-events: none !important;
  z-index: 1 !important;
  border-radius: inherit !important;
  display: block !important;
  transition: opacity 0.3s ease, transform 0.3s ease !important;
}

.section-quote-slider.quote-theme-dark .quote-card:hover::after,
.quote-card:not(.quote-theme-white):hover::after {
  opacity: 0.07 !important;
  transform: scale(1.02) !important;
}

.section-quote-slider.quote-theme-dark .quote-card > *,
.quote-card:not(.quote-theme-white) > * {
  position: relative !important;
  z-index: 2 !important;
}

"""
    if "/* Proteksi & Tampilan Pattern Quote Card Seksi Gelap" not in content:
        # Sisipkan setelah blok quote-theme-white
        pos = content.find(marker)
        if pos != -1:
            end_pos = content.find("}", pos) + 1
            content = content[:end_pos] + "\n\n" + dark_quote_pattern_css + content[end_pos:]
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print("✓ [global.css] Berhasil menambahkan pattern dark quote card (.section-quote-slider.quote-theme-dark .quote-card::after)")
        else:
            print("! [global.css] Marker quote-theme-white tidak ditemukan")
    else:
        print("- [global.css] Sudah memiliki pattern dark quote card")


def patch_beranda_css():
    path = "css/pages/beranda.css"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    beranda_quote_css = """/* Pattern Kumo Gelap untuk Slider Kutipan Beranda */
.page-beranda .section-quote-slider.quote-theme-dark .quote-card::after,
.page-beranda .quote-card::after {
  content: "" !important;
  position: absolute !important;
  inset: 0 !important;
  background-image: url("../../images/mirai/background/c1b.jpeg") !important;
  background-size: 200px auto !important;
  background-repeat: repeat !important;
  background-position: center top !important;
  opacity: 0.045 !important;
  mix-blend-mode: screen !important;
  pointer-events: none !important;
  z-index: 1 !important;
  border-radius: inherit !important;
  display: block !important;
  transition: opacity 0.3s ease, transform 0.3s ease !important;
}

.page-beranda .section-quote-slider.quote-theme-dark .quote-card:hover::after,
.page-beranda .quote-card:hover::after {
  opacity: 0.07 !important;
  transform: scale(1.02) !important;
}

.page-beranda .quote-card > * {
  position: relative !important;
  z-index: 2 !important;
}
"""
    if "/* Pattern Kumo Gelap untuk Slider Kutipan Beranda */" not in content:
        content = content + "\n" + beranda_quote_css
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("✓ [beranda.css] Berhasil menambahkan pattern Kumo Gelap (c1b) untuk quote-card di Beranda")
    else:
        print("- [beranda.css] Sudah memiliki pattern quote card")


def patch_rekomendasi_css():
    path = "css/pages/rekomendasi-motivasi.css"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    marker = ".section-quote-slider.quote-theme-white .quote-card > *"
    dark_quote_pattern_css = """/* Pattern Gelap untuk Slider Kutipan */
.section-quote-slider.quote-theme-dark .quote-card {
  position: relative !important;
  overflow: hidden !important;
}

.section-quote-slider.quote-theme-dark .quote-card::after {
  content: "" !important;
  position: absolute !important;
  inset: 0 !important;
  background-image: url("../../images/mirai/background/c1b.jpeg") !important;
  background-size: 200px auto !important;
  background-repeat: repeat !important;
  background-position: center top !important;
  opacity: 0.045 !important;
  mix-blend-mode: screen !important;
  pointer-events: none !important;
  z-index: 1 !important;
  border-radius: inherit !important;
  display: block !important;
  transition: opacity 0.3s ease, transform 0.3s ease !important;
}

.section-quote-slider.quote-theme-dark .quote-card:hover::after {
  opacity: 0.07 !important;
  transform: scale(1.02) !important;
}

.section-quote-slider.quote-theme-dark .quote-card > * {
  position: relative !important;
  z-index: 2 !important;
}

"""
    if "/* Pattern Gelap untuk Slider Kutipan */" not in content:
        pos = content.find(marker)
        if pos != -1:
            end_pos = content.find("}", pos) + 1
            content = content[:end_pos] + "\n\n" + dark_quote_pattern_css + content[end_pos:]
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print("✓ [rekomendasi-motivasi.css] Berhasil menambahkan pattern dark quote card")
        else:
            print("! [rekomendasi-motivasi.css] Marker quote-theme-white tidak ditemukan")
    else:
        print("- [rekomendasi-motivasi.css] Sudah memiliki pattern dark quote card")


if __name__ == "__main__":
    patch_tentang_css()
    patch_global_css()
    patch_beranda_css()
    patch_rekomendasi_css()
    print("\nSemua perbaikan pattern kartu selesai dikerjakan.")

