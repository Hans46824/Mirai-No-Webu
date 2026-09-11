document.addEventListener("DOMContentLoaded", () => {
    normalizeNavigation();
    setupThemeToggle();
    setupMenu();
    setupBackToTop();
    setupReveal();
    setupInstagramFeedback();
    setupLearningPanel();
    window.initKanjiDictionary?.();
    window.initSora?.();
});

function setupThemeToggle() {
    const storageKey = "mirai-no-hana-theme";
    const savedTheme = localStorage.getItem(storageKey);
    const prefersDark = window.matchMedia?.("(prefers-color-scheme: dark)").matches;
    const useDarkTheme = savedTheme ? savedTheme === "dark" : prefersDark;
    const header = document.querySelector(".nav");

    document.body.classList.toggle("theme-dark", useDarkTheme);
    if (!header) return;

    const button = document.createElement("button");
    button.className = "theme-toggle";
    button.type = "button";
    button.setAttribute("aria-pressed", String(useDarkTheme));

    function updateLabel(isDark) {
        button.innerHTML = isDark
            ? '<span aria-hidden="true">☀</span> MODE TERANG'
            : '<span aria-hidden="true">☾</span> MODE MALAM';
        button.setAttribute("aria-label", isDark ? "Aktifkan mode terang" : "Aktifkan mode malam");
    }

    updateLabel(useDarkTheme);
    button.addEventListener("click", () => {
        const isDark = !document.body.classList.contains("theme-dark");
        document.body.classList.toggle("theme-dark", isDark);
        localStorage.setItem(storageKey, isDark ? "dark" : "light");
        button.setAttribute("aria-pressed", String(isDark));
        updateLabel(isDark);
    });
    header.appendChild(button);
}

function setupLearningPanel() {
}

function setupInstagramFeedback() {
    const form = document.querySelector("[data-instagram-feedback]");
    if (!form) return;

    // Ganti nilai ini saat username Instagram resmi MIRAI NO HANA sudah tersedia.
    const INSTAGRAM_USERNAME = "mirainohana.id";

    form.addEventListener("submit", (event) => {
        event.preventDefault();
        const formData = new FormData(form);
        const message = [
            "Halo MIRAI NO HANA, saya ingin menyampaikan masukan.",
            "",
            `Nama: ${formData.get("name")}`,
            `Kelas: ${formData.get("class")}`,
            `Pesan: ${formData.get("message")}`
        ].join("\n");

        navigator.clipboard?.writeText(message).catch(() => {});
        window.open(`https://ig.me/m/${INSTAGRAM_USERNAME}`, "_blank", "noopener,noreferrer");
    });
}

function normalizeNavigation() {
    document.querySelectorAll('[data-nav-menu] a[href="kanji.html"]').forEach((link) => { link.href = "kamus.html"; link.textContent = "KAMUS"; });
    document.querySelectorAll('[data-nav-menu] a[href="about.html"]').forEach((link) => { link.href = "tentang.html"; });
}

function setupMenu() {
    const toggle = document.querySelector("[data-menu-toggle]");
    const menu = document.querySelector("[data-nav-menu]");
    if (!toggle || !menu) return;

    toggle.addEventListener("click", () => {
        const isOpen = menu.classList.toggle("is-open");
        toggle.setAttribute("aria-expanded", String(isOpen));
    });
}

function setupBackToTop() {
    const button = document.querySelector(".to-top");
    if (!button) return;

    const update = () => button.classList.toggle("is-visible", window.scrollY > 480);
    update();
    window.addEventListener("scroll", update, { passive: true });
    button.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
}

function setupReveal() {
    const targets = document.querySelectorAll(".reveal");
    if (!("IntersectionObserver" in window)) {
        targets.forEach((target) => target.classList.add("is-visible"));
        return;
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (!entry.isIntersecting) return;
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
        });
    }, { threshold: 0.12 });

    targets.forEach((target) => observer.observe(target));
}

