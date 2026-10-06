window.currentPenSize = window.currentPenSize || 'thick';

window.togglePenSize = function togglePenSize() {
    const strokeContainer = document.getElementById('stroke-stage');
    const penBtn = document.getElementById('btn-toggle-pen');

    if (strokeContainer) {
        if (strokeContainer.classList.contains('stroke-thin')) {
            strokeContainer.classList.remove('stroke-thin');
            strokeContainer.classList.add('stroke-thick');
            window.currentPenSize = 'thick';
            if (penBtn) penBtn.innerHTML = 'Kuas: Tebal 🖌️';
        } else {
            strokeContainer.classList.remove('stroke-thick');
            strokeContainer.classList.add('stroke-thin');
            window.currentPenSize = 'thin';
            if (penBtn) penBtn.innerHTML = 'Kuas: Tipis 🖊️';
        }
    } else {
        window.currentPenSize = window.currentPenSize === 'thin' ? 'thick' : 'thin';
    }

    // Sync all stroke stages and buttons across page
    document.querySelectorAll('.stroke-stage').forEach((el) => {
        if (window.currentPenSize === 'thick') {
            el.classList.remove('stroke-thin');
            el.classList.add('stroke-thick');
        } else {
            el.classList.remove('stroke-thick');
            el.classList.add('stroke-thin');
        }
    });
    document.querySelectorAll('.btn-pen-style, #btn-toggle-pen').forEach((btn) => {
        btn.innerHTML = window.currentPenSize === 'thick' ? 'Kuas: Tebal 🖌️' : 'Kuas: Tipis 🖊️';
    });
};

try {
    for (let i = localStorage.length - 1; i >= 0; i--) {
        const k = localStorage.key(i);
        if (k && (k.startsWith("mirai_stroke_v1_") || k.startsWith("mirai_stroke_v2_"))) {
            localStorage.removeItem(k);
        }
    }
} catch (e) {}

/* Animated player for local & dynamic KanjiVG-derived SVG paths. */
window.getStrokeDataAsync = async function getStrokeDataAsync(character) {
    if (!character) return null;

    // 1. Curated local data takes absolute first priority (hand-verified standard)
    if (window.MIRAI_STROKE_DATA?.[character]) {
        return window.MIRAI_STROKE_DATA[character];
    }

    const cacheKey = "mirai_stroke_v3_" + character;

    // 2. Check localStorage cache (v3)
    try {
        const cached = localStorage.getItem(cacheKey);
        if (cached) {
            const parsed = JSON.parse(cached);
            if (parsed?.paths?.length) {
                if (!window.MIRAI_STROKE_DATA) window.MIRAI_STROKE_DATA = {};
                window.MIRAI_STROKE_DATA[character] = parsed;
                return parsed;
            }
        }
    } catch (e) {}

    // Multi-char: fetch parts separately
    if (character.length > 1) {
        const parts = await Promise.all(Array.from(character).map((c) => window.getStrokeDataAsync(c)));
        if (parts.every(Boolean)) {
            return {
                isMulti: true,
                characters: Array.from(character),
                parts: parts,
                source: "KanjiVG"
            };
        }
    }

    // 3. Fetch official SVG from KanjiVG via jsDelivr CDN
    try {
        const cp = character.codePointAt(0);
        if (!cp) return null;
        const hex = cp.toString(16).padStart(5, "0").toLowerCase();
        const res = await fetch(`https://cdn.jsdelivr.net/gh/KanjiVG/kanjivg@master/kanji/${hex}.svg`);
        if (res.ok) {
            const svgText = await res.text();
            const paths = [];
            const regex = /<path[^>]+d="([^"]+)"/g;
            let match;
            while ((match = regex.exec(svgText)) !== null) {
                paths.push(match[1]);
            }
            const numbers = [];
            const numRegex = /<text[^>]+transform="matrix\([^)]+\s+([\d\.]+)\s+([\d\.]+)\)"[^>]*>([^<]+)<\/text>/g;
            let numMatch;
            while ((numMatch = numRegex.exec(svgText)) !== null) {
                numbers.push({
                    x: parseFloat(numMatch[1]),
                    y: parseFloat(numMatch[2]),
                    text: numMatch[3].trim()
                });
            }
            if (paths.length > 0) {
                const record = { viewBox: "0 0 109 109", paths, numbers, source: "KanjiVG-CDN" };
                if (!window.MIRAI_STROKE_DATA) window.MIRAI_STROKE_DATA = {};
                window.MIRAI_STROKE_DATA[character] = record;
                try {
                    localStorage.setItem(cacheKey, JSON.stringify(record));
                } catch (e) {}
                return record;
            }
        }
    } catch (err) {
        console.warn("Gagal memuat stroke KanjiVG CDN untuk:", character, err);
    }

    // 4. Fallback if any
    if (window.MIRAI_STROKE_DATA?.[character]) {
        return window.MIRAI_STROKE_DATA[character];
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
            const off = officialNumbers[i];
            const dist = Math.hypot(off.x - sx, off.y - sy);
            // Validasi: nomor tidak boleh terlalu jauh dari awal goresan (<= 20) dan dalam batas kanvas yang nyaman [9, 100]
            if (dist <= 20 && off.x >= 9 && off.x <= 100 && off.y >= 9 && off.y <= 100) {
                nx = off.x;
                ny = off.y;
            } else {
                // Re-anchor dekat titik awal goresan agar tidak melenceng jauh
                nx = sx >= 12 ? sx - 6.5 : sx + 6;
                ny = sy >= 12 ? sy - 2.5 : sy + 7;
            }
        } else {
            nx = sx >= 12 ? sx - 6.5 : sx + 6;
            ny = sy >= 12 ? sy - 2.5 : sy + 7;
        }

        // Hindari tabrakan visual antar-label nomor
        for (let attempt = 0; attempt < 5; attempt++) {
            let collision = false;
            for (let j = 0; j < placed.length; j++) {
                const dx = nx - placed[j].x;
                const dy = ny - placed[j].y;
                if (Math.hypot(dx, dy) < 7.5) {
                    collision = true;
                    break;
                }
            }
            if (collision) {
                if (ny > 16) {
                    ny -= 5.5;
                } else {
                    nx += 6.5;
                }
            } else {
                break;
            }
        }

        nx = Math.max(7, Math.min(101, nx));
        ny = Math.max(9, Math.min(102, ny));

        placed.push({
            x: nx,
            y: ny,
            text: (hasOfficial && officialNumbers[i]?.text) ? officialNumbers[i].text : String(i + 1)
        });
    });

    return placed;
}

