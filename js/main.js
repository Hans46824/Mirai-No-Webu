/**
 * File: js/main.js
 * Fungsi: Pengendali UI global (navbar, sidebar drawer, hero sticky curtain, back-to-top, scroll reveal, dan tema).
 * Penggunaan: Universal di seluruh 30 halaman HTML website (index.html, tentang, kelas, kegiatan, divisi, lomba, toko, dll.).
 */

document.addEventListener("DOMContentLoaded", () => {
    normalizeNavigation();
    setupThemeToggle();
    setupMenu();
    setupSidebarNav();
    setupBackToTop();
    setupReveal();
    setupHeroContentScroll();
    setupInstagramFeedback();
    setupLearningPanel();
    setupManagementSlider();
    setupImageLightbox();
    setupFooterQuoteSlider();
    setupExpandableCards();
    initMiraiProgress();
    window.initKanjiDictionary?.();
    window.initSora?.();
});

function setupHeroContentScroll() {
    // Efek sticky curtain dan ascending text (solid 100% tanpa transparansi) untuk seluruh hero
    const hero = document.querySelector(".hero, .page-hero, .proker-hero, .quest-hero, .toko-hero, .class-hero, .about-hero, .activities-hero, .rekomendasi-hero, .peringkat-hero, .lomba-hero, .motivasi-hero");
    if (!hero) return;

    const heroContent = hero.querySelector(".hero-text-box, .hero-content, .proker-hero-inner, .page-hero > div:not(.hero-social-sidebar), .quest-hero > div:not(.hero-social-sidebar), .toko-hero > div:not(.hero-social-sidebar), div:not(.hero-social-sidebar):not(.proker-back-wrap)");
    const heroSocial = hero.querySelector(".hero-social-sidebar");

    let ticking = false;

    function update() {
        const scrollY = window.pageYOffset || document.documentElement.scrollTop;
        const heroHeight = hero.offsetHeight || window.innerHeight;

        if (scrollY <= heroHeight) {
            // Hero aktif di viewport
            hero.style.visibility = "visible";
            const translateY = scrollY * 1.0;

            if (heroContent) {
                heroContent.style.transform = `translate3d(0, -${translateY}px, 0)`;
            }
            if (heroSocial) {
                heroSocial.style.transform = `translate3d(0, -${translateY}px, 0)`;
            }
        } else {
            // Begitu seksi berikutnya sudah menutupi hero secara penuh,
            // sembunyikan hero agar background Sora tidak pernah tembus di seksi bawah!
            hero.style.visibility = "hidden";
            if (heroContent) {
                heroContent.style.transform = `translate3d(0, -${heroHeight}px, 0)`;
            }
            if (heroSocial) {
                heroSocial.style.transform = `translate3d(0, -${heroHeight}px, 0)`;
            }
        }

        ticking = false;
    }

    window.addEventListener("scroll", () => {
        if (!ticking) {
            window.requestAnimationFrame(update);
            ticking = true;
        }
    }, { passive: true });

    update();
}

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

