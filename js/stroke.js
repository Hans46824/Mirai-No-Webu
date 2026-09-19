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

/* Animated player for local & dynamic KanjiVG-derived SVG paths. */
window.getStrokeDataAsync = async function getStrokeDataAsync(character) {
    if (!character) return null;

    const cacheKey = "mirai_stroke_v2_" + character;

    // 1. Check localStorage cache first (previously fetched from CDN = accurate)
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

    // 2. Fetch official accurate SVG from KanjiVG via jsDelivr CDN
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
            if (paths.length > 0) {
                const record = { viewBox: "0 0 109 109", paths, source: "KanjiVG-CDN" };
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

    // 3. Fallback: use local stroke-data.js (offline backup, may be less accurate)
    if (window.MIRAI_STROKE_DATA?.[character]) {
        return window.MIRAI_STROKE_DATA[character];
    }

    return null;
};

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
                <p class="stroke-source" style="margin:0;">${isMulti ? "Animasi multi-karakter (KanjiVG)" : "Data urutan goresan: KanjiVG"}</p>
                <button id="btn-toggle-pen" class="btn-pen-style" type="button" onclick="togglePenSize()">${currentPenLabel}</button>
            </div>
            <div class="stroke-status">Goresan <b data-stroke-number>1</b> dari ${totalStrokes}</div>
            <p class="stroke-guide" data-stroke-guide role="status" aria-live="polite">Langkah 1: ikuti garis merah dari awal hingga akhir.</p>
            <ol class="stroke-order" aria-label="Urutan goresan">${Array.from({ length: totalStrokes }, (_, index) => `<li data-stroke-step="${index}">${index + 1}</li>`).join("")}</ol>
            <div class="stroke-controls">
                <button type="button" data-stroke-play>PUTAR</button>
                <button type="button" data-stroke-pause>JEDA</button>
                <button type="button" data-stroke-replay>ULANG</button>
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
        // - Kosongkan container utama
        const strokeStage = host.querySelector('.stroke-stage');
        strokeStage.innerHTML = "";
        // - Jadikan container utama flexbox
        strokeStage.style.display = 'flex';
        strokeStage.style.flexDirection = 'row';
        strokeStage.style.justifyContent = 'center';
        strokeStage.style.alignItems = 'center';
        strokeStage.style.gap = '10px';
        strokeStage.style.flexWrap = 'wrap';

        // - Gunakan Array.from(kanaString).forEach((char, index) => { ... })
        Array.from(kanaString).forEach((char, index) => {
            // 3. Buat Container Unik: Di DALAM forEach
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

            // 4 & 5. Isolasi Tag SVG:
            // Pastikan hasil akhir di DOM adalah: SETIAP charWrapper memiliki SATU tag <svg viewBox="0 0 109 109"> di dalamnya.
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

            paths.forEach((d, pathIndex) => {
                const pathEl = document.createElementNS("http://www.w3.org/2000/svg", "path");
                pathEl.setAttribute("data-stroke", `${index}-${pathIndex}`);
                pathEl.setAttribute("d", d);
                pathEl.setAttribute("stroke-linecap", "round");
                pathEl.setAttribute("stroke-linejoin", "round");
                pathEl.setAttribute("fill", "none");
                svg.appendChild(pathEl);
            });

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

        // Kumpulkan semua path berurutan secara chronologis
        const lines = [...strokeStage.querySelectorAll("path")];
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
                    : `Langkah ${visibleStep}: ikuti garis merah dari awal hingga akhir.`;
            order.forEach((item, index) => {
                item.classList.toggle("is-active", index === step && playing);
                item.classList.toggle("is-done", index < step);
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
            if (step >= lines.length) reset();
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
        host.querySelector("[data-stroke-pause]").addEventListener("click", pause);
        host.querySelector("[data-stroke-replay]").addEventListener("click", () => {
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
