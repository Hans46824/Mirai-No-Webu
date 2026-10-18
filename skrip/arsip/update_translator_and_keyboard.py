#!/usr/bin/env python3
"""
File: skrip/arsip/update_translator_and_keyboard.py
Fungsi:
 1. Menghapus tombol tukar bahasa manual dan menggantikannya dengan sistem penerjemah adaptif otomatis (auto-detect bahasa Jepang vs Indonesia).
 2. Mendesain ulang tata letak Laptop/Desktop: 2 kolom berdampingan simetris, rapi, lega, dan modern.
 3. Menghapus seksi Contoh Cepat (quick chips).
 4. Membuat Virtual Keyboard melayang yang dapat digeser (draggable) ke mana saja dalam batasan layar (viewport boundaries) dan ukurannya dapat diubah (resizable) dengan batasan min/max yang aman.
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]

def update_kamus_html():
    path = ROOT / "kamus" / "index.html"
    content = path.read_text(encoding="utf-8")

    # 1. Ganti seksi Studio Translator dari awal tab panel translator sampai sebelum panelNameGen
    old_panel_pattern = re.compile(
        r'<!-- TAB PANEL 1: PENERJEMAH & VIRTUAL KEYBOARD -->\s*<div class="studio-tab-panel is-active" id="panelTranslator" data-studio-panel="translator">.*?<!-- TAB PANEL 2: GENERATOR NAMA JEPANG',
        re.DOTALL
    )

    new_panel_html = """<!-- TAB PANEL 1: PENERJEMAH & VIRTUAL KEYBOARD -->
    <div class="studio-tab-panel is-active" id="panelTranslator" data-studio-panel="translator">
        <div class="studio-container">
            <!-- BARIS KONTROL ATAS ADAPTIF: DETEKSI BAHASA OTOMATIS & TOOLBAR -->
            <div class="studio-adaptive-bar">
                <div class="adaptive-direction-badge" id="adaptiveDirectionBadge" title="Arah bahasa terdeteksi otomatis">
                    <span class="badge-icon-sparkle">✨</span>
                    <span class="badge-text" id="adaptiveDirectionText">Deteksi Otomatis (Jepang ⇄ Indonesia)</span>
                </div>
                <div class="studio-toolbar-actions">
                    <button type="button" class="ime-toggle-pill is-active" id="autoRomajiImeBtn" title="Klik untuk menyalakan/mematikan konversi Romaji otomatis">
                        <span class="ime-dot"></span>
                        <span id="imeStatusText">Auto-Romaji: ON ✨</span>
                    </button>
                    <button type="button" class="studio-btn action-keyboard-toggle" id="toggleKeyboardBtn" aria-expanded="false" title="Buka / sembunyikan virtual keyboard layar">
                        <span class="btn-icon">⌨️</span>
                        <span id="keyboardToggleText">Virtual Keyboard</span>
                    </button>
                </div>
            </div>

            <!-- AREA UTAMA: DUAL-PANEL SIMETRIS (DESKTOP: KIRI-KANAN BERDAMPINGAN; HP: STACKED RESPONSIVE) -->
            <div class="studio-box-grid">
                <!-- KOTAK INPUT KETIK (KIRI DI DESKTOP / ATAS DI HP) -->
                <div class="studio-card studio-input-card">
                    <div class="studio-card-head">
                        <div class="card-head-left">
                            <span class="card-badge lang-badge-desktop" id="sourceBadgeDesktop">
                                <span class="badge-flag" id="sourceFlag">🇯🇵</span>
                                <span class="badge-name" id="sourceName">Jepang</span>
                            </span>
                            <button type="button" class="icon-audio-btn" id="listenInputBtn" title="Dengarkan teks yang diketik (Normal)" aria-label="Dengarkan teks ketikan">
                                🔊
                            </button>
                            <button type="button" class="icon-audio-btn btn-audio-slow" id="listenInputSlowBtn" title="Dengarkan teks pelan (Slow-Mo)" aria-label="Dengarkan teks lambat">
                                🐢
                            </button>
                        </div>
                        <div class="card-head-right">
                            <span class="char-count" id="inputCharCount">0 karakter</span>
                            <button type="button" class="mini-clear-btn" id="clearInputBtn" title="Hapus ketikan" aria-label="Hapus teks">
                                🗑️
                            </button>
                        </div>
                    </div>

                    <div class="textarea-wrapper">
                        <textarea id="translatorInput" class="studio-textarea" rows="4" placeholder="Ketik kalimat atau kata dalam bahasa Jepang (かな/漢字/Romaji) atau bahasa Indonesia..."></textarea>
                    </div>

                    <!-- BARIS TOMBOL AKSI INPUT -->
                    <div class="studio-action-row studio-action-input">
                        <div class="action-left">
                            <span class="card-hint-text" id="inputHint">Sistem otomatis mendeteksi bahasa teks input</span>
                        </div>
                        <div class="action-right">
                            <button type="button" class="studio-btn studio-btn-icon" id="copyInputBtn" title="Salin teks input">
                                <span>📋 Salin</span>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- KOTAK OUTPUT TERJEMAHAN (KANAN DI DESKTOP / STRIP MENEMPEL LANGSUNG DI BAWAH INPUT DI HP) -->
                <div class="studio-card studio-output-card">
                    <div class="studio-card-head">
                        <div class="card-head-left">
                            <span class="card-badge output-badge lang-badge-desktop" id="targetBadgeDesktop">
                                <span class="badge-flag" id="targetFlag">🇮🇩</span>
                                <span class="badge-name" id="targetName">Indonesia</span>
                            </span>
                            <button type="button" class="icon-audio-btn primary" id="listenOutputBtn" title="Dengarkan hasil terjemahan (Normal)" aria-label="Dengarkan hasil terjemahan">
                                🔊
                            </button>
                            <button type="button" class="icon-audio-btn btn-audio-slow" id="listenOutputSlowBtn" title="Dengarkan hasil terjemahan pelan (Slow-Mo)" aria-label="Dengarkan hasil terjemahan lambat">
                                🐢
                            </button>
                        </div>
                        <div class="card-head-right">
                            <span class="status-indicator" id="translationStatus">Siap menerjemahkan</span>
                        </div>
                    </div>

                    <div class="output-wrapper">
                        <div id="translatorOutput" class="studio-output-text placeholder">Hasil terjemahan akan otomatis muncul di sini...</div>
                        <div id="translatorRomaji" class="studio-output-romaji" hidden></div>
                    </div>

                    <!-- BARIS TOMBOL AKSI OUTPUT -->
                    <div class="studio-action-row studio-action-output">
                        <div class="action-left">
                            <span class="trans-engine-badge">⚡ Terjemahan Adaptif + Live Sync</span>
                        </div>
                        <div class="action-right">
                            <button type="button" class="studio-btn studio-btn-icon primary" id="copyOutputBtn" title="Salin hasil terjemahan">
                                <span>📋 Salin Hasil</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- PANEL VIRTUAL KEYBOARD JEPANG: FLOATING DRAGGABLE & RESIZABLE -->
            <div class="virtual-keyboard-panel is-collapsed" id="virtualKeyboardPanel" role="region" aria-label="Keyboard Virtual Jepang Keitai 12-Key">
                <div class="kb-floating-drag-bar" id="kbDragHandle" title="Geser keyboard (Tahan &amp; Seret)">
                    <span class="kb-drag-pill"></span>
                </div>
                <div class="keyboard-header" id="kbHeaderDrag" title="Geser keyboard (Tahan &amp; Seret)">
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
                            <button type="button" class="keitai-btn action-key romaji-toggle-key" id="kbToggleRomajiBtn" title="Aktif / Nonaktifkan Auto-Romaji">
                                <span class="keitai-main-char">✨</span>
                                <span class="keitai-sub-chars" id="kbRomajiStatusText">Romaji ON</span>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- RESIZE HANDLE (SUDUT KANAN BAWAH) -->
                <div class="kb-resize-handle" id="kbResizeHandle" title="Ubah ukuran keyboard (Tahan &amp; Tarik)">
                    <svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true">
                        <path d="M10 2L2 10M10 6L6 10M10 10L10 10" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
                    </svg>
                </div>
            </div>
        </div>
    </div>

    <!-- TAB PANEL 2: GENERATOR NAMA JEPANG"""

    if old_panel_pattern.search(content):
        content = old_panel_pattern.sub(new_panel_html, content)
        path.write_text(content, encoding="utf-8")
        print("✓ kamus/index.html berhasil diperbarui dengan layout adaptif dan tanpa contoh cepat/tombol tukar manual.")
    else:
        print("! Warning: Pola tab panel translator di kamus/index.html tidak cocok secara persis.")

def update_translator_js():
    path = ROOT / "js" / "translator.js"
    content = path.read_text(encoding="utf-8")

    # 1. Hapus deklarasi duplikat translateStudioText yang lama di atas KEITAI_GROUPS
    dup_pattern = re.compile(
        r'/\*\*\s*\*\s*Menerjemahkan teks dari Jepang -> Indonesia atau Indonesia -> Jepang\s*\*/\s*async function translateStudioText\(text, direction = "ja-id"\) \{.*?\}\s*(?=// ={5,}\s*// 5\. KEITAI 12-KEY)',
        re.DOTALL
    )
    if dup_pattern.search(content):
        content = dup_pattern.sub("", content)
        print("✓ Duplikat awal translateStudioText berhasil dibersihkan.")

    # 2. Perbarui initStudioTranslator() untuk mendukung deteksi bahasa adaptif otomatis dan keyboard draggable/resizable
    init_studio_pattern = re.compile(
        r'// ={5,}\s*// 6\. KONTROLER UTAMA STUDIO TRANSLATOR & KEITAI 12-KEY KEYBOARD\s*// ={5,}\s*function initStudioTranslator\(\) \{.*?(?=// ={5,}\s*// 7\. EXPORT GLOBAL TRANSLATOR)',
        re.DOTALL
    )

    new_init_studio = """// =========================================================================
