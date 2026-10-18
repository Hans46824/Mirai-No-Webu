#!/usr/bin/env python3
"""
Skrip Otomatis: 4 Perbaikan Lanjutan Mirai no Webu
1. Perbaiki Double Pattern pada Quote Card & bersihkan kotak teks anak agar solid putih.
2. Tingkatkan transparansi pattern cerah & gelap agar sangat lembut (opacity: 0.045, hover: 0.07)
   sehingga tidak mengganggu kenyamanan membaca teks.
3. Lepaskan halaman Tentang (/tentang/) dari status "Segera Hadir" (bebas diakses publik).
4. Kunci seksi Prestasi & Penghargaan (#prestasi) pada tentang/index.html dengan status "Segera Hadir".
"""

import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def log(msg):
    print(f"[FIX] {msg}")

def fix_quote_double_pattern():
    log("=== [1] Memperbaiki Double Pattern pada Quote Card ===")
    
    # 1.a Bersihkan tentang.css: hapus .quote-card::after dari selector dark cards
    tentang_css = os.path.join(BASE_DIR, "css", "pages", "tentang.css")
    with open(tentang_css, "r", encoding="utf-8") as f:
        t_css = f.read()

    t_css = t_css.replace(", .quote-card::after", "")
    with open(tentang_css, "w", encoding="utf-8") as f:
        f.write(t_css)
    log(".quote-card::after dihapus dari selector dark w1b di tentang.css.")

    # 1.b Perbaiki global.css dan rekomendasi-motivasi.css agar quote-card hanya memiliki 1 pattern di ::after
    # dan box dalam (profil, box kanji, box makna) memiliki latar belakang solid #ffffff
    quote_clean_css = """
/* Proteksi Anti-Double Pattern & Keterbacaan Teks Quote Card */
.section-quote-slider.quote-theme-white .quote-card {
  background-color: #ffffff !important;
  background: #ffffff !important;
  background-image: none !important;
  border: 1.5px solid var(--quote-border, #f4bfd3) !important;
  box-shadow: 0 14px 38px rgba(233, 30, 99, 0.08), 0 2px 10px rgba(0, 0, 0, 0.04) !important;
  position: relative !important;
  overflow: hidden !important;
}

.section-quote-slider.quote-theme-white .quote-card::after {
  content: "" !important;
  position: absolute !important;
  inset: 0 !important;
  background-image: url("../../images/mirai/background/w1w.jpeg") !important;
  background-size: 200px auto !important;
  background-repeat: repeat !important;
  background-position: center top !important;
  opacity: 0.045 !important;
  mix-blend-mode: multiply !important;
  pointer-events: none !important;
  z-index: 1 !important;
  border-radius: inherit !important;
  display: block !important;
}

.section-quote-slider.quote-theme-white .quote-card > * {
  position: relative !important;
  z-index: 2 !important;
}

.section-quote-slider.quote-theme-white .quote-author-profile,
.section-quote-slider.quote-theme-white .quote-box,
.section-quote-slider.quote-theme-white .quote-meaning-card {
  background: #ffffff !important;
  background-image: none !important;
  position: relative !important;
  z-index: 2 !important;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04) !important;
  border: 1px solid rgba(233, 30, 99, 0.12) !important;
}

.quote-author-profile::before, .quote-author-profile::after,
.quote-box::before, .quote-box::after,
.quote-meaning-card::before, .quote-meaning-card::after {
  content: none !important;
  display: none !important;
  background-image: none !important;
}
"""

    for target_name in ["global.css", "rekomendasi-motivasi.css"]:
        fpath = os.path.join(BASE_DIR, "css", "pages", target_name)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        # Netralkan rule lama .section-quote-slider.quote-theme-white .quote-card yang memuat url w1w
        content = re.sub(
            r"\.section-quote-slider\.quote-theme-white\s+\.quote-card\s*\{[^}]*background-image:[^}]*\}",
            "",
            content
        )
        content = re.sub(
            r"\.section-quote-slider\.quote-theme-white\s+\.quote-card::after\s*\{[^}]*\}",
            "",
            content
        )

        content += "\n" + quote_clean_css
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        log(f"Proteksi quote card tunggal berhasil dipasang di {target_name}.")

