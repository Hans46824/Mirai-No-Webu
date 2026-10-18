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

// =========================================================================
// 5. KEITAI 12-KEY KEYBOARD DATA & CYCLING CONFIG
// =========================================================================
const KEITAI_GROUPS = {
  hiragana: {
    a: { main: 'あ', sub: 'あいうえお', chars: ['あ', 'い', 'う', 'え', 'お'] },
    ka: { main: 'か', sub: 'かきくけこ', chars: ['か', 'き', 'く', 'け', 'こ'] },
    sa: { main: 'さ', sub: 'さしすせそ', chars: ['さ', 'し', 'す', 'せ', 'そ'] },
    ta: { main: 'た', sub: 'たちつてと', chars: ['た', 'ち', 'つ', 'て', 'と'] },
    na: { main: 'な', sub: 'なにぬねの', chars: ['な', 'に', 'ぬ', 'ね', 'の'] },
    ha: { main: 'は', sub: 'はひふへほ', chars: ['は', 'ひ', 'ふ', 'へ', 'ほ'] },
    ma: { main: 'ま', sub: 'まみむめも', chars: ['ま', 'み', 'む', 'め', 'も'] },
    ya: { main: 'や', sub: 'やゆよ', chars: ['や', 'ゆ', 'よ'] },
    ra: { main: 'ら', sub: 'らりるれろ', chars: ['ら', 'り', 'る', 'れ', 'ろ'] },
    wa: { main: 'わ', sub: 'わをんー', chars: ['わ', 'を', 'ん', 'ー', '～'] },
    punct: { main: '、。', sub: '、。？！', chars: ['、', '。', '？', '！', '…'] }
  },
  katakana: {
    a: { main: 'ア', sub: 'アイウエオ', chars: ['ア', 'イ', 'ウ', 'エ', 'オ'] },
    ka: { main: 'カ', sub: 'カキクケコ', chars: ['カ', 'キ', 'ク', 'ケ', 'コ'] },
    sa: { main: 'サ', sub: 'サシスセソ', chars: ['サ', 'シ', 'ス', 'セ', 'ソ'] },
    ta: { main: 'タ', sub: 'タチツテト', chars: ['タ', 'チ', 'ツ', 'テ', 'ト'] },
    na: { main: 'ナ', sub: 'ナニヌネノ', chars: ['ナ', 'ニ', 'ヌ', 'ネ', 'ノ'] },
    ha: { main: 'ハ', sub: 'ハヒフヘホ', chars: ['ハ', 'ヒ', 'フ', 'ヘ', 'ホ'] },
    ma: { main: 'マ', sub: 'マミムメモ', chars: ['マ', 'ミ', 'ム', 'メ', 'モ'] },
    ya: { main: 'ヤ', sub: 'ヤユヨ', chars: ['ヤ', 'ユ', 'ヨ'] },
    ra: { main: 'ラ', sub: 'ラリルレロ', chars: ['ラ', 'リ', 'ル', 'レ', 'ロ'] },
    wa: { main: 'ワ', sub: 'ワヲンー', chars: ['ワ', 'ヲ', 'ン', 'ー', '～'] },
    punct: { main: '、。', sub: '、。？！', chars: ['、', '。', '？', '！', '…'] }
  }
};

const DAKUTEN_CYCLE_MAP = {
  // Hiragana
  'か': 'が', 'が': 'か', 'き': 'ぎ', 'ぎ': 'き', 'く': 'ぐ', 'ぐ': 'く', 'け': 'げ', 'げ': 'け', 'こ': 'ご', 'ご': 'こ',
  'さ': 'ざ', 'ざ': 'さ', 'し': 'じ', 'じ': 'し', 'す': 'ず', 'ず': 'す', 'せ': 'ぜ', 'ぜ': 'せ', 'そ': 'ぞ', 'ぞ': 'そ',
  'た': 'だ', 'だ': 'た', 'ち': 'ぢ', 'ぢ': 'ち', 'つ': 'っ', 'っ': 'づ', 'づ': 'つ', 'て': 'で', 'で': 'て', 'と': 'ど', 'ど': 'と',
  'は': 'ば', 'ば': 'ぱ', 'ぱ': 'は', 'ひ': 'び', 'び': 'ぴ', 'ぴ': 'ひ', 'ふ': 'ぶ', 'ぶ': 'ぷ', 'ぷ': 'ふ', 'へ': 'べ', 'べ': 'ぺ', 'ぺ': 'へ', 'ほ': 'ぼ', 'ぼ': 'ぽ', 'ぽ': 'ほ',
  'や': 'ゃ', 'ゃ': 'や', 'ゆ': 'ゅ', 'ゅ': 'ゆ', 'よ': 'ょ', 'ょ': 'よ',
  'あ': 'ぁ', 'ぁ': 'あ', 'い': 'ぃ', 'ぃ': 'い', 'う': 'ぅ', 'ぅ': 'う', 'え': 'ぇ', 'ぇ': 'え', 'お': 'ぉ', 'ぉ': 'お', 'わ': 'ゎ', 'ゎ': 'わ',

  // Katakana
  'カ': 'ガ', 'ガ': 'カ', 'キ': 'ギ', 'ギ': 'キ', 'ク': 'グ', 'グ': 'ク', 'ケ': 'ゲ', 'ゲ': 'ケ', 'コ': 'ゴ', 'ゴ': 'コ',
  'サ': 'ザ', 'ザ': 'サ', 'シ': 'ジ', 'ジ': 'シ', 'ス': 'ズ', 'ズ': 'ス', 'セ': 'ゼ', 'ゼ': 'セ', 'ソ': 'ゾ', 'ゾ': 'ソ',
  'タ': 'ダ', 'ダ': 'タ', 'チ': 'ヂ', 'ヂ': 'チ', 'ツ': 'ッ', 'ッ': 'ヅ', 'ヅ': 'ツ', 'テ': 'デ', 'デ': 'テ', 'ト': 'ド', 'ド': 'ト',
  'ハ': 'バ', 'バ': 'パ', 'パ': 'ハ', 'ヒ': 'ビ', 'ビ': 'ピ', 'ピ': 'ヒ', 'フ': 'ブ', 'ブ': 'プ', 'プ': 'フ', 'へ': 'ベ', 'ベ': 'ペ', 'ペ': 'へ', 'ホ': 'ボ', 'ボ': 'ポ', 'ポ': 'ホ',
  'ヤ': 'ャ', 'ャ': 'ヤ', 'ユ': 'ュ', 'ュ': 'ユ', 'ヨ': 'ョ', 'ョ': 'ヨ',
  'ア': 'ァ', 'ァ': 'ア', 'イ': 'ィ', 'ィ': 'イ', 'ウ': 'ゥ', 'ゥ': 'ヴ', 'ヴ': 'ウ', 'エ': 'ェ', 'ェ': 'エ', 'オ': 'ォ', 'ォ': 'オ', 'ワ': 'ヮ', 'ヮ': 'ワ'
};

