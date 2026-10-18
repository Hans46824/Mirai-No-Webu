#!/usr/bin/env python3
"""
Skrip Pembangun 2 Fitur Interaktif Baru:
1. Generator Nama Jepang & Kartu Anggota (kamus/index.html, js/translator.js, css/pages/kamus.css)
2. Kuis Kepribadian: Tes Kecocokan Divisi (divisi/index.html, kegiatan/index.html, js/quiz-divisi.js, css/pages/kegiatan-divisi.css)
"""

import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def log(msg):
    print(f"[FEATURE] {msg}")

# ==============================================================================
# FITUR 1: GENERATOR NAMA JEPANG & KARTU ANGGOTA
# ==============================================================================
def update_kamus_html():
    log("=== [1.a] Menambahkan Tab Switcher & Generator Nama di kamus/index.html ===")
    kamus_html_path = os.path.join(BASE_DIR, "kamus", "index.html")
    with open(kamus_html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Cek apakah sudah ada tab switcher
    if "studio-tab-bar" in html:
        log("Tab Switcher sudah ada di kamus/index.html.")
        return

    # Temukan seksi translator-studio-section
    target_start = """    <div class="studio-container">
        <!-- HEADER ARAH BAHASA KHUSUS MOBILE"""
    
    replacement_start = """    <!-- 2-TAB SWITCHER STUDIO JEPANG (PENERJEMAH & GENERATOR NAMA) -->
    <div class="studio-tab-bar" role="tablist" aria-label="Pilihan Studio Bahasa Jepang">
        <button type="button" class="studio-tab-btn is-active" id="tabBtnTranslator" role="tab" aria-selected="true" data-tab="translator">
            <span class="tab-icon">🌐</span>
            <span class="tab-text">Penerjemah &amp; Keyboard Jepang</span>
        </button>
        <button type="button" class="studio-tab-btn" id="tabBtnNameGen" role="tab" aria-selected="false" data-tab="namegen">
            <span class="tab-icon">🎴</span>
            <span class="tab-text">Generator Nama Jepang &amp; Kartu Anggota</span>
        </button>
    </div>

    <!-- TAB PANEL 1: PENERJEMAH & VIRTUAL KEYBOARD -->
    <div class="studio-tab-panel is-active" id="panelTranslator" data-studio-panel="translator">
        <div class="studio-container">
            <!-- HEADER ARAH BAHASA KHUSUS MOBILE"""

    html = html.replace(target_start, replacement_start)

    # Temukan penutup translator studio dan tambahkan Tab Panel 2 (Generator Nama)
    panel_namegen_html = """        </div>
    </div>

    <!-- TAB PANEL 2: GENERATOR NAMA JEPANG & KARTU ANGGOTA (OSATSU MIRAI NO HANA) -->
    <div class="studio-tab-panel" id="panelNameGen" data-studio-panel="namegen" hidden>
        <div class="studio-container namegen-container">
            <div class="namegen-grid">
                <!-- KOLOM KIRI: FORMULIR INPUT IDENTITAS -->
                <div class="namegen-form-card studio-card">
                    <div class="studio-card-head">
                        <div class="card-head-left">
                            <span class="card-badge">
                                <span class="badge-flag">🎴</span>
                                <span class="badge-name">Identitas Siswa</span>
                            </span>
                            <span class="namegen-badge-tag">Katakana &amp; Ateji</span>
                        </div>
                    </div>

                    <div class="namegen-form-body">
                        <div class="namegen-field-group">
                            <label for="nameGenInput" class="namegen-label">
                                <span>Nama Panggilan / Lengkap <span class="req-star">*</span></span>
                                <small class="namegen-sublabel">Sistem otomatis mengonversi fonetik Indonesia ke Katakana Jepang</small>
                            </label>
                            <div class="namegen-input-wrap">
                                <input type="text" id="nameGenInput" class="namegen-input" placeholder="Ketik nama kamu, misal: Raditya, Riska, Aqmar..." maxlength="40" autocomplete="off" value="Raditya">
                                <button type="button" class="mini-clear-btn" id="clearNameInputBtn" title="Hapus teks nama" aria-label="Hapus nama">🗑️</button>
                            </div>
                        </div>

                        <div class="namegen-row-2col">
                            <div class="namegen-field-group">
                                <label for="nameGenClass" class="namegen-label">
                                    <span>Kelas / Angkatan <small>(Opsional)</small></span>
                                </label>
                                <input type="text" id="nameGenClass" class="namegen-input" placeholder="Misal: X-E2 / Angkatan 8" maxlength="25" value="X-E2 / Angkatan 8">
                            </div>

                            <div class="namegen-field-group">
                                <label for="nameGenDivision" class="namegen-label">
                                    <span>Divisi Pilihan</span>
                                </label>
                                <div class="namegen-select-wrap">
                                    <select id="nameGenDivision" class="namegen-select">
                                        <option value="bahasa" selected>📚 Divisi Bahasa &amp; Budaya</option>
                                        <option value="cosplay">🎭 Divisi Cosplay &amp; Seni Peran</option>
                                        <option value="desain">🎨 Divisi Desain &amp; Kreatif</option>
                                        <option value="kewirausahaan">🍱 Divisi Kewirausahaan</option>
                                        <option value="anggota">🌸 Anggota Baru Klub</option>
                                    </select>
                                </div>
                            </div>
                        </div>

                        <div class="namegen-actions-bar">
                            <button type="button" class="studio-btn primary namegen-submit-btn" id="generateNameCardBtn">
                                <span>✨ Buat Nama &amp; Kartu Anggota</span>
                            </button>
                        </div>

                        <!-- CHIP CONTOH NAMA CEPAT (1-KLIK) -->
                        <div class="namegen-chips-wrap">
                            <span class="chips-label">⚡ Contoh Nama Cepat:</span>
                            <div class="quick-chips-scroll" id="nameQuickChips">
                                <button type="button" class="quick-chip name-chip" data-name="Raditya">Raditya</button>
                                <button type="button" class="quick-chip name-chip" data-name="Aqmar">Aqmar</button>
                                <button type="button" class="quick-chip name-chip" data-name="Riska">Riska</button>
                                <button type="button" class="quick-chip name-chip" data-name="Salsa">Salsa</button>
                                <button type="button" class="quick-chip name-chip" data-name="Dimas">Dimas</button>
                                <button type="button" class="quick-chip name-chip" data-name="Putri">Putri</button>
                                <button type="button" class="quick-chip name-chip" data-name="Bayu">Bayu</button>
                                <button type="button" class="quick-chip name-chip" data-name="Fajar">Fajar</button>
                                <button type="button" class="quick-chip name-chip" data-name="Nabila">Nabila</button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- KOLOM KANAN: HASIL NAMA, FILOSOFI ATEJI & KARTU TANDA ANGGOTA -->
                <div class="namegen-result-card studio-card">
                    <!-- BANNER NAMA KATAKANA -->
                    <div class="namegen-phonetic-banner">
                        <div class="phonetic-left">
                            <span class="phonetic-label">NAMA RESMI JEPANG (KATAKANA)</span>
                            <div class="phonetic-display">
                                <span class="katakana-large" id="resKatakana">ラディティヤ</span>
                                <span class="romaji-sub" id="resRomaji">(Raditiya)</span>
                            </div>
                        </div>
                        <div class="phonetic-right">
                            <button type="button" class="icon-audio-btn primary" id="listenKatakanaBtn" title="Dengarkan pelafalan nama dalam Bahasa Jepang" aria-label="Dengarkan pelafalan nama">
                                🔊
                            </button>
                        </div>
                    </div>

                    <!-- KOTAK ATEJI KANJI POSITIF -->
                    <div class="namegen-ateji-box">
                        <div class="ateji-header">
                            <span class="ateji-icon">📜</span>
                            <div class="ateji-head-text">
                                <strong>Ateji Kanji Positif &amp; Filosofi Makna</strong>
                                <small>Karakter Kanji bermakna doa dan harapan baik untuk namamu</small>
                            </div>
                        </div>
                        <div class="ateji-kanji-row" id="resAtejiRow">
                            <div class="ateji-chip"><span class="ateji-kanji">羅</span><div class="ateji-chip-info"><strong class="ateji-reading">Ra</strong><span class="ateji-meaning">Jalinan Sutra &amp; Kekuatan Pelindung</span></div></div>
                            <div class="ateji-chip"><span class="ateji-kanji">大</span><div class="ateji-chip-info"><strong class="ateji-reading">Dai</strong><span class="ateji-meaning">Kebesaran Jiwa &amp; Kelapangan Hati</span></div></div>
                            <div class="ateji-chip"><span class="ateji-kanji">矢</span><div class="ateji-chip-info"><strong class="ateji-reading">Ya</strong><span class="ateji-meaning">Ketepatan Arah Mencapai Impian</span></div></div>
                        </div>
                        <p class="ateji-philosophy-text" id="resAtejiPhilosophy">
                            "Sosok berjiwa besar yang memiliki tekad kuat, melangkah mantap mencapai cita-cita dengan ketepatan anak panah."
                        </p>
                    </div>

                    <!-- LIVE PREVIEW KARTU TANDA ANGGOTA MIRAI NO HANA (OSATSU PASS) -->
                    <div class="member-card-stage">
                        <div class="member-card-wrap" id="memberCardVisual">
                            <div class="mcard-inner">
                                <div class="mcard-topbar">
                                    <div class="mcard-brand">
                                        <span class="mcard-flower-icon">🌸</span>
                                        <div class="mcard-brand-text">
                                            <span class="mcard-club-name">MIRAI NO HANA</span>
                                            <span class="mcard-sub-jp">未来之花 · 会員証</span>
                                        </div>
                                    </div>
                                    <div class="mcard-id-pill" id="mcardIdText">MNH-2026-8821</div>
                                </div>

                                <div class="mcard-body">
                                    <div class="mcard-name-col">
                                        <div class="mcard-jp-name" id="mcardKatakana">ラディティヤ</div>
                                        <div class="mcard-latin-name" id="mcardLatin">Raditya</div>
                                        <div class="mcard-meta-row">
                                            <span class="mcard-meta-pill" id="mcardDivisionPill">📚 Divisi Bahasa &amp; Budaya</span>
                                            <span class="mcard-meta-pill class-pill" id="mcardClassPill">X-E2 / Angkatan 8</span>
                                        </div>
                                    </div>
                                    <div class="mcard-ateji-col">
                                        <div class="mcard-kanji-stamp" id="mcardKanjiStamp">
                                            <span>羅</span>
                                            <span>大</span>
                                            <span>矢</span>
                                        </div>
                                        <div class="mcard-red-seal">未来<br>之印</div>
                                    </div>
                                </div>

                                <div class="mcard-footer">
                                    <span class="mcard-school">SMA Wachid Hasyim 2 Taman Sidoarjo</span>
                                    <div class="mcard-barcode">||| | |||| | |||||| || | ||| |||| |</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- TOMBOL UNDUH KARTU PNG -->
                    <div class="namegen-download-row">
                        <button type="button" class="studio-btn primary download-card-btn" id="downloadCardPngBtn">
                            <span class="btn-icon">📥</span>
                            <span>Unduh Kartu Anggota (.PNG)</span>
                        </button>
                        <span class="download-hint">Format PNG Resolusi Tinggi (Siap simpan ke galeri HP / Story Instagram)</span>
                    </div>
                </div>
            </div>
        </div>
    </div>"""

    # Ganti tag penutup </section> sebelum </main>
    html = re.sub(
        r"(\s*</div>\s*</div>\s*</section>\s*</main>)",
        panel_namegen_html + "\n</section>\n</main>",
        html
    )

    with open(kamus_html_path, "w", encoding="utf-8") as f:
        f.write(html)
    log("kamus/index.html berhasil diperbarui dengan Tab Switcher & Generator Nama.")

# ==============================================================================
# FITUR 1: LOGIKA JAVASCRIPT DI js/translator.js
# ==============================================================================
def update_translator_js():
    log("=== [1.b] Menambahkan Logika Fonetik Katakana, Ateji, & Canvas Card di js/translator.js ===")
    translator_js_path = os.path.join(BASE_DIR, "js", "translator.js")
    with open(translator_js_path, "r", encoding="utf-8") as f:
        code = f.read()

    if "initNameGenerator" in code:
        log("Logika initNameGenerator sudah ada di js/translator.js.")
        return

    name_gen_logic = """
// =========================================================================
// 7. GENERATOR NAMA JEPANG (KATAKANA), ATEJI KANJI POSITIF & KARTU ANGGOTA
// =========================================================================

// Kamus Konversi Fonetik Bahasa Indonesia -> Katakana Jepang
function indonesianToKatakana(name) {
  if (!name || typeof name !== 'string') return '';
  const s = name.trim().toLowerCase();
  if (!s) return '';

  const multiRules = [
    ['ngan', 'ンガン'], ['ngin', 'ンギン'], ['ngun', 'ングン'], ['ngen', 'ンゲン'], ['ngon', 'ンゴン'],
    ['nga', 'ンガ'], ['ngi', 'ンギ'], ['ngu', 'ング'], ['nge', 'ンゲ'], ['ngo', 'ンゴ'],
    ['nya', 'ニャ'], ['nyi', 'ニ'], ['nyu', 'ニュ'], ['nye', 'ニェ'], ['nyo', 'ニョ'],
    ['sya', 'シャ'], ['syi', 'シ'], ['syu', 'シュ'], ['sye', 'シェ'], ['syo', 'ショ'],
    ['sha', 'シャ'], ['shi', 'シ'], ['shu', 'シュ'], ['she', 'シェ'], ['sho', 'ショ'],
    ['cha', 'チャ'], ['chi', 'チ'], ['chu', 'チュ'], ['che', 'チェ'], ['cho', 'チョ'],
    ['kh', 'ク'], ['dh', 'ド'], ['th', 'ト'],
    ['tya', 'ティヤ'], ['tyo', 'ティヨ'], ['tyu', 'ティユ'],
    ['dya', 'ディヤ'], ['dyo', 'ディヨ'], ['dyu', 'ディユ'],
    ['dia', 'ディア'], ['dio', 'ディオ'], ['diu', 'ディウ'],
    ['tia', 'ティア'], ['tio', 'ティオ'], ['tiu', 'ティウ'],
    ['di', 'ディ'], ['ti', 'ティ'], ['du', 'ドゥ'], ['tu', 'トゥ'],
    ['fa', 'ファ'], ['fi', 'フィ'], ['fu', 'フ'], ['fe', 'フェ'], ['fo', 'フォ'],
    ['va', 'ヴァ'], ['vi', 'ヴィ'], ['vu', 'ヴ'], ['ve', 'ヴェ'], ['vo', 'ヴォ'],
    ['kwa', 'クヮ'], ['kwi', 'クィ'], ['kwe', 'クェ'], ['kwo', 'クォ'],
    ['gwa', 'グヮ'], ['gwi', 'グィ'], ['gwe', 'グェ'], ['gwo', 'グォ'],
    ['ca', 'カ'], ['ci', 'チ'], ['cu', 'チュ'], ['ce', 'チェ'], ['co', 'コ'],
    ['ja', 'ジャ'], ['ji', 'ジ'], ['ju', 'ジュ'], ['je', 'ジェ'], ['jo', 'ジョ'],
    ['za', 'ザ'], ['zi', 'ジ'], ['zu', 'ズ'], ['ze', 'ゼ'], ['zo', 'ゾ'],
    ['qa', 'クァ'], ['qi', 'クィ'], ['qu', 'ク'], ['qe', 'クェ'], ['qo', 'クォ'],
    ['ka', 'カ'], ['ki', 'キ'], ['ku', 'ク'], ['ke', 'ケ'], ['ko', 'コ'],
    ['sa', 'サ'], ['si', 'シ'], ['su', 'ス'], ['se', 'セ'], ['so', 'ソ'],
    ['ta', 'タ'], ['te', 'テ'], ['to', 'ト'],
    ['na', 'ナ'], ['ni', 'ニ'], ['nu', 'ヌ'], ['ne', 'ネ'], ['no', 'ノ'],
    ['ha', 'ハ'], ['hi', 'ヒ'], ['he', 'ヘ'], ['ho', 'ホ'],
    ['ma', 'マ'], ['mi', 'ミ'], ['mu', 'ム'], ['me', 'メ'], ['mo', 'モ'],
    ['ya', 'ヤ'], ['yu', 'ユ'], ['yo', 'ヨ'], ['ye', 'イェ'],
    ['ra', 'ラ'], ['ri', 'リ'], ['ru', 'ル'], ['re', 'レ'], ['ro', 'ロ'],
    ['la', 'ラ'], ['li', 'リ'], ['lu', 'ル'], ['le', 'レ'], ['lo', 'ロ'],
    ['wa', 'ワ'], ['wi', 'ウィ'], ['wu', 'ウ'], ['we', 'ウェ'], ['wo', 'ウォ'],
    ['ba', 'バ'], ['bi', 'ビ'], ['bu', 'ブ'], ['be', 'ベ'], ['bo', 'ボ'],
    ['pa', 'パ'], ['pi', 'ピ'], ['pu', 'プ'], ['pe', 'ペ'], ['po', 'ポ'],
    ['ga', 'ガ'], ['gi', 'ギ'], ['gu', 'グ'], ['ge', 'ゲ'], ['go', 'ゴ'],
    ['a', 'ア'], ['i', 'イ'], ['u', 'ウ'], ['e', 'エ'], ['o', 'オ']
  ];

  const loneConsonants = [
    ['ng', 'ング'], ['r', 'ル'], ['l', 'ル'], ['s', 'ス'], ['k', 'ク'],
    ['q', 'ク'], ['t', 'ト'], ['d', 'ド'], ['p', 'プ'], ['b', 'ブ'],
    ['g', 'グ'], ['m', 'ム'], ['n', 'ン'], ['h', 'フ'], ['c', 'ク'],
    ['j', 'ジ'], ['z', 'ズ'], ['f', 'フ'], ['v', 'ヴ'], ['w', 'ウ'], ['y', 'イ']
  ];

  let res = '';
  let i = 0;
  while (i < s.length) {
    if (s[i] === ' ' || s[i] === '-' || s[i] === '_') {
      res += '・';
      i++;
      continue;
    }
    let matched = false;
    for (const [k, v] of multiRules) {
      if (s.startsWith(k, i)) {
        res += v;
        i += k.length;
        matched = true;
        break;
      }
    }
    if (!matched) {
      for (const [k, v] of loneConsonants) {
        if (s.startsWith(k, i)) {
          res += v;
          i += k.length;
          matched = true;
          break;
        }
      }
    }
    if (!matched) {
      res += s[i].toUpperCase();
      i++;
    }
  }
  return res;
}

// Rekonstruksi Romaji dari Katakana
function katakanaToRomajiReading(katakana) {
  if (!katakana) return '';
  const map = {
    'ア': 'A', 'イ': 'I', 'ウ': 'U', 'エ': 'E', 'オ': 'O',
    'カ': 'Ka', 'キ': 'Ki', 'ク': 'Ku', 'ケ': 'Ke', 'コ': 'Ko',
    'サ': 'Sa', 'シ': 'Shi', 'ス': 'Su', 'セ': 'Se', 'ソ': 'So',
    'タ': 'Ta', 'チ': 'Chi', 'ツ': 'Tsu', 'テ': 'Te', 'ト': 'To',
    'ナ': 'Na', 'ニ': 'Ni', 'ヌ': 'Nu', 'ネ': 'Ne', 'ノ': 'No',
    'ハ': 'Ha', 'ヒ': 'Hi', 'フ': 'Fu', 'ヘ': 'He', 'ホ': 'Ho',
    'マ': 'Ma', 'ミ': 'Mi', 'ム': 'Mu', 'メ': 'Me', 'モ': 'Mo',
    'ヤ': 'Ya', 'ユ': 'Yu', 'ヨ': 'Yo',
    'ラ': 'Ra', 'リ': 'Ri', 'ル': 'Ru', 'レ': 'Re', 'ロ': 'Ro',
    'ワ': 'Wa', 'ヲ': 'Wo', 'ン': 'n',
    'ガ': 'Ga', 'ギ': 'Gi', 'グ': 'Gu', 'ゲ': 'Ge', 'ゴ': 'Go',
    'ザ': 'Za', 'ジ': 'Ji', 'ズ': 'Zu', 'ゼ': 'Ze', 'ゾ': 'Zo',
    'ダ': 'Da', 'ヂ': 'Ji', 'ヅ': 'Zu', 'デ': 'De', 'ド': 'Do',
    'バ': 'Ba', 'ビ': 'Bi', 'ブ': 'Bu', 'ベ': 'Be', 'ボ': 'Bo',
    'パ': 'Pa', 'ピ': 'Pi', 'プ': 'Pu', 'ペ': 'Pe', 'ポ': 'Po',
    'ディ': 'Di', 'ティ': 'Ti', 'ドゥ': 'Du', 'トゥ': 'Tu',
    'ファ': 'Fa', 'フィ': 'Fi', 'フェ': 'Fe', 'フォ': 'Fo',
    'ヴァ': 'Va', 'ヴィ': 'Vi', 'ヴェ': 'Ve', 'ヴォ': 'Vo',
    'キャ': 'Kya', 'キュ': 'Kyu', 'キョ': 'Kyo',
    'シャ': 'Sha', 'シュ': 'Shu', 'ショ': 'Sho',
    'チャ': 'Cha', 'チュ': 'Chu', 'チョ': 'Cho',
    'ニャ': 'Nya', 'ニュ': 'Nyu', 'ニョ': 'Nyo',
    'ヒャ': 'Hya', 'ヒュ': 'Hyu', 'ヒョ': 'Hyo',
    'ミャ': 'Mya', 'ミュ': 'Myu', 'ミョ': 'Myo',
    'リャ': 'Rya', 'リュ': 'Ryu', 'リョ': 'Ryo',
    'ギャ': 'Gya', 'ギュ': 'Gyu', 'ギョ': 'Gyo',
    'ジャ': 'Ja', 'ジュ': 'Ju', 'ジョ': 'Jo',
    'ビャ': 'Bya', 'ビュ': 'Byu', 'ビョ': 'Byo',
    'ピャ': 'Pya', 'ピュ': 'Pyu', 'ピョ': 'Pyo',
    'クァ': 'Qwa', 'クィ': 'Qwi', 'クェ': 'Qwe', 'クォ': 'Qwo',
    '・': ' '
  };

  let out = '';
  let i = 0;
  while (i < katakana.length) {
    if (i + 1 < katakana.length && map[katakana.substring(i, i + 2)]) {
      out += map[katakana.substring(i, i + 2)];
      i += 2;
    } else if (map[katakana[i]]) {
      out += map[katakana[i]];
      i++;
    } else {
      out += katakana[i];
      i++;
    }
  }
  return out;
}

// Basis Data Ateji Kanji Positif Berdasarkan Suku Kata
const ATEJI_DICT = {
  'a': { kanji: '明', reading: 'Aki', meaning: 'Cahaya Terang & Kecerdasan Budi' },
  'i': { kanji: '愛', reading: 'Ai', meaning: 'Kasih Sayang Murni & Ketulusan' },
  'u': { kanji: '宇', reading: 'U', meaning: 'Keluasan Semesta & Harapan Tinggi' },
  'e': { kanji: '栄', reading: 'Ei', meaning: 'Kejayaan & Kemakmuran Prestasi' },
  'o': { kanji: '央', reading: 'Ou', meaning: 'Pusat Semangat & Pemimpin Teladan' },
  'ka': { kanji: '華', reading: 'Ka', meaning: 'Bunga Merekah & Kemegahan Diri' },
  'ki': { kanji: '輝', reading: 'Kagayaki', meaning: 'Kilau Cahaya Gemilang Bintang' },
  'ku': { kanji: '空', reading: 'Sora', meaning: 'Langit Luas Tanpa Batas Impian' },
  'ke': { kanji: '結', reading: 'Yui', meaning: 'Tali Ikatan Persahabatan Abadi' },
  'ko': { kanji: '心', reading: 'Kokoro', meaning: 'Keteguhan Hati & Keikhlasan Jiwa' },
  'sa': { kanji: '咲', reading: 'Saki', meaning: 'Mekar Indah Mengharumkan Sekitar' },
  'si': { kanji: '真', reading: 'Shin', meaning: 'Kebenaran Murni & Integritas' },
  'su': { kanji: '寿', reading: 'Kotobuki', meaning: 'Keberkahan & Umur Panjang Mulia' },
  'se': { kanji: '星', reading: 'Hoshi', meaning: 'Bintang Pemandu Arah Langkah' },
  'so': { kanji: '創', reading: 'Sou', meaning: 'Daya Cipta & Kreativitas Luhur' },
  'ta': { kanji: '多', reading: 'Ta', meaning: 'Kelimpahan Bakat & Keberuntungan' },
  'ti': { kanji: '智', reading: 'Chi', meaning: 'Kebijaksanaan & Cendekia' },
  'tu': { kanji: '月', reading: 'Tsuki', meaning: 'Keindahan Rembulan Penerang Malam' },
  'te': { kanji: '悌', reading: 'Tei', meaning: 'Keramahan & Cinta Persaudaraan' },
  'to': { kanji: '翔', reading: 'Kakeru', meaning: 'Terbang Tinggi Menggapai Angkasa' },
  'na': { kanji: '直', reading: 'Nao', meaning: 'Kelurusan Moral & Kejujuran' },
  'ni': { kanji: '虹', reading: 'Niji', meaning: 'Pelangi Keindahan Penuh Warna' },
  'nu': { kanji: '主', reading: 'Nushi', meaning: 'Kemampuan Mandiri & Berprinsip' },
  'ne': { kanji: '音', reading: 'Ne', meaning: 'Irama Kebaikan & Harmoni Nada' },
  'no': { kanji: '希', reading: 'Nozomi', meaning: 'Harapan Luhur Masa Depan' },
  'ha': { kanji: '花', reading: 'Hana', meaning: 'Keharuman Bunga Mirai no Hana' },
  'hi': { kanji: '陽', reading: 'You', meaning: 'Hangatnya Sinar Mentari Pagi' },
  'fu': { kanji: '富', reading: 'Fu', meaning: 'Kelimpahan Kebaikan & Berkah' },
  'he': { kanji: '平', reading: 'Hei', meaning: 'Kedamaian Batin & Ketenangan' },
  'ho': { kanji: '宝', reading: 'Takara', meaning: 'Permata Berharga Kebanggaan' },
  'ma': { kanji: '誠', reading: 'Makoto', meaning: 'Ketulusan Hati & Kesetiaan' },
  'mi': { kanji: '美', reading: 'Bi', meaning: 'Keindahan Jiwa & Budi Pekerti' },
  'mu': { kanji: '夢', reading: 'Yume', meaning: 'Impian Mulia Yang Terwujud' },
  'me': { kanji: '萌', reading: 'Moe', meaning: 'Tunas Harapan Yang Bertumbuh' },
  'mo': { kanji: '望', reading: 'Bou', meaning: 'Aspirasi Luhur Menuju Puncak' },
  'ya': { kanji: '矢', reading: 'Ya', meaning: 'Ketepatan Arah Mencapai Sasaran' },
  'yu': { kanji: '優', reading: 'Yuu', meaning: 'Kelembutan Hati & Keunggulan Prestasi' },
  'yo': { kanji: '祥', reading: 'Shou', meaning: 'Pertanda Baik & Kebahagiaan' },
  'ra': { kanji: '羅', reading: 'Ra', meaning: 'Jalinan Sutra & Kekuatan Pelindung' },
  'ri': { kanji: '理', reading: 'Ri', meaning: 'Kebenaran, Logika, & Kemuliaan' },
  'ru': { kanji: '瑠', reading: 'Ru', meaning: 'Permata Biru Lapis Lazuli Gemilang' },
  're': { kanji: '蓮', reading: 'Ren', meaning: 'Teratai Anggun Yang Tetap Suci' },
  'ro': { kanji: '朗', reading: 'Rou', meaning: 'Keriangan Jiwa & Kecerahan Hati' },
  'wa': { kanji: '和', reading: 'Wa', meaning: 'Keharmonisan & Kedamaian Luhur' },
  'di': { kanji: '大', reading: 'Dai', meaning: 'Kebesaran Jiwa & Kelapangan Tekad' },
  'ba': { kanji: '羽', reading: 'Ba', meaning: 'Sayap Melambung Mengarungi Dunia' },
  'bi': { kanji: '美', reading: 'Bi', meaning: 'Keindahan Budi & Keanggunan' },
  'bu': { kanji: '武', reading: 'Bu', meaning: 'Ksatria Berani & Berpendirian' },
  'fa': { kanji: '花', reading: 'Hana', meaning: 'Mekar Indah Mengharumkan Nama' },
  'ja': { kanji: '慈', reading: 'Ji', meaning: 'Kasih Sayang & Kepedulian' },
  'ji': { kanji: '志', reading: 'Kokorozashi', meaning: 'Cita-Cita Luhur Yang Mantap' },
  'pu': { kanji: '富', reading: 'Fu', meaning: 'Kekayaan Ilmu & Kebajikan' }
};

const ATEJI_POOL = [
  { kanji: '翔', reading: 'To', meaning: 'Terbang Tinggi Menggapai Angkasa' },
  { kanji: '優', reading: 'Yuu', meaning: 'Kelembutan Hati & Keunggulan Prestasi' },
  { kanji: '明', reading: 'Mei', meaning: 'Cahaya Terang & Kecerdasan Budi' },
  { kanji: '花', reading: 'Ka', meaning: 'Keharuman Bunga Mirai no Hana' },
  { kanji: '誠', reading: 'Sei', meaning: 'Ketulusan Hati & Integritas Mulia' },
  { kanji: '輝', reading: 'Ki', meaning: 'Kilau Cahaya Gemilang Bintang' },
  { kanji: '星', reading: 'Sei', meaning: 'Bintang Pemandu Arah Langkah' },
  { kanji: '希', reading: 'Ki', meaning: 'Harapan Luhur Masa Depan' },
  { kanji: '陽', reading: 'You', meaning: 'Hangatnya Sinar Mentari Pagi' },
  { kanji: '蓮', reading: 'Ren', meaning: 'Teratai Anggun Yang Kuat Menghadapi Ujian' }
];

function generateAtejiList(name) {
  const clean = name.trim().toLowerCase().replace(/[^a-z]/g, '');
  if (!clean) {
    return [ATEJI_POOL[0], ATEJI_POOL[2], ATEJI_POOL[3]];
  }

  const selected = [];
  const usedKanji = new Set();

  // Cari pasangan 2-huruf atau 1-huruf
  let i = 0;
  while (i < clean.length && selected.length < 3) {
    let key2 = clean.substring(i, i + 2);
    let key1 = clean.substring(i, i + 1);

    if (ATEJI_DICT[key2] && !usedKanji.has(ATEJI_DICT[key2].kanji)) {
      selected.push(ATEJI_DICT[key2]);
      usedKanji.add(ATEJI_DICT[key2].kanji);
      i += 2;
    } else if (ATEJI_DICT[key1] && !usedKanji.has(ATEJI_DICT[key1].kanji)) {
      selected.push(ATEJI_DICT[key1]);
      usedKanji.add(ATEJI_DICT[key1].kanji);
      i += 1;
    } else {
      i++;
    }
  }

  // Lengkapi jika kurang dari 2 atau 3
  let poolIdx = 0;
  while (selected.length < 3 && poolIdx < ATEJI_POOL.length) {
    const item = ATEJI_POOL[poolIdx];
    if (!usedKanji.has(item.kanji)) {
      selected.push(item);
      usedKanji.add(item.kanji);
    }
    poolIdx++;
  }

  return selected.slice(0, 3);
}

function synthesizePhilosophy(atejiList, rawName) {
  if (!atejiList || !atejiList.length) {
    return 'Sosok berjiwa luhur yang senantiasa membawa harapan, kebaikan, dan prestasi gemilang bagi keluarga dan klub Mirai no Hana.';
  }
  const meanings = atejiList.map(a => a.meaning.split('&')[0].trim());
  return `Pribadi berjiwa luhur yang memadukan ${meanings[0].toLowerCase()}, ${meanings[1] ? meanings[1].toLowerCase() : 'keteguhan hati'}, dan ${meanings[2] ? meanings[2].toLowerCase() : 'kemuliaan'}, melangkah mantap mencapai cita-cita dengan penuh keyakinan.`;
}

// Inisialisasi Fitur Generator Nama & Kartu Anggota
function initNameGenerator() {
  const tabBtnTranslator = document.getElementById('tabBtnTranslator');
  const tabBtnNameGen = document.getElementById('tabBtnNameGen');
  const panelTranslator = document.getElementById('panelTranslator');
  const panelNameGen = document.getElementById('panelNameGen');

  if (!tabBtnTranslator || !tabBtnNameGen || !panelTranslator || !panelNameGen) return;

  // 1. Tab Switcher Listener
  tabBtnTranslator.addEventListener('click', () => {
    tabBtnTranslator.classList.add('is-active');
    tabBtnTranslator.setAttribute('aria-selected', 'true');
    tabBtnNameGen.classList.remove('is-active');
    tabBtnNameGen.setAttribute('aria-selected', 'false');
    panelTranslator.hidden = false;
    panelTranslator.classList.add('is-active');
    panelNameGen.hidden = true;
    panelNameGen.classList.remove('is-active');
    window.MiraiSound?.playClickIfIdle();
  });

  tabBtnNameGen.addEventListener('click', () => {
    tabBtnNameGen.classList.add('is-active');
    tabBtnNameGen.setAttribute('aria-selected', 'true');
    tabBtnTranslator.classList.remove('is-active');
    tabBtnTranslator.setAttribute('aria-selected', 'false');
    panelNameGen.hidden = false;
    panelNameGen.classList.add('is-active');
    panelTranslator.hidden = true;
    panelTranslator.classList.remove('is-active');
    window.MiraiSound?.playClickIfIdle();
    triggerGeneration();
  });

  // 2. Elements Form & Result
  const nameInput = document.getElementById('nameGenInput');
  const classInput = document.getElementById('nameGenClass');
  const divisionSelect = document.getElementById('nameGenDivision');
  const generateBtn = document.getElementById('generateNameCardBtn');
  const clearNameBtn = document.getElementById('clearNameInputBtn');

  const resKatakana = document.getElementById('resKatakana');
  const resRomaji = document.getElementById('resRomaji');
  const resAtejiRow = document.getElementById('resAtejiRow');
  const resAtejiPhilosophy = document.getElementById('resAtejiPhilosophy');
  const listenKatakanaBtn = document.getElementById('listenKatakanaBtn');

  const mcardKatakana = document.getElementById('mcardKatakana');
  const mcardLatin = document.getElementById('mcardLatin');
  const mcardDivisionPill = document.getElementById('mcardDivisionPill');
  const mcardClassPill = document.getElementById('mcardClassPill');
  const mcardKanjiStamp = document.getElementById('mcardKanjiStamp');
  const mcardIdText = document.getElementById('mcardIdText');
  const downloadCardBtn = document.getElementById('downloadCardPngBtn');

  const divisionLabels = {
    'bahasa': '📚 Divisi Bahasa & Budaya',
    'cosplay': '🎭 Divisi Cosplay & Seni Peran',
    'desain': '🎨 Divisi Desain & Kreatif',
    'kewirausahaan': '🍱 Divisi Kewirausahaan',
    'anggota': '🌸 Anggota Baru Klub'
  };

  function getDeterministicId(name) {
    let hash = 0;
    for (let i = 0; i < name.length; i++) {
      hash = (hash << 5) - hash + name.charCodeAt(i);
      hash |= 0;
    }
    const num = Math.abs(hash % 9000) + 1000;
    return `MNH-2026-${num}`;
  }

  function triggerGeneration() {
    const rawName = (nameInput.value || '').trim() || 'Raditya';
    const rawClass = (classInput.value || '').trim() || 'X-E2 / Angkatan 8';
    const divKey = divisionSelect.value || 'bahasa';
    const divLabel = divisionLabels[divKey] || divisionLabels['bahasa'];

    // Hitung Katakana & Romaji
    const katakana = indonesianToKatakana(rawName);
    const romaji = katakanaToRomajiReading(katakana);
    const atejiList = generateAtejiList(rawName);
    const philosophy = synthesizePhilosophy(atejiList, rawName);
    const memberId = getDeterministicId(rawName);

    // Update Result UI
    if (resKatakana) resKatakana.textContent = katakana;
    if (resRomaji) resRomaji.textContent = `(${romaji})`;
    if (resAtejiPhilosophy) resAtejiPhilosophy.textContent = `"${philosophy}"`;

    if (resAtejiRow) {
      resAtejiRow.innerHTML = atejiList.map(a => `
        <div class="ateji-chip">
          <span class="ateji-kanji">${a.kanji}</span>
          <div class="ateji-chip-info">
            <strong class="ateji-reading">${a.reading}</strong>
            <span class="ateji-meaning">${a.meaning}</span>
          </div>
        </div>
      `).join('');
    }

    // Update Member Card DOM Preview
    if (mcardKatakana) mcardKatakana.textContent = katakana;
    if (mcardLatin) mcardLatin.textContent = rawName;
    if (mcardDivisionPill) mcardDivisionPill.textContent = divLabel;
    if (mcardClassPill) mcardClassPill.textContent = rawClass;
    if (mcardIdText) mcardIdText.textContent = memberId;
    if (mcardKanjiStamp) {
      mcardKanjiStamp.innerHTML = atejiList.map(a => `<span>${a.kanji}</span>`).join('');
    }
  }

  // Listeners
  if (generateBtn) {
    generateBtn.addEventListener('click', () => {
      window.MiraiSound?.playClickIfIdle();
      triggerGeneration();
    });
  }

  if (clearNameBtn && nameInput) {
    clearNameBtn.addEventListener('click', () => {
      nameInput.value = '';
      nameInput.focus();
      triggerGeneration();
    });
  }

  if (nameInput) {
    nameInput.addEventListener('input', triggerGeneration);
  }
  if (classInput) {
    classInput.addEventListener('input', triggerGeneration);
  }
  if (divisionSelect) {
    divisionSelect.addEventListener('change', triggerGeneration);
  }

  // Quick Chips
  const nameQuickChips = document.getElementById('nameQuickChips');
  if (nameQuickChips) {
    nameQuickChips.addEventListener('click', (e) => {
      const btn = e.target.closest('.name-chip');
      if (!btn) return;
      const chipName = btn.dataset.name;
      if (chipName && nameInput) {
        nameInput.value = chipName;
        window.MiraiSound?.playClickIfIdle();
        triggerGeneration();
      }
    });
  }

  // Audio Katakana Voice Button
  if (listenKatakanaBtn) {
    listenKatakanaBtn.addEventListener('click', () => {
      const textToSpeak = resKatakana?.textContent || 'ラディティヤ';
      if (window.speakText) {
        window.speakText(textToSpeak, 'ja-JP');
      } else if ('speechSynthesis' in window) {
        const u = new SpeechSynthesisUtterance(textToSpeak);
        u.lang = 'ja-JP';
        window.speechSynthesis.speak(u);
      }
    });
  }

  // 3. HTML5 Canvas High-Definition PNG Generator
  if (downloadCardBtn) {
    downloadCardBtn.addEventListener('click', () => {
      window.MiraiSound?.playClickIfIdle();
      const rawName = (nameInput.value || '').trim() || 'Raditya';
      const rawClass = (classInput.value || '').trim() || 'Anggota Klub';
      const divKey = divisionSelect.value || 'bahasa';
      const divLabel = divisionLabels[divKey] || divisionLabels['bahasa'];
      const katakana = resKatakana?.textContent || indonesianToKatakana(rawName);
      const atejiList = generateAtejiList(rawName);
      const memberId = mcardIdText?.textContent || getDeterministicId(rawName);

      // Render Canvas
      const canvas = document.createElement('canvas');
      canvas.width = 960;
      canvas.height = 560;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      // a. Background Gradient Obsidian
      const bgGrad = ctx.createLinearGradient(0, 0, 960, 560);
      bgGrad.addColorStop(0, '#191224');
      bgGrad.addColorStop(0.5, '#120d1a');
      bgGrad.addColorStop(1, '#09070d');
      ctx.fillStyle = bgGrad;
      
      // Rounded card shape
      function roundRect(ctx, x, y, w, h, r) {
        ctx.beginPath();
        ctx.moveTo(x + r, y);
        ctx.arcTo(x + w, y, x + w, y + h, r);
        ctx.arcTo(x + w, y + h, x, y + h, r);
        ctx.arcTo(x, y + h, x, y, r);
        ctx.arcTo(x, y, x + w, y, r);
        ctx.closePath();
      }

      roundRect(ctx, 0, 0, 960, 560, 32);
      ctx.fill();

      // b. Decorative Outer Border (Pink Gold)
      ctx.lineWidth = 3;
      ctx.strokeStyle = 'rgba(255, 101, 155, 0.45)';
      roundRect(ctx, 2, 2, 956, 556, 30);
      ctx.stroke();

      // c. Inner Dashed Border
      ctx.setLineDash([8, 8]);
      ctx.lineWidth = 1.5;
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.14)';
      roundRect(ctx, 16, 16, 928, 528, 20);
      ctx.stroke();
      ctx.setLineDash([]); // reset

      // d. Watermark Crest & Sakura Circle on Right
      ctx.save();
      ctx.beginPath();
      ctx.arc(810, 280, 160, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(255, 101, 155, 0.08)';
      ctx.lineWidth = 40;
      ctx.stroke();
      ctx.restore();

      // e. Header Bar
      ctx.fillStyle = '#ff659b';
      ctx.font = 'bold 30px "Plus Jakarta Sans", Arial, sans-serif';
      ctx.fillText('🌸 MIRAI NO HANA', 42, 68);

      ctx.fillStyle = 'rgba(255, 215, 230, 0.82)';
      ctx.font = '600 16px "Noto Serif JP", serif';
      ctx.fillText('未来之花 · 会員証 (KARTU ANGGOTA RESMI)', 44, 94);

      // ID Tag Pill
      ctx.fillStyle = 'rgba(255, 101, 155, 0.18)';
      roundRect(ctx, 720, 42, 195, 42, 21);
      ctx.fill();
      ctx.strokeStyle = 'rgba(255, 101, 155, 0.45)';
      ctx.lineWidth = 1.5;
      roundRect(ctx, 720, 42, 195, 42, 21);
      ctx.stroke();

      ctx.fillStyle = '#ff8ab6';
      ctx.font = 'bold 16px "Plus Jakarta Sans", monospace';
      ctx.textAlign = 'center';
      ctx.fillText(memberId, 817, 69);
      ctx.textAlign = 'left';

      // f. Nama Katakana Besar & Glow
      ctx.shadowColor = 'rgba(255, 101, 155, 0.45)';
      ctx.shadowBlur = 14;
      ctx.fillStyle = '#ffffff';
      ctx.font = '900 62px "Noto Sans JP", Arial, sans-serif';
      ctx.fillText(katakana, 42, 215);
      ctx.shadowBlur = 0; // reset

      // Nama Latin
      ctx.fillStyle = '#ffd1e3';
      ctx.font = '700 28px "Plus Jakarta Sans", sans-serif';
      ctx.fillText(rawName, 44, 260);

      // g. Division & Class Pills
      ctx.fillStyle = 'rgba(255, 255, 255, 0.07)';
      roundRect(ctx, 44, 300, 310, 40, 20);
      ctx.fill();
      ctx.fillStyle = '#f1f5f9';
      ctx.font = '600 15px "Plus Jakarta Sans", sans-serif';
      ctx.fillText(divLabel, 60, 326);

      ctx.fillStyle = 'rgba(255, 255, 255, 0.07)';
      roundRect(ctx, 368, 300, 210, 40, 20);
      ctx.fill();
      ctx.fillStyle = '#f1f5f9';
      ctx.font = '600 15px "Plus Jakarta Sans", sans-serif';
      ctx.fillText(rawClass, 384, 326);

      // h. Ateji Kanji Stamp Box (Kanan)
      ctx.fillStyle = 'rgba(30, 20, 42, 0.85)';
      roundRect(ctx, 640, 160, 150, 190, 16);
      ctx.fill();
      ctx.strokeStyle = 'rgba(255, 101, 155, 0.35)';
      ctx.lineWidth = 1.5;
      roundRect(ctx, 640, 160, 150, 190, 16);
      ctx.stroke();

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 36px "Noto Serif JP", serif';
      ctx.textAlign = 'center';
      const atejiChars = atejiList.map(a => a.kanji);
      atejiChars.forEach((ch, idx) => {
        ctx.fillText(ch, 715, 215 + (idx * 50));
      });

      // i. Red Seal Stamp (Inkan)
      ctx.fillStyle = 'rgba(225, 29, 72, 0.88)';
      roundRect(ctx, 815, 220, 95, 95, 12);
      ctx.fill();
      ctx.strokeStyle = '#ffe4e6';
      ctx.lineWidth = 2;
      roundRect(ctx, 818, 223, 89, 89, 10);
      ctx.stroke();

      ctx.fillStyle = '#ffffff';
      ctx.font = '900 24px "Noto Serif JP", serif';
      ctx.fillText('未来', 862, 260);
      ctx.fillText('之印', 862, 296);

      // j. Footer Credential & Barcode
      ctx.textAlign = 'left';
      ctx.fillStyle = '#94a3b8';
      ctx.font = '500 15px "Plus Jakarta Sans", sans-serif';
      ctx.fillText('SMA Wachid Hasyim 2 Taman Sidoarjo · Jawa Timur', 44, 490);

      ctx.fillStyle = 'rgba(255, 255, 255, 0.45)';
      ctx.font = '17px monospace';
      ctx.fillText('||| | |||| | |||||| || | ||| |||| | ||||| | ||', 620, 490);

      // Trigger Download
      const safeName = rawName.replace(/[^a-zA-Z0-9]/g, '-');
      canvas.toBlob((blob) => {
        if (!blob) return;
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `Kartu-Anggota-Mirai-${safeName}.png`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      }, 'image/png');
    });
  }

  // Trigger default generation
  triggerGeneration();
}
"""

    # Sisipkan fungsi initNameGenerator sebelum panggilan initStudioTranslator di akhir berkas
    code = code.replace(
        "if (document.readyState === \"loading\") {\n  document.addEventListener(\"DOMContentLoaded\", initStudioTranslator);\n} else {\n  initStudioTranslator();\n}",
        name_gen_logic + "\n\nfunction setupStudioAll() {\n  initStudioTranslator();\n  initNameGenerator();\n}\n\nif (document.readyState === \"loading\") {\n  document.addEventListener(\"DOMContentLoaded\", setupStudioAll);\n} else {\n  setupStudioAll();\n}"
    )

    with open(translator_js_path, "w", encoding="utf-8") as f:
        f.write(code)
    log("js/translator.js berhasil diperbarui dengan logika Fonetik Katakana, Ateji & Canvas.")

# ==============================================================================
# FITUR 1: STYLING DI css/pages/kamus.css
# ==============================================================================
def update_kamus_css():
    log("=== [1.c] Menambahkan Styling Tab Switcher & Kartu Anggota di css/pages/kamus.css ===")
    kamus_css_path = os.path.join(BASE_DIR, "css", "pages", "kamus.css")
    with open(kamus_css_path, "r", encoding="utf-8") as f:
        css = f.read()

    if "studio-tab-bar" in css:
        log("Styling studio-tab-bar sudah ada di css/pages/kamus.css.")
        return

    namegen_styles = """
/* ==========================================================================
   STUDIO TAB SWITCHER (2-TAB: TRANSLATOR & GENERATOR NAMA)
   ========================================================================== */
.studio-tab-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  max-width: 780px;
  margin: 0 auto 36px auto;
  padding: 6px;
  background: rgba(22, 17, 28, 0.65);
  border: 1.5px solid rgba(255, 101, 155, 0.28);
  border-radius: 999px;
  backdrop-filter: blur(10px);
}

.studio-tab-btn {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 12px 24px;
  background: transparent;
  color: #cbd5e1;
  font-size: 14.5px;
  font-weight: 700;
  border: none;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  user-select: none;
}

.studio-tab-btn .tab-icon {
  font-size: 18px;
}

.studio-tab-btn:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.08);
}

.studio-tab-btn.is-active {
  background: linear-gradient(135deg, #e91e63 0%, #d81b60 100%);
  color: #ffffff;
  box-shadow: 0 4px 18px rgba(233, 30, 99, 0.42);
}

.studio-tab-panel {
  display: block;
  animation: csFadeIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.studio-tab-panel[hidden] {
  display: none !important;
}

/* ==========================================================================
   GENERATOR NAMA JEPANG & KARTU ANGGOTA (OSATSU MIRAI NO HANA)
   ========================================================================== */
.namegen-container {
  max-width: 1080px;
  margin: 0 auto;
}

.namegen-grid {
  display: grid;
  grid-template-columns: 1fr 1.15fr;
  gap: 28px;
  align-items: start;
}

/* Formulir Input */
.namegen-form-card {
  background: linear-gradient(165deg, rgba(22, 17, 28, 0.94) 0%, rgba(14, 11, 18, 0.96) 100%) !important;
  border: 1.5px solid rgba(255, 101, 155, 0.3) !important;
  border-radius: 20px !important;
  padding: 24px !important;
  box-shadow: 0 14px 40px rgba(0, 0, 0, 0.45) !important;
}

.namegen-badge-tag {
  font-size: 12px;
  font-weight: 700;
  color: #ff85b3;
  background: rgba(255, 101, 155, 0.15);
  padding: 4px 12px;
  border-radius: 999px;
  border: 1px solid rgba(255, 101, 155, 0.3);
}

.namegen-form-body {
  margin-top: 18px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.namegen-field-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.namegen-label {
  font-size: 13.5px;
  font-weight: 700;
  color: #ffffff;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.namegen-label .req-star {
  color: #ff4d88;
}

.namegen-sublabel {
  font-size: 11.5px;
  font-weight: 500;
  color: #94a3b8;
}

.namegen-input-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.namegen-input {
  width: 100%;
  padding: 12px 42px 12px 16px;
  background: rgba(10, 8, 14, 0.75);
  border: 1.5px solid rgba(255, 255, 255, 0.14);
  border-radius: 12px;
  color: #ffffff;
  font-size: 15px;
  font-family: inherit;
  transition: all 0.2s ease;
}

.namegen-input:focus {
  outline: none;
  border-color: #ff659b;
  box-shadow: 0 0 0 3px rgba(255, 101, 155, 0.25);
  background: rgba(14, 11, 20, 0.95);
}

.namegen-row-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.namegen-select-wrap {
  position: relative;
}

.namegen-select {
  width: 100%;
  padding: 12px 14px;
  background: rgba(10, 8, 14, 0.75);
  border: 1.5px solid rgba(255, 255, 255, 0.14);
  border-radius: 12px;
  color: #ffffff;
  font-size: 13.5px;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s ease;
}

.namegen-select:focus {
  outline: none;
  border-color: #ff659b;
  box-shadow: 0 0 0 3px rgba(255, 101, 155, 0.25);
}

.namegen-actions-bar {
  margin-top: 6px;
}

.namegen-submit-btn {
  width: 100%;
  padding: 13px;
  font-size: 15px;
  font-weight: 800;
  border-radius: 12px;
}

.namegen-chips-wrap {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-top: 8px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.chips-label {
  font-size: 12px;
  font-weight: 700;
  color: #94a3b8;
}

/* Kolom Hasil & Kartu */
.namegen-result-card {
  background: linear-gradient(165deg, rgba(20, 15, 26, 0.95) 0%, rgba(12, 9, 16, 0.98) 100%) !important;
  border: 1.5px solid rgba(255, 101, 155, 0.32) !important;
  border-radius: 20px !important;
  padding: 24px !important;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.5) !important;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Banner Katakana */
.namegen-phonetic-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: rgba(255, 101, 155, 0.08);
  border: 1.5px solid rgba(255, 101, 155, 0.28);
  border-radius: 14px;
}

.phonetic-label {
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 1.5px;
  color: #ff85b3;
}

.phonetic-display {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-top: 4px;
}

.katakana-large {
  font-size: 30px;
  font-weight: 900;
  color: #ffffff;
  font-family: 'Noto Sans JP', sans-serif;
  text-shadow: 0 0 16px rgba(255, 101, 155, 0.4);
}

.romaji-sub {
  font-size: 15px;
  font-weight: 700;
  color: #ffb8d2;
}

/* Ateji Box */
.namegen-ateji-box {
  background: rgba(10, 8, 14, 0.65);
  border: 1.5px solid rgba(255, 255, 255, 0.1);
  border-radius: 14px;
  padding: 18px;
}

.ateji-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
}

.ateji-icon {
  font-size: 22px;
}

.ateji-head-text strong {
  display: block;
  font-size: 14px;
  color: #ffffff;
}

.ateji-head-text small {
  font-size: 11.5px;
  color: #94a3b8;
}

.ateji-kanji-row {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
}

.ateji-chip {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 101, 155, 0.22);
  border-radius: 10px;
  padding: 8px 12px;
}

.ateji-kanji {
  font-size: 24px;
  font-weight: 900;
  font-family: 'Noto Serif JP', serif;
  color: #ff659b;
  width: 36px;
  text-align: center;
}

.ateji-chip-info {
  display: flex;
  flex-direction: column;
}

.ateji-reading {
  font-size: 13px;
  color: #ffffff;
}

.ateji-meaning {
  font-size: 12px;
  color: #cbd5e1;
}

.ateji-philosophy-text {
  font-size: 13px;
  line-height: 1.6;
  color: #e2e8f0;
  font-style: italic;
  margin: 0;
  padding-top: 10px;
  border-top: 1px dashed rgba(255, 255, 255, 0.12);
}

/* ==========================================================================
   LIVE PREVIEW KARTU TANDA ANGGOTA (OSATSU MIRAI NO HANA)
   ========================================================================== */
.member-card-stage {
  perspective: 1000px;
}

.member-card-wrap {
  width: 100%;
  aspect-ratio: 16 / 9.5;
  background: linear-gradient(135deg, #1b1326 0%, #110d18 50%, #09070e 100%);
  border: 2px solid rgba(255, 101, 155, 0.45);
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 16px 45px rgba(0, 0, 0, 0.65), 0 0 24px rgba(233, 30, 99, 0.22);
  position: relative;
  overflow: hidden;
  color: #ffffff;
  display: flex;
  flex-direction: column;
}

.member-card-wrap::before {
  content: "";
  position: absolute;
  inset: 8px;
  border: 1px dashed rgba(255, 255, 255, 0.12);
  border-radius: 14px;
  pointer-events: none;
}

.member-card-wrap::after {
  content: "";
  position: absolute;
  right: -30px;
  top: 50%;
  transform: translateY(-50%);
  width: 200px;
  height: 200px;
  border-radius: 50%;
  border: 30px solid rgba(255, 101, 155, 0.05);
  pointer-events: none;
}

.mcard-inner {
  position: relative;
  z-index: 2;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.mcard-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.mcard-brand {
  display: flex;
  align-items: center;
  gap: 8px;
}

.mcard-flower-icon {
  font-size: 22px;
}

.mcard-brand-text {
  display: flex;
  flex-direction: column;
}

.mcard-club-name {
  font-size: 15px;
  font-weight: 900;
  letter-spacing: 1px;
  color: #ffffff;
}

.mcard-sub-jp {
  font-size: 10px;
  color: #ff85b3;
  font-family: 'Noto Serif JP', serif;
}

.mcard-id-pill {
  font-size: 11px;
  font-weight: 800;
  font-family: monospace;
  background: rgba(255, 101, 155, 0.18);
  border: 1px solid rgba(255, 101, 155, 0.4);
  color: #ff85b3;
  padding: 4px 10px;
  border-radius: 999px;
}

.mcard-body {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 10px 0;
}

.mcard-name-col {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.mcard-jp-name {
  font-size: 26px;
  font-weight: 900;
  font-family: 'Noto Sans JP', sans-serif;
  color: #ffffff;
  text-shadow: 0 0 12px rgba(255, 101, 155, 0.5);
}

.mcard-latin-name {
  font-size: 15px;
  font-weight: 700;
  color: #ffd1e3;
}

.mcard-meta-row {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 6px;
  flex-wrap: wrap;
}

.mcard-meta-pill {
  font-size: 10.5px;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.14);
  padding: 3px 8px;
  border-radius: 6px;
  color: #f1f5f9;
}

.mcard-ateji-col {
  display: flex;
  align-items: center;
  gap: 8px;
}

.mcard-kanji-stamp {
  display: flex;
  flex-direction: column;
  gap: 2px;
  background: rgba(20, 14, 28, 0.85);
  border: 1px solid rgba(255, 101, 155, 0.35);
  border-radius: 8px;
  padding: 4px 8px;
  font-family: 'Noto Serif JP', serif;
  font-size: 16px;
  font-weight: 800;
  color: #ffffff;
  text-align: center;
}

.mcard-red-seal {
  width: 44px;
  height: 44px;
  background: #e11d48;
  border: 1.5px solid #ffe4e6;
  border-radius: 8px;
  color: #ffffff;
  font-size: 12px;
  font-weight: 900;
  font-family: 'Noto Serif JP', serif;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  line-height: 1.1;
  box-shadow: 0 4px 10px rgba(225, 29, 72, 0.4);
}

.mcard-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 10.5px;
  color: #94a3b8;
}

.mcard-barcode {
  font-family: monospace;
  letter-spacing: 2px;
  color: rgba(255, 255, 255, 0.45);
}

.namegen-download-row {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
}

.download-card-btn {
  width: 100%;
  padding: 14px;
  font-size: 15px;
  font-weight: 800;
  border-radius: 12px;
}

.download-hint {
  font-size: 12px;
  color: #94a3b8;
  text-align: center;
}

@media (max-width: 820px) {
  .namegen-grid {
    grid-template-columns: 1fr;
  }

  .studio-tab-btn {
    padding: 10px 14px;
    font-size: 13px;
  }

  .namegen-row-2col {
    grid-template-columns: 1fr;
  }
}
"""

    css += "\n" + namegen_styles.strip() + "\n"
    with open(kamus_css_path, "w", encoding="utf-8") as f:
        f.write(css)
    log("css/pages/kamus.css berhasil diperbarui dengan styling Tab & Generator Kartu.")

# ==============================================================================
# FITUR 2: KUIS KEPRIBADIAN KECOCOKAN DIVISI
# ==============================================================================
def update_divisi_html():
    log("=== [2.a] Menambahkan Seksi Kuis Kepribadian di divisi/index.html ===")
    divisi_html_path = os.path.join(BASE_DIR, "divisi", "index.html")
    with open(divisi_html_path, "r", encoding="utf-8") as f:
        html = f.read()

    if "id=\"kuis-divisi\"" in html:
        log("Seksi kuis-divisi sudah ada di divisi/index.html.")
        return

    quiz_section_html = """
  <!-- =====================================================================
       SEKSI KUIS KEPRIBADIAN: TES KECOCOKAN DIVISI MIRAI NO HANA
       ===================================================================== -->
  <section class="section mirai-section-dark division-quiz-section" id="kuis-divisi">
    <div class="section-intro">
      <p class="section-eyebrow"><span class="jp-kanji">部活適性診断テスト</span></p>
      <h2 class="heading">🍱 Kuis Kepribadian: <span>Tes Kecocokan Divisi</span></h2>
      <p class="section-desc">Bingung ingin bergabung ke divisi mana? Jawab 5 pertanyaan santai berikut untuk menemukan divisi Mirai no Hana yang paling pas dengan minat, bakat, dan karaktermu!</p>
    </div>

    <div class="quiz-container">
      <div class="mirai-card-dark quiz-card" id="quizCard">
        <!-- PROGRESS BAR -->
        <div class="quiz-progress-wrap">
          <div class="quiz-progress-header">
            <span class="quiz-step-count" id="quizStepCount">Pertanyaan 1 dari 5</span>
            <span class="quiz-step-percent" id="quizStepPercent">20% Selesai</span>
          </div>
          <div class="quiz-progress-bar">
            <div class="quiz-progress-fill" id="quizProgressFill" style="width: 20%;"></div>
          </div>
        </div>

        <!-- STAGE PERTANYAAN -->
        <div class="quiz-stage" id="quizStage">
          <h3 class="quiz-question-title" id="quizQuestionText">1. Apa hal pertama yang paling menarik perhatianmu di acara festival budaya Jepang (Matsuri)?</h3>
          <div class="quiz-options-list" id="quizOptionsList">
            <!-- Pilihan jawaban diinjeksi via JS -->
          </div>
        </div>

        <!-- STAGE HASIL (MUNCUL SETELAH 5 SOAL SELESAI) -->
        <div class="quiz-result-stage" id="quizResultStage" hidden>
          <div class="quiz-result-hero">
            <div class="result-badge-icon" id="quizResultIcon">📚</div>
            <span class="result-kicker">HASIL DIAGNOSIS DIVISI KAMU</span>
            <h3 class="result-title" id="quizResultTitle">Divisi Bahasa &amp; Budaya</h3>
            <span class="result-kanji" id="quizResultKanji">言語・文化部門</span>
          </div>

          <div class="quiz-meter-wrap">
            <div class="meter-text-row">
              <span>Tingkat Kecocokan Karakter:</span>
              <strong class="meter-score-highlight" id="quizScoreHighlight">88% Cocok!</strong>
            </div>
            <div class="meter-bar-track">
              <div class="meter-bar-fill" id="quizMeterFill" style="width: 88%;"></div>
            </div>
          </div>

          <p class="quiz-explanation" id="quizExplanation">
            Kamu memiliki rasa ingin tahu yang mendalam terhadap percakapan, makna aksara Kanji, dan filosofi kebudayaan Jepang. Kamu adalah tipe pembelajar tekun yang senang berdiskusi dan memahami cara berpikir masyarakat Jepang dari akarnya.
          </p>

          <div class="quiz-breakdown-box">
            <h4 class="breakdown-title">📊 Rincian Skor Seluruh Divisi:</h4>
            <div class="breakdown-bars" id="quizBreakdownBars"></div>
          </div>

          <div class="quiz-actions-group">
            <a href="bahasa.html" class="btn primary quiz-cta-link" id="quizCtaLink">
              <span>🚀 Jelajahi Profil Divisi Bahasa →</span>
            </a>
            <button type="button" class="btn quiz-restart-btn" id="quizRestartBtn">
              <span>🔄 Ulangi Tes</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
"""

    html = html.replace("</main>", quiz_section_html + "\n</main>")

    # Tambahkan script quiz-divisi.js sebelum </body>
    if "quiz-divisi.js" not in html:
        html = html.replace(
            "<script src=\"../js/main.js\"></script>",
            "<script src=\"../js/main.js\"></script>\n<script src=\"../js/quiz-divisi.js\"></script>"
        )

    with open(divisi_html_path, "w", encoding="utf-8") as f:
        f.write(html)
    log("divisi/index.html berhasil diperbarui dengan Seksi Kuis.")

def create_quiz_divisi_js():
    log("=== [2.b] Membuat Berkas js/quiz-divisi.js ===")
    quiz_js_path = os.path.join(BASE_DIR, "js", "quiz-divisi.js")

    js_code = """/**
 * File: js/quiz-divisi.js
 * Deskripsi: Logika Interaktif Kuis Kepribadian & Tes Kecocokan Divisi Klub MIRAI NO HANA
 */

(() => {
  "use strict";

  const QUESTIONS = [
    {
      id: 1,
      title: "1. Apa hal pertama yang paling menarik perhatianmu di acara festival budaya Jepang (Matsuri)?",
      options: [
        {
          letter: "A",
          division: "bahasa",
          text: "Mendengarkan percakapan bahasa Jepang, lirik lagu tradisional, dan pameran kaligrafi Shodou."
        },
        {
          letter: "B",
          division: "cosplay",
          text: "Penampilan cosplayer berkostum anime keren dan aksi drama panggung atau penampilan anisong."
        },
        {
          letter: "C",
          division: "desain",
          text: "Booth seni kreatif, poster fanart ilustrator, standee maskot, dan desain stiker estetik."
        },
        {
          letter: "D",
          division: "kewirausahaan",
          text: "Deretan stan kuliner Yatai yang menjual Takoyaki, Onigiri, dan etalase merchandise eksklusif."
        }
      ]
    },
    {
      id: 2,
      title: "2. Kegiatan apa yang menurutmu paling seru dilakukan saat kumpul ekstrakurikuler mingguan?",
      options: [
        {
          letter: "A",
          division: "bahasa",
          text: "Belajar kosakata baru, latihan kaiwa (percakapan), dan kuis cerdas cermat kanji seru."
        },
        {
          letter: "B",
          division: "cosplay",
          text: "Workshop makeup karakter, tutorial styling wig, dan latihan pose performa panggung."
        },
        {
          letter: "C",
          division: "desain",
          text: "Menggambar karakter digital/manual bareng dan mendesain materi visual untuk medsos klub."
        },
        {
          letter: "D",
          division: "kewirausahaan",
          text: "Diskusi ide menu jualan baru, meracik cinderamata kreatif, dan simulasi stan konbini."
        }
      ]
    },
    {
      id: 3,
      title: "3. Skill apa yang paling ingin kamu kuasai dan kembangkan secara serius tahun ini?",
      options: [
        {
          letter: "A",
          division: "bahasa",
          text: "Lancar berbicara bahasa Jepang, membaca aksara kanji, dan persiapan sertifikasi JLPT."
        },
        {
          letter: "B",
          division: "cosplay",
          text: "Keahlian berakting/ekspresi karakter, kreasi prop aksesoris kostum, dan percaya diri tampil di publik."
        },
        {
          letter: "C",
          division: "desain",
          text: "Mahir software desain/ilustrasi (Canva, IbisPaint, Photoshop) dan membuat portofolio seni kreatif."
        },
        {
          letter: "D",
          division: "kewirausahaan",
          text: "Strategi pemasaran produk, manajemen kas organisasi, dan komunikasi tawar-menawar bisnis ramah."
        }
      ]
    },
    {
      id: 4,
      title: "4. Saat menonton anime favoritmu, aspek mana yang paling sering membuatmu kagum?",
      options: [
        {
          letter: "A",
          division: "bahasa",
          text: "Frasa unik yang diucapkan karakter, logat dialek daerah, dan pesan moral mendalam ceritanya."
        },
        {
          letter: "B",
          division: "cosplay",
          text: "Detail pakaian, bentuk rambut, sepatu, dan ekspresi ikonik sang karakter saat beraksi."
        },
        {
          letter: "C",
          division: "desain",
          text: "Gaya visual animasi, komposisi warna background, desain karakter, dan visual opening/ending."
        },
        {
          letter: "D",
          division: "kewirausahaan",
          text: "Popularitas merchandise resminya, kolaborasi cafe bertema anime, dan produk unik yang dijual."
        }
      ]
    },
    {
      id: 5,
      title: "5. Peran seperti apa yang paling cocok dengan gaya kerjamu di kepanitiaan acara sekolah?",
      options: [
        {
          letter: "A",
          division: "bahasa",
          text: "Penyusun materi sambutan, MC bilingual, atau pembuat panduan teknis yang cermat."
        },
        {
          letter: "B",
          division: "cosplay",
          text: "Penampil utama di atas panggung, koordinator talent kostum, atau pemandu interaksi penonton."
        },
        {
          letter: "C",
          division: "desain",
          text: "Koordinator publikasi visual, pembuat poster promosi, dekorasi panggung, dan kartu tanda pengenal."
        },
        {
          letter: "D",
          division: "kewirausahaan",
          text: "Koordinator sponsorship, penanggung jawab stan penjualan tiket/merchandise, dan bendahara bazaar."
        }
      ]
    }
  ];

  const DIVISION_INFO = {
    bahasa: {
      title: "Divisi Bahasa & Budaya",
      kanji: "言語・文化部門",
      icon: "📚",
      link: "bahasa.html",
      explanation: "Kamu memiliki rasa ingin tahu yang mendalam terhadap percakapan, makna aksara Kanji, dan filosofi kebudayaan Jepang. Kamu adalah tipe pembelajar tekun yang senang berdiskusi dan memahami cara berpikir masyarakat Jepang dari akarnya."
    },
    cosplay: {
      title: "Divisi Cosplay & Seni Peran",
      kanji: "コスプレ部門",
      icon: "🎭",
      link: "cosplay.html",
      explanation: "Kamu memiliki jiwa ekspresif, percaya diri, dan menyukai dunia seni peran! Kamu antusias menghidupkan karakter 2D menjadi nyata lewat kostum, tata rias wajah, wig styling, dan aksi panggung yang memukau penonton."
    },
    desain: {
      title: "Divisi Desain & Kreatif",
      kanji: "デザイン部門",
      icon: "🎨",
      link: "desain.html",
      explanation: "Kamu memiliki kepekaan visual yang tinggi dan imajinasi kreatif tanpa batas. Kamu senang menggoreskan karya ilustrasi, menyusun palet warna estetik, dan merancang identitas grafis yang memanjakan mata."
    },
    kewirausahaan: {
      title: "Divisi Kewirausahaan",
      kanji: "起業・物販部門",
      icon: "🍱",
      link: "kewirausahaan.html",
      explanation: "Kamu berjiwa strategis, komunikatif, dan senang berinovasi dalam dunia bisnis kreatif. Kamu cocok memimpin stan bazaar Mirai no Konbini, mengelola merchandise, dan mengembangkan kemandirian finansial klub."
    }
  };

  function initQuiz() {
    const quizCard = document.getElementById("quizCard");
    const quizStage = document.getElementById("quizStage");
    const quizResultStage = document.getElementById("quizResultStage");
    const quizStepCount = document.getElementById("quizStepCount");
    const quizStepPercent = document.getElementById("quizStepPercent");
    const quizProgressFill = document.getElementById("quizProgressFill");
    const quizQuestionText = document.getElementById("quizQuestionText");
    const quizOptionsList = document.getElementById("quizOptionsList");

    const quizResultIcon = document.getElementById("quizResultIcon");
    const quizResultTitle = document.getElementById("quizResultTitle");
    const quizResultKanji = document.getElementById("quizResultKanji");
    const quizScoreHighlight = document.getElementById("quizScoreHighlight");
    const quizMeterFill = document.getElementById("quizMeterFill");
    const quizExplanation = document.getElementById("quizExplanation");
    const quizBreakdownBars = document.getElementById("quizBreakdownBars");
    const quizCtaLink = document.getElementById("quizCtaLink");
    const quizRestartBtn = document.getElementById("quizRestartBtn");

    if (!quizCard || !quizStage || !quizOptionsList) return;

    let currentStep = 0;
    const scores = { bahasa: 0, cosplay: 0, desain: 0, kewirausahaan: 0 };

    function renderQuestion(stepIdx) {
      const q = QUESTIONS[stepIdx];
      if (!q) return;

      quizStepCount.textContent = `Pertanyaan ${stepIdx + 1} dari ${QUESTIONS.length}`;
      const percent = Math.round(((stepIdx + 1) / QUESTIONS.length) * 100);
      quizStepPercent.textContent = `${percent}% Selesai`;
      quizProgressFill.style.width = `${percent}%`;

      quizQuestionText.textContent = q.title;

      quizOptionsList.innerHTML = q.options.map(opt => `
        <button type="button" class="quiz-option-btn" data-div="${opt.division}">
          <span class="quiz-opt-letter">${opt.letter}</span>
          <span class="quiz-opt-text">${opt.text}</span>
        </button>
      `).join("");

      // Animasi pergantian soal
      quizStage.classList.remove("quiz-anim-pop");
      void quizStage.offsetWidth;
      quizStage.classList.add("quiz-anim-pop");
    }

    function renderResults() {
      quizStage.hidden = true;
      quizResultStage.hidden = false;

      // Hitung persentase
      const totalPoints = Object.values(scores).reduce((a, b) => a + b, 0) || 1;
      const sorted = Object.entries(scores).sort((a, b) => b[1] - a[1]);
      const topDivKey = sorted[0][0];
      const topDivInfo = DIVISION_INFO[topDivKey];

      // Kalkulasi match rate (skor tertinggi proporsional antara 78% s/d 96%)
      const matchRate = Math.min(96, Math.max(76, Math.round((sorted[0][1] / QUESTIONS.length) * 40 + 56)));

      quizResultIcon.textContent = topDivInfo.icon;
      quizResultTitle.textContent = topDivInfo.title;
      quizResultKanji.textContent = topDivInfo.kanji;
      quizScoreHighlight.textContent = `${matchRate}% Cocok!`;
      quizMeterFill.style.width = `${matchRate}%`;
      quizExplanation.textContent = topDivInfo.explanation;

      quizCtaLink.href = topDivInfo.link;
      quizCtaLink.innerHTML = `<span>🚀 Jelajahi Profil ${topDivInfo.title} →</span>`;

      // Breakdown bars
      quizBreakdownBars.innerHTML = sorted.map(([k, count]) => {
        const info = DIVISION_INFO[k];
        const barPercent = Math.round((count / QUESTIONS.length) * 100);
        return `
          <div class="breakdown-item">
            <div class="breakdown-info">
              <span>${info.icon} ${info.title}</span>
              <strong>${barPercent}%</strong>
            </div>
            <div class="breakdown-track">
              <div class="breakdown-fill ${k === topDivKey ? 'is-top' : ''}" style="width: ${barPercent}%;"></div>
            </div>
          </div>
        `;
      }).join("");

      quizResultStage.classList.remove("quiz-anim-pop");
      void quizResultStage.offsetWidth;
      quizResultStage.classList.add("quiz-anim-pop");
    }

    quizOptionsList.addEventListener("click", (e) => {
      const btn = e.target.closest(".quiz-option-btn");
      if (!btn) return;

      const divKey = btn.dataset.div;
      if (divKey && scores[divKey] !== undefined) {
        scores[divKey]++;
      }

      window.MiraiSound?.playClickIfIdle();

      currentStep++;
      if (currentStep < QUESTIONS.length) {
        renderQuestion(currentStep);
      } else {
        renderResults();
      }
    });

    if (quizRestartBtn) {
      quizRestartBtn.addEventListener("click", () => {
        window.MiraiSound?.playClickIfIdle();
        currentStep = 0;
        scores.bahasa = 0;
        scores.cosplay = 0;
        scores.desain = 0;
        scores.kewirausahaan = 0;

        quizResultStage.hidden = true;
        quizStage.hidden = false;
        renderQuestion(0);
      });
    }

    // Render soal pertama
    renderQuestion(0);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initQuiz);
  } else {
    initQuiz();
  }
})();
"""

    with open(quiz_js_path, "w", encoding="utf-8") as f:
        f.write(js_code)
    log("js/quiz-divisi.js berhasil dibuat dengan 5 pertanyaan & kalkulasi kecocokan.")

def update_kegiatan_html():
    log("=== [2.c] Menambahkan Banner Pintasan Kuis di kegiatan/index.html ===")
    kegiatan_html_path = os.path.join(BASE_DIR, "kegiatan", "index.html")
    with open(kegiatan_html_path, "r", encoding="utf-8") as f:
        html = f.read()

    if "divisi-quiz-banner" in html:
        log("Banner divisi-quiz-banner sudah ada di kegiatan/index.html.")
        return

    banner_html = """
    <!-- BANNER PINTASAN KUIS KECOCOKAN DIVISI -->
    <div class="divisi-quiz-banner mirai-card-dark" style="margin: 40px auto 25px; max-width: 920px; padding: 28px 24px; text-align: center;">
      <div style="font-size: 34px; margin-bottom: 8px;">🍱 🎌</div>
      <h3 style="font-size: 22px; font-weight: 800; color: #ffffff; margin-bottom: 10px;">Bingung Memilih Divisi yang Pas?</h3>
      <p style="color: #cbd5e1; font-size: 14.5px; max-width: 620px; margin: 0 auto 20px; line-height: 1.6;">
        Ikuti <strong>Tes Kecocokan Divisi</strong> interaktif (5 pertanyaan santai) untuk menemukan apakah minat dan bakatmu paling cocok di <strong>Bahasa</strong>, <strong>Cosplay</strong>, <strong>Desain</strong>, atau <strong>Kewirausahaan</strong>!
      </p>
      <a href="../divisi/index.html#kuis-divisi" class="btn primary" style="display: inline-flex; align-items: center; gap: 8px;">
        <span>🍱 Ikuti Tes Kecocokan Divisi (5 Soal) →</span>
      </a>
    </div>
"""

    # Sisipkan sebelum penutup dokumentasi-section di kegiatan/index.html
    html = html.replace("  </section>\n</main>", banner_html + "  </section>\n</main>")

    with open(kegiatan_html_path, "w", encoding="utf-8") as f:
        f.write(html)
    log("kegiatan/index.html berhasil ditambahkan banner pintasan kuis divisi.")

def update_kegiatan_divisi_css():
    log("=== [2.d] Menambahkan Styling Kuis Divisi di css/pages/kegiatan-divisi.css ===")
    kd_css_path = os.path.join(BASE_DIR, "css", "pages", "kegiatan-divisi.css")
    with open(kd_css_path, "r", encoding="utf-8") as f:
        css = f.read()

    if "division-quiz-section" in css:
        log("Styling division-quiz-section sudah ada di css/pages/kegiatan-divisi.css.")
        return

    quiz_styles = """
/* ==========================================================================
   KUIS KEPRIBADIAN: TES KECOCOKAN DIVISI (.division-quiz-section)
   ========================================================================== */
.division-quiz-section {
  padding-top: 60px !important;
  padding-bottom: 80px !important;
}

.quiz-container {
  max-width: 820px;
  margin: 0 auto;
}

.quiz-card {
  padding: 36px 32px !important;
  border-radius: 24px !important;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6) !important;
}

/* Progress Bar */
.quiz-progress-wrap {
  margin-bottom: 28px;
}

.quiz-progress-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 13px;
  font-weight: 700;
  color: #94a3b8;
}

.quiz-step-count {
  color: #ff85b3;
}

.quiz-progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 999px;
  overflow: hidden;
}

.quiz-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #ff659b 0%, #e91e63 100%);
  border-radius: 999px;
  transition: width 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 0 10px rgba(233, 30, 99, 0.5);
}

/* Pertanyaan & Pilihan */
.quiz-question-title {
  font-size: clamp(18px, 2.5vw, 22px);
  font-weight: 800;
  color: #ffffff;
  line-height: 1.45;
  margin: 0 0 24px 0;
}

.quiz-options-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.quiz-option-btn {
  display: flex;
  align-items: center;
  gap: 16px;
  width: 100%;
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.04);
  border: 1.5px solid rgba(255, 255, 255, 0.12);
  border-radius: 14px;
  color: #e2e8f0;
  text-align: left;
  font-family: inherit;
  font-size: 14.5px;
  line-height: 1.5;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  user-select: none;
}

.quiz-opt-letter {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  flex-shrink: 0;
  background: rgba(255, 101, 155, 0.15);
  border: 1px solid rgba(255, 101, 155, 0.35);
  border-radius: 8px;
  font-size: 14px;
  font-weight: 800;
  color: #ff85b3;
  transition: all 0.2s ease;
}

.quiz-opt-text {
  flex: 1;
}

.quiz-option-btn:hover {
  background: rgba(255, 101, 155, 0.1);
  border-color: #ff659b;
  transform: translateX(4px);
  color: #ffffff;
}

.quiz-option-btn:hover .quiz-opt-letter {
  background: #e91e63;
  color: #ffffff;
  box-shadow: 0 0 10px rgba(233, 30, 99, 0.5);
}

/* Hasil Kuis */
.quiz-result-hero {
  text-align: center;
  margin-bottom: 24px;
}

.result-badge-icon {
  font-size: 56px;
  line-height: 1;
  margin-bottom: 10px;
}

.result-kicker {
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 2px;
  color: #ff85b3;
  display: block;
  margin-bottom: 4px;
}

.result-title {
  font-size: clamp(24px, 4vw, 34px);
  font-weight: 900;
  color: #ffffff;
  margin: 0 0 4px 0;
}

.result-kanji {
  font-size: 14px;
  font-family: 'Noto Serif JP', serif;
  color: #ffd1e3;
}

/* Meter Bar */
.quiz-meter-wrap {
  background: rgba(10, 8, 14, 0.65);
  border: 1px solid rgba(255, 101, 155, 0.25);
  border-radius: 14px;
  padding: 16px 20px;
  margin-bottom: 20px;
}

.meter-text-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  color: #cbd5e1;
  margin-bottom: 8px;
}

.meter-score-highlight {
  font-size: 18px;
  font-weight: 900;
  color: #ff659b;
}

.meter-bar-track {
  width: 100%;
  height: 10px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 999px;
  overflow: hidden;
}

.meter-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #ff659b 0%, #e91e63 100%);
  border-radius: 999px;
  transition: width 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 0 12px rgba(233, 30, 99, 0.5);
}

.quiz-explanation {
  font-size: 15px;
  line-height: 1.7;
  color: #cbd5e1;
  text-align: center;
  max-width: 680px;
  margin: 0 auto 28px auto;
}

/* Breakdown Bars */
.quiz-breakdown-box {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  padding: 18px 20px;
  margin-bottom: 28px;
}

.breakdown-title {
  font-size: 13.5px;
  font-weight: 800;
  color: #ffffff;
  margin: 0 0 14px 0;
}

.breakdown-item {
  margin-bottom: 10px;
}

.breakdown-item:last-child {
  margin-bottom: 0;
}

.breakdown-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 13px;
  color: #cbd5e1;
  margin-bottom: 4px;
}

.breakdown-track {
  width: 100%;
  height: 6px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 999px;
  overflow: hidden;
}

.breakdown-fill {
  height: 100%;
  background: rgba(255, 255, 255, 0.25);
  border-radius: 999px;
  transition: width 0.5s ease;
}

.breakdown-fill.is-top {
  background: #ff659b;
  box-shadow: 0 0 8px rgba(255, 101, 155, 0.5);
}

/* Actions Group */
.quiz-actions-group {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 14px;
  flex-wrap: wrap;
}

.quiz-cta-link {
  padding: 13px 26px !important;
  font-size: 15px !important;
  font-weight: 800 !important;
}

.quiz-restart-btn {
  background: rgba(255, 255, 255, 0.08) !important;
  color: #cbd5e1 !important;
  border: 1px solid rgba(255, 255, 255, 0.16) !important;
  padding: 13px 22px !important;
  font-size: 14.5px !important;
}

.quiz-restart-btn:hover {
  background: rgba(255, 255, 255, 0.15) !important;
  color: #ffffff !important;
}

.quiz-anim-pop {
  animation: csFadeIn 0.25s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@media (max-width: 600px) {
  .quiz-card {
    padding: 24px 18px !important;
  }

  .quiz-actions-group {
    flex-direction: column;
    width: 100%;
  }

  .quiz-cta-link, .quiz-restart-btn {
    width: 100%;
    text-align: center;
    justify-content: center;
  }
}
"""

    css += "\n" + quiz_styles.strip() + "\n"
    with open(kd_css_path, "w", encoding="utf-8") as f:
        f.write(css)
    log("css/pages/kegiatan-divisi.css berhasil diperbarui dengan styling Kuis Divisi.")

def update_tree_doc():
    log("=== [3] Memperbarui panduan/tree.md dengan js/quiz-divisi.js ===")
    tree_path = os.path.join(BASE_DIR, "panduan", "tree.md")
    with open(tree_path, "r", encoding="utf-8") as f:
        tree = f.read()

    old_tree_js = """│   ├── translator.js               # Mesin bantu terjemahan
│   └── api.js                      # Koneksi endpoint data"""

    new_tree_js = """│   ├── translator.js               # Mesin terjemahan & generator nama Jepang/KTA
│   ├── quiz-divisi.js              # Kuis kepribadian & tes kecocokan 4 divisi
│   └── api.js                      # Koneksi endpoint data"""

    if old_tree_js in tree:
        tree = tree.replace(old_tree_js, new_tree_js)
        with open(tree_path, "w", encoding="utf-8") as f:
            f.write(tree)
        log("panduan/tree.md berhasil diperbarui.")

def verify_all_css():
    log("=== [4] Verifikasi Integritas Kurung Kurawal CSS ===")
    css_dir = os.path.join(BASE_DIR, "css", "pages")
    for fname in sorted(os.listdir(css_dir)):
        if not fname.endswith(".css"):
            continue
        fpath = os.path.join(css_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            c = f.read()
        o, cl = c.count("{"), c.count("}")
        assert o == cl, f"Ketidakseimbangan kurung pada {fname}: open={o}, close={cl}"
        log(f"CSS OK: {fname} ({o} pasang kurung)")
    log("SELURUH BERKAS CSS 100% BALANCED!")

if __name__ == "__main__":
    update_kamus_html()
    update_translator_js()
    update_kamus_css()
    update_divisi_html()
    create_quiz_divisi_js()
    update_kegiatan_html()
    update_kegiatan_divisi_css()
    update_tree_doc()
    verify_all_css()
    log("SEMUA 2 FITUR INTERAKTIF BERHASIL DIBANGUN & DIINTEGRASIKAN!")
