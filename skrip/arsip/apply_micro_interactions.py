#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skrip Penerapan 5 Efek Mikro-Interaksi Modern
Mirai No Webu
"""

import re

print("=== MEMULAI PENERAPAN 5 MIKRO-INTERAKSI MODERN ===")

# -------------------------------------------------------------------
# 1. Update js/main.js
# -------------------------------------------------------------------
with open("js/main.js", "r", encoding="utf-8") as f:
    main_js = f.read()

# Tambahkan pemanggilan fungsi di DOMContentLoaded jika belum ada
init_calls = """    setupScrollProgressBar();
    setupHeroSakuraPetals();
    setupCardTiltAndSpotlight();
    setupSakuraRipple();
    setupTabCascadeTransition();"""

if "setupScrollProgressBar();" not in main_js:
    # Sisipkan setelah setupSoundEffects();
    if "setupSoundEffects();" in main_js:
        main_js = main_js.replace(
            "setupSoundEffects();",
            "setupSoundEffects();\n" + init_calls
        )
        print("[js/main.js] Berhasil menyisipkan inisialisasi 5 mikro-interaksi di DOMContentLoaded")
    else:
        print("[WARN] setupSoundEffects() tidak ditemukan di js/main.js")

# Fungsi-fungsi baru yang akan ditambahkan ke bagian bawah js/main.js
functions_to_add = """

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
"""

if "function setupScrollProgressBar()" not in main_js:
    main_js = main_js.rstrip() + "\n" + functions_to_add + "\n"
    with open("js/main.js", "w", encoding="utf-8") as f:
        f.write(main_js)
    print("[js/main.js] 5 Fungsi mikro-interaksi berhasil ditambahkan")
else:
    print("[js/main.js] Fungsi mikro-interaksi sudah ada")


# -------------------------------------------------------------------
# 2. Update css/pages/navbar-hero-footer.css
# -------------------------------------------------------------------
with open("css/pages/navbar-hero-footer.css", "r", encoding="utf-8") as f:
    nav_css = f.read()

nav_css_to_add = """

/* ==========================================================================
   1. TOP SCROLL PROGRESS BAR & 2. AMBIENT SAKURA PETALS ON HERO
   ========================================================================== */

/* 1. Top Scroll Progress Bar */
.scroll-progress-bar {
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    z-index: 100005;
    background: linear-gradient(90deg, #ff4f91, #e91e63, #ff85b3);
    box-shadow: 0 0 10px rgba(233, 30, 99, 0.7);
    width: 0%;
    pointer-events: none;
    transition: width 0.08s ease-out;
    transform: translateZ(0);
    will-change: width;
}

/* 2. Ambient Sakura Petals on Hero Banner */
.hero-sakura-layer {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    pointer-events: none;
    z-index: 2;
}

.hero-petal {
    position: absolute;
    top: -30px;
    background: radial-gradient(circle at 35% 35%, #ffd4e5 0%, #ff6b9f 65%, #e91e63 100%);
    border-radius: 12px 1px 14px 1px;
    opacity: 0.72;
    box-shadow: 0 0 6px rgba(255, 105, 159, 0.45);
    pointer-events: none;
    will-change: transform, opacity;
    animation-name: heroPetalFall;
    animation-timing-function: linear;
    animation-iteration-count: infinite;
}

@keyframes heroPetalFall {
    0% {
        transform: translate3d(0, 0, 0) rotate(0deg) scale(0.85);
        opacity: 0;
    }
    12% {
        opacity: 0.85;
    }
    88% {
        opacity: 0.75;
    }
    100% {
        transform: translate3d(140px, 105vh, 0) rotate(420deg) scale(1);
        opacity: 0;
    }
}

@media (prefers-reduced-motion: reduce) {
    .scroll-progress-bar {
        transition: none !important;
    }
    .hero-sakura-layer,
    .hero-petal {
        display: none !important;
        animation: none !important;
    }
}
"""

if ".scroll-progress-bar" not in nav_css:
    nav_css = nav_css.rstrip() + "\n" + nav_css_to_add + "\n"
    with open("css/pages/navbar-hero-footer.css", "w", encoding="utf-8") as f:
        f.write(nav_css)
    print("[css/pages/navbar-hero-footer.css] Berhasil menambahkan style scroll progress bar & sakura petals")
else:
    print("[css/pages/navbar-hero-footer.css] Style scroll progress bar sudah ada")


# -------------------------------------------------------------------
# 3. Update css/pages/global.css
# -------------------------------------------------------------------
with open("css/pages/global.css", "r", encoding="utf-8") as f:
    global_css = f.read()

global_css_to_add = """

/* ==========================================================================
   3. SPOTLIGHT GLOW & 3D TILT, 4. SAKURA RIPPLE, 5. CHIBI IDLE & TAB CASCADE
   ========================================================================== */

/* 3. Interactive Spotlight Glow & 3D Tilt Halus pada Kartu */
@media (hover: hover) and (pointer: fine) {
    .start-card,
    .activity-start-card,
    .class-card,
    .course-card,
    .division-card,
    .program-card,
    .podium-card,
    .toko-card {
        --mouse-x: 50%;
        --mouse-y: 50%;
        position: relative;
        transform-style: preserve-3d;
        transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s ease;
    }

    .card-spotlight-glow {
        position: absolute;
        inset: 0;
        border-radius: inherit;
        background: radial-gradient(circle 240px at var(--mouse-x, 50%) var(--mouse-y, 50%), rgba(255, 105, 159, 0.14), transparent 72%);
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.3s ease;
        z-index: 2;
    }

    .start-card:hover > .card-spotlight-glow,
    .activity-start-card:hover > .card-spotlight-glow,
    .class-card:hover > .card-spotlight-glow,
    .course-card:hover > .card-spotlight-glow,
    .division-card:hover > .card-spotlight-glow,
    .program-card:hover > .card-spotlight-glow,
    .podium-card:hover > .card-spotlight-glow,
    .toko-card:hover > .card-spotlight-glow {
        opacity: 1;
    }
}

/* 4. Sakura Ripple Effect saat Klik / Tap */
.sakura-ripple {
    position: absolute;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255, 120, 175, 0.45) 0%, rgba(233, 30, 99, 0.28) 45%, rgba(255, 79, 145, 0) 75%);
    pointer-events: none;
    transform: translate(-50%, -50%) scale(0);
    animation: sakuraRippleAnim 0.55s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    z-index: 9999;
    will-change: transform, opacity;
}

