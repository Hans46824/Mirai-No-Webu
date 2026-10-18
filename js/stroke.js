/**
 * File: js/stroke.js
 * Fungsi: Mesin animasi kanvas urutan goresan karakter Kanji dan kombinasi Kana Yoon di atas kisi Genkouyoushi.
 * Penggunaan: kamus/index.html dan kamus/kanji.html.
*/

window.currentPenSize = 'thick';

window.togglePenSize = function togglePenSize() {
// Fitur pemilihan ukuran kuas dinonaktifkan sesuai permintaan pengguna (kuas standar dipertahankan)
};

/* ==========================================================================
SKEMA VALIDASI DATA & MANAJEMEN CACHE RESMI (KANJIVG v4)
========================================================================== */

/**
 * Memvalidasi apakah rekaman data goresan mematuhi spesifikasi standar KanjiVG.
*/
function isValidStrokeRecord(record) {
if (!record || typeof record !== 'object') return false;
if (record.viewBox !== '0 0 109 109') return false;
if (!Array.isArray(record.paths) || record.paths.length === 0) return false;
for (let i = 0; i < record.paths.length; i++) {
  const p = record.paths[i];
  if (typeof p !== 'string' || !/^\s*[Mm]\s*[-\d\.]+/.test(p)) {
    return false;
  }
}
return true;
}

// Bersihkan cache lama (v1, v2, v3, v4) dari localStorage untuk menghemat storage perangkat pengguna
try {
  for (let i = localStorage.length - 1; i >= 0; i--) {
    const k = localStorage.key(i);
    if (k && (k.startsWith("mirai_stroke_") || k.startsWith("kanjivg_cache_"))) {
      localStorage.removeItem(k);
    }
  }
} catch (e) {}

if (!window.MIRAI_STROKE_DATA) window.MIRAI_STROKE_DATA = window.STROKE_DATA || {};
window.STROKE_DATA = window.MIRAI_STROKE_DATA;

if (!window.MIRAI_STROKE_OVERRIDES) window.MIRAI_STROKE_OVERRIDES = window.STROKE_OVERRIDES || {};
window.STROKE_OVERRIDES = window.MIRAI_STROKE_OVERRIDES;

/**
 * Menerapkan lapisan override jika karakter memiliki modifikasi path, numbers, atau varian.
 */
function applyStrokeOverride(character, record) {
  if (!character || !record || typeof record !== 'object') return record;
  const overrides = window.MIRAI_STROKE_OVERRIDES || window.STROKE_OVERRIDES;
  const ov = overrides?.[character];
  if (ov) {
    if (Array.isArray(ov.paths) && ov.paths.length > 0) {
      record.paths = ov.paths;
    }
    if (Array.isArray(ov.numbers) && ov.numbers.length > 0) {
      record.numbers = ov.numbers;
    }
    if (ov.variant) {
      record.variant = ov.variant;
    }
    if (ov.note) {
      record.note = ov.note;
    }
    record.overridden = true;
  }
  return record;
}

function getAppBasePath() {
  const logo = document.querySelector(".brand img, .sidebar-footer-logo");
  if (logo) {
    const src = logo.getAttribute("src") || "";
    if (src.startsWith("../../")) return "../../";
    if (src.startsWith("../")) return "../";
  }
  const style = document.querySelector('link[rel="stylesheet"][href*="style.css"]');
  if (style) {
    const href = style.getAttribute("href") || "";
    if (href.startsWith("../../")) return "../../";
    if (href.startsWith("../")) return "../";
  }
  return "";
}

const loadedStrokeChunks = new Set();
const strokeChunkLoadingPromises = {};

/**
 * Memuat berkas chunk goresan kanji lokal data/strokes/<jlpt>.json secara on-demand.
 * Menghilangkan kebutuhan mengunduh 4.2 MB di awal, memangkas bobot menjadi ~58-450 KB per level.
 */
async function loadStrokeChunk(jlptLevel) {
  if (!jlptLevel) return null;
  const rawLvl = String(jlptLevel).toLowerCase().trim();
  const lvl = rawLvl.startsWith("n") ? rawLvl : ("n" + rawLvl);
  if (loadedStrokeChunks.has(lvl)) return window.MIRAI_STROKE_DATA;
  if (strokeChunkLoadingPromises[lvl]) return strokeChunkLoadingPromises[lvl];

  strokeChunkLoadingPromises[lvl] = (async () => {
    const base = getAppBasePath();
    try {
      const res = await fetch(base + "data/strokes/" + lvl + ".json");
      if (res.ok) {
        const chunk = await res.json();
        if (!window.MIRAI_STROKE_DATA) window.MIRAI_STROKE_DATA = {};
        for (const [ch, rec] of Object.entries(chunk)) {
          window.MIRAI_STROKE_DATA[ch] = rec;
        }
        window.STROKE_DATA = window.MIRAI_STROKE_DATA;
        loadedStrokeChunks.add(lvl);
        return window.MIRAI_STROKE_DATA;
      }
    } catch (e) {
      console.warn("[stroke.js] Gagal memuat data/strokes/" + lvl + ".json:", e);
    }
    return null;
  })();

  return strokeChunkLoadingPromises[lvl];
}
window.loadStrokeChunk = loadStrokeChunk;

