#!/usr/bin/env python3
"""
File: skrip/arsip/fix_namegen_ui.py
Fungsi:
 1. Memperbaiki UI/UX, tata letak, posisi, dan ukuran Generator Nama Jepang & Kartu Anggota (KTA Mirai no Hana).
 2. Mendesain ulang tata letak Laptop/Desktop: 2 kolom seimbang (min-width: 0, breakpoint 960px).
 3. Menghapus seksi 'Contoh Nama Cepat' dari HTML, JS, dan CSS.
 4. Memastikan kartu KTA responsive dan proporsional di HP (360px - 430px) hingga laptop/desktop.
 5. Menambah ruang bebas bawah (padding-bottom: 90px) agar tidak tertutup tombol melayang (Sora, goresan, to-top).
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]

def update_html():
    html_file = ROOT / "kamus" / "index.html"
    content = html_file.read_text(encoding="utf-8")

    # Pola untuk mengganti seluruh isi #panelNameGen
    pattern = re.compile(
        r'<!-- TAB PANEL 2: GENERATOR NAMA JEPANG & KARTU ANGGOTA \(OSATSU MIRAI NO HANA\) -->\s*<div class="studio-tab-panel" id="panelNameGen" data-studio-panel="namegen" hidden>.*?</div>\s*</div>\s*</section>',
        re.DOTALL
    )

    new_panel = """<!-- TAB PANEL 2: GENERATOR NAMA JEPANG & KARTU ANGGOTA (OSATSU MIRAI NO HANA) -->
    <div class="studio-tab-panel" id="panelNameGen" data-studio-panel="namegen" hidden>
        <div class="studio-container namegen-container">
            <div class="namegen-grid">
                <!-- KOLOM KIRI: FORMULIR INPUT IDENTITAS -->
                <div class="namegen-form-card studio-card">
                    <div class="studio-card-head">
                        <div class="card-head-left">
                            <span class="card-badge">
                                <span class="badge-flag">🎴</span>
                                <span class="badge-name">Identitas Siswa</span>
                            </span>
                            <span class="namegen-badge-tag">Katakana &amp; Ateji</span>
                        </div>
                    </div>

                    <div class="namegen-form-body">
                        <div class="namegen-field-group">
                            <label for="nameGenInput" class="namegen-label">
                                <span>Nama Panggilan / Lengkap <span class="req-star">*</span></span>
                                <small class="namegen-sublabel">Sistem otomatis mengonversi fonetik Indonesia ke Katakana &amp; Kanji Ateji</small>
                            </label>
                            <div class="namegen-input-wrap">
                                <input type="text" id="nameGenInput" class="namegen-input" placeholder="Ketik nama kamu, misal: Raditya, Riska, Aqmar..." maxlength="40" autocomplete="off" value="Raditya" aria-label="Ketik nama kamu, misal: Raditya, Riska, Aqmar...">
                                <button type="button" class="mini-clear-btn" id="clearNameInputBtn" title="Hapus teks nama" aria-label="Hapus nama">🗑️</button>
                            </div>
                        </div>

                        <div class="namegen-row-2col">
                            <div class="namegen-field-group">
                                <label for="nameGenClass" class="namegen-label">
                                    <span>Kelas / Angkatan <small>(Opsional)</small></span>
                                </label>
                                <input type="text" id="nameGenClass" class="namegen-input" placeholder="Misal: X-E2 / Angkatan 8" maxlength="25" value="X-E2 / Angkatan 8" aria-label="Misal: X-E2 / Angkatan 8">
                            </div>

                            <div class="namegen-field-group">
                                <label for="nameGenDivision" class="namegen-label">
                                    <span>Divisi Pilihan</span>
                                </label>
                                <div class="namegen-select-wrap">
                                    <select id="nameGenDivision" class="namegen-select" aria-label="Divisi Pilihan">
                                        <option value="bahasa" selected>📚 Divisi Bahasa &amp; Budaya</option>
                                        <option value="cosplay">🎭 Divisi Cosplay &amp; Seni Peran</option>
                                        <option value="desain">🎨 Divisi Desain &amp; Kreatif</option>
                                        <option value="kewirausahaan">🍱 Divisi Kewirausahaan</option>
                                        <option value="anggota">🌸 Anggota Baru Klub</option>
                                    </select>
                                </div>
                            </div>
                        </div>

                        <div class="namegen-actions-bar">
                            <button type="button" class="studio-btn primary namegen-submit-btn" id="generateNameCardBtn">
                                <span>✨ Buat Nama &amp; Kartu Anggota</span>
                            </button>
                        </div>

                        <div class="namegen-tips-box">
                            <span class="tips-icon">💡</span>
                            <span class="tips-text">Nama di atas otomatis diperbarui secara langsung saat kamu mengetik dan siap diunduh menjadi Kartu Tanda Anggota (KTA) digital.</span>
                        </div>
                    </div>
                </div>

                <!-- KOLOM KANAN: HASIL NAMA, FILOSOFI ATEJI & KARTU TANDA ANGGOTA -->
                <div class="namegen-result-card studio-card">
                    <!-- BANNER NAMA KATAKANA -->
                    <div class="namegen-phonetic-banner">
                        <div class="phonetic-left">
                            <span class="phonetic-label">NAMA RESMI JEPANG (KATAKANA)</span>
                            <div class="phonetic-display">
                                <span class="katakana-large" id="resKatakana" lang="ja">ラディティヤ</span>
                                <span class="romaji-sub" id="resRomaji">(Raditiya)</span>
                            </div>
                        </div>
                        <div class="phonetic-right" style="display:flex;gap:6px;align-items:center;">
                            <button type="button" class="icon-audio-btn primary" id="listenKatakanaBtn" title="Dengarkan pelafalan nama dalam Bahasa Jepang (Normal)" aria-label="Dengarkan pelafalan nama">
                                🔊
                            </button>
                            <button type="button" class="icon-audio-btn btn-audio-slow" id="listenKatakanaSlowBtn" title="Dengarkan pelafalan nama pelan (Slow-Mo)" aria-label="Dengarkan pelafalan nama lambat">
                                🐢
                            </button>
                        </div>
                    </div>

                    <!-- KOTAK ATEJI KANJI POSITIF -->
                    <div class="namegen-ateji-box">
                        <div class="ateji-header">
                            <span class="ateji-icon">📜</span>
                            <div class="ateji-head-text">
                                <strong>Ateji Kanji Positif &amp; Filosofi Makna</strong>
                                <small>Karakter Kanji pembawa doa &amp; harapan baik untuk namamu</small>
                            </div>
                        </div>
                        <div class="ateji-kanji-row" id="resAtejiRow">
                            <div class="ateji-chip"><span class="ateji-kanji" lang="ja">羅</span><div class="ateji-chip-info"><strong class="ateji-reading">Ra</strong><span class="ateji-meaning">Jalinan Sutra &amp; Perlindungan</span></div></div>
                            <div class="ateji-chip"><span class="ateji-kanji" lang="ja">大</span><div class="ateji-chip-info"><strong class="ateji-reading">Dai</strong><span class="ateji-meaning">Kebesaran Jiwa &amp; Kelapangan</span></div></div>
                            <div class="ateji-chip"><span class="ateji-kanji" lang="ja">矢</span><div class="ateji-chip-info"><strong class="ateji-reading">Ya</strong><span class="ateji-meaning">Ketepatan Arah Cita-Cita</span></div></div>
                        </div>
                        <p class="ateji-philosophy-text" id="resAtejiPhilosophy">
                            "Sosok berjiwa besar yang memiliki tekad kuat, melangkah mantap mencapai cita-cita dengan ketepatan anak panah."
                        </p>
                    </div>

                    <!-- LIVE PREVIEW KARTU TANDA ANGGOTA MIRAI NO HANA (OSATSU PASS) -->
                    <div class="member-card-stage">
                        <div class="member-card-wrap" id="memberCardVisual">
                            <div class="mcard-inner">
                                <div class="mcard-topbar">
                                    <div class="mcard-brand">
                                        <span class="mcard-flower-icon">🌸</span>
                                        <div class="mcard-brand-text">
                                            <span class="mcard-club-name">MIRAI NO HANA</span>
                                            <span class="mcard-sub-jp" lang="ja">未来之花 · 会員証</span>
                                        </div>
                                    </div>
                                    <div class="mcard-id-pill" id="mcardIdText">MNH-2026-8821</div>
                                </div>

                                <div class="mcard-body">
                                    <div class="mcard-name-col">
                                        <div class="mcard-jp-name" id="mcardKatakana" lang="ja">ラディティヤ</div>
                                        <div class="mcard-latin-name" id="mcardLatin">Raditya</div>
                                        <div class="mcard-meta-row">
                                            <span class="mcard-meta-pill" id="mcardDivisionPill">📚 Divisi Bahasa &amp; Budaya</span>
                                            <span class="mcard-meta-pill class-pill" id="mcardClassPill">X-E2 / Angkatan 8</span>
                                        </div>
                                    </div>
                                    <div class="mcard-ateji-col">
                                        <div class="mcard-kanji-stamp" id="mcardKanjiStamp" lang="ja">
                                            <span>羅</span>
                                            <span>大</span>
                                            <span>矢</span>
                                        </div>
                                        <div class="mcard-red-seal" lang="ja">未来<br>之印</div>
                                    </div>
                                </div>

                                <div class="mcard-footer">
                                    <span class="mcard-school">SMA Wachid Hasyim 2 Taman Sidoarjo</span>
                                    <div class="mcard-barcode">||| | |||| | |||||| || | ||| |||| |</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- TOMBOL UNDUH KARTU PNG -->
                    <div class="namegen-download-row">
                        <button type="button" class="studio-btn primary download-card-btn" id="downloadCardPngBtn">
                            <span class="btn-icon">📥</span>
                            <span>Unduh Kartu Anggota (.PNG)</span>
                        </button>
                        <span class="download-hint">Format PNG Resolusi Tinggi (Siap simpan ke galeri HP / Story Instagram)</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>"""

    if pattern.search(content):
        content = pattern.sub(lambda m: new_panel, content)
        html_file.write_text(content, encoding="utf-8")
        print("✓ kamus/index.html berhasil diperbarui dengan layout namegen baru tanpa contoh cepat.")
    else:
        print("! Warning: Pola #panelNameGen di kamus/index.html tidak cocok.")

def update_js():
    js_file = ROOT / "js" / "translator.js"
    content = js_file.read_text(encoding="utf-8")

    old_block = """  // Quick Chips
  const nameQuickChips = document.getElementById('nameQuickChips');
  if (nameQuickChips) {
    nameQuickChips.addEventListener('click', (e) => {
      const btn = e.target.closest('.name-chip');
      if (!btn) return;
      const chipName = btn.dataset.name;
      if (chipName && nameInput) {
        nameInput.value = chipName;
        window.MiraiSound?.playClickIfIdle();
        triggerGeneration();
      }
    });
  }
