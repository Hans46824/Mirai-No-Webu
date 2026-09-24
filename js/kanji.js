/**
 * ==============================================================================
 * Mirai No Hana — Kamus & Karakter Belajar (Kana & Kanji)
 * ==============================================================================
 * Modul ini mengatur fungsionalitas pencarian, filter, animasi goresan (stroke order),
 * pengambilan data KanjiAPI.dev, lokalisasi Romaji, translasi dinamis Bahasa Indonesia,
 * serta pengurutan kanji berdasarkan goresan (stroke count) dan tingkat pendidikan (grade).
 * 
 * Fitur Utama:
 * 1. Pemuatan Metadata Kanji: Memetakan 13.000+ karakter ke stroke count dan grade dari data/kanji-meta.json.
 * 2. Pengurutan Kanji Otomatis: Diurutkan berdasarkan jumlah goresan (Ascending) lalu grade (Ascending).
 * 3. Detail Kanji Komprehensif: Onyomi (China), Kunyomi (Jepang), Romaji, arti Bahasa Indonesia murni.
 * 4. Kosakata Terkait: Menampilkan [Kanji] [Kana] ([Romaji]) — [Arti Bahasa Indonesia] dengan translasi lazy.
 * 5. Tab Hiragana & Katakana: Kamus interaktif dengan animasi goresan huruf.
 * ==============================================================================
 */

/**
 * Modul komunikasi API untuk data Kanji dari KanjiAPI.dev
 * Dilengkapi dengan caching lokal (localStorage) agar beban jaringan minim dan respon instan.
 */
const KanjiAPI = {
    baseUrl: "https://kanjiapi.dev/v1",

    /**
     * Mengambil daftar karakter kanji berdasarkan level JLPT (5 sampai 1)
     * @param {number} levelNum - Angka level JLPT (5 = Dasar, 1 = Lanjutan)
     * @returns {Promise<Array<string>>} - Array karakter kanji (contoh: ["日", "一", ...])
     */
    async getJlptList(levelNum) {
        const cacheKey = `mnh_kapi_jlpt_${levelNum}`;
        try {
            const cached = localStorage.getItem(cacheKey);
            if (cached) {
                const parsed = JSON.parse(cached);
                if (Array.isArray(parsed) && parsed.length > 0) return parsed;
            }
        } catch (e) {
            // Abaikan kesalahan pembacaan localStorage
        }

        try {
            const res = await fetch(`${this.baseUrl}/kanji/jlpt-${levelNum}`);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const data = await res.json();
            if (Array.isArray(data)) {
                try {
                    localStorage.setItem(cacheKey, JSON.stringify(data));
                } catch (e) {}
                return data;
            }
        } catch (err) {
            console.warn(`Gagal memuat list JLPT N${levelNum} dari KanjiAPI:`, err);
        }
        return [];
    },

    /**
     * Mengambil detail lengkap kanji (arti, bacaan on/kun, stroke count, grade)
     * @param {string} kanji - Satu karakter kanji
     * @returns {Promise<Object|null>} - Objek detail kanji
     */
    async getKanjiDetail(kanji) {
        const cacheKey = `mnh_kapi_detail_${kanji}`;
        try {
            const cached = localStorage.getItem(cacheKey);
            if (cached) return JSON.parse(cached);
        } catch (e) {}

        try {
            const res = await fetch(`${this.baseUrl}/kanji/${encodeURIComponent(kanji)}`);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const data = await res.json();
            try {
                localStorage.setItem(cacheKey, JSON.stringify(data));
            } catch (e) {}
            return data;
        } catch (err) {
            console.warn(`Gagal memuat detail kanji ${kanji} dari KanjiAPI:`, err);
            return null;
        }
    },

    /**
     * Mengambil daftar kosakata contoh yang menggunakan kanji tertentu
     * @param {string} kanji - Satu karakter kanji
     * @returns {Promise<Array<Object>>} - Daftar objek kata dengan atribut word, reading, meaning
     */
    async getKanjiWords(kanji) {
        const cacheKey = `mnh_kapi_words_${kanji}`;
        try {
            const cached = localStorage.getItem(cacheKey);
            if (cached) {
                const parsed = JSON.parse(cached);
                if (Array.isArray(parsed)) {
                    return parsed.map((w) => ({
                        ...w,
                        rawMeaning: w.rawMeaning || w.meaning,
                        _translated: Boolean(w._translated)
                    }));
                }
            }
        } catch (e) {}

        try {
            const res = await fetch(`${this.baseUrl}/words/${encodeURIComponent(kanji)}`);
            if (!res.ok) return [];
            const raw = await res.json();
            const words = [];
            for (const item of raw) {
                const variant = item.variants?.[0];
                const glosses = item.meanings?.[0]?.glosses;
                if (variant && glosses?.length) {
                    const rawMeaning = glosses.slice(0, 2).join(", ");
                    // Terjemahkan langsung jika tersedia di kamus sinkron lokal
                    const directTrans = window.MiraiTranslator?.translateSync ? window.MiraiTranslator.translateSync(rawMeaning) : "";
                    const isTrans = Boolean(directTrans && directTrans.toLowerCase() !== rawMeaning.toLowerCase());
                    words.push({
                        word: variant.written || variant.pronounced,
                        reading: variant.pronounced,
                        rawMeaning: rawMeaning,
                        meaning: isTrans ? directTrans : rawMeaning,
                        _translated: isTrans
                    });
                    if (words.length >= 4) break;
                }
            }
            try {
                localStorage.setItem(cacheKey, JSON.stringify(words));
            } catch (e) {}
            return words;
        } catch (err) {
            return [];
        }
    }
};
window.KanjiAPI = KanjiAPI;

/**
 * Pemuat data metadata goresan dan grade kanji (data/kanji-meta.json)
 * Memuat pemetaan karakter ke [stroke_count, grade] agar pengurutan instan tanpa menunggu API detail.
 */
