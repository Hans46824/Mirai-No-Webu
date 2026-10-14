import re

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target_about_section = """        <section class="section about-preview">
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

replacement_about_section = """        <section class="section about-preview">
            <div class="section-intro">
                <p class="section-eyebrow"><span class="jp-kanji">ウェブについて</span></p>
                <h2 class="heading">Apa itu<br><span>Mirai no Webu?</span></h2>
                <p class="section-desc">Fasilitas belajar digital interaktif untuk mendalami bahasa dan kebudayaan Jepang.</p>
            </div>
            <div class="about-cards-wrap">
                <!-- CARD 1: MIRAI NO WEBU (FASILITAS BELAJAR DIGITAL - ATAS) -->
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
                    </div>
                    <img class="card-corner-chibi" src="images/mirai/icon/Ay.png" alt="Mascot Mirai No Webu" aria-hidden="true">
                </div>

                <!-- CARD 2: TENTANG MIRAI NO HANA (LACI GESER LOGO NK - BAWAH) -->
                <div class="about-feature-card about-drawer-card" id="mnhAboutDrawerCard" role="region" aria-label="Profil Klub Jepang Mirai no Hana">
                    <div class="about-feature-header">
                        <span class="about-feature-badge">
                            <span class="badge-dot"></span>
                            PROFIL KLUB JEPANG
                        </span>
                        <span class="about-feature-tag">
                            <span class="badge-dot"></span>
                            TENTANG KAMI
                        </span>
                    </div>
                    <div class="about-feature-body stacked-layout">
                        <h2 class="about-card-title">Kenali Lebih Dekat<br><span class="highlight">Mirai no Hana.</span></h2>
                        <p class="about-card-desc">Jelajahi profil lengkap Mirai no Hana mulai dari sejarah berdirinya klub, visi &amp; misi, filosofi logo serta haori resmi, struktur kepengurusan siswa, linimasa perjalanan, hingga serba-serbi maskot klub.</p>
                        <div class="about-drawer-action">
                            <a class="btn primary drawer-action-btn" href="tentang/index.html">
                                <span class="drawer-btn-text">TENTANG MIRAI NO HANA</span>
                                <span class="btn-arrow">→</span>
                            </a>
                        </div>
                    </div>
                    
                    <!-- Kompartemen Laci Geser Logo NK (Melahap Sisi Kanan Tanpa Menggeser Teks) -->
                    <div class="drawer-tray" aria-hidden="true">
                        <img class="drawer-nk-logo" src="images/mirai/logo/NK.png" alt="Logo Nihongo Kurabu">
                    </div>
                </div>
            </div>
        </section>"""

if target_about_section in html:
    html = html.replace(target_about_section, replacement_about_section, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('[index.html] Successfully updated about section markup!')
else:
    print('[index.html] Error: target_about_section not found')

# 2. Update css/pages/beranda.css
with open('css/pages/beranda.css', 'r', encoding='utf-8') as f:
    beranda_css = f.read()

# Replace previous drawer css section
drawer_pattern = re.compile(r'/\* =+\s*ABOUT PREVIEW — 2 CARDS GRID & DRAWER LOGO NK.*', re.DOTALL)
if drawer_pattern.search(beranda_css):
    beranda_css = drawer_pattern.sub('', beranda_css).rstrip()

new_drawer_css = """
/* =====================================================
   ABOUT PREVIEW — BERTUMPUK ATAS-BAWAH & DRAWER LOGO NK
   ===================================================== */
.about-cards-wrap {
    display: flex !important;
    flex-direction: column !important;
    gap: 24px !important;
    max-width: 1200px !important;
    margin: 0 auto !important;
    width: 100% !important;
}

