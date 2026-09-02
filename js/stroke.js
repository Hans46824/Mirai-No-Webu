/* Animated player for local KanjiVG-derived SVG paths. */
window.createStrokePlayer = function createStrokePlayer(host, character, fallbackCount) {
    const directRecord = window.MIRAI_STROKE_DATA?.[character];
    const componentRecords = character.length > 1 ? [...character].map((part) => window.MIRAI_STROKE_DATA?.[part]).filter(Boolean) : [];
    const composite = !directRecord && componentRecords.length === character.length;
    const record = directRecord || (composite ? { viewBox: "0 0 220 160", paths: componentRecords.flatMap((item) => item.paths) } : null);
    const sourcePaths = record?.paths || [];
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
            <svg viewBox="${record?.viewBox || "0 0 220 220"}" role="img" aria-label="Urutan goresan ${character}">
                ${pathMarkup}
            </svg>
            ${fallback ? `<span class="stroke-fallback-glyph" aria-hidden="true">${character}</span>` : ""}
        </div>
        ${fallback ? '<p class="stroke-fallback">Data stroke belum tersedia untuk karakter ini.</p>' : `<p class="stroke-source">${directRecord ? "Data urutan goresan: KanjiVG" : "Animasi dua karakter: tulis kana utama, lalu kana kecil."}</p>`}
        <div class="stroke-status">Goresan <b data-stroke-number>1</b> dari ${strokeCount}</div>
        <p class="stroke-guide" data-stroke-guide>Langkah 1: ikuti garis merah dari awal hingga akhir.</p>
        <ol class="stroke-order" aria-label="Urutan goresan">${Array.from({ length: strokeCount }, (_, index) => `<li data-stroke-step="${index}">${index + 1}</li>`).join("")}</ol>
        <div class="stroke-controls"><button type="button" data-stroke-play>PLAY</button><button type="button" data-stroke-pause>PAUSE</button><button type="button" data-stroke-replay>REPLAY</button><label>Kecepatan<select data-stroke-speed aria-label="Kecepatan animasi stroke"><option value="1.6">0.5×</option><option value="1" selected>1×</option><option value="0.72">1.5×</option><option value="0.52">2×</option></select></label></div>`;

    const lines = [...host.querySelectorAll("path")];
    const number = host.querySelector("[data-stroke-number]");
    const guide = host.querySelector("[data-stroke-guide]");
    const order = [...host.querySelectorAll("[data-stroke-step]")];
    const speed = host.querySelector("[data-stroke-speed]");
    let step = 0;
    let animation;
    let playing = false;

    const duration = () => 650 * Number(speed.value);

    function setStepLabel() {
        const visibleStep = Math.min(step + 1, lines.length);
        number.textContent = String(visibleStep);
        guide.textContent = step >= lines.length ? "Selesai! Semua goresan sudah ditampilkan." : `Langkah ${visibleStep}: ikuti garis merah dari awal hingga akhir.`;
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
        setStepLabel();
        animation = line.animate(
            [{ strokeDashoffset: length }, { strokeDashoffset: 0 }],
            { duration: duration(), easing: "cubic-bezier(.35, 0, .2, 1)", fill: "forwards" }
        );
        animation.finished.then(finishCurrentStroke).catch(() => {});
    }

    function play() {
        if (step >= lines.length) reset();
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
        hideFutureStrokes();
        setStepLabel();
    }

    host.querySelector("[data-stroke-play]").addEventListener("click", play);
    host.querySelector("[data-stroke-pause]").addEventListener("click", pause);
    host.querySelector("[data-stroke-replay]").addEventListener("click", () => {
        reset();
        play();
    });
    speed.addEventListener("change", () => {
        if (animation?.playState === "running") {
            animation.cancel();
            animation = undefined;
            drawCurrentStroke();
        }
    });

    reset();
    return { destroy: () => animation?.cancel(), play, reset };
};
