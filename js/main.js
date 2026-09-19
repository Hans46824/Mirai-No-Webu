document.addEventListener("DOMContentLoaded", () => {
    normalizeNavigation();
    setupThemeToggle();
    setupMenu();
    setupSidebarNav();
    setupBackToTop();
    setupReveal();
    setupInstagramFeedback();
    setupLearningPanel();
    setupManagementSlider();
    window.initKanjiDictionary?.();
    window.initSora?.();
});

function setupThemeToggle() {
    // Website dikunci 100% pada Light Mode
    try {
        localStorage.removeItem("mirai-no-hana-theme");
    } catch (e) {}
    document.body.classList.remove("theme-dark", "dark-mode");
    const toggle = document.querySelector(".theme-toggle, .dark-mode-toggle");
    if (toggle) toggle.remove();
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

    // Re-enable all navigation links (Coming Soon overlay removed).
    document.querySelectorAll('[data-nav-menu] a.nav-coming-soon, .nav .links a.nav-coming-soon').forEach((link) => {
        const navText = link.querySelector('.nav-text');
        const label = navText ? navText.textContent.trim().toUpperCase() : link.textContent.replace('COMING SOON', '').trim().toUpperCase();
        const href = (label === 'HOME' || label === 'BERANDA') ? 'index.html' : label === 'KEGIATAN' ? 'kegiatan.html' : label === 'TENTANG' ? 'tentang.html' : link.getAttribute('href');
        link.setAttribute('href', href);
        link.removeAttribute('aria-disabled');
        link.removeAttribute('tabindex');
        link.removeAttribute('title');
        link.classList.remove('nav-coming-soon');
        link.textContent = label;
    });

    // Re-enable brand links that were disabled.
    document.querySelectorAll('.brand.brand-disabled').forEach((brand) => {
        brand.classList.remove('brand-disabled');
        brand.setAttribute('href', 'index.html');
        brand.removeAttribute('aria-disabled');
        brand.removeAttribute('tabindex');
        brand.removeAttribute('title');
    });
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

function setupSidebarNav() {
    const menuBtn = document.querySelector(".menu-btn");
    const closeBtn = document.querySelector(".close-btn");
    const sidebarNav = document.querySelector(".sidebar-nav");
    const sidebarOverlay = document.querySelector(".sidebar-overlay");

    const openSidebar = () => {
        sidebarNav.classList.add("active");
        if (sidebarOverlay) sidebarOverlay.classList.add("active");
        document.body.classList.add("sidebar-open");
        if (menuBtn) {
            menuBtn.setAttribute("aria-expanded", "true");
            menuBtn.style.opacity = "0";
            menuBtn.style.visibility = "hidden";
            menuBtn.style.pointerEvents = "none";
        }
    };

    const closeSidebar = () => {
        sidebarNav.classList.remove("active");
        if (sidebarOverlay) sidebarOverlay.classList.remove("active");
        document.body.classList.remove("sidebar-open");
        if (menuBtn) {
            menuBtn.setAttribute("aria-expanded", "false");
            menuBtn.style.opacity = "";
            menuBtn.style.visibility = "";
            menuBtn.style.pointerEvents = "";
        }
    };

    if (menuBtn && sidebarNav && !menuBtn.dataset.sidebarInit) {
        menuBtn.dataset.sidebarInit = "true";
        menuBtn.addEventListener("click", openSidebar);
    }

    if (closeBtn && sidebarNav) {
        closeBtn.addEventListener("click", closeSidebar);
    }

    if (sidebarOverlay && sidebarNav) {
        sidebarOverlay.addEventListener("click", closeSidebar);
    }

    // Close on escape key
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && sidebarNav && sidebarNav.classList.contains("active")) {
            closeSidebar();
        }
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

function setupManagementSlider() {
    const track = document.getElementById("mgmtSliderTrack");
    if (!track) return;

    const slides = track.querySelectorAll(".mgmt-slide");
    const tabs = document.querySelectorAll(".mgmt-tab-btn");
    const prevBtn = document.getElementById("mgmtPrevBtn");
    const nextBtn = document.getElementById("mgmtNextBtn");
    const indicator = document.getElementById("mgmtPageIndicator");
    const totalSlides = slides.length;
    let currentIndex = 0;

    function updateState(index) {
        currentIndex = Math.max(0, Math.min(index, totalSlides - 1));
        tabs.forEach((tab, i) => {
            tab.classList.toggle("active", i === currentIndex);
            tab.setAttribute("aria-selected", String(i === currentIndex));
        });
        if (indicator) {
            indicator.textContent = `${currentIndex + 1} / ${totalSlides}`;
        }
        if (prevBtn) prevBtn.style.opacity = currentIndex === 0 ? "0.45" : "1";
        if (nextBtn) nextBtn.style.opacity = currentIndex === totalSlides - 1 ? "0.45" : "1";
    }

    function scrollToSlide(index) {
        currentIndex = Math.max(0, Math.min(index, totalSlides - 1));
        const slideWidth = track.clientWidth;
        track.scrollTo({
            left: currentIndex * slideWidth,
            behavior: "smooth"
        });
        updateState(currentIndex);
    }

    tabs.forEach((tab) => {
        tab.addEventListener("click", () => {
            const targetIndex = parseInt(tab.dataset.mgmtTarget, 10) || 0;
            scrollToSlide(targetIndex);
        });
    });

    prevBtn?.addEventListener("click", () => {
        scrollToSlide(currentIndex - 1);
    });

    nextBtn?.addEventListener("click", () => {
        scrollToSlide(currentIndex + 1);
    });

    let scrollTimeout;
    track.addEventListener("scroll", () => {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
            const slideWidth = track.clientWidth || 1;
            const newIndex = Math.round(track.scrollLeft / slideWidth);
            if (newIndex !== currentIndex) {
                updateState(newIndex);
            }
        }, 60);
    }, { passive: true });

    updateState(0);
}