async function setupKanjiDictionary() {
    const dictionary = document.querySelector("[data-kanji-dictionary]");
    if (!dictionary) return;

    const grid = dictionary.querySelector("[data-kanji-grid]");
    const count = dictionary.querySelector("[data-kanji-count]");
    const empty = dictionary.querySelector("[data-kanji-empty]");
    const detail = dictionary.querySelector("[data-kanji-detail]");
    const search = dictionary.querySelector("[data-kanji-search]");
    const jlpt = dictionary.querySelector("[data-kanji-jlpt]");
    const level = dictionary.querySelector("[data-kanji-level]");
    let kanjiData = [];

    try {
        const response = await fetch("data/kanji.json");
        if (!response.ok) throw new Error("Data Kamus Kanji tidak dapat dimuat.");
        kanjiData = await response.json();
    } catch (error) {
        count.textContent = "Data kamus belum dapat dimuat.";
        return;
    }

    function matches(item) {
        const query = search.value.toLowerCase().trim();
        const searchable = [
            item.kanji,
            item.meaning,
            ...item.onyomi,
            ...item.kunyomi,
            ...item.words.flatMap((word) => [word.word, word.reading, word.meaning])
        ].join(" ").toLowerCase();
        return (!query || searchable.includes(query)) &&
            (!jlpt.value || item.jlpt === jlpt.value) &&
            (!level.value || item.level === level.value);
    }

    function renderDetail(item) {
        detail.innerHTML = `
            <div class="kanji-detail-head">
                <strong>${item.kanji}</strong>
                <div><p class="card-number">${item.jlpt} / ${item.level}</p><h3>${item.meaning}</h3><p><b>Onyomi:</b> ${item.onyomi.join(", ") || "—"}<br><b>Kunyomi:</b> ${item.kunyomi.join(", ") || "—"}</p></div>
            </div>
            <h4>Kosakata contoh</h4>
            <ul>${item.words.map((word) => `<li><b>${word.word}</b> <span>${word.reading}</span> — ${word.meaning}</li>`).join("")}</ul>
            <h4>Contoh kalimat</h4>
            <p class="sentence"><b>${item.sentence.japanese}</b><br><span>${item.sentence.reading}</span><br>${item.sentence.meaning}</p>`;
    }

    function render() {
        const visible = kanjiData.filter(matches);
        grid.innerHTML = "";
        count.textContent = `Menampilkan ${visible.length} kanji`;
        empty.hidden = visible.length > 0;
        visible.forEach((item) => {
            const button = document.createElement("button");
            button.className = "kanji-card";
            button.type = "button";
            button.innerHTML = `<strong>${item.kanji}</strong><span>${item.meaning}</span><em>${item.jlpt}</em>`;
            button.addEventListener("click", () => renderDetail(item));
            grid.appendChild(button);
        });
        if (visible.length) renderDetail(visible[0]);
    }

    [search, jlpt, level].forEach((control) => {
        control.addEventListener("input", render);
        control.addEventListener("change", render);
    });
    render();
}

function setupSora() {
    let widget = document.querySelector("[data-sora]");
    if (!widget && window.SoraService) {
        widget = document.createElement("aside");
        widget.className = "sora-widget";
        widget.dataset.sora = "";
        widget.setAttribute("aria-label", "Asisten Sora");
        widget.innerHTML = [
            '<button class="sora-toggle" type="button" data-sora-toggle aria-expanded="false"><img src="images/mirai/icon/Ay.png" alt=""><span>SORA</span></button>',
            '<div class="sora-panel" data-sora-panel hidden><header><strong>Sora ✨</strong><span>Teman belajar bahasa Jepangmu.</span><button class="sora-close" type="button" data-sora-close aria-label="Tutup Sora">×</button></header>',
            '<div class="sora-messages" data-sora-messages><p class="chat-message sora">Yatta! Aku Sora ✨ Ada yang bisa kubantu?</p></div>',
            '<form class="sora-form" data-sora-form><input data-sora-input aria-label="Tanya Sora" placeholder="Tanya Sora sesuatu..." required><button type="submit">Kirim</button></form></div>'
        ].join("");
        document.body.appendChild(widget);
    }
    if (!widget || !window.SoraService) return;

    const toggle = widget.querySelector("[data-sora-toggle]");
    const panel = widget.querySelector("[data-sora-panel]");
    const form = widget.querySelector("[data-sora-form]");
    const input = widget.querySelector("[data-sora-input]");
    const messages = widget.querySelector("[data-sora-messages]");
    const close = widget.querySelector("[data-sora-close]");

    toggle.addEventListener("click", () => {
        const isOpen = panel.hidden;
        panel.hidden = !isOpen;
        toggle.setAttribute("aria-expanded", String(isOpen));
        if (isOpen) input.focus();
    });

    close?.addEventListener("click", () => {
        panel.hidden = true;
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
    });

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const message = input.value.trim();
        if (!message) return;
        appendMessage(messages, message, "user");
        input.value = "";
        const pending = appendMessage(messages, "Sora sedang mengetik…", "sora is-loading");
        try {
            const reply = await window.SoraService.sendMessage(message);
            pending.remove();
            appendMessage(messages, reply, "sora");
        } catch (error) {
            pending.remove();
            appendMessage(messages, error.message || "Maaf, Sora sedang mengalami gangguan. Coba lagi ya.", "sora is-error");
        }
    });
}

function appendMessage(container, text, author) {
    const message = document.createElement("p");
    message.className = "chat-message " + author;
    message.textContent = text;
    container.appendChild(message);
    container.scrollTop = container.scrollHeight;
    return message;
}
