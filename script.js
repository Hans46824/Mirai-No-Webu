document.addEventListener("DOMContentLoaded", () => {
    const topButton = document.querySelector(".to-top");

    if (topButton) {
        const update = () => {
            topButton.classList.toggle("is-visible", window.scrollY > 500);
        };

        update();
        window.addEventListener("scroll", update, { passive: true });
        topButton.addEventListener("click", () => {
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }

    document.querySelectorAll(".reveal").forEach((section) => {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12 });

        observer.observe(section);
    });

    const slider = document.querySelector("[data-slider]");
    if (slider) {
        const slides = [...slider.querySelectorAll(".benefit-slide")];
        const dots = document.querySelector("[data-dots]");
        let active = 0;

        const render = (index) => {
            active = (index + slides.length) % slides.length;
            slides.forEach((slide, i) => slide.classList.toggle("is-active", i === active));
            dots.querySelectorAll("button").forEach((dot, i) => {
                dot.classList.toggle("is-active", i === active);
            });
        };

        slides.forEach((_, i) => {
            const dot = document.createElement("button");
            dot.type = "button";
            dot.setAttribute("aria-label", "Tampilkan slide " + (i + 1));
            dot.addEventListener("click", () => render(i));
            dots.appendChild(dot);
        });

        document.querySelector("[data-slide='prev']").addEventListener("click", () => render(active - 1));
        document.querySelector("[data-slide='next']").addEventListener("click", () => render(active + 1));
        render(0);
        setInterval(() => render(active + 1), 5500);
    }

    const sora = document.querySelector(".sora-widget");
    if (sora) {
        const toggle = sora.querySelector(".sora-toggle");
        const panel = sora.querySelector(".sora-panel");

        const close = () => {
            panel.hidden = true;
            toggle.setAttribute("aria-expanded", "false");
        };

        toggle.addEventListener("click", () => {
            const open = panel.hidden;
            panel.hidden = !open;
            toggle.setAttribute("aria-expanded", String(open));
        });

        sora.querySelector("[data-sora-close]").addEventListener("click", close);
        sora.querySelectorAll("[data-sora-link]").forEach((button) => {
            button.addEventListener("click", () => {
                window.location.href = button.dataset.soraLink;
            });
        });
    }

    const app = document.querySelector(".learning-app");
    if (app) {
        initKanaQuest();
    }
});

const rows = [
    [1, "あいうえお", ["a", "i", "u", "e", "o"]],
    [2, "かきくけこ", ["ka", "ki", "ku", "ke", "ko"]],
    [3, "さしすせそ", ["sa", "shi", "su", "se", "so"]],
    [4, "たちつてと", ["ta", "chi", "tsu", "te", "to"]],
    [5, "なにぬねの", ["na", "ni", "nu", "ne", "no"]],
    [6, "はひふへほ", ["ha", "hi", "fu", "he", "ho"]],
    [7, "まみむめも", ["ma", "mi", "mu", "me", "mo"]],
    [8, "やゆよ", ["ya", "yu", "yo"]],
    [9, "らりるれろ", ["ra", "ri", "ru", "re", "ro"]],
    [10, "わをん", ["wa", "wo", "n"]]
];

const voiced = [
    ["がぎぐげご", ["ga", "gi", "gu", "ge", "go"]],
    ["ざじずぜぞ", ["za", "ji", "zu", "ze", "zo"]],
    ["だぢづでど", ["da", "ji", "zu", "de", "do"]],
    ["ばびぶべぼ", ["ba", "bi", "bu", "be", "bo"]],
    ["ぱぴぷぺぽ", ["pa", "pi", "pu", "pe", "po"]]
];

// Setiap Yōon disimpan sebagai satu unit. Jangan gunakan string gabungan di
// sini: spread pada "きゃ" akan memisahkan き dan ゃ, lalu membuat bacaan
// bergeser (bahkan bisa menjadi "undefined") di soal latihan.
const combos = [
    [["きゃ", "きゅ", "きょ"], ["kya", "kyu", "kyo"]],
    [["しゃ", "しゅ", "しょ"], ["sha", "shu", "sho"]],
    [["ちゃ", "ちゅ", "ちょ"], ["cha", "chu", "cho"]],
    [["にゃ", "にゅ", "にょ"], ["nya", "nyu", "nyo"]],
    [["ひゃ", "ひゅ", "ひょ"], ["hya", "hyu", "hyo"]],
    [["みゃ", "みゅ", "みょ"], ["mya", "myu", "myo"]],
    [["りゃ", "りゅ", "りょ"], ["rya", "ryu", "ryo"]],
    [["ぎゃ", "ぎゅ", "ぎょ"], ["gya", "gyu", "gyo"]],
    [["じゃ", "じゅ", "じょ"], ["ja", "ju", "jo"]],
    [["びゃ", "びゅ", "びょ"], ["bya", "byu", "byo"]],
    [["ぴゃ", "ぴゅ", "ぴょ"], ["pya", "pyu", "pyo"]]
];

