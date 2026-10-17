#!/usr/bin/env python3
"""
apply_tap_to_expand_kelas.py
Menerapkan sistem tap-to-expand ke:
1. kelas/index.html (seksi #dasar, #lanjutan, #kurikulum)
2. materi/dasar/index.html (.material-grid dan #minigames)
3. materi/lanjutan/index.html (.material-grid)
4. css/pages/kelas-materi.css (gaya CSS untuk course-card, doc-big-card, material-card)
"""

import os
import re

def update_kelas_index():
    path = "kelas/index.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Section #dasar
    # Latihan Kana
    old_dasar_1 = '''                <a class="course-card practice-course-card" href="latihan.html">
                    <span class="course-kana">練習</span>
                    <div class="course-content">
                        <p class="card-number">Kelas Dasar · Latihan</p>
                        <h3>Latihan Kana</h3>
                        <p>Uji Hiragana dan Katakana dengan soal singkat yang acak.</p>
                        <span class="btn primary">MULAI LATIHAN</span>
                    </div>
                    <img class="card-corner-chibi" src="../images/mirai/icon/Hu.png" alt="" aria-hidden="true">
                </a>'''

    new_dasar_1 = '''                <div class="course-card practice-course-card" data-expand-card>
                    <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
                    <span class="course-kana">練習</span>
                    <div class="course-content">
                        <p class="card-number">Kelas Dasar · Latihan</p>
                        <span class="card-sub-jp">仮名練習</span>
                        <h3>Latihan Kana</h3>
                        <div class="card-collapsible-content">
                            <div class="card-collapsible-inner">
                                <p>Uji Hiragana dan Katakana dengan soal singkat yang acak.</p>
                            </div>
                        </div>
                        <a class="btn primary" href="latihan.html" data-expand-cta>MULAI LATIHAN →</a>
                    </div>
                    <img class="card-corner-chibi" src="../images/mirai/icon/Hu.png" alt="" aria-hidden="true">
                </div>'''

    # Kamus Hiragana
    old_dasar_2 = '''                <a class="course-card" href="../kamus/index.html?tab=hiragana">
                    <span class="course-kana">ひらがな</span>
                    <div class="course-content">
                        <p class="card-number">Kelas Dasar · Modul 1</p>
                        <h3>Kamus Hiragana</h3>
                        <p>Kenali huruf pertama dalam bahasa Jepang.</p>
                        <span class="btn primary">BUKA HIRAGANA</span>
                    </div>
                    <img class="card-corner-chibi" src="../images/mirai/icon/Ka.png" alt="" aria-hidden="true">
                </a>'''

    new_dasar_2 = '''                <div class="course-card" data-expand-card>
                    <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
                    <span class="course-kana">ひらがな</span>
                    <div class="course-content">
                        <p class="card-number">Kelas Dasar · Modul 1</p>
                        <span class="card-sub-jp">平仮名辞書</span>
                        <h3>Kamus Hiragana</h3>
                        <div class="card-collapsible-content">
                            <div class="card-collapsible-inner">
                                <p>Kenali huruf pertama dalam bahasa Jepang.</p>
                            </div>
                        </div>
                        <a class="btn primary" href="../kamus/index.html?tab=hiragana" data-expand-cta>BUKA HIRAGANA →</a>
                    </div>
                    <img class="card-corner-chibi" src="../images/mirai/icon/Ka.png" alt="" aria-hidden="true">
                </div>'''

    # Kamus Katakana
    old_dasar_3 = '''                <a class="course-card" href="../kamus/index.html?tab=katakana">
                    <span class="course-kana">カタカナ</span>
                    <div class="course-content">
                        <p class="card-number">Kelas Dasar · Modul 2</p>
                        <h3>Kamus Katakana</h3>
                        <p>Huruf untuk kata serapan dan istilah modern.</p>
                        <span class="btn primary">BUKA KATAKANA</span>
                    </div>
                    <img class="card-corner-chibi" src="../images/mirai/icon/Fa.png" alt="" aria-hidden="true">
                </a>'''

    new_dasar_3 = '''                <div class="course-card" data-expand-card>
                    <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
                    <span class="course-kana">カタカナ</span>
                    <div class="course-content">
                        <p class="card-number">Kelas Dasar · Modul 2</p>
                        <span class="card-sub-jp">片仮名辞書</span>
                        <h3>Kamus Katakana</h3>
                        <div class="card-collapsible-content">
                            <div class="card-collapsible-inner">
                                <p>Huruf untuk kata serapan dan istilah modern.</p>
                            </div>
                        </div>
                        <a class="btn primary" href="../kamus/index.html?tab=katakana" data-expand-cta>BUKA KATAKANA →</a>
                    </div>
                    <img class="card-corner-chibi" src="../images/mirai/icon/Fa.png" alt="" aria-hidden="true">
                </div>'''

    # Mirai no Buuku
    old_dasar_4 = '''                <a class="course-card buuku-course-card" href="../materi/dasar/index.html">
                    <span class="course-kana">本</span>
                    <div class="course-content">
                        <p class="card-number">Mirai no Buuku · Dasar</p>
                        <h3>Mirai no Buuku</h3>
                        <p>Kumpulan materi dasar untuk menemani langkah pertamamu belajar bahasa Jepang.</p>
                        <span class="btn primary">BUKA BUUKU</span>
                    </div>
                    <img class="card-corner-chibi" src="../images/mirai/icon/Fli.png" alt="" aria-hidden="true">
                </a>'''

    new_dasar_4 = '''                <div class="course-card buuku-course-card" data-expand-card>
                    <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
                    <span class="course-kana">本</span>
                    <div class="course-content">
                        <p class="card-number">Mirai no Buuku · Dasar</p>
                        <span class="card-sub-jp">未来の本・基礎</span>
                        <h3>Mirai no Buuku</h3>
                        <div class="card-collapsible-content">
                            <div class="card-collapsible-inner">
                                <p>Kumpulan materi dasar untuk menemani langkah pertamamu belajar bahasa Jepang.</p>
                            </div>
                        </div>
                        <a class="btn primary" href="../materi/dasar/index.html" data-expand-cta>BUKA BUUKU →</a>
                    </div>
                    <img class="card-corner-chibi" src="../images/mirai/icon/Fli.png" alt="" aria-hidden="true">
                </div>'''

    # Choukai
    old_dasar_5 = '''                <a class="course-card choukai-course-card" href="latihan.html?game=choukai">
                    <span class="course-kana">聴解</span>
                    <div class="course-content">
                        <p class="card-number">聴解 • CHOUKAI</p>
                        <h3>Tebak Suara Kilat</h3>
                        <p>Latih ketajaman pendengaran (Choukai) dengan menebak aksara &amp; kosakata Jepang dari audio pelafalan asli.</p>
                        <span class="btn primary">MAINKAN CHOUKAI →</span>
                    </div>
                    <img class="card-corner-chibi" src="../images/mirai/icon/Ki.png" alt="" aria-hidden="true">
                </a>'''

    new_dasar_5 = '''                <div class="course-card choukai-course-card" data-expand-card>
                    <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
                    <span class="course-kana">聴解</span>
                    <div class="course-content">
                        <p class="card-number">聴解 • CHOUKAI</p>
                        <span class="card-sub-jp">聴解クイズ</span>
                        <h3>Tebak Suara Kilat</h3>
                        <div class="card-collapsible-content">
                            <div class="card-collapsible-inner">
                                <p>Latih ketajaman pendengaran (Choukai) dengan menebak aksara &amp; kosakata Jepang dari audio pelafalan asli.</p>
                            </div>
                        </div>
                        <a class="btn primary" href="latihan.html?game=choukai" data-expand-cta>MAINKAN CHOUKAI →</a>
                    </div>
                    <img class="card-corner-chibi" src="../images/mirai/icon/Ki.png" alt="" aria-hidden="true">
                </div>'''

    # Memory
    old_dasar_6 = '''                <a class="course-card memory-course-card" href="latihan.html?game=memory">
                    <span class="course-kana">記憶</span>
                    <div class="course-content">
                        <p class="card-number">記憶 • MEMORY FLIP</p>
                        <h3>Pasangan Kartu Memori</h3>
                        <p>Latih daya ingat visual dengan mencocokkan 12 kartu tertutup berisi aksara Jepang dan cara bacanya.</p>
                        <span class="btn primary">MAINKAN MEMORY →</span>
                    </div>
                    <img class="card-corner-chibi" src="../images/mirai/icon/Lo.png" alt="" aria-hidden="true">
                </a>'''

    new_dasar_6 = '''                <div class="course-card memory-course-card" data-expand-card>
                    <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
                    <span class="course-kana">記憶</span>
                    <div class="course-content">
                        <p class="card-number">記憶 • MEMORY FLIP</p>
                        <span class="card-sub-jp">記憶フリップ</span>
                        <h3>Pasangan Kartu Memori</h3>
                        <div class="card-collapsible-content">
                            <div class="card-collapsible-inner">
                                <p>Latih daya ingat visual dengan mencocokkan 12 kartu tertutup berisi aksara Jepang dan cara bacanya.</p>
                            </div>
                        </div>
                        <a class="btn primary" href="latihan.html?game=memory" data-expand-cta>MAINKAN MEMORY →</a>
                    </div>
                    <img class="card-corner-chibi" src="../images/mirai/icon/Lo.png" alt="" aria-hidden="true">
                </div>'''

    # 2. Section #lanjutan
    # Kamus Kanji
    old_lanjutan_1 = '''                <a class="course-card" href="../kamus/index.html?tab=kanji">
                    <span class="course-kana">漢字</span>
                    <div class="course-content">
                        <p class="card-number">Kelas Lanjutan · Modul 1</p>
                        <h3>Kamus Kanji</h3>
                        <p>Memahami karakter, arti, bacaan, serta penggunaannya.</p>
                        <span class="btn primary">BUKA KANJI</span>
                    </div>
                    <img class="card-corner-chibi" src="../images/mirai/icon/Chi.png" alt="" aria-hidden="true">
                </a>'''

    new_lanjutan_1 = '''                <div class="course-card" data-expand-card>
                    <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
                    <span class="course-kana">漢字</span>
                    <div class="course-content">
                        <p class="card-number">Kelas Lanjutan · Modul 1</p>
                        <span class="card-sub-jp">漢字辞書</span>
                        <h3>Kamus Kanji</h3>
                        <div class="card-collapsible-content">
                            <div class="card-collapsible-inner">
                                <p>Memahami karakter, arti, bacaan, serta penggunaannya.</p>
                            </div>
                        </div>
                        <a class="btn primary" href="../kamus/index.html?tab=kanji" data-expand-cta>BUKA KANJI →</a>
                    </div>
                    <img class="card-corner-chibi" src="../images/mirai/icon/Chi.png" alt="" aria-hidden="true">
                </div>'''

    # Buuku Lanjutan
    old_lanjutan_2 = '''                <a class="course-card buuku-course-card" href="../materi/lanjutan/index.html">
                    <span class="course-kana">本</span>
                    <div class="course-content">
                        <p class="card-number">Mirai no Buuku · Lanjutan</p>
                        <h3>Mirai No Buuku</h3>
                        <p>Kumpulan materi lanjutan untuk memperdalam kemampuan bahasa Jepangmu.</p>
                        <span class="btn primary">BUKA BUUKU</span>
                    </div>
                    <img class="card-corner-chibi" src="../images/mirai/icon/Wa.png" alt="" aria-hidden="true">
                </a>'''

    new_lanjutan_2 = '''                <div class="course-card buuku-course-card" data-expand-card>
                    <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
                    <span class="course-kana">本</span>
                    <div class="course-content">
                        <p class="card-number">Mirai no Buuku · Lanjutan</p>
                        <span class="card-sub-jp">未来の本・上級</span>
                        <h3>Mirai No Buuku</h3>
                        <div class="card-collapsible-content">
                            <div class="card-collapsible-inner">
                                <p>Kumpulan materi lanjutan untuk memperdalam kemampuan bahasa Jepangmu.</p>
                            </div>
                        </div>
                        <a class="btn primary" href="../materi/lanjutan/index.html" data-expand-cta>BUKA BUUKU →</a>
                    </div>
                    <img class="card-corner-chibi" src="../images/mirai/icon/Wa.png" alt="" aria-hidden="true">
                </div>'''

    # 3. Section #kurikulum
    # Dokumen 1
    old_doc_1 = '''                <!-- Dokumen 1: Kurikulum Pembelajaran -->
                <article class="doc-big-card" id="kurikulum-doc">
                    <div class="doc-card-header">
                        <div class="doc-header-left">
                            <span class="doc-kana">教本</span>
                            <span class="doc-index-badge">
                                <span class="badge-dot" aria-hidden="true"></span>
                                <span>DOKUMEN 1</span>
                            </span>
                        </div>
                        <span class="doc-format-badge">
                            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                            <span>FORMAT PDF</span>
                        </span>
                    </div>
                    <div class="doc-card-body">
                        <div class="doc-hero-row">
                            <div class="doc-icon-box" aria-hidden="true">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
                            </div>
                            <div class="doc-headings">
                                <p class="card-number">Silabus Resmi Klub</p>
                                <h3 class="doc-title">Kurikulum Pembelajaran</h3>
                            </div>
                        </div>
                        <p class="doc-desc">Memuat panduan alur materi berjenjang mulai dari Hiragana, Katakana, Kanji, tata bahasa dasar hingga lanjutan, serta acuan capaian belajar anggota.</p>
                    </div>
                    <div class="doc-card-footer">
                        <a class="doc-btn-download btn-doc-download" href="kurikulum/kurikulum-pembelajaran.pdf" target="_blank" rel="noopener noreferrer" download>
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                            <span>Unduh PDF</span>
                        </a>
                        <a class="doc-btn-view btn-doc-view" href="kurikulum/kurikulum-pembelajaran.pdf" target="_blank" rel="noopener noreferrer">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                            <span class="doc-btn-label-full">Buka Dokumen</span>
                            <span class="doc-btn-label-short">Buka</span>
                        </a>
                    </div>
                    <img class="card-corner-chibi" src="../images/mirai/icon/Al.png" alt="" aria-hidden="true">
                </article>'''

    new_doc_1 = '''                <!-- Dokumen 1: Kurikulum Pembelajaran -->
                <article class="doc-big-card" id="kurikulum-doc" data-expand-card>
                    <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
                    <div class="doc-card-header">
                        <div class="doc-header-left">
                            <span class="doc-kana">教本</span>
                            <span class="doc-index-badge">
                                <span class="badge-dot" aria-hidden="true"></span>
                                <span>DOKUMEN 1</span>
                            </span>
                        </div>
                        <span class="doc-format-badge">
                            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                            <span>FORMAT PDF</span>
                        </span>
                    </div>
                    <div class="doc-card-body">
                        <div class="doc-hero-row">
                            <div class="doc-icon-box" aria-hidden="true">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
                            </div>
                            <div class="doc-headings">
                                <p class="card-number">Silabus Resmi Klub</p>
                                <span class="card-sub-jp">教育カリキュラム</span>
                                <h3 class="doc-title">Kurikulum Pembelajaran</h3>
                            </div>
                        </div>
                        <div class="card-collapsible-content">
                            <div class="card-collapsible-inner">
                                <p class="doc-desc">Memuat panduan alur materi berjenjang mulai dari Hiragana, Katakana, Kanji, tata bahasa dasar hingga lanjutan, serta acuan capaian belajar anggota.</p>
                            </div>
                        </div>
                    </div>
                    <div class="doc-card-footer">
                        <a class="doc-btn-download btn-doc-download" href="kurikulum/kurikulum-pembelajaran.pdf" target="_blank" rel="noopener noreferrer" download data-expand-cta>
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                            <span>Unduh PDF</span>
                        </a>
                        <a class="doc-btn-view btn-doc-view" href="kurikulum/kurikulum-pembelajaran.pdf" target="_blank" rel="noopener noreferrer" data-expand-cta>
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                            <span class="doc-btn-label-full">Buka Dokumen</span>
                            <span class="doc-btn-label-short">Buka</span>
                        </a>
                    </div>
                    <img class="card-corner-chibi" src="../images/mirai/icon/Al.png" alt="" aria-hidden="true">
                </article>'''

    # Dokumen 2
    old_doc_2 = '''                <!-- Dokumen 2: Tata Cara Mengajar -->
                <article class="doc-big-card" id="tatacara">
                    <div class="doc-card-header">
                        <div class="doc-header-left">
                            <span class="doc-kana">指導</span>
                            <span class="doc-index-badge">
                                <span class="badge-dot" aria-hidden="true"></span>
                                <span>DOKUMEN 2</span>
                            </span>
                        </div>
                        <span class="doc-format-badge">
                            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                            <span>FORMAT PDF</span>
                        </span>
                    </div>
                    <div class="doc-card-body">
                        <div class="doc-hero-row">
                            <div class="doc-icon-box" aria-hidden="true">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>
                            </div>
                            <div class="doc-headings">
                                <p class="card-number">Panduan Pengajaran Tutor</p>
                                <h3 class="doc-title">Tata Cara Mengajar</h3>
                            </div>
                        </div>
                        <p class="doc-desc">Pedoman teknis bagi tutor dan pengurus dalam menyampaikan materi bahasa Jepang secara interaktif, menyenangkan, terstruktur, serta panduan evaluasi belajar.</p>
                    </div>
                    <div class="doc-card-footer">
                        <a class="doc-btn-download btn-doc-download" href="kurikulum/tata-cara-mengajar.pdf" target="_blank" rel="noopener noreferrer" download>
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                            <span>Unduh PDF</span>
                        </a>
                        <a class="doc-btn-view btn-doc-view" href="kurikulum/tata-cara-mengajar.pdf" target="_blank" rel="noopener noreferrer">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                            <span class="doc-btn-label-full">Buka Dokumen</span>
                            <span class="doc-btn-label-short">Buka</span>
                        </a>
                    </div>
                    <img class="card-corner-chibi" src="../images/mirai/icon/Fu.png" alt="" aria-hidden="true">
                </article>'''

    new_doc_2 = '''                <!-- Dokumen 2: Tata Cara Mengajar -->
                <article class="doc-big-card" id="tatacara" data-expand-card>
                    <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
                    <div class="doc-card-header">
                        <div class="doc-header-left">
                            <span class="doc-kana">指導</span>
                            <span class="doc-index-badge">
                                <span class="badge-dot" aria-hidden="true"></span>
                                <span>DOKUMEN 2</span>
                            </span>
                        </div>
                        <span class="doc-format-badge">
                            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                            <span>FORMAT PDF</span>
                        </span>
                    </div>
                    <div class="doc-card-body">
                        <div class="doc-hero-row">
                            <div class="doc-icon-box" aria-hidden="true">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>
                            </div>
                            <div class="doc-headings">
                                <p class="card-number">Panduan Pengajaran Tutor</p>
                                <span class="card-sub-jp">指導方法</span>
                                <h3 class="doc-title">Tata Cara Mengajar</h3>
                            </div>
                        </div>
                        <div class="card-collapsible-content">
                            <div class="card-collapsible-inner">
                                <p class="doc-desc">Pedoman teknis bagi tutor dan pengurus dalam menyampaikan materi bahasa Jepang secara interaktif, menyenangkan, terstruktur, serta panduan evaluasi belajar.</p>
                            </div>
                        </div>
                    </div>
                    <div class="doc-card-footer">
                        <a class="doc-btn-download btn-doc-download" href="kurikulum/tata-cara-mengajar.pdf" target="_blank" rel="noopener noreferrer" download data-expand-cta>
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                            <span>Unduh PDF</span>
                        </a>
                        <a class="doc-btn-view btn-doc-view" href="kurikulum/tata-cara-mengajar.pdf" target="_blank" rel="noopener noreferrer" data-expand-cta>
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                            <span class="doc-btn-label-full">Buka Dokumen</span>
                            <span class="doc-btn-label-short">Buka</span>
                        </a>
                    </div>
                    <img class="card-corner-chibi" src="../images/mirai/icon/Fu.png" alt="" aria-hidden="true">
                </article>'''

    replacements = [
        (old_dasar_1, new_dasar_1),
        (old_dasar_2, new_dasar_2),
        (old_dasar_3, new_dasar_3),
        (old_dasar_4, new_dasar_4),
        (old_dasar_5, new_dasar_5),
        (old_dasar_6, new_dasar_6),
        (old_lanjutan_1, new_lanjutan_1),
        (old_lanjutan_2, new_lanjutan_2),
        (old_doc_1, new_doc_1),
        (old_doc_2, new_doc_2),
    ]

    for idx, (old, new) in enumerate(replacements):
        if old in content:
            content = content.replace(old, new)
            print(f"kelas/index.html: replaced block {idx+1}")
        else:
            print(f"kelas/index.html: FAILED to find block {idx+1}")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated kelas/index.html successfully.")