window.createStrokePlayer = function createStrokePlayer(host, kanaString, fallbackCount, options = {}) {

    if (!kanaString || !host) return null;
    const showClearControl = options.showClear === true;
    let destroyed = false;
    let internalController = null;

    const characters = Array.from(kanaString);
    const isMulti = characters.length > 1;

    // Helper to get cached character record
    const getCached = (c) => window.MIRAI_STROKE_DATA?.[c];
    const allImmediate = characters.every(getCached);

    function setupPlayerWithRecords(records) {
        if (destroyed || !host) return;

        // Calculate total strokes
        let totalStrokes = 0;
        records.forEach((rec) => {
            if (rec?.paths?.length) {
                totalStrokes += rec.paths.length;
            }
        });
        if (totalStrokes === 0) {
            totalStrokes = Math.max(2, Math.min(fallbackCount || 3, 4)) * characters.length;
        }

        const currentPenClass = window.currentPenSize === 'thick' ? 'stroke-thick' : 'stroke-thin';
        const currentPenLabel = window.currentPenSize === 'thick' ? 'Kuas: Tebal 🖌️' : 'Kuas: Tipis 🖊️';

        // Render external controls skeleton
        host.innerHTML = `
            <div class="stroke-stage ${currentPenClass}" id="stroke-stage" aria-label="Animasi urutan menulis ${kanaString}"></div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin:8px 0 4px; gap:10px;">
                <p class="stroke-source" style="margin:0;">${isMulti ? "Animasi multi-karakter" : "Standar Penulisan Karakter Jepang"}</p>
                <button id="btn-toggle-pen" class="btn-pen-style" type="button" onclick="togglePenSize()">${currentPenLabel}</button>
            </div>
            <div class="stroke-status">Goresan <b data-stroke-number>1</b> dari ${totalStrokes}</div>
            <p class="stroke-guide" data-stroke-guide role="status" aria-live="polite">Ikuti angka urutan goresan di kanvas atau tekan PUTAR untuk animasi.</p>
            <ol class="stroke-order" aria-label="Urutan goresan">${Array.from({ length: totalStrokes }, (_, index) => `<li data-stroke-step="${index}">${index + 1}</li>`).join("")}</ol>
            <div class="stroke-controls">
                <button type="button" data-stroke-play>PUTAR</button>
                ${showClearControl ? `<button type="button" data-stroke-clear aria-label="Bersihkan tampilan urutan goresan ${kanaString}">BERSIHKAN</button>` : ""}
                <label>Kecepatan<select data-stroke-speed aria-label="Kecepatan animasi stroke">
                    <option value="1.6">0.5×</option>
                    <option value="1" selected>1×</option>
                    <option value="0.72">1.5×</option>
                    <option value="0.52">2×</option>
                </select></label>
            </div>
        `;

        // 2. Isolasi Instance Render (JS)
        const strokeStage = host.querySelector('.stroke-stage');
        strokeStage.innerHTML = "";
        strokeStage.style.display = 'flex';
        strokeStage.style.flexDirection = 'row';
        strokeStage.style.justifyContent = 'center';
        strokeStage.style.alignItems = 'center';
        strokeStage.style.gap = '10px';
        strokeStage.style.flexWrap = 'wrap';

        let globalStrokeOffset = 0;

        Array.from(kanaString).forEach((char, index) => {
            let charWrapper = document.createElement('div');
            charWrapper.id = 'stroke-char-' + index;
            charWrapper.className = 'kanjivg-char-box';
            charWrapper.style.position = 'relative';

            if (isMulti) {
                charWrapper.style.width = '90px';
                charWrapper.style.height = '90px';
            } else {
                charWrapper.style.width = '200px';
                charWrapper.style.height = '200px';
                charWrapper.classList.add('single-char');
            }

            const rec = records[index];
            const paths = rec?.paths?.length
                ? rec.paths
                : ["M55 52 L165 52", "M72 38 L72 172", "M52 115 L168 115", "M164 48 L164 172"].slice(0, Math.max(2, Math.min(fallbackCount || 3, 4)));

            let svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
            svg.setAttribute("viewBox", rec?.viewBox || "0 0 109 109");
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

            // Layer 1: Bentuk Asli Karakter Standar (Ghost Reference Glyph)
            const bgGlyph = document.createElementNS("http://www.w3.org/2000/svg", "text");
            bgGlyph.setAttribute("x", "54.5");
            bgGlyph.setAttribute("y", "54.5");
            bgGlyph.setAttribute("text-anchor", "middle");
            bgGlyph.setAttribute("dominant-baseline", "central");
            bgGlyph.setAttribute("class", "stroke-bg-reference-glyph");
            bgGlyph.setAttribute("aria-hidden", "true");
            bgGlyph.textContent = char;
            svg.appendChild(bgGlyph);

            // Layer 2 (Dasar): Goresan Panduan Transparan (Transparent Guide Strokes)
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

            // Layer 3 (Tengah): Goresan Animasi Solid (Active Animated Strokes)
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

            // Layer 4 (Atas): Angka Penunjuk Urutan Goresan (Stroke Order Numbers)
            const numbersGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
            numbersGroup.setAttribute("class", "stroke-numbers-group");
            const numPositions = calculateStrokeNumbers(paths, rec?.numbers);
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

            if (!rec?.paths?.length) {
                const fallbackSpan = document.createElement('span');
                fallbackSpan.className = 'stroke-fallback-glyph';
                fallbackSpan.textContent = char;
                fallbackSpan.style.fontSize = isMulti ? '50px' : '130px';
                charWrapper.appendChild(fallbackSpan);
            }

            // Append ke container utama
            strokeStage.appendChild(charWrapper);
        });

        // Kumpulkan semua path aktif berurutan secara kronologis
        const lines = [...strokeStage.querySelectorAll("path[data-stroke]")];
        const numberLabels = [...strokeStage.querySelectorAll(".stroke-number-label")];
        const number = host.querySelector("[data-stroke-number]");
        const guide = host.querySelector("[data-stroke-guide]");
        const order = [...host.querySelectorAll("[data-stroke-step]")];
        const speed = host.querySelector("[data-stroke-speed]");
        let step = 0;
        let animation;
        let playing = false;
        let cleared = false;

        const duration = () => 650 * Number(speed.value);

        function setStepLabel() {
            const visibleStep = Math.min(step + 1, lines.length);
            number.textContent = cleared ? "0" : String(visibleStep);
            guide.textContent = cleared
                ? "Tampilan goresan dibersihkan. Tekan PUTAR untuk menampilkan ulang."
                : step >= lines.length
                    ? "Selesai! Semua goresan sudah ditampilkan."
                    : (playing
                        ? `Memutar goresan ke-${visibleStep} dari ${lines.length}...`
                        : `Langkah ${visibleStep}: ikuti goresan pink atau angka urutan di atas.`);
            order.forEach((item, index) => {
                item.classList.toggle("is-active", index === step && playing);
                item.classList.toggle("is-done", index < step);
            });
            numberLabels.forEach((numLabel, index) => {
                numLabel.classList.toggle("is-active", index === step && playing);
                numLabel.classList.toggle("is-done", index < step);
            });
        }

        function hideFutureStrokes() {
            lines.forEach((line, index) => {
                const length = line.getTotalLength();
                line.style.strokeDasharray = `${length}`;
                line.style.strokeDashoffset = index < step ? "0" : `${length}`;
                line.style.opacity = index < step ? "1" : "0";
            });
        }

        function finishCurrentStroke() {
            step += 1;
            animation = undefined;
            if (step >= lines.length) playing = false;
            setStepLabel();
            if (playing) drawCurrentStroke();
        }

        function drawCurrentStroke() {
            if (!playing || step >= lines.length || animation) return;
            const line = lines[step];
            const length = line.getTotalLength();
            line.style.strokeDasharray = `${length}`;
            line.style.strokeDashoffset = `${length}`;
            line.style.opacity = "1";
            setStepLabel();
            animation = line.animate(
                [{ strokeDashoffset: length }, { strokeDashoffset: 0 }],
                { duration: duration(), easing: "cubic-bezier(.35, 0, .2, 1)", fill: "forwards" }
            );
            animation.finished.then(finishCurrentStroke).catch(() => {});
        }

        function play() {
            if (playing && animation) {
                reset();
            } else if (step >= lines.length) {
                reset();
            }
            cleared = false;
            playing = true;
            if (animation?.playState === "paused") {
                animation.play();
                setStepLabel();
                return;
            }
            drawCurrentStroke();
        }

        function pause() {
            if (!animation || animation.playState !== "running") return;
            animation.pause();
            playing = false;
            setStepLabel();
        }

        function reset() {
            animation?.cancel();
            animation = undefined;
            playing = false;
            step = 0;
            cleared = false;
            hideFutureStrokes();
            setStepLabel();
        }

        function clear() {
            animation?.cancel();
            animation = undefined;
            playing = false;
            step = 0;
            cleared = true;
            hideFutureStrokes();
            setStepLabel();
        }

        host.querySelector("[data-stroke-play]").addEventListener("click", play);
        host.querySelector("[data-stroke-pause]")?.addEventListener("click", pause);
        host.querySelector("[data-stroke-replay]")?.addEventListener("click", () => {
            reset();
            play();
        });
        host.querySelector("[data-stroke-clear]")?.addEventListener("click", clear);
        speed.addEventListener("change", () => {
            if (animation?.playState === "running") {
                animation.cancel();
                animation = undefined;
                drawCurrentStroke();
            }
        });

        // Interaksi klik angka urutan: pengguna bisa klik angka di kanvas atau di bawah untuk melihat goresan
        order.forEach((item, index) => {
            item.style.cursor = "pointer";
            item.title = `Lihat goresan ke-${index + 1}`;
            item.addEventListener("click", () => {
                animation?.cancel();
                animation = undefined;
                step = index;
                cleared = false;
                playing = true;
                hideFutureStrokes();
                drawCurrentStroke();
            });
        });

        numberLabels.forEach((numLabel, index) => {
            numLabel.style.cursor = "pointer";
            numLabel.addEventListener("click", () => {
                animation?.cancel();
                animation = undefined;
                step = index;
                cleared = false;
                playing = true;
                hideFutureStrokes();
                drawCurrentStroke();
            });
        });

        reset();
        internalController = { destroy: () => animation?.cancel(), play, reset, clear };
    }

    if (allImmediate) {
        setupPlayerWithRecords(characters.map(getCached));
    } else {
        // Show loading state and fetch async per character from KanjiVG
        host.innerHTML = `
            <div class="stroke-stage is-fallback">
                <span class="stroke-fallback-glyph" style="opacity:0.35;">${kanaString}</span>
            </div>
            <p class="stroke-source">Memuat data goresan KanjiVG...</p>
        `;
        Promise.all(characters.map((c) => window.getStrokeDataAsync(c))).then((records) => {
            if (!destroyed) {
                setupPlayerWithRecords(records);
            }
        });
    }

    return {
        destroy: () => {
            destroyed = true;
            internalController?.destroy();
        },
        play: () => internalController?.play(),
        reset: () => internalController?.reset(),
        clear: () => internalController?.clear()
    };
};