/**
 * Fetch Terjemahan Online Bebas CORS via Google Translate (client=gtx)
 */
async function fetchGoogleTranslate(text, sourceLang, targetLang) {
  if (!text || !text.trim()) return null;
  const raw = text.trim();
  const cacheKey = `gtx_trans_${sourceLang}_${targetLang}_${raw}`;
  try {
    const cached = localStorage.getItem(cacheKey);
    if (cached) return JSON.parse(cached);
  } catch (e) {}

  try {
    const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=${sourceLang}&tl=${targetLang}&dt=t&dt=rm&q=${encodeURIComponent(raw)}`;
    const res = await fetch(url);
    if (res.ok) {
      const data = await res.json();
      let translated = "";
      let romaji = "";
      if (Array.isArray(data) && Array.isArray(data[0])) {
        data[0].forEach((item) => {
          if (item && item[0]) translated += item[0];
          if (item && item[3]) romaji += (romaji ? " " : "") + item[3];
        });
      }
      if (translated.trim()) {
        const result = { text: translated.trim(), romaji: romaji.trim() };
        try { localStorage.setItem(cacheKey, JSON.stringify(result)); } catch (e) {}
        return result;
      }
    }
  } catch (err) {
    console.warn("Google Translate fetch error:", err);
  }

  // Fallback Online: MyMemory Translation API
  try {
    const mmUrl = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(raw)}&langpair=${sourceLang}|${targetLang}`;
    const mmRes = await fetch(mmUrl);
    if (mmRes.ok) {
      const mmData = await mmRes.json();
      const mmTrans = mmData?.responseData?.translatedText;
      if (mmTrans && typeof mmTrans === "string" && mmTrans.toLowerCase() !== raw.toLowerCase()) {
        const clean = mmTrans.replace(/&#39;/g, "'").replace(/&quot;/g, '"').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').trim();
        const result = { text: clean, romaji: "" };
        try { localStorage.setItem(cacheKey, JSON.stringify(result)); } catch (e) {}
        return result;
      }
    }
  } catch (mmErr) {}

  return null;
}

/**
 * Terjemahan Utama Studio: Cek Kamus Lokal -> Google Translate -> Fallback
 */
async function translateStudioText(text, direction = "ja-id") {
  const raw = text.trim();
  if (!raw) return { text: "", romaji: "", from: direction };

  const isJaToId = direction === "ja-id";
  const srcLang = isJaToId ? "ja" : "id";
  const tgtLang = isJaToId ? "id" : "ja";

  // 1. Cek Kamus Cepat Lokal
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

  // 2. Cek Data Kanji Lokal (jika 1 karakter kanji diinputkan)
  if (window.KANJI_FULL_DATA && isJaToId) {
    const kanjiObj = window.KANJI_FULL_DATA.find((k) => k.kanji === raw);
    if (kanjiObj && kanjiObj.meaning) {
      return {
        text: kanjiObj.meaning,
        romaji: getRomajiReading(raw),
        isLocal: true
      };
    }
  }

  // 3. Panggil Google Translate API (gtx)
  const gResult = await fetchGoogleTranslate(raw, srcLang, tgtLang);
  if (gResult && gResult.text) {
    return {
      text: gResult.text,
      romaji: gResult.romaji || (isJaToId ? getRomajiReading(raw) : getRomajiReading(gResult.text)),
      isOnline: true
    };
  }

  // 4. Fallback Kamus Kata per Kata
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
    text: raw,
    romaji: isJaToId ? getRomajiReading(raw) : "",
    isNone: true
  };
}