function normalizeNavigation() {
    const basePath = getAppBasePath();
    document.querySelectorAll('[data-nav-menu] a[href$="kanji.html"]').forEach((link) => {
        link.href = basePath + "kamus/index.html";
        link.textContent = "KAMUS";
    });
    document.querySelectorAll('[data-nav-menu] a[href$="about.html"]').forEach((link) => {
        link.href = basePath + "tentang/index.html";
    });

    // Aktifkan kembali seluruh tautan navigasi (lapisan Coming Soon telah dihapus).
    document.querySelectorAll('[data-nav-menu] a.nav-coming-soon, .nav .links a.nav-coming-soon').forEach((link) => {
        const navText = link.querySelector('.nav-text');
        const label = navText ? navText.textContent.trim().toUpperCase() : link.textContent.replace('COMING SOON', '').trim().toUpperCase();
        const href = (label === 'HOME' || label === 'BERANDA') ? basePath + 'index.html' : label === 'KEGIATAN' ? basePath + 'kegiatan/index.html' : label === 'TENTANG' ? basePath + 'tentang/index.html' : link.getAttribute('href');
        link.setAttribute('href', href);
        link.removeAttribute('aria-disabled');
        link.removeAttribute('tabindex');
        link.removeAttribute('title');
        link.classList.remove('nav-coming-soon');
        link.textContent = label;
    });

    // Aktifkan kembali tautan brand yang sebelumnya dinonaktifkan.
    document.querySelectorAll('.brand.brand-disabled').forEach((brand) => {
        brand.classList.remove('brand-disabled');
        brand.setAttribute('href', basePath + 'index.html');
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

    // Tutup saat tombol Escape ditekan
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
    // 1. Daftarkan seluruh seksi halaman
    // PENTING: Seksi pertama tepat di bawah hero (.hero + section, .page-hero + section, .toko-catalog-section)
    // TIDAK BOLEH disembunyikan dengan opacity 0 karena berfungsi sebagai tirai penutup solid yang langsung terlihat di viewport awal (above the fold)
    const heroExclusions = ":not(.hero):not(.page-hero):not(.about-hero):not(.lomba-hero):not(.activities-hero):not(.class-hero):not(.peringkat-hero):not(.rekomendasi-hero):not(.toko-hero):not(.motivasi-hero):not(.buuku-hero):not(.quest-hero)";
    
    const sectionSelectors = [
        `main > section${heroExclusions}:not(.toko-catalog-section)`,
        ".proker-section",
        ".kegiatan-section",
        ".content-section",
        ".facility-section",
        ".division-section",
        ".learning-path",
        ".feedback-preview",
        ".home-activities-dark-section",
        ".journey-section",
        ".about-preview"
    ];

    document.querySelectorAll(sectionSelectors.join(",")).forEach((sec) => {
        // Jangan beri section-reveal ke seksi pertama tepat di bawah hero
        if (sec.matches(".hero + section, .page-hero + section, .proker-hero + section, .quest-hero + section, .toko-catalog-section")) {
            sec.classList.remove("section-reveal");
            sec.classList.add("is-visible");
            return;
        }

        if (!sec.classList.contains("section-reveal")) {
            sec.classList.add("section-reveal");
        }
    });

    // 2. Daftarkan seluruh kartu komponen dan elemen kartu di dalam seksi
    const cardSelectors = [
        "article",
        "[class*='-card']",
        ".journey-step",
        ".activity-item",
        ".mission-box",
        ".history-origin-card",
        ".pembina-card",
        ".feedback-card",
        ".home-about-banner",
        ".facility-card",
        ".podium-card",
        ".rek-card",
        ".event-card",
        ".course-card",
        ".class-card",
        ".division-card",
        ".program-card",
        ".management-card",
        ".haori-card",
        ".accessory-card"
    ];

    document.querySelectorAll(cardSelectors.join(",")).forEach((card) => {
        // Jangan beri animasi scroll pada elemen di dalam hero, header, floating drawer chat, atau modal/latihan
        if (card.closest(".hero, .page-hero, .about-hero, .lomba-hero, .activities-hero, .class-hero, #drawer, #launcher, .sidebar-nav, .home-header, .lightbox, .modal, .practice-view, .result-view, [data-practice-view], [data-result-view]")) return;

        if (!card.classList.contains("motion-reveal") && !card.classList.contains("reveal")) {
            card.classList.add("motion-reveal");
            const parent = card.parentElement;
            if (parent) {
                const siblings = Array.from(parent.children).filter(c => c.matches(cardSelectors.join(",")));
                const index = siblings.indexOf(card);
                const stagger = ((index >= 0 ? index : 0) % 6) + 1;
                card.classList.add(`motion-delay-${stagger}`);
            }
        }
    });

    const targets = document.querySelectorAll(".section-reveal, .motion-reveal, .reveal");
    if (!targets.length) return;

    // Langsung aktifkan elemen yang sudah berada di dalam atau di atas viewport saat render awal (above the fold)
    // agar konten tidak pernah tertahan sembunyi (blank/black void) saat pengguna pertama kali membuka halaman
    targets.forEach((target) => {
        const rect = target.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom > 0) {
            target.classList.add("is-visible");
        }
    });

    if (!("IntersectionObserver" in window)) {
        targets.forEach((target) => target.classList.add("is-visible"));
        return;
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting || entry.intersectionRatio > 0) {
                entry.target.classList.add("is-visible");
                observer.unobserve(entry.target);
            }
        });
    }, { 
        threshold: 0.01, 
        rootMargin: "0px 0px -10px 0px" 
    });

    targets.forEach((target) => {
        if (!target.classList.contains("is-visible")) {
            observer.observe(target);
        }
    });
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
        const response = await fetch(getAppBasePath() + "data/kanji.json");
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
        const basePath = getAppBasePath();
        widget = document.createElement("aside");
        widget.className = "sora-widget";
        widget.dataset.sora = "";
        widget.setAttribute("aria-label", "Asisten Sora");
        widget.innerHTML = [
            `<button class="sora-toggle" type="button" data-sora-toggle aria-expanded="false"><img src="${basePath}images/mirai/icon/Ay.png" alt=""><span>SORA</span></button>`,
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
        document.body.classList.toggle("sora-widget-open", isOpen);
        if (isOpen) input.focus();
    });

    close?.addEventListener("click", () => {
        panel.hidden = true;
        toggle.setAttribute("aria-expanded", "false");
        document.body.classList.remove("sora-widget-open");
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
            indicator.textContent = `${currentIndex + 1} dari ${totalSlides}`;
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

    function syncManagementGridHeight() {
        const soraSlide = track.querySelector('.mgmt-slide[data-slide-index="0"]');
        const cloverGrid = track.querySelector('.mgmt-slide[data-slide-index="1"] .management-grid--11');
        if (soraSlide && cloverGrid) {
            const soraGrid = soraSlide.querySelector('.management-grid');
            if (soraGrid) {
                const soraHeight = soraGrid.getBoundingClientRect().height || soraGrid.offsetHeight;
                if (soraHeight > 100) {
                    cloverGrid.style.maxHeight = `${Math.round(soraHeight)}px`;
                }
            }
        }
    }

    updateState(0);
    syncManagementGridHeight();
    window.addEventListener("resize", syncManagementGridHeight, { passive: true });
    window.addEventListener("load", syncManagementGridHeight, { passive: true });
}

function setupImageLightbox() {
    let lightbox = null;
    let imgEl = null;
    let captionEl = null;

    function createLightbox() {
        if (lightbox) return;
        lightbox = document.createElement("div");
        lightbox.id = "imgLightboxModal";
        lightbox.className = "img-lightbox";
        lightbox.setAttribute("role", "dialog");
        lightbox.setAttribute("aria-label", "Pratinjau Foto");
        lightbox.setAttribute("aria-modal", "true");
        lightbox.innerHTML = [
            '<button class="img-lightbox-close" type="button" aria-label="Tutup Pratinjau">✕</button>',
            '<div class="img-lightbox-container">',
            '    <img class="img-lightbox-img" src="" alt="Pratinjau Foto">',
            '    <div class="img-lightbox-caption"></div>',
            '    <div class="img-lightbox-hint">Klik di mana saja atau tekan ESC untuk menutup</div>',
            '</div>'
        ].join("");
        document.body.appendChild(lightbox);

        imgEl = lightbox.querySelector(".img-lightbox-img");
        captionEl = lightbox.querySelector(".img-lightbox-caption");
        const closeBtn = lightbox.querySelector(".img-lightbox-close");

        closeBtn.addEventListener("click", closeLightbox);
        lightbox.addEventListener("click", (e) => {
            if (e.target !== captionEl) {
                closeLightbox();
            }
        });

        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape" && lightbox.classList.contains("is-open")) {
                closeLightbox();
            }
        });
    }

    function openLightbox(sourceImg) {
        if (!sourceImg || !sourceImg.src) return;
        createLightbox();

        imgEl.src = sourceImg.currentSrc || sourceImg.src;
        const caption = sourceImg.alt || sourceImg.title || "";
        captionEl.textContent = caption;

        lightbox.classList.add("is-open");
        document.body.classList.add("lightbox-open");
        document.body.style.overflow = "hidden";
    }

    function closeLightbox() {
        if (!lightbox) return;
        lightbox.classList.remove("is-open");
        document.body.classList.remove("lightbox-open");
        document.body.style.overflow = "";
        setTimeout(() => {
            if (imgEl && !lightbox.classList.contains("is-open")) {
                imgEl.src = "";
            }
        }, 260);
    }

    // Deteksi klik ganda (double-click) untuk Desktop
    document.addEventListener("dblclick", (e) => {
        const img = e.target.closest("img");
        if (!img) return;
        if (img.closest(".img-lightbox") || img.closest("#launcher") || img.closest(".to-top")) return;
        if (!img.src) return;
        e.preventDefault();
        openLightbox(img);
    });

    // Deteksi ketukan ganda (double-tap) untuk Mobile (ketuk dua kali dalam 320ms)
    let lastTapTime = 0;
    let lastTapTarget = null;
    document.addEventListener("touchend", (e) => {
        const img = e.target.closest("img");
        if (!img) return;
        if (img.closest(".img-lightbox") || img.closest("#launcher") || img.closest(".to-top")) return;
        if (!img.src) return;

        const now = Date.now();
        const diff = now - lastTapTime;
        if (diff < 320 && diff > 40 && lastTapTarget === img) {
            e.preventDefault();
            openLightbox(img);
            lastTapTime = 0;
            lastTapTarget = null;
        } else {
            lastTapTime = now;
            lastTapTarget = img;
        }
    }, { passive: false });
}