const wordBankHiragana = [
    // LV 1 — あいうえお (a i u e o)
    { character: "あい", romaji: "ai", meaning: "cinta", level: 1 },
    { character: "うえ", romaji: "ue", meaning: "atas", level: 1 },
    { character: "あお", romaji: "ao", meaning: "biru", level: 1 },
    { character: "いえ", romaji: "ie", meaning: "rumah", level: 1 },
    { character: "あう", romaji: "au", meaning: "bertemu", level: 1 },
    { character: "うお", romaji: "uo", meaning: "ikan", level: 1 },
    { character: "おい", romaji: "oi", meaning: "keponakan", level: 1 },
    { character: "いい", romaji: "ii", meaning: "baik", level: 1 },
    { character: "おう", romaji: "ou", meaning: "raja", level: 1 },
    { character: "あおい", romaji: "aoi", meaning: "berwarna biru", level: 1 },
    { character: "おおい", romaji: "ooi", meaning: "banyak", level: 1 },

    // LV 2 — かきくけこ (ka ki ku ke ko)
    { character: "いか", romaji: "ika", meaning: "cumi-cumi", level: 2 },
    { character: "かお", romaji: "kao", meaning: "wajah", level: 2 },
    { character: "かき", romaji: "kaki", meaning: "buah kesemek", level: 2 },
    { character: "あか", romaji: "aka", meaning: "merah", level: 2 },
    { character: "いけ", romaji: "ike", meaning: "kolam", level: 2 },
    { character: "こい", romaji: "koi", meaning: "ikan koi / cinta", level: 2 },
    { character: "かく", romaji: "kaku", meaning: "menulis", level: 2 },
    { character: "きく", romaji: "kiku", meaning: "mendengar", level: 2 },
    { character: "いく", romaji: "iku", meaning: "pergi", level: 2 },
    { character: "ここ", romaji: "koko", meaning: "di sini", level: 2 },
    { character: "あき", romaji: "aki", meaning: "musim gugur", level: 2 },
    { character: "えき", romaji: "eki", meaning: "stasiun", level: 2 },
    { character: "こえ", romaji: "koe", meaning: "suara", level: 2 },
    { character: "いき", romaji: "iki", meaning: "napas", level: 2 },
    { character: "くうき", romaji: "kuuki", meaning: "udara", level: 2 },

    // LV 3 — さしすせそ (sa shi su se so)
    { character: "すし", romaji: "sushi", meaning: "sushi", level: 3 },
    { character: "しか", romaji: "shika", meaning: "rusa", level: 3 },
    { character: "いす", romaji: "isu", meaning: "kursi", level: 3 },
    { character: "かさ", romaji: "kasa", meaning: "payung", level: 3 },
    { character: "あさ", romaji: "asa", meaning: "pagi", level: 3 },
    { character: "せかい", romaji: "sekai", meaning: "dunia", level: 3 },
    { character: "すこし", romaji: "sukoshi", meaning: "sedikit", level: 3 },
    { character: "あせ", romaji: "ase", meaning: "keringat", level: 3 },
    { character: "けさ", romaji: "kesa", meaning: "pagi ini", level: 3 },
    { character: "くさ", romaji: "kusa", meaning: "rumput", level: 3 },
    { character: "さけ", romaji: "sake", meaning: "sake / ikan salmon", level: 3 },
    { character: "しお", romaji: "shio", meaning: "garam", level: 3 },
    { character: "うそ", romaji: "uso", meaning: "bohong", level: 3 },
    { character: "あし", romaji: "ashi", meaning: "kaki", level: 3 },
    { character: "おかし", romaji: "okashi", meaning: "kue / permen", level: 3 },

    // LV 4 — たちつてと (ta chi tsu te to)
    { character: "した", romaji: "shita", meaning: "bawah", level: 4 },
    { character: "たこ", romaji: "tako", meaning: "gurita", level: 4 },
    { character: "つくえ", romaji: "tsukue", meaning: "meja", level: 4 },
    { character: "いち", romaji: "ichi", meaning: "satu", level: 4 },
    { character: "とけい", romaji: "tokei", meaning: "jam", level: 4 },
    { character: "ちか", romaji: "chika", meaning: "bawah tanah", level: 4 },
    { character: "あした", romaji: "ashita", meaning: "besok", level: 4 },
    { character: "たかい", romaji: "takai", meaning: "mahal / tinggi", level: 4 },
    { character: "ちかい", romaji: "chikai", meaning: "dekat", level: 4 },
    { character: "おと", romaji: "oto", meaning: "suara / bunyi", level: 4 },
    { character: "そと", romaji: "soto", meaning: "luar", level: 4 },
    { character: "くつ", romaji: "kutsu", meaning: "sepatu", level: 4 },
    { character: "つち", romaji: "tsuchi", meaning: "tanah", level: 4 },
    { character: "いと", romaji: "ito", meaning: "benang", level: 4 },
    { character: "ちち", romaji: "chichi", meaning: "ayah", level: 4 },
    { character: "とおい", romaji: "tooi", meaning: "jauh", level: 4 },

    // LV 5 — なにぬねの (na ni nu ne no)
    { character: "いぬ", romaji: "inu", meaning: "anjing", level: 5 },
    { character: "ねこ", romaji: "neko", meaning: "kucing", level: 5 },
    { character: "なつ", romaji: "natsu", meaning: "musim panas", level: 5 },
    { character: "なに", romaji: "nani", meaning: "apa", level: 5 },
    { character: "さかな", romaji: "sakana", meaning: "ikan", level: 5 },
    { character: "いのち", romaji: "inochi", meaning: "nyawa", level: 5 },
    { character: "にく", romaji: "niku", meaning: "daging", level: 5 },
    { character: "たのしい", romaji: "tanoshii", meaning: "menyenangkan", level: 5 },
    { character: "きのう", romaji: "kinou", meaning: "kemarin", level: 5 },
    { character: "おなか", romaji: "onaka", meaning: "perut", level: 5 },
    { character: "なな", romaji: "nana", meaning: "tujuh", level: 5 },
    { character: "あに", romaji: "ani", meaning: "kakak laki-laki", level: 5 },
    { character: "あね", romaji: "ane", meaning: "kakak perempuan", level: 5 },
    { character: "たね", romaji: "tane", meaning: "biji", level: 5 },
    { character: "なす", romaji: "nasu", meaning: "terong", level: 5 },
    { character: "ねつ", romaji: "netsu", meaning: "demam", level: 5 },
    { character: "きぬ", romaji: "kinu", meaning: "sutra", level: 5 },

    // LV 6 — はひふへほ (ha hi fu he ho)
    { character: "はな", romaji: "hana", meaning: "bunga", level: 6 },
    { character: "ほし", romaji: "hoshi", meaning: "bintang", level: 6 },
    { character: "ひと", romaji: "hito", meaning: "orang", level: 6 },
    { character: "ふね", romaji: "fune", meaning: "kapal", level: 6 },
    { character: "はし", romaji: "hashi", meaning: "sumpit / jembatan", level: 6 },
    { character: "はい", romaji: "hai", meaning: "ya", level: 6 },
    { character: "ひこうき", romaji: "hikouki", meaning: "pesawat terbang", level: 6 },
    { character: "へた", romaji: "heta", meaning: "tidak mahir", level: 6 },
    { character: "ほそい", romaji: "hosoi", meaning: "tipis", level: 6 },
    { character: "ふtoi", romaji: "futoi", meaning: "tebal", level: 6 },
    { character: "はたけ", romaji: "hatake", meaning: "ladang", level: 6 },
    { character: "ふた", romaji: "futa", meaning: "tutup", level: 6 },
    { character: "ひふ", romaji: "hifu", meaning: "kulit", level: 6 },
    { character: "はは", romaji: "haha", meaning: "ibu", level: 6 },
    { character: "ふく", romaji: "fuku", meaning: "pakaian", level: 6 },

    // LV 7 — まみむめも (ma mi mu me mo)
    { character: "うみ", romaji: "umi", meaning: "laut", level: 7 },
    { character: "かみ", romaji: "kami", meaning: "kertas / rambut", level: 7 },
    { character: "くも", romaji: "kumo", meaning: "awan", level: 7 },
    { character: "なみ", romaji: "nami", meaning: "gelombang", level: 7 },
    { character: "みみ", romaji: "mimi", meaning: "telinga", level: 7 },
    { character: "むし", romaji: "mushi", meaning: "serangga", level: 7 },
    { character: "まち", romaji: "machi", meaning: "kota", level: 7 },
    { character: "こめ", romaji: "kome", meaning: "beras", level: 7 },
    { character: "うま", romaji: "uma", meaning: "kuda", level: 7 },
    { character: "さむい", romaji: "samui", meaning: "dingin", level: 7 },
    { character: "みなと", romaji: "minato", meaning: "pelabuhan", level: 7 },
    { character: "あたま", romaji: "atama", meaning: "kepala", level: 7 },
    { character: "くま", romaji: "kuma", meaning: "beruang", level: 7 },
    { character: "はさみ", romaji: "hasami", meaning: "gunting", level: 7 },
    { character: "むら", romaji: "mura", meaning: "desa", level: 7 },
    { character: "ひみつ", romaji: "himitsu", meaning: "rahasia", level: 7 },
    { character: "むすめ", romaji: "musume", meaning: "anak perempuan", level: 7 },
    { character: "うめ", romaji: "ume", meaning: "buah plum", level: 7 },

    // LV 8 — やゆよ (ya yu yo)
    { character: "やま", romaji: "yama", meaning: "gunung", level: 8 },
    { character: "ゆき", romaji: "yuki", meaning: "salju", level: 8 },
    { character: "やさい", romaji: "yasai", meaning: "sayur", level: 8 },
    { character: "へや", romaji: "heya", meaning: "kamar", level: 8 },
    { character: "ゆめ", romaji: "yume", meaning: "mimpi", level: 8 },
    { character: "やすい", romaji: "yasui", meaning: "murah", level: 8 },
    { character: "やおや", romaji: "yaoya", meaning: "toko sayur", level: 8 },
    { character: "ふゆ", romaji: "fuyu", meaning: "musim dingin", level: 8 },
    { character: "よむ", romaji: "yomu", meaning: "membaca", level: 8 },
    { character: "やすみ", romaji: "yasumi", meaning: "libur", level: 8 },
    { character: "やくそく", romaji: "yakusoku", meaning: "janji", level: 8 },
    { character: "おや", romaji: "oya", meaning: "orang tua", level: 8 },
    { character: "やね", romaji: "yane", meaning: "atap", level: 8 },
    { character: "よやく", romaji: "yoyaku", meaning: "reservasi", level: 8 },

    // LV 9 — らりるれろ (ra ri ru re ro)
    { character: "そら", romaji: "sora", meaning: "langit", level: 9 },
    { character: "さくら", romaji: "sakura", meaning: "bunga sakura", level: 9 },
    { character: "とり", romaji: "tori", meaning: "burung", level: 9 },
    { character: "くろ", romaji: "kuro", meaning: "hitam", level: 9 },
    { character: "しろ", romaji: "shiro", meaning: "putih", level: 9 },
    { character: "くるま", romaji: "kuruma", meaning: "mobil", level: 9 },
    { character: "さる", romaji: "saru", meaning: "monyet", level: 9 },
    { character: "よる", romaji: "yoru", meaning: "malam", level: 9 },
    { character: "はる", romaji: "haru", meaning: "musim semi", level: 9 },
    { character: "ふるい", romaji: "furui", meaning: "tua / lawas", level: 9 },
    { character: "うるさい", romaji: "urusai", meaning: "berisik", level: 9 },
    { character: "からい", romaji: "karai", meaning: "pedas", level: 9 },
    { character: "あかるい", romaji: "akarui", meaning: "terang", level: 9 },
    { character: "くらい", romaji: "kurai", meaning: "gelap", level: 9 },
    { character: "しろい", romaji: "shiroi", meaning: "berwarna putih", level: 9 },
    { character: "くろい", romaji: "kuroi", meaning: "berwarna hitam", level: 9 },
    { character: "れい", romaji: "rei", meaning: "contoh", level: 9 },
    { character: "あり", romaji: "ari", meaning: "semut", level: 9 },
    { character: "はれ", romaji: "hare", meaning: "cuaca cerah", level: 9 },
    { character: "いる", romaji: "iru", meaning: "ada", level: 9 },
    { character: "いろ", romaji: "iro", meaning: "warna", level: 9 },

    // LV 10 — わをん (wa wo n)
    { character: "ほん", romaji: "hon", meaning: "buku", level: 10 },
    { character: "かんたん", romaji: "kantan", meaning: "mudah", level: 10 },
    { character: "わかる", romaji: "wakaru", meaning: "mengerti", level: 10 },
    { character: "わたし", romaji: "watashi", meaning: "saya", level: 10 },
    { character: "かわ", romaji: "kawa", meaning: "sungai", level: 10 },
    { character: "にほん", romaji: "nihon", meaning: "Jepang", level: 10 },
    { character: "ほんや", romaji: "honya", meaning: "toko buku", level: 10 },
    { character: "せんせい", romaji: "sensei", meaning: "guru", level: 10 },
    { character: "しんぶん", romaji: "shinbun", meaning: "koran", level: 10 },
    { character: "こんにちは", romaji: "konnichiwa", meaning: "halo / selamat siang", level: 10 },
    { character: "すみません", romaji: "sumimasen", meaning: "maaf", level: 10 },
    { character: "にもつ", romaji: "nimotsu", meaning: "barang bawaan", level: 10 },
    { character: "わすれる", romaji: "wasureru", meaning: "lupa", level: 10 },
    { character: "わかい", romaji: "wakai", meaning: "muda", level: 10 },

    // LV 11–15 — Dakuten & Handakuten (が ざ だ ば ぱ)
    { character: "かぎ", romaji: "kagi", meaning: "kunci", level: 11 },
    { character: "かがみ", romaji: "kagami", meaning: "cermin", level: 11 },
    { character: "がいこく", romaji: "gaikoku", meaning: "luar negeri", level: 11 },
    { character: "げんき", romaji: "genki", meaning: "sehat / semangat", level: 11 },
    { character: "ごはん", romaji: "gohan", meaning: "nasi", level: 11 },
    { character: "えいが", romaji: "eiga", meaning: "film", level: 11 },
    { character: "まんが", romaji: "manga", meaning: "komik", level: 11 },
    { character: "りんご", romaji: "ringo", meaning: "apel", level: 11 },
    { character: "たまご", romaji: "tamago", meaning: "telur", level: 11 },
    { character: "かぜ", romaji: "kaze", meaning: "angin", level: 12 },
    { character: "みず", romaji: "mizu", meaning: "air", level: 12 },
    { character: "ちず", romaji: "chizu", meaning: "peta", level: 12 },
    { character: "じかん", romaji: "jikan", meaning: "waktu", level: 12 },
    { character: "かぞく", romaji: "kazoku", meaning: "keluarga", level: 12 },
    { character: "ぞう", romaji: "zou", meaning: "gajah", level: 12 },
    { character: "だいがく", romaji: "daigaku", meaning: "universitas", level: 13 },
    { character: "でんわ", romaji: "denwa", meaning: "telepon", level: 13 },
    { character: "どこ", romaji: "doko", meaning: "di mana", level: 13 },
    { character: "だれ", romaji: "dare", meaning: "siapa", level: 13 },
    { character: "くだもの", romaji: "kudamono", meaning: "buah-buahan", level: 13 },
    { character: "でんき", romaji: "denki", meaning: "listrik", level: 13 },
    { character: "ともだち", romaji: "tomodachi", meaning: "teman", level: 13 },
    { character: "こども", romaji: "kodomo", meaning: "anak", level: 13 },
    { character: "かばん", romaji: "kaban", meaning: "tas", level: 14 },
    { character: "ぼうし", romaji: "boushi", meaning: "topi", level: 14 },
    { character: "ことば", romaji: "kotoba", meaning: "kata", level: 14 },
    { character: "ぶどう", romaji: "budou", meaning: "anggur", level: 14 },
    { character: "べんとう", romaji: "bentou", meaning: "bekal", level: 14 },
    { character: "たべる", romaji: "taberu", meaning: "makan", level: 14 },
    { character: "のむ", romaji: "nomu", meaning: "minum", level: 14 },
    { character: "ぱん", romaji: "pan", meaning: "roti", level: 15 },
    { character: "えんぴつ", romaji: "enpitsu", meaning: "pensil", level: 15 },
    { character: "さんぽ", romaji: "sanpo", meaning: "jalan-jalan", level: 15 },
    { character: "てんぷら", romaji: "tenpura", meaning: "tempura", level: 15 },
    { character: "ぷりん", romaji: "purin", meaning: "puding", level: 15 },

    // LV 16–26 — Yōon (きゃ しゃ ちゃ にゃ ひゃ みゃ りゃ ぎゃ じゃ びゃ ぴゃ)
    { character: "きょう", romaji: "kyou", meaning: "hari ini", level: 16 },
    { character: "きゅうり", romaji: "kyuuri", meaning: "mentimun", level: 16 },
    { character: "きゃく", romaji: "kyaku", meaning: "tamu", level: 16 },
    { character: "きょうだい", romaji: "kyoudai", meaning: "saudara", level: 16 },
    { character: "きょり", romaji: "kyori", meaning: "jarak", level: 16 },
    { character: "きょうしつ", romaji: "kyoushitsu", meaning: "ruang kelas", level: 16 },
    { character: "しゃしん", romaji: "shashin", meaning: "foto", level: 17 },
    { character: "しょくじ", romaji: "shokuji", meaning: "makan (formal)", level: 17 },
    { character: "しゅくだい", romaji: "shukudai", meaning: "pekerjaan rumah", level: 17 },
    { character: "かいしゃ", romaji: "kaisha", meaning: "perusahaan", level: 17 },
    { character: "でんしゃ", romaji: "densha", meaning: "kereta", level: 17 },
    { character: "じしょ", romaji: "jisho", meaning: "kamus", level: 17 },
    { character: "しゅみ", romaji: "shumi", meaning: "hobi", level: 17 },
    { character: "おちゃ", romaji: "ocha", meaning: "teh", level: 18 },
    { character: "ちゃいろ", romaji: "chairo", meaning: "warna cokelat", level: 18 },
    { character: "こうちゃ", romaji: "koucha", meaning: "teh hitam", level: 18 },
    { character: "ちゃわん", romaji: "chawan", meaning: "mangkuk", level: 18 },
    { character: "にゃんこ", romaji: "nyanko", meaning: "kucing", level: 19 },
    { character: "こんにゃく", romaji: "konnyaku", meaning: "konjac", level: 19 },
    { character: "ひゃく", romaji: "hyaku", meaning: "seratus", level: 20 },
    { character: "にひゃく", romaji: "nihyaku", meaning: "dua ratus", level: 20 },
    { character: "ひょうじ", romaji: "hyouji", meaning: "tampilan", level: 20 },
    { character: "みゃく", romaji: "myaku", meaning: "nadi", level: 21 },
    { character: "みょうじ", romaji: "myouji", meaning: "nama keluarga", level: 21 },
    { character: "りゃく", romaji: "ryaku", meaning: "singkatan", level: 22 },
    { character: "りょこう", romaji: "ryokou", meaning: "perjalanan", level: 22 },
    { character: "りょうり", romaji: "ryouri", meaning: "masakan", level: 22 },
    { character: "ぎゃく", romaji: "gyaku", meaning: "kebalikan", level: 23 },
    { character: "きんぎょ", romaji: "kingyo", meaning: "ikan mas", level: 23 },
    { character: "ぎゅうにゅう", romaji: "gyuunyuu", meaning: "susu sapi", level: 23 },
    { character: "じゃがいも", romaji: "jagaimo", meaning: "kentang", level: 24 },
    { character: "じゃま", romaji: "jama", meaning: "gangguan", level: 24 },
    { character: "にんじゃ", romaji: "ninja", meaning: "ninja", level: 24 },
    { character: "じゅうどう", romaji: "juudou", meaning: "judo", level: 24 },
    { character: "さんびゃく", romaji: "sanbyaku", meaning: "tiga ratus", level: 25 },
    { character: "びょういん", romaji: "byouin", meaning: "rumah sakit", level: 25 },
    { character: "びょうき", romaji: "byouki", meaning: "sakit", level: 25 },
    { character: "ろっぴゃく", romaji: "roppyaku", meaning: "enam ratus", level: 26 },
    { character: "ぴょんぴょん", romaji: "pyonpyon", meaning: "melompat", level: 26 }
];

