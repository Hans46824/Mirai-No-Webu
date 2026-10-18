#!/usr/bin/env python3
"""
Sistem Visual & Transparansi Pattern Universal - Mirai no Webu
=============================================================
Skrip otomatis untuk:
1. Menambahkan & mengunci variabel pattern dan overlay di :root (css/pages/global.css)
2. Menyeragamkan seluruh URL pattern ke variabel master di 11 file css/pages/*.css
3. Menyeragamkan opacity pattern (11% terang, 18% gelap) di seluruh pseudo-element
4. Mengunci background sub-kartu (inner boxes) solid/glass bersih (anti-double-pattern)
5. Mengaktifkan sistem selang-seling section otomatis & pewarisan universal .card
6. Mencatat 7 Sistem Visual Universal di panduan/agent.md dan panduan/PANDUAN-DEVELOPER.md
"""

import os
import re
import glob

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PAGES_DIR = os.path.join(PROJECT_ROOT, 'css', 'pages')
PANDUAN_DIR = os.path.join(PROJECT_ROOT, 'panduan')

print("=== [1] MEMULAI SISTEM VISUAL & TRANSPARANSI PATTERN UNIVERSAL ===")

# -----------------------------------------------------------------------------
# 1. UPDATE css/pages/global.css DENGAN VARIABEL MASTER & SISTEM OTOMATIS
# -----------------------------------------------------------------------------
global_css_path = os.path.join(PAGES_DIR, 'global.css')
with open(global_css_path, 'r', encoding='utf-8') as f:
    global_css = f.read()

# Masukkan variabel master di :root jika belum ada
root_vars = """  /* ==========================================================================
     SISTEM VISUAL & TRANSPARANSI PATTERN UNIVERSAL
     ========================================================================== */
  --pattern-c1w: url("../../images/mirai/background/c1w.jpeg");
  --pattern-c1b: url("../../images/mirai/background/c1b.jpeg");
  --pattern-w1w: url("../../images/mirai/background/w1w.jpeg");
  --pattern-w1b: url("../../images/mirai/background/w1b.jpeg");
  --overlay-card-light: linear-gradient(135deg, rgba(255, 250, 252, 0.89), rgba(255, 245, 249, 0.89));
  --overlay-card-dark: linear-gradient(135deg, rgba(16, 12, 22, 0.82), rgba(22, 16, 30, 0.82));
  --overlay-section-dark: linear-gradient(180deg, rgba(14, 11, 18, 0.82), rgba(14, 11, 18, 0.82));"""

if '--pattern-c1w' not in global_css:
    global_css = global_css.replace(
        '  --pink-border: #f4bfd3;\n}',
        f'  --pink-border: #f4bfd3;\n{root_vars}\n}}'
    )
    print("  -> Variabel master pattern & overlay berhasil ditambahkan ke :root di global.css")

# Update section genap agar menggunakan --overlay-section-dark dan --pattern-w1b
global_css = re.sub(
    r'(main\s*>\s*section:nth-of-type\(even\)[^{]+)\{\s*background-color:\s*#111111\s*!important;\s*color:\s*#f5edf4\s*!important;\s*\}',
    r'''\1{
  background-color: #0e0b12 !important;
  background-image: var(--overlay-section-dark), var(--pattern-w1b) !important;
  background-size: auto, 280px auto !important;
  background-repeat: repeat, repeat !important;
  background-position: top left, top left !important;
  color: #f5edf4 !important;
}''',
    global_css
)

global_css = re.sub(
    r'(\.proker-hero\s*~\s*section:nth-of-type\(even\)[^{]+)\{\s*background-color:\s*#111111\s*!important;\s*color:\s*#f5edf4\s*!important;\s*\}',
    r'''\1{
  background-color: #0e0b12 !important;
  background-image: var(--overlay-section-dark), var(--pattern-w1b) !important;
  background-size: auto, 280px auto !important;
  background-repeat: repeat, repeat !important;
  background-position: top left, top left !important;
  color: #f5edf4 !important;
}''',
    global_css
)

