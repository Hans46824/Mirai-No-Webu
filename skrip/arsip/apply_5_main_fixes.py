#!/usr/bin/env python3
"""
Skrip Otomatis: 5 Perbaikan Utama Mirai no Webu
1. Pulihkan Desain Kartu & Badge (Hapus selector agresif di global.css, bersihkan lomba.css, hapus skrip/skrip/)
2. Buat Pattern Jadi Landscape Utuh (Rotasi c1b/c1w jika portrait, no-repeat cover, lembutkan dark pattern 0.08 & hover 0.12)
3. Kamus Kana: Hapus tombol suara di dalam kana-card, kembalikan quick-jump Urutan Goresan
4. Perbaiki Fitur Translate: Real-time 300ms debounce + Google Translate API + kamus lokal
5. Floating Mobile 12-Key Keitai Keyboard dengan multi-tap cycle & popup 5 vokal
"""

import os
import re
import shutil
from PIL import Image

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def log(msg):
    print(f"[FIX] {msg}")

# ==============================================================================
# 1. BERSIHKAN SELECTOR UNIVERSAL AGRESIF DI global.css & lomba.css
# ==============================================================================
def fix_task_1():
    log("=== [1] Membersihkan Selector Agresif di global.css & lomba.css ===")
    
    # 1.a Hapus folder kosong skrip/skrip/ jika ada
    skrip_skrip = os.path.join(BASE_DIR, "skrip", "skrip")
    if os.path.exists(skrip_skrip):
        shutil.rmtree(skrip_skrip, ignore_errors=True)
        log("Folder kosong skrip/skrip/ berhasil dihapus.")

    # 1.b Bersihkan bagian bawah css/pages/global.css jika ada blok agresif wildcard
    global_css_path = os.path.join(BASE_DIR, "css", "pages", "global.css")
    with open(global_css_path, "r", encoding="utf-8") as f:
        content = f.read()

    split_marker = "/* ==========================================================================\nSISTEM SECTION & KARTU UNIVERSAL OTOMATIS"
    if split_marker in content:
        content = content.split(split_marker)[0].rstrip() + "\n"
        with open(global_css_path, "w", encoding="utf-8") as f:
            f.write(content)
        log("Blok wildcard aggressive universal cards di global.css berhasil dihilangkan.")

    # 1.c Pastikan di css/pages/lomba.css header & badge tidak dibingkai border aneh
    lomba_css_path = os.path.join(BASE_DIR, "css", "pages", "lomba.css")
    with open(lomba_css_path, "r", encoding="utf-8") as f:
        lomba_css = f.read()

    protection_rule = """
/* Proteksi Header Kompak & Sub-Label Poin Lomba (Bebas Kotak Border Aneh) */
.lomba-card-top,
.lomba-card-head,
.lomba-card-header-compact {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}

.badge-card-item {
  box-shadow: none !important;
}

.badge-card-item .badge-card-label {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  padding: 0 !important;
}
"""
    if "/* Proteksi Header Kompak & Sub-Label Poin Lomba" not in lomba_css:
        lomba_css += "\n" + protection_rule
        with open(lomba_css_path, "w", encoding="utf-8") as f:
            f.write(lomba_css)
        log("Proteksi header & badge-card-label di lomba.css berhasil dipasang.")

