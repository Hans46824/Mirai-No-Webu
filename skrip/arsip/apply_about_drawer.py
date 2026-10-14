import re

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target_about_preview = """        <section class="section about-preview">
            <div class="section-intro">
                <p class="section-eyebrow"><span class="jp-kanji">ウェブについて</span></p>
                <h2 class="heading">Apa itu<br><span>Mirai no Webu?</span></h2>
                <p class="section-desc">Pusat belajar digital interaktif untuk mendalami bahasa dan kebudayaan Jepang.</p>
            </div>
            <div class="about-feature-card">
                <div class="about-feature-header">
                    <span class="about-feature-badge">
                        <span class="badge-dot"></span>
                        PUSAT BELAJAR DIGITAL
                    </span>
                    <span class="about-feature-tag">
                        <span class="badge-dot"></span>
                        MIRAI NO WEBU
                    </span>
                </div>
                <div class="about-feature-body stacked-layout">
                    <h2 class="about-card-title">Belajar di mana pun,<br><span class="highlight">dan kapanpun.</span></h2>
                    <p class="about-card-desc">Mirai no Webu hadir sebagai pusat belajar digital interaktif untuk mendalami bahasa dan budaya Jepang. Lebih dari sekadar modul pembelajaran, web ini adalah jembatan untuk mengenal lebih dekat keseruan program, sejarah, dan makna dari Mirai no Hana Nihongo Kurabu.</p>
                    <div class="about-feature-action">
                        <a class="btn primary about-cta-btn" href="tentang/index.html">
                            <span>TENTANG MIRAI NO HANA</span>
                            <span class="btn-arrow">→</span>
                        </a>
                    </div>
                </div>
                <img class="card-corner-chibi" src="images/mirai/icon/Ay.png" alt="Mascot Mirai No Webu" aria-hidden="true">
            </div>
        </section>"""

replacement_about_preview = """        <section class="section about-preview">
            <div class="section-intro">
                <p class="section-eyebrow"><span class="jp-kanji">ウェブについて</span></p>
                <h2 class="heading">Apa itu<br><span>Mirai no Webu?</span></h2>
                <p class="section-desc">Fasilitas belajar digital interaktif untuk mendalami bahasa dan kebudayaan Jepang.</p>
            </div>
            <div class="about-cards-wrap">
                <!-- CARD 1: MIRAI NO WEBU (FASILITAS BELAJAR DIGITAL) -->
                <div class="about-feature-card">
                    <div class="about-feature-header">
                        <span class="about-feature-badge">
                            <span class="badge-dot"></span>
                            FASILITAS BELAJAR DIGITAL
                        </span>
                        <span class="about-feature-tag">
                            <span class="badge-dot"></span>
                            MIRAI NO WEBU
                        </span>
                    </div>
                    <div class="about-feature-body stacked-layout">
                        <h2 class="about-card-title">Belajar di mana pun,<br><span class="highlight">dan kapanpun.</span></h2>
                        <p class="about-card-desc">Berfungsi sebagai fasilitas belajar mandiri yang bertujuan mempermudah anggota menguasai aksara, kosakata, dan tata bahasa Jepang secara terstruktur, interaktif, dan fleksibel.</p>
                        <div class="about-feature-action">
                            <a class="btn primary about-cta-btn" href="kelas/index.html">
                                <span>JELAJAHI KELAS &amp; MATERI</span>
                                <span class="btn-arrow">→</span>
                            </a>
                        </div>
                    </div>
                    <img class="card-corner-chibi" src="images/mirai/icon/Ay.png" alt="Mascot Mirai No Webu" aria-hidden="true">
                </div>

                <!-- CARD 2: TENTANG MIRAI NO HANA (LACI GESER LOGO NK) -->
                <div class="about-feature-card about-drawer-card" id="mnhAboutDrawerCard" role="button" tabindex="0" aria-label="Buka profil Tentang Mirai no Hana">
                    <div class="about-feature-header">
                        <span class="about-feature-badge">
                            <span class="badge-dot"></span>
                            PROFIL KLUB JEJEPANGAN
                        </span>
                        <span class="about-feature-tag">
                            <span class="badge-dot"></span>
                            TENTANG KAMI
                        </span>
                    </div>
                    <div class="about-feature-body stacked-layout">
                        <h2 class="about-card-title">Kenali Lebih Dekat<br><span class="highlight">Mirai no Hana.</span></h2>
                        <p class="about-card-desc">Ingin tahu lebih banyak tentang wadah kreativitas kami? Yuk, kenali sejarah perjalanan, visi-misi, kepengurusan siswa, filosofi haori, dan keseruan kegiatan yang kami bangun bersama!</p>
                        <div class="about-drawer-action">
                            <a class="btn primary drawer-action-btn" href="tentang/index.html">
                                <span class="drawer-btn-text">TENTANG MIRAI NO HANA</span>
                                <span class="btn-arrow">→</span>
                            </a>
                            <span class="drawer-hint">
                                <span class="drawer-hint-dot"></span>
                                <span class="drawer-hint-text">Klik kartu untuk menarik laci profil</span>
                            </span>
                        </div>
                    </div>
                    
                    <!-- Kompartemen Laci Geser Logo NK (Drawer Tray) -->
                    <div class="drawer-tray" aria-hidden="true">
                        <div class="drawer-pull-tab">
                            <span class="drawer-pull-line"></span>
                        </div>
                        <div class="drawer-content-box">
                            <img class="drawer-nk-logo" src="images/mirai/logo/NK.png" alt="Logo Nihongo Kurabu">
                            <span class="drawer-nk-title">NIHONGO KURABU</span>
                            <span class="drawer-nk-sub">MIRAI NO HANA</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>"""