# Update quote card di global.css
quote_white_card_old = """.section-quote-slider.quote-theme-white .quote-card {
  background-color: #ffffff !important;
  background-image: linear-gradient(165deg, rgba(255, 255, 255, 0.88) 0%, rgba(253, 246, 250, 0.88) 100%),
        url("../../images/mirai/background/w1w.jpeg") !important;
  background-size: auto, 260px auto !important;
  background-repeat: repeat, repeat !important;
  background-position: top left, top left !important;
  border: 1.5px solid var(--quote-border, #f4bfd3) !important;
  box-shadow: 0 14px 38px rgba(233, 30, 99, 0.08), 0 2px 10px rgba(0, 0, 0, 0.04) !important;
  position: relative !important;
  overflow: hidden !important;
}"""

quote_white_card_new = """.section-quote-slider.quote-theme-white .quote-card {
  background-color: #ffffff !important;
  background-image: var(--overlay-card-light), var(--pattern-c1w) !important;
  background-size: auto, 260px auto !important;
  background-repeat: repeat, repeat !important;
  background-position: top left, top left !important;
  border: 1.5px solid var(--quote-border, #f4bfd3) !important;
  box-shadow: 0 14px 38px rgba(233, 30, 99, 0.08), 0 2px 10px rgba(0, 0, 0, 0.04) !important;
  position: relative !important;
  overflow: hidden !important;
}"""

if quote_white_card_old in global_css:
    global_css = global_css.replace(quote_white_card_old, quote_white_card_new)

# Matikan double pattern pseudo ::after pada quote card putih
quote_white_after_old = """.section-quote-slider.quote-theme-white .quote-card::after {
  content: "" !important;
  position: absolute !important;
  inset: 0 !important;
  background-image: url("../../images/mirai/background/w1w.jpeg") !important;
  background-size: 260px auto !important;
  background-repeat: repeat !important;
  background-position: top left !important;
  opacity: 0.16 !important;
  mix-blend-mode: multiply !important;
  pointer-events: none !important;
  z-index: 1 !important;
  border-radius: inherit !important;
  display: block !important;
}"""

quote_white_after_new = """.section-quote-slider.quote-theme-white .quote-card::after {
  content: none !important;
  display: none !important;
}"""

if quote_white_after_old in global_css:
    global_css = global_css.replace(quote_white_after_old, quote_white_after_new)

# Update dark quote card di global.css
quote_dark_card_old = """.section-quote-slider.quote-theme-dark .quote-card {
  background: linear-gradient(165deg, #16121d 0%, #0d0a13 100%) !important;
  border: 1.5px solid var(--quote-border, rgba(255, 101, 155, 0.28)) !important;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
}"""

quote_dark_card_new = """.section-quote-slider.quote-theme-dark .quote-card {
  background-color: #120e18 !important;
  background-image: var(--overlay-card-dark), var(--pattern-c1b) !important;
  background-size: auto, 260px auto !important;
  background-repeat: repeat, repeat !important;
  background-position: top left, top left !important;
  border: 1.5px solid var(--quote-border, rgba(255, 101, 155, 0.28)) !important;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
}"""

if quote_dark_card_old in global_css:
    global_css = global_css.replace(quote_dark_card_old, quote_dark_card_new)