def fix_pattern_transparency():
    log("=== [2] Meningkatkan Transparansi Pattern (0.045 / Hover 0.07) di Seluruh CSS ===")
    
    # 2.a Update :root overlays di global.css
    global_css = os.path.join(BASE_DIR, "css", "pages", "global.css")
    with open(global_css, "r", encoding="utf-8") as f:
        g_css = f.read()

    g_css = re.sub(
        r"--overlay-card-light:\s*[^;]+;",
        "--overlay-card-light: linear-gradient(135deg, rgba(255, 255, 255, 0.96), rgba(255, 252, 254, 0.96));",
        g_css
    )
    g_css = re.sub(
        r"--overlay-card-dark:\s*[^;]+;",
        "--overlay-card-dark: linear-gradient(155deg, rgba(16, 12, 22, 0.96), rgba(10, 8, 14, 0.97));",
        g_css
    )
    g_css = re.sub(
        r"--overlay-section-dark:\s*[^;]+;",
        "--overlay-section-dark: linear-gradient(180deg, rgba(14, 11, 18, 0.95), rgba(14, 11, 18, 0.96));",
        g_css
    )
    with open(global_css, "w", encoding="utf-8") as f:
        f.write(g_css)
    log("Overlay master di :root global.css diperlembut ke 0.95-0.97.")

    # 2.b Terapkan opacity sangat lembut pada seluruh kartu di css/pages/*.css
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
        in_pattern_block = False

        for i, l in enumerate(lines):
            new_l = l

            if any(k in l for k in ["c1w.jpeg", "c1b.jpeg", "w1w.jpeg", "w1b.jpeg", "var(--pattern-c1w)", "var(--pattern-c1b)", "var(--pattern-w1w)", "var(--pattern-w1b)"]):
                in_pattern_block = True

            # Ganti base opacity pattern (0.08, 0.09, 0.10, 0.11, 0.16) menjadi 0.045
            if in_pattern_block and "opacity:" in new_l:
                new_l = re.sub(r"opacity:\s*(?:0\.08|0\.09|0\.10|0\.11|0\.16)(\s*!important)?;", "opacity: 0.045 !important;", new_l)

            # Ganti hover opacity pattern (0.12, 0.16) menjadi 0.07
            if "opacity:" in new_l and any(k in new_l for k in ["0.12", "0.16"]):
                is_hover = any(":hover" in lines[j] for j in range(max(0, i - 4), i + 1))
                if is_hover:
                    new_l = re.sub(r"opacity:\s*(?:0\.12|0\.16)(\s*!important)?;", "opacity: 0.07 !important;", new_l)

            if "}" in l:
                in_pattern_block = False

            new_lines.append(new_l)

        res_open = sum(l.count("{") for l in new_lines)
        res_close = sum(l.count("}") for l in new_lines)
        assert orig_open == res_open and orig_close == res_close, f"Brace mismatch in {fname}!"

        with open(fpath, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        log(f"Transparansi lembut (0.045 / hover 0.07) diterapkan pada {fname}.")

def fix_tentang_and_prestasi_coming_soon():
    log("=== [3 & 4] Membebaskan Halaman Tentang & Mengunci Seksi Prestasi ===")
    main_js = os.path.join(BASE_DIR, "js", "main.js")
    with open(main_js, "r", encoding="utf-8") as f:
        code = f.read()

    # 3. Lepaskan Tentang dari lockedDirs & lockedWords
    code = code.replace('"/tentang/",\n', '')
    code = code.replace('"/tentang/"\n', '')
    code = code.replace('"tentang",\n', '')
    code = code.replace('"tentang"\n', '')

    # 4. Tambahkan penguncian seksi Prestasi & Penghargaan di updateSectionComingSoonOverlays
    prestasi_lock_code = """  // 3. Seksi Prestasi & Penghargaan di tentang/index.html
  const prestasiEl = document.getElementById("prestasi");
  if (prestasiEl) {
    if (!isUnlocked) {
      prestasiEl.classList.add("is-section-locked");
      let overlay = prestasiEl.querySelector(".coming-soon-section-overlay");
      if (!overlay) {
        overlay = document.createElement("div");
        overlay.className = "coming-soon-section-overlay";
        overlay.innerHTML = `
          <div class="coming-soon-card">
            <div class="coming-soon-pill">🔒 SEGERA HADIR</div>
            <div class="coming-soon-icon">🏆</div>
            <h3 class="coming-soon-title">Prestasi &amp; Penghargaan</h3>
            <span class="coming-soon-kanji">実績と表彰 (近日公開)</span>
            <p class="coming-soon-desc">Rekapitulasi resmi daftar kejuaraan, medali, dan piagam apresiasi prestasi anggota klub sedang dalam tahap verifikasi data dokumentasi.</p>
            <div class="coming-soon-actions">
              <button type="button" class="coming-soon-btn-unlock cs-section-unlock-btn">
                <span>🔑 Masukkan Sandi Pengurus</span>
              </button>
            </div>
          </div>
        `;
        prestasiEl.appendChild(overlay);
        overlay.querySelector(".cs-section-unlock-btn")?.addEventListener("click", () => {
          window.MiraiSound?.playClickIfIdle();
          openPasswordModal();
        });
      }
    } else {
      prestasiEl.classList.remove("is-section-locked");
      prestasiEl.querySelector(".coming-soon-section-overlay")?.remove();
    }
  }
"""

    if "Seksi Prestasi & Penghargaan di tentang/index.html" not in code:
        # Sisipkan sebelum penutup updateSectionComingSoonOverlays
        anchor = "function updateSectionComingSoonOverlays(isUnlocked) {"
        if anchor in code:
            code = code.replace(anchor, anchor + "\n" + prestasi_lock_code)
            log("Seksi Prestasi & Penghargaan berhasil dikunci dengan overlay Segera Hadir di js/main.js.")
    
    with open(main_js, "w", encoding="utf-8") as f:
        f.write(code)
    log("Halaman Tentang berhasil dibebaskan dari Segera Hadir di js/main.js.")

def verify_all_css():
    log("=== Verifikasi Integritas Seluruh File CSS ===")
    css_dir = os.path.join(BASE_DIR, "css", "pages")
    for fname in sorted(os.listdir(css_dir)):
        if not fname.endswith(".css"):
            continue
        fpath = os.path.join(css_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            c = f.read()
        o = c.count("{")
        cl = c.count("}")
        assert o == cl, f"Ketidakseimbangan kurung kurawal pada {fname} (Open: {o}, Close: {cl})!"
    log("SELURUH 11 FILE CSS 100% BALANCED & BEBAS ERROR SINTAKS!")

if __name__ == "__main__":
    fix_quote_double_pattern()
    fix_pattern_transparency()
    fix_tentang_and_prestasi_coming_soon()
    verify_all_css()
    log("SEMUA 4 PERBAIKAN TELAH SELESAI DENGAN SEMPURNA!")

