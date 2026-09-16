(() => {
    // Instant offline English -> Indonesian dictionary for Japanese/Kanji glosses
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
        "far": "jauh", "east": "timur", "west": "barat", "south": "selatan", "north": "utara",

        // Qualities & Adjectives
        "big": "besar", "large": "besar", "small": "kecil", "tiny": "sangat kecil",
        "long": "panjang", "short": "pendek", "high": "tinggi", "tall": "tinggi",
        "low": "rendah", "deep": "dalam", "shallow": "dangkal", "wide": "lebar",
        "broad": "luas, lebar", "narrow": "sempit", "thick": "tebal", "thin": "tipis",
        "heavy": "berat", "light": "ringan, terang", "dark": "gelap", "bright": "terang",
        "hot": "panas", "cold": "dingin", "warm": "hangat", "cool": "sejuk",
        "new": "baru", "old": "lama, tua", "ancient": "kuno", "young": "muda",
        "good": "baik, bagus", "bad": "buruk", "evil": "jahat", "right": "benar, tepat",
        "correct": "benar", "wrong": "salah", "true": "benar", "false": "palsu, salah",
        "real": "nyata, asli", "beautiful": "indah, cantik", "ugly": "jelek",
        "clean": "bersih", "dirty": "kotor", "fast": "cepat", "quick": "cepat",
        "slow": "lambat", "early": "pagi, awal", "late": "terlambat", "easy": "mudah",
        "difficult": "sulit", "hard": "keras, sulit", "soft": "lembut", "sweet": "manis",
        "bitter": "pahit", "spicy": "pedas", "salty": "asin", "sour": "asam",
        "delicious": "lezat, enak", "red": "merah", "blue": "biru", "green": "hijau",
        "yellow": "kuning", "black": "hitam", "white": "putih", "brown": "cokelat",
        "purple": "ungu", "color": "warna",

        // Abstract & Social Concepts
        "truth": "kebenaran", "justice": "keadilan", "virtue": "kebajikan", "morals": "moral",
        "law": "hukum", "rule": "aturan", "order": "keteraturan, pesanan", "freedom": "kebebasan",
        "liberty": "kebebasan", "right": "hak", "duty": "kewajiban", "responsibility": "tanggung jawab",
        "dream": "mimpi", "hope": "harapan", "wish": "keinginan, harapan", "faith": "kepercayaan, iman",
        "belief": "keyakinan", "religion": "agama", "god": "tuhan, dewa", "deity": "dewa",
        "spirit": "roh, semangat", "ghost": "hantu", "demon": "iblis, monster", "magic": "sihir",
        "science": "ilmu pengetahuan", "mathematics": "matematika", "literature": "sastra", "history": "sejarah",
        "art": "seni", "music": "musik", "song": "lagu", "dance": "tarian",
        "economy": "ekonomi", "finance": "keuangan", "trade": "perdagangan", "business": "bisnis",
        "politics": "politik", "government": "pemerintahan", "nation": "bangsa", "culture": "budaya",
        "custom": "kebiasaan, adat", "tradition": "tradisi", "festival": "festival, perayaan", "holiday": "hari libur",
        "travel": "perjalanan, wisata", "journey": "perjalanan", "trip": "perjalanan", "pathway": "jalur"
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

    async function fetchOnlineTranslation(text) {
        const cacheKey = `mnh_trans_${text.toLowerCase().trim()}`;
        try {
            const cached = localStorage.getItem(cacheKey);
            if (cached) return cached;
        } catch (e) {}

        try {
            const res = await fetch(`https://api.mymemory.translated.net/get?q=${encodeURIComponent(text)}&langpair=en|id`);
            if (res.ok) {
                const data = await res.json();
                const trans = data?.responseData?.translatedText;
                if (trans && typeof trans === "string" && trans.toLowerCase() !== text.toLowerCase()) {
                    const clean = trans.trim().toLowerCase();
                    try {
                        localStorage.setItem(cacheKey, clean);
                    } catch (e) {}
                    return clean;
                }
            }
        } catch (err) {
            // Silently fall back
        }
        return null;
    }

    window.MiraiTranslator = {
        dictionary,
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

            // 2. Jika kata tunggal ada di kamus lokal, gunakan langsung
            const cleaned = cleanEnglish(raw);
            const direct = translateWordDirect(cleaned) || translateWordDirect(raw);
            if (direct) {
                try { localStorage.setItem(cacheKey, direct); } catch (e) {}
                return direct;
            }

            // 3. Terjemahkan frasa penuh menggunakan MyMemory API agar tidak ada kata Inggris tersisa
            const online = await fetchOnlineTranslation(raw);
            if (online) return online;

            // 4. Fallback jika offline
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
})();