const wordBankKatakana = [
    // LV 1 — アイウエオ (a i u e o)
    { character: "アイ", romaji: "ai", meaning: "mata / cinta", level: 1 },
    { character: "エア", romaji: "ea", meaning: "udara", level: 1 },
    { character: "イエ", romaji: "ie", meaning: "rumah", level: 1 },
    { character: "アオ", romaji: "ao", meaning: "biru", level: 1 },
    { character: "ウエ", romaji: "ue", meaning: "atas", level: 1 },
    { character: "オイ", romaji: "oi", meaning: "hei", level: 1 },

    // LV 2 — カキクケコ (ka ki ku ke ko)
    { character: "イカ", romaji: "ika", meaning: "cumi-cumi", level: 2 },
    { character: "カキ", romaji: "kaki", meaning: "buah kesemek", level: 2 },
    { character: "カカオ", romaji: "kakao", meaning: "kakao", level: 2 },
    { character: "ココア", romaji: "kokoa", meaning: "cokelat panas", level: 2 },
    { character: "エキ", romaji: "eki", meaning: "stasiun", level: 2 },
    { character: "キウイ", romaji: "kiui", meaning: "buah kiwi", level: 2 },
    { character: "ケーキ", romaji: "keeki", meaning: "kue", level: 2 },
    { character: "ココ", romaji: "koko", meaning: "di sini", level: 2 },

    // LV 3 — サシスセソ (sa shi su se so)
    { character: "サッカー", romaji: "sakkaa", meaning: "sepak bola", level: 3 },
    { character: "スキー", romaji: "sukii", meaning: "ski", level: 3 },
    { character: "ソース", romaji: "soosu", meaning: "saus", level: 3 },
    { character: "ケース", romaji: "keesu", meaning: "kotak / wadah", level: 3 },
    { character: "イス", romaji: "isu", meaning: "kursi", level: 3 },
    { character: "スシ", romaji: "sushi", meaning: "sushi", level: 3 },
    { character: "カサ", romaji: "kasa", meaning: "payung", level: 3 },

    // LV 4 — タチツテト (ta chi tsu te to)
    { character: "タクシー", romaji: "takushii", meaning: "taksi", level: 4 },
    { character: "テスト", romaji: "tesuto", meaning: "tes / ujian", level: 4 },
    { character: "チーズ", romaji: "chiizu", meaning: "keju", level: 4 },
    { character: "チケット", romaji: "chiketto", meaning: "tiket", level: 4 },
    { character: "スーツ", romaji: "suutsu", meaning: "setelan jas", level: 4 },
    { character: "カット", romaji: "katto", meaning: "potongan / potong", level: 4 },
    { character: "タコ", romaji: "tako", meaning: "gurita", level: 4 },

    // LV 5 — ナニヌネノ (na ni nu ne no)
    { character: "テニス", romaji: "tenisu", meaning: "tenis", level: 5 },
    { character: "ネクタイ", romaji: "nekutai", meaning: "dasi", level: 5 },
    { character: "アニメ", romaji: "anime", meaning: "animasi / anime", level: 5 },
    { character: "ノート", romaji: "nooto", meaning: "buku catatan", level: 5 },
    { character: "イヌ", romaji: "inu", meaning: "anjing", level: 5 },
    { character: "ネコ", romaji: "neko", meaning: "kucing", level: 5 },
    { character: "カヌー", romaji: "kanuu", meaning: "kano", level: 5 },

    // LV 6 — ハヒフヘホ (ha hi fu he ho)
    { character: "コーヒー", romaji: "koohii", meaning: "kopi", level: 6 },
    { character: "ナイフ", romaji: "naifu", meaning: "pisau", level: 6 },
    { character: "ヒーター", romaji: "hiitaa", meaning: "pemanas", level: 6 },
    { character: "ヘア", romaji: "hea", meaning: "rambut", level: 6 },
    { character: "ホット", romaji: "hotto", meaning: "panas", level: 6 },
    { character: "ハット", romaji: "hatto", meaning: "topi", level: 6 },

    // LV 7 — マミムメモ (ma mi mu me mo)
    { character: "カメラ", romaji: "kamera", meaning: "kamera", level: 7 },
    { character: "メモ", romaji: "memo", meaning: "catatan", level: 7 },
    { character: "ハム", romaji: "hamu", meaning: "ham", level: 7 },
    { character: "ミス", romaji: "misu", meaning: "kesalahan", level: 7 },
    { character: "マナー", romaji: "manaa", meaning: "etiket", level: 7 },
    { character: "ママ", romaji: "mama", meaning: "mama", level: 7 },

    // LV 8 — ヤユヨ (ya yu yo)
    { character: "タイヤ", romaji: "taiya", meaning: "ban", level: 8 },
    { character: "ユーモア", romaji: "yuumoa", meaning: "humor", level: 8 },
    { character: "ヤクザ", romaji: "yakuza", meaning: "mafia Jepang", level: 8 },
    { character: "ヨガ", romaji: "yoga", meaning: "yoga", level: 8 },
    { character: "ユニット", romaji: "yunitto", meaning: "unit", level: 8 },

    // LV 9 — ラリルレロ (ra ri ru re ro)
    { character: "ホテル", romaji: "hoteru", meaning: "hotel", level: 9 },
    { character: "カラオケ", romaji: "karaoke", meaning: "karaoke", level: 9 },
    { character: "ライト", romaji: "raito", meaning: "lampu", level: 9 },
    { character: "タオル", romaji: "taoru", meaning: "handuk", level: 9 },
    { character: "トイレ", romaji: "toire", meaning: "toilet", level: 9 },
    { character: "リスト", romaji: "risuto", meaning: "daftar", level: 9 },
    { character: "ロケット", romaji: "roketto", meaning: "roket", level: 9 },
    { character: "ルール", romaji: "ruuru", meaning: "aturan", level: 9 },
    { character: "リアル", romaji: "riaru", meaning: "nyata", level: 9 },

    // LV 10 — ワヲン (wa wo n)
    { character: "ワイン", romaji: "wain", meaning: "anggur", level: 10 },
    { character: "セーター", romaji: "seetaa", meaning: "sweter", level: 10 },
    { character: "コーナー", romaji: "koonaa", meaning: "sudut", level: 10 },
    { character: "カウンター", romaji: "kauntaa", meaning: "konter", level: 10 },
    { character: "ライオン", romaji: "raion", meaning: "singa", level: 10 },
    { character: "レモン", romaji: "remon", meaning: "lemon", level: 10 },
    { character: "メロン", romaji: "meron", meaning: "melon", level: 10 },
    { character: "ラーメン", romaji: "raamen", meaning: "ramen", level: 10 },

    // LV 11–15 — Dakuten & Handakuten (ガ ザ ダ バ パ)
    { character: "ガラス", romaji: "garasu", meaning: "kaca", level: 11 },
    { character: "ゴルフ", romaji: "gorufu", meaning: "golf", level: 11 },
    { character: "ガス", romaji: "gasu", meaning: "gas", level: 11 },
    { character: "ゲーム", romaji: "geemu", meaning: "permainan", level: 11 },
    { character: "ガイド", romaji: "gaido", meaning: "pemandu", level: 11 },
    { character: "マンガ", romaji: "manga", meaning: "komik", level: 11 },
    { character: "ロゴ", romaji: "rogo", meaning: "logo", level: 11 },
    { character: "ジム", romaji: "jimu", meaning: "gym", level: 12 },
    { character: "サイズ", romaji: "saizu", meaning: "ukuran", level: 12 },
    { character: "ゼロ", romaji: "zero", meaning: "nol", level: 12 },
    { character: "ゾーン", romaji: "zoon", meaning: "zona", level: 12 },
    { character: "エンジン", romaji: "enjin", meaning: "mesin", level: 12 },
    { character: "ラジオ", romaji: "rajio", meaning: "radio", level: 12 },
    { character: "ドア", romaji: "doa", meaning: "pintu", level: 13 },
    { character: "サラダ", romaji: "sarada", meaning: "salad", level: 13 },
    { character: "デザイン", romaji: "dezain", meaning: "desain", level: 13 },
    { character: "ドラマ", romaji: "dorama", meaning: "drama", level: 13 },
    { character: "カレンダー", romaji: "karendaa", meaning: "kalender", level: 13 },
    { character: "ダンス", romaji: "dansu", meaning: "tarian", level: 13 },
    { character: "ドル", romaji: "doru", meaning: "dolar", level: 13 },
    { character: "カード", romaji: "kaado", meaning: "kartu", level: 13 },
    { character: "デスク", romaji: "desuku", meaning: "meja kerja", level: 13 },
    { character: "ソーダ", romaji: "sooda", meaning: "soda", level: 13 },
    { character: "バス", romaji: "basu", meaning: "bus", level: 14 },
    { character: "ビル", romaji: "biru", meaning: "gedung", level: 14 },
    { character: "バナナ", romaji: "banana", meaning: "pisang", level: 14 },
    { character: "タバコ", romaji: "tabako", meaning: "rokok", level: 14 },
    { character: "ボール", romaji: "booru", meaning: "bola", level: 14 },
    { character: "ビール", romaji: "biiru", meaning: "bir", level: 14 },
    { character: "バター", romaji: "bataa", meaning: "mentega", level: 14 },
    { character: "ボタン", romaji: "botan", meaning: "tombol", level: 14 },
    { character: "バッグ", romaji: "baggu", meaning: "tas", level: 14 },
    { character: "ベッド", romaji: "beddo", meaning: "tempat tidur", level: 14 },
    { character: "ブラシ", romaji: "burashi", meaning: "sikat", level: 14 },
    { character: "ベスト", romaji: "besuto", meaning: "terbaik", level: 14 },
    { character: "ボート", romaji: "booto", meaning: "perahu", level: 14 },
    { character: "パン", romaji: "pan", meaning: "roti", level: 15 },
    { character: "ペン", romaji: "pen", meaning: "pena", level: 15 },
    { character: "ピアノ", romaji: "piano", meaning: "piano", level: 15 },
    { character: "スーパー", romaji: "suupaa", meaning: "supermarket", level: 15 },
    { character: "パソコン", romaji: "pasokon", meaning: "komputer", level: 15 },
    { character: "コップ", romaji: "koppu", meaning: "gelas", level: 15 },
    { character: "ペット", romaji: "petto", meaning: "hewan peliharaan", level: 15 },
    { character: "パスタ", romaji: "pasuta", meaning: "pasta", level: 15 },
    { character: "ピンク", romaji: "pinku", meaning: "merah muda", level: 15 },
    { character: "パンダ", romaji: "panda", meaning: "panda", level: 15 },
    { character: "プリン", romaji: "purin", meaning: "puding", level: 15 },
    { character: "ピザ", romaji: "piza", meaning: "pizza", level: 15 },

    // LV 16–26 — Yōon (キャ シャ チャ ニャ ヒュ ミュ リュック ギャ ジャ ビュ ピュ)
    { character: "キャンプ", romaji: "kyanpu", meaning: "kemah", level: 16 },
    { character: "キャベツ", romaji: "kyabetsu", meaning: "kubis", level: 16 },
    { character: "キュウリ", romaji: "kyuuri", meaning: "mentimun", level: 16 },
    { character: "キャプテン", romaji: "kyaputen", meaning: "kapten", level: 16 },
    { character: "シャツ", romaji: "shatsu", meaning: "kemeja", level: 17 },
    { character: "シャワー", romaji: "shawaa", meaning: "pancuran", level: 17 },
    { character: "ショック", romaji: "shokku", meaning: "syok", level: 17 },
    { character: "シャンプー", romaji: "shanpuu", meaning: "sampo", level: 17 },
    { character: "チョコ", romaji: "choko", meaning: "cokelat", level: 18 },
    { character: "チャンス", romaji: "chansu", meaning: "kesempatan", level: 18 },
    { character: "チャット", romaji: "chatto", meaning: "chat", level: 18 },
    { character: "ニュース", romaji: "nyuusu", meaning: "berita", level: 19 },
    { character: "ヒューズ", romaji: "hyuuzu", meaning: "sekring", level: 20 },
    { character: "メニュー", romaji: "menyuu", meaning: "menu", level: 21 },
    { character: "ミュージック", romaji: "myuujikku", meaning: "musik", level: 21 },
    { character: "リュック", romaji: "ryukku", meaning: "ransel", level: 22 },
    { character: "ギャング", romaji: "gyangu", meaning: "geng", level: 23 },
    { character: "ジュース", romaji: "juusu", meaning: "jus", level: 24 },
    { character: "ジャム", romaji: "jamu", meaning: "selai", level: 24 },
    { character: "パジャマ", romaji: "pajama", meaning: "piyama", level: 24 },
    { character: "ジョギング", romaji: "jogingu", meaning: "jogging", level: 24 },
    { character: "ビューティー", romaji: "byuutii", meaning: "beauty", level: 25 },
    { character: "ピュア", romaji: "pyua", meaning: "murni / pure", level: 26 }
];

