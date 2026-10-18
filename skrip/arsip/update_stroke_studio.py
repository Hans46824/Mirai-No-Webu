#!/usr/bin/env python3
"""
File: skrip/arsip/update_stroke_studio.py
Fungsi:
 1. Rename 'Urutan Goresan' menjadi 'Goresan' di tombol melayang (#quickStrokeBtn), heading kamus, dan kanji/kana.
 2. Mentransformasikan pemutar goresan menjadi Studio Goresan Interaktif 3 Kotak (Trio Panel):
    - Kotak 1: Acuan Resmi Goresan (Animasi & langkah standar)
    - Kotak 2: Kanvas Tulis Mandiri (Interaktif sentuh/mouse, undo, clear, panduan samar, warna pena)
    - Kotak 3: Hasil & Putar Otomatis (Menampilkan goresan user + animasi resmi yang otomatis berputar)
 3. Memperbagus desain dan peletakan 'Lapor Goresan Salah' menjadi tombol pill modern yang elegan.
 4. Tata letak responsif desktop (3 kolom seimbang), tablet (2 kolom), dan mobile (stacked / tabbed).
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]

def update_rename():
    # 1. Update kamus/index.html
    html_file = ROOT / "kamus" / "index.html"
    content = html_file.read_text(encoding="utf-8")
    content = content.replace(
        '<span class="quick-stroke-text">Urutan Goresan</span>',
        '<span class="quick-stroke-text">Goresan</span>'
    )
    content = content.replace(
        'aria-label="Geser ke Urutan Goresan" title="Geser ke Urutan Goresan"',
        'aria-label="Geser ke Goresan" title="Geser ke Goresan"'
    )
    html_file.write_text(content, encoding="utf-8")
    print("✓ kamus/index.html: quickStrokeBtn di-rename menjadi 'Goresan'.")

    # 2. Update js/kanji.js
    kanji_file = ROOT / "js" / "kanji.js"
    k_content = kanji_file.read_text(encoding="utf-8")
    k_content = k_content.replace(
        '<span class="quick-stroke-text">Urutan Goresan</span>',
        '<span class="quick-stroke-text">Goresan</span>'
    )
    k_content = k_content.replace(
        'btn.setAttribute("aria-label", "Geser ke Urutan Goresan");\n  btn.setAttribute("title", "Geser ke Urutan Goresan");',
        'btn.setAttribute("aria-label", "Geser ke Goresan");\n  btn.setAttribute("title", "Geser ke Goresan");'
    )
    k_content = k_content.replace(
        '<h4>Urutan Menulis (KanjiVG)</h4>',
        '<h4>Goresan Karakter (KanjiVG)</h4>'
    )
    kanji_file.write_text(k_content, encoding="utf-8")
    print("✓ js/kanji.js: quickStrokeBtn dan heading di-rename menjadi 'Goresan'.")

    # 3. Update js/kana.js
    kana_file = ROOT / "js" / "kana.js"
    kana_content = kana_file.read_text(encoding="utf-8")
    kana_content = kana_content.replace(
        '<h3>Urutan Menulis (${item.strokes} Goresan)</h3>',
        '<h3>Goresan Karakter (${item.strokes} Goresan)</h3>'
    )
    kana_file.write_text(kana_content, encoding="utf-8")
    print("✓ js/kana.js: heading di-rename menjadi 'Goresan Karakter'.")

def update_stroke_js():
    stroke_file = ROOT / "js" / "stroke.js"
    content = stroke_file.read_text(encoding="utf-8")

    # Ganti fungsi setupPlayerWithRecords untuk mendukung 3 Kotak Interaktif
    # Cari awal setupPlayerWithRecords sampai akhir blok internalController
    old_setup_pattern = re.compile(
        r'function setupPlayerWithRecords\(records\) \{.*?internalController = \{.*?host\._miraiStrokeController = internalController;\s*\}',
        re.DOTALL
    )

    new_setup_code = """function setupPlayerWithRecords(records) {
  if (destroyed || !host) return;

  // Validasi ketersediaan data untuk semua karakter
  const hasAllValidRecords = records.length > 0 && records.every((rec) => rec && isValidStrokeRecord(rec));
  if (!hasAllValidRecords) {
    renderUnavailableState();
    return;
  }

  // Hitung total goresan asli tanpa memalsukan
  const totalStrokes = records.reduce((sum, rec) => sum + rec.paths.length, 0);
  if (totalStrokes === 0) {
    renderUnavailableState();
    return;
  }

  // Buat daftar thumbnail goresan per langkah progresif
  const flattenedStrokes = [];
  records.forEach((rec, cIdx) => {
    rec.paths.forEach((d, pIdx) => {
      flattenedStrokes.push({
        charIdx: cIdx,
        pathIdx: pIdx,
        paths: rec.paths,
        d: d
      });
    });
  });

  const strokeThumbsHtml = flattenedStrokes.map((item, index) => {
    const prevPaths = item.paths.slice(0, item.pathIdx);
    const prevSvg = prevPaths.map((p) => `<path d="${p}" class="step-thumb-prev"></path>`).join("");
    const currentSvg = `<path d="${item.d}" class="step-thumb-current"></path>`;

    return `<li class="stroke-step-thumb" data-stroke-step="${index}" title="Goresan ke-${index + 1}">` +
      `<span class="step-thumb-badge">${index + 1}</span>` +
      `<svg class="step-thumb-svg" viewBox="-8 -8 125 125" aria-hidden="true">` +
      `<line x1="5" y1="54.5" x2="104" y2="54.5" class="step-thumb-grid"></line>` +
      `<line x1="54.5" y1="5" x2="54.5" y2="104" class="step-thumb-grid"></line>` +
      `${prevSvg}` +
      `${currentSvg}` +
      `</svg>` +
      `</li>`;
  }).join("");

  // Catatan varian gaya buku teks atau alasan override
  const notes = records
    .filter((r) => r && (r.note || r.variant))
    .map((r) => r.note || (r.variant === 'kyokasho' ? 'Gaya buku teks resmi (kyōkasho).' : `Varian: ${r.variant}`));
  const noteHtml = notes.length > 0 ? `
    <div class="stroke-variant-note" role="note" aria-label="Catatan varian karakter">
      <span class="stroke-note-icon" aria-hidden="true">💡</span>
      <span class="stroke-note-text">${notes.join(" • ")}</span>
    </div>
  ` : "";

  // Tombol lapor goresan salah membuka GForm dengan parameter URL prefilled
  const firstChar = characters[0] || kanaString;
  const cp = firstChar.codePointAt(0) || 0;
  const hexCode = cp.toString(16).padStart(5, "0").toUpperCase();
  const prefillParam = encodeURIComponent(`Laporan Goresan: ${kanaString} (U+${hexCode})`);
  const reportUrl = `https://forms.gle/dFPRM842xxKq5YMt9?usp=pp_url&entry.lapor=${prefillParam}`;
  const reportBtnHtml = `
    <a href="${reportUrl}" target="_blank" rel="noopener noreferrer" class="stroke-report-pill stroke-report-link" title="Buka formulir untuk melaporkan goresan ${kanaString} (U+${hexCode})">
      <span class="report-icon">🚩</span>
      <span class="report-text">Lapor goresan salah</span>
    </a>
  `;

  // Render Kerangka Studio Goresan Interaktif 3 Kotak (Trio Panel)
  host.innerHTML = `
    <div class="stroke-studio-container">
      <div class="stroke-studio-header">
        <div class="stroke-studio-title-wrap">
          <span class="stroke-studio-badge">✨ Studio Goresan Interaktif</span>
          <span class="stroke-studio-sub">Amati acuan, latih goresan mandiri, dan bandingkan secara langsung</span>
        </div>
        <div class="stroke-mode-tabs" role="tablist">
          <button type="button" class="stroke-mode-btn is-active" data-stroke-mode="all">Semua Kotak</button>
          <button type="button" class="stroke-mode-btn" data-stroke-mode="official">1. Acuan</button>
          <button type="button" class="stroke-mode-btn" data-stroke-mode="practice">2. Tulis</button>
          <button type="button" class="stroke-mode-btn" data-stroke-mode="compare">3. Bandingkan</button>
        </div>
      </div>

      <!-- GRID 3 KOTAK UTAMA -->
      <div class="stroke-studio-trio">
        
        <!-- KOTAK 1: ACUAN RESMI (ANIMASI & URUTAN STANDAR) -->
        <div class="stroke-panel-card stroke-official-card" data-panel-box="official">
          <div class="panel-card-head">
            <span class="panel-card-title">
              <span class="panel-num">1</span>
              <strong>Acuan Resmi</strong>
            </span>
            <span class="panel-card-tag">Standar KanjiVG</span>
          </div>
          <div class="stroke-stage stroke-thick" aria-label="Animasi urutan menulis ${kanaString}"></div>
          <div class="stroke-status">Goresan <b data-stroke-number>1</b> dari ${totalStrokes}</div>
          <ol class="stroke-order" aria-label="Urutan visual goresan">${strokeThumbsHtml}</ol>
          <div class="stroke-controls" role="toolbar" aria-label="Kontrol animasi goresan">
            <button type="button" data-stroke-prev aria-label="Langkah sebelumnya" title="Langkah sebelumnya">⏮</button>
            <button type="button" data-stroke-play aria-label="Putar animasi goresan">PUTAR ▶</button>
            <button type="button" data-stroke-next aria-label="Langkah berikutnya" title="Langkah berikutnya">⏭</button>
            <button type="button" data-stroke-replay aria-label="Ulangi dari awal" title="Ulangi dari awal">🔄</button>
            ${showClearControl ? `<button type="button" data-stroke-clear aria-label="Bersihkan tampilan urutan goresan ${kanaString}">BERSIHKAN</button>` : ""}
            <label>Kecepatan<select data-stroke-speed aria-label="Kecepatan animasi stroke">
              <option value="1.6">0.5×</option>
              <option value="1" selected>1×</option>
              <option value="0.72">1.5×</option>
              <option value="0.52">2×</option>
            </select></label>
          </div>
        </div>

        <!-- KOTAK 2: KANVAS LATIHAN TULIS (INTERAKTIF USER) -->
        <div class="stroke-panel-card stroke-practice-card" data-panel-box="practice">
          <div class="panel-card-head">
            <span class="panel-card-title">
              <span class="panel-num">2</span>
              <strong>Tulis Sendiri</strong>
            </span>
            <span class="panel-card-tag">Sentuh &amp; Mouse</span>
          </div>
          <div class="user-canvas-wrapper">
            <canvas class="user-draw-canvas" width="220" height="220" aria-label="Kanvas menulis mandiri untuk ${kanaString}"></canvas>
            <div class="user-canvas-guide-char" aria-hidden="true">${kanaString}</div>
          </div>
          <div class="user-canvas-toolbar">
            <button type="button" class="canvas-tool-btn" data-canvas-clear title="Hapus goresan pada kanvas">
              🗑️ Bersihkan
            </button>
            <button type="button" class="canvas-tool-btn" data-canvas-undo title="Batalkan goresan terakhir">
              ↩️ Undo
            </button>
            <button type="button" class="canvas-tool-btn is-active" data-canvas-guide-toggle title="Nyalakan/matikan bayangan panduan huruf">
              👁️ Panduan: ON
            </button>
          </div>
          <div class="user-canvas-footer">
            <span class="user-canvas-hint">Tulis huruf di kanvas. Hasil otomatis dianalisis dan diputar di Kotak 3!</span>
            <button type="button" class="studio-btn primary canvas-finish-btn" data-canvas-finish>
              ✨ Periksa Goresan Saya
            </button>
          </div>
        </div>

        <!-- KOTAK 3: HASIL & PERBANDINGAN OTOMATIS (AUTO-PLAY) -->
        <div class="stroke-panel-card stroke-compare-card" data-panel-box="compare">
          <div class="panel-card-head">
            <span class="panel-card-title">
              <span class="panel-num">3</span>
              <strong>Hasil &amp; Putar Otomatis</strong>
            </span>
            <span class="panel-card-tag" id="compareBadge">Menunggu Goresan</span>
          </div>
          
          <div class="compare-display-area" id="compareDisplayArea">
            <!-- Placeholder saat belum ada goresan -->
            <div class="compare-placeholder" id="comparePlaceholder">
              <span class="placeholder-icon">✍️</span>
              <strong>Belum Ada Goresan</strong>
              <p>Coba tulis huruf <b>"${kanaString}"</b> di Kotak 2. Hasil goresanmu dan animasi acuan otomatis berputar di sini!</p>
            </div>

            <!-- Tampilan aktif perbandingan setelah user menulis -->
            <div class="compare-active-view" id="compareActiveView" hidden>
              <div class="compare-stage-duo">
                <div class="compare-box user-result-box">
                  <span class="compare-label">Goresan Kamu</span>
                  <img class="user-result-img" id="userResultImg" alt="Goresan buatan kamu">
                </div>
                <div class="compare-box official-replay-box">
                  <span class="compare-label">Acuan Standar</span>
                  <div class="compare-official-stage" id="compareOfficialStage"></div>
                </div>
              </div>
              <div class="compare-feedback-banner" id="compareFeedback">
                <span class="feedback-sparkle">✨</span>
                <span class="feedback-text" id="compareFeedbackText">Goresanmu siap dibandingkan! Amati arah dan proporsinya.</span>
              </div>
              <div class="compare-actions-bar">
                <button type="button" class="studio-btn primary compare-replay-btn" id="compareReplayBtn">
                  🔄 Putar Ulang Animasi
                </button>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- FOOTER: CATATAN VARIAN & TOMBOL LAPOR GORESAN ELEGAN -->
      <div class="stroke-footer-bar">
        ${noteHtml}
        <div class="stroke-footer-actions">
          ${reportBtnHtml}
        </div>
      </div>
    </div>
  `;

  // Render kontainer kanvas SVG resmi di Kotak 1
  const strokeStage = host.querySelector('.stroke-stage');
  strokeStage.innerHTML = "";
  strokeStage.style.display = 'flex';
  strokeStage.style.flexDirection = 'row';
  strokeStage.style.justifyContent = 'center';
  strokeStage.style.alignItems = 'center';
  strokeStage.style.gap = characters.length === 2 ? '14px' : '10px';
  strokeStage.style.flexWrap = 'wrap';

  let globalStrokeOffset = 0;

  characters.forEach((char, index) => {
    const charWrapper = document.createElement('div');
    charWrapper.id = 'stroke-char-' + index;
    charWrapper.className = 'kanjivg-char-box';
    charWrapper.style.position = 'relative';

    if (isMulti) {
      if (characters.length === 2) {
        charWrapper.classList.add('yoon-char');
        charWrapper.style.width = '100%';
        charWrapper.style.maxWidth = '180px';
        charWrapper.style.aspectRatio = '1 / 1';
      } else {
        charWrapper.classList.add('multi-char');
        charWrapper.style.width = '100%';
        charWrapper.style.maxWidth = characters.length === 3 ? '110px' : '90px';
        charWrapper.style.aspectRatio = '1 / 1';
      }
    } else {
      charWrapper.style.width = '100%';
      charWrapper.style.maxWidth = '200px';
      charWrapper.style.aspectRatio = '1 / 1';
      charWrapper.classList.add('single-char');
    }

    const rec = records[index];
    const paths = rec.paths;

    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("viewBox", "0 0 109 109");
    svg.setAttribute("preserveAspectRatio", "xMidYMid meet");
    svg.setAttribute("role", "img");
    svg.setAttribute("aria-label", `Urutan goresan ${char}`);
    svg.style.width = '100%';
    svg.style.height = '100%';
    svg.style.position = 'relative';
    svg.style.display = 'block';

    // Layer 0: Garis Kotak Panduan Genkouyoushi
    const gridGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
    gridGroup.setAttribute("class", "stroke-grid-group");
    gridGroup.setAttribute("aria-hidden", "true");

    const hLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
    hLine.setAttribute("x1", "5");
    hLine.setAttribute("y1", "54.5");
    hLine.setAttribute("x2", "104");
    hLine.setAttribute("y2", "54.5");
    hLine.setAttribute("class", "stroke-grid-line");

    const vLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
    vLine.setAttribute("x1", "54.5");
    vLine.setAttribute("y1", "5");
    vLine.setAttribute("x2", "54.5");
    vLine.setAttribute("y2", "104");
    vLine.setAttribute("class", "stroke-grid-line");

    gridGroup.appendChild(hLine);
    gridGroup.appendChild(vLine);
    svg.appendChild(gridGroup);

    // Layer 1: Goresan Panduan Transparan
    const guideGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
    guideGroup.setAttribute("class", "stroke-guide-group");
    paths.forEach((d) => {
      const guidePath = document.createElementNS("http://www.w3.org/2000/svg", "path");
      guidePath.setAttribute("class", "stroke-guide-path");
      guidePath.setAttribute("d", d);
      guidePath.setAttribute("stroke-linecap", "round");
      guidePath.setAttribute("stroke-linejoin", "round");
      guidePath.setAttribute("fill", "none");
      guideGroup.appendChild(guidePath);
    });
    svg.appendChild(guideGroup);

    // Layer 2: Goresan Animasi Solid
    const activeGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
    activeGroup.setAttribute("class", "stroke-active-group");
    paths.forEach((d, pathIndex) => {
      const pathEl = document.createElementNS("http://www.w3.org/2000/svg", "path");
      pathEl.setAttribute("class", "stroke-active-path");
      pathEl.setAttribute("data-stroke", `${index}-${pathIndex}`);
      pathEl.setAttribute("d", d);
      pathEl.setAttribute("stroke-linecap", "round");
      pathEl.setAttribute("stroke-linejoin", "round");
      pathEl.setAttribute("fill", "none");
      activeGroup.appendChild(pathEl);
    });
    svg.appendChild(activeGroup);

    // Layer 3: Angka Penunjuk Urutan Goresan
    const numbersGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
    numbersGroup.setAttribute("class", "stroke-numbers-group");
    const numPositions = calculateStrokeNumbers(paths, rec.numbers);
    numPositions.forEach((pos, pathIndex) => {
      const textEl = document.createElementNS("http://www.w3.org/2000/svg", "text");
      textEl.setAttribute("class", "stroke-number-label");
      textEl.setAttribute("x", String(pos.x));
      textEl.setAttribute("y", String(pos.y));
      textEl.setAttribute("data-stroke-num", `${index}-${pathIndex}`);
      textEl.textContent = String(globalStrokeOffset + pathIndex + 1);
      numbersGroup.appendChild(textEl);
    });
    svg.appendChild(numbersGroup);

    globalStrokeOffset += paths.length;
    charWrapper.appendChild(svg);
    strokeStage.appendChild(charWrapper);
  });

  // Koleksi elemen kontrol animasi Kotak 1
  const lines = [...strokeStage.querySelectorAll("path[data-stroke]")];
  const numberLabels = [...strokeStage.querySelectorAll(".stroke-number-label")];
  const number = host.querySelector("[data-stroke-number]");
  const order = [...host.querySelectorAll("[data-stroke-step]")];
  const speed = host.querySelector("[data-stroke-speed]");
  const playBtn = host.querySelector("[data-stroke-play]");

  let step = 0;
  let animation = null;
  let playing = false;
  let paused = false;
  let cleared = false;

  const duration = () => 650 * Number(speed.value || 1);

  function setStepLabel() {
    if (destroyed) return;
    const visibleStep = Math.min(step + 1, lines.length);
    if (number) number.textContent = cleared ? "0" : String(visibleStep);

    order.forEach((item, index) => {
      item.classList.toggle("is-active", index === step && (playing || paused));
      item.classList.toggle("is-done", index < step);
    });

    numberLabels.forEach((numLabel, index) => {
      numLabel.classList.toggle("is-active", index === step && (playing || paused));
      numLabel.classList.toggle("is-done", index < step);
    });

    if (playBtn) {
      if (playing) {
        playBtn.innerHTML = "JEDA ⏸";
      } else if (paused) {
        playBtn.innerHTML = "LANJUT ▶";
      } else {
        playBtn.innerHTML = "PUTAR ▶";
      }
    }
  }

  function applyActiveState(instant = false) {
    if (destroyed) return;
    lines.forEach((line, index) => {
      const len = line.getTotalLength ? line.getTotalLength() : 100;
      line.style.strokeDasharray = `${len} ${len}`;
      if (index < step) {
        line.style.transition = instant ? "none" : "stroke-dashoffset 0.15s ease";
        line.style.strokeDashoffset = "0";
      } else {
        line.style.transition = "none";
        line.style.strokeDashoffset = `${len}`;
      }
    });
    setStepLabel();
  }

  function animateSingleStroke(index, onComplete) {
    if (destroyed) return;
    const line = lines[index];
    if (!line) {
      if (onComplete) onComplete();
      return;
    }
    const len = line.getTotalLength ? line.getTotalLength() : 100;
    line.style.strokeDasharray = `${len} ${len}`;
    line.style.strokeDashoffset = `${len}`;
    line.getBoundingClientRect(); // reflow
    line.style.transition = `stroke-dashoffset ${duration()}ms cubic-bezier(0.4, 0, 0.2, 1)`;
    line.style.strokeDashoffset = "0";

    const timer = setTimeout(() => {
      if (onComplete) onComplete();
    }, duration() + 80);

    animation = {
      cancel: () => {
        clearTimeout(timer);
        line.style.transition = "none";
      }
    };
  }

  function playSequence() {
    if (destroyed || !playing) return;
    if (step >= lines.length) {
      playing = false;
      paused = false;
      setStepLabel();
      return;
    }
    setStepLabel();
    animateSingleStroke(step, () => {
      if (!playing) return;
      step++;
      if (step < lines.length) {
        playSequence();
      } else {
        playing = false;
        paused = false;
        setStepLabel();
      }
    });
  }

  function play() {
    if (destroyed) return;
    cleared = false;
    if (animation) animation.cancel();
    if (paused) {
      playing = true;
      paused = false;
      playSequence();
      return;
    }
    if (step >= lines.length) step = 0;
    applyActiveState(true);
    playing = true;
    paused = false;
    playSequence();
  }

  function pause() {
    if (destroyed || !playing) return;
    if (animation) animation.cancel();
    playing = false;
    paused = true;
    setStepLabel();
  }

  function resume() {
    if (destroyed || !paused) return;
    playing = true;
    paused = false;
    playSequence();
  }

  function togglePlay() {
    if (playing) pause();
    else if (paused) resume();
    else play();
  }

  function replay() {
    if (destroyed) return;
    if (animation) animation.cancel();
    step = 0;
    cleared = false;
    applyActiveState(true);
    playing = true;
    paused = false;
    playSequence();
  }

  function prevStep() {
    if (destroyed) return;
    if (animation) animation.cancel();
    playing = false;
    paused = false;
    cleared = false;
    step = Math.max(0, step - 1);
    applyActiveState(true);
  }

  function nextStep() {
    if (destroyed) return;
    if (animation) animation.cancel();
    playing = false;
    paused = false;
    cleared = false;
    step = Math.min(lines.length - 1, step + 1);
    applyActiveState(true);
  }

  function reset() {
    if (destroyed) return;
    if (animation) animation.cancel();
    step = 0;
    playing = false;
    paused = false;
    cleared = false;
    applyActiveState(true);
  }

  function clearView() {
    if (destroyed) return;
    if (animation) animation.cancel();
    step = 0;
    playing = false;
    paused = false;
    cleared = true;
    lines.forEach((line) => {
      const len = line.getTotalLength ? line.getTotalLength() : 100;
      line.style.transition = "none";
      line.style.strokeDashoffset = `${len}`;
    });
    setStepLabel();
  }

  // Event Listeners Kotak 1
  if (playBtn) playBtn.addEventListener("click", togglePlay);
  const clearBtn = host.querySelector("[data-stroke-clear]");
  if (clearBtn) clearBtn.addEventListener("click", clearView);
  const prevBtn = host.querySelector("[data-stroke-prev]");
  if (prevBtn) prevBtn.addEventListener("click", prevStep);
  const nextBtn = host.querySelector("[data-stroke-next]");
  if (nextBtn) nextBtn.addEventListener("click", nextStep);
  const replayBtn = host.querySelector("[data-stroke-replay]");
  if (replayBtn) replayBtn.addEventListener("click", replay);

  order.forEach((thumb, idx) => {
    thumb.addEventListener("click", () => {
      if (destroyed) return;
      if (animation) animation.cancel();
      playing = false;
      paused = false;
      cleared = false;
      step = idx + 1;
      applyActiveState(true);
    });
  });

  numberLabels.forEach((numLabel, idx) => {
    numLabel.addEventListener("click", () => {
      if (destroyed) return;
      if (animation) animation.cancel();
      playing = false;
      paused = false;
      cleared = false;
      step = idx + 1;
      applyActiveState(true);
    });
  });

  // Tampilkan kondisi awal
  applyActiveState(true);

  // =========================================================================
  // INISIALISASI KOTAK 2: KANVAS TULIS INTERAKTIF (USER DRAW CANVAS)
  // =========================================================================
  const drawCanvas = host.querySelector('.user-draw-canvas');
  const guideChar = host.querySelector('.user-canvas-guide-char');
  const canvasClearBtn = host.querySelector('[data-canvas-clear]');
  const canvasUndoBtn = host.querySelector('[data-canvas-undo]');
  const canvasGuideToggle = host.querySelector('[data-canvas-guide-toggle]');
  const canvasFinishBtn = host.querySelector('[data-canvas-finish]');

  let userStrokes = [];
  let currentStroke = [];
  let isDrawing = false;
  let autoCompareTimeout = null;
  const drawColor = '#e91e63';
  const drawLineWidth = 6;

  function renderDrawCanvasGrid() {
    if (!drawCanvas) return;
    const ctx = drawCanvas.getContext('2d');
    if (!ctx) return;
    ctx.clearRect(0, 0, drawCanvas.width, drawCanvas.height);

    // Garis bantu salib (crosshair)
    ctx.save();
    ctx.strokeStyle = 'rgba(233, 30, 99, 0.16)';
    ctx.lineWidth = 1;
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(10, drawCanvas.height / 2);
    ctx.lineTo(drawCanvas.width - 10, drawCanvas.height / 2);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(drawCanvas.width / 2, 10);
    ctx.lineTo(drawCanvas.width / 2, drawCanvas.height - 10);
    ctx.stroke();
    ctx.restore();

    // Gambar ulang seluruh goresan yang sudah dibuat
    ctx.save();
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.lineWidth = drawLineWidth;
    ctx.strokeStyle = drawColor;

    userStrokes.forEach(stroke => {
      if (stroke.length < 2) {
        if (stroke.length === 1) {
          ctx.beginPath();
          ctx.arc(stroke[0].x, stroke[0].y, drawLineWidth / 2, 0, Math.PI * 2);
          ctx.fillStyle = drawColor;
          ctx.fill();
        }
        return;
      }
      ctx.beginPath();
      ctx.moveTo(stroke[0].x, stroke[0].y);
      for (let i = 1; i < stroke.length; i++) {
        ctx.lineTo(stroke[i].x, stroke[i].y);
      }
      ctx.stroke();
    });
    ctx.restore();
  }

  if (drawCanvas) {
    const ctx = drawCanvas.getContext('2d');
    renderDrawCanvasGrid();

    function getCanvasPos(e) {
      const rect = drawCanvas.getBoundingClientRect();
      const scaleX = drawCanvas.width / rect.width;
      const scaleY = drawCanvas.height / rect.height;
      const clientX = e.clientX ?? (e.touches && e.touches[0].clientX);
      const clientY = e.clientY ?? (e.touches && e.touches[0].clientY);
      return {
        x: (clientX - rect.left) * scaleX,
        y: (clientY - rect.top) * scaleY
      };
    }

    function onPointerDown(e) {
      isDrawing = true;
      const pos = getCanvasPos(e);
      currentStroke = [pos];
      renderDrawCanvasGrid();
      if (e.cancelable && e.type.startsWith('touch')) e.preventDefault();
    }

    function onPointerMove(e) {
      if (!isDrawing) return;
      const pos = getCanvasPos(e);
      currentStroke.push(pos);

      ctx.save();
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      ctx.lineWidth = drawLineWidth;
      ctx.strokeStyle = drawColor;
      if (currentStroke.length >= 2) {
        const p1 = currentStroke[currentStroke.length - 2];
        const p2 = currentStroke[currentStroke.length - 1];
        ctx.beginPath();
        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(p2.x, p2.y);
        ctx.stroke();
      }
      ctx.restore();
      if (e.cancelable && e.type.startsWith('touch')) e.preventDefault();
    }

    function onPointerUp() {
      if (!isDrawing) return;
      isDrawing = false;
      if (currentStroke.length > 0) {
        userStrokes.push(currentStroke);
        currentStroke = [];
        renderDrawCanvasGrid();

        // Pemicu otomatis: Munculkan Kotak 3 & Putar Otomatis setelah jeda 650ms!
        clearTimeout(autoCompareTimeout);
        autoCompareTimeout = setTimeout(() => {
          triggerCompareAutoPlay();
        }, 650);
      }
    }

    drawCanvas.addEventListener('mousedown', onPointerDown);
    window.addEventListener('mousemove', onPointerMove);
    window.addEventListener('mouseup', onPointerUp);

    drawCanvas.addEventListener('touchstart', onPointerDown, { passive: false });
    drawCanvas.addEventListener('touchmove', onPointerMove, { passive: false });
    drawCanvas.addEventListener('touchend', onPointerUp);
    drawCanvas.addEventListener('touchcancel', onPointerUp);

    // Toolbar Kanvas
    if (canvasClearBtn) {
      canvasClearBtn.addEventListener('click', () => {
        userStrokes = [];
        currentStroke = [];
        renderDrawCanvasGrid();
        resetCompareView();
      });
    }

    if (canvasUndoBtn) {
      canvasUndoBtn.addEventListener('click', () => {
        if (userStrokes.length > 0) {
          userStrokes.pop();
          renderDrawCanvasGrid();
          if (userStrokes.length > 0) {
            triggerCompareAutoPlay();
          } else {
            resetCompareView();
          }
        }
      });
    }

    if (canvasGuideToggle && guideChar) {
      canvasGuideToggle.addEventListener('click', () => {
        const isHidden = guideChar.style.display === 'none';
        guideChar.style.display = isHidden ? 'flex' : 'none';
        canvasGuideToggle.classList.toggle('is-active', isHidden);
        canvasGuideToggle.textContent = isHidden ? '👁️ Panduan: ON' : '👁️ Panduan: OFF';
      });
    }

    if (canvasFinishBtn) {
      canvasFinishBtn.addEventListener('click', () => {
        triggerCompareAutoPlay();
      });
    }
  }

  // =========================================================================
  // INISIALISASI KOTAK 3: HASIL & PUTAR OTOMATIS (AUTO-PLAY COMPARISON)
  // =========================================================================
  const comparePlaceholder = host.querySelector('#comparePlaceholder');
  const compareActiveView = host.querySelector('#compareActiveView');
  const userResultImg = host.querySelector('#userResultImg');
  const compareOfficialStage = host.querySelector('#compareOfficialStage');
  const compareFeedbackText = host.querySelector('#compareFeedbackText');
  const compareBadge = host.querySelector('#compareBadge');
  const compareReplayBtn = host.querySelector('#compareReplayBtn');

  let compareAnimationTimer = null;

  function resetCompareView() {
    if (comparePlaceholder) comparePlaceholder.hidden = false;
    if (compareActiveView) compareActiveView.hidden = true;
    if (compareBadge) {
      compareBadge.textContent = 'Menunggu Goresan';
      compareBadge.classList.remove('is-active');
    }
    if (compareOfficialStage) compareOfficialStage.innerHTML = '';
    clearTimeout(compareAnimationTimer);
  }

  function startOfficialCompareAnimation() {
    if (!compareOfficialStage) return;
    compareOfficialStage.innerHTML = '';

    // Render clone SVG dari Kotak 1 untuk diputar otomatis di Kotak 3
    characters.forEach((char, index) => {
      const rec = records[index];
      const paths = rec.paths;
      const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svg.setAttribute("viewBox", "0 0 109 109");
      svg.setAttribute("preserveAspectRatio", "xMidYMid meet");
      svg.style.width = '100%';
      svg.style.height = '100%';
      svg.style.display = 'block';

      // Panduan
      const gGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
      paths.forEach(d => {
        const p = document.createElementNS("http://www.w3.org/2000/svg", "path");
        p.setAttribute("d", d);
        p.setAttribute("class", "stroke-guide-path");
        p.setAttribute("fill", "none");
        gGroup.appendChild(p);
      });
      svg.appendChild(gGroup);

      // Active
      const aGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
      paths.forEach((d, pIdx) => {
        const p = document.createElementNS("http://www.w3.org/2000/svg", "path");
        p.setAttribute("d", d);
        p.setAttribute("class", "stroke-active-path");
        p.setAttribute("data-cmp-stroke", `${index}-${pIdx}`);
        p.setAttribute("fill", "none");
        aGroup.appendChild(p);
      });
      svg.appendChild(aGroup);
      compareOfficialStage.appendChild(svg);
    });

    const cmpLines = [...compareOfficialStage.querySelectorAll('path[data-cmp-stroke]')];
    cmpLines.forEach(l => {
      const len = l.getTotalLength ? l.getTotalLength() : 100;
      l.style.strokeDasharray = `${len} ${len}`;
      l.style.strokeDashoffset = `${len}`;
      l.style.transition = 'none';
    });

    // Auto-play otomatis urutan goresan dari awal sampai selesai
    let cmpStep = 0;
    function playNextCmp() {
      if (cmpStep >= cmpLines.length) return;
      const l = cmpLines[cmpStep];
      const len = l.getTotalLength ? l.getTotalLength() : 100;
      l.getBoundingClientRect(); // reflow
      l.style.transition = `stroke-dashoffset 420ms cubic-bezier(0.4, 0, 0.2, 1)`;
      l.style.strokeDashoffset = '0';
      cmpStep++;
      compareAnimationTimer = setTimeout(playNextCmp, 480);
    }
    clearTimeout(compareAnimationTimer);
    compareAnimationTimer = setTimeout(playNextCmp, 200);
  }

  function triggerCompareAutoPlay() {
    if (userStrokes.length === 0 || !drawCanvas) return;
    if (comparePlaceholder) comparePlaceholder.hidden = true;
    if (compareActiveView) compareActiveView.hidden = false;

    // Ambil gambar snapshot dari canvas user
    if (userResultImg) {
      userResultImg.src = drawCanvas.toDataURL('image/png');
    }

    if (compareBadge) {
      compareBadge.textContent = `${userStrokes.length} Goresan Digambar`;
      compareBadge.classList.add('is-active');
    }

    if (compareFeedbackText) {
      const diff = userStrokes.length - totalStrokes;
      if (diff === 0) {
        compareFeedbackText.innerHTML = `Hebat! Jumlah goresanmu tepat <b>${totalStrokes} goresan</b>. Animasi otomatis berputar di samping!`;
      } else if (diff > 0) {
        compareFeedbackText.innerHTML = `Kamu membuat <b>${userStrokes.length} goresan</b> (acuan resmi: ${totalStrokes}). Perhatikan urutan animasinya!`;
      } else {
        compareFeedbackText.innerHTML = `Kamu membuat <b>${userStrokes.length} goresan</b> dari ${totalStrokes} goresan resmi. Coba lengkapi lagi!`;
      }
    }

    // Putar animasi acuan secara OTOMATIS tanpa perlu klik tombol dulu!
    startOfficialCompareAnimation();
  }

  if (compareReplayBtn) {
    compareReplayBtn.addEventListener('click', () => {
      startOfficialCompareAnimation();
    });
  }

  // Mode Switcher Tabs (Semua Kotak / Kotak 1 / Kotak 2 / Kotak 3)
  const modeBtns = host.querySelectorAll('.stroke-mode-btn');
  const panelBoxes = host.querySelectorAll('.stroke-panel-card');
  modeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      modeBtns.forEach(b => b.classList.remove('is-active'));
      btn.classList.add('is-active');
      const mode = btn.dataset.strokeMode;
      panelBoxes.forEach(box => {
        if (mode === 'all') {
          box.hidden = false;
        } else {
          box.hidden = box.dataset.panelBox !== mode;
        }
      });
    });
  });

  // Pasang internalController untuk kompatibilitas penuh dengan sistem
  internalController = {
    destroy: () => {
      destroyed = true;
      if (animation) animation.cancel();
      clearTimeout(autoCompareTimeout);
      clearTimeout(compareAnimationTimer);
    },
    play,
    pause,
    resume,
    togglePlay,
    replay,
    prev: prevStep,
    next: nextStep,
    reset,
    clear: clearView,
    isAvailable: true,
    getStep: () => step,
    getTotalSteps: () => lines.length,
    isPlaying: () => playing,
    isPaused: () => paused
  };
  host._miraiStrokeController = internalController;
}"""

    if old_setup_pattern.search(content):
        content = old_setup_pattern.sub(lambda m: new_setup_code, content)
        stroke_file.write_text(content, encoding="utf-8")
        print("✓ js/stroke.js: Studio Goresan Interaktif 3 Kotak & Auto-Play berhasil dipasang.")
    else:
        print("! Warning: Pola setupPlayerWithRecords di js/stroke.js tidak cocok.")

def update_css():
    css_file = ROOT / "css" / "pages" / "kamus.css"
    content = css_file.read_text(encoding="utf-8")

    studio_css = """
