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
    setupImageLightbox();
    setupFooterQuoteSlider();
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

    // Aktifkan kembali seluruh tautan navigasi (lapisan Coming Soon telah dihapus).
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

    // Aktifkan kembali tautan brand yang sebelumnya dinonaktifkan.
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
        document.body.style.overflow = "hidden";
    }

    function closeLightbox() {
        if (!lightbox) return;
        lightbox.classList.remove("is-open");
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
    const logo = document.querySelector(".footer-logo, .home-header .brand img");
    const logoSrc = logo ? (logo.getAttribute("src") || "") : "";
    const basePath = logoSrc.startsWith("../../") ? "../../" : "";

    const quotes = [
        {
            id: 1,
            animeId: "one-piece",
            tokohBadge: "TOKOH 01 · 麦わらのルフィ",
            tag: "ONE PIECE · ワンピース · EIICHIRO ODA",
            name: "Monkey D. Luffy",
            anime: "One Piece",
            animeJP: "ワンピース",
            author: "Eiichiro Oda",
            sticker: "sor.jpeg",
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
            tokohBadge: "TOKOH 02 · 調査兵団",
            tag: "ATTACK ON TITAN · 進撃の巨人 · HAJIME ISAYAMA",
            name: "Eren Yeager & Pasukan Penyelidik",
            anime: "Attack on Titan",
            animeJP: "進撃の巨人",
            author: "Hajime Isayama",
            sticker: "mas.jpeg",
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
            tokohBadge: "TOKOH 03 · うずまきナルト",
            tag: "NARUTO · ナルト · MASASHI KISHIMOTO",
            name: "Uzumaki Naruto",
            anime: "Naruto",
            animeJP: "NARUTO -ナルト-",
            author: "Masashi Kishimoto",
            sticker: "ita.jpeg",
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
            tokohBadge: "TOKOH 04 · デク · PLUS ULTRA",
            tag: "MY HERO ACADEMIA · 僕のヒーローアカデミア · KOHEI HORIKOSHI",
            name: "Midoriya Izuku / Deku",
            anime: "My Hero Academia",
            animeJP: "僕のヒーローアカデミア",
            author: "Kohei Horikoshi",
            sticker: "kok.jpeg",
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
            tokohBadge: "TOKOH 05 · 竈門炭治郎",
            tag: "DEMON SLAYER · 鬼滅の刃 · KOYOHARU GOTOUGE",
            name: "Tanjiro Kamado",
            anime: "Demon Slayer",
            animeJP: "鬼滅の刃",
            author: "Koyoharu Gotouge",
            sticker: "kar.jpeg",
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
        },
        {
            id: 6,
            animeId: "black-clover",
            tokohBadge: "TOKOH 06 · アスタ · 諦めない",
            tag: "BLACK CLOVER · ブラッククローバー · YŪKI TABATA",
            name: "Asta",
            anime: "Black Clover",
            animeJP: "ブラッククローバー",
            author: "Yūki Tabata",
            sticker: "jaw.jpeg",
            chibi: "Ki.png",
            kanji: "諦めないのが、俺の魔法だ！",
            romaji: "Akiramenai no ga, ore no mahou da!",
            literal: 'Arti Harfiah: "Tidak menyerah adalah sihirku!"',
            meaningTitle: "Kerja Keras Mengalahkan Bakat Alami",
            meaningText: "Tidak punya keistimewaan sejak awal bukan alasan untuk mundur. Ketekunan dan sifat pantang menyerah adalah kekuatan terbesar yang bisa mengimbangi siapa pun yang berbakat.",
            accent: "#e11d48",
            glow: "rgba(225, 29, 72, 0.4)",
            line: "linear-gradient(90deg, #e11d48, #a855f7)",
            border: "rgba(225, 29, 72, 0.35)",
            badgeBg: "rgba(225, 29, 72, 0.16)",
            badgeBorder: "rgba(225, 29, 72, 0.45)"
        },
        {
            id: 7,
            animeId: "haikyuu",
            tokohBadge: "TOKOH 07 · 烏野高校 · 飛べ",
            tag: "HAIKYUU!! · ハイキュー!! · HARUICHI FURUDATE",
            name: "Kageyama Tobio & Hinata Shoyo",
            anime: "Haikyuu!!",
            animeJP: "ハイキュー!!",
            author: "Haruichi Furudate",
            sticker: "ber.jpeg",
            chibi: "Fa.png",
            kanji: "飛べ！",
            romaji: "Tobe!",
            literal: 'Arti Harfiah: "Terbanglah!"',
            meaningTitle: "Lepaskan Rasa Takut & Percaya pada Sayapmu Sendiri",
            meaningText: "Slogan ikonik spanduk Karasuno yang mengajak siapa pun untuk melepaskan beban keraguan dan berani melompat tinggi menyambut peluang baru.",
            accent: "#f59e0b",
            glow: "rgba(245, 158, 11, 0.4)",
            line: "linear-gradient(90deg, #f59e0b, #f97316)",
            border: "rgba(245, 158, 11, 0.35)",
            badgeBg: "rgba(245, 158, 11, 0.16)",
            badgeBorder: "rgba(245, 158, 11, 0.45)"
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
                                <img class="quote-avatar-img" src="${basePath}images/mirai/stiker/${q.sticker}" alt="${q.name}">
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