const wordBank = wordBankHiragana;

function getWordBank(type) {
    return type === "katakana" ? wordBankKatakana : wordBankHiragana;
}

function makeKana(type) {
    const offset = type === "katakana" ? 0x30a0 - 0x3040 : 0;
    const convert = (text) => [...text].map((char) => String.fromCodePoint(char.codePointAt(0) + offset)).join("");
    const data = [];

    rows.forEach(([level, chars, readings]) => {
        [...chars].forEach((character, index) => {
            data.push({
                character: convert(character),
                romaji: readings[index],
                category: readings.join(" "),
                level,
                kanaType: type,
                difficulty: level > 6 ? 2 : 1,
                exampleWords: [],
                audio: null
            });
        });
    });

    voiced.forEach(([chars, readings], index) => {
        [...chars].forEach((character, charIndex) => {
            data.push({
                character: convert(character),
                romaji: readings[charIndex],
                category: readings.join(" "),
                level: 11 + index,
                kanaType: type,
                difficulty: 2,
                exampleWords: [],
                audio: null
            });
        });
    });

    combos.forEach(([chars, readings], comboIndex) => {
        chars.forEach((character, index) => {
            data.push({
                character: convert(character),
                romaji: readings[index],
                category: readings.join(" "),
                level: 16 + comboIndex,
                kanaType: type,
                difficulty: 3,
                exampleWords: [],
                audio: null
            });
        });
    });

    return data;
}