# Tambahkan aturan Universal Auto-Inheritance & Anti-Double-Pattern di akhir global.css jika belum ada
universal_block = """/* ==========================================================================
SISTEM SECTION & KARTU UNIVERSAL OTOMATIS (AUTO INHERITANCE)
Standar Desain Universal Mirai no Webu
========================================================================== */
/* [1] Pewarisan Kartu Universal Otomatis */
:where(.card, [class*="-card"]):not([class*="-card-header"]):not([class*="-card-body"]):not([class*="-card-footer"]):not([class*="-card-title"]):not([class*="-card-desc"]):not([class*="-card-sub"]):not([class*="-card-badge"]):not([class*="-card-tag"]):not([class*="-card-icon"]):not([class*="-card-img"]):not([class*="-card-thumb"]):not([class*="-card-btn"]):not([class*="-card-wrap"]):not([class*="-card-grid"]):not([class*="-card-list"]):not([class*="-card-inner"]):not([class*="-card-specs"]) {
  border-radius: 18px;
  position: relative;
  transition: transform 0.28s ease, border-color 0.28s ease, box-shadow 0.28s ease;
}

/* Kartu di Seksi Terang / Putih */
main > section:nth-of-type(odd) :where(.card, [class*="-card"]):not([class*="-card-header"]):not([class*="-card-body"]):not([class*="-card-footer"]):not([class*="-card-title"]):not([class*="-card-desc"]):not([class*="-card-sub"]):not([class*="-card-badge"]):not([class*="-card-tag"]):not([class*="-card-icon"]):not([class*="-card-img"]):not([class*="-card-thumb"]):not([class*="-card-btn"]):not([class*="-card-wrap"]):not([class*="-card-grid"]):not([class*="-card-list"]):not([class*="-card-inner"]):not([class*="-card-specs"]):not(.quote-meaning-card),
.card-light,
.theme-light :where(.card, [class*="-card"]) {
  background-color: #ffffff;
  background-image: var(--overlay-card-light), var(--pattern-c1w);
  background-size: auto, 260px auto;
  background-repeat: repeat, repeat;
  background-position: top left, top left;
  border: 1px solid var(--pink-border, #f4bfd3);
  box-shadow: 0 8px 24px rgba(233, 30, 99, 0.06);
  color: #18151b;
}

/* Kartu di Seksi Gelap / Obsidian */
main > section:nth-of-type(even) :where(.card, [class*="-card"]):not([class*="-card-header"]):not([class*="-card-body"]):not([class*="-card-footer"]):not([class*="-card-title"]):not([class*="-card-desc"]):not([class*="-card-sub"]):not([class*="-card-badge"]):not([class*="-card-tag"]):not([class*="-card-icon"]):not([class*="-card-img"]):not([class*="-card-thumb"]):not([class*="-card-btn"]):not([class*="-card-wrap"]):not([class*="-card-grid"]):not([class*="-card-list"]):not([class*="-card-inner"]):not([class*="-card-specs"]):not(.quote-meaning-card),
.card-dark,
body.theme-dark :where(.card, [class*="-card"]):not([class*="-card-header"]):not([class*="-card-body"]):not([class*="-card-footer"]):not([class*="-card-title"]):not([class*="-card-desc"]):not([class*="-card-sub"]):not([class*="-card-badge"]):not([class*="-card-tag"]):not([class*="-card-icon"]):not([class*="-card-img"]):not([class*="-card-thumb"]):not([class*="-card-btn"]):not([class*="-card-wrap"]):not([class*="-card-grid"]):not([class*="-card-list"]):not([class*="-card-inner"]):not([class*="-card-specs"]):not(.quote-meaning-card) {
  background-color: #16121d;
  background-image: var(--overlay-card-dark), var(--pattern-c1b);
  background-size: auto, 260px auto;
  background-repeat: repeat, repeat;
  background-position: top left, top left;
  border: 1px solid rgba(255, 101, 155, 0.22);
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.4);
  color: #ffffff;
}

/* [2] Aturan Anti-Double-Pattern pada Sub-Kartu (Inner Boxes) */
.quote-card .quote-author-profile,
.quote-card .quote-box,
.quote-card .quote-char-box,
.quote-card .quote-speech-box,
.quote-card .quote-meaning-box,
.quote-card .quote-meaning-card,
.quote-card .quote-literal,
.quote-theme-white .quote-author-profile,
.quote-theme-white .quote-box,
.quote-theme-white .quote-char-box,
.quote-theme-white .quote-speech-box,
.quote-theme-white .quote-meaning-box,
.quote-theme-white .quote-meaning-card,
.quote-theme-white .quote-literal,
.card-light .card-inner-box,
.card-light .sub-panel,
main > section:nth-of-type(odd) .card-inner-box,
main > section:nth-of-type(odd) .sub-panel {
  background: rgba(255, 255, 255, 0.94) !important;
  background-image: none !important;
}

.quote-theme-dark .quote-author-profile,
.quote-theme-dark .quote-box,
.quote-theme-dark .quote-char-box,
.quote-theme-dark .quote-speech-box,
.quote-theme-dark .quote-meaning-box,
.quote-theme-dark .quote-meaning-card,
.quote-theme-dark .quote-literal,
.card-dark .card-inner-box,
.card-dark .sub-panel,
main > section:nth-of-type(even) .card-inner-box,
main > section:nth-of-type(even) .sub-panel,
body.theme-dark .card-inner-box,
body.theme-dark .sub-panel {
  background: rgba(24, 19, 34, 0.90) !important;
  background-image: none !important;
}

/* Cegah Pseudo-Element Pattern pada Seluruh Sub-Kartu / Inner Boxes */
.quote-char-box::before, .quote-char-box::after,
.quote-speech-box::before, .quote-speech-box::after,
.quote-meaning-box::before, .quote-meaning-box::after,
.quote-author-profile::before, .quote-author-profile::after,
.quote-box::before, .quote-box::after,
.quote-meaning-card::before, .quote-meaning-card::after,
.quote-literal::before, .quote-literal::after,
.origin-phase-item::before, .origin-phase-item::after,
.origin-highlight-box::before, .origin-highlight-box::after,
.badge-card-item::before, .badge-card-item::after,
.lb-row-item::before, .lb-row-item::after,
.lb-rule-box::before, .lb-rule-box::after,
.lb-table-row::before, .lb-table-row::after,
.card-inner-box::before, .card-inner-box::after,
.sub-panel::before, .sub-panel::after {
  content: none !important;
  display: none !important;
  background-image: none !important;
}
"""