// =========================================================================
// 6. KONTROLER UTAMA STUDIO TRANSLATOR & KEITAI 12-KEY KEYBOARD
// =========================================================================
function initStudioTranslator() {
  const studio = document.getElementById('studio-terjemahan');
  if (!studio) return;

  const adaptiveDirectionBadge = document.getElementById('adaptiveDirectionBadge');
  const adaptiveDirectionText = document.getElementById('adaptiveDirectionText');

  const sourceFlag = document.getElementById('sourceFlag');
  const sourceName = document.getElementById('sourceName');
  const targetFlag = document.getElementById('targetFlag');
  const targetName = document.getElementById('targetName');

  const textarea = document.getElementById('translatorInput');
  const outputEl = document.getElementById('translatorOutput');
  const romajiEl = document.getElementById('translatorRomaji');
  const statusEl = document.getElementById('translationStatus');
  const inputHint = document.getElementById('inputHint');
  const charCount = document.getElementById('inputCharCount');

  const listenInputBtn = document.getElementById('listenInputBtn');
  const listenInputSlowBtn = document.getElementById('listenInputSlowBtn');
  const listenOutputBtn = document.getElementById('listenOutputBtn');
  const listenOutputSlowBtn = document.getElementById('listenOutputSlowBtn');
  const copyInputBtn = document.getElementById('copyInputBtn');
  const copyOutputBtn = document.getElementById('copyOutputBtn');
  const clearInputBtn = document.getElementById('clearInputBtn');

  const toggleKeyboardBtn = document.getElementById('toggleKeyboardBtn');
  const keyboardPanel = document.getElementById('virtualKeyboardPanel');
  const keyboardToggleText = document.getElementById('keyboardToggleText');
  const kbCloseBtn = document.getElementById('kbCloseBtn');

  const autoRomajiImeBtn = document.getElementById('autoRomajiImeBtn');
  const imeStatusText = document.getElementById('imeStatusText');

  const kbScriptHiraganaBtn = document.getElementById('kbScriptHiraganaBtn');
  const kbScriptKatakanaBtn = document.getElementById('kbScriptKatakanaBtn');
  const kbToggleRomajiBtn = document.getElementById('kbToggleRomajiBtn');
  const kbRomajiStatusText = document.getElementById('kbRomajiStatusText');

  const kbDakutenBtn = document.getElementById('kbDakutenBtn');
  const kbSpaceBtn = document.getElementById('kbSpaceBtn');
  const kbBackspaceBtn = document.getElementById('kbBackspaceBtn');
  const kbEnterBtn = document.getElementById('kbEnterBtn');

  let activeDirection = 'ja-id';
  let activeScript = 'hiragana';
  let isAutoRomajiOn = true;
  let translateDebounceTimer = null;

  // Keitai multi-tap state
  let lastTapGroup = null;
  let lastTapIndex = 0;
  let tapCycleTimer = null;
  let currentActiveBubble = null;

  function removeAllKeitaiPopups() {
    document.querySelectorAll('.keitai-popup, .keitai-popup-bubble').forEach((el) => {
      el.hidden = true;
      el.replaceChildren();
      if (el.classList.contains('keitai-popup')) {
        el.remove();
      }
    });
    if (currentActiveBubble) {
      currentActiveBubble.hidden = true;
      currentActiveBubble.replaceChildren();
      currentActiveBubble = null;
    }
  }

  function isMobileScreen() {
    return window.innerWidth <= 768;
  }

  function applyMobileKeyboardGuard() {
    if (!textarea) return;
    const isKbOpen = keyboardPanel && !keyboardPanel.classList.contains('is-collapsed');
    if (isMobileScreen() && isKbOpen && activeScript !== 'qwerty') {
      textarea.setAttribute('inputmode', 'none');
    } else {
      textarea.removeAttribute('inputmode');
      textarea.readOnly = false;
    }
  }

  function insertTextAtCursor(charToInsert) {
    if (!textarea) return;
    applyMobileKeyboardGuard();

    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const currentVal = textarea.value;

    textarea.value = currentVal.substring(0, start) + charToInsert + currentVal.substring(end);
    const newPos = start + charToInsert.length;
    textarea.selectionStart = newPos;
    textarea.selectionEnd = newPos;

    try { textarea.focus({ preventScroll: true }); } catch (e) { textarea.focus(); }
    triggerInputUpdate();
    window.MiraiSound?.playClickIfIdle();
  }

  function replaceTextAtCursor(newChar) {
    if (!textarea) return;
    const pos = textarea.selectionStart;
    if (pos <= 0) {
      insertTextAtCursor(newChar);
      return;
    }
    textarea.value = textarea.value.slice(0, pos - 1) + newChar + textarea.value.slice(pos);
    textarea.selectionStart = pos;
    textarea.selectionEnd = pos;
    try { textarea.focus({ preventScroll: true }); } catch (e) {}
    triggerInputUpdate();
    window.MiraiSound?.playClickIfIdle();
  }

  function backspaceAtCursor() {
    if (!textarea) return;
    applyMobileKeyboardGuard();
    commitPendingTap();

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

    try { textarea.focus({ preventScroll: true }); } catch (e) {}
    triggerInputUpdate();
    window.MiraiSound?.playClickIfIdle();
  }

  function commitPendingTap() {
    clearTimeout(tapCycleTimer);
    lastTapGroup = null;
    lastTapIndex = 0;
    removeAllKeitaiPopups();
  }

  // Handle Keitai Key Tap (Multi-tap cycle + mini popup bubble)
  function handleKeitaiKeyTap(groupKey, wrapperEl) {
    applyMobileKeyboardGuard();
    const groupData = KEITAI_GROUPS[activeScript]?.[groupKey] || KEITAI_GROUPS.hiragana[groupKey];
    if (!groupData) return;

    const chars = groupData.chars;
    const bubbleEl = wrapperEl ? wrapperEl.querySelector('.keitai-popup-bubble') : null;

    if (lastTapGroup === groupKey) {
      lastTapIndex = (lastTapIndex + 1) % chars.length;
      const currentChar = chars[lastTapIndex];
      replaceTextAtCursor(currentChar);
    } else {
      commitPendingTap();
      lastTapGroup = groupKey;
      lastTapIndex = 0;
      const currentChar = chars[0];
      insertTextAtCursor(currentChar);
    }

    if (bubbleEl) {
      removeAllKeitaiPopups();
      currentActiveBubble = bubbleEl;
      bubbleEl.replaceChildren();

      chars.forEach((c, idx) => {
        const pill = document.createElement('button');
        pill.type = 'button';
        pill.className = 'keitai-bubble-pill' + (idx === lastTapIndex ? ' is-active' : '');
        pill.textContent = c;
        pill.addEventListener('click', (e) => {
          e.stopPropagation();
          replaceTextAtCursor(c);
          commitPendingTap();
          removeAllKeitaiPopups();
          window.speakText && window.speakText(c, 'ja-JP');
        });
        bubbleEl.append(pill);
      });

      bubbleEl.hidden = false;
    }

    window.speakText && window.speakText(chars[lastTapIndex], 'ja-JP');

    clearTimeout(tapCycleTimer);
    tapCycleTimer = setTimeout(() => {
      commitPendingTap();
    }, 1400);
  }

  function updateKeitaiKeyLabels() {
    const script = activeScript === 'katakana' ? 'katakana' : 'hiragana';
    const groups = KEITAI_GROUPS[script];
    studio.querySelectorAll('[data-keitai-key]').forEach((btn) => {
      const k = btn.dataset.keitaiKey;
      if (groups[k]) {
        const mainEl = btn.querySelector('.keitai-main-char');
        const subEl = btn.querySelector('.keitai-sub-chars');
        if (mainEl) mainEl.textContent = groups[k].main;
        if (subEl) subEl.textContent = groups[k].sub;
      }
    });
  }

  studio.querySelectorAll('.keitai-key-wrapper[data-key-group]').forEach((wrap) => {
    const groupKey = wrap.dataset.keyGroup;
    const btn = wrap.querySelector('.keitai-btn');
    if (btn) {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        handleKeitaiKeyTap(groupKey, wrap);
      });
    }
  });

  if (kbDakutenBtn) {
    kbDakutenBtn.addEventListener('click', () => {
      applyMobileKeyboardGuard();
      const pos = textarea.selectionStart;
      if (pos > 0) {
        const prevChar = textarea.value[pos - 1];
        if (DAKUTEN_CYCLE_MAP[prevChar]) {
          const transformed = DAKUTEN_CYCLE_MAP[prevChar];
          textarea.value = textarea.value.slice(0, pos - 1) + transformed + textarea.value.slice(pos);
          textarea.selectionStart = pos;
          textarea.selectionEnd = pos;
          try { textarea.focus({ preventScroll: true }); } catch (e) {}
          triggerInputUpdate();
          window.MiraiSound?.playClickIfIdle();
          window.speakText && window.speakText(transformed, 'ja-JP');
          commitPendingTap();
          return;
        }
      }
      window.MiraiSound?.playClickIfIdle();
    });
  }

  if (kbSpaceBtn) {
    kbSpaceBtn.addEventListener('click', () => {
      commitPendingTap();
      insertTextAtCursor(' ');
    });
  }
  if (kbBackspaceBtn) {
    kbBackspaceBtn.addEventListener('click', () => {
      backspaceAtCursor();
    });
  }
  if (kbEnterBtn) {
    kbEnterBtn.addEventListener('click', () => {
      commitPendingTap();
      insertTextAtCursor('\n');
    });
  }

  // Toggle Virtual Keyboard Panel (Floating Window)
  function setKeyboardCollapsed(collapsed) {
    if (!keyboardPanel) return;
    removeAllKeitaiPopups();
    keyboardPanel.classList.toggle('is-collapsed', collapsed);
    keyboardPanel.classList.toggle('is-open', !collapsed);
    if (toggleKeyboardBtn) {
      toggleKeyboardBtn.setAttribute('aria-expanded', String(!collapsed));
    }
    if (keyboardToggleText) {
      keyboardToggleText.textContent = collapsed
        ? 'Virtual Keyboard'
        : 'Tutup Keyboard ▴';
    }
    applyMobileKeyboardGuard();
    if (!collapsed) {
      updateKeitaiKeyLabels();
      if (typeof window.ensureKeyboardInView === 'function') {
        window.ensureKeyboardInView();
      }
    }
  }

  if (toggleKeyboardBtn) {
    toggleKeyboardBtn.addEventListener('click', () => {
      const isNowCollapsed = !keyboardPanel.classList.contains('is-collapsed');
      setKeyboardCollapsed(isNowCollapsed);
      window.MiraiSound?.playClickIfIdle();
    });
  }

  if (kbCloseBtn) {
    kbCloseBtn.addEventListener('click', () => {
      commitPendingTap();
      removeAllKeitaiPopups();
      setKeyboardCollapsed(true);
      window.MiraiSound?.playClickIfIdle();
    });
  }

  document.addEventListener('click', (e) => {
    if (!e.target.closest('.keitai-key-wrapper') && !e.target.closest('.keitai-popup') && !e.target.closest('.keitai-popup-bubble')) {
      removeAllKeitaiPopups();
    }
  });

  function setScriptMode(mode) {
    activeScript = mode === 'katakana' ? 'katakana' : 'hiragana';
    if (kbScriptHiraganaBtn) kbScriptHiraganaBtn.classList.toggle('is-active', activeScript === 'hiragana');
    if (kbScriptKatakanaBtn) kbScriptKatakanaBtn.classList.toggle('is-active', activeScript === 'katakana');
    updateKeitaiKeyLabels();
    applyMobileKeyboardGuard();
  }

  if (kbScriptHiraganaBtn) {
    kbScriptHiraganaBtn.addEventListener('click', () => {
      setScriptMode('hiragana');
      window.MiraiSound?.playClickIfIdle();
    });
  }
  if (kbScriptKatakanaBtn) {
    kbScriptKatakanaBtn.addEventListener('click', () => {
      setScriptMode('katakana');
      window.MiraiSound?.playClickIfIdle();
    });
  }

  function updateRomajiToggleState() {
    if (autoRomajiImeBtn) {
      autoRomajiImeBtn.classList.toggle('is-active', isAutoRomajiOn);
      autoRomajiImeBtn.classList.toggle('is-off', !isAutoRomajiOn);
    }
    if (imeStatusText) {
      imeStatusText.textContent = isAutoRomajiOn ? 'Auto-Romaji: ON ✨' : 'Auto-Romaji: OFF';
    }
    if (kbToggleRomajiBtn) {
      kbToggleRomajiBtn.classList.toggle('is-active', isAutoRomajiOn);
    }
    if (kbRomajiStatusText) {
      kbRomajiStatusText.textContent = isAutoRomajiOn ? 'Romaji ON' : 'Romaji OFF';
    }
  }

  if (autoRomajiImeBtn) {
    autoRomajiImeBtn.addEventListener('click', () => {
      isAutoRomajiOn = !isAutoRomajiOn;
      updateRomajiToggleState();
      window.MiraiSound?.playClickIfIdle();
    });
  }

  if (kbToggleRomajiBtn) {
    kbToggleRomajiBtn.addEventListener('click', () => {
      isAutoRomajiOn = !isAutoRomajiOn;
      updateRomajiToggleState();
      window.MiraiSound?.playClickIfIdle();
    });
  }

  // =========================================================================
  // SISTEM PENDETEKSI BAHASA ADAPTIF OTOMATIS (JEPANG vs INDONESIA)
  // =========================================================================
  const COMMON_JA_ROMAJI = new Set([
    'watashi', 'boku', 'ore', 'anata', 'kore', 'sore', 'are', 'dore',
    'koko', 'soko', 'asoko', 'doko', 'nani', 'nan', 'dare', 'itsu',
    'doushite', 'naze', 'arigatou', 'arigato', 'ohayou', 'ohayo',
    'konnichiwa', 'konbanwa', 'sayounara', 'sayonara', 'oyasumi',
    'sumimasen', 'gomen', 'gomenasai', 'itadakimasu', 'gochisousama',
    'hajimemashite', 'yoroshiku', 'desu', 'masu', 'da', 'ne', 'yo',
    'suki', 'kirai', 'kawaii', 'sugoi', 'kakkoii', 'oishii', 'samui',
    'atsui', 'hayai', 'osoi', 'ii', 'warui', 'chotto', 'motto',
    'nihon', 'nihongo', 'tokyo', 'sensei', 'gakusei', 'tomodachi'
  ]);

  const COMMON_INDONESIAN_WORDS = new Set([
    'saya', 'aku', 'kamu', 'anda', 'dia', 'mereka', 'kita', 'kami',
    'apa', 'siapa', 'kapan', 'dimana', 'bagaimana', 'kenapa', 'mengapa',
    'ini', 'itu', 'di', 'ke', 'dari', 'yang', 'dan', 'atau', 'tapi', 'tetapi',
    'karena', 'untuk', 'dengan', 'pada', 'adalah', 'bisa', 'dapat', 'mau',
    'ingin', 'akan', 'sudah', 'telah', 'sedang', 'belum', 'tidak', 'bukan', 'jangan',
    'halo', 'selamat', 'pagi', 'siang', 'sore', 'malam', 'terima', 'kasih',
    'sama', 'tolong', 'maaf', 'permisi', 'senang', 'bertemu', 'belajar',
    'makan', 'minum', 'pergi', 'datang', 'pulang', 'buku', 'rumah', 'sekolah', 'teman'
  ]);

  function detectLanguage(text) {
    if (!text || !text.trim()) return null;

    // 1. Cek aksara Jepang asli: Kanji, Hiragana, Katakana, dan Tanda Baca Jepang
    const JAPANESE_CHAR_REGEX = /[\u4E00-\u9FAF\u3040-\u309F\u30A0-\u30FF\u31F0-\u31FF\uFF65-\uFF9F]/;
    if (JAPANESE_CHAR_REGEX.test(text)) {
      return 'ja';
    }

    // 2. Cek kamus lokal langsung
    const clean = text.toLowerCase().trim();
    if (jaToIdDictionary[clean]) return 'ja';
    if (idToJaDictionary[clean]) return 'id';

    // 3. Pencocokan token kata Romaji Jepang vs Bahasa Indonesia
    const words = clean.split(/[\s,.\-!?;:"'()]+/).filter(Boolean);
    let jaHits = 0;
    let idHits = 0;

    for (const w of words) {
      if (COMMON_JA_ROMAJI.has(w) || jaToIdDictionary[w]) jaHits++;
      if (COMMON_INDONESIAN_WORDS.has(w) || idToJaDictionary[w]) idHits++;
    }

    if (jaHits > idHits) return 'ja';
    if (idHits > jaHits) return 'id';

    // Default jika huruf latin tanpa kata kunci khusus: anggap bahasa Indonesia
    return 'id';
  }

  function setDirectionUI(direction) {
    activeDirection = direction;
    const isJa = activeDirection === 'ja-id';

    if (sourceFlag) sourceFlag.textContent = isJa ? '🇯🇵' : '🇮🇩';
    if (sourceName) sourceName.textContent = isJa ? 'Jepang (Input)' : 'Indonesia (Input)';
    if (targetFlag) targetFlag.textContent = isJa ? '🇮🇩' : '🇯🇵';
    if (targetName) targetName.textContent = isJa ? 'Indonesia (Hasil)' : 'Jepang (Hasil)';

    if (adaptiveDirectionText) {
      if (!textarea.value.trim()) {
        adaptiveDirectionText.textContent = 'Deteksi Otomatis (Jepang ⇄ Indonesia)';
      } else {
        adaptiveDirectionText.textContent = isJa
          ? '🇯🇵 Jepang ➔ 🇮🇩 Indonesia (Otomatis)'
          : '🇮🇩 Indonesia ➔ 🇯🇵 Jepang (Otomatis)';
      }
    }

    if (inputHint) {
      if (!textarea.value.trim()) {
        inputHint.textContent = 'Sistem otomatis mendeteksi bahasa teks input';
      } else {
        inputHint.textContent = isJa ? '✓ Aksara Jepang terdeteksi' : '✓ Bahasa Indonesia terdeteksi';
      }
    }
  }

  // Real-time Input Update dengan Auto-Detect Bahasa & Debounce 220ms
  function triggerInputUpdate() {
    const text = textarea.value;
    if (charCount) charCount.textContent = text.length + " karakter";
    if (statusEl) statusEl.textContent = "Mengetik...";

    clearTimeout(translateDebounceTimer);
    if (!text.trim()) {
      if (outputEl) {
        outputEl.textContent = "Hasil terjemahan akan otomatis muncul di sini...";
        outputEl.classList.add("placeholder");
      }
      if (romajiEl) romajiEl.hidden = true;
      if (statusEl) statusEl.textContent = "Siap menerjemahkan";
      setDirectionUI('ja-id');
      return;
    }

    // Auto-detect bahasa input pengguna
    const detectedLang = detectLanguage(text);
    const targetDirection = (detectedLang === 'ja') ? 'ja-id' : 'id-ja';
    if (activeDirection !== targetDirection) {
      setDirectionUI(targetDirection);
    } else if (adaptiveDirectionText) {
      adaptiveDirectionText.textContent = (targetDirection === 'ja-id')
        ? '🇯🇵 Jepang ➔ 🇮🇩 Indonesia (Otomatis)'
        : '🇮🇩 Indonesia ➔ 🇯🇵 Jepang (Otomatis)';
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
            romajiEl.textContent = "(Romaji: " + result.romaji + ")";
            romajiEl.hidden = false;
          } else {
            romajiEl.hidden = true;
          }
        }
        if (statusEl) {
          statusEl.textContent = result.isOnline
            ? 'Terjemahan Online (Live)'
            : (result.isLocal ? 'Kamus Internal (Instan)' : 'Selesai diterjemahkan');
        }
      } catch (e) {
        if (statusEl) statusEl.textContent = 'Gagal menerjemahkan';
      }
    }, 220);
  }

  function applyRealtimeImeConversion() {
    if (!textarea || typeof window.wanakana === "undefined") return;
    const cursorPos = textarea.selectionStart;
    const val = textarea.value;
    if (!val) return;

    const converted = activeScript === "katakana" ? window.wanakana.toKatakana(val) : window.wanakana.toHiragana(val);
    if (converted !== val) {
      textarea.value = converted;
      const diff = converted.length - val.length;
      textarea.selectionStart = Math.max(0, cursorPos + diff);
      textarea.selectionEnd = Math.max(0, cursorPos + diff);
    }
  }

  textarea.addEventListener('input', () => {
    if (isAutoRomajiOn) {
      applyRealtimeImeConversion();
    }
    triggerInputUpdate();
  });

  textarea.addEventListener('focus', () => {
    applyMobileKeyboardGuard();
  });

  // Audio Buttons (Adaptif sesuai bahasa terdeteksi)
  if (listenInputBtn) {
    listenInputBtn.addEventListener('click', () => {
      const text = textarea.value.trim();
      if (!text) return;
      window.speakText(text, activeDirection === 'ja-id' ? 'ja-JP' : 'id-ID', false);
    });
  }
  if (listenInputSlowBtn) {
    listenInputSlowBtn.addEventListener('click', () => {
      const text = textarea.value.trim();
      if (!text) return;
      window.speakText(text, activeDirection === 'ja-id' ? 'ja-JP' : 'id-ID', true);
    });
  }

  if (listenOutputBtn) {
    listenOutputBtn.addEventListener('click', () => {
      if (outputEl.classList.contains('placeholder')) return;
      const text = outputEl.textContent.trim();
      if (!text) return;
      window.speakText(text, activeDirection === 'ja-id' ? 'id-ID' : 'ja-JP', false);
    });
  }
  if (listenOutputSlowBtn) {
    listenOutputSlowBtn.addEventListener('click', () => {
      if (outputEl.classList.contains('placeholder')) return;
      const text = outputEl.textContent.trim();
      if (!text) return;
      window.speakText(text, activeDirection === 'ja-id' ? 'id-ID' : 'ja-JP', true);
    });
  }

  function copyWithFeedback(text, buttonEl) {
    if (!text) return;
    navigator.clipboard.writeText(text).then(() => {
      const orig = buttonEl.innerHTML;
      buttonEl.innerHTML = '<span>✓ Tersalin!</span>';
      buttonEl.classList.add('btn-copied');
      setTimeout(() => {
        buttonEl.innerHTML = orig;
        buttonEl.classList.remove('btn-copied');
      }, 1800);
    }).catch(() => {
      const temp = document.createElement('textarea');
      temp.value = text;
      document.body.appendChild(temp);
      temp.select();
      document.execCommand('copy');
      document.body.removeChild(temp);
    });
  }

  if (copyInputBtn) copyInputBtn.addEventListener('click', () => copyWithFeedback(textarea.value, copyInputBtn));
  if (copyOutputBtn) copyOutputBtn.addEventListener('click', () => {
    if (!outputEl.classList.contains('placeholder')) copyWithFeedback(outputEl.textContent, copyOutputBtn);
  });
  if (clearInputBtn) {
    clearInputBtn.addEventListener('click', () => {
      textarea.value = '';
      commitPendingTap();
      triggerInputUpdate();
      try { textarea.focus(); } catch (e) {}
      window.MiraiSound?.playClickIfIdle();
    });
  }

  updateKeitaiKeyLabels();
  initKeyboardDragAndResize();
}

