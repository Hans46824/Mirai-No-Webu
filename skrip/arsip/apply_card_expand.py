#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skrip Idempoten Penerapan Mode "Tap-to-Expand" Kartu Beranda & Tentang
Mirai no Webu — Klub Bahasa & Kebudayaan Jepang MIRAI NO HANA
"""

import os
import sys
import re

DRY_RUN = "--dry-run" in sys.argv

def log(msg):
    prefix = "[DRY-RUN]" if DRY_RUN else "[APPLY]"
    print(f"{prefix} {msg}")

# ==============================================================================
# 1. TRANSFORMATION: index.html
# ==============================================================================
def process_index_html(content):
    changed = False
    new_content = content

    # 1.1 Transform start-card
    start_card_pattern = r'<a class="start-card" href="([^"]+)">(.*?)</a>'
    def replace_start_card(match):
        nonlocal changed
        changed = True
        href = match.group(1)
        inner = match.group(2)
        
        chibi = re.search(r'src="([^"]+)"', inner).group(1)
        num = re.search(r'<span class="card-step-num">([^<]+)</span>', inner).group(1)
        title = re.search(r'<h3>([^<]+)</h3>', inner).group(1)
        p = re.search(r'<p>([^<]+)</p>', inner).group(1)
        btn_m = re.search(r'<(?:span|a) class="card-go-btn"[^>]*>([^<]+)</(?:span|a)>', inner)
        btn_text = btn_m.group(1) if btn_m else f"Buka {title} →"
        
        return f"""<div class="start-card nav-card" data-expand-card>
                    <img class="card-corner-chibi" src="{chibi}" alt="" aria-hidden="true">
                    <span class="card-step-num">{num}</span>
                    <h3>{title}</h3>
                    <div class="card-collapsible-content">
                        <div class="card-collapsible-inner">
                            <p>{p}</p>
                        </div>
                    </div>
                    <a class="card-go-btn" href="{href}" data-expand-cta>{btn_text}</a>
                    <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
                </div>"""

    if '<a class="start-card"' in new_content:
        new_content = re.sub(start_card_pattern, replace_start_card, new_content, flags=re.DOTALL)

    # 1.2 Transform activity-start-card
    act_card_pattern = r'<a class="activity-start-card activity-card-active" href="([^"]+)">(.*?)</a>'
    def replace_act_card(match):
        nonlocal changed
        changed = True
        href = match.group(1)
        inner = match.group(2)
        
        chibi = re.search(r'src="([^"]+)"', inner).group(1)
        num = re.search(r'<span class="card-step-num">([^<]+)</span>', inner).group(1)
        title = re.search(r'<h3>([^<]+)</h3>', inner).group(1)
        p = re.search(r'<p>([^<]+)</p>', inner).group(1)
        btn_m = re.search(r'<(?:span|a) class="card-go-btn"[^>]*>([^<]+)</(?:span|a)>', inner)
        btn_text = btn_m.group(1) if btn_m else f"Buka {title} →"
        
        return f"""<div class="activity-start-card nav-card activity-card-active" data-expand-card>
                    <img class="card-corner-chibi" src="{chibi}" alt="" aria-hidden="true">
                    <span class="card-step-num">{num}</span>
                    <h3>{title}</h3>
                    <div class="card-collapsible-content">
                        <div class="card-collapsible-inner">
                            <p>{p}</p>
                        </div>
                    </div>
                    <a class="card-go-btn" href="{href}" data-expand-cta>{btn_text}</a>
                    <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
                </div>"""

    if '<a class="activity-start-card' in new_content:
        new_content = re.sub(act_card_pattern, replace_act_card, new_content, flags=re.DOTALL)

    # 1.3 Card 1: Apa itu Mirai no Webu?
    card1_regex = r'(<div class="about-feature-card"(?! data-expand-card)>.*?<h2 class="about-card-title">Apa itu<br><span class="highlight">Mirai no Webu\?</span></h2>\s*<div class="card-collapsible-content">)\s*(<p class="about-card-desc">.*?</p>)\s*(</div>\s*</div>\s*)(<img class="card-corner-chibi"[^>]*>)\s*(</div>)'
    def replace_card1(m):
        nonlocal changed
        changed = True
        return f"""<div class="about-feature-card" data-expand-card>
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
                        <h2 class="about-card-title">Apa itu<br><span class="highlight">Mirai no Webu?</span></h2>
                        <div class="card-collapsible-content">
                            <div class="card-collapsible-inner">
                                {m.group(2)}
                            </div>
                        </div>
                    </div>
                    <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
                    {m.group(4)}
                </div>"""

    if 'Apa itu<br><span class="highlight">Mirai no Webu?</span></h2>' in new_content and 'data-expand-card' not in new_content.split('Apa itu<br><span class="highlight">Mirai no Webu?</span></h2>')[0].split('<div class="about-feature-card"')[-1]:
        new_content = re.sub(card1_regex, replace_card1, new_content, flags=re.DOTALL)

    # 1.4 Card 2: Tentang Mirai no Hana (laci logo NK)
    card2_regex = r'<div class="about-feature-card about-drawer-card"[^>]*id="mnhAboutDrawerCard"[^>]*>(.*?)<h2 class="about-card-title">Kenali Lebih Dekat<br><span class="highlight">Mirai no Hana\.</span></h2>\s*<div class="card-collapsible-content">\s*(<p class="about-card-desc">.*?</p>)\s*<div class="about-drawer-action">\s*(<a class="btn primary drawer-action-btn" href="tentang/index.html">.*?</a>)\s*</div>\s*</div>\s*</div>\s*(<img class="card-corner-chibi"[^>]*>)\s*(<!--.*?-->)?\s*(<div class="drawer-tray"[^>]*>.*?</div>)\s*</div>'
    def replace_card2(m):
        nonlocal changed
        changed = True
        cta_btn = m.group(3)
        if 'data-expand-cta' not in cta_btn:
            cta_btn = cta_btn.replace('<a class="btn primary drawer-action-btn"', '<a class="btn primary drawer-action-btn" data-expand-cta')
        return f"""<div class="about-feature-card about-drawer-card" id="mnhAboutDrawerCard" role="region" aria-label="Profil Klub Jepang Mirai no Hana" data-expand-card>
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
                        <div class="card-collapsible-content">
                            <div class="card-collapsible-inner">
                                {m.group(2)}
                            </div>
                        </div>
                        <div class="about-drawer-action">
                            {cta_btn}
                        </div>
                    </div>
                    <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
                    {m.group(4)}
                    {m.group(6)}
                </div>"""

    if 'id="mnhAboutDrawerCard"' in new_content and 'data-expand-card' not in new_content.split('id="mnhAboutDrawerCard"')[0].split('<div class="about-feature-card')[-1]:
        new_content = re.sub(card2_regex, replace_card2, new_content, flags=re.DOTALL)

    # 1.5 Card 3: Kritik & Saran di index.html
    card3_regex = r'<div class="feedback-feature-card"(?! data-expand-card)>.*?<div class="feedback-feature-header">\s*(<span class="feedback-feature-tag">.*?</span>)\s*</div>\s*<div class="feedback-feature-body stacked-layout">\s*(<h2 class="feedback-card-title">.*?</h2>)\s*<div class="card-collapsible-content">\s*(<p class="feedback-card-desc">.*?</p>)\s*<div class="feedback-feature-action">\s*(<a class="btn primary feedback-cta-btn" [^>]*>.*?</a>)\s*</div>\s*</div>\s*</div>\s*(<img class="card-corner-chibi"[^>]*>)\s*</div>'
    def replace_card3(m):
        nonlocal changed
        changed = True
        cta_btn = m.group(4)
        if 'data-expand-cta' not in cta_btn:
            cta_btn = cta_btn.replace('<a class="btn primary feedback-cta-btn"', '<a class="btn primary feedback-cta-btn" data-expand-cta')
        return f"""<div class="feedback-feature-card" data-expand-card>
                <div class="feedback-feature-header">
                    {m.group(1)}
                </div>
                <div class="feedback-feature-body stacked-layout">
                    {m.group(2)}
                    <div class="card-collapsible-content">
                        <div class="card-collapsible-inner">
                            {m.group(3)}
                        </div>
                    </div>
                    <div class="feedback-feature-action">
                        {cta_btn}
                    </div>
                </div>
                <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
                {m.group(5)}
            </div>"""

    if '<div class="feedback-feature-card">' in new_content:
        new_content = re.sub(card3_regex, replace_card3, new_content, flags=re.DOTALL)

    return new_content, changed


# ==============================================================================
# 2. TRANSFORMATION: tentang/index.html
# ==============================================================================
def process_tentang_html(content):
    changed = False
    new_content = content

    # Ganti kartu Kritik & Saran di tentang/index.html
    tentang_card_regex = r'<div class="feedback-feature-card"(?! data-expand-card)>.*?<div class="feedback-feature-header">.*?<span class="feedback-feature-tag">.*?</span>\s*</div>\s*<div class="feedback-feature-body stacked-layout">\s*<h2 class="feedback-card-title">.*?</h2>\s*(?:<span class="card-expand-hint">.*?</span>\s*)?<div class="card-collapsible-content">\s*(<p class="feedback-card-desc">.*?</p>)\s*<div class="feedback-feature-action">\s*(<a class="btn primary feedback-cta-btn" [^>]*>.*?</a>)\s*</div>\s*</div>\s*</div>\s*(<img class="card-corner-chibi"[^>]*>)\s*</div>'

    def replace_tentang_card(m):
        nonlocal changed
        changed = True
        cta_btn = m.group(2)
        if 'data-expand-cta' not in cta_btn:
            cta_btn = cta_btn.replace('<a class="btn primary feedback-cta-btn"', '<a class="btn primary feedback-cta-btn" data-expand-cta')
        return f"""<div class="feedback-feature-card" data-expand-card>
                <div class="feedback-feature-header">
                    <span class="feedback-feature-tag">
                        <span class="badge-dot"></span>
                        SUARA MIRAI NO HANA
                    </span>
                </div>
                <div class="feedback-feature-body stacked-layout">
                    <h2 class="feedback-card-title">Kritik &amp;<br><span class="highlight">Saran.</span></h2>
                    <div class="card-collapsible-content">
                        <div class="card-collapsible-inner">
                            {m.group(1)}
                        </div>
                    </div>
                    <div class="feedback-feature-action">
                        {cta_btn}
                    </div>
                </div>
                <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
                {m.group(3)}
            </div>"""

    if '<div class="feedback-feature-card">' in new_content:
        new_content = re.sub(tentang_card_regex, replace_tentang_card, new_content, flags=re.DOTALL)

    return new_content, changed


# ==============================================================================
# 3. TRANSFORMATION: css/pages/kelas-materi.css
# ==============================================================================
def process_kelas_materi_css(content):
    changed = False
    new_content = content

    # Hapus blok lama TAP-TO-EXPAND di kelas-materi.css
    km_pattern = r'/\* =+\s*INTERACTIVE TAP-TO-EXPAND: KARTU NAVIGASI & KELAS.*?(?=/\* =+\s*LATIHAN GABUNGAN|\Z)'
    if re.search(km_pattern, new_content, re.DOTALL):
        new_content = re.sub(km_pattern, '', new_content, flags=re.DOTALL)
        changed = True

    return new_content, changed


# ==============================================================================
# 4. TRANSFORMATION: css/pages/beranda.css
# ==============================================================================
CARD_EXPAND_CSS = """/* MNH-CARD-EXPAND START */
/* ==========================================================================
   INTERACTIVE TAP-TO-EXPAND CARDS (BERANDA & TENTANG)
   Animasi buka-tutup modern berbasis CSS grid-template-rows (0fr -> 1fr).
   ========================================================================== */

