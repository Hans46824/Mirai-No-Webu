/**
 * File: js/translator.js
 * Fungsi: Mesin Penerjemah 2 Arah (Jepang ⇄ Indonesia), Kamus Leksikal Kanji,
 *         dan Kontroler Virtual Keyboard Dual-Mode (Kana & QWERTY IME).
 * Penggunaan: kamus/index.html dan kamus/kanji.html.
 */

(() => {
    "use strict";

    // =========================================================================
    // 1. KAMUS LEKSIKAL BAHASA INGGRIS -> INDONESIA (Untuk Makna Kanji)
    // =========================================================================
    const dictionary = {
        // Nature & Elements
        "day": "hari, siang", "sun": "matahari", "moon": "bulan", "month": "bulan", "year": "tahun",
        "fire": "api", "water": "air", "tree": "pohon", "wood": "kayu", "gold": "emas", "money": "uang",
        "earth": "tanah, bumi", "ground": "tanah", "soil": "tanah", "stone": "batu", "mountain": "gunung",
        "river": "sungai", "stream": "aliran air", "sea": "laut", "ocean": "samudra", "rain": "hujan",
        "snow": "salju", "wind": "angin", "cloud": "awan", "sky": "langit", "heavens": "surga, langit",
        "flower": "bunga", "blossom": "mekar, bunga", "cherry blossom": "bunga sakura", "grass": "rumput",
        "forest": "hutan", "woods": "hutan kayu", "field": "ladang, lapangan", "rice field": "sawah",
        "rice paddy": "sawah", "spring": "musim semi, mata air", "summer": "musim panas",
        "autumn": "musim gugur", "fall": "musim gugur", "winter": "musim dingin", "season": "musim",
        "nature": "alam", "weather": "cuaca", "thunder": "petir", "lightning": "kilat",

        // People & Relationships
        "person": "orang", "people": "orang-orang", "man": "pria, laki-laki", "male": "laki-laki",
        "woman": "wanita, perempuan", "female": "perempuan", "child": "anak", "children": "anak-anak",
        "boy": "anak laki-laki", "girl": "anak perempuan", "baby": "bayi", "friend": "teman, sahabat",
        "companion": "rekan, teman", "father": "ayah", "mother": "ibu", "parent": "orang tua",
        "parents": "orang tua", "older brother": "kakak laki-laki", "younger brother": "adik laki-laki",
        "older sister": "kakak perempuan", "younger sister": "adik perempuan", "brother": "saudara laki-laki",
        "sister": "saudara perempuan", "family": "keluarga", "ancestor": "leluhur", "generation": "generasi",
        "self": "diri sendiri", "oneself": "diri sendiri", "teacher": "guru", "master": "guru, ahli",
        "student": "murid, siswa", "pupil": "murid", "doctor": "dokter", "physician": "dokter",
        "king": "raja", "emperor": "kaisar", "queen": "ratu", "lord": "tuan, penguasa",
        "human": "manusia", "mankind": "umat manusia", "life": "hidup, kehidupan", "birth": "kelahiran",
        "death": "kematian", "die": "mati, meninggal", "alive": "hidup", "living": "hidup",

        // Body & Mind
        "body": "tubuh, badan", "head": "kepala", "face": "wajah", "eye": "mata", "eyes": "mata",
        "ear": "telinga", "ears": "telinga", "mouth": "mulut", "lip": "bibir", "nose": "hidung",
        "tooth": "gigi", "teeth": "gigi", "tongue": "lidah", "throat": "tenggorokan", "neck": "leher",
        "shoulder": "bahu", "hand": "tangan", "arm": "lengan", "finger": "jari", "foot": "kaki",
        "leg": "kaki", "knee": "lutut", "bone": "tulang", "skin": "kulit", "blood": "darah",
        "heart": "hati, jantung", "mind": "pikiran, hati", "spirit": "semangat, jiwa", "soul": "jiwa",
        "thought": "pikiran", "think": "berpikir", "feel": "merasa", "feeling": "perasaan",
        "emotion": "emosi", "love": "cinta, kasih sayang", "affection": "kasih sayang", "hate": "benci",
        "anger": "kemarahan", "sadness": "kesedihan", "joy": "kegembiraan", "happiness": "kebahagiaan",
        "fear": "ketakutan", "pain": "rasa sakit", "illness": "penyakit", "sickness": "sakit",
        "disease": "penyakit", "health": "kesehatan", "healthy": "sehat", "strength": "kekuatan",
        "power": "kekuatan, daya", "energy": "energi, tenaga", "voice": "suara", "sound": "bunyi, suara",

        // Actions & Verbs
        "eat": "makan", "food": "makanan", "meal": "makanan", "drink": "minum", "beverage": "minuman",
        "see": "melihat", "look": "melihat", "watch": "menonton", "view": "pemandangan, melihat",
        "hear": "mendengar", "listen": "mendengarkan", "speak": "berbicara", "talk": "berbicara",
        "say": "mengatakan", "tell": "menceritakan", "word": "kata", "words": "kata-kata",
        "speech": "pidato, ucapan", "language": "bahasa", "read": "membaca", "write": "menulis",
        "draw": "menggambar", "paint": "melukis", "walk": "berjalan", "run": "berlari",
        "stand": "berdiri", "sit": "duduk", "lie down": "berbaring", "sleep": "tidur",
        "wake up": "bangun", "go": "pergi", "come": "datang", "return": "kembali, pulang",
        "enter": "masuk", "exit": "keluar", "leave": "meninggalkan", "arrive": "tiba, sampai",
        "meet": "bertemu", "meeting": "pertemuan", "gather": "berkumpul", "fly": "terbang",
        "swim": "berenang", "play": "bermain", "sing": "menyanyi", "dance": "menari",
        "study": "belajar", "learn": "mempelajari", "teach": "mengajar", "work": "bekerja, karya",
        "job": "pekerjaan", "profession": "profesi", "buy": "membeli", "sell": "menjual",
        "pay": "membayar", "give": "memberi", "receive": "menerima", "take": "mengambil",
        "hold": "memegang", "carry": "membawa", "put": "meletakkan", "make": "membuat",
        "build": "membangun", "create": "menciptakan", "destroy": "menghancurkan", "break": "merusak",
        "cut": "memotong", "open": "membuka", "close": "menutup", "start": "mulai",
        "begin": "memulai", "end": "berakhir, selesai", "finish": "selesai", "stop": "berhenti",
        "continue": "melanjutkan", "wait": "menunggu", "hurry": "tergesa-gesa", "help": "menolong",
        "save": "menyelamatkan", "win": "menang", "lose": "kalah, kehilangan", "fight": "bertarung",
        "war": "perang", "battle": "pertempuran", "peace": "kedamaian",

        // Objects & Places
        "book": "buku", "letter": "surat, huruf", "character": "karakter, huruf", "paper": "kertas",
        "pen": "pena", "brush": "kuas", "picture": "gambar, foto", "photo": "foto",
        "house": "rumah", "home": "rumah", "room": "kamar, ruangan", "door": "pintu",
        "window": "jendela", "wall": "dinding", "gate": "gerbang", "roof": "atap",
        "building": "gedung, bangunan", "school": "sekolah", "university": "universitas", "college": "perguruan tinggi",
        "hospital": "rumah sakit", "station": "stasiun", "train": "kereta api", "electric train": "kereta listrik",
        "car": "mobil", "automobile": "mobil", "vehicle": "kendaraan", "bicycle": "sepeda",
        "airplane": "pesawat terbang", "ship": "kapal", "boat": "perahu", "road": "jalan",
        "street": "jalan raya", "path": "jalur, jalan kecil", "bridge": "jembatan", "town": "kota kecil",
        "city": "kota", "village": "desa", "country": "negara", "state": "negara bagian",
        "world": "dunia", "society": "masyarakat", "company": "perusahaan", "office": "kantor",
        "store": "toko", "shop": "toko", "market": "pasar", "restaurant": "restoran",
        "temple": "kuil", "shrine": "kuil Shinto", "park": "taman", "garden": "kebun, taman",
        "table": "meja", "chair": "kursi", "bed": "tempat tidur", "clothes": "pakaian",
        "clothing": "pakaian", "shoe": "sepatu", "shoes": "sepatu", "hat": "topi", "bag": "tas",
        "clock": "jam dinding", "watch": "jam tangan", "bell": "lonceng, bel", "mirror": "cermin",
        "box": "kotak", "cup": "cangkir", "plate": "piring", "dish": "hidangan, piring",
        "knife": "pisau", "sword": "pedang", "gun": "senjata, pistol", "bow": "busur",

        // Concepts, Numbers & Time
        "one": "satu", "two": "dua", "three": "tiga", "four": "empat", "five": "lima",
        "six": "enam", "seven": "tujuh", "eight": "delapan", "nine": "sembilan", "ten": "sepuluh",
        "hundred": "seratus", "thousand": "seribu", "ten thousand": "sepuluh ribu", "zero": "nol",
        "half": "setengah, separuh", "all": "semua", "every": "setiap", "many": "banyak",
        "few": "sedikit", "little": "sedikit, kecil", "much": "banyak", "number": "angka, nomor",
        "time": "waktu", "hour": "jam", "minute": "menit", "second": "detik",
        "morning": "pagi", "noon": "siang", "afternoon": "sore", "evening": "malam, petang",
        "night": "malam", "today": "hari ini", "yesterday": "kemarin", "tomorrow": "besok",
        "now": "sekarang", "past": "masa lalu", "future": "masa depan", "ago": "yang lalu",
        "before": "sebelum", "after": "sesudah", "front": "depan", "back": "belakang",
        "right": "kanan", "left": "kiri", "up": "atas", "above": "di atas",
        "down": "bawah", "below": "di bawah", "middle": "tengah", "center": "pusat, tengah",
        "inside": "dalam", "outside": "luar", "side": "samping, sisi", "near": "dekat",
        "far": "jauh", "east": "timur", "west": "barat", "south": "selatan", "north": "utara"
    };

    function cleanEnglish(str) {
        if (!str) return "";
        return str
            .replace(/\([^)]*\)/g, "")
            .replace(/["']/g, "")
            .replace(/\s+/g, " ")
            .trim();
    }

    function translateWordDirect(word) {
        const lower = word.toLowerCase().trim();
        if (dictionary[lower]) return dictionary[lower];
        if (lower.endsWith("s") && dictionary[lower.slice(0, -1)]) {
            return dictionary[lower.slice(0, -1)];
        }
        return null;
    }

    // =========================================================================
    // 2. KAMUS DUA ARAH OFFLINE (JEPANG ⇄ INDONESIA)
    // =========================================================================
    const jaToIdDictionary = {
        // Salam & Ungkapan
        "こんにちは": "Halo / Selamat siang",
        "おはよう": "Selamat pagi",
        "おはようございます": "Selamat pagi (sopan)",
        "こんばんは": "Selamat malam",
        "おやすみ": "Selamat malam / Selamat tidur",
        "おやすみなさい": "Selamat beristirahat (sopan)",
        "さようなら": "Selamat tinggal",
        "じゃあね": "Sampai jumpa nanti",
        "またね": "Sampai jumpa",
        "ありがとう": "Terima kasih",
        "ありがとうございます": "Terima kasih banyak (sopan)",
        "どうもありがとうございます": "Terima kasih banyak sekali",
        "どういたしまして": "Sama-sama",
        "すみません": "Permisi / Maaf",
        "ごめんなさい": "Mohon maaf",
        "はい": "Ya",
        "いいえ": "Tidak / Bukan",
        "いただきます": "Selamat makan",
        "ごちそうさまでした": "Terima kasih atas makanannya",
        "はじめまして": "Senang berkenalan denganmu",
        "よろしくおねがいします": "Mohon bantuannya / Salam kenal",
        "よろしくお願いします": "Mohon bantuannya / Salam kenal",
        "おねがいします": "Tolong / Mohon",
        "お元気ですか": "Apa kabar?",
        "元気です": "Kabar baik",
        "だいじょうぶ": "Tidak apa-apa / Aman",
        "大丈夫": "Tidak apa-apa",

        // Kata Ganti
        "わたし": "Saya / Aku",
        "私": "Saya",
        "ぼく": "Aku (laki-laki)",
        "僕": "Aku (laki-laki)",
        "あなた": "Kamu / Anda",
        "かれ": "Dia (laki-laki)",
        "彼": "Dia (laki-laki)",
        "かのじょ": "Dia (perempuan) / Pacar",
        "彼女": "Dia (perempuan)",
        "わたしたち": "Kami / Kita",
        "私たち": "Kami / Kita",
        "みんな": "Semuanya / Kalian semua",

        // Tunjuk
        "これ": "Ini",
        "それ": "Itu (dekat lawan bicara)",
        "あれ": "Itu (jauh dari keduanya)",
        "どれ": "Yang mana",
        "ここ": "Di sini",
        "そこ": "Di situ",
        "あそこ": "Di sana",
        "どこ": "Di mana",
        "だれ": "Siapa",
        "何": "Apa",
        "なに": "Apa",
        "いつ": "Kapan",
        "どうして": "Kenapa / Mengapa",
        "なぜ": "Mengapa",
        "どう": "Bagaimana",

        // Benda & Tempat
        "ほん": "Buku",
        "本": "Buku",
        "がっこう": "Sekolah",
        "学校": "Sekolah",
        "せんせい": "Guru / Tutor",
        "先生": "Guru",
        "ともだち": "Teman",
        "友達": "Teman",
        "にほん": "Jepang",
        "日本": "Jepang",
        "にほんご": "Bahasa Jepang",
        "日本語": "Bahasa Jepang",
        "インドネシア": "Indonesia",
        "インドネシア語": "Bahasa Indonesia",
        "みず": "Air",
        "水": "Air",
        "ごはん": "Nasi / Makanan",
        "おちゃ": "Teh Jepang",
        "くるま": "Mobil",
        "車": "Mobil",
        "いえ": "Rumah",
        "家": "Rumah",

        // Kata Sifat & Kerja Dasar
        "すき": "Suka",
        "好き": "Suka",
        "だいすき": "Sangat suka",
        "大好き": "Sangat suka",
        "たべる": "Makan",
        "食べる": "Makan",
        "のむ": "Minum",
        "飲む": "Minum",
        "いく": "Pergi",
        "行く": "Pergi",
        "くる": "Datang",
        "来る": "Datang",
        "みる": "Melihat / Menonton",
        "見る": "Melihat",
        "きく": "Mendengar",
        "聞く": "Mendengar",
        "はなす": "Berbicara",
        "話す": "Berbicara",
        "べんきょう": "Belajar",
        "勉強": "Belajar",
        "いい": "Bagus / Baik",
        "わるい": "Buruk",
        "おいしい": "Enak / Lezat",
        "たのしい": "Menyenangkan",
        "かわいい": "Lucu / Imut",
        "すごい": "Hebat / Luar biasa"
    };

    // Kamus Kebalikan Indonesia -> Jepang
    const idToJaDictionary = {
        "halo": "こんにちは (Konnichiwa)",
        "hai": "こんにちは (Konnichiwa)",
        "selamat pagi": "おはようございます (Ohayou gozaimasu)",
        "selamat siang": "こんにちは (Konnichiwa)",
        "selamat malam": "こんばんは (Konbanwa)",
        "selamat tidur": "おやすみなさい (Oyasuminasai)",
        "selamat tinggal": "さようなら (Sayounara)",
        "sampai jumpa": "またね (Mata ne)",
        "terima kasih": "ありがとう (Arigatou)",
        "terima kasih banyak": "ありがとうございます (Arigatou gozaimasu)",
        "sama-sama": "どういたしまして (Douitashimashite)",
        "permisi": "すみません (Sumimasen)",
        "maaf": "ごめんなさい (Gomennasai)",
        "ya": "はい (Hai)",
        "tidak": "いいえ (Iie)",
        "bukan": "いいえ (Iie)",
        "apa kabar": "お元気ですか (Ogenki desu ka?)",
        "kabar baik": "元気です (Genki desu)",
        "tidak apa-apa": "大丈夫です (Daijoubu desu)",
        "senang berkenalan denganmu": "はじめまして (Hajimemashite)",
        "mohon bantuannya": "よろしくお願いします (Yoroshiku onegaishimasu)",
        "saya": "私 (Watashi)",
        "aku": "僕 (Boku) / 私 (Watashi)",
        "kamu": "あなた (Anata)",
        "dia": "彼 (Kare) / 彼女 (Kanojo)",
        "mereka": "彼ら (Karera)",
        "kami": "私たち (Watashitachi)",
        "kita": "私たち (Watashitachi)",
        "ini": "これ (Kore)",
        "itu": "それ (Sore) / あれ (Are)",
        "apa": "何 (Nani / Nan)",
        "siapa": "誰 (Dare)",
        "kapan": "いつ (Itsu)",
        "di mana": "どこ (Doko)",
        "mengapa": "なぜ (Naze) / どうして (Doushite)",
        "bagaimana": "どう (Dou) / いかが (Ikaga)",
        "buku": "本 (Hon)",
        "sekolah": "学校 (Gakkou)",
        "guru": "先生 (Sensei)",
        "teman": "友達 (Tomodachi)",
        "sahabat": "親友 (Shinyuu)",
        "jepang": "日本 (Nihon)",
        "bahasa jepang": "日本語 (Nihongo)",
        "indonesia": "インドネシア (Indoneshia)",
        "bahasa indonesia": "インドネシア語 (Indoneshiago)",
        "air": "水 (Mizu)",
        "makanan": "食べ物 (Tabemono)",
        "minuman": "飲み物 (Nomimono)",
        "rumah": "家 (Ie)",
        "mobil": "車 (Kuruma)",
        "suka": "好き (Suki)",
        "cinta": "愛 (Ai) / 大好き (Daisuki)",
        "makan": "食べる (Taberu)",
        "minum": "飲む (Nomu)",
        "pergi": "行く (Iku)",
        "datang": "来る (Kuru)",
        "melihat": "見る (Miru)",
        "belajar": "勉強する (Benkyou suru)",
        "bagus": "いい (Ii)",
        "enak": "美味しい (Oishii)",
        "hebat": "すごい (Sugoi)",
        "lucu": "可愛い (Kawaii)"
    };

    // =========================================================================
    // 3. TABEL MAPPING ROMAJI KE HIRAGANA (SMART IME)
    // =========================================================================
    const romajiToHiraganaMap = {
        "kya": "きゃ", "kyu": "きゅ", "kyo": "きょ",
        "sha": "しゃ", "shu": "しゅ", "sho": "しょ",
        "cha": "ちゃ", "chu": "ちゅ", "cho": "ちょ",
        "nya": "にゃ", "nyu": "にゅ", "nyo": "にょ",
        "hya": "ひゃ", "hyu": "ひゅ", "hyo": "ひょ",
        "mya": "みゃ", "myu": "みゅ", "myo": "みょ",
        "rya": "りゃ", "ryu": "りゅ", "ryo": "りょ",
        "gya": "ぎゃ", "gyu": "ぎゅ", "gyo": "ぎょ",
        "ja": "じゃ", "ju": "じゅ", "jo": "じょ",
        "bya": "びゃ", "byu": "びゅ", "byo": "びょ",
        "pya": "ぴゃ", "pyu": "ぴゅ", "pyo": "ぴょ",
        "tsu": "つ", "chi": "ち", "shi": "し",

        "ka": "か", "ki": "き", "ku": "く", "ke": "け", "ko": "こ",
        "sa": "さ", "si": "し", "su": "す", "se": "せ", "so": "そ",
        "ta": "た", "ti": "ち", "tu": "つ", "te": "て", "to": "と",
        "na": "な", "ni": "に", "nu": "ぬ", "ne": "ね", "no": "の",
        "ha": "は", "hi": "ひ", "fu": "ふ", "hu": "ふ", "he": "へ", "ho": "ほ",
        "ma": "ま", "mi": "み", "mu": "む", "me": "め", "mo": "も",
        "ya": "や", "yu": "ゆ", "yo": "よ",
        "ra": "ら", "ri": "り", "ru": "る", "re": "れ", "ro": "ろ",
        "wa": "わ", "wo": "を", "nn": "ん", "n'": "ん",

        "ga": "が", "gi": "ぎ", "gu": "ぐ", "ge": "げ", "go": "ご",
        "za": "ざ", "zi": "じ", "zu": "ず", "ze": "ぜ", "zo": "ぞ",
        "da": "だ", "di": "ぢ", "du": "づ", "de": "で", "do": "ど",
        "ba": "ば", "bi": "び", "bu": "ぶ", "be": "べ", "bo": "ぼ",
        "pa": "ぱ", "pi": "ぴ", "pu": "ぷ", "pe": "ぺ", "po": "ぽ",

        "a": "あ", "i": "い", "u": "う", "e": "え", "o": "お",
        "-": "ー"
    };

    /**
     * Mengonversi teks Romaji menjadi Hiragana secara cerdas (mendukung konsonan ganda sokuon 'っ')
     * @param {string} text - Teks romaji
     * @returns {string} - Hasil kana
     */
    function convertRomajiToKana(text) {
        if (!text) return "";
        if (window.wanakana && typeof window.wanakana.toHiragana === "function") {
            try {
                return window.wanakana.toHiragana(text);
            } catch (e) {}
        }

        let out = "";
        let i = 0;
        const len = text.length;
        const lower = text.toLowerCase();

        while (i < len) {
            // Sokuon konsonan ganda (tt -> っt, kk -> っk, dsb.)
            if (i + 1 < len && lower[i] === lower[i + 1] && /[b-df-hj-np-tv-z]/.test(lower[i]) && lower[i] !== "n") {
                out += "っ";
                i++;
                continue;
            }

            // Cek 3 huruf
            if (i + 3 <= len) {
                const sub3 = lower.slice(i, i + 3);
                if (romajiToHiraganaMap[sub3]) {
                    out += romajiToHiraganaMap[sub3];
                    i += 3;
                    continue;
                }
            }

            // Cek 2 huruf
            if (i + 2 <= len) {
                const sub2 = lower.slice(i, i + 2);
                if (romajiToHiraganaMap[sub2]) {
                    out += romajiToHiraganaMap[sub2];
                    i += 2;
                    continue;
                }
            }

            // Cek 1 huruf
            const sub1 = lower.slice(i, i + 1);
            if (romajiToHiraganaMap[sub1]) {
                out += romajiToHiraganaMap[sub1];
                i += 1;
                continue;
            }

            out += text[i];
            i++;
        }
        return out;
    }

    /**
     * Menghasilkan pelafalan Romaji dari teks Kana / Kanji
     */
    function getRomajiReading(text) {
        if (!text) return "";
        if (window.wanakana && typeof window.wanakana.toRomaji === "function") {
            try {
                const rom = window.wanakana.toRomaji(text);
                return rom !== text ? rom : "";
            } catch (e) {}
        }
        return "";
    }

    // =========================================================================
    // 4. API TRANSLASI DUA ARAH (ONLINE + FALLBACK OFFLINE)
    // =========================================================================
    async function fetchMyMemoryTranslation(text, sourceLang, targetLang) {
        const langpair = `${sourceLang}|${targetLang}`;
        const cacheKey = `mnh_bidir_${langpair}_${text.trim().toLowerCase()}`;

        try {
            const cached = localStorage.getItem(cacheKey);
            if (cached) return cached;
        } catch (e) {}

        try {
            const url = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(text.trim())}&langpair=${encodeURIComponent(langpair)}`;
            const res = await fetch(url);
            if (res.ok) {
                const data = await res.json();
                const trans = data?.responseData?.translatedText;
                if (trans && typeof trans === "string" && trans.trim().toLowerCase() !== text.trim().toLowerCase()) {
                    const clean = trans
                        .replace(/&#39;/g, "'")
                        .replace(/&quot;/g, '"')
                        .replace(/&amp;/g, "&")
                        .replace(/&lt;/g, "<")
                        .replace(/&gt;/g, ">")
                        .trim();
                    try {
                        localStorage.setItem(cacheKey, clean);
                    } catch (e) {}
                    return clean;
                }
            }
        } catch (err) {
            console.warn("MyMemory API fetch network error:", err);
        }
        return null;
    }

    /**
     * Menerjemahkan teks dari Jepang -> Indonesia atau Indonesia -> Jepang
     */
    async function translateStudioText(text, direction = "ja-id") {
        const raw = text.trim();
        if (!raw) return { text: "", romaji: "", from: direction };

        const isJaToId = direction === "ja-id";
        const srcLang = isJaToId ? "ja" : "id";
        const tgtLang = isJaToId ? "id" : "ja";

        // 1. Cek kamus lokal instan
        const localDict = isJaToId ? jaToIdDictionary : idToJaDictionary;
        const lowerRaw = raw.toLowerCase();

        if (localDict[raw]) {
            const res = localDict[raw];
            return {
                text: res,
                romaji: !isJaToId ? getRomajiReading(res) : getRomajiReading(raw),
                isLocal: true
            };
        }
        if (localDict[lowerRaw]) {
            const res = localDict[lowerRaw];
            return {
                text: res,
                romaji: !isJaToId ? getRomajiReading(res) : getRomajiReading(raw),
                isLocal: true
            };
        }

        // 2. Cek API online MyMemory
        const online = await fetchMyMemoryTranslation(raw, srcLang, tgtLang);
        if (online) {
            return {
                text: online,
                romaji: isJaToId ? getRomajiReading(raw) : getRomajiReading(online),
                isOnline: true
            };
        }

        // 3. Fallback kamus leksikal per kata jika online gagal
        if (isJaToId) {
            let fallbackResult = raw;
            for (const [k, v] of Object.entries(jaToIdDictionary)) {
                if (fallbackResult.includes(k)) {
                    fallbackResult = fallbackResult.split(k).join(` ${v} `);
                }
            }
            if (fallbackResult !== raw) {
                return {
                    text: fallbackResult.replace(/\s+/g, " ").trim(),
                    romaji: getRomajiReading(raw),
                    isFallback: true
                };
            }
        }

        return {
            text: `(Terjemahan belum tersedia offline untuk: "${raw}")`,
            romaji: isJaToId ? getRomajiReading(raw) : "",
            isNone: true
        };
    }

    // =========================================================================
    // 5. DATA KARAKTER VIRTUAL KEYBOARD
    // =========================================================================
    const KANA_KEYBOARD_LAYOUTS = {
        hiragana: [
            ["あ", "い", "う", "え", "お"],
            ["か", "き", "く", "け", "こ"],
            ["さ", "し", "す", "せ", "そ"],
            ["た", "ち", "つ", "て", "と"],
            ["な", "に", "ぬ", "ね", "の"],
            ["は", "ひ", "ふ", "へ", "ほ"],
            ["ま", "み", "む", "め", "も"],
            ["や", "（ゆ）", "ゆ", "（よ）", "よ"],
            ["ら", "り", "る", "れ", "ろ"],
            ["わ", "を", "ん", "っ", "ー"]
        ],
        katakana: [
            ["ア", "イ", "ウ", "エ", "オ"],
            ["カ", "キ", "ク", "ケ", "コ"],
            ["サ", "シ", "ス", "セ", "ソ"],
            ["タ", "チ", "ツ", "テ", "ト"],
            ["ナ", "ニ", "ヌ", "ネ", "ノ"],
            ["ハ", "ヒ", "フ", "ヘ", "ホ"],
            ["マ", "ミ", "ム", "メ", "モ"],
            ["ヤ", "（ユ）", "ユ", "（ヨ）", "ヨ"],
            ["ラ", "リ", "ル", "レ", "ロ"],
            ["ワ", "ヲ", "ン", "ッ", "ー"]
        ],
        dakuten: [
            ["が", "ぎ", "ぐ", "げ", "ご"],
            ["ざ", "じ", "ず", "ぜ", "ぞ"],
            ["だ", "ぢ", "づ", "で", "ど"],
            ["ば", "び", "ぶ", "べ", "ぼ"],
            ["ぱ", "ぴ", "ぷ", "ぺ", "ぽ"],
            ["ガ", "ギ", "グ", "ゲ", "ゴ"],
            ["ザ", "ジ", "ズ", "ゼ", "ゾ"],
            ["ダ", "ヂ", "ヅ", "デ", "ド"],
            ["バ", "ビ", "ブ", "ベ", "ボ"],
            ["パ", "ピ", "プ", "ペ", "ポ"]
        ],
        yoon: [
            ["きゃ", "きゅ", "きょ", "ぎゃ", "ぎゅ"],
            ["しゃ", "しゅ", "しょ", "じゃ", "じゅ"],
            ["ちゃ", "ちゅ", "ちょ", "びゃ", "びゅ"],
            ["にゃ", "にゅ", "にょ", "ぴゃ", "ぴゅ"],
            ["ひゃ", "ひゅ", "ひょ", "みゃ", "みゅ"],
            ["りゃ", "りゅ", "りょ", "ぎょ", "じょ"],
            ["キャ", "キュ", "キョ", "ギャ", "ギュ"],
            ["シャ", "シュ", "ショ", "ジャ", "ジュ"],
            ["チャ", "チュ", "チョ", "ビャ", "ビュ"],
            ["ニャ", "ニュ", "ニョ", "ピャ", "ピュ"]
        ]
    };

    const QWERTY_ROWS = [
        ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
        ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
        ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
        ["z", "x", "c", "v", "b", "n", "m"]
    ];

    // =========================================================================
    // 6. KONTROLER UTAMA STUDIO TRANSLATOR & VIRTUAL KEYBOARD
    // =========================================================================
    function initStudioTranslator() {
        const studio = document.getElementById("studio-terjemahan");
        if (!studio) return;

        const sourceFlag = document.getElementById("sourceFlag");
        const sourceName = document.getElementById("sourceName");
        const targetFlag = document.getElementById("targetFlag");
        const targetName = document.getElementById("targetName");
        const swapBtn = document.getElementById("swapLangBtn");

        const textarea = document.getElementById("translatorInput");
        const outputEl = document.getElementById("translatorOutput");
        const romajiEl = document.getElementById("translatorRomaji");
        const statusEl = document.getElementById("translationStatus");
        const inputHint = document.getElementById("inputHint");
        const charCount = document.getElementById("inputCharCount");

        const listenInputBtn = document.getElementById("listenInputBtn");
        const listenOutputBtn = document.getElementById("listenOutputBtn");
        const copyInputBtn = document.getElementById("copyInputBtn");
        const copyOutputBtn = document.getElementById("copyOutputBtn");
        const clearInputBtn = document.getElementById("clearInputBtn");
        const toggleKeyboardBtn = document.getElementById("toggleKeyboardBtn");
        const keyboardPanel = document.getElementById("virtualKeyboardPanel");
        const keyboardToggleText = document.getElementById("keyboardToggleText");

        const kbModeKanaBtn = document.getElementById("kbModeKanaBtn");
        const kbModeQwertyBtn = document.getElementById("kbModeQwertyBtn");
        const kanaSubtoggles = document.getElementById("kanaSubtoggles");
        const qwertyImeControl = document.getElementById("qwertyImeControl");
        const autoRomajiImeCheckbox = document.getElementById("autoRomajiImeCheckbox");

        const kbKanaGrid = document.getElementById("kbKanaGrid");
        const kbQwertyGrid = document.getElementById("kbQwertyGrid");
        const kbSpaceBtn = document.getElementById("kbSpaceBtn");
        const kbBackspaceBtn = document.getElementById("kbBackspaceBtn");
        const kbEnterBtn = document.getElementById("kbEnterBtn");
        const kbPunctuation = document.getElementById("kbPunctuation");

        let activeDirection = "ja-id"; // "ja-id" atau "id-ja"
        let activeKbMode = "kana";     // "kana" atau "qwerty"
        let activeKanaSub = "hiragana"; // "hiragana", "katakana", "dakuten", "yoon"
        let translateDebounceTimer = null;

        // --- Sisipkan karakter pada posisi kursor textarea ---
        function insertTextAtCursor(charToInsert) {
            if (!textarea) return;
            const start = textarea.selectionStart;
            const end = textarea.selectionEnd;
            const currentVal = textarea.value;

            textarea.value = currentVal.substring(0, start) + charToInsert + currentVal.substring(end);
            const newPos = start + charToInsert.length;
            textarea.selectionStart = newPos;
            textarea.selectionEnd = newPos;
            textarea.focus();

            triggerInputUpdate();
            window.MiraiSound?.playClickIfIdle();
        }

        // --- Hapus karakter sebelum kursor ---
        function backspaceAtCursor() {
            if (!textarea) return;
            const start = textarea.selectionStart;
            const end = textarea.selectionEnd;
            const currentVal = textarea.value;

            if (start === end) {
                if (start > 0) {
                    textarea.value = currentVal.substring(0, start - 1) + currentVal.substring(end);
                    textarea.selectionStart = start - 1;
                    textarea.selectionEnd = start - 1;
                }
            } else {
                textarea.value = currentVal.substring(0, start) + currentVal.substring(end);
                textarea.selectionStart = start;
                textarea.selectionEnd = start;
            }
            textarea.focus();
            triggerInputUpdate();
            window.MiraiSound?.playClickIfIdle();
        }

        // --- Render Tombol Grid Kana ---
        function renderKanaGrid() {
            if (!kbKanaGrid) return;
            kbKanaGrid.replaceChildren();

            const rows = KANA_KEYBOARD_LAYOUTS[activeKanaSub] || KANA_KEYBOARD_LAYOUTS.hiragana;
            rows.forEach((row) => {
                const rowEl = document.createElement("div");
                rowEl.className = "kb-row";

                row.forEach((char) => {
                    const btn = document.createElement("button");
                    btn.type = "button";
                    btn.className = "kb-key kana-key";

                    if (char.startsWith("（") && char.endsWith("）")) {
                        btn.className += " kb-key-empty";
                        btn.disabled = true;
                        btn.textContent = "";
                    } else {
                        btn.textContent = char;
                        btn.dataset.char = char;
                        btn.addEventListener("click", () => {
                            insertTextAtCursor(char);
                            window.speakText && window.speakText(char, "ja-JP");
                        });
                    }
                    rowEl.append(btn);
                });
                kbKanaGrid.append(rowEl);
            });
        }

        // --- Render Tombol Grid QWERTY ---
        function renderQwertyGrid() {
            if (!kbQwertyGrid) return;
            kbQwertyGrid.replaceChildren();

            QWERTY_ROWS.forEach((row) => {
                const rowEl = document.createElement("div");
                rowEl.className = "kb-row";

                row.forEach((key) => {
                    const btn = document.createElement("button");
                    btn.type = "button";
                    btn.className = "kb-key qwerty-key";
                    btn.textContent = key;
                    btn.dataset.key = key;

                    btn.addEventListener("click", () => {
                        handleQwertyKeyPress(key);
                    });
                    rowEl.append(btn);
                });
                kbQwertyGrid.append(rowEl);
            });
        }

        // --- Handle Ketikan QWERTY (Virtual & Fisik dengan Auto-IME) ---
        function handleQwertyKeyPress(key) {
            const isImeActive = autoRomajiImeCheckbox && autoRomajiImeCheckbox.checked && activeDirection === "ja-id";
            if (!isImeActive) {
                insertTextAtCursor(key);
                return;
            }

            // Jika IME aktif, masukkan huruf dan konversi kata terakhir yang sedang diketik
            insertTextAtCursor(key);
            applyRealtimeImeConversion();
        }

        function applyRealtimeImeConversion() {
            if (!textarea) return;
            const val = textarea.value;
            const cursorPos = textarea.selectionStart;

            // Cari batas kata sebelum kursor
            const beforeCursor = val.slice(0, cursorPos);
            const match = beforeCursor.match(/([a-zA-Z\-']+)$/);
            if (!match) return;

            const romajiWord = match[1];
            const kanaConverted = convertRomajiToKana(romajiWord);

            if (kanaConverted && kanaConverted !== romajiWord) {
                const wordStart = cursorPos - romajiWord.length;
                textarea.value = val.slice(0, wordStart) + kanaConverted + val.slice(cursorPos);
                const newCursor = wordStart + kanaConverted.length;
                textarea.selectionStart = newCursor;
                textarea.selectionEnd = newCursor;
                triggerInputUpdate();
            }
        }

        // --- Update Teks & Trigger Translasi Otomatis ---
        function triggerInputUpdate() {
            const text = textarea.value;
            if (charCount) charCount.textContent = `${text.length} karakter`;

            if (statusEl) statusEl.textContent = "Mengetik...";

            clearTimeout(translateDebounceTimer);
            if (!text.trim()) {
                if (outputEl) {
                    outputEl.textContent = "Hasil terjemahan akan otomatis muncul di sini...";
                    outputEl.classList.add("placeholder");
                }
                if (romajiEl) romajiEl.hidden = true;
                if (statusEl) statusEl.textContent = "Siap menerjemahkan";
                return;
            }

            translateDebounceTimer = setTimeout(async () => {
                if (statusEl) statusEl.textContent = "Menerjemahkan...";
                try {
                    const result = await translateStudioText(text, activeDirection);
                    if (outputEl) {
                        outputEl.textContent = result.text || "";
                        outputEl.classList.remove("placeholder");
                    }
                    if (romajiEl) {
                        if (result.romaji && result.romaji !== result.text) {
                            romajiEl.textContent = `Romaji: ${result.romaji}`;
                            romajiEl.hidden = false;
                        } else {
                            romajiEl.hidden = true;
                        }
                    }
                    if (statusEl) {
                        statusEl.textContent = result.isOnline ? "Terjemahan Online (Live)" : (result.isLocal ? "Kamus Internal (Instan)" : "Selesai diterjemahkan");
                    }
                } catch (e) {
                    if (statusEl) statusEl.textContent = "Gagal menerjemahkan";
                }
            }, 450);
        }

        // --- Event Listener Textarea ---
        textarea.addEventListener("input", (e) => {
            if (autoRomajiImeCheckbox && autoRomajiImeCheckbox.checked && activeDirection === "ja-id") {
                applyRealtimeImeConversion();
            }
            triggerInputUpdate();
        });

        // --- Swap Arah Bahasa ---
        if (swapBtn) {
            swapBtn.addEventListener("click", () => {
                activeDirection = activeDirection === "ja-id" ? "id-ja" : "ja-id";
                const isJa = activeDirection === "ja-id";

                // Update label & flag
                if (sourceFlag) sourceFlag.textContent = isJa ? "🇯🇵" : "🇮🇩";
                if (sourceName) sourceName.textContent = isJa ? "Bahasa Jepang" : "Bahasa Indonesia";
                if (targetFlag) targetFlag.textContent = isJa ? "🇮🇩" : "🇯🇵";
                if (targetName) targetName.textContent = isJa ? "Bahasa Indonesia" : "Bahasa Jepang";

                if (inputHint) {
                    inputHint.textContent = isJa ? "Ketik dalam aksara Jepang atau Romaji" : "Ketik dalam Bahasa Indonesia";
                }
                textarea.placeholder = isJa
                    ? "Ketik atau paste teks Jepang / Romaji di sini... (Contoh: こんにちは, arigatou, 日本)"
                    : "Ketik kalimat Bahasa Indonesia di sini... (Contoh: Selamat pagi, terima kasih, saya belajar)";

                // Tukar isi teks input & output jika output berisi terjemahan valid
                const currentInput = textarea.value;
                const currentOutput = outputEl.classList.contains("placeholder") ? "" : outputEl.textContent;

                if (currentOutput && !currentOutput.startsWith("(Terjemahan belum")) {
                    textarea.value = currentOutput;
                } else if (currentInput) {
                    textarea.value = currentInput;
                }

                // Switch keyboard mode otomatis sesuai bahasa
                if (!isJa) {
                    switchKeyboardMode("qwerty");
                }

                window.MiraiSound?.playClickIfIdle();
                triggerInputUpdate();
            });
        }

        // --- Toggle Keyboard Tampilkan / Sembunyikan ---
        if (toggleKeyboardBtn && keyboardPanel) {
            toggleKeyboardBtn.addEventListener("click", () => {
                const isHidden = keyboardPanel.classList.toggle("is-collapsed");
                toggleKeyboardBtn.setAttribute("aria-expanded", String(!isHidden));
                if (keyboardToggleText) {
                    keyboardToggleText.textContent = isHidden ? "Tampilkan Keyboard" : "Sembunyikan Keyboard";
                }
                window.MiraiSound?.playClickIfIdle();
            });
        }

        // --- Switch Mode Keyboard (Kana vs QWERTY) ---
        function switchKeyboardMode(mode) {
            activeKbMode = mode;
            if (kbModeKanaBtn) kbModeKanaBtn.classList.toggle("is-active", mode === "kana");
            if (kbModeQwertyBtn) kbModeQwertyBtn.classList.toggle("is-active", mode === "qwerty");

            if (kbKanaGrid) kbKanaGrid.hidden = mode !== "kana";
            if (kbQwertyGrid) kbQwertyGrid.hidden = mode !== "qwerty";

            if (kanaSubtoggles) kanaSubtoggles.hidden = mode !== "kana";
            if (qwertyImeControl) qwertyImeControl.hidden = mode !== "qwerty";
        }

        if (kbModeKanaBtn) {
            kbModeKanaBtn.addEventListener("click", () => {
                switchKeyboardMode("kana");
                window.MiraiSound?.playClickIfIdle();
            });
        }
        if (kbModeQwertyBtn) {
            kbModeQwertyBtn.addEventListener("click", () => {
                switchKeyboardMode("qwerty");
                window.MiraiSound?.playClickIfIdle();
            });
        }

        // --- Sub-toggles Kana (Hiragana, Katakana, Dakuten, Yoon) ---
        if (kanaSubtoggles) {
            kanaSubtoggles.querySelectorAll("[data-kana-sub]").forEach((btn) => {
                btn.addEventListener("click", () => {
                    kanaSubtoggles.querySelectorAll("[data-kana-sub]").forEach((b) => b.classList.remove("is-active"));
                    btn.classList.add("is-active");
                    activeKanaSub = btn.dataset.kanaSub;
                    renderKanaGrid();
                    window.MiraiSound?.playClickIfIdle();
                });
            });
        }

        // --- Utility Keys (Space, Backspace, Enter, Punctuation) ---
        if (kbSpaceBtn) {
            kbSpaceBtn.addEventListener("click", () => {
                insertTextAtCursor(activeDirection === "ja-id" ? " " : " ");
            });
        }
        if (kbBackspaceBtn) {
            kbBackspaceBtn.addEventListener("click", () => {
                backspaceAtCursor();
            });
        }
        if (kbEnterBtn) {
            kbEnterBtn.addEventListener("click", () => {
                insertTextAtCursor("\n");
            });
        }
        if (kbPunctuation) {
            kbPunctuation.querySelectorAll("[data-insert]").forEach((btn) => {
                btn.addEventListener("click", () => {
                    insertTextAtCursor(btn.dataset.insert);
                });
            });
        }

        // --- Audio Listen Buttons ---
        if (listenInputBtn) {
            listenInputBtn.addEventListener("click", () => {
                const text = textarea.value.trim();
                if (!text) return;
                const lang = activeDirection === "ja-id" ? "ja-JP" : "id-ID";
                window.speakText(text, lang);
            });
        }

        if (listenOutputBtn) {
            listenOutputBtn.addEventListener("click", () => {
                if (outputEl.classList.contains("placeholder")) return;
                const text = outputEl.textContent.trim();
                if (!text) return;
                const lang = activeDirection === "ja-id" ? "id-ID" : "ja-JP";
                window.speakText(text, lang);
            });
        }

        // --- Copy & Clear Buttons ---
        function copyWithFeedback(text, buttonEl, defaultLabel) {
            if (!text) return;
            navigator.clipboard.writeText(text).then(() => {
                const orig = buttonEl.innerHTML;
                buttonEl.innerHTML = "<span>✓ Tersalin!</span>";
                buttonEl.classList.add("btn-copied");
                setTimeout(() => {
                    buttonEl.innerHTML = orig;
                    buttonEl.classList.remove("btn-copied");
                }, 1800);
            }).catch(() => {
                // Fallback
                const temp = document.createElement("textarea");
                temp.value = text;
                document.body.appendChild(temp);
                temp.select();
                document.execCommand("copy");
                document.body.removeChild(temp);
                alert("Tersalin ke clipboard!");
            });
        }

        if (copyInputBtn) {
            copyInputBtn.addEventListener("click", () => {
                copyWithFeedback(textarea.value, copyInputBtn, "📋 Salin");
            });
        }
        if (copyOutputBtn) {
            copyOutputBtn.addEventListener("click", () => {
                if (outputEl.classList.contains("placeholder")) return;
                copyWithFeedback(outputEl.textContent, copyOutputBtn, "📋 Salin Hasil");
            });
        }
        if (clearInputBtn) {
            clearInputBtn.addEventListener("click", () => {
                textarea.value = "";
                triggerInputUpdate();
                textarea.focus();
                window.MiraiSound?.playClickIfIdle();
            });
        }

        // Inisialisasi awal keyboard grid
        renderKanaGrid();
        renderQwertyGrid();
    }

    // =========================================================================
    // 7. EXPORT GLOBAL TRANSLATOR & INISIALISASI
    // =========================================================================
    window.MiraiTranslator = {
        dictionary,
        jaToIdDictionary,
        idToJaDictionary,
        convertRomajiToKana,
        getRomajiReading,
        translateStudioText,

        translateSync(text) {
            if (!text || typeof text !== "string") return text || "";
            const raw = text.trim();
            if (!raw) return "";

            try {
                const cached = localStorage.getItem(`mnh_trans_${raw.toLowerCase()}`);
                if (cached) return cached;
            } catch (e) {}

            const cleaned = cleanEnglish(raw);
            const direct = translateWordDirect(cleaned) || translateWordDirect(raw);
            if (direct) return direct;

            if (raw.includes(",")) {
                const parts = raw.split(",").map((p) => p.trim()).filter(Boolean);
                const translatedParts = parts.map((p) => {
                    const c = cleanEnglish(p);
                    return translateWordDirect(c) || translateWordDirect(p) || p;
                });
                return [...new Set(translatedParts.flatMap((p) => p.split(",").map((s) => s.trim())))].join(", ");
            }

            return raw;
        },

        async translateText(text) {
            if (!text || typeof text !== "string") return text || "";
            const raw = text.trim();
            if (!raw) return "";

            // 1. Cek cache
            const cacheKey = `mnh_trans_${raw.toLowerCase()}`;
            try {
                const cached = localStorage.getItem(cacheKey);
                if (cached) return cached;
            } catch (e) {}

            // 2. Cek kamus lokal langsung
            const cleaned = cleanEnglish(raw);
            const direct = translateWordDirect(cleaned) || translateWordDirect(raw);
            if (direct) {
                try { localStorage.setItem(cacheKey, direct); } catch (e) {}
                return direct;
            }

            // 3. Online fetch
            try {
                const res = await fetch(`https://api.mymemory.translated.net/get?q=${encodeURIComponent(raw)}&langpair=en|id`);
                if (res.ok) {
                    const data = await res.json();
                    const trans = data?.responseData?.translatedText;
                    if (trans && typeof trans === "string" && trans.toLowerCase() !== raw.toLowerCase()) {
                        const clean = trans.trim().toLowerCase();
                        try { localStorage.setItem(cacheKey, clean); } catch (e) {}
                        return clean;
                    }
                }
            } catch (err) {}

            // 4. Fallback
            const syncResult = this.translateSync(raw);
            if (syncResult && syncResult.toLowerCase() !== raw.toLowerCase()) {
                return syncResult;
            }

            return raw;
        },

        async translateList(items) {
            if (!Array.isArray(items)) return [];
            return Promise.all(items.map((item) => this.translateText(item)));
        }
    };

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initStudioTranslator);
    } else {
        initStudioTranslator();
    }
})();