// =========================================================================
// FITUR KEYBOARD MELAYANG: DRAGGABLE & RESIZABLE DENGAN VIEWPORT BOUNDARIES
// =========================================================================
function initKeyboardDragAndResize() {
  const kb = document.getElementById('virtualKeyboardPanel');
  const dragHandle = document.getElementById('kbDragHandle');
  const headerHandle = document.getElementById('kbHeaderDrag') || document.querySelector('.keyboard-header');
  const resizeHandle = document.getElementById('kbResizeHandle');
  if (!kb) return;

  let isDragging = false;
  let isResizing = false;
  let startX = 0, startY = 0;
  let startLeft = 0, startTop = 0;
  let startWidth = 0, startHeight = 0;
  let hasCustomPosition = false;

  function clampPosition(left, top) {
    const pad = 8;
    const rect = kb.getBoundingClientRect();
    const minX = pad;
    const maxX = Math.max(pad, window.innerWidth - rect.width - pad);
    const minY = pad;
    const maxY = Math.max(pad, window.innerHeight - rect.height - pad);

    const clampedX = Math.max(minX, Math.min(left, maxX));
    const clampedY = Math.max(minY, Math.min(top, maxY));
    return { x: clampedX, y: clampedY };
  }

  function clampSize(w, h) {
    const minW = Math.min(310, window.innerWidth - 16);
    const maxW = Math.min(760, window.innerWidth - 16);
    const minH = 210;
    const maxH = Math.min(680, window.innerHeight - 20);

    const clampedW = Math.max(minW, Math.min(w, maxW));
    const clampedH = Math.max(minH, Math.min(h, maxH));
    return { w: clampedW, h: clampedH };
  }

  function onDragStart(e) {
    if (e.target.closest('button') || e.target.closest('.kb-mode-pill-group')) return;
    isDragging = true;
    kb.classList.add('is-dragging');

    const clientX = e.clientX ?? (e.touches && e.touches[0].clientX);
    const clientY = e.clientY ?? (e.touches && e.touches[0].clientY);
    startX = clientX;
    startY = clientY;

    const rect = kb.getBoundingClientRect();
    startLeft = rect.left;
    startTop = rect.top;

    kb.style.transform = 'none';
    kb.style.left = `${startLeft}px`;
    kb.style.top = `${startTop}px`;
    kb.style.bottom = 'auto';
    hasCustomPosition = true;

    window.addEventListener('pointermove', onDragMove, { passive: false });
    window.addEventListener('pointerup', onDragEnd);
    window.addEventListener('touchmove', onDragMove, { passive: false });
    window.addEventListener('touchend', onDragEnd);
    e.preventDefault();
  }

  function onDragMove(e) {
    if (!isDragging) return;
    const clientX = e.clientX ?? (e.touches && e.touches[0].clientX);
    const clientY = e.clientY ?? (e.touches && e.touches[0].clientY);
    const dx = clientX - startX;
    const dy = clientY - startY;

    const pos = clampPosition(startLeft + dx, startTop + dy);
    kb.style.left = `${pos.x}px`;
    kb.style.top = `${pos.y}px`;
    if (e.cancelable) e.preventDefault();
  }

  function onDragEnd() {
    if (!isDragging) return;
    isDragging = false;
    kb.classList.remove('is-dragging');
    window.removeEventListener('pointermove', onDragMove);
    window.removeEventListener('pointerup', onDragEnd);
    window.removeEventListener('touchmove', onDragMove);
    window.removeEventListener('touchend', onDragEnd);
  }

  if (dragHandle) {
    dragHandle.addEventListener('pointerdown', onDragStart);
    dragHandle.addEventListener('touchstart', onDragStart, { passive: false });
  }
  if (headerHandle) {
    headerHandle.addEventListener('pointerdown', onDragStart);
    headerHandle.addEventListener('touchstart', onDragStart, { passive: false });
  }

  function onResizeStart(e) {
    isResizing = true;
    kb.classList.add('is-resizing');

    const clientX = e.clientX ?? (e.touches && e.touches[0].clientX);
    const clientY = e.clientY ?? (e.touches && e.touches[0].clientY);
    startX = clientX;
    startY = clientY;

    const rect = kb.getBoundingClientRect();
    startWidth = rect.width;
    startHeight = rect.height;

    if (!hasCustomPosition) {
      kb.style.transform = 'none';
      kb.style.left = `${rect.left}px`;
      kb.style.top = `${rect.top}px`;
      kb.style.bottom = 'auto';
      hasCustomPosition = true;
    }

    window.addEventListener('pointermove', onResizeMove, { passive: false });
    window.addEventListener('pointerup', onResizeEnd);
    window.addEventListener('touchmove', onResizeMove, { passive: false });
    window.addEventListener('touchend', onResizeEnd);
    e.preventDefault();
    e.stopPropagation();
  }

  function onResizeMove(e) {
    if (!isResizing) return;
    const clientX = e.clientX ?? (e.touches && e.touches[0].clientX);
    const clientY = e.clientY ?? (e.touches && e.touches[0].clientY);
    const dw = clientX - startX;
    const dh = clientY - startY;

    const size = clampSize(startWidth + dw, startHeight + dh);
    kb.style.width = `${size.w}px`;
    kb.style.height = `${size.h}px`;

    const rect = kb.getBoundingClientRect();
    const pos = clampPosition(rect.left, rect.top);
    kb.style.left = `${pos.x}px`;
    kb.style.top = `${pos.y}px`;

    if (e.cancelable) e.preventDefault();
  }

  function onResizeEnd() {
    if (!isResizing) return;
    isResizing = false;
    kb.classList.remove('is-resizing');
    window.removeEventListener('pointermove', onResizeMove);
    window.removeEventListener('pointerup', onResizeEnd);
    window.removeEventListener('touchmove', onResizeMove);
    window.removeEventListener('touchend', onResizeEnd);
  }

  if (resizeHandle) {
    resizeHandle.addEventListener('pointerdown', onResizeStart);
    resizeHandle.addEventListener('touchstart', onResizeStart, { passive: false });
  }

  window.addEventListener('resize', () => {
    if (!kb.classList.contains('is-collapsed') && hasCustomPosition) {
      const rect = kb.getBoundingClientRect();
      const pos = clampPosition(rect.left, rect.top);
      kb.style.left = `${pos.x}px`;
      kb.style.top = `${pos.y}px`;
      const size = clampSize(rect.width, rect.height);
      kb.style.width = `${size.w}px`;
      kb.style.height = `${size.h}px`;
    }
  });

  window.ensureKeyboardInView = function() {
    if (!hasCustomPosition) {
      const rect = kb.getBoundingClientRect();
      const targetLeft = Math.max(8, (window.innerWidth - rect.width) / 2);
      const targetTop = Math.max(8, window.innerHeight - rect.height - 24);
      kb.style.transform = 'none';
      kb.style.left = `${targetLeft}px`;
      kb.style.top = `${targetTop}px`;
      kb.style.bottom = 'auto';
      hasCustomPosition = true;
    } else {
      const rect = kb.getBoundingClientRect();
      const pos = clampPosition(rect.left, rect.top);
      kb.style.left = `${pos.x}px`;
      kb.style.top = `${pos.y}px`;
    }
  };
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
  const listenKatakanaSlowBtn = document.getElementById('listenKatakanaSlowBtn');

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


  // Audio Katakana Voice Button (Normal & Slow-Mo)
  if (listenKatakanaBtn) {
    listenKatakanaBtn.addEventListener('click', () => {
      const textToSpeak = resKatakana?.textContent || 'ラディティヤ';
      if (window.speakText) {
        window.speakText(textToSpeak, 'ja-JP', false);
      } else if ('speechSynthesis' in window) {
        const u = new SpeechSynthesisUtterance(textToSpeak);
        u.lang = 'ja-JP';
        window.speechSynthesis.speak(u);
      }
    });
  }
  if (listenKatakanaSlowBtn) {
    listenKatakanaSlowBtn.addEventListener('click', () => {
      const textToSpeak = resKatakana?.textContent || 'ラディティヤ';
      if (window.speakText) {
        window.speakText(textToSpeak, 'ja-JP', true);
      } else if ('speechSynthesis' in window) {
        const u = new SpeechSynthesisUtterance(textToSpeak);
        u.lang = 'ja-JP';
        u.rate = 0.48;
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


function setupStudioAll() {
  initStudioTranslator();
  initNameGenerator();
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", setupStudioAll);
} else {
  setupStudioAll();
}
})();