/* 1. Tata Letak Grid Responsif Beranda */
.start-grid {
    display: grid !important;
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 20px !important;
    align-items: start !important;
}

@media (min-width: 1400px) {
    .start-grid {
        grid-template-columns: repeat(4, 1fr) !important;
    }
}

.activities-two-grid {
    display: grid !important;
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 22px !important;
    align-items: start !important;
}

.activities-two-grid > .activity-start-card:last-child:nth-child(odd) {
    grid-column: 1 / -1 !important;
}

@media (min-width: 1400px) {
    .activities-two-grid {
        grid-template-columns: repeat(12, 1fr) !important;
    }
    .activities-two-grid > .activity-start-card:nth-child(-n+4) {
        grid-column: span 3 !important;
    }
    .activities-two-grid > .activity-start-card:nth-child(n+5) {
        grid-column: span 4 !important;
    }
    .activities-two-grid > .activity-start-card:last-child:nth-child(odd) {
        grid-column: span 4 !important;
    }
}

/* 2. Format Kartu Navigasi (Tinggi Seragam & Mode Tap-to-Expand) */
.start-card,
.activity-start-card {
    min-height: 232px !important;
    display: flex !important;
    flex-direction: column !important;
    position: relative !important;
    cursor: pointer !important;
    user-select: none !important;
    box-sizing: border-box !important;
    border-radius: 18px !important;
    padding: 24px 22px !important;
    background: #ffffff !important;
    border: 1.5px solid rgba(255, 101, 155, 0.28) !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.04) !important;
    transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.25s ease, box-shadow 0.25s ease !important;
}