/* ==========================================================================
   FOOTER QUOTE SLIDER (KATA MOTIVASI DI ATAS DISCLAIMER)
   ========================================================================== */
function setupFooterQuoteSlider() {
    // Jangan pasang slider jika berada di halaman arsip motivasi itu sendiri
    if (document.body.classList.contains("page-motivasi")) return;

    const footer = document.querySelector(".global-footer");
    if (!footer) return;

    // Hindari duplikasi
    if (document.getElementById("footerQuoteSliderSection")) return;

    // Deteksi base relative path
    const basePath = getAppBasePath();

    const quotes = [
        {
            id: 1,
            animeId: "one-piece",
            tokohBadge: "Tokoh 1 · 麦わらのルフィ",
            tag: "ONE PIECE · ワンピース · EIICHIRO ODA",
            name: "Monkey D. Luffy",
            anime: "One Piece",
            animeJP: "ワンピース",
            author: "Eiichiro Oda",
            image: "luf.jpeg",
            chibi: "Ay.png",
            kanji: "海賊王に、おれはなる！",
            romaji: "Kaizoku-ou ni, ore wa naru!",
            literal: 'Arti Harfiah: "Aku akan menjadi Raja Bajak Laut!"',
            meaningTitle: "Berani Bermimpi Besar Tanpa Ragu",
            meaningText: "Deklarasi tanpa kompromi untuk menancapkan tujuan hidup setinggi-tingginya. Jangan takut memimpikan hal yang dianggap mustahil oleh orang lain; ucapkan dengan yakin dan kejarlah dengan seluruh tenaga.",
            accent: "#ff5252",
            glow: "rgba(255, 82, 82, 0.4)",
            line: "linear-gradient(90deg, #ff5252, #ffb142)",
            border: "rgba(255, 82, 82, 0.35)",
            badgeBg: "rgba(255, 82, 82, 0.16)",
            badgeBorder: "rgba(255, 82, 82, 0.45)"
        },
        {
            id: 2,
            animeId: "attack-on-titan",
            tokohBadge: "Tokoh 2 · 調査兵団",
            tag: "ATTACK ON TITAN · 進撃の巨人 · HAJIME ISAYAMA",
            name: "Eren Yeager & Pasukan Penyelidik",
            anime: "Attack on Titan",
            animeJP: "進撃の巨人",
            author: "Hajime Isayama",
            image: "ere.jpeg",
            chibi: "Ka.png",
            kanji: "心臓を捧げよ！",
            romaji: "Shinzou o sasageyo!",
            literal: 'Arti Harfiah: "Persembahkan hatimu!"',
            meaningTitle: "Dedikasi Total & Berikan yang Terbaik",
            meaningText: 'Memberikan "hati" bukan berarti mengorbankan nyawa secara sia-sia, melainkan mencurahkan 100% komitmen, energi, dan ketulusan pada apa yang sedang diperjuangkan (seperti belajar, berkarya, atau memajukan komunitas).',
            accent: "#10b981",
            glow: "rgba(16, 185, 129, 0.4)",
            line: "linear-gradient(90deg, #10b981, #34d399)",
            border: "rgba(16, 185, 129, 0.35)",
            badgeBg: "rgba(16, 185, 129, 0.16)",
            badgeBorder: "rgba(16, 185, 129, 0.45)"
        },
        {
            id: 3,
            animeId: "naruto",
            tokohBadge: "Tokoh 3 · うずまきナルト",
            tag: "NARUTO · ナルト · MASASHI KISHIMOTO",
            name: "Uzumaki Naruto",
            anime: "Naruto",
            animeJP: "NARUTO -ナルト-",
            author: "Masashi Kishimoto",
            image: "nar.jpeg",
            chibi: "Lo.png",
            kanji: "まっすぐ自分の言葉は曲げねぇ。それが俺の忍道だ！",
            romaji: "Massugu jibun no kotoba wa magenee. Sore ga ore no nindou da!",
            literal: 'Arti Harfiah: "Aku tidak akan menarik kembali kata-kataku. Itulah jalan ninjaku!"',
            meaningTitle: "Integritas & Memegang Teguh Prinsip",
            meaningText: "Komitmen sejati terhadap janji dan tujuan diri sendiri. Apabila sudah menetapkan target untuk berkembang, jangan goyah oleh godaan rasa malas atau omongan orang lain.",
            accent: "#f97316",
            glow: "rgba(249, 115, 22, 0.4)",
            line: "linear-gradient(90deg, #f97316, #fbbf24)",
            border: "rgba(249, 115, 22, 0.35)",
            badgeBg: "rgba(249, 115, 22, 0.16)",
            badgeBorder: "rgba(249, 115, 22, 0.45)"
        },
        {
            id: 4,
            animeId: "my-hero-academia",
            tokohBadge: "Tokoh 4 · デク · PLUS ULTRA",
            tag: "MY HERO ACADEMIA · 僕のヒーローアカデミア · KOHEI HORIKOSHI",
            name: "Midoriya Izuku (Deku)",
            anime: "My Hero Academia",
            animeJP: "僕のヒーローアカデミア",
            author: "Kohei Horikoshi",
            image: "dek.jpeg",
            chibi: "Al.png",
            kanji: "限界を超えて、さらに向こうへ！プルス・ウルトラ！",
            romaji: "Genkai o koete, sara ni mukou e! Purusu Urutora! (Plus Ultra)",
            literal: 'Arti Harfiah: "Lampaui batas, melangkah lebih jauh lagi! Plus Ultra!"',
            meaningTitle: "Terus Mengembangkan Diri Tanpa Batas",
            meaningText: "Saat merasa sudah berada di ujung kemampuan, itu adalah tanda bahwa potensi diri sedang siap naik ke tingkat berikutnya. Selalu ada ruang untuk melangkah satu langkah lebih jauh dari kemarin.",
            accent: "#06b6d4",
            glow: "rgba(6, 182, 212, 0.4)",
            line: "linear-gradient(90deg, #06b6d4, #10b981)",
            border: "rgba(6, 182, 212, 0.35)",
            badgeBg: "rgba(6, 182, 212, 0.16)",
            badgeBorder: "rgba(6, 182, 212, 0.45)"
        },
        {
            id: 5,
            animeId: "demon-slayer",
            tokohBadge: "Tokoh 5 · 竈門炭治郎",
            tag: "DEMON SLAYER · 鬼滅の刃 · KOYOHARU GOTOUGE",
            name: "Tanjiro Kamado",
            anime: "Demon Slayer",
            animeJP: "鬼滅の刃",
            author: "Koyoharu Gotouge",
            image: "tan.jpeg",
            chibi: "Fu.png",
            kanji: "頑張れ炭治郎、頑張れ！俺は今までよくやってきた！",
            romaji: "Ganbare Tanjiro, ganbare! Ore wa ima made yoku yatte kita!",
            literal: 'Arti Harfiah: "Semangat Tanjiro, semangat! Selama ini aku sudah berjuang dengan baik!"',
            meaningTitle: "Apresiasi Diri Sendiri (Self-Compassion)",
            meaningText: "Saat menghadapi rintangan berat, jangan terburu-buru mengkritik diri sendiri. Beri semangat pada diri, hargai proses perjuangan yang telah dilewati, lalu bangkit lagi dengan kepala tegak.",
            accent: "#38bdf8",
            glow: "rgba(56, 189, 248, 0.4)",
            line: "linear-gradient(90deg, #38bdf8, #ef4444)",
            border: "rgba(56, 189, 248, 0.35)",
            badgeBg: "rgba(56, 189, 248, 0.16)",
            badgeBorder: "rgba(56, 189, 248, 0.45)"
        }
    ];

    let currentIndex = 0;
    let autoTimer = null;

    // Buat elemen section slider independen (halaman/blok hitam mandiri, terpisah dari disclaimer)
    const section = document.createElement("section");
    section.className = "section-quote-slider";
    section.id = "footerQuoteSliderSection";
    section.setAttribute("aria-label", "Kata-Kata Motivasi Karakter Anime");
    section.innerHTML = `
        <div class="footer-quote-slider-section">
            <div class="footer-quote-slider-header">
                <div class="footer-quote-header-left">
                    <span class="footer-quote-pill">
                        <span class="badge-dot"></span>
                        KUTIPAN INSPIRATIF · 名言
                    </span>
                    <h3 class="footer-quote-heading">Kata-Kata Motivasi Karakter Anime</h3>
                </div>
                <div class="footer-quote-controls">
                    <button type="button" class="footer-quote-btn" id="footerQuotePrevBtn" aria-label="Kutipan Sebelumnya">‹</button>
                    <span class="footer-quote-counter" id="footerQuoteCounter">1 / ${quotes.length}</span>
                    <button type="button" class="footer-quote-btn" id="footerQuoteNextBtn" aria-label="Kutipan Selanjutnya">›</button>
                </div>
            </div>
            <div class="footer-quote-card-container" id="footerQuoteCardContainer"></div>
            <div class="footer-quote-dots" id="footerQuoteDots">
                ${quotes.map((_, i) => `<button type="button" class="footer-quote-dot ${i === 0 ? "active" : ""}" data-quote-dot="${i}" aria-label="Pilih kutipan ${i + 1}"></button>`).join("")}
            </div>
        </div>
    `;

    // Pasang sebelum .global-footer sehingga menjadi section tersendiri di atas disclaimer
    footer.parentNode.insertBefore(section, footer);

    const cardContainer = section.querySelector("#footerQuoteCardContainer");
    const counterEl = section.querySelector("#footerQuoteCounter");
    const prevBtn = section.querySelector("#footerQuotePrevBtn");
    const nextBtn = section.querySelector("#footerQuoteNextBtn");
    const dots = section.querySelectorAll(".footer-quote-dot");

    function renderSlide(index) {
        currentIndex = (index + quotes.length) % quotes.length;
        const q = quotes[currentIndex];

        cardContainer.innerHTML = `
            <article class="quote-card quote-slide-enter" data-anime="${q.animeId}" style="--quote-accent: ${q.accent}; --quote-glow: ${q.glow}; --quote-line: ${q.line}; --quote-border: ${q.border}; --quote-badge-bg: ${q.badgeBg}; --quote-badge-border: ${q.badgeBorder};">
                <div class="quote-card-header">
                    <span class="quote-card-badge">
                        <span class="badge-dot"></span>
                        ${q.tokohBadge}
                    </span>
                    <span class="quote-card-tag">
                        <span class="badge-dot"></span>
                        ${q.tag}
                    </span>
                </div>
                <div class="quote-card-body">
                    <!-- BARIS ATAS: 2 BOX (KIRI FOTO & IDENTITAS, KANAN KUTIPAN) -->
                    <div class="quote-top-row">
                        <div class="quote-author-profile">
                            <div class="quote-avatar-wrap">
                                <img class="quote-avatar-img" src="${basePath}images/mirai/karakter/${q.image}" alt="${q.name}">
                            </div>
                            <h3 class="quote-author-name">${q.name}</h3>
                        </div>
                        <div class="quote-box">
                            <h4 class="quote-kanji">${q.kanji}</h4>
                            <p class="quote-romaji">${q.romaji}</p>
                            <div class="quote-literal">
                                <span>${q.literal}</span>
                            </div>
                        </div>
                    </div>

                    <!-- BARIS BAWAH: 1 BOX MEMANJANG (MAKNA KUTIPAN) -->
                    <div class="quote-meaning-card">
                        <div class="quote-meaning-head">
                            <span class="quote-meaning-badge">🌟 Makna Kutipan</span>
                            <h5 class="quote-meaning-title">${q.meaningTitle}</h5>
                        </div>
                        <p class="quote-meaning-body">${q.meaningText}</p>
                    </div>
                </div>
            </article>
        `;

        if (counterEl) counterEl.textContent = `${currentIndex + 1} / ${quotes.length}`;

        dots.forEach((dot, i) => {
            dot.classList.toggle("active", i === currentIndex);
            if (i === currentIndex) {
                dot.style.setProperty("--quote-accent", q.accent);
            }
        });
    }

    function startAutoTimer() {
        stopAutoTimer();
        autoTimer = setInterval(() => {
            renderSlide(currentIndex + 1);
        }, 6500);
    }

    function stopAutoTimer() {
        if (autoTimer) {
            clearInterval(autoTimer);
            autoTimer = null;
        }
    }

    prevBtn?.addEventListener("click", () => {
        renderSlide(currentIndex - 1);
        startAutoTimer();
    });

    nextBtn?.addEventListener("click", () => {
        renderSlide(currentIndex + 1);
        startAutoTimer();
    });

    dots.forEach((dot, i) => {
        dot.addEventListener("click", () => {
            renderSlide(i);
            startAutoTimer();
        });
    });

    // Jeda otomatis jika kursor berada di atas kartu kutipan
    section.addEventListener("mouseenter", stopAutoTimer);
    section.addEventListener("mouseleave", startAutoTimer);

    // Gestur geser layar sentuh (touch swipe) untuk perangkat mobile
    let touchStartX = 0;
    section.addEventListener("touchstart", (e) => {
        touchStartX = e.touches[0].clientX;
        stopAutoTimer();
    }, { passive: true });

    section.addEventListener("touchend", (e) => {
        const touchEndX = e.changedTouches[0].clientX;
        const diffX = touchEndX - touchStartX;
        if (Math.abs(diffX) > 45) {
            if (diffX < 0) {
                renderSlide(currentIndex + 1);
            } else {
                renderSlide(currentIndex - 1);
            }
        }
        startAutoTimer();
    }, { passive: true });

    // Render kartu pertama dan jalankan timer otomatis
    renderSlide(0);
    startAutoTimer();
}