@keyframes sakuraRippleAnim {
    0% {
        transform: translate(-50%, -50%) scale(0);
        opacity: 0.95;
    }
    100% {
        transform: translate(-50%, -50%) scale(3.5);
        opacity: 0;
    }
}

/* 5. Chibi Idle Breathing / Floating Animation */
@keyframes chibiIdleFloat {
    0% {
        transform: translateY(0px) scale(1);
    }
    50% {
        transform: translateY(-4px) scale(1.02);
    }
    100% {
        transform: translateY(0px) scale(1);
    }
}

.card-corner-chibi,
.page-hero-chibi {
    animation: chibiIdleFloat 3.6s ease-in-out infinite;
    will-change: transform;
    transform-origin: center bottom;
}

:hover > .card-corner-chibi,
:hover > .page-hero-chibi,
.course-card:hover .card-corner-chibi,
.start-card:hover .card-corner-chibi,
.activity-start-card:hover .card-corner-chibi,
.page-hero:hover .page-hero-chibi,
.hero:hover .page-hero-chibi {
    animation-play-state: paused;
}

/* Tab Cascade Transition */
@keyframes fadeSlideUp {
    0% {
        opacity: 0;
        transform: translateY(12px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

.tab-cascade-animate,
.tab-content.is-active,
.tab-pane.is-active,
.lb-tab-pane.is-active,
.rek-tab-pane.is-active,
.lomba-grid[data-active="true"],
.toko-catalog-grid.is-active {
    animation: fadeSlideUp 0.32s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Accessibility: Nonaktifkan seluruh animasi jika prefers-reduced-motion aktif */
@media (prefers-reduced-motion: reduce) {
    .card-corner-chibi,
    .page-hero-chibi {
        animation: none !important;
    }
    .tab-cascade-animate,
    .tab-content.is-active,
    .tab-pane.is-active,
    .lb-tab-pane.is-active,
    .rek-tab-pane.is-active,
    .lomba-grid[data-active="true"],
    .toko-catalog-grid.is-active {
        animation: none !important;
    }
    .sakura-ripple {
        display: none !important;
        animation: none !important;
    }
    .start-card,
    .activity-start-card,
    .class-card,
    .course-card,
    .division-card,
    .program-card,
    .podium-card,
    .toko-card {
        transform: none !important;
        transition: none !important;
    }
    .card-spotlight-glow {
        display: none !important;
    }
}
"""

if "chibiIdleFloat" not in global_css:
    global_css = global_css.rstrip() + "\n" + global_css_to_add + "\n"
    with open("css/pages/global.css", "w", encoding="utf-8") as f:
        f.write(global_css)
    print("[css/pages/global.css] Berhasil menambahkan spotlight tilt, sakura ripple, chibi idle, & tab cascade")
else:
    print("[css/pages/global.css] Style chibi idle sudah ada")

print("=== SELESAI PENERAPAN 5 MIKRO-INTERAKSI MODERN ===")