if 'SISTEM SECTION & KARTU UNIVERSAL OTOMATIS' not in global_css:
    global_css += "\n" + universal_block
    print("  -> Aturan universal section & kartu otomatis berhasil ditambahkan ke global.css")

with open(global_css_path, 'w', encoding='utf-8') as f:
    f.write(global_css)

# -----------------------------------------------------------------------------
# 2. UPDATE rekomendasi-motivasi.css (Quote Card & Inner Boxes)
# -----------------------------------------------------------------------------
rek_path = os.path.join(PAGES_DIR, 'rekomendasi-motivasi.css')
with open(rek_path, 'r', encoding='utf-8') as f:
    rek_css = f.read()

rek_quote_white_old = """.section-quote-slider.quote-theme-white .quote-card {
  background-color: #ffffff !important;
  background-image: linear-gradient(165deg, rgba(255, 255, 255, 0.88) 0%, rgba(253, 246, 250, 0.88) 100%),
        url("../../images/mirai/background/w1w.jpeg") !important;
  background-size: auto, 260px auto !important;
  background-repeat: repeat, repeat !important;
  background-position: top left, top left !important;
  border: 1.5px solid var(--quote-border, #f4bfd3) !important;
  box-shadow: 0 14px 38px rgba(233, 30, 99, 0.08), 0 2px 10px rgba(0, 0, 0, 0.04) !important;
  position: relative !important;
  overflow: hidden !important;
}"""

rek_quote_white_new = """.section-quote-slider.quote-theme-white .quote-card {
  background-color: #ffffff !important;
  background-image: var(--overlay-card-light), var(--pattern-c1w) !important;
  background-size: auto, 260px auto !important;
  background-repeat: repeat, repeat !important;
  background-position: top left, top left !important;
  border: 1.5px solid var(--quote-border, #f4bfd3) !important;
  box-shadow: 0 14px 38px rgba(233, 30, 99, 0.08), 0 2px 10px rgba(0, 0, 0, 0.04) !important;
  position: relative !important;
  overflow: hidden !important;
}"""

if rek_quote_white_old in rek_css:
    rek_css = rek_css.replace(rek_quote_white_old, rek_quote_white_new)