def update_materi_dasar():
    path = "materi/dasar/index.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Material cards
    old_grid = '''            <div class="material-grid">
                <a class="material-card" href="hiragana.html">
                    <span>01</span>
                    <h3>Huruf Hiragana</h3>
                    <p>Mengenal sistem aksara fonetik asli Jepang (46 huruf pokok, Dakuon &amp; Youon).</p>
                    <b>BUKA LANGKAH 1 →</b>
                </a>
                <a class="material-card" href="katakana.html">
                    <span>02</span>
                    <h3>Huruf Katakana</h3>
                    <p>Aksara untuk kata serapan, istilah asing modern, nama negara, dan onomatope.</p>
                    <b>BUKA LANGKAH 2 →</b>
                </a>
                <a class="material-card" href="kosakata.html">
                    <span>03</span>
                    <h3>Kosakata Dasar</h3>
                    <p>Koleksi kata benda esensial: angka, warna, hari, benda kelas, dan anggota keluarga.</p>
                    <b>BUKA LANGKAH 3 →</b>
                </a>
                <a class="material-card" href="jikoshokai.html">
                    <span>04</span>
                    <h3>Salam &amp; Jikoshokai</h3>
                    <p>Ungkapan salam harian (Aisatsu) dan tata cara perkenalan diri mandiri yang santun.</p>
                    <b>BUKA LANGKAH 4 →</b>
                </a>
                <a class="material-card" href="../lanjutan/index.html">
                    <span>05-07</span>
                    <h3>Materi Lanjutan (Buuku 2)</h3>
                    <p>Lanjutkan ke Tata Bahasa &amp; Partikel, Aksara Kanji N5, dan Membaca Kalimat.</p>
                    <b>LANJUTKAN →</b>
                </a>
                <a class="material-card" href="../../kelas/latihan.html">
                    <span>08</span>
                    <h3>Latihan &amp; Mini-Game</h3>
                    <p>Uji kemampuanmu lewat Tebak Suara Choukai, Pasangan Kartu Memory, dan Kuis Evaluasi.</p>
                    <b>UJI KEMAMPUAN →</b>
                </a>
            </div>'''

    new_grid = '''            <div class="material-grid">
                <div class="material-card" data-expand-card>
                    <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
                    <span>01</span>
                    <span class="card-sub-jp">平仮名</span>
                    <h3>Huruf Hiragana</h3>
                    <div class="card-collapsible-content">
                        <div class="card-collapsible-inner">
                            <p>Mengenal sistem aksara fonetik asli Jepang (46 huruf pokok, Dakuon &amp; Youon).</p>
                        </div>
                    </div>
                    <a class="material-btn" href="hiragana.html" data-expand-cta>BUKA LANGKAH 1 →</a>
                </div>
                <div class="material-card" data-expand-card>
                    <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
                    <span>02</span>
                    <span class="card-sub-jp">片仮名</span>
                    <h3>Huruf Katakana</h3>
                    <div class="card-collapsible-content">
                        <div class="card-collapsible-inner">
                            <p>Aksara untuk kata serapan, istilah asing modern, nama negara, dan onomatope.</p>
                        </div>
                    </div>
                    <a class="material-btn" href="katakana.html" data-expand-cta>BUKA LANGKAH 2 →</a>
                </div>
                <div class="material-card" data-expand-card>
                    <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
                    <span>03</span>
                    <span class="card-sub-jp">基本単語</span>
                    <h3>Kosakata Dasar</h3>
                    <div class="card-collapsible-content">
                        <div class="card-collapsible-inner">
                            <p>Koleksi kata benda esensial: angka, warna, hari, benda kelas, dan anggota keluarga.</p>
                        </div>
                    </div>
                    <a class="material-btn" href="kosakata.html" data-expand-cta>BUKA LANGKAH 3 →</a>
                </div>
                <div class="material-card" data-expand-card>
                    <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
                    <span>04</span>
                    <span class="card-sub-jp">挨拶と自己紹介</span>
                    <h3>Salam &amp; Jikoshokai</h3>
                    <div class="card-collapsible-content">
                        <div class="card-collapsible-inner">
                            <p>Ungkapan salam harian (Aisatsu) dan tata cara perkenalan diri mandiri yang santun.</p>
                        </div>
                    </div>
                    <a class="material-btn" href="jikoshokai.html" data-expand-cta>BUKA LANGKAH 4 →</a>
                </div>
                <div class="material-card" data-expand-card>
                    <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
                    <span>05-07</span>
                    <span class="card-sub-jp">上級教材</span>
                    <h3>Materi Lanjutan (Buuku 2)</h3>
                    <div class="card-collapsible-content">
                        <div class="card-collapsible-inner">
                            <p>Lanjutkan ke Tata Bahasa &amp; Partikel, Aksara Kanji N5, dan Membaca Kalimat.</p>
                        </div>
                    </div>
                    <a class="material-btn" href="../lanjutan/index.html" data-expand-cta>LANJUTKAN →</a>
                </div>
                <div class="material-card" data-expand-card>
                    <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
                    <span>08</span>
                    <span class="card-sub-jp">練習とゲーム</span>
                    <h3>Latihan &amp; Mini-Game</h3>
                    <div class="card-collapsible-content">
                        <div class="card-collapsible-inner">
                            <p>Uji kemampuanmu lewat Tebak Suara Choukai, Pasangan Kartu Memory, dan Kuis Evaluasi.</p>
                        </div>
                    </div>
                    <a class="material-btn" href="../../kelas/latihan.html" data-expand-cta>UJI KEMAMPUAN →</a>
                </div>
            </div>'''

    # Mini games course cards
    old_minigames = '''            <div class="course-cards course-cards--two">
                <a class="course-card choukai-course-card" href="../../kelas/latihan.html?game=choukai">
                    <span class="course-kana">聴解</span>
                    <div class="course-content">
                        <p class="card-number">聴解 • CHOUKAI</p>
                        <h3>Tebak Suara Kilat</h3>
                        <p>Latih ketajaman pendengaran (Choukai) dengan menebak aksara &amp; kosakata Jepang dari audio pelafalan asli.</p>
                        <span class="btn primary">MAINKAN CHOUKAI →</span>
                    </div>
                    <img class="card-corner-chibi" src="../../images/mirai/icon/Ki.png" alt="" aria-hidden="true">
                </a>
                <a class="course-card memory-course-card" href="../../kelas/latihan.html?game=memory">
                    <span class="course-kana">記憶</span>
                    <div class="course-content">
                        <p class="card-number">記憶 • MEMORY FLIP</p>
                        <h3>Pasangan Kartu Memori</h3>
                        <p>Latih daya ingat visual dengan mencocokkan 12 kartu tertutup berisi aksara Jepang dan cara bacanya.</p>
                        <span class="btn primary">MAINKAN MEMORY →</span>
                    </div>
                    <img class="card-corner-chibi" src="../../images/mirai/icon/Lo.png" alt="" aria-hidden="true">
                </a>
            </div>'''

    new_minigames = '''            <div class="course-cards course-cards--two">
                <div class="course-card choukai-course-card" data-expand-card>
                    <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
                    <span class="course-kana">聴解</span>
                    <div class="course-content">
                        <p class="card-number">聴解 • CHOUKAI</p>
                        <span class="card-sub-jp">聴解クイズ</span>
                        <h3>Tebak Suara Kilat</h3>
                        <div class="card-collapsible-content">
                            <div class="card-collapsible-inner">
                                <p>Latih ketajaman pendengaran (Choukai) dengan menebak aksara &amp; kosakata Jepang dari audio pelafalan asli.</p>
                            </div>
                        </div>
                        <a class="btn primary" href="../../kelas/latihan.html?game=choukai" data-expand-cta>MAINKAN CHOUKAI →</a>
                    </div>
                    <img class="card-corner-chibi" src="../../images/mirai/icon/Ki.png" alt="" aria-hidden="true">
                </div>
                <div class="course-card memory-course-card" data-expand-card>
                    <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
                    <span class="course-kana">記憶</span>
                    <div class="course-content">
                        <p class="card-number">記憶 • MEMORY FLIP</p>
                        <span class="card-sub-jp">記憶フリップ</span>
                        <h3>Pasangan Kartu Memori</h3>
                        <div class="card-collapsible-content">
                            <div class="card-collapsible-inner">
                                <p>Latih daya ingat visual dengan mencocokkan 12 kartu tertutup berisi aksara Jepang dan cara bacanya.</p>
                            </div>
                        </div>
                        <a class="btn primary" href="../../kelas/latihan.html?game=memory" data-expand-cta>MAINKAN MEMORY →</a>
                    </div>
                    <img class="card-corner-chibi" src="../../images/mirai/icon/Lo.png" alt="" aria-hidden="true">
                </div>
            </div>'''

    if old_grid in content:
        content = content.replace(old_grid, new_grid)
        print("materi/dasar/index.html: replaced material-grid")
    else:
        print("materi/dasar/index.html: FAILED to find material-grid")

    if old_minigames in content:
        content = content.replace(old_minigames, new_minigames)
        print("materi/dasar/index.html: replaced minigames")
    else:
        print("materi/dasar/index.html: FAILED to find minigames")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated materi/dasar/index.html successfully.")