function setupExpandableCards() {
    const cards = document.querySelectorAll("[data-expand-card]");
    if (!cards.length) return;

    cards.forEach((card) => {
        const toggleBtn = card.querySelector(".card-toggle");
        const isAboutDrawerCard = card.classList.contains("about-drawer-card") || card.id === "mnhAboutDrawerCard";

        if (isAboutDrawerCard) {
            setupAboutDrawerCard(card, toggleBtn);
            return;
        }

        // Standard 2-step card logic for all other cards
        card.addEventListener("click", (e) => {
            const ctaBtn = e.target.closest("[data-expand-cta]");
            if (ctaBtn) {
                // Biarkan kombinasi Ctrl / Cmd / Shift / Alt klik membuka tab baru secara normal
                if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) {
                    return;
                }

                // Jika kartu masih tertutup: buka kartu dulu dan batalkan navigasi
                if (!card.classList.contains("is-expanded")) {
                    e.preventDefault();
                    e.stopPropagation();
                    toggleCard(card, true);
                    return;
                }
                // Jika kartu sudah terbuka: navigasi berjalan normal, stop bubbling agar kartu tidak tertutup
                e.stopPropagation();
                return;
            }

            // Jika klik pada link atau tombol interaktif lain selain toggle
            const otherInteractive = e.target.closest("a, button:not(.card-toggle), input, textarea, select");
            if (otherInteractive) {
                return;
            }

            // Toggle buka / tutup kartu
            const nextState = !card.classList.contains("is-expanded");
            toggleCard(card, nextState);
        });

        // Handler khusus toggle button (keyboard accessible & click)
        if (toggleBtn) {
            toggleBtn.addEventListener("click", (e) => {
                e.stopPropagation();
                const nextState = !card.classList.contains("is-expanded");
                toggleCard(card, nextState);
            });
        }
    });

    function toggleCard(card, shouldOpen) {
        card.classList.toggle("is-expanded", shouldOpen);

        const toggleBtn = card.querySelector(".card-toggle");
        if (toggleBtn) {
            toggleBtn.setAttribute("aria-expanded", shouldOpen ? "true" : "false");
            toggleBtn.setAttribute("aria-label", shouldOpen ? "Tutup detail kartu" : "Buka detail kartu");
        }
    }

    /**
     * Khusus Card Tentang Mirai no Hana:
     * Alur 3x Klik & Penutupan Bertahap:
     * - Klik 1 (card / tombol saat tertutup): buka deskripsi kartu (is-expanded: true, is-pulled: false)
     * - Klik 2 (card / tombol saat deskripsi buka): buka animasi laci logo NK (is-pulled: true)
     * - Klik 3 (tombol saat animasi logo NK buka): navigasi menuju halaman tujuan (tentang/index.html)
     * - Klik mundur 1 (card saat animasi logo NK buka): tutup animasi logo NK (is-pulled: false, deskripsi tetap buka)
     * - Klik mundur 2 (card saat deskripsi buka setelah animasi tutup): tutup deskripsi kartu (is-expanded: false)
     */
    function setupAboutDrawerCard(card, toggleBtn) {
        function updateToggle(shouldOpen) {
            if (toggleBtn) {
                toggleBtn.setAttribute("aria-expanded", shouldOpen ? "true" : "false");
                toggleBtn.setAttribute("aria-label", shouldOpen ? "Tutup detail kartu" : "Buka detail kartu");
            }
        }

        card.addEventListener("click", (e) => {
            const ctaBtn = e.target.closest("[data-expand-cta]");

            // 1. Aksi Klik pada Tombol CTA ("TENTANG MIRAI NO HANA ->")
            if (ctaBtn) {
                if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) {
                    return;
                }

                // Klik 1: Jika kartu masih tertutup -> buka deskripsi
                if (!card.classList.contains("is-expanded")) {
                    e.preventDefault();
                    e.stopPropagation();
                    card.classList.add("is-expanded");
                    card.classList.remove("is-pulled");
                    card.dataset.drawerPhase = "desc";
                    updateToggle(true);
                    return;
                }

                // Klik 2: Jika deskripsi sudah buka, tapi animasi logo NK belum buka -> buka animasi logo NK
                if (!card.classList.contains("is-pulled")) {
                    e.preventDefault();
                    e.stopPropagation();
                    card.classList.add("is-pulled");
                    card.dataset.drawerPhase = "logo";
                    return;
                }

                // Klik 3: Jika animasi logo NK sudah buka -> pindah ke page yang dituju
                e.stopPropagation();
                return;
            }

            // Abaikan jika klik elemen interaktif lain selain toggle
            const otherInteractive = e.target.closest("a, input, textarea, select");
            if (otherInteractive) {
                return;
            }

            // 2. Aksi Klik pada Area Card atau Tombol Toggle
            // Klik 1: Jika kartu masih tertutup -> buka deskripsi
            if (!card.classList.contains("is-expanded")) {
                card.classList.add("is-expanded");
                card.classList.remove("is-pulled");
                card.dataset.drawerPhase = "desc";
                updateToggle(true);
                return;
            }

            // Klik mundur 1: Jika animasi logo NK sedang buka -> tutup animasi logo NK
            if (card.classList.contains("is-pulled")) {
                card.classList.remove("is-pulled");
                card.dataset.drawerPhase = "closing"; // Tandai fase penutupan mundur
                return;
            }

            // Klik mundur 2: Jika deskripsi buka dan animasi baru ditutup -> tutup deskripsi
            if (card.dataset.drawerPhase === "closing") {
                card.classList.remove("is-expanded");
                card.classList.remove("is-pulled");
                card.dataset.drawerPhase = "0";
                updateToggle(false);
                return;
            }

            // Klik 2 (fase maju): Jika deskripsi buka -> buka animasi logo NK
            card.classList.add("is-pulled");
            card.dataset.drawerPhase = "logo";
        });
    }
}