/**
 * Mengambil data goresan secara asinkron (100% lokal tanpa CDN eksternal):
 * 1. Karakter Kana: tersedia langsung dari dataset inline (window.MIRAI_STROKE_DATA)
 * 2. Karakter Kanji: diambil on-demand dari chunk lokal data/strokes/<jlpt>.json
 */
window.getStrokeDataAsync = async function getStrokeDataAsync(character, optionalJlpt) {
  if (!character) return null;

  // 1. Cek apakah sudah ada di memori lokal (Kana inline atau chunk kanji yang telah dimuat)
  const localRec = window.STROKE_DATA?.[character] || window.MIRAI_STROKE_DATA?.[character];
  if (localRec && isValidStrokeRecord(localRec)) {
    const finalRec = applyStrokeOverride(character, localRec);
    window.STROKE_DATA[character] = finalRec;
    window.MIRAI_STROKE_DATA[character] = finalRec;
    return finalRec;
  }

  // Multi-karakter (Yoon / kata gabungan)
  if (character.length > 1) {
    const parts = await Promise.all(Array.from(character).map((c) => window.getStrokeDataAsync(c, optionalJlpt)));
    if (parts.length > 0 && parts.every((p) => p && isValidStrokeRecord(p))) {
      return {
        isMulti: true,
        characters: Array.from(character),
        parts: parts,
        source: "KanjiVG"
      };
    }
    return null;
  }

  // 2. Muat chunk data/strokes/<jlpt>.json on-demand jika karakter berupa Kanji
  let targetLvl = optionalJlpt || window.getKanjiJlpt?.(character) || window.currentSelectedKanjiJlpt;
  if (targetLvl) {
    await loadStrokeChunk(targetLvl);
  }

  // Jika belum ditemukan di chunk target, periksa chunk lain yang belum dimuat
  if (!window.MIRAI_STROKE_DATA?.[character]) {
    for (const lvl of ['n5', 'n4', 'n3', 'n2', 'n1']) {
      if (!loadedStrokeChunks.has(lvl)) {
        await loadStrokeChunk(lvl);
        if (window.MIRAI_STROKE_DATA?.[character]) break;
      }
    }
  }

  const chunkRec = window.MIRAI_STROKE_DATA?.[character];
  if (chunkRec && isValidStrokeRecord(chunkRec)) {
    const finalRec = applyStrokeOverride(character, chunkRec);
    window.STROKE_DATA[character] = finalRec;
    window.MIRAI_STROKE_DATA[character] = finalRec;
    return finalRec;
  }

  return null;
};

// Helper cerdas menghitung posisi label angka urutan goresan pada canvas KanjiVG
function calculateStrokeNumbers(paths, officialNumbers) {
function parseStart(d) {
  let sx = 25, sy = 25;
  const m = /^[Mm]\s*([-\d\.]+)[,\s]+([-\d\.]+)/.exec(d);
  if (m) {
    sx = parseFloat(m[1]);
    sy = parseFloat(m[2]);
  }
  return { sx, sy };
}

const hasOfficial = Array.isArray(officialNumbers) && officialNumbers.length >= paths.length;
const placed = [];

paths.forEach((d, i) => {
  const { sx, sy } = parseStart(d);
  let nx, ny;

  if (hasOfficial && officialNumbers[i] && typeof officialNumbers[i].x === 'number') {
    nx = officialNumbers[i].x;
    ny = officialNumbers[i].y;
  } else {
    nx = sx >= 12 ? sx - 6.5 : sx + 6;
    ny = sy >= 12 ? sy - 2.5 : sy + 7;
  }

  nx = Math.max(5, Math.min(104, nx));
  ny = Math.max(5, Math.min(104, ny));

  placed.push({
    x: nx,
    y: ny,
    text: (hasOfficial && officialNumbers[i]?.text) ? officialNumbers[i].text : String(i + 1)
  });
});

return placed;
}

/* ==========================================================================
PEMUTAR ANIMASI GORESAN UTAMA (createStrokePlayer)
========================================================================== */

