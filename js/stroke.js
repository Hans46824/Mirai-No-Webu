/* Animated player for local & dynamic KanjiVG-derived SVG paths. */
window.getStrokeDataAsync = async function getStrokeDataAsync(character) {
    if (!character) return null;
    if (window.MIRAI_STROKE_DATA?.[character]) {
        return window.MIRAI_STROKE_DATA[character];
    }
    const cacheKey = "mirai_stroke_" + character;
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

    // Multi-char composite (e.g. kana digraphs)
    if (character.length > 1) {
        const parts = await Promise.all([...character].map((c) => window.getStrokeDataAsync(c)));
        if (parts.every(Boolean)) {
            const composite = {
                viewBox: "0 0 220 160",
                paths: parts.flatMap((p) => p.paths),
                source: "KanjiVG"
            };
            return composite;
        }
    }

    // Fetch official SVG from KanjiVG via jsDelivr CDN
    try {
        const cp = character.codePointAt(0);
        if (!cp) return null;
        const hex = cp.toString(16).padStart(5, "0").toLowerCase();
        const res = await fetch(`https://cdn.jsdelivr.net/gh/KanjiVG/kanjivg@master/kanji/${hex}.svg`);
        if (!res.ok) return null;
        const svgText = await res.text();
        const paths = [];
        const regex = /<path[^>]+d="([^"]+)"/g;
        let match;
        while ((match = regex.exec(svgText)) !== null) {
            paths.push(match[1]);
        }
        if (paths.length > 0) {
            const record = { viewBox: "0 0 109 109", paths, source: "KanjiVG" };
            if (!window.MIRAI_STROKE_DATA) window.MIRAI_STROKE_DATA = {};
            window.MIRAI_STROKE_DATA[character] = record;
            try {
                localStorage.setItem(cacheKey, JSON.stringify(record));
            } catch (e) {}
            return record;
        }
    } catch (err) {
        console.warn("Gagal memuat stroke KanjiVG untuk:", character, err);
    }
    return null;
};

window.createStrokePlayer = function createStrokePlayer(host, character, fallbackCount, options = {}) {
    const showClearControl = options.showClear === true;
    let destroyed = false;
    let internalController = null;

    function renderWithRecord(record) {
        if (destroyed || !host) return;
        const directRecord = record || window.MIRAI_STROKE_DATA?.[character];
        const componentRecords = character.length > 1 ? [...character].map((part) => window.MIRAI_STROKE_DATA?.[part]).filter(Boolean) : [];
        const composite = !directRecord && componentRecords.length === character.length;
        const activeRecord = directRecord || (composite ? { viewBox: "0 0 220 160", paths: componentRecords.flatMap((item) => item.paths) } : null);
        const sourcePaths = activeRecord?.paths || [];
        const fallback = !sourcePaths.length;
        const paths = fallback
            ? ["M55 52 L165 52", "M72 38 L72 172", "M52 115 L168 115", "M164 48 L164 172"].slice(0, Math.max(2, Math.min(fallbackCount || 3, 4)))
            : sourcePaths;

        const pathMarkup = composite
            ? componentRecords.map((item, componentIndex) => `<g transform="${componentIndex === 0 ? "translate(10 18) scale(1.05)" : "translate(134 72) scale(.62)"}">${item.paths.map((path, pathIndex) => `<path data-stroke="${componentIndex}-${pathIndex}" d="${path}" />`).join("")}</g>`).join("")
            : paths.map((path, index) => `<path data-stroke="${index}" d="${path}" />`).join("");
        const strokeCount = composite ? componentRecords.reduce((total, item) => total + item.paths.length, 0) : paths.length;

        host.innerHTML = `
            <div class="stroke-stage ${fallback ? "is-fallback" : ""}" aria-label="Animasi urutan menulis ${character}">
                <svg viewBox="${activeRecord?.viewBox || "0 0 220 220"}" role="img" aria-label="Urutan goresan ${character}">
                    ${pathMarkup}
                </svg>
                ${fallback ? `<span class="stroke-fallback-glyph" aria-hidden="true">${character}</span>` : ""}
            </div>
            ${fallback ? '<p class="stroke-fallback">Data stroke belum tersedia untuk karakter ini.</p>' : `<p class="stroke-source">${activeRecord?.source === "KanjiVG" || directRecord ? "Data urutan goresan: KanjiVG" : "Animasi dua karakter: tulis kana utama, lalu kana kecil."}</p>`}
            <div class="stroke-status">Goresan <b data-stroke-number>1</b> dari ${strokeCount}</div>
            <p class="stroke-guide" data-stroke-guide role="status" aria-live="polite">Langkah 1: ikuti garis merah dari awal hingga akhir.</p>
            <ol class="stroke-order" aria-label="Urutan goresan">${Array.from({ length: strokeCount }, (_, index) => `<li data-stroke-step="${index}">${index + 1}</li>`).join("")}</ol>
            <div class="stroke-controls"><button type="button" data-stroke-play>PUTAR</button><button type="button" data-stroke-pause>JEDA</button><button type="button" data-stroke-replay>ULANG</button>${showClearControl ? `<button type="button" data-stroke-clear aria-label="Bersihkan tampilan urutan goresan ${character}">BERSIHKAN</button>` : ""}<label>Kecepatan<select data-stroke-speed aria-label="Kecepatan animasi stroke"><option value="1.6">0.5×</option><option value="1" selected>1×</option><option value="0.72">1.5×</option><option value="0.52">2×</option></select></label></div>`;

        const lines = [...host.querySelectorAll("path")];
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

    const immediate = window.MIRAI_STROKE_DATA?.[character];
    if (immediate) {
        renderWithRecord(immediate);
    } else {
        // Show loading state and fetch async from KanjiVG
        host.innerHTML = `
            <div class="stroke-stage is-fallback">
                <span class="stroke-fallback-glyph" style="opacity:0.35;">${character}</span>
            </div>
            <p class="stroke-source">Memuat data goresan KanjiVG...</p>
        `;
        window.getStrokeDataAsync(character).then((record) => {
            if (!destroyed) {
                renderWithRecord(record);
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

