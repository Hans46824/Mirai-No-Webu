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

// Bersihkan cache versi usang (v1, v2, v3) tanpa menghapus data v4 yang valid
try {
    for (let i = localStorage.length - 1; i >= 0; i--) {
        const k = localStorage.key(i);
        if (k && (k.startsWith("mirai_stroke_v1_") || k.startsWith("mirai_stroke_v2_") || k.startsWith("mirai_stroke_v3_"))) {
            localStorage.removeItem(k);
        }
    }
} catch (e) {}

/**
 * Mengambil data goresan secara asinkron dengan hierarki aman:
 * 1. Pustaka lokal tervalidasi (window.MIRAI_STROKE_DATA) - prioritas tertinggi
 * 2. Cache lokal terverifikasi skema (mirai_stroke_v4_*)
 * 3. Jaringan resmi KanjiVG via CDN dengan parsing DOMParser & validasi ketat
 */
window.getStrokeDataAsync = async function getStrokeDataAsync(character) {
    if (!character) return null;

    // 1. Data lokal kurasi (window.MIRAI_STROKE_DATA) prioritas mutlak
    if (window.MIRAI_STROKE_DATA?.[character]) {
        const localRec = window.MIRAI_STROKE_DATA[character];
        if (isValidStrokeRecord(localRec)) {
            return localRec;
        }
    }

    const cacheKey = "mirai_stroke_v4_" + character;

    // 2. Periksa cache localStorage (skema v4)
    try {
        const cachedRaw = localStorage.getItem(cacheKey);
        if (cachedRaw) {
            const parsedEnvelope = JSON.parse(cachedRaw);
            if (parsedEnvelope?.v === 4 && isValidStrokeRecord(parsedEnvelope?.record)) {
                if (!window.MIRAI_STROKE_DATA) window.MIRAI_STROKE_DATA = {};
                window.MIRAI_STROKE_DATA[character] = parsedEnvelope.record;
                return parsedEnvelope.record;
            } else {
                localStorage.removeItem(cacheKey);
            }
        }
    } catch (e) {}

    // Multi-karakter (Yoon / kata): ambil bagian-bagiannya
    if (character.length > 1) {
        const parts = await Promise.all(Array.from(character).map((c) => window.getStrokeDataAsync(c)));
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

    // 3. Fallback: Unduh berkas SVG resmi dari KanjiVG via CDN
    try {
        const cp = character.codePointAt(0);
        if (!cp) return null;
        const hex = cp.toString(16).padStart(5, "0").toLowerCase();
        const res = await fetch(`https://cdn.jsdelivr.net/gh/KanjiVG/kanjivg@master/kanji/${hex}.svg`);
        if (res.ok) {
            const svgText = await res.text();
            let paths = [];
            let numbers = [];

            try {
                const parser = new DOMParser();
                const doc = parser.parseFromString(svgText, "image/svg+xml");
                const pathsGroup = doc.querySelector("[id*='StrokePaths']") || doc;
                const pathElements = Array.from(pathsGroup.querySelectorAll("path"));

                pathElements.sort((a, b) => {
                    const ma = /-s(\d+)$/.exec(a.id || "");
                    const mb = /-s(\d+)$/.exec(b.id || "");
                    if (ma && mb) return parseInt(ma[1], 10) - parseInt(mb[1], 10);
                    return 0;
                });
                paths = pathElements.map((p) => p.getAttribute("d")).filter(Boolean);

                const numbersGroup = doc.querySelector("[id*='StrokeNumbers']");
                if (numbersGroup) {
                    numbersGroup.querySelectorAll("text").forEach((t) => {
                        const trans = t.getAttribute("transform") || "";
                        const m = /matrix\s*\(\s*[^,\s]+\s*[, ]\s*[^,\s]+\s*[, ]\s*[^,\s]+\s*[, ]\s*[^,\s]+\s*[, ]\s*([-\d\.]+)\s*[, ]\s*([-\d\.]+)\s*\)/i.exec(trans);
                        if (m) {
                            numbers.push({
                                x: parseFloat(m[1]),
                                y: parseFloat(m[2]),
                                text: (t.textContent || "").trim()
                            });
                        }
                    });
                }
            } catch (parseErr) {
                const regex = /<path[^>]+d="([^"]+)"/g;
                let match;
                while ((match = regex.exec(svgText)) !== null) {
                    paths.push(match[1]);
                }
            }

            const record = { viewBox: "0 0 109 109", paths, numbers, source: "KanjiVG-CDN" };
            if (isValidStrokeRecord(record)) {
                if (!window.MIRAI_STROKE_DATA) window.MIRAI_STROKE_DATA = {};
                window.MIRAI_STROKE_DATA[character] = record;
                try {
                    const envelope = { v: 4, char: character, time: Date.now(), record };
                    localStorage.setItem(cacheKey, JSON.stringify(envelope));
                } catch (e) {}
                return record;
            }
        }
    } catch (err) {
        console.warn("Gagal memuat stroke KanjiVG CDN untuk:", character, err);
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

    // Helper data karakter lokal
    const getCached = (c) => {
        const rec = window.MIRAI_STROKE_DATA?.[c];
        return (rec && isValidStrokeRecord(rec)) ? rec : null;
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

        // Render kerangka kontrol UI pemutar lengkap
        host.innerHTML = `
            <div class="stroke-stage stroke-thick" aria-label="Animasi urutan menulis ${kanaString}"></div>
            <div class="stroke-status">Goresan <b data-stroke-number>1</b> dari ${totalStrokes}</div>
            <ol class="stroke-order" aria-label="Urutan visual goresan">${strokeThumbsHtml}</ol>
            <div class="stroke-controls" role="toolbar" aria-label="Kontrol animasi goresan">
                <button type="button" data-stroke-play aria-label="Putar animasi goresan">PUTAR ▶</button>
                ${showClearControl ? `<button type="button" data-stroke-clear aria-label="Bersihkan tampilan urutan goresan ${kanaString}">BERSIHKAN</button>` : ""}
                <label>Kecepatan<select data-stroke-speed aria-label="Kecepatan animasi stroke">
                    <option value="1.6">0.5×</option>
                    <option value="1" selected>1×</option>
                    <option value="0.72">1.5×</option>
                    <option value="0.52">2×</option>
                </select></label>
            </div>
        `;

        // Render kontainer kanvas SVG responsif
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

            // Layer 0: Garis Kotak Panduan Latihan (Genkouyoushi Practice Grid Crosshair)
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

            // Layer 1 (Dasar): Goresan Panduan Transparan Urutan (Transparent Guide Strokes)
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

            // Layer 2 (Tengah): Goresan Animasi Solid (Active Animated Strokes)
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

            // Layer 3 (Atas): Angka Penunjuk Urutan Goresan (Stroke Order Numbers)
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

        // Koleksi elemen kontrol animasi
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
            number.textContent = cleared ? "0" : String(visibleStep);

            order.forEach((item, index) => {
                item.classList.toggle("is-active", index === step && (playing || paused));
                item.classList.toggle("is-done", index < step);
            });

            numberLabels.forEach((numLabel, index) => {
                numLabel.classList.toggle("is-active", index === step && (playing || paused));
                numLabel.classList.toggle("is-done", index < step);
            });

            // Perbarui label tombol putar utama (PUTAR / JEDA / LANJUTKAN)
            if (playBtn) {
                if (playing) {
                    playBtn.innerHTML = "JEDA ⏸";
                    playBtn.setAttribute("aria-label", "Jeda animasi goresan");
                } else if (paused) {
                    playBtn.innerHTML = "LANJUTKAN ▶";
                    playBtn.setAttribute("aria-label", "Lanjutkan animasi goresan");
                } else if (step >= lines.length || cleared) {
                    playBtn.innerHTML = "PUTAR ULANG ▶";
                    playBtn.setAttribute("aria-label", "Putar ulang dari goresan pertama");
                } else {
                    playBtn.innerHTML = "PUTAR ▶";
                    playBtn.setAttribute("aria-label", "Putar animasi goresan");
                }
            }
        }

        function hideFutureStrokes() {
            lines.forEach((line, index) => {
                const length = line.getTotalLength();
                line.style.strokeDasharray = `${length}`;
                line.style.strokeDashoffset = index < step ? "0" : `${length}`;
                line.style.opacity = index < step ? "1" : "0";
            });
        }

        function renderStaticState() {
            lines.forEach((line, index) => {
                const length = line.getTotalLength();
                line.style.strokeDasharray = `${length}`;
                if (index <= step) {
                    line.style.strokeDashoffset = "0";
                    line.style.opacity = "1";
                } else {
                    line.style.strokeDashoffset = `${length}`;
                    line.style.opacity = "0";
                }
            });
            setStepLabel();
        }

        function finishCurrentStroke() {
            step += 1;
            animation = null;
            if (step >= lines.length) {
                playing = false;
                paused = false;
            }
            setStepLabel();
            if (playing) {
                drawCurrentStroke();
            }
        }

        function drawCurrentStroke() {
            if (destroyed || !playing || step >= lines.length || animation) return;
            const line = lines[step];
            const length = line.getTotalLength();
            line.style.strokeDasharray = `${length}`;
            line.style.strokeDashoffset = `${length}`;
            line.style.opacity = "1";
            setStepLabel();

            try {
                animation = line.animate(
                    [{ strokeDashoffset: length }, { strokeDashoffset: 0 }],
                    { duration: duration(), easing: "cubic-bezier(.35, 0, .2, 1)", fill: "forwards" }
                );
                animation.finished.then(finishCurrentStroke).catch(() => {});
            } catch (animErr) {
                line.style.strokeDashoffset = "0";
                finishCurrentStroke();
            }
        }

        function play() {
            if (paused) {
                resume();
                return;
            }
            if (step >= lines.length || cleared) {
                reset();
            }
            cleared = false;
            paused = false;
            playing = true;
            setStepLabel();
            drawCurrentStroke();
        }

        function pause() {
            if (animation && animation.playState === "running") {
                animation.pause();
            }
            playing = false;
            paused = true;
            setStepLabel();
        }

        function resume() {
            if (animation && animation.playState === "paused") {
                animation.play();
                playing = true;
                paused = false;
                setStepLabel();
                return;
            }
            playing = true;
            paused = false;
            setStepLabel();
            drawCurrentStroke();
        }

        function togglePlay() {
            if (playing) {
                pause();
            } else {
                play();
            }
        }

        function replay() {
            if (animation) {
                try { animation.cancel(); } catch (e) {}
                animation = null;
            }
            step = 0;
            cleared = false;
            paused = false;
            playing = true;
            hideFutureStrokes();
            setStepLabel();
            drawCurrentStroke();
        }

        function prevStep() {
            if (animation) {
                try { animation.cancel(); } catch (e) {}
                animation = null;
            }
            playing = false;
            paused = false;
            cleared = false;
            if (step > 0) {
                step -= 1;
            }
            renderStaticState();
        }

        function nextStep() {
            if (animation) {
                try { animation.cancel(); } catch (e) {}
                animation = null;
            }
            playing = false;
            paused = false;
            cleared = false;
            if (step < lines.length - 1) {
                step += 1;
            }
            renderStaticState();
        }

        function reset() {
            if (animation) {
                try { animation.cancel(); } catch (e) {}
                animation = null;
            }
            playing = false;
            paused = false;
            step = 0;
            cleared = false;
            hideFutureStrokes();
            setStepLabel();
        }

        function clear() {
            if (animation) {
                try { animation.cancel(); } catch (e) {}
                animation = null;
            }
            playing = false;
            paused = false;
            step = 0;
            cleared = true;
            hideFutureStrokes();
            setStepLabel();
        }

        function destroy() {
            destroyed = true;
            if (animation) {
                try { animation.cancel(); } catch (e) {}
                animation = null;
            }
            if (host._miraiStrokeController === internalController) {
                host._miraiStrokeController = null;
            }
        }

        // Hubungkan event listeners ke antarmuka kontrol
        host.querySelector("[data-stroke-play]")?.addEventListener("click", togglePlay);
        host.querySelector("[data-stroke-pause]")?.addEventListener("click", pause);
        host.querySelector("[data-stroke-resume]")?.addEventListener("click", resume);
        host.querySelector("[data-stroke-replay]")?.addEventListener("click", replay);
        host.querySelector("[data-stroke-prev]")?.addEventListener("click", prevStep);
        host.querySelector("[data-stroke-next]")?.addEventListener("click", nextStep);
        host.querySelector("[data-stroke-clear]")?.addEventListener("click", clear);

        speed.addEventListener("change", () => {
            if (animation && animation.playState === "running") {
                try { animation.cancel(); } catch (e) {}
                animation = null;
                drawCurrentStroke();
            }
        });

        // Interaksi klik tombol penomoran goresan (pills)
        order.forEach((item, index) => {
            item.style.cursor = "pointer";
            item.addEventListener("click", () => {
                if (animation) {
                    try { animation.cancel(); } catch (e) {}
                    animation = null;
                }
                step = index;
                playing = false;
                paused = false;
                cleared = false;
                renderStaticState();
            });
        });

        // Interaksi klik angka label di kanvas SVG
        numberLabels.forEach((numLabel, index) => {
            numLabel.style.cursor = "pointer";
            numLabel.addEventListener("click", () => {
                if (animation) {
                    try { animation.cancel(); } catch (e) {}
                    animation = null;
                }
                step = index;
                playing = false;
                paused = false;
                cleared = false;
                renderStaticState();
            });
        });

        reset();

        internalController = {
            destroy,
            play,
            pause,
            resume,
            togglePlay,
            replay,
            prev: prevStep,
            next: nextStep,
            reset,
            clear,
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

        Promise.all(characters.map((c) => window.getStrokeDataAsync(c))).then((records) => {
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