def update_materi_lanjutan():
    path = "materi/lanjutan/index.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    old_grid = '''<div class="material-grid">
    <a class="material-card" href="grammar.html">
        <span>05</span>
        <h3>Tata Bahasa &amp; Partikel</h3>
        <p>Logika susunan kalimat SOV dan peta 7 partikel esensial (wa, o, ni, de, no, to, ka).</p>
        <b>BUKA LANGKAH 5 →</b>
    </a>
    <a class="material-card" href="kanji.html">
        <span>06</span>
        <h3>Aksara Kanji &amp; JLPT</h3>
        <p>Konsep logografis, aturan Onyomi vs Kunyomi, serta kanji pokok standar JLPT N5.</p>
        <b>BUKA LANGKAH 6 →</b>
    </a>
    <a class="material-card" href="kalimat.html">
        <span>07</span>
        <h3>Membaca Kalimat Sederhana</h3>
        <p>Latihan membaca paragraf utuh tanpa spasi dengan topik aktivitas harian &amp; kafe.</p>
        <b>BUKA LANGKAH 7 →</b>
    </a>
    <a class="material-card" href="../../kelas/latihan.html">
        <span>08</span>
        <h3>Latihan &amp; Evaluasi Akhir</h3>
        <p>Uji pemahaman komprehensif seluruh materi dasar dan lanjutan klub.</p>
        <b>MULAI EVALUASI →</b>
    </a>
    <a class="material-card" href="../dasar/index.html">
        <span>01-04</span>
        <h3>Kembali ke Buuku Dasar</h3>
        <p>Pelajari kembali Hiragana, Katakana, Kosakata Esensial, dan Jikoshokai.</p>
        <b>BUKA DASAR →</b>
    </a>
    <a class="material-card" href="../../kamus/index.html?tab=kanji">
        <span>2.136+</span>
        <h3>Kamus Kanji Interaktif</h3>
        <p>Eksplorasi ribuan karakter Joyo Kanji lengkap dengan animasi goresan stroke.</p>
        <b>BUKA KAMUS →</b>
    </a>