/* ==========================================================================
   5 EFEK MIKRO-INTERAKSI MODERN (GPU-Accelerated & 60fps)
   ========================================================================== */

/**
 * 1. Top Scroll Progress Bar
 * Membuat elemen progress bar di bagian paling atas viewport yang lebarnya
 * di-update menggunakan requestAnimationFrame saat user scroll.
 */
function setupScrollProgressBar() {
    let bar = document.querySelector(".scroll-progress-bar");
    if (!bar) {
        bar = document.createElement("div");
        bar.className = "scroll-progress-bar";
        document.body.prepend(bar);
    }

    let ticking = false;
    function updateProgress() {
        const scrollTop = window.scrollY || document.documentElement.scrollTop;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const progress = docHeight > 0 ? Math.min(100, Math.max(0, (scrollTop / docHeight) * 100)) : 0;
        bar.style.width = `${progress}%`;
        ticking = false;
    }

    window.addEventListener("scroll", () => {
        if (!ticking) {
            window.requestAnimationFrame(updateProgress);
            ticking = true;
        }
    }, { passive: true });

    window.addEventListener("resize", () => {
        if (!ticking) {
            window.requestAnimationFrame(updateProgress);
            ticking = true;
        }
    }, { passive: true });

    updateProgress();
}

/**
 * 2. Ambient Sakura Petals pada Hero Banner
 * Menyuntikkan kontainer .hero-sakura-layer dan 10 partikel kelopak sakura
 * CSS murni (.hero-petal) ke dalam seluruh hero banner.
 */