let kanjiMetaCache = null;
async function ensureKanjiMeta() {
    if (kanjiMetaCache) return kanjiMetaCache;
    try {
        const res = await fetch("data/kanji-meta.json");
        if (res.ok) {
            kanjiMetaCache = await res.json();
            return kanjiMetaCache;
        }
    } catch (e) {
        console.warn("Gagal memuat data/kanji-meta.json:", e);
    }
    return {};
}
window.ensureKanjiMeta = ensureKanjiMeta;

/**
 * Mengubah teks Kana (Hiragana/Katakana) menjadi Romaji Latin
 * Mengutamakan library WanaKana bila tersedia di browser, dengan fallback tabel konversi mandiri.
 * 
 * @param {string} kana - String kana (misal: "ハン", "なか.ば", "にほん")
 * @returns {string} - Representasi Romaji huruf kecil (misal: "han", "naka.ba", "nihon")
 */
function kanaToRomaji(kana) {
    if (!kana || typeof kana !== "string") return "";

    // 1. Prioritaskan WanaKana jika CDN aktif
    if (window.wanakana && typeof window.wanakana.toRomaji === "function") {
        return window.wanakana.toRomaji(kana);
    }

    // 2. Fallback offline mandiri
    const kanaMap = {
        "あ":"a","い":"i","う":"u","え":"e","お":"o",
        "か":"ka","き":"ki","く":"ku","け":"ke","こ":"ko",
        "さ":"sa","し":"shi","す":"su","せ":"se","そ":"so",
        "た":"ta","ち":"chi","つ":"tsu","て":"te","と":"to",
        "な":"na","に":"ni","ぬ":"nu","ne":"ne","の":"no",
        "は":"ha","ひ":"hi","ふ":"fu","へ":"he","ほ":"ho",
        "ま":"ma","み":"mi","む":"mu","め":"me","も":"mo",
        "や":"ya","ゆ":"yu","よ":"yo",
        "ら":"ra","り":"ri","る":"ru","れ":"re","ろ":"ro",
        "わ":"wa","ゐ":"wi","ゑ":"we","を":"wo","ん":"n",
        "が":"ga","ぎ":"gi","ぐ":"gu","げ":"ge","ご":"go",
        "ざ":"za","じ":"ji","ず":"zu","ぜ":"ze","ぞ":"zo",
        "だ":"da","ぢ":"ji","づ":"zu","で":"de","ど":"do",
        "ば":"ba","び":"bi","ぶ":"bu","べ":"be","ぼ":"bo",
        "ぱ":"pa","ぴ":"pi","ぷ":"pu","ぺ":"pe","ぽ":"po",
        "きゃ":"kya","きゅ":"kyu","きょ":"kyo",
        "しゃ":"sha","しゅ":"shu","しょ":"sho",
        "ちゃ":"cha","ちゅ":"chu","ちょ":"cho",
        "にゃ":"nya","にゅ":"nyu","にょ":"nyo",
        "ひゃ":"hya","ひゅ":"hyu","ひょ":"hyo",
        "みゃ":"mya","みゅ":"myu","みょ":"myo",
        "りゃ":"rya","りゅ":"ryu","りょ":"ryo",
        "ぎゃ":"gya","ぎゅ":"gyu","ぎょ":"gyo",
        "じゃ":"ja","じゅ":"ju","じょ":"jo",
        "びゃ":"bya","びゅ":"byu","びょ":"byo",
        "ぴゃ":"pya","ぴゅ":"pyu","ぴょ":"pyo",
        "ア":"a","イ":"i","ウ":"u","エ":"e","オ":"o",
        "カ":"ka","キ":"ki","ク":"ku","ケ":"ke","コ":"ko",
        "サ":"sa","シ":"shi","ス":"su","セ":"se","ソ":"so",
        "タ":"ta","チ":"chi","ツ":"tsu","テ":"te","ト":"to",
        "ナ":"na","ニ":"ni","ヌ":"nu","ネ":"ne","ノ":"no",
        "ハ":"ha","ヒ":"hi","フ":"fu","ヘ":"he","ホ":"ho",
        "マ":"ma","ミ":"mi","ム":"mu","メ":"me","モ":"mo",
        "ヤ":"ya","ユ":"yu","ヨ":"yo",
        "ラ":"ra","リ":"ri","ル":"ru","レ":"re","ロ":"ro",
        "ワ":"wa","ヰ":"wi","ヱ":"we","ヲ":"wo","ン":"n",
        "ガ":"ga","ギ":"gi","グ":"gu","ゲ":"ge","ゴ":"go",
        "ザ":"za","ジ":"ji","ズ":"zu","ゼ":"ze","ぞ":"zo",
        "ダ":"da","ヂ":"ji","ヅ":"zu","デ":"de","ド":"do",
        "バ":"ba","ビ":"bi","ブ":"bu","ベ":"be","ボ":"bo",
        "パ":"pa","ピ":"pi","プ":"pu","ペ":"pe","ポ":"po",
        "キャ":"kya","キュ":"kyu","キョ":"kyo",
        "シャ":"sha","シュ":"shu","ショ":"sho",
        "チャ":"cha","チュ":"chu","チョ":"cho",
        "ニャ":"nya","ニュ":"nyu","ニョ":"nyo",
        "ヒャ":"hya","ヒュ":"hyu","ヒョ":"hyo",
        "ミャ":"mya","ミュ":"myu","ミョ":"myo",
        "リャ":"rya","リュ":"ryu","リョ":"ryo",
        "ギャ":"gya","ギュ":"gyu","ギョ":"gyo",
        "ジャ":"ja","ジュ":"ju","ジョ":"jo",
        "ビャ":"bya","ビュ":"byu","ビョ":"byo",
        "ピャ":"pya","ピュ":"pyu","ピョ":"pyo",
        "ショク":"shoku","ショ":"sho","シュ":"shu","ジョ":"jo","ジョウ":"jou"
    };

    let result = "";
    let i = 0;
    while (i < kana.length) {
        if (kana[i] === "っ" || kana[i] === "ッ") {
            const nextTwo = kana.substr(i + 1, 2);
            const nextOne = kana.substr(i + 1, 1);
            const nextRomaji = kanaMap[nextTwo] || kanaMap[nextOne] || "";
            if (nextRomaji) result += nextRomaji[0];
            i++;
            continue;
        }
        if (kana[i] === "ー") {
            const lastChar = result.slice(-1);
            result += lastChar || "-";
            i++;
            continue;
        }
        const two = kana.substr(i, 2);
        if (kanaMap[two]) {
            result += kanaMap[two];
            i += 2;
            continue;
        }
        const one = kana[i];
        if (kanaMap[one]) {
            result += kanaMap[one];
            i++;
            continue;
        }
        result += one;
        i++;
    }
    return result;
}
window.kanaToRomaji = kanaToRomaji;