const $ = (selector) => document.querySelector(selector);

function shuffle(array) {
    return [...array].sort(() => Math.random() - 0.5);
}

function buildNormalQuestion(pool, previous, fullPool = pool) {
    const validPool = pool.filter((item) => item && item.character && item.romaji);
    const sourcePool = validPool.length ? validPool : fullPool;
    const candidates = sourcePool.filter((item) => item.character !== previous?.answer?.character);
    const answer = (candidates.length ? candidates : sourcePool)[
        Math.floor(Math.random() * (candidates.length || sourcePool.length))
    ];
    const kinds = ["kana", "romaji", "understand"];
    const kind = kinds[Math.floor(Math.random() * kinds.length)];

    let distractorCandidates = pool.filter(
        (item) => item && item.character && item.romaji && item.character !== answer.character && item.romaji !== answer.romaji
    );

    if (distractorCandidates.length < 2 && fullPool && fullPool.length) {
        const extraCandidates = fullPool.filter(
            (item) => item && item.character && item.romaji && item.character !== answer.character && item.romaji !== answer.romaji
        );
        distractorCandidates = [...distractorCandidates, ...extraCandidates];
    }

    const seenChars = new Set([answer.character]);
    const seenRomaji = new Set([answer.romaji]);
    const uniqueDistractors = [];

    for (const cand of shuffle(distractorCandidates)) {
        if (!seenChars.has(cand.character) && !seenRomaji.has(cand.romaji)) {
            seenChars.add(cand.character);
            seenRomaji.add(cand.romaji);
            uniqueDistractors.push(cand);
            if (uniqueDistractors.length >= 2) break;
        }
    }

    return {
        type: "normal",
        answer,
        kind,
        choices: shuffle([answer, ...uniqueDistractors])
    };
}

function getLevelTargetChars(levels, scriptType = "hiragana") {
    if (!levels || !levels.length) return [];
    const kanaList = makeKana(scriptType);
    const targetKana = kanaList.filter((k) => levels.includes(k.level));
    return targetKana.map((k) => k.character);
}

function filterLevelWordBank(bank, levels, scriptType = "hiragana", minCount = 4) {
    if (!levels || !levels.length) {
        return bank;
    }

    const maxLevel = Math.max(...levels);
    const minLevel = Math.min(...levels);
    const targetChars = getLevelTargetChars(levels, scriptType);

    // Learned words pool (words with level <= maxLevel)
    let learnedWords = bank.filter((w) => (minLevel >= 16 ? w.level >= 16 : true) && w.level <= maxLevel);
    if (learnedWords.length === 0) {
        learnedWords = bank.filter((w) => w.level <= maxLevel);
    }
    if (learnedWords.length === 0) {
        learnedWords = bank;
    }

    // Target words: words that belong to the active level OR contain target kana characters
    const targetWords = learnedWords.filter((w) => {
        const matchesLevel = levels.includes(w.level);
        const hasTargetChar = targetChars.length > 0 && targetChars.some((char) => w.character.includes(char));
        return matchesLevel || hasTargetChar;
    });

    if (targetWords.length >= minCount) {
        return targetWords;
    }

    // If target words are fewer than needed, prioritize all target words and pad with learned words
    const remaining = learnedWords.filter((w) => !targetWords.some((tw) => tw.character === w.character));
    const combined = [...targetWords, ...shuffle(remaining)];
    return combined.length >= minCount ? combined : bank;
}

function buildWordQuestions(scriptType = "hiragana", levels = null) {
    const bank = getWordBank(scriptType);
    const pool = filterLevelWordBank(bank, levels, scriptType, 4);

    const selected = shuffle([...pool]).slice(0, 4);

    const maxLevel = levels && levels.length ? Math.max(...levels) : 99;
    const distractorBank = bank.filter((w) => w.level <= maxLevel);
    const distractorPool = distractorBank.length >= 3 ? distractorBank : bank;

    return selected.map((item, index) => {
        const kind = index % 2 === 0 ? "romaji" : "kana";
        const distractors = shuffle(
            distractorPool.filter((candidate) => candidate.character !== item.character)
        ).slice(0, 2);

        return {
            type: "word",
            answer: item,
            kind,
            choices: shuffle([
                item,
                ...distractors
            ])
        };
    });
}

function buildMatchQuestion(scriptType = "hiragana", levels = null) {
    const bank = getWordBank(scriptType);
    const pool = filterLevelWordBank(bank, levels, scriptType, 5);

    const selected = shuffle([...pool]).slice(0, 5);
    const pairs = selected.map((item) => ({
        id: `${item.character}-${item.romaji}`,
        character: item.character,
        romaji: item.romaji,
        meaning: item.meaning
    }));

    return {
        type: "match-table",
        match: {
            leftOptions: shuffle(pairs.map((pair) => ({
                id: pair.id,
                character: pair.character,
                meaning: pair.meaning,
                romaji: pair.romaji
            }))),
            rightOptions: shuffle(pairs.map((pair) => ({
                id: pair.id,
                romaji: pair.romaji,
                character: pair.character,
                meaning: pair.meaning
            }))),
            selectedLeft: null,
            selectedRight: null,
            matchedIds: [],
            total: pairs.length
        }
    };
}

function buildPracticeQuestions(levels, pool, scriptType = "hiragana", fullPool = pool) {
    const standardQuestions = [];
    while (standardQuestions.length < 10) {
        standardQuestions.push(buildNormalQuestion(pool, standardQuestions.at(-1), fullPool));
    }

    const wordQuestions = buildWordQuestions(scriptType, levels);
    const matchQuestion = buildMatchQuestion(scriptType, levels);

    return [...standardQuestions, ...wordQuestions, matchQuestion];
}