// 6. KONTROLER UTAMA STUDIO TRANSLATOR & KEITAI 12-KEY KEYBOARD
// =========================================================================
function initStudioTranslator() {
  const studio = document.getElementById('studio-terjemahan');
  if (!studio) return;

  const adaptiveDirectionBadge = document.getElementById('adaptiveDirectionBadge');
  const adaptiveDirectionText = document.getElementById('adaptiveDirectionText');

  const sourceFlag = document.getElementById('sourceFlag');
  const sourceName = document.getElementById('sourceName');
  const targetFlag = document.getElementById('targetFlag');
  const targetName = document.getElementById('targetName');

  const textarea = document.getElementById('translatorInput');
  const outputEl = document.getElementById('translatorOutput');
  const romajiEl = document.getElementById('translatorRomaji');
  const statusEl = document.getElementById('translationStatus');
  const inputHint = document.getElementById('inputHint');
  const charCount = document.getElementById('inputCharCount');

  const listenInputBtn = document.getElementById('listenInputBtn');
  const listenInputSlowBtn = document.getElementById('listenInputSlowBtn');
  const listenOutputBtn = document.getElementById('listenOutputBtn');
  const listenOutputSlowBtn = document.getElementById('listenOutputSlowBtn');
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
  const kbToggleRomajiBtn = document.getElementById('kbToggleRomajiBtn');
  const kbRomajiStatusText = document.getElementById('kbRomajiStatusText');

  const kbDakutenBtn = document.getElementById('kbDakutenBtn');
  const kbSpaceBtn = document.getElementById('kbSpaceBtn');
  const kbBackspaceBtn = document.getElementById('kbBackspaceBtn');
  const kbEnterBtn = document.getElementById('kbEnterBtn');

  let activeDirection = 'ja-id';
  let activeScript = 'hiragana';
  let isAutoRomajiOn = true;
  let translateDebounceTimer = null;

  // Keitai multi-tap state
  let lastTapGroup = null;
  let lastTapIndex = 0;
  let tapCycleTimer = null;
  let currentActiveBubble = null;

  function removeAllKeitaiPopups() {
    document.querySelectorAll('.keitai-popup, .keitai-popup-bubble').forEach((el) => {
      el.hidden = true;
      el.replaceChildren();
      if (el.classList.contains('keitai-popup')) {
        el.remove();
      }
    });
    if (currentActiveBubble) {
      currentActiveBubble.hidden = true;
      currentActiveBubble.replaceChildren();
      currentActiveBubble = null;
    }
  }

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
    removeAllKeitaiPopups();
  }

  // Handle Keitai Key Tap (Multi-tap cycle + mini popup bubble)
  function handleKeitaiKeyTap(groupKey, wrapperEl) {
    applyMobileKeyboardGuard();
    const groupData = KEITAI_GROUPS[activeScript]?.[groupKey] || KEITAI_GROUPS.hiragana[groupKey];
    if (!groupData) return;

    const chars = groupData.chars;
    const bubbleEl = wrapperEl ? wrapperEl.querySelector('.keitai-popup-bubble') : null;

    if (lastTapGroup === groupKey) {
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

    if (bubbleEl) {
      removeAllKeitaiPopups();
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
          removeAllKeitaiPopups();
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

  // Toggle Virtual Keyboard Panel (Floating Window)
  function setKeyboardCollapsed(collapsed) {
    if (!keyboardPanel) return;
    removeAllKeitaiPopups();
    keyboardPanel.classList.toggle('is-collapsed', collapsed);
    keyboardPanel.classList.toggle('is-open', !collapsed);
    if (toggleKeyboardBtn) {
      toggleKeyboardBtn.setAttribute('aria-expanded', String(!collapsed));
    }
    if (keyboardToggleText) {
      keyboardToggleText.textContent = collapsed
        ? 'Virtual Keyboard'
        : 'Tutup Keyboard ▴';
    }
    applyMobileKeyboardGuard();
    if (!collapsed) {
      updateKeitaiKeyLabels();
      if (typeof window.ensureKeyboardInView === 'function') {
        window.ensureKeyboardInView();
      }
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
      removeAllKeitaiPopups();
      setKeyboardCollapsed(true);
      window.MiraiSound?.playClickIfIdle();
    });
  }

  document.addEventListener('click', (e) => {
    if (!e.target.closest('.keitai-key-wrapper') && !e.target.closest('.keitai-popup') && !e.target.closest('.keitai-popup-bubble')) {
      removeAllKeitaiPopups();
    }
  });

  function setScriptMode(mode) {
    activeScript = mode === 'katakana' ? 'katakana' : 'hiragana';
    if (kbScriptHiraganaBtn) kbScriptHiraganaBtn.classList.toggle('is-active', activeScript === 'hiragana');
    if (kbScriptKatakanaBtn) kbScriptKatakanaBtn.classList.toggle('is-active', activeScript === 'katakana');
    updateKeitaiKeyLabels();
    applyMobileKeyboardGuard();
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

  function updateRomajiToggleState() {
    if (autoRomajiImeBtn) {
      autoRomajiImeBtn.classList.toggle('is-active', isAutoRomajiOn);
      autoRomajiImeBtn.classList.toggle('is-off', !isAutoRomajiOn);
    }
    if (imeStatusText) {
      imeStatusText.textContent = isAutoRomajiOn ? 'Auto-Romaji: ON ✨' : 'Auto-Romaji: OFF';
    }
    if (kbToggleRomajiBtn) {
      kbToggleRomajiBtn.classList.toggle('is-active', isAutoRomajiOn);
    }
    if (kbRomajiStatusText) {
      kbRomajiStatusText.textContent = isAutoRomajiOn ? 'Romaji ON' : 'Romaji OFF';
    }
  }

  if (autoRomajiImeBtn) {
    autoRomajiImeBtn.addEventListener('click', () => {
      isAutoRomajiOn = !isAutoRomajiOn;
      updateRomajiToggleState();
      window.MiraiSound?.playClickIfIdle();
    });
  }

  if (kbToggleRomajiBtn) {
    kbToggleRomajiBtn.addEventListener('click', () => {
      isAutoRomajiOn = !isAutoRomajiOn;
      updateRomajiToggleState();
      window.MiraiSound?.playClickIfIdle();
    });
  }

  // =========================================================================
  // SISTEM PENDETEKSI BAHASA ADAPTIF OTOMATIS (JEPANG vs INDONESIA)
  // =========================================================================
  const COMMON_JA_ROMAJI = new Set([
    'watashi', 'boku', 'ore', 'anata', 'kore', 'sore', 'are', 'dore',
    'koko', 'soko', 'asoko', 'doko', 'nani', 'nan', 'dare', 'itsu',
    'doushite', 'naze', 'arigatou', 'arigato', 'ohayou', 'ohayo',
    'konnichiwa', 'konbanwa', 'sayounara', 'sayonara', 'oyasumi',
    'sumimasen', 'gomen', 'gomenasai', 'itadakimasu', 'gochisousama',
    'hajimemashite', 'yoroshiku', 'desu', 'masu', 'da', 'ne', 'yo',
    'suki', 'kirai', 'kawaii', 'sugoi', 'kakkoii', 'oishii', 'samui',
    'atsui', 'hayai', 'osoi', 'ii', 'warui', 'chotto', 'motto',
    'nihon', 'nihongo', 'tokyo', 'sensei', 'gakusei', 'tomodachi'
  ]);

  const COMMON_INDONESIAN_WORDS = new Set([
    'saya', 'aku', 'kamu', 'anda', 'dia', 'mereka', 'kita', 'kami',
    'apa', 'siapa', 'kapan', 'dimana', 'bagaimana', 'kenapa', 'mengapa',
    'ini', 'itu', 'di', 'ke', 'dari', 'yang', 'dan', 'atau', 'tapi', 'tetapi',
    'karena', 'untuk', 'dengan', 'pada', 'adalah', 'bisa', 'dapat', 'mau',
    'ingin', 'akan', 'sudah', 'telah', 'sedang', 'belum', 'tidak', 'bukan', 'jangan',
    'halo', 'selamat', 'pagi', 'siang', 'sore', 'malam', 'terima', 'kasih',
    'sama', 'tolong', 'maaf', 'permisi', 'senang', 'bertemu', 'belajar',
    'makan', 'minum', 'pergi', 'datang', 'pulang', 'buku', 'rumah', 'sekolah', 'teman'
  ]);

  function detectLanguage(text) {
    if (!text || !text.trim()) return null;

    // 1. Cek aksara Jepang asli: Kanji, Hiragana, Katakana, dan Tanda Baca Jepang
    const JAPANESE_CHAR_REGEX = /[\\u4E00-\\u9FAF\\u3040-\\u309F\\u30A0-\\u30FF\\u31F0-\\u31FF\\uFF65-\\uFF9F]/;
    if (JAPANESE_CHAR_REGEX.test(text)) {
      return 'ja';
    }

    // 2. Cek kamus lokal langsung
    const clean = text.toLowerCase().trim();
    if (jaToIdDictionary[clean]) return 'ja';
    if (idToJaDictionary[clean]) return 'id';

    // 3. Pencocokan token kata Romaji Jepang vs Bahasa Indonesia
    const words = clean.split(/[\\s,.\\-!?;:"'()]+/).filter(Boolean);
    let jaHits = 0;
    let idHits = 0;

    for (const w of words) {
      if (COMMON_JA_ROMAJI.has(w) || jaToIdDictionary[w]) jaHits++;
      if (COMMON_INDONESIAN_WORDS.has(w) || idToJaDictionary[w]) idHits++;
    }

    if (jaHits > idHits) return 'ja';
    if (idHits > jaHits) return 'id';

    // Default jika huruf latin tanpa kata kunci khusus: anggap bahasa Indonesia
    return 'id';
  }

  function setDirectionUI(direction) {
    activeDirection = direction;
    const isJa = activeDirection === 'ja-id';

    if (sourceFlag) sourceFlag.textContent = isJa ? '🇯🇵' : '🇮🇩';
    if (sourceName) sourceName.textContent = isJa ? 'Jepang (Input)' : 'Indonesia (Input)';
    if (targetFlag) targetFlag.textContent = isJa ? '🇮🇩' : '🇯🇵';
    if (targetName) targetName.textContent = isJa ? 'Indonesia (Hasil)' : 'Jepang (Hasil)';

    if (adaptiveDirectionText) {
      if (!textarea.value.trim()) {
        adaptiveDirectionText.textContent = 'Deteksi Otomatis (Jepang ⇄ Indonesia)';
      } else {
        adaptiveDirectionText.textContent = isJa
          ? '🇯🇵 Jepang ➔ 🇮🇩 Indonesia (Otomatis)'
          : '🇮🇩 Indonesia ➔ 🇯🇵 Jepang (Otomatis)';
      }
    }

    if (inputHint) {
      if (!textarea.value.trim()) {
        inputHint.textContent = 'Sistem otomatis mendeteksi bahasa teks input';
      } else {
        inputHint.textContent = isJa ? '✓ Aksara Jepang terdeteksi' : '✓ Bahasa Indonesia terdeteksi';
      }
    }
  }

  // Real-time Input Update dengan Auto-Detect Bahasa & Debounce 220ms
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
      setDirectionUI('ja-id');
      return;
    }

    // Auto-detect bahasa input pengguna
    const detectedLang = detectLanguage(text);
    const targetDirection = (detectedLang === 'ja') ? 'ja-id' : 'id-ja';
    if (activeDirection !== targetDirection) {
      setDirectionUI(targetDirection);
    } else if (adaptiveDirectionText) {
      adaptiveDirectionText.textContent = (targetDirection === 'ja-id')
        ? '🇯🇵 Jepang ➔ 🇮🇩 Indonesia (Otomatis)'
        : '🇮🇩 Indonesia ➔ 🇯🇵 Jepang (Otomatis)';
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
    }, 220);
  }

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
    if (isAutoRomajiOn) {
      applyRealtimeImeConversion();
    }
    triggerInputUpdate();
  });

  textarea.addEventListener('focus', () => {
    applyMobileKeyboardGuard();
  });

  // Audio Buttons (Adaptif sesuai bahasa terdeteksi)
  if (listenInputBtn) {
    listenInputBtn.addEventListener('click', () => {
      const text = textarea.value.trim();
      if (!text) return;
      window.speakText(text, activeDirection === 'ja-id' ? 'ja-JP' : 'id-ID', false);
    });
  }
  if (listenInputSlowBtn) {
    listenInputSlowBtn.addEventListener('click', () => {
      const text = textarea.value.trim();
      if (!text) return;
      window.speakText(text, activeDirection === 'ja-id' ? 'ja-JP' : 'id-ID', true);
    });
  }

  if (listenOutputBtn) {
    listenOutputBtn.addEventListener('click', () => {
      if (outputEl.classList.contains('placeholder')) return;
      const text = outputEl.textContent.trim();
      if (!text) return;
      window.speakText(text, activeDirection === 'ja-id' ? 'id-ID' : 'ja-JP', false);
    });
  }
  if (listenOutputSlowBtn) {
    listenOutputSlowBtn.addEventListener('click', () => {
      if (outputEl.classList.contains('placeholder')) return;
      const text = outputEl.textContent.trim();
      if (!text) return;
      window.speakText(text, activeDirection === 'ja-id' ? 'id-ID' : 'ja-JP', true);
    });
  }

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
  initKeyboardDragAndResize();
}