if target_about_preview in html:
    html = html.replace(target_about_preview, replacement_about_preview, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('[index.html] Successfully updated with 2 cards!')
else:
    print('[index.html] Error: target_about_preview not found')

# 2. Update css/pages/beranda.css
with open('css/pages/beranda.css', 'r', encoding='utf-8') as f:
    beranda_css = f.read()

new_drawer_css = """
/* =====================================================
   ABOUT PREVIEW — 2 CARDS GRID & DRAWER LOGO NK
   ===================================================== */
.about-cards-wrap {
    display: grid !important;
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    gap: 24px !important;
    max-width: 1200px !important;
    margin: 0 auto !important;
    align-items: stretch !important;
}

@media (max-width: 960px) {
    .about-cards-wrap {
        grid-template-columns: 1fr !important;
        gap: 20px !important;
    }
}

/* Card 2: Tentang Mirai no Hana dengan Garis Vertikal Kiri & Animasi Laci */
.about-drawer-card {
    border-left: 6px solid var(--pink, #e91e63) !important;
    cursor: pointer !important;
    user-select: none !important;
    transition: transform 0.28s ease, border-color 0.28s ease, box-shadow 0.28s ease, padding 0.35s ease !important;
}

.about-drawer-card:hover {
    transform: translateY(-5px) !important;
    border-color: var(--pink, #e91e63) !important;
    box-shadow: 0 24px 50px rgba(233, 30, 99, 0.26), 0 6px 18px rgba(0, 0, 0, 0.6) !important;
}

.about-drawer-card .about-feature-body {
    transition: padding-right 0.38s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

.about-drawer-card.is-pulled .about-feature-body {
    padding-right: 140px !important;
}

/* Kompartemen Laci Geser Logo NK (Drawer Tray) */
.drawer-tray {
    position: absolute !important;
    top: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    width: 145px !important;
    background: linear-gradient(135deg, rgba(28, 20, 36, 0.98), rgba(16, 12, 22, 0.99)) !important;
    border-left: 1.5px solid rgba(255, 79, 145, 0.45) !important;
    box-shadow: -14px 0 38px rgba(0, 0, 0, 0.75) !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 16px !important;
    box-sizing: border-box !important;
    transform: translateX(100%) !important;
    transition: transform 0.45s cubic-bezier(0.16, 1, 0.3, 1) !important;
    z-index: 5 !important;
    pointer-events: none !important;
}

.about-drawer-card.is-pulled .drawer-tray {
    transform: translateX(0) !important;
}

/* Pegangan / Tab Laci yang terlihat mengintip */
.drawer-pull-tab {
    position: absolute !important;
    left: -14px !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    width: 14px !important;
    height: 52px !important;
    background: var(--pink, #e91e63) !important;
    border-radius: 6px 0 0 6px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: -4px 0 14px rgba(233, 30, 99, 0.55) !important;
}

.drawer-pull-line {
    width: 2.5px !important;
    height: 22px !important;
    background: #ffffff !important;
    border-radius: 2px !important;
}

.about-drawer-card.is-pulled .drawer-pull-tab {
    opacity: 0 !important;
    visibility: hidden !important;
}

/* Konten Logo NK di Dalam Laci */
.drawer-content-box {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    text-align: center !important;
    gap: 8px !important;
    transform: scale(0.85) !important;
    opacity: 0.7 !important;
    transition: transform 0.45s cubic-bezier(0.34, 1.56, 0.64, 1) 0.1s, opacity 0.35s ease 0.1s !important;
}

.about-drawer-card.is-pulled .drawer-content-box {
    transform: scale(1) !important;
    opacity: 1 !important;
}

.drawer-nk-logo {
    width: 82px !important;
    height: auto !important;
    object-fit: contain !important;
    filter: drop-shadow(0 6px 18px rgba(233, 30, 99, 0.55)) !important;
}

.drawer-nk-title {
    font-size: 11px !important;
    font-weight: 800 !important;
    letter-spacing: 1.5px !important;
    color: var(--pink, #ff4f91) !important;
    text-transform: uppercase !important;
}

.drawer-nk-sub {
    font-size: 9.5px !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    letter-spacing: 1px !important;
    opacity: 0.85 !important;
}

/* Action & Hint Text */
.about-drawer-action {
    display: flex !important;
    align-items: center !important;
    gap: 16px !important;
    flex-wrap: wrap !important;
    margin-top: 14px !important;
}

.drawer-hint {
    display: inline-flex !important;
    align-items: center !important;
    gap: 7px !important;
    font-size: 12px !important;
    color: var(--pink, #ff659b) !important;
    font-weight: 600 !important;
    letter-spacing: 0.4px !important;
}

.drawer-hint-dot {
    width: 6px !important;
    height: 6px !important;
    border-radius: 50% !important;
    background: var(--pink, #e91e63) !important;
    box-shadow: 0 0 8px var(--pink, #e91e63) !important;
    animation: drawerPulse 1.8s infinite !important;
}

@keyframes drawerPulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.4); opacity: 0.6; }
}

@media (max-width: 600px) {
    .about-drawer-card.is-pulled .about-feature-body {
        padding-right: 110px !important;
    }
    .drawer-tray {
        width: 115px !important;
        padding: 10px !important;
    }
    .drawer-nk-logo {
        width: 64px !important;
    }
}
"""

beranda_css += new_drawer_css
with open('css/pages/beranda.css', 'w', encoding='utf-8') as f:
    f.write(beranda_css)
print('[beranda.css] Successfully added drawer styles!')

# 3. Update js/main.js
with open('js/main.js', 'r', encoding='utf-8') as f:
    main_js = f.read()

target_dom = '    setupFooterQuoteSlider();'
replacement_dom = '''    setupFooterQuoteSlider();
    setupAboutDrawerCard();'''

if target_dom in main_js:
    main_js = main_js.replace(target_dom, replacement_dom, 1)

function_code = """
function setupAboutDrawerCard() {
    const card = document.getElementById("mnhAboutDrawerCard");
    if (!card) return;

    let isPulled = false;

    card.addEventListener("click", (e) => {
        // Jika belum ditarik: klik 1x menarik laci keluar menampilkan logo NK
        if (!isPulled) {
            e.preventDefault();
            isPulled = true;
            card.classList.add("is-pulled");
            const hintText = card.querySelector(".drawer-hint-text");
            if (hintText) {
                hintText.textContent = "Laci terbuka! Klik lagi untuk menuju halaman Tentang →";
            }
            const btnText = card.querySelector(".drawer-btn-text");
            if (btnText) {
                btnText.textContent = "BUKA PROFIL SEKARANG";
            }
        } else {
            // Jika sudah ditarik: klik lagi langsung pergi ke page tentang
            window.location.href = "tentang/index.html";
        }
    });

    // Aksesibilitas keyboard (Enter / Spasi)
    card.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            card.click();
        }
    });
}
"""

main_js += function_code
with open('js/main.js', 'w', encoding='utf-8') as f:
    f.write(main_js)
print('[main.js] Successfully added setupAboutDrawerCard()!')

print('All changes applied successfully!')