"""
    if old_block in content:
        content = content.replace(old_block, "")
        js_file.write_text(content, encoding="utf-8")
        print("✓ js/translator.js: Listener nameQuickChips berhasil dibersihkan.")
    elif "nameQuickChips" in content:
        # Fallback regex jika ada sedikit perbedaan whitespace
        content = re.sub(r'[ \t]*// Quick Chips\s*const nameQuickChips = document\.getElementById\(\'nameQuickChips\'\);[\s\S]*?\}\s*\}\s*\}\s*\n', '', content)
        js_file.write_text(content, encoding="utf-8")
        print("✓ js/translator.js: Listener nameQuickChips berhasil dibersihkan via regex fallback.")
    else:
        print("ℹ js/translator.js: nameQuickChips sudah bersih.")

def update_css():
    css_file = ROOT / "css" / "pages" / "kamus.css"
    content = css_file.read_text(encoding="utf-8")

    # 1. Bersihkan duplikasi / blok lama yang menyembunyikan quick-chips-scroll global
    content = content.replace(
        """.studio-swap-column,
.studio-mobile-lang-bar,
.quick-examples-wrap,
.quick-chips-scroll,
.quick-chip {
  display: none !important;
}""",
        """/* Sembunyikan elemen lama swap dan quick-examples */