/* ==========================================================================
   STUDIO GORESAN INTERAKTIF 3 KOTAK (TRIO PANEL KANVAS & AUTO-PLAY)
   ========================================================================== */
.stroke-studio-container {
  width: 100%;
  margin: 14px 0 24px;
  box-sizing: border-box;
}

.stroke-studio-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.stroke-studio-title-wrap {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.stroke-studio-badge {
  font-size: 13px;
  font-weight: 800;
  color: var(--pink, #e91e63);
  letter-spacing: 0.5px;
}

.stroke-studio-sub {
  font-size: 11.5px;
  color: var(--muted, #6d6471);
}

body.theme-dark .stroke-studio-sub,
body.dark-mode .stroke-studio-sub {
  color: #a89cb0;
}

.stroke-mode-tabs {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: #fdf2f7;
  border: 1px solid var(--pink-border, #fcd1e5);
  border-radius: 999px;
  padding: 3px;
}

body.theme-dark .stroke-mode-tabs,
body.dark-mode .stroke-mode-tabs {
  background: #231a29;
  border-color: rgba(233, 30, 99, 0.3);
}

.stroke-mode-btn {
  border: none;
  background: transparent;
  padding: 5px 12px;
  border-radius: 999px;
  font-size: 11.5px;
  font-weight: 700;
  color: var(--muted, #6d6471);
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
}

body.theme-dark .stroke-mode-btn,
body.dark-mode .stroke-mode-btn {
  color: #b5a8bd;
}

.stroke-mode-btn.is-active {
  background: var(--pink, #e91e63);
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(233, 30, 99, 0.3);
}

/* Grid 3 Kotak Berdampingan (Desktop) */
.stroke-studio-trio {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
  align-items: stretch;
}

.stroke-panel-card {
  min-width: 0;
  background: #ffffff;
  border: 1.5px solid var(--pink-border, #fcd1e5);
  border-radius: 18px;
  padding: 16px;
  box-shadow: 0 6px 20px rgba(72, 32, 52, 0.05);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-sizing: border-box;
  transition: all 0.2s ease;
}

body.theme-dark .stroke-panel-card,
body.dark-mode .stroke-panel-card {
  background: #191422;
  border-color: rgba(233, 30, 99, 0.3);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.panel-card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px dashed rgba(233, 30, 99, 0.18);
}

.panel-card-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.panel-num {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--pink, #e91e63);
  color: #ffffff;
  font-size: 11px;
  font-weight: 900;
  display: flex;
  align-items: center;
  justify-content: center;
}

.panel-card-title strong {
  font-size: 13px;
  font-weight: 800;
  color: var(--ink, #201c26);
}

body.theme-dark .panel-card-title strong,
body.dark-mode .panel-card-title strong {
  color: #ffffff;
}

.panel-card-tag {
  font-size: 10px;
  font-weight: 700;
  color: var(--pink, #e91e63);
  background: #fff0f5;
  border: 1px solid #ffd4e5;
  border-radius: 999px;
  padding: 2px 8px;
  white-space: nowrap;
}

body.theme-dark .panel-card-tag,
body.dark-mode .panel-card-tag {
  background: rgba(233, 30, 99, 0.18);
  border-color: rgba(233, 30, 99, 0.35);
  color: #ff6090;
}

/* Kotak 2: Kanvas Tulis Mandiri */
.user-canvas-wrapper {
  position: relative;
  width: 100%;
  max-width: 220px;
  aspect-ratio: 1 / 1;
  margin: 0 auto 12px;
  background: #fffcfd;
  border: 1.5px solid var(--pink-border, #fcd1e5);
  border-radius: 14px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

body.theme-dark .user-canvas-wrapper,
body.dark-mode .user-canvas-wrapper {
  background: #15111d;
  border-color: rgba(233, 30, 99, 0.3);
}

.user-draw-canvas {
  position: relative;
  z-index: 2;
  width: 100%;
  height: 100%;
  display: block;
  cursor: crosshair;
  touch-action: none;
}

.user-canvas-guide-char {
  position: absolute;
  inset: 0;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 120px;
  font-family: var(--font-jp, "Noto Sans JP", sans-serif);
  color: rgba(233, 30, 99, 0.14);
  user-select: none;
  pointer-events: none;
  line-height: 1;
}

body.theme-dark .user-canvas-guide-char,
body.dark-mode .user-canvas-guide-char {
  color: rgba(255, 101, 155, 0.18);
}

.user-canvas-toolbar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.canvas-tool-btn {
  border: 1px solid var(--pink-border, #fcd1e5);
  background: #ffffff;
  color: var(--ink, #201c26);
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
}

body.theme-dark .canvas-tool-btn,
body.dark-mode .canvas-tool-btn {
  background: #231b2e;
  border-color: rgba(233, 30, 99, 0.3);
  color: #f1ecf4;
}

.canvas-tool-btn:hover {
  background: #fff0f5;
  border-color: var(--pink, #e91e63);
  color: var(--pink, #e91e63);
}

.canvas-tool-btn.is-active {
  background: var(--pink, #e91e63);
  color: #ffffff;
  border-color: var(--pink, #e91e63);
}

.user-canvas-footer {
  display: flex;
  flex-direction: column;
  gap: 8px;
  text-align: center;
}

.user-canvas-hint {
  font-size: 11px;
  color: var(--muted, #6d6471);
  line-height: 1.4;
}

body.theme-dark .user-canvas-hint,
body.dark-mode .user-canvas-hint {
  color: #a89cb0;
}

.canvas-finish-btn {
  width: 100%;
  padding: 10px;
  font-size: 12.5px;
  font-weight: 800;
  border-radius: 10px;
}

/* Kotak 3: Hasil & Perbandingan Auto-Play */
.compare-display-area {
  min-height: 240px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.compare-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 24px 14px;
  color: var(--muted, #6d6471);
  gap: 6px;
}

body.theme-dark .compare-placeholder,
body.dark-mode .compare-placeholder {
  color: #a89cb0;
}

.placeholder-icon {
  font-size: 36px;
  margin-bottom: 4px;
  opacity: 0.7;
}

.compare-placeholder strong {
  font-size: 13.5px;
  color: var(--ink, #201c26);
}

body.theme-dark .compare-placeholder strong,
body.dark-mode .compare-placeholder strong {
  color: #f1ecf4;
}

.compare-placeholder p {
  font-size: 11.5px;
  margin: 0;
  line-height: 1.45;
}

.compare-active-view {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.compare-stage-duo {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  align-items: center;
}

.compare-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.compare-label {
  font-size: 10.5px;
  font-weight: 800;
  color: var(--pink, #e91e63);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.user-result-img,
.compare-official-stage {
  width: 100%;
  max-width: 105px;
  aspect-ratio: 1 / 1;
  background: #fffcfd;
  border: 1.5px solid var(--pink-border, #fcd1e5);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
}

body.theme-dark .user-result-img,
body.theme-dark .compare-official-stage,
body.dark-mode .user-result-img,
body.dark-mode .compare-official-stage {
  background: #15111d;
  border-color: rgba(233, 30, 99, 0.3);
}

.compare-feedback-banner {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  padding: 8px 10px;
  background: #fdf2f7;
  border: 1px solid var(--pink-border, #fcd1e5);
  border-radius: 10px;
  font-size: 11px;
  line-height: 1.4;
  color: var(--ink, #201c26);
}

body.theme-dark .compare-feedback-banner,
body.dark-mode .compare-feedback-banner {
  background: #231a29;
  border-color: rgba(233, 30, 99, 0.3);
  color: #f1ecf4;
}

.feedback-sparkle {
  font-size: 14px;
  flex-shrink: 0;
}

.compare-actions-bar {
  display: flex;
  justify-content: center;
}

.compare-replay-btn {
  width: 100%;
  padding: 10px;
  font-size: 12px;
  font-weight: 800;
  border-radius: 10px;
}

/* ==========================================================================
   DESAIN ELEGAN: TOMBOL LAPOR GORESAN SALAH (POINT 3)
   ========================================================================== */
.stroke-footer-bar {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 12px !important;
  margin-top: 16px !important;
  padding-top: 12px !important;
  border-top: 1px dashed rgba(233, 30, 99, 0.2) !important;
  flex-wrap: wrap !important;
  width: 100% !important;
  max-width: 100% !important;
}

.stroke-report-pill {
  display: inline-flex !important;
  align-items: center !important;
  gap: 6px !important;
  padding: 6px 14px !important;
  background: rgba(233, 30, 99, 0.08) !important;
  border: 1.5px solid rgba(233, 30, 99, 0.28) !important;
  border-radius: 999px !important;
  font-size: 12px !important;
  font-weight: 700 !important;
  color: var(--pink, #e91e63) !important;
  text-decoration: none !important;
  transition: all 0.22s ease !important;
  user-select: none !important;
}

.stroke-report-pill:hover {
  background: var(--pink, #e91e63) !important;
  color: #ffffff !important;
  border-color: var(--pink, #e91e63) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 14px rgba(233, 30, 99, 0.3) !important;
}

body.theme-dark .stroke-report-pill,
body.dark-mode .stroke-report-pill {
  background: rgba(233, 30, 99, 0.18) !important;
  border-color: rgba(233, 30, 99, 0.4) !important;
  color: #ff6090 !important;
}

body.theme-dark .stroke-report-pill:hover,
body.dark-mode .stroke-report-pill:hover {
  background: #e91e63 !important;
  color: #ffffff !important;
}

/* Responsivitas Layar */
@media (max-width: 1024px) and (min-width: 681px) {
  .stroke-studio-trio {
    grid-template-columns: 1fr 1fr;
  }
  .stroke-compare-card {
    grid-column: span 2;
  }
}

@media (max-width: 680px) {
  .stroke-studio-trio {
    grid-template-columns: 1fr;
    gap: 14px;
  }
}
"""

    if "/* STUDIO GORESAN INTERAKTIF 3 KOTAK" not in content:
        content = content.rstrip() + "\n" + studio_css
        css_file.write_text(content, encoding="utf-8")
        print("✓ css/pages/kamus.css: Gaya Studio Goresan Interaktif 3 Kotak berhasil ditambahkan.")
    else:
        # Perbarui blok jika sudah ada
        pattern = re.compile(r'/\* =+\s*STUDIO GORESAN INTERAKTIF 3 KOTAK.*?$', re.DOTALL)
        content = pattern.sub(studio_css.strip(), content)
        css_file.write_text(content, encoding="utf-8")
        print("✓ css/pages/kamus.css: Gaya Studio Goresan Interaktif 3 Kotak berhasil dimutakhirkan.")

if __name__ == "__main__":
    print("=== MEMPERBARUI STUDIO GORESAN INTERAKTIF 3 KOTAK ===")
    update_rename()
    update_stroke_js()
    update_css()
    print("=== SELESAI ===")