/**
 * Memformat array bacaan kana (Onyomi / Kunyomi) menjadi format: Kana (romaji)
 * Contoh: "ハン (han) / なか.ば (naka.ba)"
 * 
 * @param {Array<string>} readings - Daftar bacaan kana
 * @returns {string} - String bacaan terformat
 */
function formatKanaReadings(readings) {
    if (!readings || !Array.isArray(readings) || readings.length === 0) return "—";
    return readings.map((r) => {
        const romaji = kanaToRomaji(r);
        return romaji ? `${r} (${romaji})` : r;
    }).join(" / ");
}
window.formatKanaReadings = formatKanaReadings;

/**
 * Memformat satu item kosakata terkait ke dalam markup HTML
 * Format: <li><b>[Kanji]</b> <span>[Kana] ([Romaji])</span> — [Arti Bahasa Indonesia]</li>
 * Contoh: <li><b>日本</b> <span>にほん (nihon)</span> — Jepang</li>
 * 
 * @param {Object} w - Objek kata ({ word, reading, meaning })
 * @returns {string} - String HTML untuk tag <li>
 */
function formatWordItem(w) {
    const romaji = kanaToRomaji(w.reading);
    const readingText = romaji ? `${w.reading} (${romaji})` : w.reading;
    return `<li><b>${w.word}</b> <span>${readingText}</span> — ${w.meaning}</li>`;
}
window.formatWordItem = formatWordItem;

/**
 * Menerjemahkan teks bahasa Inggris ke bahasa Indonesia menggunakan:
 * 1. Cache lokal (localStorage)
 * 2. Kamus kamus statis offline (MiraiTranslator)
 * 3. Layanan gratis MyMemory API (lazy fetch saat kanji diklik)
 * 
 * @param {string} text - Teks bahasa Inggris yang akan diterjemahkan
 * @returns {Promise<string>} - Hasil terjemahan dalam bahasa Indonesia
 */