</div>'''

    new_grid = '''<div class="material-grid">
    <div class="material-card" data-expand-card>
        <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
        <span>05</span>
        <span class="card-sub-jp">文法と助詞</span>
        <h3>Tata Bahasa &amp; Partikel</h3>
        <div class="card-collapsible-content">
            <div class="card-collapsible-inner">
                <p>Logika susunan kalimat SOV dan peta 7 partikel esensial (wa, o, ni, de, no, to, ka).</p>
            </div>
        </div>
        <a class="material-btn" href="grammar.html" data-expand-cta>BUKA LANGKAH 5 →</a>
    </div>
    <div class="material-card" data-expand-card>
        <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
        <span>06</span>
        <span class="card-sub-jp">漢字とJLPT</span>
        <h3>Aksara Kanji &amp; JLPT</h3>
        <div class="card-collapsible-content">
            <div class="card-collapsible-inner">
                <p>Konsep logografis, aturan Onyomi vs Kunyomi, serta kanji pokok standar JLPT N5.</p>
            </div>
        </div>
        <a class="material-btn" href="kanji.html" data-expand-cta>BUKA LANGKAH 6 →</a>
    </div>
    <div class="material-card" data-expand-card>
        <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
        <span>07</span>
        <span class="card-sub-jp">短文読解</span>
        <h3>Membaca Kalimat Sederhana</h3>
        <div class="card-collapsible-content">
            <div class="card-collapsible-inner">
                <p>Latihan membaca paragraf utuh tanpa spasi dengan topik aktivitas harian &amp; kafe.</p>
            </div>
        </div>
        <a class="material-btn" href="kalimat.html" data-expand-cta>BUKA LANGKAH 7 →</a>
    </div>
    <div class="material-card" data-expand-card>
        <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
        <span>08</span>
        <span class="card-sub-jp">最終評価</span>
        <h3>Latihan &amp; Evaluasi Akhir</h3>
        <div class="card-collapsible-content">
            <div class="card-collapsible-inner">
                <p>Uji pemahaman komprehensif seluruh materi dasar dan lanjutan klub.</p>
            </div>
        </div>
        <a class="material-btn" href="../../kelas/latihan.html" data-expand-cta>MULAI EVALUASI →</a>
    </div>
    <div class="material-card" data-expand-card>
        <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
        <span>01-04</span>
        <span class="card-sub-jp">基礎に戻る</span>
        <h3>Kembali ke Buuku Dasar</h3>
        <div class="card-collapsible-content">
            <div class="card-collapsible-inner">
                <p>Pelajari kembali Hiragana, Katakana, Kosakata Esensial, dan Jikoshokai.</p>
            </div>
        </div>
        <a class="material-btn" href="../dasar/index.html" data-expand-cta>BUKA DASAR →</a>
    </div>
    <div class="material-card" data-expand-card>
        <button type="button" class="card-toggle" aria-expanded="false" aria-label="Buka tutup detail"></button>
        <span>2.136+</span>
        <span class="card-sub-jp">対話型漢字辞書</span>
        <h3>Kamus Kanji Interaktif</h3>
        <div class="card-collapsible-content">
            <div class="card-collapsible-inner">
                <p>Eksplorasi ribuan karakter Joyo Kanji lengkap dengan animasi goresan stroke.</p>
            </div>
        </div>
        <a class="material-btn" href="../../kamus/index.html?tab=kanji" data-expand-cta>BUKA KAMUS →</a>
    </div>