function setupHeroSakuraPetals() {
    const heroElements = document.querySelectorAll(".hero, .page-hero, .proker-hero, .quest-hero, .toko-hero");
    if (!heroElements.length) return;

    heroElements.forEach((hero) => {
        if (hero.querySelector(".hero-sakura-layer")) return;

        const layer = document.createElement("div");
        layer.className = "hero-sakura-layer";
        layer.setAttribute("aria-hidden", "true");

        // 10 partikel kelopak sakura dengan parameter acak
        for (let i = 0; i < 10; i++) {
            const petal = document.createElement("div");
            petal.className = "hero-petal";

            const left = Math.random() * 92 + 2; // 2% - 94%
            const width = 10 + Math.random() * 6; // 10px - 16px
            const height = width * 1.35;
            const duration = 8 + Math.random() * 6; // 8s - 14s
            const delay = -(Math.random() * duration); // Tersebar merata sejak awal
            const opacity = 0.5 + Math.random() * 0.35;

            petal.style.left = `${left.toFixed(1)}%`;
            petal.style.width = `${width.toFixed(1)}px`;
            petal.style.height = `${height.toFixed(1)}px`;
            petal.style.animationDuration = `${duration.toFixed(2)}s`;
            petal.style.animationDelay = `${delay.toFixed(2)}s`;
            petal.style.opacity = `${opacity.toFixed(2)}`;

            layer.appendChild(petal);
        }

        hero.appendChild(layer);
    });
}