window.createStrokePlayer = function createStrokePlayer(host, kanaString, fallbackCount, options = {}) {
if (!kanaString || !host) return null;

// 1. Batalkan dan bersihkan instance pemutar lama pada host yang sama
if (host._miraiStrokeController && typeof host._miraiStrokeController.destroy === 'function') {
  try {
    host._miraiStrokeController.destroy();
  } catch (e) {}
  host._miraiStrokeController = null;
}

// 2. Penghitung generasi host untuk mencegah hasil permintaan lama menimpa karakter baru
host._miraiStrokeGen = (host._miraiStrokeGen || 0) + 1;
const currentGen = host._miraiStrokeGen;

const showClearControl = options.showClear === true;
let destroyed = false;
let internalController = null;

const characters = Array.from(kanaString);
const isMulti = characters.length > 1;

// Helper data karakter lokal dengan proteksi lapisan override
const getCached = (c) => {
  const rec = window.MIRAI_STROKE_DATA?.[c];
  return (rec && isValidStrokeRecord(rec)) ? applyStrokeOverride(c, rec) : null;
};
const allImmediate = characters.every(getCached);

function renderUnavailableState() {
  if (destroyed || !host) return;

  host.innerHTML = `
            <div class="stroke-stage stroke-unavailable ${window.currentPenSize === 'thick' ? 'stroke-thick' : 'stroke-thin'}" aria-label="Urutan goresan ${kanaString} belum tersedia">
                <div class="kanjivg-char-box single-char" style="position:relative; width:100%; max-width:200px; aspect-ratio:1/1; display:flex; align-items:center; justify-content:center;">
                    <svg viewBox="0 0 109 109" preserveAspectRatio="xMidYMid meet" style="width:100%; height:100%; display:block;" role="img" aria-label="Kanvas ${kanaString}">
                        <g class="stroke-grid-group" aria-hidden="true">
                            <line x1="5" y1="54.5" x2="104" y2="54.5" class="stroke-grid-line" />
                            <line x1="54.5" y1="5" x2="54.5" y2="104" class="stroke-grid-line" />
                        </g>
                    </svg>
                    <span class="stroke-fallback-glyph" style="position:absolute; font-size:${isMulti ? '70px' : '110px'}; opacity:0.65; user-select:none;">${kanaString}</span>
                </div>
            </div>
            <div class="stroke-unavailable-box" style="margin: 14px 0 8px; text-align: center;">
                <p class="stroke-source" style="margin:0 0 4px; font-weight:700; color:var(--pink, #e91e63);">Data Urutan Goresan Belum Tersedia</p>
                <p class="stroke-guide" style="margin:0; font-size:12.5px; color:var(--muted, #666); line-height:1.5;">
                    Vektor kurva goresan resmi untuk karakter <b>&ldquo;${kanaString}&rdquo;</b> belum terdaftar dalam pustaka offline.
                </p>
            </div>
        `;

  internalController = {
    destroy: () => { destroyed = true; },
    play: () => {},
    pause: () => {},
    resume: () => {},
    togglePlay: () => {},
    replay: () => {},
    prev: () => {},
    next: () => {},
    reset: () => {},
    clear: () => {},
    isAvailable: false,
    getStep: () => 0,
    getTotalSteps: () => 0,
    isPlaying: () => false,
    isPaused: () => false
  };
  host._miraiStrokeController = internalController;
}

function setupPlayerWithRecords(records) {
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
}

if (allImmediate) {
  setupPlayerWithRecords(characters.map(getCached));
} else {
  // Tampilkan status memuat transparan jika membutuhkan fetch jaringan
  host.innerHTML = `
            <div class="stroke-stage is-loading ${window.currentPenSize === 'thick' ? 'stroke-thick' : 'stroke-thin'}">
                <div class="kanjivg-char-box single-char" style="position:relative; width:100%; max-width:200px; aspect-ratio:1/1; display:flex; align-items:center; justify-content:center;">
                    <svg viewBox="0 0 109 109" preserveAspectRatio="xMidYMid meet" style="width:100%; height:100%; display:block;" role="img" aria-hidden="true">
                        <g class="stroke-grid-group">
                            <line x1="5" y1="54.5" x2="104" y2="54.5" class="stroke-grid-line" />
                            <line x1="54.5" y1="5" x2="54.5" y2="104" class="stroke-grid-line" />
                        </g>
                    </svg>
                    <span class="stroke-fallback-glyph" style="position:absolute; font-size:${isMulti ? '70px' : '110px'}; opacity:0.35; user-select:none;">${kanaString}</span>
                </div>
            </div>
            <p class="stroke-source" style="margin: 8px 0; text-align: center;">Memuat data goresan KanjiVG...</p>
        `;

  Promise.all(characters.map((c) => window.getStrokeDataAsync(c, options.jlpt || options.level))).then((records) => {
    if (!destroyed && host._miraiStrokeGen === currentGen) {
    setupPlayerWithRecords(records);
    }
  }).catch(() => {
    if (!destroyed && host._miraiStrokeGen === currentGen) {
    renderUnavailableState();
    }
  });
}

return {
  destroy: () => internalController?.destroy(),
  play: () => internalController?.play(),
  pause: () => internalController?.pause(),
  resume: () => internalController?.resume(),
  togglePlay: () => internalController?.togglePlay(),
  replay: () => internalController?.replay(),
  prev: () => internalController?.prev(),
  next: () => internalController?.next(),
  reset: () => internalController?.reset(),
  clear: () => internalController?.clear(),
  isAvailable: () => internalController ? internalController.isAvailable : false
};
};