.studio-swap-column,
.studio-mobile-lang-bar,
.quick-examples-wrap,
#panelTranslator .quick-chips-scroll,
#panelTranslator .quick-chip {
  display: none !important;
}"""
    )

    # 2. Ganti seluruh blok CSS Generator Nama Jepang
    # dari /* === GENERATOR NAMA JEPANG sampai sebelum STICKY KANJI DETAIL PANEL
    namegen_css_pattern = re.compile(
        r'/\* =+\s*GENERATOR NAMA JEPANG & KARTU ANGGOTA.*?(?=/\* =+\s*STICKY KANJI DETAIL PANEL)',
        re.DOTALL
    )

    new_namegen_css = """/* ==========================================================================
   GENERATOR NAMA JEPANG & KARTU ANGGOTA (OSATSU MIRAI NO HANA)
   ========================================================================== */
.namegen-container {
  max-width: 1120px;
  margin: 0 auto;
  box-sizing: border-box;
}

.namegen-grid {
  display: grid !important;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1.25fr) !important;
  gap: 28px !important;
  align-items: start !important;
}

/* Formulir Input Identitas (Kolom Kiri) */
.namegen-form-card {
  min-width: 0 !important;
  background: #ffffff !important;
  border: 1.5px solid var(--pink-border, #fcd1e5) !important;
  border-radius: 20px !important;
  padding: 24px !important;
  box-shadow: 0 8px 26px rgba(72, 32, 52, 0.05) !important;
  box-sizing: border-box !important;
}

body.theme-dark .namegen-form-card,
body.dark-mode .namegen-form-card {
  background: #191422 !important;
  border-color: rgba(233, 30, 99, 0.3) !important;
  box-shadow: 0 8px 26px rgba(0, 0, 0, 0.3) !important;
}

.namegen-badge-tag {
  font-size: 12px;
  font-weight: 700;
  color: var(--pink, #e91e63);
  background: #fff0f5;
  padding: 4px 12px;
  border-radius: 999px;
  border: 1px solid #ffd4e5;
}

body.theme-dark .namegen-badge-tag,
body.dark-mode .namegen-badge-tag {
  background: rgba(233, 30, 99, 0.2);
  border-color: rgba(233, 30, 99, 0.4);
  color: #ff6090;
}

.namegen-form-body {
  margin-top: 18px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.namegen-field-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 0;
}

.namegen-label {
  font-size: 13.5px;
  font-weight: 700;
  color: var(--ink, #2c2030);
  display: flex;
  flex-direction: column;
  gap: 2px;
}

body.theme-dark .namegen-label,
body.dark-mode .namegen-label {
  color: #f1ecf4;
}

.namegen-label .req-star {
  color: var(--pink, #e91e63);
}

.namegen-sublabel {
  font-size: 11.5px;
  font-weight: 500;
  color: var(--muted, #6d5b72);
}

body.theme-dark .namegen-sublabel,
body.dark-mode .namegen-sublabel {
  color: #a89cb0;
}

.namegen-input-wrap {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
}

.namegen-input,
.namegen-select {
  width: 100%;
  padding: 12px 16px;
  background: #ffffff;
  border: 1.5px solid var(--pink-border, #fcd1e5);
  border-radius: 12px;
  color: var(--ink, #201c26);
  font-size: 15px;
  font-family: inherit;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.namegen-input {
  padding-right: 42px;
}

body.theme-dark .namegen-input,
body.theme-dark .namegen-select,
body.dark-mode .namegen-input,
body.dark-mode .namegen-select {
  background: #231b2e;
  border-color: rgba(233, 30, 99, 0.35);
  color: #f1ecf4;
}

.namegen-input:focus,
.namegen-select:focus {
  outline: none;
  border-color: var(--pink, #e91e63);
  box-shadow: 0 0 0 3px rgba(255, 101, 155, 0.2);
}

.namegen-row-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.namegen-select-wrap {
  position: relative;
}

.namegen-select {
  cursor: pointer;
}

.namegen-actions-bar {
  margin-top: 4px;
}

.namegen-submit-btn {
  width: 100%;
  padding: 14px;
  font-size: 15px;
  font-weight: 800;
  border-radius: 12px;
  background: linear-gradient(135deg, #ff4f91 0%, #e91e63 100%);
  color: #ffffff;
  box-shadow: 0 6px 18px rgba(233, 30, 99, 0.28);
  transition: all 0.2s ease;
}

.namegen-submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 22px rgba(233, 30, 99, 0.38);
}

.namegen-tips-box {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 14px;
  background: #fdf5f8;
  border: 1px solid #f8d5e3;
  border-radius: 12px;
  font-size: 12px;
  line-height: 1.5;
  color: #6d5462;
}

body.theme-dark .namegen-tips-box,
body.dark-mode .namegen-tips-box {
  background: #211928;
  border-color: rgba(233, 30, 99, 0.25);
  color: #c9bed0;
}

.tips-icon {
  font-size: 16px;
  flex-shrink: 0;
}

/* Kolom Kanan: Hasil Nama, Ateji, & Kartu KTA */
.namegen-result-card {
  min-width: 0 !important;
  background: #ffffff !important;
  border: 1.5px solid var(--pink-border, #fcd1e5) !important;
  border-radius: 20px !important;
  padding: 24px !important;
  box-shadow: 0 8px 26px rgba(72, 32, 52, 0.05) !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 18px !important;
  box-sizing: border-box !important;
}

body.theme-dark .namegen-result-card,
body.dark-mode .namegen-result-card {
  background: #191422 !important;
  border-color: rgba(233, 30, 99, 0.3) !important;
  box-shadow: 0 8px 26px rgba(0, 0, 0, 0.3) !important;
}

/* Banner Katakana */
.namegen-phonetic-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: #fff4f8;
  border: 1.5px solid #fbd3e5;
  border-radius: 16px;
  gap: 12px;
  flex-wrap: wrap;
}

body.theme-dark .namegen-phonetic-banner,
body.dark-mode .namegen-phonetic-banner {
  background: #23192a;
  border-color: rgba(233, 30, 99, 0.35);
}

.phonetic-left {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.phonetic-label {
  font-size: 11px;
  font-weight: 800;
  color: var(--pink, #e91e63);
  letter-spacing: 0.8px;
  text-transform: uppercase;
}

.phonetic-display {
  display: flex;
  align-items: baseline;
  gap: 10px;
  flex-wrap: wrap;
}

.katakana-large {
  font-size: clamp(24px, 3.5vw, 32px);
  font-weight: 900;
  color: var(--ink, #201c26);
  font-family: var(--font-jp, "Noto Sans JP", sans-serif);
  letter-spacing: 1px;
  line-height: 1.2;
}

body.theme-dark .katakana-large,
body.dark-mode .katakana-large {
  color: #ffffff;
}

.romaji-sub {
  font-size: 15px;
  font-weight: 700;
  color: var(--pink, #e91e63);
}

/* Ateji Box */
.namegen-ateji-box {
  background: #faf7fc;
  border: 1.5px solid #f0e4f4;
  border-radius: 16px;
  padding: 16px;
}

body.theme-dark .namegen-ateji-box,
body.dark-mode .namegen-ateji-box {
  background: #20182b;
  border-color: rgba(233, 30, 99, 0.25);
}

.ateji-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.ateji-icon {
  font-size: 20px;
}

.ateji-head-text strong {
  display: block;
  font-size: 13.5px;
  font-weight: 800;
  color: var(--ink, #201c26);
}

body.theme-dark .ateji-head-text strong,
body.dark-mode .ateji-head-text strong {
  color: #f1ecf4;
}

.ateji-head-text small {
  font-size: 11.5px;
  color: var(--muted, #6d6471);
}

body.theme-dark .ateji-head-text small,
body.dark-mode .ateji-head-text small {
  color: #a89cb0;
}

.ateji-kanji-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
  gap: 10px;
  margin-bottom: 12px;
}

.ateji-chip {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #ffffff;
  border: 1px solid #f0d8e4;
  border-radius: 12px;
  padding: 8px 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
  min-width: 0;
}

body.theme-dark .ateji-chip,
body.dark-mode .ateji-chip {
  background: #171220;
  border-color: rgba(233, 30, 99, 0.3);
}

.ateji-kanji {
  font-size: 26px;
  font-weight: 900;
  font-family: 'Noto Serif JP', serif;
  color: #e91e63;
  width: 32px;
  flex-shrink: 0;
  text-align: center;
  line-height: 1;
}

.ateji-chip-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
  overflow: hidden;
}

.ateji-reading {
  font-size: 13px;
  font-weight: 800;
  color: var(--ink, #201c26);
  line-height: 1.2;
}

body.theme-dark .ateji-reading,
body.dark-mode .ateji-reading {
  color: #ffffff;
}

.ateji-meaning {
  font-size: 11px;
  color: var(--muted, #6d6471);
  line-height: 1.3;
  word-break: break-word;
}

body.theme-dark .ateji-meaning,
body.dark-mode .ateji-meaning {
  color: #b5a8bd;
}

.ateji-philosophy-text {
  font-size: 12.5px;
  line-height: 1.6;
  color: #4a3b4d;
  font-style: italic;
  margin: 0;
  padding-top: 10px;
  border-top: 1px dashed rgba(233, 30, 99, 0.2);
}

body.theme-dark .ateji-philosophy-text,
body.dark-mode .ateji-philosophy-text {
  color: #d1c8d6;
}

/* ==========================================================================
   LIVE PREVIEW KARTU TANDA ANGGOTA (OSATSU MIRAI NO HANA)
   ========================================================================== */
.member-card-stage {
  width: 100%;
  max-width: 520px;
  margin: 0 auto;
}

.member-card-wrap {
  width: 100%;
  aspect-ratio: 16 / 9.5;
  background: linear-gradient(135deg, #1b1326 0%, #110d18 50%, #09070e 100%);
  border: 2px solid rgba(255, 101, 155, 0.55);
  border-radius: 20px;
  padding: clamp(12px, 3.2vw, 20px);
  box-shadow: 0 16px 45px rgba(0, 0, 0, 0.65), 0 0 24px rgba(233, 30, 99, 0.22);
  position: relative;
  overflow: hidden;
  color: #ffffff;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

.member-card-wrap::before {
  content: "";
  position: absolute;
  inset: 6px;
  border: 1px dashed rgba(255, 255, 255, 0.14);
  border-radius: 14px;
  pointer-events: none;
}

.member-card-wrap::after {
  content: "";
  position: absolute;
  right: -30px;
  top: 50%;
  transform: translateY(-50%);
  width: 180px;
  height: 180px;
  border-radius: 50%;
  border: 24px solid rgba(255, 101, 155, 0.06);
  pointer-events: none;
}

.mcard-inner {
  position: relative;
  z-index: 2;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.mcard-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.mcard-brand {
  display: flex;
  align-items: center;
  gap: 8px;
}

.mcard-flower-icon {
  font-size: clamp(16px, 3vw, 22px);
}

.mcard-brand-text {
  display: flex;
  flex-direction: column;
}

.mcard-club-name {
  font-size: clamp(12px, 2.2vw, 15px);
  font-weight: 900;
  letter-spacing: 1px;
  color: #ffffff;
  line-height: 1.1;
}

.mcard-sub-jp {
  font-size: clamp(8px, 1.6vw, 10px);
  color: #ff85b3;
  font-family: 'Noto Serif JP', serif;
}

.mcard-id-pill {
  font-size: clamp(9px, 1.8vw, 11px);
  font-weight: 800;
  font-family: monospace;
  background: rgba(255, 101, 155, 0.2);
  border: 1px solid rgba(255, 101, 155, 0.45);
  color: #ff85b3;
  padding: 3px 8px;
  border-radius: 999px;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.mcard-body {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 6px 0;
  gap: 12px;
}

.mcard-name-col {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.mcard-jp-name {
  font-size: clamp(18px, 4.2vw, 26px);
  font-weight: 900;
  font-family: 'Noto Sans JP', sans-serif;
  color: #ffffff;
  text-shadow: 0 0 12px rgba(255, 101, 155, 0.5);
  line-height: 1.15;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.mcard-latin-name {
  font-size: clamp(12px, 2.4vw, 15px);
  font-weight: 700;
  color: #ffd1e3;
  line-height: 1.2;
}

.mcard-meta-row {
  display: flex;
  align-items: center;
  gap: 5px;
  margin-top: 4px;
  flex-wrap: wrap;
}

.mcard-meta-pill {
  font-size: clamp(8.5px, 1.7vw, 10.5px);
  font-weight: 600;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.16);
  padding: 2px 7px;
  border-radius: 6px;
  color: #f1f5f9;
  white-space: nowrap;
}

.mcard-ateji-col {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.mcard-kanji-stamp {
  display: flex;
  flex-direction: column;
  gap: 1px;
  background: rgba(20, 14, 28, 0.85);
  border: 1px solid rgba(255, 101, 155, 0.4);
  border-radius: 8px;
  padding: 3px 6px;
  font-family: 'Noto Serif JP', serif;
  font-size: clamp(12px, 2.5vw, 16px);
  font-weight: 800;
  color: #ffffff;
  text-align: center;
  line-height: 1.1;
}

.mcard-red-seal {
  width: clamp(34px, 6vw, 44px);
  height: clamp(34px, 6vw, 44px);
  background: #e11d48;
  border: 1.5px solid #ffe4e6;
  border-radius: 8px;
  color: #ffffff;
  font-size: clamp(9px, 1.8vw, 12px);
  font-weight: 900;
  font-family: 'Noto Serif JP', serif;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  line-height: 1.1;
  box-shadow: 0 4px 10px rgba(225, 29, 72, 0.4);
  flex-shrink: 0;
}

.mcard-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: clamp(8px, 1.6vw, 10.5px);
  color: #94a3b8;
  gap: 8px;
}

.mcard-school {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.mcard-barcode {
  font-family: monospace;
  letter-spacing: 1.5px;
  color: rgba(255, 255, 255, 0.45);
  font-size: clamp(7.5px, 1.5vw, 10px);
  white-space: nowrap;
}

.namegen-download-row {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
  width: 100%;
}

.download-card-btn {
  width: 100%;
  padding: 14px;
  font-size: 15px;
  font-weight: 800;
  border-radius: 12px;
}

.download-hint {
  font-size: 12px;
  color: var(--muted, #6d6471);
  text-align: center;
}

body.theme-dark .download-hint,
body.dark-mode .download-hint {
  color: #a89cb0;
}

/* Responsivitas Layar Menengah & HP */
@media (max-width: 960px) {
  .namegen-grid {
    grid-template-columns: 1fr !important;
    gap: 22px !important;
  }

  .studio-tab-btn {
    padding: 10px 14px;
    font-size: 13px;
  }
}

@media (max-width: 540px) {
  .namegen-row-2col {
    grid-template-columns: 1fr !important;
    gap: 12px !important;
  }
  .namegen-form-card,
  .namegen-result-card {
    padding: 18px !important;
    border-radius: 16px !important;
  }
  .ateji-kanji-row {
    grid-template-columns: 1fr !important;
  }
}

/* Safe clearance agar tidak tertutup tombol melayang */
.translator-studio-section {
  padding-bottom: 90px !important;
}

"""

    if namegen_css_pattern.search(content):
        content = namegen_css_pattern.sub(lambda m: new_namegen_css, content)
        css_file.write_text(content, encoding="utf-8")
        print("✓ css/pages/kamus.css berhasil diperbarui dengan layout namegen responsif.")
    else:
        print("! Warning: Pola CSS Generator Nama Jepang di kamus.css tidak cocok.")

if __name__ == "__main__":
    print("=== MEMPERBAIKI TATA LETAK & UI GENERATOR NAMA JEPANG ===")
    update_html()
    update_js()
    update_css()
    print("=== SELESAI ===")