/**
 * 3. Interactive Spotlight Glow & 3D Tilt Halus pada Kartu
 * Pada perangkat hover: hover, menambahkan efek spotlight kursor (--mouse-x, --mouse-y)
 * dan kemiringan perspektif 3D halus (maksimal 3.5 derajat).
 */
function setupCardTiltAndSpotlight() {
    const isHoverDevice = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
    if (!isHoverDevice) return;

    const cardSelectors = [
        ".start-card",
        ".activity-start-card",
        ".class-card",
        ".course-card",
        ".division-card",
        ".program-card",
        ".podium-card",
        ".toko-card"
    ];
    const cards = document.querySelectorAll(cardSelectors.join(","));
    if (!cards.length) return;

    cards.forEach((card) => {
        if (!card.querySelector(".card-spotlight-glow")) {
            const glow = document.createElement("div");
            glow.className = "card-spotlight-glow";
            glow.setAttribute("aria-hidden", "true");
            card.appendChild(glow);
        }

        let rafId = null;

        card.addEventListener("mousemove", (e) => {
            if (rafId) cancelAnimationFrame(rafId);
            rafId = requestAnimationFrame(() => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

                card.style.setProperty("--mouse-x", `${x}px`);
                card.style.setProperty("--mouse-y", `${y}px`);

                // 3D Tilt: maksimal 3.5 derajat
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                const rotateX = (((y - centerY) / centerY) * -3.5).toFixed(2);
                const rotateY = (((x - centerX) / centerX) * 3.5).toFixed(2);

                card.style.transform = `perspective(900px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-3px)`;
            });
        });

        card.addEventListener("mouseleave", () => {
            if (rafId) cancelAnimationFrame(rafId);
            card.style.transform = "none";
        });
    });
}

/**
 * 4. Sakura Ripple Effect saat Klik / Tap
 * Memunculkan riak lingkaran sakura di titik koordinat klik yang membesar
 * dan memudar dalam 0.55 detik lalu otomatis dihapus.
 */
function setupSakuraRipple() {
    const targetSelector = ".btn, button, .start-card, .class-card, .rek-cat-btn, .lb-tab-btn, .toko-cat-btn";

    document.addEventListener("pointerdown", (e) => {
        const target = e.target.closest(targetSelector);
        if (!target) return;

        // Jangan picu ripple pada tombol yang dinonaktifkan
        if (target.disabled || target.getAttribute("aria-disabled") === "true") return;

        const rect = target.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height) * 0.9;
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        // Pastikan kontainer memiliki posisi non-static dan overflow hidden
        const comp = window.getComputedStyle(target);
        if (comp.position === "static") {
            target.style.position = "relative";
        }
        if (comp.overflow !== "hidden") {
            target.style.overflow = "hidden";
        }

        const ripple = document.createElement("span");
        ripple.className = "sakura-ripple";
        ripple.style.width = `${size}px`;
        ripple.style.height = `${size}px`;
        ripple.style.left = `${x}px`;
        ripple.style.top = `${y}px`;

        target.appendChild(ripple);

        setTimeout(() => {
            ripple.remove();
        }, 550);
    }, { passive: true });
}

/**
 * 5. Tab Cascade Transition
 * Memberikan animasi masuk fadeSlideUp setiap kali konten tab di Kamus,
 * Peringkat, Rekomendasi, Lomba, atau Toko berganti.
 */
function setupTabCascadeTransition() {
    document.addEventListener("click", (e) => {
        const tabBtn = e.target.closest(".lb-tab-btn, .rek-cat-btn, .lomba-filter-chip, .toko-cat-btn, .mgmt-tab-btn, [role='tab'], .tab-btn");
        if (!tabBtn) return;

        requestAnimationFrame(() => {
            const targetContainers = document.querySelectorAll(
                "#rekomendasiGrid, #eventsGrid, #tokoProductGrid, .lb-points-grid, .lb-podium-grid, .leaderboard-table-wrapper, .tab-pane.active, .tab-content.active, [data-tab-content].active, .kanji-grid, .mgmt-slider-container"
            );
            targetContainers.forEach((container) => {
                container.classList.remove("tab-cascade-animate");
                void container.offsetWidth; // Reflow trigger
                container.classList.add("tab-cascade-animate");
            });
        });
    }, { passive: true });
}

/* ==========================================================================
   MIRAI PROGRESS ENGINE (localStorage-based learning progress)
   ========================================================================== */