async function translateToIndonesian(text) {
    if (!text || typeof text !== "string") return "";
    const raw = text.trim();
    if (!raw) return "";

    const cacheKey = `mnh_trans_${raw.toLowerCase()}`;
    try {
        const cached = localStorage.getItem(cacheKey);
        if (cached) return cached;
    } catch (e) {}

    // 1. Cek kamus offline jika kata tunggal tersedia
    if (window.MiraiTranslator?.dictionary) {
        const direct = window.MiraiTranslator.dictionary[raw.toLowerCase()];
        if (direct) {
            try { localStorage.setItem(cacheKey, direct); } catch (e) {}
            return direct;
        }
    }

    // 2. Fetch MyMemory API agar seluruh teks diterjemahkan ke Bahasa Indonesia
    try {
        const res = await fetch(`https://api.mymemory.translated.net/get?q=${encodeURIComponent(raw)}&langpair=en|id`);
        if (res.ok) {
            const data = await res.json();
            const trans = data?.responseData?.translatedText;
            if (trans && typeof trans === "string" && trans.toLowerCase() !== raw.toLowerCase()) {
                const cleaned = trans
                    .replace(/&#39;/g, "'")
                    .replace(/&quot;/g, '"')
                    .replace(/&amp;/g, '&')
                    .replace(/&lt;/g, '<')
                    .replace(/&gt;/g, '>')
                    .trim()
                    .toLowerCase();
                try {
                    localStorage.setItem(cacheKey, cleaned);
                } catch (e) {}
                return cleaned;
            }
        }
    } catch (err) {
        console.warn("Penerjemahan MyMemory fallback gagal:", err);
    }

    // 3. Fallback kamus sinkron
    if (window.MiraiTranslator?.translateSync) {
        const fallback = window.MiraiTranslator.translateSync(raw);
        if (fallback && fallback.toLowerCase() !== raw.toLowerCase()) {
            return fallback;
        }
    }

    return raw;
}
window.translateToIndonesian = translateToIndonesian;

/**
 * Mengurutkan array kanji secara Ascending:
 * 1. Jumlah goresan (strokes / stroke_count) dari yang terkecil ke terbesar
 * 2. Tingkat pendidikan (grade) dari terkecil ke terbesar jika jumlah goresan sama
 * 3. Urutan karakter alfabetis / Unicode sebagai penentu kestabilan
 * 
 * @param {Array<Object>} list - Daftar objek entri kanji
 * @returns {Array<Object>} - Salinan daftar yang telah diurutkan
 */
function sortKanjiEntries(list) {
    return list.slice().sort((a, b) => {
        const strokesA = Number(a.strokes || 0);
        const strokesB = Number(b.strokes || 0);
        if (strokesA !== strokesB) return strokesA - strokesB;

        const gradeA = Number(a.grade !== undefined ? a.grade : 99);
        const gradeB = Number(b.grade !== undefined ? b.grade : 99);
        if (gradeA !== gradeB) return gradeA - gradeB;

        return a.kanji.localeCompare(b.kanji);
    });
}
window.sortKanjiEntries = sortKanjiEntries;

/**
 * Inisialisasi Kamus Kanji & Kana
 * Mengontrol seluruh lifecycle interaksi: muat data JLPT, render grid terurut,
 * panel detail kanan, pencarian multi-kriteria, dan tab Kana.
 */
window.initKanjiDictionary = async function initKanjiDictionary() {
    const dictionary = document.querySelector("[data-kanji-dictionary]");
    if (!dictionary) return;

    // Seleksi elemen DOM utama
    const grid = dictionary.querySelector("[data-kanji-grid]");
    const count = dictionary.querySelector("[data-kanji-count]");
    const empty = dictionary.querySelector("[data-kanji-empty]");
    const detail = dictionary.querySelector("[data-kanji-detail]");
    const search = dictionary.querySelector("[data-kanji-search]");
    const jlpt = dictionary.querySelector("[data-kanji-jlpt]");
    const level = dictionary.querySelector("[data-kanji-level]");
    let strokes = dictionary.querySelector("[data-kanji-strokes]");
    
    // State penyimpanan memori
    const entryMap = new Map();
    let entries = [];
    let player;
    let currentRenderLimit = 72;
    let selectedKanjiChar = null;

    // Buat dropdown pilihan jumlah goresan jika belum ada di HTML
    if (!strokes) {
        const label = document.createElement("label");
        let strokeOptions = '<option value="">Semua</option>';
        for (let i = 1; i <= 29; i++) {
            strokeOptions += `<option value="${i}">${i}</option>`;
        }
        label.innerHTML = `Goresan<select data-kanji-strokes>${strokeOptions}</select>`;
        dictionary.querySelector(".dictionary-controls").append(label);
        strokes = label.querySelector("select");
    }

    // Tambahkan tombol kanji acak jika belum ada
    if (!dictionary.querySelector("[data-random-kanji]")) {
        const random = document.createElement("button");
        random.className = "btn";
        random.type = "button";
        random.dataset.randomKanji = "";
        random.textContent = "KANJI ACAK";
        dictionary.querySelector(".dictionary-controls").append(random);
    }

    /**
     * Memetakan angka level JLPT ke sebutan tingkat belajar Bahasa Indonesia
     */
    function getLevelName(jlptNum) {
        if (jlptNum === 5) return "Dasar";
        if (jlptNum === 4 || jlptNum === 3) return "Menengah";
        return "Lanjutan";
    }

    /**
     * Mengambil dan mendaftarkan karakter kanji untuk level JLPT tertentu.
     * Menggunakan metadata goresan dan grade dari data/kanji-meta.json secara langsung.
     * 
     * @param {number} levelNum - Level JLPT (1 s/d 5)
     */
    async function loadJlptList(levelNum) {
        const [charList, meta] = await Promise.all([
            KanjiAPI.getJlptList(levelNum),
            ensureKanjiMeta()
        ]);
        const levelName = getLevelName(levelNum);
        let addedNew = false;

        charList.forEach((char) => {
            if (!entryMap.has(char)) {
                // Cek cache detail di localStorage
                let cachedDetail = null;
                try {
                    const raw = localStorage.getItem(`mnh_kapi_detail_${char}`);
                    if (raw) cachedDetail = JSON.parse(raw);
                } catch (e) {}

                const metaInfo = meta[char] || [];
                const strokeCount = (cachedDetail && cachedDetail.stroke_count) || metaInfo[0] || 0;
                const gradeVal = (cachedDetail && cachedDetail.grade !== undefined) ? cachedDetail.grade : (metaInfo[1] !== undefined ? metaInfo[1] : 99);

                if (cachedDetail) {
                    const rawEng = cachedDetail.meanings?.slice(0, 3).join(", ") || "";
                    let cachedIndo = "";
                    try {
                        cachedIndo = localStorage.getItem(`mnh_trans_${rawEng.toLowerCase()}`);
                    } catch (e) {}
                    const isTranslated = Boolean(cachedIndo && cachedIndo.toLowerCase() !== rawEng.toLowerCase());
                    entryMap.set(char, {
                        kanji: char,
                        meaning: isTranslated ? cachedIndo : "Karakter kanji",
                        meaningEn: rawEng,
                        onyomi: cachedDetail.on_readings || [],
                        kunyomi: cachedDetail.kun_readings || [],
                        jlpt: `N${levelNum}`,
                        level: levelName,
                        strokes: strokeCount,
                        grade: gradeVal,
                        words: [],
                        sentence: { japanese: char, reading: "", meaning: "" },
                        _needsDetail: false,
                        _translated: isTranslated
                    });
                } else {
                    entryMap.set(char, {
                        kanji: char,
                        meaning: "Karakter kanji",
                        meaningEn: "",
                        onyomi: [],
                        kunyomi: [],
                        jlpt: `N${levelNum}`,
                        level: levelName,
                        strokes: strokeCount,
                        grade: gradeVal,
                        words: [],
                        sentence: { japanese: char, reading: "", meaning: "" },
                        _needsDetail: true,
                        _translated: false
                    });
                }
                addedNew = true;
            }
        });

        if (addedNew) {
            entries = Array.from(entryMap.values());
            render();
        }
    }

    /**
     * Memuat data kanji dari N5 ke N1 secara berurutan,
     * serta menyediakan cadangan offline dari data/kanji.json jika jaringan bermasalah.
     */
    async function loadAllJlpt() {
        // Muat N5 terlebih dahulu agar UI segera muncul, lalu N4 sampai N1
        for (const lvl of [5, 4, 3, 2, 1]) {
            await loadJlptList(lvl);
        }

        // Cadangan offline bila data KanjiAPI gagal dimuat sama sekali
        if (entryMap.size === 0) {
            try {
                const res = await fetch("data/kanji.json");
                if (res.ok) {
                    const localData = await res.json();
                    const meta = await ensureKanjiMeta();
                    localData.forEach((item) => {
                        const metaInfo = meta[item.kanji] || [];
                        entryMap.set(item.kanji, {
                            ...item,
                            jlpt: item.jlpt || "N5",
                            level: item.level || "Dasar",
                            strokes: item.strokes || metaInfo[0] || 0,
                            grade: item.grade || metaInfo[1] || 99,
                            _needsDetail: false,
                            _translated: true
                        });
                    });
                    entries = Array.from(entryMap.values());
                    render();
                }
            } catch (e) {}
        }
    }
    loadAllJlpt();

    /**
     * Menampilkan detail lengkap kanji pada panel samping (kanan):
     * - Arti utama (Bahasa Indonesia murni setelah translasi)
     * - Label Onyomi (Cara baca China) & Kunyomi (Cara baca Jepang) beserta Romaji
     * - Animasi urutan penulisan KanjiVG
     * - Kosakata terkait dengan format: [Kanji] [Kana] ([Romaji]) — [Arti Bahasa Indonesia]
     * 
     * @param {Object} item - Objek kanji yang dipilih pengguna
     */
    async function renderDetail(item) {
        player?.destroy();
        selectedKanjiChar = item.kanji;

        // Berikan sorotan visual (active state) pada kartu yang dipilih di grid
        grid.querySelectorAll(".kanji-card").forEach((card) => {
            card.classList.toggle("is-active", card.dataset.kanji === item.kanji);
        });

        const strokeCountDisplay = item.strokes || window.MIRAI_STROKE_DATA?.[item.kanji]?.paths?.length || "—";
        const initialMeaning = item._translated
            ? item.meaning
            : '<span style="font-size:0.85em; opacity:0.75; font-weight:normal; font-style:italic;">Menerjemahkan arti ke Bahasa Indonesia...</span>';

        // Render struktur panel detail dengan label bahasa Indonesia
        detail.innerHTML = `
            <div class="kanji-detail-head">
                <strong>${item.kanji}</strong>
                <div>
                    <p class="card-number">${item.jlpt} / ${item.level} · <span data-detail-strokes>${strokeCountDisplay}</span> GORESAN</p>
                    <h3 data-detail-meaning>${initialMeaning}</h3>
                    <p>
                        <b>Onyomi (Cara baca China):</b> <span data-detail-onyomi>${formatKanaReadings(item.onyomi)}</span><br>
                        <b>Kunyomi (Cara baca Jepang):</b> <span data-detail-kunyomi>${formatKanaReadings(item.kunyomi)}</span>
                    </p>
                </div>
            </div>
            <h4>Urutan Menulis (KanjiVG)</h4>
            <div data-stroke-player></div>
            <h4>Kosakata Terkait</h4>
            <ul data-detail-words>${item.words?.length ? item.words.map(formatWordItem).join("") : '<li><em style="color:var(--muted)">Memuat kosakata...</em></li>'}</ul>
            <h4>Contoh Kalimat / Catatan</h4>
            <p class="sentence" data-detail-sentence>
                <b>${item.sentence?.japanese || item.kanji}</b><br>
                <span>${item.sentence?.reading || ""}</span><br>
                ${item.sentence?.meaning || `Data resmi dari KanjiAPI.dev (JLPT ${item.jlpt})`}
            </p>
        `;

        // Jalankan player animasi goresan
        player = window.createStrokePlayer(detail.querySelector("[data-stroke-player]"), item.kanji, item.strokes || 4);
        window.updateQuickStrokeArrow?.();

        // Ambil detail dan kosakata secara lazy HANYA saat kanji diklik
        const needsDetail = item._needsDetail;
        const needsWords = !item.words?.length;

        let detailData = null;
        let wordData = null;

        if (needsDetail || needsWords) {
            [detailData, wordData] = await Promise.all([
                needsDetail ? KanjiAPI.getKanjiDetail(item.kanji) : null,
                needsWords ? KanjiAPI.getKanjiWords(item.kanji) : Promise.resolve(item.words)
            ]);
        }

        // Cegah race condition jika pengguna berpindah ke kanji lain saat fetch sedang berlangsung
        if (selectedKanjiChar !== item.kanji) return;

        // Perbarui atribut kanji jika detail baru diambil dari API
        if (detailData) {
            item.meaningEn = detailData.meanings?.slice(0, 3).join(", ") || "";
            item.onyomi = detailData.on_readings || [];
            item.kunyomi = detailData.kun_readings || [];
            if (detailData.stroke_count) item.strokes = detailData.stroke_count;
            if (detailData.grade !== undefined) item.grade = detailData.grade;
            item._needsDetail = false;

            const sEl = detail.querySelector("[data-detail-strokes]");
            if (sEl) sEl.textContent = item.strokes;
            const onEl = detail.querySelector("[data-detail-onyomi]");
            if (onEl) onEl.textContent = formatKanaReadings(item.onyomi);
            const kunEl = detail.querySelector("[data-detail-kunyomi]");
            if (kunEl) kunEl.textContent = formatKanaReadings(item.kunyomi);
        }

        // Tampilkan daftar kosakata awal
        if (wordData && wordData.length > 0) {
            item.words = wordData;
            const wordsEl = detail.querySelector("[data-detail-words]");
            if (wordsEl && selectedKanjiChar === item.kanji) {
                wordsEl.innerHTML = item.words.map(formatWordItem).join("");
            }
        } else if (item.words?.length === 0) {
            const wordsEl = detail.querySelector("[data-detail-words]");
            if (wordsEl && selectedKanjiChar === item.kanji) {
                wordsEl.innerHTML = '<li><em style="color:var(--muted)">Belum ada kosakata tambahan.</em></li>';
            }
        }

        // Terjemahkan arti kosakata dari Inggris ke Indonesia secara lazy
        if (item.words?.length > 0) {
            const wordsToTranslate = item.words.filter((w) => !w._translated && (w.rawMeaning || w.meaning));
            if (wordsToTranslate.length > 0) {
                Promise.all(wordsToTranslate.map(async (w) => {
                    const src = w.rawMeaning || w.meaning;
                    const indo = await translateToIndonesian(src);
                    if (indo && indo.toLowerCase() !== src.toLowerCase()) {
                        w.meaning = indo;
                        w._translated = true;
                    }
                })).then(() => {
                    try {
                        localStorage.setItem(`mnh_kapi_words_${item.kanji}`, JSON.stringify(item.words));
                    } catch (e) {}

                    // Render ulang daftar kata jika panel masih aktif pada karakter ini
                    if (selectedKanjiChar === item.kanji) {
                        const wordsElUpdated = detail.querySelector("[data-detail-words]");
                        if (wordsElUpdated) {
                            wordsElUpdated.innerHTML = item.words.map(formatWordItem).join("");
                        }
                    }
                });
            }
        }

        // Terjemahkan arti kanji utama (Inggris -> Indonesia) secara lazy
        if (!item._translated) {
            const englishText = item.meaningEn || (!item._translated && item.meaning !== "Karakter kanji" && item.meaning !== "Memuat arti..." ? item.meaning : "");
            if (englishText) {
                const indonesianMeaning = await translateToIndonesian(englishText);
                if (indonesianMeaning) {
                    // TIMPA (replace) teks sepenuhnya dengan hasil bahasa Indonesia murni
                    item.meaning = indonesianMeaning;
                    item._translated = true;
                }
            }
        }

        // Tampilkan arti bahasa Indonesia pada panel detail dan perbarui kartu di grid
        if (selectedKanjiChar === item.kanji) {
            const mEl = detail.querySelector("[data-detail-meaning]");
            if (mEl) {
                mEl.textContent = item.meaning;
            }
        }

        const cardSpan = grid.querySelector(`[data-kanji="${item.kanji}"] span`);
        if (cardSpan) {
            cardSpan.textContent = item.meaning;
        }
    }

    /**
     * Memfilter daftar kanji berdasarkan kata kunci pencarian, level JLPT, kelompok level,
     * serta jumlah goresan, lalu mengembalikan entri yang TERURUT ASCENDING berdasarkan goresan & grade.
     * 
     * @returns {Array<Object>} - Daftar entri kanji yang lolos filter dan sudah terurut
     */
    function visibleEntries() {
        const query = search.value.trim().toLowerCase();
        const filtered = entries.filter((item) => {
            const onyomiRomaji = item.onyomi.map(kanaToRomaji).join(" ");
            const kunyomiRomaji = item.kunyomi.map(kanaToRomaji).join(" ");
            const searchable = [
                item.kanji,
                item.meaning,
                item.meaningEn || "",
                ...item.onyomi,
                onyomiRomaji,
                ...item.kunyomi,
                kunyomiRomaji,
                ...item.words.flatMap((word) => [word.word, word.reading, word.meaning])
            ].join(" ").toLowerCase();

            const strokeCount = item.strokes || window.MIRAI_STROKE_DATA?.[item.kanji]?.paths?.length || 0;
            const matchesQuery = !query || searchable.includes(query) || item.kanji === query;
            const matchesJlpt = !jlpt.value || item.jlpt === jlpt.value;
            const matchesLevel = !level.value || item.level === level.value;
            const matchesStrokes = !strokes?.value || strokeCount === Number(strokes.value);

            return matchesQuery && matchesJlpt && matchesLevel && matchesStrokes;
        });

        // Wajib diurutkan: Goresan (strokes) Ascending -> Grade Ascending -> Karakter
        return sortKanjiEntries(filtered);
    }

    /**
     * Merender kartu kanji ke dalam grid HTML dengan paginasi / limit tampilan dinamis.
     * Menggunakan satu loop / komponen seragam untuk semua level N5-N1.
     */
    function render() {
        const visible = visibleEntries();
        grid.replaceChildren();
        count.textContent = `Menampilkan ${visible.length} kanji (N5–N1)`;
        empty.hidden = visible.length > 0;

        const sliced = visible.slice(0, currentRenderLimit);
        sliced.forEach((item) => {
            const button = document.createElement("button");
            button.type = "button";
            button.className = "kanji-card";
            button.dataset.kanji = item.kanji;
            if (item.kanji === selectedKanjiChar) {
                button.classList.add("is-active");
            }
            button.innerHTML = `<strong>${item.kanji}</strong><span>${item.meaning}</span><em>${item.jlpt}</em>`;
            button.addEventListener("click", () => renderDetail(item));
            grid.append(button);
        });

        // Tombol Muat Lebih Banyak jika data melebihi limit tampilan saat ini
        if (visible.length > currentRenderLimit) {
            const loadMoreWrap = document.createElement("div");
            loadMoreWrap.style.gridColumn = "1 / -1";
            loadMoreWrap.style.textAlign = "center";
            loadMoreWrap.style.padding = "16px 0";

            const loadMoreBtn = document.createElement("button");
            loadMoreBtn.className = "btn";
            loadMoreBtn.type = "button";
            const remaining = visible.length - currentRenderLimit;
            loadMoreBtn.textContent = `Tampilkan Lebih Banyak (+${Math.min(remaining, 72)} dari ${remaining} tersisa)`;
            loadMoreBtn.addEventListener("click", () => {
                currentRenderLimit += 72;
                render();
            });
            loadMoreWrap.append(loadMoreBtn);
            grid.append(loadMoreWrap);
        }

        // Tampilkan detail otomatis untuk kartu pertama atau pertahankan kartu yang sedang dipilih
        if (visible.length) {
            const isSelectedVisible = visible.some((item) => item.kanji === selectedKanjiChar);
            if (!selectedKanjiChar || !isSelectedVisible) {
                renderDetail(visible[0]);
            }
        } else {
            detail.innerHTML = "<p>Pilih pencarian atau filter lain untuk melihat detail karakter.</p>";
        }
    }

    // Pasang event listener untuk input pencarian dan filter kontrol
    [search, jlpt, level, strokes].filter(Boolean).forEach((control) => {
        control.addEventListener("input", () => {
            currentRenderLimit = 72;
            render();
        });
        control.addEventListener("change", () => {
            currentRenderLimit = 72;
            render();
        });
    });

    // Pasang tombol kanji acak
    dictionary.querySelector("[data-random-kanji]")?.addEventListener("click", () => {
        const visible = visibleEntries();
        if (visible.length) {
            const randomIndex = Math.floor(Math.random() * visible.length);
            renderDetail(visible[randomIndex]);
        }
    });

    // Render grid awal dan inisialisasi tab Kana
    render();
    setupTabs();
    setupQuickStrokeButton();
};

/**
 * Mengatur tab beralih antara Hiragana, Katakana, dan Kanji
 */
function setupTabs() {
    const practiceLink = document.querySelector(".dictionary-practice-link a");
    const urlParams = new URLSearchParams(window.location.search);
    const hash = window.location.hash.replace("#", "").toLowerCase();
    const requestedTab = (urlParams.get("tab") || hash || "").toLowerCase();

    const switchTab = (mode) => {
        const tab = document.querySelector(`[data-script-tab="${mode}"]`);
        if (!tab) return;
        if (practiceLink) practiceLink.href = mode === "katakana" ? "latihan.html?script=katakana" : "latihan.html?script=hiragana";
        document.querySelectorAll("[data-script-tab]").forEach((button) => {
            const active = button === tab;
            button.classList.toggle("is-active", active);
            button.setAttribute("aria-selected", String(active));
        });
        document.querySelectorAll("[data-script-panel]").forEach((panel) => {
            panel.hidden = panel.dataset.scriptPanel !== mode;
        });
        if (mode !== "kanji") renderKanaPanel(mode);
        window.updateQuickStrokeArrow?.();
    };

    document.querySelectorAll("[data-script-tab]").forEach((tab) => {
        tab.addEventListener("click", () => {
            switchTab(tab.dataset.scriptTab);
        });
    });

    if (requestedTab && document.querySelector(`[data-script-tab="${requestedTab}"]`)) {
        switchTab(requestedTab);
    } else {
        const activeTab = document.querySelector("[data-script-tab].is-active");
        if (activeTab && activeTab.dataset.scriptTab !== "kanji") {
            renderKanaPanel(activeTab.dataset.scriptTab);
        }
    }
}

/**
 * Merender panel interaktif Hiragana atau Katakana dengan kategori huruf,
 * pencarian, dan animasi urutan menulis.
 * 
 * @param {string} mode - "hiragana" atau "katakana"
 */
function renderKanaPanel(mode) {
    const panel = document.querySelector(`[data-script-panel="${mode}"]`);
    if (!panel || panel.dataset.ready) return;
    panel.dataset.ready = "true";
    const categories = window.KanaData.categoriesConfig;
    let player;
    let selectedChar = null;

    panel.innerHTML = `
        <div class="dictionary-controls">
            <label>Cari<input type="search" data-kana-search placeholder="Contoh: ${mode === 'katakana' ? 'ア, a, anime' : 'あ, a, cinta'}"></label>
            <label>Kategori<select data-kana-type>
                <option value="">Semua Kategori</option>
                <option value="basic">1. Huruf Dasar (46)</option>
                <option value="dakuten">2. Dakuten (20)</option>
                <option value="handakuten">3. Handakuten (5)</option>
                <option value="yoon">4. Yōon Gabungan (33)</option>
            </select></label>
            <button class="btn" type="button" data-random-kana>ACAK</button>
        </div>
        <p class="result-count" data-kana-count></p>
        <div class="dictionary-layout">
            <div class="kana-categorized-wrap" data-kana-grid-live style="display:flex; flex-direction:column; gap:28px;"></div>
            <aside class="kana-detail" data-kana-detail-live><p>Pilih satu karakter untuk melihat detail dan urutan goresan.</p></aside>
        </div>
    `;

    const container = panel.querySelector("[data-kana-grid-live]");
    const search = panel.querySelector("[data-kana-search]");
    const typeFilter = panel.querySelector("[data-kana-type]");
    const count = panel.querySelector("[data-kana-count]");
    const detail = panel.querySelector("[data-kana-detail-live]");

    const toKatakana = (text) => {
        return [...text].map((char) => {
            const code = char.charCodeAt(0);
            return (code >= 0x3041 && code <= 0x3096) ? String.fromCharCode(code + 0x60) : char;
        }).join("");
    };

    const show = (character) => {
        selectedChar = character;
        container.querySelectorAll(".kana-card").forEach((btn) => {
            btn.classList.toggle("is-selected", btn.dataset.character === character);
        });

        const item = window.KanaData.getDetail(character, mode);
        player?.destroy();
        detail.innerHTML = `
            <p class="card-number">${mode.toUpperCase()} / ${item.reading}</p>
            <div class="selected-kana">${character}</div>
            <p><b>Romaji:</b> ${item.reading}</p>
            <p><b>Contoh:</b> <b>${item.example[0]}</b> (<em>${item.example[1]}</em>) — ${item.example[2]}</p>
            <h4>Urutan Menulis</h4>
            <div data-stroke-player></div>
        `;
        player = window.createStrokePlayer(detail.querySelector("[data-stroke-player]"), character, 3, {
            showClear: true
        });
        window.updateQuickStrokeArrow?.();
    };

    const render = () => {
        const query = search.value.trim().toLowerCase();
        const selectedType = typeFilter.value;
        container.replaceChildren();

        let totalVisible = 0;
        let firstButton = null;

        categories.forEach((cat) => {
            if (selectedType && cat.id !== selectedType) {
                return;
            }

            const chars = mode === "katakana" ? cat.hiraChars.map(toKatakana) : cat.hiraChars;
            const filteredChars = chars.filter((character) => {
                const item = window.KanaData.getDetail(character, mode);
                return !query || `${character} ${item.reading} ${item.example.join(" ")}`.toLowerCase().includes(query);
            });

            if (filteredChars.length === 0) {
                return;
            }

            totalVisible += filteredChars.length;

            const section = document.createElement("section");
            section.className = "kana-section-group";

            const header = document.createElement("div");
            header.className = "kana-section-header";

            const titleWrap = document.createElement("div");
            titleWrap.className = "kana-section-title-wrap";

            const title = document.createElement("h3");
            title.className = "kana-section-title";
            title.textContent = cat.title;

            const badge = document.createElement("span");
            badge.className = "kana-section-badge";
            badge.textContent = cat.badge;

            titleWrap.append(title, badge);

            const descCard = document.createElement("div");
            descCard.className = "kana-section-desc-card";

            const desc = document.createElement("p");
            desc.className = "kana-section-desc";
            desc.textContent = cat.description[mode] || cat.description.hiragana;

            descCard.append(desc);
            header.append(titleWrap, descCard);

            const grid = document.createElement("div");
            grid.className = "kana-section-grid";

            filteredChars.forEach((character) => {
                const item = window.KanaData.getDetail(character, mode);
                const button = document.createElement("button");
                button.className = "kana-card";
                button.type = "button";
                button.dataset.character = character;
                if (character === selectedChar) {
                    button.classList.add("is-selected");
                }
                button.innerHTML = `<strong>${character}</strong><span>${item.reading}</span>`;
                button.addEventListener("click", () => show(character));
                grid.append(button);

                if (!firstButton) {
                    firstButton = { button, character };
                }
            });

            section.append(header, grid);
            container.append(section);
        });

        count.textContent = `Menampilkan ${totalVisible} karakter ${mode === 'katakana' ? 'Katakana' : 'Hiragana'}`;

        if (totalVisible === 0) {
            const emptyEl = document.createElement("div");
            emptyEl.className = "kana-empty-state";
            emptyEl.innerHTML = `<p>Tidak ada karakter yang cocok dengan pencarian “${query}”.</p>`;
            container.append(emptyEl);
        } else if (!selectedChar && firstButton) {
            show(firstButton.character);
        }
    };

    search.addEventListener("input", render);
    typeFilter.addEventListener("change", render);
    panel.querySelector("[data-random-kana]").addEventListener("click", () => {
        const allChars = window.KanaData.getCharacters(mode);
        const randomChar = allChars[Math.floor(Math.random() * allChars.length)];
        show(randomChar);
    });

    render();
}

/**
 * Tombol Cepat Mengikuti (Floating Quick Button) Khusus Kamus:
 * Geser langsung ke tampilan animasi live stroke (urutan goresan).
 */
function setupQuickStrokeButton() {
    if (!document.body.classList.contains("page-kamus")) return;

    let btn = document.getElementById("quickStrokeBtn");
    if (!btn) {
        btn = document.createElement("button");
        btn.id = "quickStrokeBtn";
        btn.className = "quick-stroke-btn";
        btn.type = "button";
        btn.setAttribute("aria-label", "Geser ke Live Stroke");
        btn.setAttribute("title", "Geser ke Live Stroke (Urutan Menulis)");
        btn.innerHTML = `
            <span class="quick-stroke-icon">✍️</span>
            <span class="quick-stroke-text">Live Stroke</span>
            <span class="quick-stroke-arrow">↓</span>
        `;
        const toTop = document.querySelector(".to-top");
        if (toTop && toTop.parentNode) {
            toTop.parentNode.insertBefore(btn, toTop);
        } else {
            document.body.appendChild(btn);
        }
    }

    const getActiveLiveStrokeElement = () => {
        const activePanel = document.querySelector('[data-script-panel]:not([hidden])');
        if (!activePanel) {
            return document.querySelector('#stroke-stage, [data-stroke-player], .kana-detail, .kanji-detail');
        }

        const strokeStage = activePanel.querySelector('#stroke-stage')
            || activePanel.querySelector('.stroke-stage')
            || activePanel.querySelector('[data-stroke-player]');
        if (strokeStage) return strokeStage;

        return activePanel.querySelector('.kana-detail, .kanji-detail');
    };

    const arrowEl = btn.querySelector(".quick-stroke-arrow");

    const updateArrow = () => {
        if (!arrowEl) return;
        const target = getActiveLiveStrokeElement();
        if (!target) return;
        const rect = target.getBoundingClientRect();
        const vh = window.innerHeight || document.documentElement.clientHeight;

        if (rect.top > vh * 0.72) {
            arrowEl.textContent = "↓";
        } else if (rect.bottom < vh * 0.28) {
            arrowEl.textContent = "↑";
        } else {
            arrowEl.textContent = "●";
        }
    };

    if (!btn.dataset.initialized) {
        btn.dataset.initialized = "true";
        btn.addEventListener("click", () => {
            const target = getActiveLiveStrokeElement();
            if (!target) return;

            target.scrollIntoView({
                behavior: "smooth",
                block: "center"
            });

            const pulseEl = target.closest(".stroke-stage") 
                || target.querySelector(".stroke-stage") 
                || target.closest(".kana-detail, .kanji-detail") 
                || target;

            pulseEl.classList.remove("stroke-target-pulse");
            void pulseEl.offsetWidth;
            pulseEl.classList.add("stroke-target-pulse");

            setTimeout(updateArrow, 450);
        });

        window.addEventListener("scroll", updateArrow, { passive: true });
        window.addEventListener("resize", updateArrow, { passive: true });
    }

    window.updateQuickStrokeArrow = updateArrow;
    updateArrow();
}

// Inisialisasi otomatis saat dokumen selesai dimuat
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => {
        window.initKanjiDictionary?.();
        setupQuickStrokeButton();
    });
} else {
    window.initKanjiDictionary?.();
    setupQuickStrokeButton();
}