/* Card 2: Tentang Mirai no Hana dengan Garis Vertikal Kiri */
.about-drawer-card {
    border-left: 6px solid var(--pink, #e91e63) !important;
    cursor: pointer !important;
    user-select: none !important;
    position: relative !important;
    overflow: hidden !important;
    transition: transform 0.28s ease, border-color 0.28s ease, box-shadow 0.28s ease !important;
}

.about-drawer-card:hover {
    transform: translateY(-5px) !important;
    border-color: var(--pink, #e91e63) !important;
    box-shadow: 0 24px 50px rgba(233, 30, 99, 0.26), 0 6px 18px rgba(0, 0, 0, 0.6) !important;
}

/* Tombol Tentang Mirai no Hana Berbentuk Agak Lingkaran / Rounded Pill */
.about-drawer-action {
    margin-top: 20px !important;
}

.about-drawer-action .drawer-action-btn {
    border-radius: 999px !important;
    padding: 13px 32px !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 10px !important;
    box-shadow: 0 8px 24px rgba(233, 30, 99, 0.35) !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

.about-drawer-action .drawer-action-btn:hover {
    transform: translateY(-3px) scale(1.03) !important;
    box-shadow: 0 12px 30px rgba(233, 30, 99, 0.55) !important;
}

/* Kompartemen Laci Geser Logo NK (Melahap Sisi Kanan Tanpa Menggeser Teks) */
.drawer-tray {
    position: absolute !important;
    top: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    width: clamp(220px, 30vw, 340px) !important;
    background: linear-gradient(135deg, rgba(32, 22, 42, 0.98), rgba(15, 11, 20, 0.99)) !important;
    border-left: 2px solid rgba(255, 79, 145, 0.6) !important;
    box-shadow: -20px 0 50px rgba(0, 0, 0, 0.85), inset 1px 0 0 rgba(255, 255, 255, 0.1) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 24px !important;
    box-sizing: border-box !important;
    transform: translateX(105%) !important;
    transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1) !important;
    z-index: 10 !important;
    pointer-events: none !important;
}

.about-drawer-card.is-pulled .drawer-tray {
    transform: translateX(0) !important;
}

/* Logo NK Besar dengan Efek Animasi Rotasi */
.drawer-nk-logo {
    width: clamp(120px, 16vw, 165px) !important;
    height: auto !important;
    object-fit: contain !important;
    filter: drop-shadow(0 10px 28px rgba(233, 30, 99, 0.65)) !important;
    transform: rotate(-180deg) scale(0.4) !important;
    opacity: 0 !important;
    transition: transform 0.55s cubic-bezier(0.34, 1.56, 0.64, 1) 0.08s, opacity 0.35s ease 0.05s !important;
}

.about-drawer-card.is-pulled .drawer-nk-logo {
    transform: rotate(0deg) scale(1) !important;
    opacity: 1 !important;
}

@media (max-width: 600px) {
    .drawer-tray {
        width: 170px !important;
        padding: 14px !important;
    }
    .drawer-nk-logo {
        width: 105px !important;
    }
}
"""

beranda_css += "\n" + new_drawer_css
with open('css/pages/beranda.css', 'w', encoding='utf-8') as f:
    f.write(beranda_css)
print('[beranda.css] Successfully updated styles for stacked cards and rotating logo drawer!')

# 3. Update js/main.js
with open('js/main.js', 'r', encoding='utf-8') as f:
    main_js = f.read()

# Replace setupAboutDrawerCard implementation
js_pattern = re.compile(r'function setupAboutDrawerCard\(\)\s*\{.*?\}\n?', re.DOTALL)
new_js_func = """function setupAboutDrawerCard() {
    const card = document.getElementById("mnhAboutDrawerCard");
    if (!card) return;

    card.addEventListener("click", (e) => {
        // Jika yang diklik adalah tombol link Tentang, biarkan langsung bernavigasi
        if (e.target.closest(".drawer-action-btn")) {
            return;
        }

        // Klik pada card: TOGGLE BUKA / TUTUP LACI (efek membuka dan menutup laci kembali)
        card.classList.toggle("is-pulled");
    });

    // Aksesibilitas keyboard (Enter / Spasi untuk toggle)
    card.addEventListener("keydown", (e) => {
        if ((e.key === "Enter" || e.key === " ") && !e.target.closest(".drawer-action-btn")) {
            e.preventDefault();
            card.classList.toggle("is-pulled");
        }
    });
}
"""

if js_pattern.search(main_js):
    main_js = js_pattern.sub(new_js_func, main_js)
else:
    main_js += "\n" + new_js_func

with open('js/main.js', 'w', encoding='utf-8') as f:
    f.write(main_js)
print('[main.js] Successfully updated setupAboutDrawerCard toggle logic!')

print('All 12 items successfully implemented!')