const MiraiProgress = {
    STORAGE_KEY_COMPLETED: "mirai_completed_materi",
    STORAGE_KEY_LAST: "mirai_last_materi",
    STORAGE_KEY_WRONG: "mirai_wrong_questions",

    TOTAL_MATERI: 8,

    getCompleted() {
        try {
            const raw = localStorage.getItem(this.STORAGE_KEY_COMPLETED);
            if (!raw) return [];
            const parsed = JSON.parse(raw);
            return Array.isArray(parsed) ? parsed : [];
        } catch (e) {
            return [];
        }
    },

    isCompleted(materiId) {
        if (!materiId) return false;
        return this.getCompleted().includes(materiId);
    },

    toggleCompleted(materiId) {
        if (!materiId) return false;
        let list = this.getCompleted();
        let newState = false;
        if (list.includes(materiId)) {
            list = list.filter((id) => id !== materiId);
            newState = false;
        } else {
            list.push(materiId);
            newState = true;
        }
        try {
            localStorage.setItem(this.STORAGE_KEY_COMPLETED, JSON.stringify(list));
        } catch (e) {
            console.warn("Gagal menyimpan progress materi:", e);
        }
        return newState;
    },

    getLastMateri() {
        try {
            const raw = localStorage.getItem(this.STORAGE_KEY_LAST);
            if (!raw) return null;
            const parsed = JSON.parse(raw);
            return typeof parsed === "object" && parsed !== null ? parsed : null;
        } catch (e) {
            return null;
        }
    },

    setLastMateri(id, title, step, url) {
        if (!id || !url) return;
        try {
            const item = {
                id,
                title: title || id,
                step: step || "",
                url,
                timestamp: Date.now()
            };
            localStorage.setItem(this.STORAGE_KEY_LAST, JSON.stringify(item));
        } catch (e) {}
    },

    setupLessonPage() {
        const container = document.querySelector("[data-materi-id]");
        if (!container) return;

        const materiId = container.dataset.materiId;
        const materiTitle = container.dataset.materiTitle || document.title.split("—")[0].trim();
        const materiStep = container.dataset.materiStep || "Modul";

        // Otomatis simpan sebagai materi terakhir dibuka
        this.setLastMateri(materiId, materiTitle, materiStep, window.location.href);

        // Pengendali tombol "Tandai Materi Selesai"
        const toggleBtn = document.querySelector(".materi-complete-toggle");
        if (toggleBtn) {
            const updateBtnUI = (isDone) => {
                if (isDone) {
                    toggleBtn.classList.add("is-active");
                    toggleBtn.innerHTML = `<span>✓</span><span>Materi Selesai</span>`;
                    toggleBtn.setAttribute("aria-pressed", "true");
                } else {
                    toggleBtn.classList.remove("is-active");
                    toggleBtn.innerHTML = `<span>○</span><span>Tandai Selesai</span>`;
                    toggleBtn.setAttribute("aria-pressed", "false");
                }
            };

            updateBtnUI(this.isCompleted(materiId));

            toggleBtn.addEventListener("click", () => {
                const isNowDone = this.toggleCompleted(materiId);
                updateBtnUI(isNowDone);
            });
        }

        // Pengendali Kuis Cepat Pemahaman
        const quizCards = document.querySelectorAll(".buuku-quiz-card");
        quizCards.forEach((card) => {
            const optButtons = card.querySelectorAll(".buuku-quiz-opt-btn");
            const feedbackEl = card.querySelector(".buuku-quiz-feedback");

            optButtons.forEach((btn) => {
                btn.addEventListener("click", () => {
                    const isCorrect = btn.dataset.correct === "true";
                    optButtons.forEach((b) => {
                        b.disabled = true;
                        if (b.dataset.correct === "true") {
                            b.classList.add("is-correct");
                        }
                    });

                    if (!isCorrect) {
                        btn.classList.add("is-wrong");
                    }

                    if (feedbackEl) {
                        feedbackEl.classList.add("is-visible");
                        feedbackEl.classList.add(isCorrect ? "correct" : "wrong");
                    }
                });
            });
        });
    },

    setupResumeBanner() {
        const isClassIndex = window.location.pathname.endsWith("/kelas/index.html") || window.location.pathname.endsWith("/kelas/");
        const isMateriDasarIndex = window.location.pathname.includes("/materi/dasar/index.html") || window.location.pathname.endsWith("/materi/dasar/");
        const isMateriLanjutanIndex = window.location.pathname.includes("/materi/lanjutan/index.html") || window.location.pathname.endsWith("/materi/lanjutan/");

        if (!isClassIndex && !isMateriDasarIndex && !isMateriLanjutanIndex) return;

        const completed = this.getCompleted();
        const lastMateri = this.getLastMateri();

        // 1. Beri badge "✓ Selesai" pada kartu modul yang link-nya cocok
        const cards = document.querySelectorAll(".material-card, .course-card");
        cards.forEach((card) => {
            const href = card.getAttribute("href") || "";
            const matchedId = completed.find((id) => {
                const shortName = id.replace("materi-dasar-", "").replace("materi-lanjutan-", "");
                return href.includes(shortName);
            });

            if (matchedId && !card.querySelector(".materi-status-badge")) {
                const badge = document.createElement("span");
                badge.className = "materi-status-badge is-completed";
                badge.innerHTML = "✓ Selesai";
                badge.style.marginLeft = "8px";
                const heading = card.querySelector("h3");
                if (heading) {
                    heading.appendChild(badge);
                }
            }
        });

        // 2. Tampilkan banner "Lanjutkan Belajar" jika ada materi terakhir atau progres
        if (lastMateri) {
            const parentContainer = document.querySelector(".material-library, .learning-path#dasar, .learning-path");
            if (parentContainer && !document.querySelector(".progress-resume-banner")) {
                const pct = Math.round((completed.length / this.TOTAL_MATERI) * 100);

                const banner = document.createElement("div");
                banner.className = "progress-resume-banner";
                banner.innerHTML = `
                    <div class="progress-resume-left">
                        <div class="progress-resume-icon" aria-hidden="true">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                        </div>
                        <div class="progress-resume-title-wrap">
                            <h4>Lanjutkan Belajar Terakhir (${lastMateri.step || "Modul"})</h4>
                            <p>${lastMateri.title || "Materi Pembelajaran"}</p>
                        </div>
                    </div>
                    <div class="progress-resume-center">
                        <div class="progress-resume-stat">
                            <span>Progres Kurikulum</span>
                            <span>${completed.length} / ${this.TOTAL_MATERI} Materi (${pct}%)</span>
                        </div>
                        <div class="progress-bar-track">
                            <div class="progress-bar-fill" style="width: ${pct}%"></div>
                        </div>
                    </div>
                    <div class="progress-resume-right">
                        <a class="progress-resume-btn" href="${lastMateri.url}">
                            <span>LANJUTKAN →</span>
                        </a>
                    </div>
                `;
                parentContainer.prepend(banner);
            }
        }
    }
};

window.MiraiProgress = MiraiProgress;

function initMiraiProgress() {
    MiraiProgress.setupLessonPage();
    MiraiProgress.setupResumeBanner();
}