// =========================================================================
// FITUR KEYBOARD MELAYANG: DRAGGABLE & RESIZABLE DENGAN VIEWPORT BOUNDARIES
// =========================================================================
function initKeyboardDragAndResize() {
  const kb = document.getElementById('virtualKeyboardPanel');
  const dragHandle = document.getElementById('kbDragHandle');
  const headerHandle = document.getElementById('kbHeaderDrag') || document.querySelector('.keyboard-header');
  const resizeHandle = document.getElementById('kbResizeHandle');
  if (!kb) return;

  let isDragging = false;
  let isResizing = false;
  let startX = 0, startY = 0;
  let startLeft = 0, startTop = 0;
  let startWidth = 0, startHeight = 0;
  let hasCustomPosition = false;

  function clampPosition(left, top) {
    const pad = 8;
    const rect = kb.getBoundingClientRect();
    const minX = pad;
    const maxX = Math.max(pad, window.innerWidth - rect.width - pad);
    const minY = pad;
    const maxY = Math.max(pad, window.innerHeight - rect.height - pad);

    const clampedX = Math.max(minX, Math.min(left, maxX));
    const clampedY = Math.max(minY, Math.min(top, maxY));
    return { x: clampedX, y: clampedY };
  }

  function clampSize(w, h) {
    const minW = Math.min(310, window.innerWidth - 16);
    const maxW = Math.min(760, window.innerWidth - 16);
    const minH = 210;
    const maxH = Math.min(680, window.innerHeight - 20);

    const clampedW = Math.max(minW, Math.min(w, maxW));
    const clampedH = Math.max(minH, Math.min(h, maxH));
    return { w: clampedW, h: clampedH };
  }

  function onDragStart(e) {
    if (e.target.closest('button') || e.target.closest('.kb-mode-pill-group')) return;
    isDragging = true;
    kb.classList.add('is-dragging');

    const clientX = e.clientX ?? (e.touches && e.touches[0].clientX);
    const clientY = e.clientY ?? (e.touches && e.touches[0].clientY);
    startX = clientX;
    startY = clientY;

    const rect = kb.getBoundingClientRect();
    startLeft = rect.left;
    startTop = rect.top;

    kb.style.transform = 'none';
    kb.style.left = `${startLeft}px`;
    kb.style.top = `${startTop}px`;
    kb.style.bottom = 'auto';
    hasCustomPosition = true;

    window.addEventListener('pointermove', onDragMove, { passive: false });
    window.addEventListener('pointerup', onDragEnd);
    window.addEventListener('touchmove', onDragMove, { passive: false });
    window.addEventListener('touchend', onDragEnd);
    e.preventDefault();
  }

  function onDragMove(e) {
    if (!isDragging) return;
    const clientX = e.clientX ?? (e.touches && e.touches[0].clientX);
    const clientY = e.clientY ?? (e.touches && e.touches[0].clientY);
    const dx = clientX - startX;
    const dy = clientY - startY;

    const pos = clampPosition(startLeft + dx, startTop + dy);
    kb.style.left = `${pos.x}px`;
    kb.style.top = `${pos.y}px`;
    if (e.cancelable) e.preventDefault();
  }

  function onDragEnd() {
    if (!isDragging) return;
    isDragging = false;
    kb.classList.remove('is-dragging');
    window.removeEventListener('pointermove', onDragMove);
    window.removeEventListener('pointerup', onDragEnd);
    window.removeEventListener('touchmove', onDragMove);
    window.removeEventListener('touchend', onDragEnd);
  }

  if (dragHandle) {
    dragHandle.addEventListener('pointerdown', onDragStart);
    dragHandle.addEventListener('touchstart', onDragStart, { passive: false });
  }
  if (headerHandle) {
    headerHandle.addEventListener('pointerdown', onDragStart);
    headerHandle.addEventListener('touchstart', onDragStart, { passive: false });
  }

  function onResizeStart(e) {
    isResizing = true;
    kb.classList.add('is-resizing');

    const clientX = e.clientX ?? (e.touches && e.touches[0].clientX);
    const clientY = e.clientY ?? (e.touches && e.touches[0].clientY);
    startX = clientX;
    startY = clientY;

    const rect = kb.getBoundingClientRect();
    startWidth = rect.width;
    startHeight = rect.height;

    if (!hasCustomPosition) {
      kb.style.transform = 'none';
      kb.style.left = `${rect.left}px`;
      kb.style.top = `${rect.top}px`;
      kb.style.bottom = 'auto';
      hasCustomPosition = true;
    }

    window.addEventListener('pointermove', onResizeMove, { passive: false });
    window.addEventListener('pointerup', onResizeEnd);
    window.addEventListener('touchmove', onResizeMove, { passive: false });
    window.addEventListener('touchend', onResizeEnd);
    e.preventDefault();
    e.stopPropagation();
  }

  function onResizeMove(e) {
    if (!isResizing) return;
    const clientX = e.clientX ?? (e.touches && e.touches[0].clientX);
    const clientY = e.clientY ?? (e.touches && e.touches[0].clientY);
    const dw = clientX - startX;
    const dh = clientY - startY;

    const size = clampSize(startWidth + dw, startHeight + dh);
    kb.style.width = `${size.w}px`;
    kb.style.height = `${size.h}px`;

    const rect = kb.getBoundingClientRect();
    const pos = clampPosition(rect.left, rect.top);
    kb.style.left = `${pos.x}px`;
    kb.style.top = `${pos.y}px`;

    if (e.cancelable) e.preventDefault();
  }

  function onResizeEnd() {
    if (!isResizing) return;
    isResizing = false;
    kb.classList.remove('is-resizing');
    window.removeEventListener('pointermove', onResizeMove);
    window.removeEventListener('pointerup', onResizeEnd);
    window.removeEventListener('touchmove', onResizeMove);
    window.removeEventListener('touchend', onResizeEnd);
  }

  if (resizeHandle) {
    resizeHandle.addEventListener('pointerdown', onResizeStart);
    resizeHandle.addEventListener('touchstart', onResizeStart, { passive: false });
  }

  window.addEventListener('resize', () => {
    if (!kb.classList.contains('is-collapsed') && hasCustomPosition) {
      const rect = kb.getBoundingClientRect();
      const pos = clampPosition(rect.left, rect.top);
      kb.style.left = `${pos.x}px`;
      kb.style.top = `${pos.y}px`;
      const size = clampSize(rect.width, rect.height);
      kb.style.width = `${size.w}px`;
      kb.style.height = `${size.h}px`;
    }
  });

  window.ensureKeyboardInView = function() {
    if (!hasCustomPosition) {
      const rect = kb.getBoundingClientRect();
      const targetLeft = Math.max(8, (window.innerWidth - rect.width) / 2);
      const targetTop = Math.max(8, window.innerHeight - rect.height - 24);
      kb.style.transform = 'none';
      kb.style.left = `${targetLeft}px`;
      kb.style.top = `${targetTop}px`;
      kb.style.bottom = 'auto';
      hasCustomPosition = true;
    } else {
      const rect = kb.getBoundingClientRect();
      const pos = clampPosition(rect.left, rect.top);
      kb.style.left = `${pos.x}px`;
      kb.style.top = `${pos.y}px`;
    }
  };
}
"""

    if init_studio_pattern.search(content):
        content = init_studio_pattern.sub(lambda m: new_init_studio, content)
        path.write_text(content, encoding="utf-8")
        print("✓ js/translator.js berhasil diperbarui dengan pendeteksi bahasa adaptif & keyboard draggable/resizable.")
    else:
        print("! Warning: Pola initStudioTranslator di js/translator.js tidak cocok.")

def update_kamus_css():
    path = ROOT / "css" / "pages" / "kamus.css"
    content = path.read_text(encoding="utf-8")

    # CSS tambahan untuk Adaptive Bar, Dual-Panel Desktop Redesign, dan Draggable/Resizable Floating Keyboard
    custom_css_addon = """