rek_quote_after_old = """.section-quote-slider.quote-theme-white .quote-card::after {
  content: "" !important;
  position: absolute !important;
  inset: 0 !important;
  background-image: url("../../images/mirai/background/w1w.jpeg") !important;
  background-size: 260px auto !important;
  background-repeat: repeat !important;
  background-position: top left !important;
  opacity: 0.16 !important;
  mix-blend-mode: multiply !important;
  pointer-events: none !important;
  z-index: 1 !important;
  border-radius: inherit !important;
  display: block !important;
}"""

rek_quote_after_new = """.section-quote-slider.quote-theme-white .quote-card::after {
  content: none !important;
  display: none !important;
}"""

if rek_quote_after_old in rek_css:
    rek_css = rek_css.replace(rek_quote_after_old, rek_quote_after_new)

rek_quote_dark_old = """.section-quote-slider.quote-theme-dark .quote-card {
  background: linear-gradient(165deg, #16121d 0%, #0d0a13 100%) !important;
  border: 1.5px solid var(--quote-border, rgba(255, 101, 155, 0.28)) !important;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
}"""

rek_quote_dark_new = """.section-quote-slider.quote-theme-dark .quote-card {
  background-color: #120e18 !important;
  background-image: var(--overlay-card-dark), var(--pattern-c1b) !important;
  background-size: auto, 260px auto !important;
  background-repeat: repeat, repeat !important;
  background-position: top left, top left !important;
  border: 1.5px solid var(--quote-border, rgba(255, 101, 155, 0.28)) !important;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
}"""

if rek_quote_dark_old in rek_css:
    rek_css = rek_css.replace(rek_quote_dark_old, rek_quote_dark_new)

# Sub-kotak quote slider di rekomendasi-motivasi.css
rek_css = re.sub(
    r'\.section-quote-slider\.quote-theme-white\s*\.quote-author-profile\s*\{[^}]*\}',
    '''.section-quote-slider.quote-theme-white .quote-author-profile {
  background: rgba(255, 255, 255, 0.94) !important;
  background-image: none !important;
  border: 1px solid #fce4ec !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
  backdrop-filter: blur(8px) !important;
}''',
    rek_css
)

rek_css = re.sub(
    r'\.section-quote-slider\.quote-theme-white\s*\.quote-box\s*\{[^}]*\}',
    '''.section-quote-slider.quote-theme-white .quote-box {
  background: rgba(255, 255, 255, 0.94) !important;
  background-image: none !important;
  border: 1px solid #fce4ec !important;
  border-left: 3.5px solid var(--quote-accent, var(--pink, #e91e63)) !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03) !important;
  backdrop-filter: blur(8px) !important;
}''',
    rek_css
)

rek_css = re.sub(
    r'\.section-quote-slider\.quote-theme-white\s*\.quote-meaning-card\s*\{[^}]*\}',
    '''.section-quote-slider.quote-theme-white .quote-meaning-card {
  background: rgba(255, 255, 255, 0.94) !important;
  background-image: none !important;
  border: 1.5px dashed var(--quote-badge-border, rgba(233, 30, 99, 0.35)) !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03) !important;
  backdrop-filter: blur(8px) !important;
}''',
    rek_css
)

rek_css = re.sub(
    r'\.section-quote-slider\.quote-theme-dark\s*\.quote-author-profile\s*\{[^}]*\}',
    '''.section-quote-slider.quote-theme-dark .quote-author-profile {
  background: rgba(24, 19, 34, 0.90) !important;
  background-image: none !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  backdrop-filter: blur(8px) !important;
}''',
    rek_css
)

rek_css = re.sub(
    r'\.section-quote-slider\.quote-theme-dark\s*\.quote-box\s*\{[^}]*\}',
    '''.section-quote-slider.quote-theme-dark .quote-box {
  background: rgba(24, 19, 34, 0.90) !important;
  background-image: none !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  border-left: 3.5px solid var(--quote-accent, var(--pink, #e91e63)) !important;
  backdrop-filter: blur(8px) !important;
}''',
    rek_css
)