body.theme-dark .start-card,
body.theme-dark .activity-start-card {
    background: linear-gradient(160deg, #1d1624, #130f18) !important;
    border-color: rgba(255, 101, 155, 0.22) !important;
}

.start-card.is-expanded,
.activity-start-card.is-expanded,
.about-feature-card.is-expanded,
.feedback-feature-card.is-expanded {
    border-color: var(--pink, #e91e63) !important;
    box-shadow: 0 14px 36px rgba(233, 30, 99, 0.22) !important;
}

/* 3. Animasi Collapsible Modern Grid (0fr -> 1fr) */
.card-collapsible-content {
    display: grid !important;
    grid-template-rows: 0fr !important;
    transition: grid-template-rows 0.35s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.28s ease, margin 0.35s ease !important;
    opacity: 0 !important;
    margin-top: 0 !important;
    margin-bottom: 0 !important;
    pointer-events: none !important;
    position: relative !important;
    z-index: 3 !important;
}

.card-collapsible-content > .card-collapsible-inner {
    overflow: hidden !important;
    min-height: 0 !important;
}

.card-collapsible-content > .card-collapsible-inner p,
.about-card-desc,
.feedback-card-desc {
    margin: 0 !important;
    padding-top: 4px !important;
    padding-bottom: 4px !important;
    font-size: 13.5px !important;
    line-height: 1.55 !important;
    color: #475569 !important;
}

body.theme-dark .card-collapsible-content > .card-collapsible-inner p,
body.theme-dark .about-card-desc,
body.theme-dark .feedback-card-desc {
    color: #cbd5e1 !important;
}

[data-expand-card].is-expanded .card-collapsible-content,
.about-feature-card.is-expanded .card-collapsible-content,
.feedback-feature-card.is-expanded .card-collapsible-content {
    grid-template-rows: 1fr !important;
    opacity: 1 !important;
    margin-top: 10px !important;
    margin-bottom: 8px !important;
    pointer-events: auto !important;
}

/* 4. Tombol Aksi Seragam: Kotak Agak Bundar (Border-Radius: 12px) */
.card-go-btn,
.drawer-action-btn,
.feedback-cta-btn {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 8px !important;
    width: fit-content !important;
    margin-top: auto !important;
    padding: 9px 18px !important;
    background: linear-gradient(135deg, var(--pink, #e91e63), #ff4f91) !important;
    color: #ffffff !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    letter-spacing: 0.3px !important;
    box-shadow: 0 4px 14px rgba(233, 30, 99, 0.35) !important;
    transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease, background 0.2s ease !important;
    text-decoration: none !important;
    line-height: 1.25 !important;
    cursor: pointer !important;
    user-select: none !important;
    z-index: 3 !important;
}

.about-feature-card .drawer-action-btn,
.feedback-feature-card .feedback-cta-btn {
    margin-top: 14px !important;
}

.card-go-btn:hover,
.drawer-action-btn:hover,
.feedback-cta-btn:hover {
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: 0 8px 22px rgba(233, 30, 99, 0.5) !important;
}

.card-go-btn:active,
.drawer-action-btn:active,
.feedback-cta-btn:active {
    transform: translateY(0) scale(0.98) !important;
}

/* 5. Penanda Buka-Tutup: Ikon Panah Chevron CSS Murni */
.card-toggle {
    position: absolute !important;
    top: 18px !important;
    right: 18px !important;
    width: 34px !important;
    height: 34px !important;
    border-radius: 50% !important;
    background: rgba(255, 79, 145, 0.12) !important;
    border: 1px solid rgba(255, 101, 155, 0.28) !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), background 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease !important;
    z-index: 15 !important;
    padding: 0 !important;
    color: var(--pink, #ff659b) !important;
}

.card-toggle::after {
    content: "" !important;
    display: block !important;
    width: 8px !important;
    height: 8px !important;
    border-right: 2px solid currentColor !important;
    border-bottom: 2px solid currentColor !important;
    transform: translateY(-2px) rotate(45deg) !important;
    transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

[data-expand-card].is-expanded .card-toggle::after,
.about-feature-card.is-expanded .card-toggle::after,
.feedback-feature-card.is-expanded .card-toggle::after {
    transform: translateY(2px) rotate(-135deg) !important;
}

.card-toggle:hover {
    background: rgba(255, 79, 145, 0.25) !important;
    border-color: rgba(255, 101, 155, 0.6) !important;
    transform: scale(1.06) !important;
}

.card-toggle:focus-visible,
[data-expand-cta]:focus-visible,
.card-go-btn:focus-visible,
.drawer-action-btn:focus-visible,
.feedback-cta-btn:focus-visible {
    outline: 2px solid var(--pink, #ff4f91) !important;
    outline-offset: 3px !important;
}

/* Sembunyikan elemen lama: panah b dan teks detail hint */
.start-card b,
.activity-start-card b,
.card-expand-hint,
.card-detail-hint {
    display: none !important;
}

/* 6. Kompartemen Laci Geser Logo NK (Melahap Sisi Kanan Tanpa Menggeser Teks dengan Animasi Rotasi) */
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

.about-drawer-card.is-expanded .drawer-tray,
.about-drawer-card.is-pulled .drawer-tray {
    transform: translateX(0) !important;
}

/* Logo NK Besar dengan Efek Animasi Rotasi Halus Spring/Elastic */
.drawer-nk-logo {
    width: clamp(120px, 16vw, 165px) !important;
    height: auto !important;
    object-fit: contain !important;
    filter: drop-shadow(0 10px 28px rgba(233, 30, 99, 0.65)) !important;
    transform: rotate(-180deg) scale(0.4) !important;
    opacity: 0 !important;
    transition: transform 0.55s cubic-bezier(0.34, 1.56, 0.64, 1) 0.08s, opacity 0.35s ease 0.05s !important;
}

.about-drawer-card.is-expanded .drawer-nk-logo,
.about-drawer-card.is-pulled .drawer-nk-logo {
    transform: rotate(0deg) scale(1) !important;
    opacity: 1 !important;
}

/* Efek Memudar Halus Maskot Chibi Pojok Saat Laci Meluncur Masuk */
.about-drawer-card.is-expanded > .card-corner-chibi,
.about-drawer-card.is-pulled > .card-corner-chibi {
    opacity: 0 !important;
    transition: opacity 0.25s ease !important;
}

.about-drawer-action,
.about-drawer-card .drawer-action-btn {
    position: relative !important;
    z-index: 12 !important;
}

.about-drawer-card.is-expanded .card-toggle {
    background: rgba(30, 20, 40, 0.75) !important;
    border-color: rgba(255, 101, 155, 0.5) !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5) !important;
}

/* Responsif Layar Tablet (601px - 900px) untuk Laci Logo NK */
@media (min-width: 601px) and (max-width: 900px) {
    .drawer-tray {
        width: clamp(175px, 28vw, 240px) !important;
        padding: 16px !important;
    }
    .drawer-nk-logo {
        width: clamp(100px, 16vw, 130px) !important;
    }
}

/* Responsif Layar HP (<= 600px) untuk Laci Logo NK (Melahap Sisi Kanan 40-45%) */
@media (max-width: 600px) {
    .drawer-tray {
        width: clamp(140px, 42vw, 175px) !important;
        padding: 12px !important;
    }
    .drawer-nk-logo {
        width: clamp(85px, 24vw, 108px) !important;
    }
}

/* 7. Responsif Layar HP (<= 600px) untuk Kartu Navigasi */
@media (max-width: 600px) {
    .start-grid,
    .activities-two-grid {
        grid-template-columns: 1fr !important;
        gap: 14px !important;
    }

    .activities-two-grid > .activity-start-card:last-child:nth-child(odd) {
        grid-column: auto !important;
    }

    .start-card,
    .activity-start-card {
        display: grid !important;
        grid-template-columns: auto 1fr auto !important;
        grid-template-areas:
            "num title toggle"
            "desc desc desc"
            "btn btn btn" !important;
        align-items: center !important;
        row-gap: 8px !important;
        column-gap: 12px !important;
        min-height: auto !important;
        padding: 15px 16px !important;
    }

    .start-card .card-step-num,
    .activity-start-card .card-step-num {
        grid-area: num !important;
        margin: 0 !important;
        width: 28px !important;
        height: 28px !important;
        font-size: 13px !important;
    }

    .start-card h3,
    .activity-start-card h3 {
        grid-area: title !important;
        margin: 0 !important;
        font-size: 15px !important;
        line-height: 1.25 !important;
        max-width: 100% !important;
    }

    .start-card .card-toggle,
    .activity-start-card .card-toggle {
        grid-area: toggle !important;
        position: static !important;
        width: 32px !important;
        height: 32px !important;
        margin: 0 !important;
    }

    .start-card .card-collapsible-content,
    .activity-start-card .card-collapsible-content {
        grid-area: desc !important;
        width: 100% !important;
    }

    .start-card .card-go-btn,
    .activity-start-card .card-go-btn {
        grid-area: btn !important;
        margin-top: 6px !important;
        max-width: calc(100% - 76px) !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

    .start-card .card-corner-chibi,
    .activity-start-card .card-corner-chibi {
        position: absolute !important;
        width: 62px !important;
        height: 62px !important;
        bottom: 8px !important;
        right: 10px !important;
        z-index: 2 !important;
    }
}

/* 8. Responsif Layar HP (<= 680px) untuk Kartu Fitur Besar */
@media (max-width: 680px) {
    .about-feature-card,
    .feedback-feature-card {
        padding: 18px 18px !important;
        padding-bottom: 24px !important;
    }

    .about-feature-card.is-expanded,
    .feedback-feature-card.is-expanded {
        padding-bottom: 84px !important;
    }

    .about-feature-card > .card-corner-chibi,
    .feedback-feature-card > .card-corner-chibi {
        width: 64px !important;
        height: 64px !important;
        bottom: 10px !important;
        right: 12px !important;
    }

    .about-feature-body.stacked-layout,
    .about-card-desc,
    .feedback-card-desc {
        max-width: 100% !important;
        padding-right: 0 !important;
    }
}

/* 9. Aksesibilitas Reduced Motion */
@media (prefers-reduced-motion: reduce) {
    .card-collapsible-content,
    .card-toggle,
    .card-toggle::after,
    .drawer-tray,
    .about-feature-body,
    .drawer-nk-logo {
        transition: none !important;
    }
}
/* MNH-CARD-EXPAND END */"""

def process_beranda_css(content):
    changed = False
    new_content = content

    # 1. Hapus blok lama INTERACTIVE TAP-TO-EXPAND di beranda.css
    b_pattern1 = r'/\* =+\s*INTERACTIVE TAP-TO-EXPAND: KARTU FITUR BERANDA.*?(?=/\* =+\s*RESPONSIF MOBILE / HP|\Z)'
    if re.search(b_pattern1, new_content, re.DOTALL):
        new_content = re.sub(b_pattern1, '', new_content, flags=re.DOTALL)
        changed = True

    # 2. Hapus override lama di bagian akhir beranda.css (display:block !important dan max-height:none !important)
    b_pattern2 = r'/\* Pastikan deskripsi <p> pada start-card & activity-start-card selalu tampil rapi \*/.*?(?=/\* MNH-CARD-EXPAND START|\Z)'
    if re.search(b_pattern2, new_content, re.DOTALL):
        new_content = re.sub(b_pattern2, '', new_content, flags=re.DOTALL)
        changed = True

    # 2.5 Hapus aturan lama drawer-tray width: 100% di media query 680px
    old_mobile_drawer = r'\s*\.drawer-tray\s*\{[^}]*width:\s*100%\s*!important;[^}]*\}\s*\.about-drawer-card\.is-pulled\s*\.drawer-tray[^{]*\{[^}]*\}\s*\.drawer-nk-logo\s*\{[^}]*\}'
    if re.search(old_mobile_drawer, new_content):
        new_content = re.sub(old_mobile_drawer, '', new_content)
        changed = True

    # 3. Tulis/ganti blok MNH-CARD-EXPAND START/END
    if '/* MNH-CARD-EXPAND START */' in new_content:
        expand_pattern = r'/\* MNH-CARD-EXPAND START \*/.*?/\* MNH-CARD-EXPAND END \*/'
        if re.search(expand_pattern, new_content, re.DOTALL):
            new_content = re.sub(expand_pattern, CARD_EXPAND_CSS, new_content, flags=re.DOTALL)
            changed = True
    else:
        new_content = new_content.rstrip() + "\n\n" + CARD_EXPAND_CSS + "\n"
        changed = True

    return new_content, changed


# ==============================================================================
# 5. TRANSFORMATION: js/main.js
# ==============================================================================
EXPAND_JS_CODE = """function setupExpandableCards() {
    const cards = document.querySelectorAll("[data-expand-card]");
    if (!cards.length) return;

    cards.forEach((card) => {
        // Klik di dalam kartu
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
        const toggleBtn = card.querySelector(".card-toggle");
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

        // Jika kartu laci logo NK: sinkronkan status .is-pulled
        if (card.classList.contains("about-drawer-card") || card.id === "mnhAboutDrawerCard") {
            card.classList.toggle("is-pulled", shouldOpen);
        }

        const toggleBtn = card.querySelector(".card-toggle");
        if (toggleBtn) {
            toggleBtn.setAttribute("aria-expanded", shouldOpen ? "true" : "false");
            toggleBtn.setAttribute("aria-label", shouldOpen ? "Tutup detail kartu" : "Buka detail kartu");
        }
    }
}
"""

def process_main_js(content):
    changed = False
    new_content = content

    # 1. Di DOMContentLoaded: ganti setupAboutDrawerCard() & setupTapToExpandCards() dengan setupExpandableCards()
    if "setupAboutDrawerCard();" in new_content:
        new_content = new_content.replace("setupAboutDrawerCard();", "setupExpandableCards();")
        changed = True
    if "setupTapToExpandCards();" in new_content:
        new_content = new_content.replace("setupTapToExpandCards();\n", "")
        new_content = new_content.replace("setupTapToExpandCards();", "")
        changed = True

    # 2. Ganti fungsi setupAboutDrawerCard dan setupTapToExpandCards dengan setupExpandableCards
    func_pattern = r'function setupAboutDrawerCard\(\)\s*\{.*?\n\}\s*(?:\nfunction setupTapToExpandCards\(\)\s*\{.*?\n\})?'
    if re.search(func_pattern, new_content, re.DOTALL):
        new_content = re.sub(func_pattern, EXPAND_JS_CODE, new_content, flags=re.DOTALL)
        changed = True
    elif "function setupExpandableCards()" not in new_content:
        new_content = new_content.rstrip() + "\n\n" + EXPAND_JS_CODE + "\n"
        changed = True

    # 3. Pastikan jeda baris rapi setelah penutup fungsi setupExpandableCards
    if "}/* =" in new_content:
        new_content = new_content.replace("}/* =", "}\n\n/* =")
        changed = True

    return new_content, changed


# ==============================================================================
# 6. DOCUMENTATION UPDATES (agent.md, tree.md, skrip/README.md)
# ==============================================================================
AGENT_SECTION = """
### N. Standar Kartu Expandable Beranda & Tentang (Tap-to-Expand Standard)
- **Arsitektur Tap-to-Expand**:
  - Kartu navigasi Beranda (`.start-card`, `.activity-start-card`) dan kartu fitur besar (`.about-feature-card`, `.feedback-feature-card`) menggunakan tag `<div>` dengan atribut `[data-expand-card]`, BUKAN tag link pembungkus `<a>`.
  - **Kondisi Awal (Collapsed)**: Hanya menampilkan nomor urut (`.card-step-num`), judul (`<h3>` atau `<h2>`), maskot chibi di pojok kanan bawah, tombol aksi CTA, dan tombol panah buka-tutup (`.card-toggle`). Deskripsi disembunyikan.
  - **Kondisi Terbuka (`.is-expanded`)**: Mengetuk kartu atau tombol panah membuka deskripsi menggunakan transisi CSS Grid modern `grid-template-rows: 0fr -> 1fr` (`.card-collapsible-content > .card-collapsible-inner`) tanpa `display: none` agar animasi berjalan mulus.
  - **Perilaku Tombol Aksi (`[data-expand-cta]`)**:
    * Jika tombol ditekan saat kartu masih tertutup: kartu membuka terlebih dahulu, tidak langsung berpindah halaman.
    * Jika tombol ditekan saat kartu sudah terbuka: berpindah ke halaman tujuan.
    * Kombinasi Ctrl/Cmd/Shift/Alt klik dibiarkan membuka tab baru secara normal.
  - **Format Tombol Seragam**: Seluruh tombol aksi kartu berformat kotak agak bundar (`border-radius: 12px`).
  - **Ikon Panah Toggle (`.card-toggle`)**: Menggunakan chevron CSS murni di sudut kanan atas dengan atribut `aria-expanded` dan styling `:focus-visible`.
  - **Laci Logo NK (`#mnhAboutDrawerCard`)**: Tampil di seluruh ukuran layar (desktop, tablet, mobile). Saat kartu diekspansi (`.is-expanded` / `.is-pulled`), laci logo NK meluncur keluar dari kanan (`transform: translateX(0)`) melahap/memakan sisi kanan kartu tanpa menggeser teks, disertai animasi rotasi spring/elastic logo NK (`rotate(-180deg) scale(0.4) -> rotate(0deg) scale(1)`).
  - **Tata Letak Responsif**:
    * `.start-grid`: 2 kolom di tablet/desktop, 4 kolom di layar lebar `>= 1400px`, 1 kolom di HP `<= 600px`.
    * `.activities-two-grid`: 2 kolom di tablet/desktop (kartu ganjil terakhir span penuh), 12 kolom di `>= 1400px` (4 kartu span 3, 3 kartu span 4), 1 kolom di HP `<= 600px`.
    * HP (`<= 600px`): Nomor urut, judul, dan panah tertata dalam 1 baris, tombol `max-width: calc(100% - 76px)` dan maskot chibi 62px di pojok kanan bawah.
"""

def process_agent_md(content):
    changed = False
    new_content = content
    pattern = r'### N\. Standar Kartu Expandable Beranda & Tentang.*?(?=\n---\n|## 5\.|\Z)'
    if re.search(pattern, new_content, re.DOTALL):
        updated = re.sub(pattern, AGENT_SECTION.strip() + "\n\n", new_content, flags=re.DOTALL)
        if updated != new_content:
            new_content = updated
            changed = True
    elif "### N. Standar Kartu Expandable Beranda & Tentang" not in new_content:
        anchor = "## 5. Perawatan & Pengelolaan Fitur Chat Sora"
        if anchor in new_content:
            new_content = new_content.replace(anchor, AGENT_SECTION.strip() + "\n\n---\n\n" + anchor)
            changed = True
        else:
            new_content = new_content.rstrip() + "\n\n" + AGENT_SECTION + "\n"
            changed = True
    return new_content, changed

def process_tree_md(content):
    changed = False
    new_content = content
    if "apply_card_expand.py" not in new_content:
        anchor = "├── skrip/                          # Pemeliharaan Kode Python\n│   ├── README.md                   # Panduan skrip pengembang\n│   └── arsip/                      # Arsip skrip perbaikan sekali-pakai (dikecualikan dari watcher)\n"
        replacement = anchor + "│       ├── apply_card_expand.py\n"
        if anchor in new_content:
            new_content = new_content.replace(anchor, replacement)
            changed = True
        else:
            new_content = new_content.replace("│   └── arsip/", "│   └── arsip/\n│       ├── apply_card_expand.py")
            changed = True
    return new_content, changed

def process_skrip_readme(content):
    changed = False
    new_content = content
    entry = "- **`apply_card_expand.py`**: Skrip idempoten pembaruan mode interaktif tap-to-expand pada kartu Beranda dan Tentang.\n"
    if "apply_card_expand.py" not in new_content:
        anchor = "## Fungsi Skrip-Skrip:\n"
        if anchor in new_content:
            new_content = new_content.replace(anchor, anchor + entry)
            changed = True
        else:
            new_content = new_content.rstrip() + "\n" + entry
            changed = True
    return new_content, changed


# ==============================================================================
# VALIDATION UTILITIES
# ==============================================================================
def check_bracket_balance(text):
    stack = []
    in_string = None
    in_comment = False
    in_line_comment = False
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if in_line_comment:
            if c == '\n': in_line_comment = False
        elif in_comment:
            if c == '*' and i + 1 < n and text[i+1] == '/':
                in_comment = False
                i += 1
        elif in_string:
            if c == '\\\\': i += 1
            elif c == in_string: in_string = None
        else:
            if c == '/' and i + 1 < n:
                if text[i+1] == '/': in_line_comment = True; i += 1
                elif text[i+1] == '*': in_comment = True; i += 1
            elif c in ['"', "'", '`']:
                in_string = c
            elif c in '([{':
                stack.append((c, i))
            elif c in ')]}':
                if not stack:
                    return f"Unexpected closing {c} at {i}"
                open_c, _ = stack.pop()
                if (open_c == '(' and c != ')') or (open_c == '[' and c != ']') or (open_c == '{' and c != '}'):
                    return f"Mismatched {open_c} and {c} at {i}"
        i += 1
    if stack:
        return f"Unclosed brackets: {len(stack)} items left on stack"
    return "OK"

def check_css_brace_balance(text):
    open_count = text.count('{')
    close_count = text.count('}')
    return open_count == close_count, open_count, close_count

def check_html_tags(text):
    for tag in ['div', 'section', 'article', 'button', 'a', 'p', 'h2', 'h3']:
        opens = len(re.findall(rf'<{tag}(?:\s+[^>]*)?>', text, re.IGNORECASE))
        closes = len(re.findall(rf'</{tag}>', text, re.IGNORECASE))
        if opens != closes:
            return False, f"Tag <{tag}> unbalance: opens={opens}, closes={closes}"
    return True, "OK"


# ==============================================================================
# MAIN RUNNER
# ==============================================================================
def main():
    print("===================================================================")
    print("  MIRAI NO WEBU - TAP-TO-EXPAND CARD AUTOMATION & CLEANUP")
    print("===================================================================")
    if DRY_RUN:
        log("Mode DRY-RUN aktif: tidak ada berkas yang ditulis ke disk.")

    files_to_process = [
        ("index.html", process_index_html),
        ("tentang/index.html", process_tentang_html),
        ("css/pages/kelas-materi.css", process_kelas_materi_css),
        ("css/pages/beranda.css", process_beranda_css),
        ("js/main.js", process_main_js),
        ("panduan/agent.md", process_agent_md),
        ("panduan/tree.md", process_tree_md),
        ("skrip/README.md", process_skrip_readme)
    ]

    modified_files = []

    for filepath, processor in files_to_process:
        if not os.path.exists(filepath):
            log(f"Berkas tidak ditemukan: {filepath}")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            original_content = f.read()

        new_content, changed = processor(original_content)

        if changed and new_content != original_content:
            modified_files.append(filepath)
            log(f"Perubahan terdeteksi pada: {filepath}")
            if not DRY_RUN:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                log(f"Berhasil menyimpan pembaruan: {filepath}")
        else:
            log(f"Tidak ada perubahan (sudah mutakhir): {filepath}")

    print("\n--- HASIL PEMROSESAN ---")
    if modified_files:
        print(f"Total {len(modified_files)} berkas mengalami perubahan:")
        for mf in modified_files:
            print(f"  * {mf}")
    else:
        print("Semua berkas sudah dalam kondisi mutakhir (idempoten).")

    # ==========================================================================
    # VALIDASI INTEGRITAS
    # ==========================================================================
    print("\n--- VALIDASI INTEGRITAS & SINTAKS ---")

    # 1. Validasi js/main.js
    if os.path.exists("js/main.js"):
        with open("js/main.js", "r", encoding="utf-8") as f:
            js_txt = f.read()
        res_js = check_bracket_balance(js_txt)
        print(f"1. JS Bracket Balance (js/main.js): {res_js}")
        assert res_js == "OK", f"Error pada sintaks js/main.js: {res_js}"

    # 2. Validasi HTML tags
    for hf in ["index.html", "tentang/index.html"]:
        if os.path.exists(hf):
            with open(hf, "r", encoding="utf-8") as f:
                htxt = f.read()
            ok, msg = check_html_tags(htxt)
            print(f"2. HTML Tag Balance ({hf}): {msg}")
            assert ok, f"Error pada tag HTML {hf}: {msg}"

    # 3. Validasi CSS braces
    for cf in ["css/pages/beranda.css", "css/pages/kelas-materi.css"]:
        if os.path.exists(cf):
            with open(cf, "r", encoding="utf-8") as f:
                ctxt = f.read()
            ok, opens, closes = check_css_brace_balance(ctxt)
            print(f"3. CSS Brace Balance ({cf}): opens={opens}, closes={closes} -> {'OK' if ok else 'FAIL'}")
            assert ok, f"Error kurung kurawal CSS tidak seimbang pada {cf}!"

    print("\n=== SEMUA VALIDASI BERHASIL 100%! ===")

if __name__ == "__main__":
    main()