/* ==========================================================================
   STUDIO TRANSLATOR ADAPTIF & DESKTOP REDESIGN (CLEAN & COMPACT)
   ========================================================================== */
.studio-adaptive-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin: 22px 0 18px;
  flex-wrap: wrap;
}

.adaptive-direction-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 18px;
  background: #ffffff;
  border: 1.5px solid var(--pink-border, #fcd1e5);
  border-radius: 999px;
  font-size: 13px;
  font-weight: 800;
  color: var(--pink, #e91e63);
  box-shadow: 0 4px 16px rgba(72, 32, 52, 0.05);
  transition: all 0.25s ease;
  user-select: none;
}

body.theme-dark .adaptive-direction-badge,
body.dark-mode .adaptive-direction-badge {
  background: #1c1724;
  border-color: rgba(233, 30, 99, 0.35);
  color: #ff6090;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
}

.studio-toolbar-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

/* Dual Panel Grid: Desktop 2 Kolom Seimbang */
.studio-box-grid {
  display: grid !important;
  grid-template-columns: 1fr 1fr !important;
  gap: 24px !important;
  align-items: stretch !important;
  margin-bottom: 24px !important;
}

.studio-card {
  background: #ffffff;
  border: 1.5px solid var(--pink-border, #fcd1e5);
  border-radius: 20px;
  padding: 22px;
  box-shadow: 0 8px 28px rgba(72, 32, 52, 0.05);
  display: flex;
  flex-direction: column;
  min-height: 290px;
  box-sizing: border-box;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.studio-output-card {
  background: #fffcfd;
}

body.theme-dark .studio-output-card,
body.dark-mode .studio-output-card {
  background: #18141f;
}

.studio-textarea {
  width: 100%;
  min-height: 140px;
  border: none;
  outline: none;
  resize: vertical;
  font-size: 16px;
  line-height: 1.6;
  font-family: inherit;
  color: var(--ink, #201c26);
  background: transparent;
  box-sizing: border-box;
}

body.theme-dark .studio-textarea,
body.dark-mode .studio-textarea {
  color: #f0eef5;
}

.studio-output-text {
  min-height: 140px;
  font-size: 16px;
  line-height: 1.6;
  color: var(--ink, #201c26);
  word-break: break-word;
  box-sizing: border-box;
}

body.theme-dark .studio-output-text,
body.dark-mode .studio-output-text {
  color: #f0eef5;
}

/* Sembunyikan elemen lama tombol tukar & seksi contoh cepat */
.studio-swap-column,
.studio-mobile-lang-bar,
.quick-examples-wrap,
#panelTranslator .quick-chips-scroll,
#panelTranslator .quick-chip {
  display: none !important;
}

/* ==========================================================================
   KEYBOARD MELAYANG: DRAGGABLE & RESIZABLE DENGAN LIMIT BOUNDARIES
   ========================================================================== */
.virtual-keyboard-panel {
  position: fixed !important;
  z-index: 99999 !important;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  width: 440px;
  min-width: 310px;
  max-width: min(740px, 96vw);
  min-height: 220px;
  max-height: min(680px, 85vh);
  background: rgba(255, 255, 255, 0.98) !important;
  backdrop-filter: blur(20px) !important;
  -webkit-backdrop-filter: blur(20px) !important;
  border: 1.5px solid var(--pink-border, #f4bfd3) !important;
  border-radius: 20px !important;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.22), 0 2px 14px rgba(233, 30, 99, 0.15) !important;
  padding: 8px 14px 14px !important;
  box-sizing: border-box !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 8px !important;
  user-select: none;
  touch-action: none;
}

body.theme-dark .virtual-keyboard-panel,
body.dark-mode .virtual-keyboard-panel {
  background: rgba(24, 19, 30, 0.98) !important;
  border-color: rgba(233, 30, 99, 0.35) !important;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.55), 0 2px 14px rgba(233, 30, 99, 0.25) !important;
}

.virtual-keyboard-panel.is-collapsed {
  display: none !important;
}

.virtual-keyboard-panel.is-dragging {
  cursor: grabbing !important;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.32), 0 4px 20px rgba(233, 30, 99, 0.25) !important;
}

.kb-floating-drag-bar {
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
  padding: 4px 0 6px !important;
  cursor: grab !important;
  touch-action: none !important;
}

.kb-floating-drag-bar:active,
.virtual-keyboard-panel.is-dragging .kb-floating-drag-bar {
  cursor: grabbing !important;
}

.kb-drag-pill {
  width: 48px !important;
  height: 5px !important;
  border-radius: 99px !important;
  background: rgba(233, 30, 99, 0.35) !important;
  transition: background 0.2s ease, width 0.2s ease;
}

.kb-floating-drag-bar:hover .kb-drag-pill {
  background: var(--pink, #e91e63) !important;
  width: 56px !important;
}

.keyboard-header {
  cursor: grab;
  touch-action: none;
}

.keyboard-header:active,
.virtual-keyboard-panel.is-dragging .keyboard-header {
  cursor: grabbing;
}

.keyboard-body {
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow-y: auto;
}

.keitai-12key-grid {
  display: grid !important;
  grid-template-columns: repeat(4, 1fr) !important;
  gap: 7px !important;
  width: 100% !important;
  box-sizing: border-box !important;
}

.keitai-btn {
  width: 100% !important;
  min-height: 48px !important;
  height: 100% !important;
  border-radius: 12px !important;
}

.kb-resize-handle {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 20px;
  height: 20px;
  cursor: nwse-resize;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(233, 30, 99, 0.45);
  touch-action: none;
  z-index: 10;
}

.kb-resize-handle:hover,
.virtual-keyboard-panel.is-resizing .kb-resize-handle {
  color: var(--pink, #e91e63);
}

@media (max-width: 850px) {
  .studio-box-grid {
    grid-template-columns: 1fr !important;
    gap: 14px !important;
  }
  .studio-card {
    min-height: auto;
    padding: 16px;
    border-radius: 16px;
  }
  .studio-textarea {
    min-height: 80px;
    font-size: 15px;
  }
  .studio-output-text {
    min-height: 60px;
    font-size: 15px;
  }
}
"""

    if "/* STUDIO TRANSLATOR ADAPTIF & DESKTOP REDESIGN" not in content:
        content = content.rstrip() + "\n" + custom_css_addon
        path.write_text(content, encoding="utf-8")
        print("✓ css/pages/kamus.css berhasil diperbarui dengan gaya adaptif, laptop layout, dan keyboard resize/drag.")
    else:
        # Perbarui blok CSS jika sudah pernah ada
        pattern = re.compile(r'/\* =+\s*STUDIO TRANSLATOR ADAPTIF & DESKTOP REDESIGN.*?$', re.DOTALL)
        content = pattern.sub(lambda m: custom_css_addon.strip(), content)
        path.write_text(content, encoding="utf-8")
        print("✓ css/pages/kamus.css gaya adaptif berhasil dimutakhirkan.")

if __name__ == "__main__":
    print("=== MEMPERBARUI PENERJEMAH ADAPTIF & KEYBOARD MELAYANG ===")
    update_kamus_html()
    update_translator_js()
    update_kamus_css()
    print("=== SELESAI ===")