rek_css = re.sub(
    r'\.section-quote-slider\.quote-theme-dark\s*\.quote-meaning-card\s*\{[^}]*\}',
    '''.section-quote-slider.quote-theme-dark .quote-meaning-card {
  background: rgba(24, 19, 34, 0.90) !important;
  background-image: none !important;
  border: 1.5px dashed var(--quote-badge-border, rgba(255, 101, 155, 0.35)) !important;
  backdrop-filter: blur(8px) !important;
}''',
    rek_css
)

with open(rek_path, 'w', encoding='utf-8') as f:
    f.write(rek_css)
print("  -> Kartu kutipan & inner box di rekomendasi-motivasi.css berhasil diseragamkan")

# -----------------------------------------------------------------------------
# 3. PROSES SELURUH FILE CSS DI css/pages/*.css
# -----------------------------------------------------------------------------
print("\n=== [2] MENYERAGAMKAN URL PATTERN & TRANSPARANSI DI SELURUH CSS ===")

all_css_files = sorted(glob.glob(os.path.join(PAGES_DIR, '*.css')))

for cf in all_css_files:
    fname = os.path.basename(cf)
    with open(cf, 'r', encoding='utf-8') as f:
        content = f.read()

    orig_content = content
    replacements_made = 0

    # 1. Ganti semua deklarasi url() di luar :root dengan variabel master
    # Kecuali jika sedang di dalam deklarasi :root { ... }
    lines = content.splitlines(True)
    in_root = False
    new_lines = []

    for line in lines:
        if ':root {' in line:
            in_root = True
        elif in_root and '}' in line:
            in_root = False

        if not in_root:
            if 'url("../../images/mirai/background/c1w.jpeg")' in line:
                line = line.replace('url("../../images/mirai/background/c1w.jpeg")', 'var(--pattern-c1w)')
                replacements_made += 1
            if 'url("../../images/mirai/background/c1b.jpeg")' in line:
                line = line.replace('url("../../images/mirai/background/c1b.jpeg")', 'var(--pattern-c1b)')
                replacements_made += 1
            if 'url("../../images/mirai/background/w1w.jpeg")' in line:
                line = line.replace('url("../../images/mirai/background/w1w.jpeg")', 'var(--pattern-w1w)')
                replacements_made += 1
            if 'url("../../images/mirai/background/w1b.jpeg")' in line:
                line = line.replace('url("../../images/mirai/background/w1b.jpeg")', 'var(--pattern-w1b)')
                replacements_made += 1
        new_lines.append(line)

    content = ''.join(new_lines)

    # 2. Seragamkan Opacity pada block aturan CSS yang memiliki pattern
    # Regex untuk mencari rule blok CSS
    def process_rule(match):
        sel = match.group(1)
        body = match.group(2)
        sel_strip = sel.strip()

        # Cek apakah blok ini mengandung pattern
        has_light = 'var(--pattern-c1w)' in body or 'var(--pattern-w1w)' in body
        has_dark = 'var(--pattern-c1b)' in body or 'var(--pattern-w1b)' in body or 'var(--overlay-section-dark)' in body

        if not (has_light or has_dark):
            # Cek juga apakah blok ini adalah hover dari pattern element
            if ':hover' in sel_strip and ('::after' in sel_strip or '::before' in sel_strip):
                # Periksa apakah ada opacity
                if re.search(r'opacity:\s*0\.(?:045|08|09|10|14);?', body):
                    # Kita sesuaikan hover opacity
                    body = re.sub(r'opacity:\s*0\.(?:045|08|09|10|14)(\s*!important)?;?', r'opacity: 0.24 !important;', body)
            return f"{sel}{{{body}}}"

        is_hover = ':hover' in sel_strip

        if has_light:
            target_opacity = '0.16 !important' if is_hover else '0.11 !important'
            if re.search(r'opacity:\s*[^;]+;', body):
                body = re.sub(r'opacity:\s*[^;]+;', f'opacity: {target_opacity};', body)
            else:
                # Jika pseudo element tanpa opacity, tambahkan opacity
                if '::after' in sel or '::before' in sel:
                    body = body.rstrip() + f"\n  opacity: {target_opacity};\n"

        if has_dark:
            target_opacity = '0.24 !important' if is_hover else '0.18 !important'
            if re.search(r'opacity:\s*[^;]+;', body):
                body = re.sub(r'opacity:\s*[^;]+;', f'opacity: {target_opacity};', body)
            else:
                if '::after' in sel or '::before' in sel:
                    body = body.rstrip() + f"\n  opacity: {target_opacity};\n"

        return f"{sel}{{{body}}}"

    content = re.sub(r'([^{}]+)\{([^{}]+)\}', process_rule, content)

    # Tulis jika ada perubahan
    if content != orig_content:
        with open(cf, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  -> {fname}: Berhasil diseragamkan ({replacements_made} url declarations updated)")
    else:
        print(f"  -> {fname}: Sudah sesuai standar")

# -----------------------------------------------------------------------------
# 4. UPDATE DOKUMENTASI panduan/agent.md & panduan/PANDUAN-DEVELOPER.md
# -----------------------------------------------------------------------------
print("\n=== [3] MEMPERBARUI DOKUMENTASI MASTER (7 SISTEM VISUAL UNIVERSAL) ===")

doc_rule = """## 🎨 7 Sistem Visual & Transparansi Pattern Universal (Master Design Standard)

Seluruh pengembang dan AI asisten **WAJIB mematuhi 7 Aturan Visual Universal** ini untuk menjaga konsistensi, estetika, dan keterbacaan (WCAG AAA) di seluruh halaman Mirai no Webu:

1. **Master Variabel Pattern & Gradien Terpusat di `:root` (`css/pages/global.css`)**:
   - `--pattern-c1w: url("../../images/mirai/background/c1w.jpeg");` (Kumo/Awan Terang)
   - `--pattern-c1b: url("../../images/mirai/background/c1b.jpeg");` (Kumo/Awan Gelap)
   - `--pattern-w1w: url("../../images/mirai/background/w1w.jpeg");` (Wagara/Ombak Terang)
   - `--pattern-w1b: url("../../images/mirai/background/w1b.jpeg");` (Wagara/Ombak Gelap)
   - `--overlay-card-light: linear-gradient(135deg, rgba(255, 250, 252, 0.89), rgba(255, 245, 249, 0.89));` (Kunci transparansi pattern terang tepat di 11%)
   - `--overlay-card-dark: linear-gradient(135deg, rgba(16, 12, 22, 0.82), rgba(22, 16, 30, 0.82));` (Kunci transparansi pattern gelap tepat di 18%)
   - `--overlay-section-dark: linear-gradient(180deg, rgba(14, 11, 18, 0.82), rgba(14, 11, 18, 0.82));` (Kunci transparansi background section gelap tepat di 18%)

2. **Kunci Transparansi Universal (11% Terang, 18% Gelap)**:
   - Pola Terang (`c1w` / `w1w`): Wajib tepat **11%** (`opacity: 0.11 !important` atau via `--overlay-card-light` dengan `alpha: 0.89`).
   - Pola Gelap (`c1b` / `w1b`): Wajib tepat **18%** (`opacity: 0.18 !important` atau via `--overlay-card-dark` dengan `alpha: 0.82`).
   - Dilarang keras menggunakan transparansi acak/belang-belang (seperti 0.045 atau 0.16).

3. **Seksi Selang-Seling Otomatis (Alternating Sections)**:
   - Semua `<section>` konten setelah Hero otomatis bergantian:
     - Seksi Ganjil (`nth-of-type(odd)`): Putih Bersih (`#ffffff`) dengan teks kontras tinggi (`#18151b` / `#554e57`).
     - Seksi Genap (`nth-of-type(even)`): Hitam Obsidian (`#0e0b12`) berlapis `--overlay-section-dark, var(--pattern-w1b)` dengan teks kontras terang (`#ffffff` / `#d5ccd3`).

4. **Pewarisan Kartu Universal Otomatis (Auto-Inheritance)**:
   - Setiap elemen kartu standar (`.card`, `[class*="-card"]`, di luar elemen inner/title/desc) otomatis mewarisi radius border (18px), border beraksen pink (`#f4bfd3` untuk kartu terang, `rgba(255, 101, 155, 0.22)` untuk kartu gelap), dan pattern universal yang sesuai dengan warna latarnya.

5. **Aturan Anti-Double-Pattern pada Sub-Kartu (Inner Boxes)**:
   - Semua kotak/panel anak di dalam kartu utama (seperti `.quote-char-box`, `.quote-speech-box`, `.quote-meaning-box`, profile box, badge box, dll.) WAJIB menggunakan latar solid/glass (`background: rgba(255, 255, 255, 0.94) !important;` di kartu terang, `background: rgba(24, 19, 34, 0.90) !important;` di kartu gelap) TANPA pattern gambar (`background-image: none !important`), memastikan teks 100% bersih, jernih, dan tidak bertabrakan dengan background.

6. **Harmoni Motif Berbasis Karakter Halaman**:
   - Halaman Interaktif & Dinamis (Beranda, Kamus, Rekomendasi, Lomba, Toko): Menggunakan motif Kumo Awan (`--pattern-c1w` / `--pattern-c1b`).
   - Halaman Kurikulum & Prestasi (Kelas, Kegiatan, Peringkat, Tentang): Menggunakan motif Ombak Seigaiha (`--pattern-w1w` / `--pattern-w1b`).

7. **Standar Kontras & Aksesibilitas WCAG AAA**:
   - Di seksi terang: Heading berwarna `#18151b`, paragraf `#554e57`, aksen pink `#e91e63`.
   - Di seksi gelap: Heading berwarna `#ffffff`, paragraf `#d5ccd3`, aksen pink `#ff4f91` atau `#ff659b`.
"""

# Update panduan/agent.md
agent_path = os.path.join(PANDUAN_DIR, 'agent.md')
with open(agent_path, 'r', encoding='utf-8') as f:
    agent_text = f.read()

if '7 Sistem Visual & Transparansi Pattern Universal' not in agent_text:
    target_anchor = '## 1. Protokol Eksekusi Cepat (Fast-Execution Protocol)'
    agent_text = agent_text.replace(target_anchor, doc_rule + "\n---\n\n" + target_anchor)
    with open(agent_path, 'w', encoding='utf-8') as f:
        f.write(agent_text)
    print("  -> panduan/agent.md berhasil diperbarui dengan 7 Aturan Visual Universal")

# Update panduan/PANDUAN-DEVELOPER.md
dev_path = os.path.join(PANDUAN_DIR, 'PANDUAN-DEVELOPER.md')
with open(dev_path, 'r', encoding='utf-8') as f:
    dev_text = f.read()

if '7 Sistem Visual & Transparansi Pattern Universal' not in dev_text:
    target_anchor_dev = '## 1. Pengenalan Arsitektur Web (Zero-Framework Architecture)'
    dev_text = dev_text.replace(target_anchor_dev, doc_rule + "\n---\n\n" + target_anchor_dev)
    with open(dev_path, 'w', encoding='utf-8') as f:
        f.write(dev_text)
    print("  -> panduan/PANDUAN-DEVELOPER.md berhasil diperbarui dengan 7 Aturan Visual Universal")

# -----------------------------------------------------------------------------
# 5. INTEGRITY CHECK (Braces & Syntax Balance)
# -----------------------------------------------------------------------------
print("\n=== [4] INTEGRITY CHECK (PENGECEKAN SINTAKS & TANDA KURUNG) ===")
all_passed = True
for cf in all_css_files:
    fname = os.path.basename(cf)
    with open(cf, 'r', encoding='utf-8') as f:
        c = f.read()
    open_b = c.count('{')
    close_b = c.count('}')
    if open_b == close_b:
        print(f"  [OK] {fname}: {open_b} kurung kurawal cocok sempurna")
    else:
        print(f"  [ERROR] {fname}: {open_b} open vs {close_b} close!")
        all_passed = False

if all_passed:
    print("\n✅ SELURUH PENGECEKAN BERHASIL 100%! SISTEM VISUAL UNIVERSAL RESMI TERKUNCI.")
else:
    print("\n⚠️ PERINGATAN: ADA KETIDAKSESUAIAN BRACES PADA CSS.")