</div>'''

    if old_grid in content:
        content = content.replace(old_grid, new_grid)
        print("materi/lanjutan/index.html: replaced material-grid")
    else:
        print("materi/lanjutan/index.html: FAILED to find material-grid")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated materi/lanjutan/index.html successfully.")

def update_css():
    css_path = "css/pages/kelas-materi.css"
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()

    new_css_rules = """
/* ==========================================================================
   SISTEM TAP-TO-EXPAND PADA COURSE CARD, DOC BIG CARD, & MATERIAL CARD
   ========================================================================== */

/* 1. Grid alignment: items dimulai dari atas agar kartu tertutup tidak melar saat kartu lain terbuka */
.course-cards,
.course-cards--two,
.course-cards--three,
#dasar .course-cards,
#lanjutan .course-cards,
.doc-cards-grid,
.material-grid {
    align-items: start !important;
}

/* 2. COURSE CARD EXPANDABLE */
.course-card[data-expand-card] {
    cursor: pointer !important;
    user-select: none;
    min-height: 220px !important;
    position: relative !important;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease, min-height 0.3s ease !important;
}

.course-card[data-expand-card].is-expanded {
    min-height: 300px !important;
    border-color: var(--pink, #e91e63) !important;
    box-shadow: 0 16px 36px rgba(233, 30, 99, 0.2) !important;
}

#lanjutan .course-card[data-expand-card].is-expanded {
    border-color: #ff659b !important;
    box-shadow: 0 18px 40px rgba(233, 30, 99, 0.3), 0 4px 14px rgba(0, 0, 0, 0.6) !important;
}

.course-card .card-content {
    display: flex !important;
    flex-direction: column !important;
    flex-grow: 1 !important;
    position: relative !important;
    z-index: 2 !important;
    width: 100% !important;
}

.course-card .card-sub-jp {
    font-size: 11.5px !important;
    font-weight: 700 !important;
    letter-spacing: 0.8px !important;
    color: var(--pink, #e91e63) !important;
    font-family: var(--font-jp, "Noto Sans JP", sans-serif) !important;
    margin: 0 0 4px 0 !important;
    display: block !important;
    line-height: 1.3 !important;
}

#lanjutan .course-card .card-sub-jp {
    color: #ff659b !important;
}

/* Collapsible Content di Course Card */
.course-card .card-collapsible-content {
    display: grid !important;
    grid-template-rows: 0fr !important;
    opacity: 0 !important;
    margin: 0 !important;
    transition: grid-template-rows 0.35s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.28s ease, margin 0.35s ease !important;
    pointer-events: none !important;
    width: 100% !important;
}

.course-card.is-expanded .card-collapsible-content {
    grid-template-rows: 1fr !important;
    opacity: 1 !important;
    margin: 6px 0 18px 0 !important;
    pointer-events: auto !important;
}

.course-card .card-collapsible-inner {
    overflow: hidden !important;
    min-height: 0 !important;
}

.course-card .card-collapsible-inner p {
    margin: 0 !important;
    font-size: 13.5px !important;
    line-height: 1.6 !important;
    max-width: calc(100% - 65px) !important;
}

#dasar .course-card .card-collapsible-inner p {
    color: #554857 !important;
}

#lanjutan .course-card .card-collapsible-inner p {
    color: rgba(255, 255, 255, 0.76) !important;
}

/* Tombol Toggle Panah Chevron di Course Card */
.course-card .card-toggle {
    position: absolute !important;
    top: 18px !important;
    right: 18px !important;
    width: 32px !important;
    height: 32px !important;
    border-radius: 50% !important;
    background: rgba(233, 30, 99, 0.1) !important;
    border: 1px solid rgba(233, 30, 99, 0.25) !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), background 0.2s ease, border-color 0.2s ease !important;
    z-index: 10 !important;
    padding: 0 !important;
    color: var(--pink, #e91e63) !important;
}

#lanjutan .course-card .card-toggle {
    background: rgba(255, 101, 155, 0.15) !important;
    border-color: rgba(255, 101, 155, 0.35) !important;
    color: #ff659b !important;
}

.course-card .card-toggle::after {
    content: "" !important;
    display: block !important;
    width: 7px !important;
    height: 7px !important;
    border-right: 2px solid currentColor !important;
    border-bottom: 2px solid currentColor !important;
    transform: translateY(-2px) rotate(45deg) !important;
    transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

.course-card.is-expanded .card-toggle::after {
    transform: translateY(2px) rotate(-135deg) !important;
}

/* 3. DOC BIG CARD EXPANDABLE (KURIKULUM & TATA CARA) */
.doc-big-card[data-expand-card] {
    cursor: pointer !important;
    user-select: none;
    min-height: 220px !important;
    transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease, min-height 0.3s ease !important;
}

.page-kelas #kurikulum .doc-big-card[data-expand-card] {
    min-height: 220px !important;
}

.doc-big-card[data-expand-card].is-expanded,
.page-kelas #kurikulum .doc-big-card[data-expand-card].is-expanded {
    min-height: 300px !important;
    border-color: #ff659b !important;
    box-shadow: 0 16px 36px rgba(233, 30, 99, 0.2) !important;
}

.doc-big-card .card-sub-jp {
    font-size: 11.5px !important;
    font-weight: 700 !important;
    letter-spacing: 0.8px !important;
    color: var(--pink, #e91e63) !important;
    font-family: var(--font-jp, "Noto Sans JP", sans-serif) !important;
    margin: 0 0 4px 0 !important;
    display: block !important;
    line-height: 1.3 !important;
}

.doc-big-card .doc-card-header {
    padding-right: 54px !important;
}

.doc-big-card .card-toggle {
    position: absolute !important;
    top: 14px !important;
    right: 14px !important;
    width: 32px !important;
    height: 32px !important;
    border-radius: 50% !important;
    background: rgba(255, 101, 155, 0.14) !important;
    border: 1px solid rgba(255, 101, 155, 0.3) !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), background 0.2s ease !important;
    z-index: 10 !important;
    padding: 0 !important;
    color: var(--pink, #ff659b) !important;
}

.doc-big-card .card-toggle::after {
    content: "" !important;
    display: block !important;
    width: 7px !important;
    height: 7px !important;
    border-right: 2px solid currentColor !important;
    border-bottom: 2px solid currentColor !important;
    transform: translateY(-2px) rotate(45deg) !important;
    transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

.doc-big-card.is-expanded .card-toggle::after {
    transform: translateY(2px) rotate(-135deg) !important;
}

.doc-big-card .card-collapsible-content {
    display: grid !important;
    grid-template-rows: 0fr !important;
    opacity: 0 !important;
    margin: 0 !important;
    transition: grid-template-rows 0.35s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.28s ease, margin 0.35s ease !important;
    pointer-events: none !important;
    width: 100% !important;
}

.doc-big-card.is-expanded .card-collapsible-content {
    grid-template-rows: 1fr !important;
    opacity: 1 !important;
    margin: 10px 0 6px 0 !important;
    pointer-events: auto !important;
}

.doc-big-card .card-collapsible-inner {
    overflow: hidden !important;
    min-height: 0 !important;
}

.doc-big-card .card-collapsible-inner .doc-desc {
    margin: 0 !important;
}

/* 4. MATERIAL CARD EXPANDABLE (BUUKU DASAR & LANJUTAN) */
.material-card[data-expand-card] {
    cursor: pointer !important;
    user-select: none;
    position: relative !important;
    min-height: 180px !important;
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease, min-height 0.3s ease !important;
}

.material-card[data-expand-card].is-expanded {
    min-height: 250px !important;
    border-color: var(--pink, #e91e63) !important;
    box-shadow: 0 14px 28px rgba(233, 30, 99, 0.18) !important;
}

.material-card .card-toggle {
    position: absolute !important;
    top: 14px !important;
    right: 14px !important;
    width: 30px !important;
    height: 30px !important;
    border-radius: 50% !important;
    background: rgba(233, 30, 99, 0.08) !important;
    border: 1px solid rgba(233, 30, 99, 0.2) !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), background 0.2s ease !important;
    z-index: 10 !important;
    padding: 0 !important;
    color: var(--pink, #e91e63) !important;
}

.material-card .card-toggle::after {
    content: "" !important;
    display: block !important;
    width: 7px !important;
    height: 7px !important;
    border-right: 2px solid currentColor !important;
    border-bottom: 2px solid currentColor !important;
    transform: translateY(-2px) rotate(45deg) !important;
    transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

.material-card.is-expanded .card-toggle::after {
    transform: translateY(2px) rotate(-135deg) !important;
}

.material-card .card-sub-jp {
    font-size: 11px !important;
    font-weight: 700 !important;
    color: var(--pink, #e91e63) !important;
    font-family: var(--font-jp, "Noto Sans JP", sans-serif) !important;
    margin: 8px 0 2px 0 !important;
    display: block !important;
    line-height: 1.3 !important;
}

.material-card .card-collapsible-content {
    display: grid !important;
    grid-template-rows: 0fr !important;
    opacity: 0 !important;
    margin: 0 !important;
    transition: grid-template-rows 0.35s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.28s ease, margin 0.35s ease !important;
    pointer-events: none !important;
    width: 100% !important;
}

.material-card.is-expanded .card-collapsible-content {
    grid-template-rows: 1fr !important;
    opacity: 1 !important;
    margin: 6px 0 16px 0 !important;
    pointer-events: auto !important;
}

.material-card .card-collapsible-inner {
    overflow: hidden !important;
    min-height: 0 !important;
}

.material-card .card-collapsible-inner p {
    margin: 0 !important;
    color: var(--muted) !important;
    font-size: 14px !important;
    line-height: 1.65 !important;
}

.material-card .material-btn {
    margin-top: auto !important;
    display: inline-block !important;
    color: var(--pink, #e91e63) !important;
    font-size: 11px !important;
    font-weight: 800 !important;
    letter-spacing: 1.2px !important;
    text-decoration: none !important;
    transition: color 0.2s ease, transform 0.2s ease !important;
}

.material-card .material-btn:hover {
    color: #c2185b !important;
    transform: translateX(4px) !important;
}

/* 5. Mobile & Tablet Overrides */
@media (max-width: 768px) {
    .course-card[data-expand-card],
    .doc-big-card[data-expand-card],
    .page-kelas #kurikulum .doc-big-card[data-expand-card],
    .material-card[data-expand-card] {
        min-height: auto !important;
    }
}
"""

    if "SISTEM TAP-TO-EXPAND PADA COURSE CARD, DOC BIG CARD, & MATERIAL CARD" not in css:
        css += "\n" + new_css_rules
        with open(css_path, "w", encoding="utf-8") as f:
            f.write(css)
        print("Updated css/pages/kelas-materi.css successfully.")
    else:
        print("css/pages/kelas-materi.css already has the tap-to-expand rules.")

if __name__ == "__main__":
    update_kelas_index()
    update_materi_dasar()
    update_materi_lanjutan()
    update_css()