# ==============================================================================
# 2. PATTERN LANDSCAPE, COVER/NO-REPEAT & LEMBUTKAN TRANSPARANSI GELAP (0.08 / 0.12)
# ==============================================================================
def fix_task_2():
    log("=== [2] Mengubah Pattern ke Landscape, Cover, & Lembutkan Opacity Gelap ===")
    
    bg_dir = os.path.join(BASE_DIR, "images", "mirai", "background")
    for name in ["c1b.jpeg", "c1w.jpeg"]:
        img_path = os.path.join(bg_dir, name)
        orig_path = os.path.join(bg_dir, name.replace(".jpeg", "_orig.jpeg"))
        if os.path.exists(img_path):
            with Image.open(img_path) as im:
                w, h = im.size
                if h > w:
                    log(f"Dimensi {name} adalah Portrait ({w}x{h}). Melakukan rotasi 90 derajat ke Landscape...")
                    if not os.path.exists(orig_path):
                        shutil.copy2(img_path, orig_path)
                        log(f"Backup {name} disimpan ke {os.path.basename(orig_path)}.")
                    rotated = im.transpose(Image.Transpose.ROTATE_270)
                    rotated.save(img_path, quality=95)
                    log(f"{name} sekarang Landscape: {rotated.size[0]}x{rotated.size[1]}.")
                else:
                    log(f"{name} sudah Landscape ({w}x{h}).")

    # Update :root di global.css untuk menyertakan master pattern & overlay variables
    global_css_path = os.path.join(BASE_DIR, "css", "pages", "global.css")
    with open(global_css_path, "r", encoding="utf-8") as f:
        g_css = f.read()

    root_vars = """  /* Variabel Master Sistem Visual Pattern & Transparansi Universal */
  --pattern-c1w: url("../../images/mirai/background/c1w.jpeg");
  --pattern-c1b: url("../../images/mirai/background/c1b.jpeg");
  --pattern-w1w: url("../../images/mirai/background/w1w.jpeg");
  --pattern-w1b: url("../../images/mirai/background/w1b.jpeg");
  --overlay-card-light: linear-gradient(135deg, rgba(255, 250, 252, 0.89), rgba(255, 245, 249, 0.89));
  --overlay-card-dark: linear-gradient(155deg, rgba(18, 14, 26, 0.92), rgba(11, 9, 16, 0.94));
  --overlay-section-dark: linear-gradient(180deg, rgba(14, 11, 18, 0.90), rgba(14, 11, 18, 0.92));
"""
    if "--pattern-c1b:" not in g_css:
        g_css = g_css.replace(":root {", ":root {\n" + root_vars)
        with open(global_css_path, "w", encoding="utf-8") as f:
            f.write(g_css)
        log("Variabel pattern & overlay berhasil ditambahkan ke :root di global.css.")

    # Update seluruh css/pages/*.css secara aman (Line-by-Line agar tidak merusak kurung kurawal)
    css_dir = os.path.join(BASE_DIR, "css", "pages")
    for fname in sorted(os.listdir(css_dir)):
        if not fname.endswith(".css"):
            continue
        fpath = os.path.join(css_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        orig_open = sum(l.count("{") for l in lines)
        orig_close = sum(l.count("}") for l in lines)

        new_lines = []
        in_dark_pattern = False

        for i, l in enumerate(lines):
            new_l = l

            # Cek apakah blok saat ini adalah pattern gelap
            if any(x in l for x in ["c1b.jpeg", "w1b.jpeg", "var(--pattern-c1b)", "var(--pattern-w1b)"]):
                in_dark_pattern = True
            if "}" in l:
                in_dark_pattern = False

            # Ganti opacity kartu gelap (0.045 -> 0.08)
            if in_dark_pattern and "opacity: 0.045" in new_l:
                new_l = re.sub(r"opacity:\s*0\.045(\s*!important)?;", "opacity: 0.08 !important;", new_l)

            # Ganti hover opacity kartu gelap (0.08 -> 0.12)
            if "opacity:" in new_l and "0.08" in new_l:
                # Periksa apakah baris ini atau sebelumnya adalah selektor :hover
                is_hover = any(":hover" in lines[j] for j in range(max(0, i - 4), i + 1))
                if is_hover:
                    new_l = re.sub(r"opacity:\s*0\.08(\s*!important)?;", "opacity: 0.12 !important;", new_l)

            # Geometri pattern: no-repeat, cover, center
            if "background-size: 260px auto" in new_l:
                new_l = re.sub(r"background-size:\s*260px\s+auto(\s*!important)?;", "background-size: cover !important;", new_l)
            if "background-repeat: repeat" in new_l:
                new_l = re.sub(r"background-repeat:\s*repeat(\s*!important)?;", "background-repeat: no-repeat !important;", new_l)
            if "background-position: top left" in new_l and ("!important" in new_l or in_dark_pattern):
                new_l = re.sub(r"background-position:\s*top\s+left(\s*!important)?;", "background-position: center center !important;", new_l)

            # Netralkan gradasi pink pada kartu putih agar murni putih
            if "background: linear-gradient(165deg, #ffffff 0%, #fffbfc 100%) !important;" in new_l:
                new_l = new_l.replace("background: linear-gradient(165deg, #ffffff 0%, #fffbfc 100%) !important;", "background: #ffffff !important;")
            if "background: linear-gradient(135deg, #ffffff 0%, #fff0f5 100%);" in new_l:
                new_l = new_l.replace("background: linear-gradient(135deg, #ffffff 0%, #fff0f5 100%);", "background: #ffffff;")
            if "background: linear-gradient(135deg, #fff5f9 0%, #fffbfd 100%);" in new_l:
                new_l = new_l.replace("background: linear-gradient(135deg, #fff5f9 0%, #fffbfd 100%);", "background: #ffffff;")

            new_lines.append(new_l)

        # Verifikasi integritas tanda kurung kurawal
        res_open = sum(l.count("{") for l in new_lines)
        res_close = sum(l.count("}") for l in new_lines)
        assert orig_open == res_open and orig_close == res_close, f"Brace mismatch in {fname}!"

        with open(fpath, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        log(f"Pattern cover & opacity lembut (0.08/0.12) berhasil diterapkan pada {fname}.")

# ==============================================================================
# 3. KAMUS KANA: HAPUS AUDIO DI KANA-CARD & KEMBALIKAN QUICK-STROKE-BTN
# ==============================================================================
def fix_task_3():
    log("=== [3] Merapikan Kamus Kana & Quick-Stroke Button ===")

    # 3.a Hapus speaker 🔊 dari dalam kana-card di js/kana.js
    kana_js = os.path.join(BASE_DIR, "js", "kana.js")
    with open(kana_js, "r", encoding="utf-8") as f:
        k_code = f.read()

    old_snippet = 'button.innerHTML = `<strong>${character}</strong><span>${item.reading}</span><span class="kana-card-speaker" title="Dengarkan suara ${character}">🔊</span>`;'
    new_snippet = 'button.innerHTML = `<strong>${character}</strong><span>${item.reading}</span>`;'
    if old_snippet in k_code:
        k_code = k_code.replace(old_snippet, new_snippet)
        with open(kana_js, "w", encoding="utf-8") as f:
            f.write(k_code)
        log("Speaker 🔊 dihapus dari kotak .kana-card di js/kana.js.")

    # 3.b Hapus speaker 🔊 dari dalam kana-card di js/kanji.js
    kanji_js = os.path.join(BASE_DIR, "js", "kanji.js")
    with open(kanji_js, "r", encoding="utf-8") as f:
        kj_code = f.read()

    if old_snippet in kj_code:
        kj_code = kj_code.replace(old_snippet, new_snippet)
        with open(kanji_js, "w", encoding="utf-8") as f:
            f.write(kj_code)
        log("Speaker 🔊 dihapus dari kotak .kana-card di js/kanji.js.")

    # 3.c Hapus quick-translator-pill dan pasang quick-stroke-btn di kamus/index.html
    kamus_html = os.path.join(BASE_DIR, "kamus", "index.html")
    with open(kamus_html, "r", encoding="utf-8") as f:
        html = f.read()

    # Hapus quick-translator-pill
    html = re.sub(r'<a class="quick-translator-pill"[^>]*>.*?</a>', '', html)

    # Pastikan quickStrokeBtn ada di samping to-top button
    stroke_btn_markup = '<button id="quickStrokeBtn" class="quick-stroke-btn" type="button" aria-label="Geser ke Urutan Goresan" title="Geser ke Urutan Goresan"><span class="quick-stroke-icon">✍️</span><span class="quick-stroke-text">Urutan Goresan</span><span class="quick-stroke-arrow">↓</span></button>'
    if 'id="quickStrokeBtn"' not in html:
        html = html.replace('<button class="to-top"', stroke_btn_markup + '\n<button class="to-top"')
        log("quickStrokeBtn ditambahkan ke DOM kamus/index.html.")

    with open(kamus_html, "w", encoding="utf-8") as f:
        f.write(html)

# ==============================================================================
# 4 & 5. TRANSLATOR REALTIME & FLOATING MOBILE 12-KEY KEITAI KEYBOARD
# ==============================================================================
def fix_task_4_and_5():
    log("=== [4 & 5] Membangun Floating 12-Key Keitai Keyboard & Realtime Translator ===")

    # 4.a Update Markup Keyboard di kamus/index.html jika belum ada Keitai 12-Key
    kamus_html = os.path.join(BASE_DIR, "kamus", "index.html")
    with open(kamus_html, "r", encoding="utf-8") as f:
        html = f.read()

    new_keyboard_markup = """        <!-- PANEL VIRTUAL KEYBOARD JEPANG: FLOATING MOBILE 12-KEY KEITAI KEYBOARD -->
        <div class="virtual-keyboard-panel is-collapsed" id="virtualKeyboardPanel" role="region" aria-label="Keyboard Virtual Jepang Keitai 12-Key">
            <div class="kb-floating-drag-bar" id="kbDragHandle">
                <span class="kb-drag-pill"></span>
            </div>
            <div class="keyboard-header">
                <div class="kb-title-badge">
                    <span class="kb-title-icon">⌨️</span>
                    <span class="kb-title-text">Keitai 12-Key</span>
                </div>
                <div class="kb-mode-pill-group" role="tablist">
                    <button type="button" class="kb-pill-btn is-active" id="kbScriptHiraganaBtn" data-script="hiragana">あ Hiragana</button>
                    <button type="button" class="kb-pill-btn" id="kbScriptKatakanaBtn" data-script="katakana">ア Katakana</button>
                </div>
                <div class="kb-header-right">
                    <button type="button" class="kb-close-btn" id="kbCloseBtn" title="Tutup virtual keyboard">✕ Tutup</button>
                </div>
            </div>

            <!-- 12-KEY KEITAI GRID (4x4: 10 KELOMPOK HURUF + MODIFIER + AKSI) -->
            <div class="keyboard-body">
                <div class="keitai-12key-grid" id="keitai12KeyGrid">
                    <!-- Baris 1 -->
                    <div class="keitai-key-wrapper" data-key-group="a">
                        <button type="button" class="keitai-btn" data-keitai-key="a">
                            <span class="keitai-main-char">あ</span>
                            <span class="keitai-sub-chars">あいうえお</span>
                        </button>
                        <div class="keitai-popup-bubble" hidden></div>
                    </div>
                    <div class="keitai-key-wrapper" data-key-group="ka">
                        <button type="button" class="keitai-btn" data-keitai-key="ka">
                            <span class="keitai-main-char">か</span>
                            <span class="keitai-sub-chars">かきくけこ</span>
                        </button>
                        <div class="keitai-popup-bubble" hidden></div>
                    </div>
                    <div class="keitai-key-wrapper" data-key-group="sa">
                        <button type="button" class="keitai-btn" data-keitai-key="sa">
                            <span class="keitai-main-char">さ</span>
                            <span class="keitai-sub-chars">さしすせそ</span>
                        </button>
                        <div class="keitai-popup-bubble" hidden></div>
                    </div>
                    <div class="keitai-key-wrapper">
                        <button type="button" class="keitai-btn action-key backspace-key" id="kbBackspaceBtn" title="Hapus karakter (Backspace)">
                            <span class="keitai-main-char">⌫</span>
                            <span class="keitai-sub-chars">Hapus</span>
                        </button>
                    </div>

                    <!-- Baris 2 -->
                    <div class="keitai-key-wrapper" data-key-group="ta">
                        <button type="button" class="keitai-btn" data-keitai-key="ta">
                            <span class="keitai-main-char">た</span>
                            <span class="keitai-sub-chars">たちつてと</span>
                        </button>
                        <div class="keitai-popup-bubble" hidden></div>
                    </div>
                    <div class="keitai-key-wrapper" data-key-group="na">
                        <button type="button" class="keitai-btn" data-keitai-key="na">
                            <span class="keitai-main-char">な</span>
                            <span class="keitai-sub-chars">なにぬねの</span>
                        </button>
                        <div class="keitai-popup-bubble" hidden></div>
                    </div>
                    <div class="keitai-key-wrapper" data-key-group="ha">
                        <button type="button" class="keitai-btn" data-keitai-key="ha">
                            <span class="keitai-main-char">は</span>
                            <span class="keitai-sub-chars">はひふへほ</span>
                        </button>
                        <div class="keitai-popup-bubble" hidden></div>
                    </div>
                    <div class="keitai-key-wrapper">
                        <button type="button" class="keitai-btn action-key space-key" id="kbSpaceBtn" title="Spasi">
                            <span class="keitai-main-char">␣</span>
                            <span class="keitai-sub-chars">Spasi</span>
                        </button>
                    </div>

                    <!-- Baris 3 -->
                    <div class="keitai-key-wrapper" data-key-group="ma">
                        <button type="button" class="keitai-btn" data-keitai-key="ma">
                            <span class="keitai-main-char">ま</span>
                            <span class="keitai-sub-chars">まみむめも</span>
                        </button>
                        <div class="keitai-popup-bubble" hidden></div>
                    </div>
                    <div class="keitai-key-wrapper" data-key-group="ya">
                        <button type="button" class="keitai-btn" data-keitai-key="ya">
                            <span class="keitai-main-char">や</span>
                            <span class="keitai-sub-chars">やゆよ</span>
                        </button>
                        <div class="keitai-popup-bubble" hidden></div>
                    </div>
                    <div class="keitai-key-wrapper" data-key-group="ra">
                        <button type="button" class="keitai-btn" data-keitai-key="ra">
                            <span class="keitai-main-char">ら</span>
                            <span class="keitai-sub-chars">らりるれろ</span>
                        </button>
                        <div class="keitai-popup-bubble" hidden></div>
                    </div>
                    <div class="keitai-key-wrapper">
                        <button type="button" class="keitai-btn action-key enter-key" id="kbEnterBtn" title="Baris Baru (Enter)">
                            <span class="keitai-main-char">↵</span>
                            <span class="keitai-sub-chars">Enter</span>
                        </button>
                    </div>

                    <!-- Baris 4 -->
                    <div class="keitai-key-wrapper">
                        <button type="button" class="keitai-btn action-key dakuten-key" id="kbDakutenBtn" title="Ubah bunyi Dakuten / Handakuten / Huruf Kecil">
                            <span class="keitai-main-char">゛゜小</span>
                            <span class="keitai-sub-chars">Ubah Bunyi</span>
                        </button>
                    </div>
                    <div class="keitai-key-wrapper" data-key-group="wa">
                        <button type="button" class="keitai-btn" data-keitai-key="wa">
                            <span class="keitai-main-char">わ</span>
                            <span class="keitai-sub-chars">わをんー</span>
                        </button>
                        <div class="keitai-popup-bubble" hidden></div>
                    </div>
                    <div class="keitai-key-wrapper" data-key-group="punct">
                        <button type="button" class="keitai-btn" data-keitai-key="punct">
                            <span class="keitai-main-char">、。</span>
                            <span class="keitai-sub-chars">、。？！</span>
                        </button>
                        <div class="keitai-popup-bubble" hidden></div>
                    </div>
                    <div class="keitai-key-wrapper">
                        <button type="button" class="keitai-btn action-key qwerty-key" id="kbModeQwertyBtn" title="Ganti ke Mode Ketik Biasa / Auto-Romaji">
                            <span class="keitai-main-char">🌐</span>
                            <span class="keitai-sub-chars">QWERTY</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>"""

    if "Keitai 12-Key" not in html:
        # Regex replace virtual-keyboard-panel lama
        html = re.sub(r'<!-- PANEL VIRTUAL KEYBOARD JEPANG[\s\S]*?</div>\s*</div>\s*</section>', new_keyboard_markup + '\n    </div>\n</section>', html)
        with open(kamus_html, "w", encoding="utf-8") as f:
            f.write(html)
        log("Markup Keitai 12-Key Keyboard berhasil dipasang di kamus/index.html.")
    else:
        log("Markup Keitai 12-Key Keyboard sudah terpasang di kamus/index.html.")

    # 4.b Update CSS di css/pages/kamus.css
    kamus_css = os.path.join(BASE_DIR, "css", "pages", "kamus.css")
    with open(kamus_css, "r", encoding="utf-8") as f:
        k_css = f.read()

    keitai_css_styles = """
/* ==========================================================================
FLOATING MOBILE 12-KEY KEITAI KEYBOARD (DOCK MELAYANG ANTI-CUT)
========================================================================== */
.virtual-keyboard-panel {
  position: fixed !important;
  bottom: 0 !important;
  left: 50% !important;
  transform: translateX(-50%) !important;
  width: 100% !important;
  max-width: 480px !important;
  background: rgba(255, 255, 255, 0.98) !important;
  backdrop-filter: blur(16px) !important;
  -webkit-backdrop-filter: blur(16px) !important;
  border: 1.5px solid var(--pink-border, #f4bfd3) !important;
  border-bottom: none !important;
  border-radius: 22px 22px 0 0 !important;
  box-shadow: 0 -8px 32px rgba(0, 0, 0, 0.16), 0 -2px 10px rgba(233, 30, 99, 0.1) !important;
  z-index: 9999 !important;
  padding: 10px 14px 18px !important;
  box-sizing: border-box !important;
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.25s ease !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 10px !important;
}

.virtual-keyboard-panel.is-collapsed {
  transform: translateX(-50%) translateY(115%) !important;
  pointer-events: none !important;
  opacity: 0 !important;
}

.kb-floating-drag-bar {
  display: flex !important;
  justify-content: center !important;
  padding: 2px 0 4px !important;
  cursor: pointer !important;
}

.kb-drag-pill {
  width: 42px !important;
  height: 4.5px !important;
  border-radius: 99px !important;
  background: rgba(0, 0, 0, 0.18) !important;
}

.keyboard-header {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 8px !important;
}

.kb-title-badge {
  display: inline-flex !important;
  align-items: center !important;
  gap: 6px !important;
  font-size: 12px !important;
  font-weight: 800 !important;
  color: var(--pink, #e91e63) !important;
}

.kb-mode-pill-group {
  display: inline-flex !important;
  background: rgba(0, 0, 0, 0.05) !important;
  padding: 3px !important;
  border-radius: 99px !important;
  gap: 3px !important;
}

.kb-pill-btn {
  font-family: inherit !important;
  font-size: 11.5px !important;
  font-weight: 700 !important;
  border: none !important;
  background: transparent !important;
  color: #555 !important;
  padding: 5px 12px !important;
  border-radius: 99px !important;
  cursor: pointer !important;
  transition: all 0.2s ease !important;
}

.kb-pill-btn.is-active {
  background: #ffffff !important;
  color: var(--pink, #e91e63) !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
}

.kb-close-btn {
  font-family: inherit !important;
  font-size: 12px !important;
  font-weight: 700 !important;
  color: #666 !important;
  background: rgba(0, 0, 0, 0.05) !important;
  border: none !important;
  border-radius: 99px !important;
  padding: 6px 12px !important;
  cursor: pointer !important;
  transition: all 0.2s ease !important;
}

.kb-close-btn:hover {
  background: rgba(233, 30, 99, 0.12) !important;
  color: var(--pink, #e91e63) !important;
}

/* 4x4 Grid 12-Key Keitai */
.keitai-12key-grid {
  display: grid !important;
  grid-template-columns: repeat(4, 1fr) !important;
  gap: 8px !important;
  width: 100% !important;
  box-sizing: border-box !important;
}

.keitai-key-wrapper {
  position: relative !important;
  display: flex !important;
  flex-direction: column !important;
}

.keitai-btn {
  width: 100% !important;
  min-height: 52px !important;
  height: 52px !important;
  border-radius: 12px !important;
  border: 1.5px solid #e5e7eb !important;
  background: #ffffff !important;
  color: #1f2937 !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  cursor: pointer !important;
  user-select: none !important;
  -webkit-user-select: none !important;
  touch-action: manipulation !important;
  transition: transform 0.1s ease, background 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease !important;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04) !important;
  padding: 2px 4px !important;
}

.keitai-btn:active, .keitai-btn.is-pressed {
  transform: scale(0.94) !important;
  background: #fce7f3 !important;
  border-color: var(--pink, #e91e63) !important;
}

.keitai-main-char {
  font-size: 19px !important;
  font-weight: 800 !important;
  line-height: 1.1 !important;
}

.keitai-sub-chars {
  font-size: 9.5px !important;
  color: #6b7280 !important;
  font-weight: 600 !important;
  letter-spacing: -0.2px !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  max-width: 100% !important;
}

/* Action Keys */
.keitai-btn.action-key {
  background: #f3f4f6 !important;
  border-color: #d1d5db !important;
}

.keitai-btn.action-key:active {
  background: #e5e7eb !important;
}

.keitai-btn.action-key.backspace-key,
.keitai-btn.action-key.enter-key {
  color: var(--pink, #e91e63) !important;
}

/* Mini Popup Balloon Vowel Selector */
.keitai-popup-bubble {
  position: absolute !important;
  bottom: calc(100% + 8px) !important;
  left: 50% !important;
  transform: translateX(-50%) !important;
  display: inline-flex !important;
  background: rgba(30, 24, 38, 0.94) !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
  padding: 4px 6px !important;
  border-radius: 99px !important;
  gap: 4px !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3) !important;
  z-index: 10001 !important;
  white-space: nowrap !important;
  animation: keitaiBubblePop 0.15s ease-out !important;
}

.keitai-popup-bubble::after {
  content: "" !important;
  position: absolute !important;
  top: 100% !important;
  left: 50% !important;
  transform: translateX(-50%) !important;
  border-width: 6px 6px 0 6px !important;
  border-style: solid !important;
  border-color: rgba(30, 24, 38, 0.94) transparent transparent transparent !important;
}

@keyframes keitaiBubblePop {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(6px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0) scale(1);
  }
}

.keitai-bubble-pill {
  min-width: 28px !important;
  height: 28px !important;
  border-radius: 99px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  color: #ffffff !important;
  font-size: 14px !important;
  font-weight: 700 !important;
  background: transparent !important;
  border: none !important;
  cursor: pointer !important;
  padding: 0 4px !important;
  transition: all 0.15s ease !important;
}

.keitai-bubble-pill.is-active, .keitai-bubble-pill:active {
  background: var(--pink, #e91e63) !important;
  color: #ffffff !important;
  box-shadow: 0 0 10px rgba(233, 30, 99, 0.6) !important;
  transform: scale(1.15) !important;
}

/* Dark Mode Support for Keitai Keyboard */
body.theme-dark .virtual-keyboard-panel, body.dark-mode .virtual-keyboard-panel {
  background: rgba(22, 17, 28, 0.97) !important;
  border-color: rgba(255, 101, 155, 0.28) !important;
  box-shadow: 0 -10px 36px rgba(0, 0, 0, 0.65) !important;
}

body.theme-dark .kb-drag-pill, body.dark-mode .kb-drag-pill {
  background: rgba(255, 255, 255, 0.25) !important;
}

body.theme-dark .kb-mode-pill-group, body.dark-mode .kb-mode-pill-group {
  background: rgba(255, 255, 255, 0.08) !important;
}

body.theme-dark .kb-pill-btn, body.dark-mode .kb-pill-btn {
  color: #bbb !important;
}

body.theme-dark .kb-pill-btn.is-active, body.dark-mode .kb-pill-btn.is-active {
  background: #2b1f30 !important;
  color: #ff659b !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.35) !important;
}

body.theme-dark .kb-close-btn, body.dark-mode .kb-close-btn {
  color: #ccc !important;
  background: rgba(255, 255, 255, 0.08) !important;
}

body.theme-dark .keitai-btn, body.dark-mode .keitai-btn {
  background: #201726 !important;
  border-color: #35273d !important;
  color: #f3f4f6 !important;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.25) !important;
}

body.theme-dark .keitai-btn:active, body.dark-mode .keitai-btn:active {
  background: #3b1d31 !important;
  border-color: var(--pink, #e91e63) !important;
}

body.theme-dark .keitai-sub-chars, body.dark-mode .keitai-sub-chars {
  color: #9ca3af !important;
}

body.theme-dark .keitai-btn.action-key, body.dark-mode .keitai-btn.action-key {
  background: #18111e !important;
  border-color: #35273d !important;
}
"""
    if "FLOATING MOBILE 12-KEY KEITAI KEYBOARD" not in k_css:
        k_css += "\n" + keitai_css_styles
        with open(kamus_css, "w", encoding="utf-8") as f:
            f.write(k_css)
        log("CSS Keitai 12-Key Keyboard berhasil ditambahkan ke kamus.css.")
    else:
        log("CSS Keitai 12-Key Keyboard sudah ada di kamus.css.")

    # 4.c Update Logika Translator & Keitai Keyboard di js/translator.js
    update_translator_js()

def update_translator_js():
    translator_js_path = os.path.join(BASE_DIR, "js", "translator.js")
    with open(translator_js_path, "r", encoding="utf-8") as f:
        code = f.read()

    new_script_controller = """
// =========================================================================
// 5. KEITAI 12-KEY KEYBOARD DATA & CYCLING CONFIG
// =========================================================================
const KEITAI_GROUPS = {
  hiragana: {
    a: { main: 'あ', sub: 'あいうえお', chars: ['あ', 'い', 'う', 'え', 'お'] },
    ka: { main: 'か', sub: 'かきくけこ', chars: ['か', 'き', 'く', 'け', 'こ'] },
    sa: { main: 'さ', sub: 'さしすせそ', chars: ['さ', 'し', 'す', 'せ', 'そ'] },
    ta: { main: 'た', sub: 'たちつてと', chars: ['た', 'ち', 'つ', 'て', 'と'] },
    na: { main: 'な', sub: 'なにぬねの', chars: ['な', 'に', 'ぬ', 'ね', 'の'] },
    ha: { main: 'は', sub: 'はひふへほ', chars: ['は', 'ひ', 'ふ', 'へ', 'ほ'] },
    ma: { main: 'ま', sub: 'まみむめも', chars: ['ま', 'み', 'む', 'め', 'も'] },
    ya: { main: 'や', sub: 'やゆよ', chars: ['や', 'ゆ', 'よ'] },
    ra: { main: 'ら', sub: 'らりるれろ', chars: ['ら', 'り', 'る', 'le', 'ろ'] },
    wa: { main: 'わ', sub: 'わをんー', chars: ['わ', 'を', 'ん', 'ー', '～'] },
    punct: { main: '、。', sub: '、。？！', chars: ['、', '。', '？', '！', '…'] }
  },
  katakana: {
    a: { main: 'ア', sub: 'アイウエオ', chars: ['ア', 'イ', 'ウ', 'エ', 'オ'] },
    ka: { main: 'カ', sub: 'カキクケコ', chars: ['カ', 'キ', 'ク', 'ケ', 'コ'] },
    sa: { main: 'サ', sub: 'サシスセソ', chars: ['サ', 'シ', 'ス', 'セ', 'ソ'] },
    ta: { main: 'タ', sub: 'タチツテト', chars: ['タ', 'チ', 'ツ', 'テ', 'ト'] },
    na: { main: 'ナ', sub: 'ナニヌネノ', chars: ['ナ', 'ニ', 'ヌ', 'ネ', 'ノ'] },
    ha: { main: 'ハ', sub: 'ハヒフヘホ', chars: ['ハ', 'ヒ', 'フ', 'ヘ', 'ホ'] },
    ma: { main: 'マ', sub: 'マミムメモ', chars: ['マ', 'ミ', 'ム', 'メ', 'モ'] },
    ya: { main: 'ヤ', sub: 'ヤユヨ', chars: ['ヤ', 'ユ', 'ヨ'] },
    ra: { main: 'ラ', sub: 'ラリルレロ', chars: ['ラ', 'リ', 'ル', 'レ', 'ロ'] },
    wa: { main: 'ワ', sub: 'ワヲンー', chars: ['ワ', 'ヲ', 'ン', 'ー', '～'] },
    punct: { main: '、。', sub: '、。？！', chars: ['、', '。', '？', '！', '…'] }
  }
};

const DAKUTEN_CYCLE_MAP = {
  // Hiragana
  'か': 'が', 'が': 'か', 'き': 'ぎ', 'ぎ': 'き', 'く': 'ぐ', 'ぐ': 'く', 'け': 'げ', 'げ': 'け', 'こ': 'ご', 'ご': 'こ',
  'さ': 'ざ', 'ざ': 'さ', 'し': 'じ', 'じ': 'し', 'す': 'ず', 'ず': 'す', 'せ': 'ぜ', 'ぜ': 'せ', 'そ': 'ぞ', 'ぞ': 'そ',
  'た': 'だ', 'だ': 'た', 'ち': 'ぢ', 'ぢ': 'ち', 'つ': 'っ', 'っ': 'づ', 'づ': 'つ', 'て': 'で', 'de': 'te', 'と': 'ど', 'ど': 'と',
  'は': 'ば', 'ば': 'ぱ', 'ぱ': 'は', 'ひ': 'び', 'び': 'ぴ', 'ぴ': 'ひ', 'ふ': 'ぶ', 'ぶ': 'ぷ', 'ぷ': 'ふ', 'へ': 'べ', 'べ': 'ぺ', 'ぺ': 'へ', 'ほ': 'ぼ', 'ぼ': 'ぽ', 'ぽ': 'ほ',
  'や': 'ゃ', 'ゃ': 'や', 'ゆ': 'ゅ', 'ゅ': 'ゆ', 'よ': 'ょ', 'ょ': 'よ',
  'あ': 'ぁ', 'ぁ': 'あ', 'い': 'ぃ', 'ぃ': 'い', 'う': 'ぅ', 'ぅ': 'う', 'え': 'ぇ', 'ぇ': 'え', 'お': 'ぉ', 'ぉ': 'お', 'わ': 'ゎ', 'ゎ': 'わ',

  // Katakana
  'カ': 'ガ', 'ガ': 'カ', 'キ': 'ギ', 'ギ': 'キ', 'ク': 'グ', 'グ': 'ク', 'ケ': 'ゲ', 'ゲ': 'ケ', 'コ': 'ゴ', 'ゴ': 'コ',
  'サ': 'ザ', 'ザ': 'サ', 'シ': 'ジ', 'ジ': 'シ', 'ス': 'ズ', 'ズ': 'ス', 'セ': 'ゼ', 'ゼ': 'セ', 'ソ': 'ゾ', 'ゾ': 'ソ',
  'タ': 'ダ', 'ダ': 'タ', 'チ': 'ヂ', 'ヂ': 'チ', 'ツ': 'ッ', 'ッ': 'ヅ', 'ヅ': 'ツ', 'テ': 'デ', 'デ': 'テ', 'ト': 'ド', 'ド': 'ト',
  'ハ': 'バ', 'バ': 'パ', 'パ': 'ハ', 'ヒ': 'ビ', 'ビ': 'ピ', 'ピ': 'ヒ', 'フ': 'ブ', 'ぶ': 'プ', 'プ': 'フ', 'へ': 'ベ', 'ベ': 'ペ', 'ペ': 'へ', 'ホ': 'ボ', 'ボ': 'ポ', 'ポ': 'ホ',
  'ヤ': 'ャ', 'ャ': 'ヤ', 'ユ': 'ュ', 'ュ': 'ユ', 'ヨ': 'ョ', 'ョ': 'ヨ',
  'ア': 'ァ', 'ァ': 'ア', 'イ': 'ィ', 'ィ': 'イ', 'ウ': 'ゥ', 'ゥ': 'ヴ', 'ヴ': 'ウ', 'エ': 'ェ', 'ェ': 'エ', 'オ': 'ォ', 'ォ': 'オ', 'ワ': 'ヮ', 'ヮ': 'ワ'
};

/**
 * Fetch Terjemahan Online Bebas CORS via Google Translate (client=gtx)
 */
async function fetchGoogleTranslate(text, sourceLang, targetLang) {
  if (!text || !text.trim()) return null;
  const raw = text.trim();
  const cacheKey = `gtx_trans_${sourceLang}_${targetLang}_${raw}`;
  try {
    const cached = localStorage.getItem(cacheKey);
    if (cached) return JSON.parse(cached);
  } catch (e) {}

  try {
    const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=${sourceLang}&tl=${targetLang}&dt=t&dt=rm&q=${encodeURIComponent(raw)}`;
    const res = await fetch(url);
    if (res.ok) {
      const data = await res.json();
      let translated = "";
      let romaji = "";
      if (Array.isArray(data) && Array.isArray(data[0])) {
        data[0].forEach((item) => {
          if (item && item[0]) translated += item[0];
          if (item && item[3]) romaji += (romaji ? " " : "") + item[3];
        });
      }
      if (translated.trim()) {
        const result = { text: translated.trim(), romaji: romaji.trim() };
        try { localStorage.setItem(cacheKey, JSON.stringify(result)); } catch (e) {}
        return result;
      }
    }
  } catch (err) {
    console.warn("Google Translate fetch error:", err);
  }
  return null;
}

/**
 * Terjemahan Utama Studio: Cek Kamus Lokal -> Google Translate -> Fallback
 */
async function translateStudioText(text, direction = "ja-id") {
  const raw = text.trim();
  if (!raw) return { text: "", romaji: "", from: direction };

  const isJaToId = direction === "ja-id";
  const srcLang = isJaToId ? "ja" : "id";
  const tgtLang = isJaToId ? "id" : "ja";

  // 1. Cek Kamus Cepat Lokal
  const localDict = isJaToId ? jaToIdDictionary : idToJaDictionary;
  const lowerRaw = raw.toLowerCase();

  if (localDict[raw]) {
    const res = localDict[raw];
    return {
      text: res,
      romaji: !isJaToId ? getRomajiReading(res) : getRomajiReading(raw),
      isLocal: true
    };
  }
  if (localDict[lowerRaw]) {
    const res = localDict[lowerRaw];
    return {
      text: res,
      romaji: !isJaToId ? getRomajiReading(res) : getRomajiReading(raw),
      isLocal: true
    };
  }

  // 2. Cek Data Kanji Lokal (jika 1 karakter kanji diinputkan)
  if (window.KANJI_FULL_DATA && isJaToId) {
    const kanjiObj = window.KANJI_FULL_DATA.find((k) => k.kanji === raw);
    if (kanjiObj && kanjiObj.meaning) {
      return {
        text: kanjiObj.meaning,
        romaji: getRomajiReading(raw),
        isLocal: true
      };
    }
  }

  // 3. Panggil Google Translate API (gtx)
  const gResult = await fetchGoogleTranslate(raw, srcLang, tgtLang);
  if (gResult && gResult.text) {
    return {
      text: gResult.text,
      romaji: gResult.romaji || (isJaToId ? getRomajiReading(raw) : getRomajiReading(gResult.text)),
      isOnline: true
    };
  }

  // 4. Fallback Kamus Kata per Kata
  if (isJaToId) {
    let fallbackResult = raw;
    for (const [k, v] of Object.entries(jaToIdDictionary)) {
      if (fallbackResult.includes(k)) {
        fallbackResult = fallbackResult.split(k).join(` ${v} `);
      }
    }
    if (fallbackResult !== raw) {
      return {
        text: fallbackResult.replace(/\\s+/g, " ").trim(),
        romaji: getRomajiReading(raw),
        isFallback: true
      };
    }
  }

  return {
    text: raw,
    romaji: isJaToId ? getRomajiReading(raw) : "",
    isNone: true
  };
}

// =========================================================================
// 6. KONTROLER UTAMA STUDIO TRANSLATOR & KEITAI 12-KEY KEYBOARD
// =========================================================================
function initStudioTranslator() {
  const studio = document.getElementById('studio-terjemahan');
  if (!studio) return;

  const sourceFlag = document.getElementById('sourceFlag');
  const sourceName = document.getElementById('sourceName');
  const targetFlag = document.getElementById('targetFlag');
  const targetName = document.getElementById('targetName');
  const sourceFlagMobile = document.getElementById('sourceFlagMobile');
  const sourceNameMobile = document.getElementById('sourceNameMobile');
  const targetFlagMobile = document.getElementById('targetFlagMobile');
  const targetNameMobile = document.getElementById('targetNameMobile');

  const swapBtn = document.getElementById('swapLangBtn');
  const swapBtnMobile = document.getElementById('swapLangBtnMobile');

  const textarea = document.getElementById('translatorInput');
  const outputEl = document.getElementById('translatorOutput');
  const romajiEl = document.getElementById('translatorRomaji');
  const statusEl = document.getElementById('translationStatus');
  const inputHint = document.getElementById('inputHint');
  const charCount = document.getElementById('inputCharCount');

  const listenInputBtn = document.getElementById('listenInputBtn');
  const listenOutputBtn = document.getElementById('listenOutputBtn');
  const copyInputBtn = document.getElementById('copyInputBtn');
  const copyOutputBtn = document.getElementById('copyOutputBtn');
  const clearInputBtn = document.getElementById('clearInputBtn');

  const toggleKeyboardBtn = document.getElementById('toggleKeyboardBtn');
  const keyboardPanel = document.getElementById('virtualKeyboardPanel');
  const keyboardToggleText = document.getElementById('keyboardToggleText');
  const kbCloseBtn = document.getElementById('kbCloseBtn');

  const autoRomajiImeBtn = document.getElementById('autoRomajiImeBtn');
  const imeStatusText = document.getElementById('imeStatusText');

  const kbScriptHiraganaBtn = document.getElementById('kbScriptHiraganaBtn');
  const kbScriptKatakanaBtn = document.getElementById('kbScriptKatakanaBtn');
  const kbModeQwertyBtn = document.getElementById('kbModeQwertyBtn');

  const kbDakutenBtn = document.getElementById('kbDakutenBtn');
  const kbSpaceBtn = document.getElementById('kbSpaceBtn');
  const kbBackspaceBtn = document.getElementById('kbBackspaceBtn');
  const kbEnterBtn = document.getElementById('kbEnterBtn');
  const quickChipsScroll = document.getElementById('quickChipsScroll');

  let activeDirection = 'ja-id';
  let activeScript = 'hiragana';
  let isAutoRomajiOn = true;
  let translateDebounceTimer = null;

  // Keitai multi-tap state
  let lastTapGroup = null;
  let lastTapIndex = 0;
  let tapCycleTimer = null;
  let currentActiveBubble = null;

  function isMobileScreen() {
    return window.innerWidth <= 768;
  }

  function applyMobileKeyboardGuard() {
    if (!textarea) return;
    const isKbOpen = keyboardPanel && !keyboardPanel.classList.contains('is-collapsed');
    if (isMobileScreen() && isKbOpen && activeScript !== 'qwerty') {
      textarea.setAttribute('inputmode', 'none');
    } else {
      textarea.removeAttribute('inputmode');
      textarea.readOnly = false;
    }
  }

  function insertTextAtCursor(charToInsert) {
    if (!textarea) return;
    applyMobileKeyboardGuard();

    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const currentVal = textarea.value;

    textarea.value = currentVal.substring(0, start) + charToInsert + currentVal.substring(end);
    const newPos = start + charToInsert.length;
    textarea.selectionStart = newPos;
    textarea.selectionEnd = newPos;

    try { textarea.focus({ preventScroll: true }); } catch (e) { textarea.focus(); }
    triggerInputUpdate();
    window.MiraiSound?.playClickIfIdle();
  }

  function replaceTextAtCursor(newChar) {
    if (!textarea) return;
    const pos = textarea.selectionStart;
    if (pos <= 0) {
      insertTextAtCursor(newChar);
      return;
    }
    textarea.value = textarea.value.slice(0, pos - 1) + newChar + textarea.value.slice(pos);
    textarea.selectionStart = pos;
    textarea.selectionEnd = pos;
    try { textarea.focus({ preventScroll: true }); } catch (e) {}
    triggerInputUpdate();
    window.MiraiSound?.playClickIfIdle();
  }

  function backspaceAtCursor() {
    if (!textarea) return;
    applyMobileKeyboardGuard();
    commitPendingTap();

    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const currentVal = textarea.value;

    if (start === end) {
      if (start > 0) {
        textarea.value = currentVal.substring(0, start - 1) + currentVal.substring(end);
        textarea.selectionStart = start - 1;
        textarea.selectionEnd = start - 1;
      }
    } else {
      textarea.value = currentVal.substring(0, start) + currentVal.substring(end);
      textarea.selectionStart = start;
      textarea.selectionEnd = start;
    }

    try { textarea.focus({ preventScroll: true }); } catch (e) {}
    triggerInputUpdate();
    window.MiraiSound?.playClickIfIdle();
  }

  function commitPendingTap() {
    clearTimeout(tapCycleTimer);
    lastTapGroup = null;
    lastTapIndex = 0;
    if (currentActiveBubble) {
      currentActiveBubble.hidden = true;
      currentActiveBubble = null;
    }
  }

  // Handle Keitai Key Tap (Multi-tap cycle + mini popup bubble)
  function handleKeitaiKeyTap(groupKey, wrapperEl) {
    applyMobileKeyboardGuard();
    const groupData = KEITAI_GROUPS[activeScript]?.[groupKey] || KEITAI_GROUPS.hiragana[groupKey];
    if (!groupData) return;

    const chars = groupData.chars;
    const bubbleEl = wrapperEl ? wrapperEl.querySelector('.keitai-popup-bubble') : null;

    if (lastTapGroup === groupKey) {
      // Cycle ke huruf berikutnya dalam grup
      lastTapIndex = (lastTapIndex + 1) % chars.length;
      const currentChar = chars[lastTapIndex];
      replaceTextAtCursor(currentChar);
    } else {
      commitPendingTap();
      lastTapGroup = groupKey;
      lastTapIndex = 0;
      const currentChar = chars[0];
      insertTextAtCursor(currentChar);
    }

    // Render Popup Bubble Balon Vokal
    if (bubbleEl) {
      if (currentActiveBubble && currentActiveBubble !== bubbleEl) {
        currentActiveBubble.hidden = true;
      }
      currentActiveBubble = bubbleEl;
      bubbleEl.replaceChildren();

      chars.forEach((c, idx) => {
        const pill = document.createElement('button');
        pill.type = 'button';
        pill.className = 'keitai-bubble-pill' + (idx === lastTapIndex ? ' is-active' : '');
        pill.textContent = c;
        pill.addEventListener('click', (e) => {
          e.stopPropagation();
          replaceTextAtCursor(c);
          commitPendingTap();
          window.speakText && window.speakText(c, 'ja-JP');
        });
        bubbleEl.append(pill);
      });

      bubbleEl.hidden = false;
    }

    window.speakText && window.speakText(chars[lastTapIndex], 'ja-JP');

    clearTimeout(tapCycleTimer);
    tapCycleTimer = setTimeout(() => {
      commitPendingTap();
    }, 1400);
  }

  // Update UI Labels for Keitai Keys according to Hiragana / Katakana
  function updateKeitaiKeyLabels() {
    const script = activeScript === 'katakana' ? 'katakana' : 'hiragana';
    const groups = KEITAI_GROUPS[script];
    studio.querySelectorAll('[data-keitai-key]').forEach((btn) => {
      const k = btn.dataset.keitaiKey;
      if (groups[k]) {
        const mainEl = btn.querySelector('.keitai-main-char');
        const subEl = btn.querySelector('.keitai-sub-chars');
        if (mainEl) mainEl.textContent = groups[k].main;
        if (subEl) subEl.textContent = groups[k].sub;
      }
    });
  }

  // Pasang Event Klik pada Key Wrapper Keitai
  studio.querySelectorAll('.keitai-key-wrapper[data-key-group]').forEach((wrap) => {
    const groupKey = wrap.dataset.keyGroup;
    const btn = wrap.querySelector('.keitai-btn');
    if (btn) {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        handleKeitaiKeyTap(groupKey, wrap);
      });
    }
  });

  // Tombol Dakuten / Handakuten / Huruf Kecil
  if (kbDakutenBtn) {
    kbDakutenBtn.addEventListener('click', () => {
      applyMobileKeyboardGuard();
      const pos = textarea.selectionStart;
      if (pos > 0) {
        const prevChar = textarea.value[pos - 1];
        if (DAKUTEN_CYCLE_MAP[prevChar]) {
          const transformed = DAKUTEN_CYCLE_MAP[prevChar];
          textarea.value = textarea.value.slice(0, pos - 1) + transformed + textarea.value.slice(pos);
          textarea.selectionStart = pos;
          textarea.selectionEnd = pos;
          try { textarea.focus({ preventScroll: true }); } catch (e) {}
          triggerInputUpdate();
          window.MiraiSound?.playClickIfIdle();
          window.speakText && window.speakText(transformed, 'ja-JP');
          commitPendingTap();
          return;
        }
      }
      window.MiraiSound?.playClickIfIdle();
    });
  }

  // Tombol Spasi & Backspace & Enter
  if (kbSpaceBtn) {
    kbSpaceBtn.addEventListener('click', () => {
      commitPendingTap();
      insertTextAtCursor(' ');
    });
  }
  if (kbBackspaceBtn) {
    kbBackspaceBtn.addEventListener('click', () => {
      backspaceAtCursor();
    });
  }
  if (kbEnterBtn) {
    kbEnterBtn.addEventListener('click', () => {
      commitPendingTap();
      insertTextAtCursor('\\n');
    });
  }

  // Toggle Virtual Keyboard Panel (Floating Bottom Dock)
  function setKeyboardCollapsed(collapsed) {
    if (!keyboardPanel) return;
    keyboardPanel.classList.toggle('is-collapsed', collapsed);
    if (toggleKeyboardBtn) {
      toggleKeyboardBtn.setAttribute('aria-expanded', String(!collapsed));
    }
    if (keyboardToggleText) {
      keyboardToggleText.textContent = collapsed
        ? 'Buka Virtual Keyboard Layar ▾'
        : 'Sembunyikan Virtual Keyboard ▴';
    }
    applyMobileKeyboardGuard();
    if (!collapsed) {
      updateKeitaiKeyLabels();
    }
  }

  if (toggleKeyboardBtn) {
    toggleKeyboardBtn.addEventListener('click', () => {
      const isNowCollapsed = !keyboardPanel.classList.contains('is-collapsed');
      setKeyboardCollapsed(isNowCollapsed);
      window.MiraiSound?.playClickIfIdle();
    });
  }

  if (kbCloseBtn) {
    kbCloseBtn.addEventListener('click', () => {
      commitPendingTap();
      setKeyboardCollapsed(true);
      window.MiraiSound?.playClickIfIdle();
    });
  }

  // Switch Script Mode (Hiragana vs Katakana vs QWERTY)
  function setScriptMode(mode) {
    activeScript = mode;
    if (kbScriptHiraganaBtn) kbScriptHiraganaBtn.classList.toggle('is-active', mode === 'hiragana');
    if (kbScriptKatakanaBtn) kbScriptKatakanaBtn.classList.toggle('is-active', mode === 'katakana');

    if (mode === 'qwerty') {
      commitPendingTap();
      setKeyboardCollapsed(true);
      textarea.removeAttribute('inputmode');
      textarea.readOnly = false;
      isAutoRomajiOn = true;
      if (autoRomajiImeBtn) {
        autoRomajiImeBtn.classList.add('is-active');
        autoRomajiImeBtn.classList.remove('is-off');
      }
      if (imeStatusText) imeStatusText.textContent = 'Auto-Romaji: ON ✨';
      try { textarea.focus(); } catch (e) {}
    } else {
      updateKeitaiKeyLabels();
      applyMobileKeyboardGuard();
    }
  }

  if (kbScriptHiraganaBtn) {
    kbScriptHiraganaBtn.addEventListener('click', () => {
      setScriptMode('hiragana');
      window.MiraiSound?.playClickIfIdle();
    });
  }
  if (kbScriptKatakanaBtn) {
    kbScriptKatakanaBtn.addEventListener('click', () => {
      setScriptMode('katakana');
      window.MiraiSound?.playClickIfIdle();
    });
  }
  if (kbModeQwertyBtn) {
    kbModeQwertyBtn.addEventListener('click', () => {
      setScriptMode('qwerty');
      window.MiraiSound?.playClickIfIdle();
    });
  }

  // Real-time Input Update dengan Debounce 300ms
  function triggerInputUpdate() {
    const text = textarea.value;
    if (charCount) charCount.textContent = text.length + " karakter";
    if (statusEl) statusEl.textContent = "Mengetik...";

    clearTimeout(translateDebounceTimer);
    if (!text.trim()) {
      if (outputEl) {
        outputEl.textContent = "Hasil terjemahan akan otomatis muncul di sini...";
        outputEl.classList.add("placeholder");
      }
      if (romajiEl) romajiEl.hidden = true;
      if (statusEl) statusEl.textContent = "Siap menerjemahkan";
      return;
    }

    translateDebounceTimer = setTimeout(async () => {
      if (statusEl) statusEl.textContent = "Menerjemahkan...";
      try {
        const result = await translateStudioText(text, activeDirection);
        if (outputEl) {
          outputEl.textContent = result.text || "";
          outputEl.classList.remove("placeholder");
        }
        if (romajiEl) {
          if (result.romaji && result.romaji !== result.text) {
            romajiEl.textContent = "(Romaji: " + result.romaji + ")";
            romajiEl.hidden = false;
          } else {
            romajiEl.hidden = true;
          }
        }
        if (statusEl) {
          statusEl.textContent = result.isOnline
            ? 'Terjemahan Online (Live)'
            : (result.isLocal ? 'Kamus Internal (Instan)' : 'Selesai diterjemahkan');
        }
      } catch (e) {
        if (statusEl) statusEl.textContent = 'Gagal menerjemahkan';
      }
    }, 300);
  }

  // Auto-Romaji Realtime Conversion on Physical Typing
  function applyRealtimeImeConversion() {
    if (!textarea || typeof window.wanakana === "undefined") return;
    const cursorPos = textarea.selectionStart;
    const val = textarea.value;
    if (!val) return;

    const converted = activeScript === "katakana" ? window.wanakana.toKatakana(val) : window.wanakana.toHiragana(val);
    if (converted !== val) {
      textarea.value = converted;
      const diff = converted.length - val.length;
      textarea.selectionStart = Math.max(0, cursorPos + diff);
      textarea.selectionEnd = Math.max(0, cursorPos + diff);
    }
  }

  textarea.addEventListener('input', () => {
    if (isAutoRomajiOn && activeDirection === 'ja-id') {
      applyRealtimeImeConversion();
    }
    triggerInputUpdate();
  });

  textarea.addEventListener('focus', () => {
    applyMobileKeyboardGuard();
  });

  // Tombol Auto-Romaji Toggle
  if (autoRomajiImeBtn) {
    autoRomajiImeBtn.addEventListener('click', () => {
      isAutoRomajiOn = !isAutoRomajiOn;
      autoRomajiImeBtn.classList.toggle('is-active', isAutoRomajiOn);
      autoRomajiImeBtn.classList.toggle('is-off', !isAutoRomajiOn);
      if (imeStatusText) {
        imeStatusText.textContent = isAutoRomajiOn ? 'Auto-Romaji: ON ✨' : 'Auto-Romaji: OFF';
      }
      window.MiraiSound?.playClickIfIdle();
    });
  }

  // Swap Direction
  function doSwapLanguage() {
    activeDirection = activeDirection === 'ja-id' ? 'id-ja' : 'ja-id';
    const isJa = activeDirection === 'ja-id';

    if (sourceFlag) sourceFlag.textContent = isJa ? '🇯🇵' : '🇮🇩';
    if (sourceName) sourceName.textContent = isJa ? 'Jepang' : 'Indonesia';
    if (targetFlag) targetFlag.textContent = isJa ? '🇮🇩' : '🇯🇵';
    if (targetName) targetName.textContent = isJa ? 'Indonesia' : 'Jepang';

    if (sourceFlagMobile) sourceFlagMobile.textContent = isJa ? '🇯🇵' : '🇮🇩';
    if (sourceNameMobile) sourceNameMobile.textContent = isJa ? 'Jepang' : 'Indonesia';
    if (targetFlagMobile) targetFlagMobile.textContent = isJa ? '🇮🇩' : '🇯🇵';
    if (targetNameMobile) targetNameMobile.textContent = isJa ? 'Indonesia' : 'Jepang';

    if (inputHint) {
      inputHint.textContent = isJa ? 'Ketik aksara Jepang atau Romaji' : 'Ketik dalam Bahasa Indonesia';
    }
    textarea.placeholder = isJa
      ? 'Ketik watashi di keyboard fisik langsung berubah jadi わたし...'
      : 'Ketik kalimat Bahasa Indonesia di sini... (Contoh: Selamat pagi, terima kasih)';

    const currentInput = textarea.value;
    const currentOutput = outputEl.classList.contains('placeholder') ? '' : outputEl.textContent;

    if (currentOutput && !currentOutput.startsWith('(Terjemahan belum')) {
      textarea.value = currentOutput;
    } else if (currentInput) {
      textarea.value = currentInput;
    }

    if (!isJa) {
      setScriptMode('qwerty');
    } else {
      setScriptMode('hiragana');
    }

    window.MiraiSound?.playClickIfIdle();
    triggerInputUpdate();
  }

  if (swapBtn) swapBtn.addEventListener('click', doSwapLanguage);
  if (swapBtnMobile) swapBtnMobile.addEventListener('click', doSwapLanguage);

  // Quick Chips
  if (quickChipsScroll) {
    quickChipsScroll.querySelectorAll('.quick-chip').forEach((chip) => {
      chip.addEventListener('click', () => {
        const text = chip.dataset.text || chip.textContent.split('(')[0].trim();
        textarea.value = text;
        triggerInputUpdate();
        window.MiraiSound?.playClickIfIdle();
      });
    });
  }

  // Audio Buttons
  if (listenInputBtn) {
    listenInputBtn.addEventListener('click', () => {
      const text = textarea.value.trim();
      if (!text) return;
      window.speakText(text, activeDirection === 'ja-id' ? 'ja-JP' : 'id-ID');
    });
  }

  if (listenOutputBtn) {
    listenOutputBtn.addEventListener('click', () => {
      if (outputEl.classList.contains('placeholder')) return;
      const text = outputEl.textContent.trim();
      if (!text) return;
      window.speakText(text, activeDirection === 'ja-id' ? 'id-ID' : 'ja-JP');
    });
  }

  // Copy Buttons
  function copyWithFeedback(text, buttonEl) {
    if (!text) return;
    navigator.clipboard.writeText(text).then(() => {
      const orig = buttonEl.innerHTML;
      buttonEl.innerHTML = '<span>✓ Tersalin!</span>';
      buttonEl.classList.add('btn-copied');
      setTimeout(() => {
        buttonEl.innerHTML = orig;
        buttonEl.classList.remove('btn-copied');
      }, 1800);
    }).catch(() => {
      const temp = document.createElement('textarea');
      temp.value = text;
      document.body.appendChild(temp);
      temp.select();
      document.execCommand('copy');
      document.body.removeChild(temp);
    });
  }

  if (copyInputBtn) copyInputBtn.addEventListener('click', () => copyWithFeedback(textarea.value, copyInputBtn));
  if (copyOutputBtn) copyOutputBtn.addEventListener('click', () => {
    if (!outputEl.classList.contains('placeholder')) copyWithFeedback(outputEl.textContent, copyOutputBtn);
  });
  if (clearInputBtn) {
    clearInputBtn.addEventListener('click', () => {
      textarea.value = '';
      commitPendingTap();
      triggerInputUpdate();
      try { textarea.focus(); } catch (e) {}
      window.MiraiSound?.playClickIfIdle();
    });
  }

  updateKeitaiKeyLabels();
}
"""

    start_marker = "// =========================================================================\n// 5. DATA KARAKTER & LAYOUT KEYBOARD"
    if start_marker in code and "window.MiraiTranslator = {" in code:
        pre = code.split(start_marker)[0]
        idx_end = code.find("window.MiraiTranslator = {")
        sec7_idx = code.rfind("// 7. EXPORT GLOBAL TRANSLATOR", 0, idx_end)
        if sec7_idx != -1:
            div_idx = code.rfind("// ===", 0, sec7_idx)
            if div_idx != -1:
                post = code[div_idx:]
            else:
                post = code[sec7_idx:]
        else:
            post = "// =========================================================================\n// 7. EXPORT GLOBAL TRANSLATOR & INISIALISASI\n// =========================================================================\n" + code[idx_end:]
        code = pre + new_script_controller.strip() + "\n\n" + post
        with open(translator_js_path, "w", encoding="utf-8") as f:
            f.write(code)
        log("Logika Translator Realtime & Keitai 12-Key Keyboard berhasil diperbarui di js/translator.js.")
    else:
        log("Logika Translator Realtime & Keitai 12-Key sudah terintegrasi.")

# ==============================================================================
# MAIN RUNNER
# ==============================================================================
if __name__ == "__main__":
    log("MEMULAI EKSEKUSI 5 PERBAIKAN UTAMA MIRAI NO WEBU...")
    fix_task_1()
    fix_task_2()
    fix_task_3()
    fix_task_4_and_5()
    log("SEMUA 5 PERBAIKAN UTAMA TELAH BERHASIL DISELESAIKAN DENGAN SEMPURNA!")