function initKanaQuest() {
    const yoonStartLevel = rows.length + voiced.length + 1;
    const totalLevels = rows.length + voiced.length + combos.length;
    const allLevelIds = Array.from({ length: totalLevels }, (_, index) => index + 1);
    const saved = {
        xp: 0,
        streak: 1,
        review: [],
        hiragana: { unlocked: totalLevels, completed: [], best: {} },
        katakana: { unlocked: totalLevels, completed: [], best: {} }
    };

    let script = new URLSearchParams(window.location.search).get("script") === "katakana"
        ? "katakana"
        : "hiragana";
    let currentSession = null;
    const data = { hiragana: makeKana("hiragana"), katakana: makeKana("katakana") };

    document.querySelectorAll(".script-tabs [data-script]").forEach((button) => {
        button.classList.toggle("is-active", button.dataset.script === script);
    });

    const save = () => {};
    const allLevels = [
        ...rows.map(([id, chars, readings]) => ({ id, chars, label: readings.join(" ") })),
        ...voiced.map(([chars, readings], index) => ({
            id: 11 + index,
            chars,
            label: readings.join(" ")
        })),
        ...combos.map(([chars, readings], index) => ({
            id: yoonStartLevel + index,
            chars,
            label: readings.join(" ")
        }))
    ];

    const displayChars = (chars) => {
        const text = Array.isArray(chars) ? chars.join("") : chars;
        if (script === "katakana") {
            return [...text].map((char) => String.fromCodePoint(char.codePointAt(0) + 0x60)).join("");
        }
        return text;
    };

    const renderDashboard = () => {
        const userLevel = Math.floor(saved.xp / 1000) + 1;
        $("[data-user-level]").textContent = userLevel;
        $("[data-total-xp]").textContent = saved.xp;
        $("[data-level-xp]").textContent = saved.xp % 1000;
        $("[data-xp-bar]").style.width = `${(saved.xp % 1000) / 10}%`;
        $("[data-streak]").textContent = saved.streak;
        $("[data-review-count]").textContent = saved.review.length;
        $("[data-script-title]").innerHTML = `${script[0].toUpperCase() + script.slice(1)} <span>${script === "hiragana" ? "ひらがな" : "カタカナ"}</span>`;

        const progress = Math.round((saved[script].unlocked - 1) / (totalLevels - 1) * 100);
        $("[data-script-progress]").textContent = `${progress}%`;
        $("[data-script-progress-bar]").style.width = `${progress}%`;

        $("[data-level-grid]").innerHTML = allLevels.map((level) => {
            const unlocked = level.id <= saved[script].unlocked;
            const completed = saved[script].completed.includes(level.id);

            return `
                <article class="level-card ${unlocked ? "is-unlocked" : "is-locked"} ${completed ? "is-completed" : ""}">
                    <div class="level-card-top">
                        <span>${completed ? "✓ Completed" : unlocked ? "🔓 Unlocked" : "🔒 Locked"}</span>
                        <b>LV ${level.id}</b>
                    </div>
                    <h3>${level.label}</h3>
                    <strong>${displayChars(level.chars)}</strong>
                    <div class="mini-progress">
                        <i style="width:${completed ? 100 : unlocked ? 18 : 0}%"></i>
                    </div>
                    <small>
                        ${completed
                            ? "Siap diulang kapan saja"
                            : unlocked
                                ? "Mulai dari sini"
                                : `Selesaikan ${level.id - 1 < 11 ? `LV ${level.id - 1}` : "level sebelumnya"}`}
                    </small>
                    <button class="start-level" data-level="${level.id}" ${unlocked ? "" : "disabled"}>
                        ${completed ? "Latih Lagi →" : "Mulai Latihan →"}
                    </button>
                </article>
            `;
        }).join("");

        $("[data-level-grid]").querySelectorAll("[data-level]").forEach((button) => {
            button.addEventListener("click", () => startPractice([Number(button.dataset.level)]));
        });

        renderModes();
    };

    function renderModes() {
        const modes = [
            { label: "LV 1–2", levels: [1, 2] },
            { label: "LV 1–3", levels: [1, 2, 3] },
            { label: "LV 1–5", levels: [1, 2, 3, 4, 5] },
            { label: "LV 1–10", levels: Array.from({ length: rows.length }, (_, index) => index + 1) },
            { label: "LV 6–10", levels: [6, 7, 8, 9, 10] },
            { label: `Basic ${script}`, levels: Array.from({ length: rows.length }, (_, index) => index + 1) },
            { label: "Dakuten & Handakuten", levels: Array.from({ length: voiced.length }, (_, index) => rows.length + index + 1) },
            { label: "Yōon lengkap", levels: Array.from({ length: combos.length }, (_, index) => yoonStartLevel + index) },
            { label: "SEMUA MATERI", levels: allLevelIds },
            { label: "RANDOM CHALLENGE", levels: allLevelIds.filter((level) => level <= saved[script].unlocked) }
        ];

        $("[data-mode-grid]").innerHTML = modes.map((mode, index) => {
            return `
                <button class="mode-card" data-mode="${index}">
                    <b>${index === 9 ? "✦" : "→"}</b>
                    <span>${mode.label}</span>
                    <small>15 soal • campuran</small>
                </button>
            `;
        }).join("");

        $("[data-mode-grid]").querySelectorAll("[data-mode]").forEach((button) => {
            button.addEventListener("click", () => {
                startPractice(modes[Number(button.dataset.mode)].levels);
            });
        });
    }

    function startPractice(levels) {
        const unlockedLevels = levels.filter((level) => level <= saved[script].unlocked && level <= totalLevels);
        const pool = data[script].filter((item) => unlockedLevels.includes(item.level));

        if (pool.length < 3) {
            return;
        }

        currentSession = {
            levels,
            pool,
            questions: buildPracticeQuestions(levels, pool, script, data[script]),
            index: 0,
            results: [],
            matchMistakes: [],
            streak: 0,
            best: 0,
            started: Date.now()
        };

        $("[data-practice-view]").hidden = false;
        document.body.classList.add("is-practicing");
        renderQuestion();
    }

    function renderQuestion() {
        const question = currentSession.questions[currentSession.index];

        $("[data-practice-label]").textContent = `${script[0].toUpperCase() + script.slice(1)} • ${question.type === "match-table" ? "PASANGKAN KATA" : question.type === "word" ? "KOSAKATA" : question.answer?.category || "KANA"}`;
        $("[data-question-total]").textContent = currentSession.questions.length;
        $("[data-question-number]").textContent = currentSession.index + 1;
        $("[data-question-progress]").style.width = `${(currentSession.index / currentSession.questions.length) * 100}%`;
        $("[data-question-dots]").innerHTML = currentSession.questions.map((_, index) => {
            const itemState = currentSession.results[index]
                ? currentSession.results[index].state
                : index === currentSession.index ? "is-current" : "";
            return `<i class="${itemState}"></i>`;
        }).join("");

        $("[data-audio]").hidden = true;
        $("[data-answer-grid]").innerHTML = "";
        $("[data-feedback]").hidden = true;

        const defaultSub = document.querySelector(".question-card > p");

        if (question.type === "match-table") {
            $("[data-answer-grid]").classList.add("is-match-grid");
            $("[data-answer-grid]").style.cssText = "display: block !important; width: 100% !important; max-width: 100% !important; margin: 0 auto !important; grid-template-columns: none !important;";
            const { match } = question;
            $("[data-question-kind]").textContent = "PASANGKAN KATA";
            $("[data-question-prompt]").innerHTML = `
                <div class="match-prompt-head">
                    <h3 class="match-title">Pasangkan Kata & Bacaan</h3>
                    <p class="match-subtitle">Klik kata di kiri dan cocokkan dengan romaji di kanan <span class="match-counter">(${match.matchedIds.length}/${match.total} selesai)</span></p>
                </div>
            `;

            if (defaultSub) defaultSub.hidden = true;

            $("[data-answer-grid]").innerHTML = `
                <div class="match-container" style="grid-column: 1 / -1 !important; width: 100% !important; max-width: 580px !important; margin: 0 auto !important; display: block !important; box-sizing: border-box !important;">
                    <div class="match-grid" style="display: grid !important; grid-template-columns: 1fr 1fr !important; gap: 16px !important; width: 100% !important; box-sizing: border-box !important; align-items: stretch !important;">
                        <div class="match-col match-col-left" style="display: flex !important; flex-direction: column !important; gap: 12px !important; width: 100% !important; box-sizing: border-box !important; align-items: stretch !important;">
                            ${match.leftOptions.map((option) => {
                                const isMatched = match.matchedIds.includes(option.id);
                                const isSelected = match.selectedLeft === option.id;
                                return `
                                    <button
                                        class="match-button match-button--left ${isSelected ? "is-selected" : ""} ${isMatched ? "is-matched" : ""}"
                                        type="button"
                                        data-match-side="left"
                                        data-match-id="${option.id}"
                                        ${isMatched ? "disabled" : ""}
                                        style="display: flex !important; flex-direction: column !important; align-items: center !important; justify-content: center !important; width: 100% !important; min-height: 72px !important; padding: 12px 16px !important; white-space: nowrap !important; word-break: keep-all !important; text-align: center !important; box-sizing: border-box !important;"
                                    >
                                        <span class="match-kana-char" style="font-size: clamp(22px, 4vw, 28px) !important; font-weight: 700 !important; line-height: 1.25 !important; white-space: nowrap !important; word-break: keep-all !important; display: inline-block !important;">${option.character}</span>
                                        <small class="match-meaning" style="display: block !important; margin-top: 4px !important; font-size: 13px !important; white-space: nowrap !important;">(${option.meaning})</small>
                                    </button>
                                `;
                            }).join("")}
                        </div>
                        <div class="match-col match-col-right" style="display: flex !important; flex-direction: column !important; gap: 12px !important; width: 100% !important; box-sizing: border-box !important; align-items: stretch !important;">
                            ${match.rightOptions.map((option) => {
                                const isMatched = match.matchedIds.includes(option.id);
                                const isSelected = match.selectedRight === option.id;
                                return `
                                    <button
                                        class="match-button match-button--right ${isSelected ? "is-selected" : ""} ${isMatched ? "is-matched" : ""}"
                                        type="button"
                                        data-match-side="right"
                                        data-match-id="${option.id}"
                                        ${isMatched ? "disabled" : ""}
                                        style="display: flex !important; flex-direction: column !important; align-items: center !important; justify-content: center !important; width: 100% !important; min-height: 72px !important; padding: 12px 16px !important; white-space: nowrap !important; word-break: keep-all !important; text-align: center !important; box-sizing: border-box !important;"
                                    >
                                        <span class="match-romaji-char" style="font-size: clamp(18px, 3.5vw, 22px) !important; font-weight: 700 !important; white-space: nowrap !important; display: inline-block !important;">${option.romaji}</span>
                                    </button>
                                `;
                            }).join("")}
                        </div>
                    </div>
                </div>
            `;

            $("[data-answer-grid]").querySelectorAll("[data-match-side]").forEach((button) => {
                button.addEventListener("click", () => handleMatchSelection(button.dataset.matchSide, button.dataset.matchId));
            });

            return;
        }

        $("[data-answer-grid]").classList.remove("is-match-grid");
        $("[data-answer-grid]").style.cssText = "";

        if (defaultSub) {
            defaultSub.hidden = false;
            defaultSub.textContent = question.type === "word"
                ? (question.kind === "kana" || question.kind === "understand" ? "Bagaimana cara membaca kata ini?" : "Pilih penulisan kata yang tepat")
                : "Bagaimana bacaannya?";
        }

        const labels = {
            kana: "KANA → ROMAJI",
            romaji: "ROMAJI → KANA",
            audio: "DENGARKAN → PILIH KANA",
            understand: "KANA → PILIH BACAAN"
        };

        $("[data-question-kind]").textContent = question.type === "word" ? `KOSAKATA • ${labels[question.kind]}` : labels[question.kind];

        if (question.type === "word") {
            const displayChar = question.kind === "kana" || question.kind === "understand"
                ? question.answer.character
                : question.answer.romaji;
            $("[data-question-prompt]").innerHTML = `
                <div class="question-prompt-text">${displayChar}</div>
                <div class="question-prompt-meaning">(${question.answer.meaning})</div>
            `;
        } else {
            $("[data-question-prompt]").textContent = question.kind === "kana" || question.kind === "understand"
                ? question.answer.character
                : question.answer.romaji;
        }

        $("[data-answer-grid]").innerHTML = question.choices.map((choice) => {
            const display = question.kind === "kana" || question.kind === "audio"
                ? choice.romaji
                : choice.character;

            return `<button data-answer="${choice.character}">${display}</button>`;
        }).join("");

        $("[data-answer-grid]").querySelectorAll("button").forEach((button) => {
            button.addEventListener("click", () => answerQuestion(button.dataset.answer));
        });
    }

    function handleMatchSelection(side, id) {
        const question = currentSession.questions[currentSession.index];
        const match = question.match;

        if (match.matchedIds.includes(id)) {
            return;
        }

        // Track which side was selected first
        if (!match.selectedLeft && !match.selectedRight) {
            match.firstSelectedSide = side;
            match.firstSelectedId = id;
        }

        if (side === "left") {
            match.selectedLeft = id;
        } else if (side === "right") {
            match.selectedRight = id;
        }

        const leftButtons = $("[data-answer-grid]").querySelectorAll("[data-match-side='left']");
        const rightButtons = $("[data-answer-grid]").querySelectorAll("[data-match-side='right']");

        leftButtons.forEach((button) => {
            if (!match.matchedIds.includes(button.dataset.matchId)) {
                button.classList.toggle("is-selected", button.dataset.matchId === match.selectedLeft);
            }
        });

        rightButtons.forEach((button) => {
            if (!match.matchedIds.includes(button.dataset.matchId)) {
                button.classList.toggle("is-selected", button.dataset.matchId === match.selectedRight);
            }
        });

        if (!match.selectedLeft || !match.selectedRight) {
            return;
        }

        if (match.selectedLeft === match.selectedRight) {
            const matchedId = match.selectedLeft;
            match.matchedIds.push(matchedId);
            match.selectedLeft = null;
            match.selectedRight = null;
            match.firstSelectedSide = null;
            match.firstSelectedId = null;

            $("[data-answer-grid]").querySelectorAll(`[data-match-id="${matchedId}"]`).forEach((button) => {
                button.classList.remove("is-selected", "is-wrong-match", "is-correct-glow");
                button.classList.add("is-matched");
                button.disabled = true;
            });

            const matchedItem = match.leftOptions.find((o) => o.id === matchedId);
            const counterEl = $("[data-question-prompt] .match-counter");
            if (counterEl) {
                counterEl.textContent = `(${match.matchedIds.length}/${match.total} selesai)`;
            }

            const feedback = $("[data-feedback]");
            feedback.hidden = false;

            if (match.matchedIds.length >= match.total) {
                feedback.className = "feedback is-good";
                feedback.innerHTML = "<strong>Semua pasangan benar! 🎉</strong><span>Lanjut ke hasil latihan...</span>";

                currentSession.results[currentSession.index] = {
                    state: "is-correct",
                    question,
                    value: "match-complete"
                };

                currentSession.streak += 1;
                currentSession.best = Math.max(currentSession.best, currentSession.streak);

                setTimeout(() => {
                    currentSession.index += 1;
                    if (currentSession.index >= currentSession.questions.length) {
                        finishPractice();
                    } else {
                        renderQuestion();
                    }
                }, 450);
            } else {
                feedback.className = "feedback is-good";
                const info = matchedItem ? `<b>${matchedItem.character}</b> = <b>${matchedItem.romaji}</b> (${matchedItem.meaning})` : "";
                feedback.innerHTML = `<strong>Cocok! ✨</strong><span>${info}</span>`;
            }

            return;
        }

        // Wrong match selected
        const wrongLeftId = match.selectedLeft;
        const wrongRightId = match.selectedRight;

        const wrongLeftBtn = $("[data-answer-grid]").querySelector(`[data-match-side='left'][data-match-id="${wrongLeftId}"]`);
        const wrongRightBtn = $("[data-answer-grid]").querySelector(`[data-match-side='right'][data-match-id="${wrongRightId}"]`);

        // Mark chosen mismatch buttons with red shake only
        if (wrongLeftBtn) wrongLeftBtn.classList.add("is-wrong-match");
        if (wrongRightBtn) wrongRightBtn.classList.add("is-wrong-match");

        // Glow ONLY the correct partner of the FIRST option picked by the user
        const firstSide = match.firstSelectedSide || "left";
        const firstId = match.firstSelectedId || wrongLeftId;

        let correctTargetBtn = null;
        let notifText = "";

        if (firstSide === "left") {
            const firstItem = match.leftOptions.find((o) => o.id === firstId);
            correctTargetBtn = $("[data-answer-grid]").querySelector(`[data-match-side='right'][data-match-id="${firstId}"]`);
            if (firstItem) {
                notifText = `• <b>${firstItem.character}</b> pasangannya adalah <b>${firstItem.romaji}</b> (${firstItem.meaning})`;
            }
        } else {
            const firstItem = match.rightOptions.find((o) => o.id === firstId);
            correctTargetBtn = $("[data-answer-grid]").querySelector(`[data-match-side='left'][data-match-id="${firstId}"]`);
            if (firstItem) {
                notifText = `• <b>${firstItem.romaji}</b> pasangannya adalah <b>${firstItem.character}</b> (${firstItem.meaning})`;
            }
        }

        if (correctTargetBtn && !match.matchedIds.includes(firstId)) {
            correctTargetBtn.classList.add("is-correct-glow");
        }

        // Record mistake for Review Kesalahan
        const leftPair = match.leftOptions.find((o) => o.id === wrongLeftId);
        const rightPair = match.rightOptions.find((o) => o.id === wrongRightId);
        if (leftPair && rightPair) {
            currentSession.matchMistakes.push({
                character: leftPair.character,
                meaning: leftPair.meaning,
                chosenRomaji: rightPair.romaji,
                correctRomaji: leftPair.romaji
            });
        }

        const message = $("[data-feedback]");
        message.hidden = false;
        message.className = "feedback is-bad";
        message.innerHTML = `<strong>Pasangan Belum Tepat</strong><span>${notifText}</span>`;

        setTimeout(() => {
            match.selectedLeft = null;
            match.selectedRight = null;
            match.firstSelectedSide = null;
            match.firstSelectedId = null;
            if (wrongLeftBtn) wrongLeftBtn.classList.remove("is-selected", "is-wrong-match");
            if (wrongRightBtn) wrongRightBtn.classList.remove("is-selected", "is-wrong-match");
            if (correctTargetBtn) correctTargetBtn.classList.remove("is-correct-glow");
        }, 1100);
    }

    function answerQuestion(value, state = "answered") {
        if (currentSession.results[currentSession.index]) {
            return;
        }

        const question = currentSession.questions[currentSession.index];
        const correct = state !== "skipped" && value === question.answer.character;

        const displayKind = question.kind === "kana" || question.kind === "audio" ? "romaji" : "character";
        const chosenItem = question.choices ? question.choices.find((c) => c.character === value) : null;
        const userChoiceDisplay = state === "skipped"
            ? "Dilewati"
            : chosenItem ? (chosenItem[displayKind] || chosenItem.character) : value;
        const correctDisplay = question.answer[displayKind] || question.answer.romaji;

        currentSession.results[currentSession.index] = {
            state: state === "skipped" ? "skipped" : correct ? "is-correct" : "is-wrong",
            question,
            value: correct ? correctDisplay : userChoiceDisplay,
            userChoice: userChoiceDisplay,
            correctChoice: correctDisplay
        };

        currentSession.streak = correct ? currentSession.streak + 1 : 0;
        currentSession.best = Math.max(currentSession.best, currentSession.streak);

        const feedback = $("[data-feedback]");
        feedback.hidden = false;
        feedback.className = `feedback ${correct ? "is-good" : state === "skipped" ? "is-skip" : "is-bad"}`;

        const meaningText = question.type === "word" ? ` (${question.answer.meaning})` : "";

        if (correct) {
            feedback.innerHTML = `<strong>Benar! 🎉</strong><span>${question.answer.character} = ${question.answer.romaji}${meaningText}${currentSession.streak > 2 ? ` • 🔥 ${currentSession.streak} runtunan` : ""}</span>`;
        } else if (state === "skipped") {
            feedback.innerHTML = `<strong>Soal Dilewati</strong><span>Jawaban benar: <b>${question.answer.character}</b> = <b>${question.answer.romaji}</b>${meaningText}</span>`;
        } else {
            feedback.innerHTML = `<strong>Jawaban Kurang Tepat</strong><span>Jawaban benar: <b>${question.answer.character}</b> = <b>${question.answer.romaji}</b>${meaningText}</span>`;
        }

        $("[data-answer-grid]").querySelectorAll("button").forEach((button) => {
            button.disabled = true;
            if (button.dataset.answer === question.answer.character) {
                if (correct) {
                    button.classList.add("is-answer");
                } else {
                    button.classList.add("is-correct-glow");
                }
            } else if (!correct && button.dataset.answer === value) {
                button.classList.add("is-wrong-choice");
            }
        });

        const transitionDelay = correct ? 350 : 850;

        setTimeout(() => {
            currentSession.index += 1;
            if (currentSession.index >= currentSession.questions.length) {
                finishPractice();
            } else {
                renderQuestion();
            }
        }, transitionDelay);
    }

    $("[data-skip]").addEventListener("click", () => answerQuestion("", "skipped"));

    $("[data-close-practice]").addEventListener("click", () => {
        $("[data-practice-view]").hidden = true;
        document.body.classList.remove("is-practicing");
    });

    $("[data-result-home]").addEventListener("click", () => {
        $("[data-result-view]").hidden = true;
        renderDashboard();
    });

    $("[data-retry]").addEventListener("click", () => {
        $("[data-result-view]").hidden = true;
        startPractice(currentSession.levels);
    });

    $("[data-review-result]").addEventListener("click", () => {
        $("[data-mistake-list]").scrollIntoView({ behavior: "smooth" });
    });

    $("[data-audio]").addEventListener("click", () => {
        if ("speechSynthesis" in window) {
            speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(currentSession.questions[currentSession.index].answer.romaji);
            utterance.lang = "ja-JP";
            speechSynthesis.speak(utterance);
        }
    });

    $(".script-tabs").querySelectorAll("[data-script]").forEach((button) => {
        button.addEventListener("click", () => {
            script = button.dataset.script;
            $(".script-tabs .is-active").classList.remove("is-active");
            button.classList.add("is-active");
            renderDashboard();
        });
    });

    renderDashboard();

    function finishPractice() {
        const wrong = currentSession.results.filter((result) => result.state === "is-wrong" || result.state === "skipped");
        const correct = currentSession.results.filter((result) => result.state === "is-correct").length;
        const accuracy = Math.round((correct / currentSession.questions.length) * 100);

        if (accuracy >= 70) {
            const highest = Math.max(...currentSession.levels);
            saved[script].unlocked = Math.min(16, Math.max(saved[script].unlocked, highest + 1));
            saved[script].completed = [...new Set([...saved[script].completed, ...currentSession.levels])];
        }

        wrong.forEach((result) => {
            if (result.question?.answer?.character && !saved.review.includes(result.question.answer.character)) {
                saved.review.push(result.question.answer.character);
            }
        });

        save();
        $("[data-practice-view]").hidden = true;
        $("[data-result-view]").hidden = false;
        document.body.classList.remove("is-practicing");

        const xpEl = $("[data-result-xp]");
        if (xpEl) xpEl.style.display = "none";

        $("[data-result-accuracy]").textContent = `${accuracy}%`;
        $("[data-result-correct]").textContent = correct;
        $("[data-result-wrong]").textContent = wrong.length;
        $("[data-result-time]").textContent = formatTime(Date.now() - currentSession.started);
        $("[data-result-streak]").textContent = `Runtunan terbaik: ${currentSession.best}`;

        // Compile all mistakes (both quiz questions and match mismatches)
        const allMistakes = [];

        wrong.forEach((result) => {
            const q = result.question;
            const isWord = q.type === "word";
            const badge = isWord ? "KOSAKATA" : "KANA";
            const prompt = isWord
                ? `${q.answer.character} (${q.answer.meaning})`
                : q.answer.character;
            const userAns = result.userChoice || result.value || "Dilewati";
            const correctAns = result.correctChoice || (q.kind === "kana" || q.kind === "audio" || isWord ? q.answer.romaji : q.answer.character);

            const explanation = isWord
                ? `Kata “${q.answer.character}” dibaca “${q.answer.romaji}”, artinya “${q.answer.meaning}”.`
                : `Huruf “${q.answer.character}” dibaca “${q.answer.romaji}” (${q.answer.category || "Kana dasar"}).`;

            allMistakes.push({
                badge,
                prompt,
                userAns,
                correctAns,
                explanation
            });
        });

        (currentSession.matchMistakes || []).forEach((m) => {
            const prompt = `${m.character} (${m.meaning})`;
            if (!allMistakes.some((item) => item.prompt === prompt)) {
                allMistakes.push({
                    badge: "PASANGKAN KATA",
                    prompt,
                    userAns: m.chosenRomaji,
                    correctAns: m.correctRomaji,
                    explanation: `“${m.character}” berpasangan dengan “${m.correctRomaji}” yang berarti “${m.meaning}”.`
                });
            }
        });

        const mistakeContainer = $("[data-mistake-list]");
        if (allMistakes.length > 0) {
            mistakeContainer.innerHTML = `
                <div class="mistake-review-header">
                    <h3>Review Kesalahan (${allMistakes.length})</h3>
                    <p>Pelajari kembali catatan di bawah untuk memperkuat ingatanmu.</p>
                </div>
                <div class="mistake-list-wrap">
                    ${allMistakes.map((item, idx) => `
                        <div class="mistake-item-card">
                            <div class="mistake-card-top">
                                <span class="mistake-badge">${item.badge}</span>
                                <span class="mistake-num">#${idx + 1}</span>
                            </div>
                            <div class="mistake-prompt">${item.prompt}</div>
                            <div class="mistake-comparison-boxes">
                                <div class="mistake-box is-wrong">
                                    <small>❌ Jawaban Kamu</small>
                                    <strong>${item.userAns}</strong>
                                </div>
                                <div class="mistake-box is-correct">
                                    <small>✅ Jawaban Benar</small>
                                    <strong>${item.correctAns}</strong>
                                </div>
                            </div>
                            <div class="mistake-explanation-box">
                                <span class="exp-icon">💡</span>
                                <span>${item.explanation}</span>
                            </div>
                        </div>
                    `).join("")}
                </div>
            `;
        } else {
            mistakeContainer.innerHTML = `
                <div class="perfect-note">
                    <strong>🎉 Luar Biasa! Sempurna!</strong>
                    <p>Semua soal kamu selesaikan dengan benar tanpa ada kesalahan.</p>
                </div>
            `;
        }
    }

    function formatTime(milliseconds) {
        const seconds = Math.floor(milliseconds / 1000);
        return `${String(Math.floor(seconds / 60)).padStart(2, "0")}:${String(seconds % 60).padStart(2, "0")}`;
    }

    setInterval(() => {
        if (currentSession && !$("[data-practice-view]").hidden) {
            $("[data-timer]").textContent = formatTime(Date.now() - currentSession.started);
        }
    }, 1000);

    const answerObserver = new MutationObserver(() => {
        if (!currentSession) {
            return;
        }

        const question = currentSession.questions[currentSession.index];
        if (question.kind === "audio") {
            $("[data-question-prompt]").textContent = "🔊";
        }

        if (question.kind !== "understand" && question.kind !== "audio") {
            return;
        }

        $("[data-answer-grid]").querySelectorAll("button").forEach((button) => {
            const choice = question.choices.find((item) => item.character === button.dataset.answer);
            if (choice) {
                button.textContent = question.kind === "understand" ? choice.romaji : choice.character;
            }
        });
    });

    answerObserver.observe($("[data-answer-grid]"), { childList: true });
}

document.addEventListener("DOMContentLoaded", () => {
    const grid = document.querySelector("[data-level-grid]");
    if (!grid) {
        return;
    }

    const cleanLabels = () => {
        grid.querySelectorAll(".level-card small").forEach((item) => {
            item.textContent = item.textContent.replace(/Selesaikan LV \d+/, "Selesaikan materi sebelumnya");
        });
    };

    cleanLabels();
    new MutationObserver(cleanLabels).observe(grid, { childList: true });
});
