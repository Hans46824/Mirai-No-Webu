(() => {
    const hiraRows = [
        "あいうえお", "かきくけこ", "さしすせそ", "たちつてと", "なにぬねの",
        "はひふへほ", "まみむめも", "やゆよ", "らりるれろ", "わをん",
        "がぎぐげご", "ざじずぜぞ", "だぢづでど", "ばびぶべぼ", "ぱぴぷぺぽ",
        "きゃきゅきょ", "しゃしゅしょ", "ちゃちゅちょ", "にゃにゅにょ", "ひゃひゅひょ",
        "みゃみゅみょ", "りゃりゅりょ", "ぎゃぎゅぎょ", "じゃじゅじょ", "びゃびゅびょ",
        "ぴゃぴゅぴょ", "っ"
    ];

    const romanRows = [
        "a i u e o", "ka ki ku ke ko", "sa shi su se so", "ta chi tsu te to", "na ni nu ne no",
        "ha hi fu he ho", "ma mi mu me mo", "ya yu yo", "ra ri ru re ro", "wa wo n",
        "ga gi gu ge go", "za ji zu ze zo", "da ji zu de do", "ba bi bu be bo", "pa pi pu pe po",
        "kya kyu kyo", "sha shu sho", "cha chu cho", "nya nyu nyo", "hya hyu hyo",
        "mya myu myo", "rya ryu ryo", "gya gyu gyo", "ja ju jo", "bya byu byo",
        "pya pyu pyo", "tsu kecil"
    ];

    const roman = Object.fromEntries(
        hiraRows.slice(0, 15).flatMap((row, rowIndex) =>
            [...row].map((character, index) => [character, romanRows[rowIndex].split(" ")[index]])
        )
    );
    roman["っ"] = "tsu kecil";

    const combinationReading = {
        "きゃ": "kya", "きゅ": "kyu", "きょ": "kyo",
        "しゃ": "sha", "しゅ": "shu", "しょ": "sho",
        "ちゃ": "cha", "ちゅ": "chu", "ちょ": "cho",
        "にゃ": "nya", "にゅ": "nyu", "にょ": "nyo",
        "ひゃ": "hya", "ひゅ": "hyu", "ひょ": "hyo",
        "みゃ": "mya", "みゅ": "myu", "みょ": "myo",
        "りゃ": "rya", "りゅ": "ryu", "りょ": "ryo",
        "ぎゃ": "gya", "ぎゅ": "gyu", "ぎょ": "gyo",
        "じゃ": "ja", "じゅ": "ju", "じょ": "jo",
        "びゃ": "bya", "びゅ": "byu", "びょ": "byo",
        "ぴゃ": "pya", "ぴゅ": "pyu", "ぴょ": "pyo"
    };

    const examples = {
        あ: ["あさ", "asa", "pagi"],
        い: ["いぬ", "inu", "anjing"],
        う: ["うみ", "umi", "laut"],
        え: ["えき", "eki", "stasiun"],
        お: ["おちゃ", "ocha", "teh hijau"],
        か: ["かさ", "kasa", "payung"],
        き: ["き", "ki", "pohon"],
        く: ["くるま", "kuruma", "mobil"],
        け: ["けさ", "kesa", "pagi ini"],
        こ: ["こども", "kodomo", "anak-anak"],
        さ: ["さくら", "sakura", "bunga sakura"],
        し: ["しま", "shima", "pulau"],
        す: ["すし", "sushi", "sushi"],
        せ: ["せんせい", "sensei", "guru"],
        そ: ["そら", "sora", "langit"],
        た: ["たまご", "tamago", "telur"],
        ち: ["ちず", "chizu", "peta"],
        つ: ["つき", "tsuki", "bulan"],
        て: ["て", "te", "tangan"],
        と: ["とり", "tori", "burung"],
        な: ["なつ", "natsu", "musim panas"],
        に: ["にほん", "nihon", "Jepang"],
        ぬ: ["ぬいぐるみ", "nuigurumi", "boneka"],
        ね: ["ねこ", "neko", "kucing"],
        の: ["のみもの", "nomimono", "minuman"],
        は: ["はな", "hana", "bunga"],
        ひ: ["ひと", "hito", "orang"],
        ふ: ["ふね", "fune", "kapal"],
        へ: ["へや", "heya", "kamar"],
        ほ: ["ほん", "hon", "buku"],
        ま: ["まど", "mado", "jendela"],
        み: ["みず", "mizu", "air"],
        む: ["むし", "mushi", "serangga"],
        め: ["め", "me", "mata"],
        も: ["もり", "mori", "hutan"],
        や: ["やま", "yama", "gunung"],
        ゆ: ["ゆき", "yuki", "salju"],
        よ: ["よる", "yoru", "malam"],
        ら: ["らいねん", "rainen", "tahun depan"],
        り: ["りんご", "ringo", "apel"],
        る: ["るす", "rusu", "tidak di rumah"],
        れ: ["れきし", "rekishi", "sejarah"],
        ろ: ["ろうそく", "rousoku", "lilin"],
        わ: ["わたし", "watashi", "saya"],
        を: ["ほんをよむ", "hon o yomu", "membaca buku (partikel)"],
        ん: ["にほん", "nihon", "Jepang"],
        が: ["がくせい", "gakusei", "siswa"],
        ぎ: ["ぎんこう", "ginkou", "bank"],
        ぐ: ["ぐんたい", "guntai", "tentara"],
        げ: ["げんき", "genki", "sehat / bersemangat"],
        ご: ["ごはん", "gohan", "nasi"],
        ざ: ["ざっし", "zasshi", "majalah"],
        じ: ["じかん", "jikan", "waktu"],
        ず: ["ずっと", "zutto", "selamanya / terus"],
        ぜ: ["ぜんぶ", "zenbu", "semua"],
        ぞ: ["ぞう", "zou", "gajah"],
        だ: ["だいがく", "daigaku", "universitas"],
        ぢ: ["はなぢ", "hanaji", "mimisan"],
        づ: ["つづく", "tsuzuku", "berlanjut"],
        で: ["でんしゃ", "densha", "kereta listrik"],
        ど: ["どこ", "doko", "di mana"],
        ば: ["ばしょ", "basho", "tempat"],
        び: ["びょういん", "byouin", "rumah sakit"],
        ぶ: ["ぶんか", "bunka", "budaya"],
        べ: ["べんきょう", "benkyou", "belajar"],
        ぼ: ["ぼうし", "boushi", "topi"],
        ぱ: ["ぱん", "pan", "roti"],
        ぴ: ["ぴかぴか", "pikapika", "berkilau"],
        ぷ: ["ぷれぜんと", "purezento", "hadiah"],
        ぺ: ["ぺん", "pen", "pena"],
        ぽ: ["ぽけっと", "poketto", "saku"],
        きゃ: ["きゃく", "kyaku", "tamu / pelanggan"],
        きゅ: ["きゅうり", "kyuuri", "mentimun"],
        きょ: ["きょう", "kyou", "hari ini"],
        しゃ: ["しゃしん", "shashin", "foto"],
        しゅ: ["しゅくだい", "shukudai", "pekerjaan rumah"],
        しょ: ["しょくどう", "shokudou", "kantin"],
        ちゃ: ["おちゃ", "ocha", "teh"],
        ちゅ: ["ちゅうごく", "chuugoku", "China"],
        ちょ: ["ちょっと", "chotto", "sebentar"],
        にゃ: ["にゃー", "nyaa", "meong (suara kucing)"],
        にゅ: ["にゅうがく", "nyuugaku", "masuk sekolah"],
        にょ: ["にょうぼう", "nyoubou", "istri"],
        ひゃ: ["ひゃく", "hyaku", "seratus"],
        ひゅ: ["ひゅうひゅう", "hyuuhyuu", "desiran angin"],
        ひょ: ["ひょうじ", "hyouji", "tampilan"],
        みゃ: ["みゃく", "myaku", "denyut nadi"],
        みゅ: ["みゅーじっく", "myuujikku", "musik"],
        みょ: ["みょうじ", "myouji", "nama keluarga"],
        りゃ: ["りゃくご", "ryakugo", "singkatan"],
        りゅ: ["りゅうがく", "ryuugaku", "studi luar negeri"],
        りょ: ["りょこう", "ryokou", "perjalanan / liburan"],
        ぎゃ: ["ぎゃくてん", "gyakuten", "pembalikan keadaan"],
        ぎゅ: ["ぎゅうにゅう", "gyuunyuu", "susu sapi"],
        ぎょ: ["ぎょぎょう", "gyogyou", "perikanan"],
        じゃ: ["じゃがいも", "jagaimo", "kentang"],
        じゅ: ["じゅぎょう", "jugyou", "pelajaran"],
        じょ: ["じょせい", "josei", "wanita"],
        びゃ: ["びゃくだん", "byakudan", "kayu cendana"],
        びゅ: ["びゅうびゅう", "byuubyuu", "tiupan angin kencang"],
        びょ: ["びょうき", "byouki", "sakit / penyakit"],
        ぴゃ: ["さんぴゃく", "sanpyaku", "tiga ratus"],
        ぴゅ: ["ぴゅーま", "pyuuma", "puma"],
        ぴょ: ["ぴょんぴょん", "pyonpyon", "melompat-lompat"],
        っ: ["がっこう", "gakkou", "sekolah (konsonan ganda)"],
        ア: ["アニメ", "anime", "animasi / anime"],
        イ: ["インターネット", "intaanetto", "internet"],
        ウ: ["ウイルス", "uirusu", "virus"],
        エ: ["エレベーター", "erebeetaa", "lift / elevator"],
        オ: ["オレンジ", "orenji", "jeruk"],
        カ: ["カメラ", "kamera", "kamera"],
        キ: ["キッチン", "kicchin", "dapur"],
        ク: ["クラス", "kurasu", "kelas"],
        ケ: ["ケーキ", "keeki", "kue"],
        コ: ["コーヒー", "koohii", "kopi"],
        サ: ["サラダ", "sarada", "salad"],
        シ: ["シャツ", "shatsu", "kemeja"],
        ス: ["スポーツ", "supootsu", "olahraga"],
        セ: ["セーター", "seetaa", "sweater"],
        ソ: ["ソファ", "sofa", "sofa"],
        タ: ["タクシー", "takushii", "taksi"],
        チ: ["チーズ", "chiizu", "keju"],
        ツ: ["ツアー", "tsuaa", "tur / perjalanan"],
        テ: ["テレビ", "terebi", "televisi"],
        ト: ["トイレ", "toire", "toilet"],
        ナ: ["ナイフ", "naifu", "pisau"],
        ニ: ["ニュース", "nyuusu", "berita"],
        ヌ: ["ヌードル", "nuudoru", "mi"],
        ネ: ["ネクタイ", "nekutai", "dasi"],
        ノ: ["ノート", "nooto", "buku catatan"],
        ハ: ["ホテル", "hoteru", "hotel"],
        ヒ: ["ヒーター", "hiitaa", "pemanas"],
        フ: ["フォーク", "fooku", "garpu"],
        ヘ: ["ヘリコプター", "herikoputaa", "helikopter"],
        ホ: ["ホーム", "hoomu", "peron stasiun"],
        マ: ["マンガ", "manga", "komik jepang"],
        ミ: ["ミルク", "miruku", "susu"],
        ム: ["ムービー", "muubii", "film"],
        メ: ["メニュー", "menyuu", "menu"],
        モ: ["モデル", "moderu", "model"],
        ヤ: ["ヤンキー", "yankii", "anak muda bergaya"],
        ユ: ["ユーザー", "yuuzaa", "pengguna"],
        ヨ: ["ヨーグルト", "yooguruto", "yogurt"],
        ラ: ["ラジオ", "rajio", "radio"],
        リ: ["リモコン", "rimokon", "remote control"],
        ル: ["ルール", "ruuru", "aturan"],
        レ: ["レストラン", "resutoran", "restoran"],
        ロ: ["ロボット", "robotto", "robot"],
        ワ: ["ワイン", "wain", "anggur / wine"],
        ヲ: ["ヲタク", "wotaku", "penggemar berat / otaku"],
        ン: ["パン", "pan", "roti"],
        ッ: ["ベッド", "beddo", "tempat tidur (konsonan ganda)"]
    };

    function toKatakana(text) {
        return text.replace(/[ぁ-ん]/g, (character) => String.fromCharCode(character.charCodeAt(0) + 0x60));
    }

    const kataRows = hiraRows.map(toKatakana);
    const kataRoman = Object.fromEntries(
        Object.entries(roman).map(([character, reading]) => [toKatakana(character), reading])
    );

    const categoriesConfig = [
        {
            id: "basic",
            title: "1. Huruf Dasar (Gojūon • 五十音)",
            badge: "46 Karakter Pokok",
            description: {
                hiragana: "Huruf dasar Hiragana merupakan 46 suku kata pokok yang mencakup 5 vokal utama (a, i, u, e, o) dan kombinasi konsonan K, S, T, N, H, M, Y, R, W, serta N. Huruf ini digunakan untuk menulis kata asli bahasa Jepang, partikel, dan akhiran kata (okurigana).",
                katakana: "Huruf dasar Katakana terdiri dari 46 suku kata bersudut tegas yang mewakili bunyi vokal dan konsonan standar. Digunakan terutama untuk menulis kata serapan bahasa asing (gairaigo), nama asing, onomatope, dan istilah modern."
            },
            hiraChars: [
                "あ","い","う","え","お",
                "か","き","く","け","こ",
                "さ","し","す","せ","そ",
                "た","ち","つ","て","と",
                "な","に","ぬ","ね","の",
                "は","ひ","ふ","へ","ほ",
                "ま","み","む","め","も",
                "や","ゆ","よ",
                "ら","り","る","れ","ろ",
                "わ","を","ん",
                "っ"
            ]
        },
        {
            id: "dakuten",
            title: "2. Dakuten (濁点 • Bunyi Bersuara)",
            badge: "20 Karakter (Tenten ゛)",
            description: {
                hiragana: "Dakuten adalah bunyi bersuara yang dibentuk dengan menambahkan tanda petik dua (゛ / tenten) di sudut kanan atas huruf dasar. Tanda ini mengubah konsonan tak bersuara menjadi bersuara: baris K → G (が), S → Z (ざ), T → D (だ), dan H → B (ば).",
                katakana: "Dakuten Katakana dibentuk dengan menambahkan tanda petik dua (゛ / tenten) pada huruf dasar baris Ka, Sa, Ta, dan Ha untuk mengubah konsonannya menjadi Ga, Za, Da, dan Ba."
            },
            hiraChars: [
                "が","ぎ","ぐ","げ","ご",
                "ざ","じ","ず","ぜ","ぞ",
                "だ","ぢ","づ","で","ど",
                "ば","び","ぶ","べ","ぼ"
            ]
        },
        {
            id: "handakuten",
            title: "3. Handakuten (半濁点 • Bunyi Semi-bersuara)",
            badge: "5 Karakter Bunyi P (Maru ゜)",
            description: {
                hiragana: "Handakuten adalah bunyi semi-bersuara yang dibentuk dengan menambahkan lingkaran kecil (゜ / maru) di sudut kanan atas huruf baris H (はひふへほ). Tanda ini mengubah bunyi H menjadi konsonan P (ぱぴぷぺぽ).",
                katakana: "Handakuten Katakana dibentuk dengan menambahkan tanda maru (゜) pada baris Ha (ハヒフヘホ) untuk menghasilkan baris Pa, Pi, Pu, Pe, Po (パピプペポ)."
            },
            hiraChars: [
                "ぱ","ぴ","ぷ","ぺ","ぽ"
            ]
        },
        {
            id: "yoon",
            title: "4. Yōon (拗音 • Bunyi Gabungan / Diftong)",
            badge: "33 Karakter Diftong",
            description: {
                hiragana: "Yōon adalah bunyi gabungan atau diftong yang dibentuk dari suku kata baris vokal 'i' (ki, shi, chi, ni, hi, mi, ri, gi, ji, bi, pi) dikombinasikan dengan huruf kecil ya, yu, yo (ゃ, ゅ, ょ). Diucapkan menyatu dalam satu hembusan napas (contoh: き + ゃ = kya, bukan ki-ya).",
                katakana: "Yōon Katakana dibentuk dari huruf berakhiran 'i' yang digabungkan dengan huruf kecil ャ, ュ, ョ untuk menghasilkan bunyi gabungan seperti Kya, Sha, Cha, Nya, Hya, Mya, Rya, Gya, Ja, Bya, dan Pya."
            },
            hiraChars: [
                "きゃ","きゅ","きょ",
                "しゃ","しゅ","しょ",
                "ちゃ","ちゅ","ちょ",
                "にゃ","にゅ","にょ",
                "ひゃ","ひゅ","ひょ",
                "みゃ","みゅ","みょ",
                "りゃ","りゅ","りょ",
                "ぎゃ","ぎゅ","ぎょ",
                "じゃ","じゅ","じょ",
                "びゃ","びゅ","びょ",
                "ぴゃ","ぴゅ","ぴょ"
            ]
        }
    ];

    function getCharacters(type) {
        return categoriesConfig.flatMap((cat) =>
            type === "katakana" ? cat.hiraChars.map(toKatakana) : cat.hiraChars
        );
    }

    function getDetail(character, type) {
        let reading = "";
        if (type === "hiragana") {
            reading = roman[character] || combinationReading[character];
        } else {
            const hiraChar = character.replace(/[ァ-ン]/g, (value) =>
                String.fromCharCode(value.charCodeAt(0) - 0x60)
            );
            reading = kataRoman[character] || combinationReading[hiraChar] || roman[hiraChar];
        }

        const example = examples[character] || [character, reading || "bunyi", "contoh penggunaan"];
        return { character, reading: reading || "bunyi gabungan", example };
    }

    function initLesson() {
        const type = document.body.dataset.kanaPage;
        if (!type) return;

        const grid = document.querySelector("[data-kana-grid]");
        const detail = document.querySelector("[data-kana-detail]");
        const search = document.querySelector("[data-kana-lesson-search]");
        let player;

        function show(character) {
            const item = getDetail(character, type);
            player?.destroy();
            detail.innerHTML = `
                <p class="card-number">${type.toUpperCase()} / ${item.reading}</p>
                <div class="selected-kana">${character}</div>
                <h3>Urutan Menulis</h3>
                <p>Ikuti arah setiap goresan, lalu ulangi perlahan dengan tanganmu.</p>
                <div data-stroke-player></div>
                <h4>Contoh kata</h4>
                <div class="word-examples">
                    <p><b>${item.example[0]}</b><span>${item.example[1]}</span>${item.example[2]}</p>
                </div>
            `;
            player = window.createStrokePlayer(detail.querySelector("[data-stroke-player]"), character, 3, {
                showClear: true
            });
        }

        const render = () => {
            const query = search?.value.trim().toLowerCase() || "";
            grid.replaceChildren();

            let totalMatches = 0;
            let firstMatchedButton = null;

            categoriesConfig.forEach((cat) => {
                const chars = type === "katakana" ? cat.hiraChars.map(toKatakana) : cat.hiraChars;
                const visibleChars = chars.filter((character) => {
                    const item = getDetail(character, type);
                    return !query || `${character} ${item.reading}`.toLowerCase().includes(query);
                });

                if (visibleChars.length === 0) {
                    return;
                }

                totalMatches += visibleChars.length;

                const section = document.createElement("section");
                section.className = "kana-section-group";

                const descText = cat.description[type] || cat.description.hiragana;
                section.innerHTML = `
                    <div class="kana-section-header">
                        <div class="kana-section-title-wrap">
                            <h3 class="kana-section-title">${cat.title}</h3>
                            <span class="kana-section-badge">${cat.badge}</span>
                        </div>
                        <div class="kana-section-desc-card">
                            <p class="kana-section-desc">${descText}</p>
                        </div>
                    </div>
                    <div class="kana-grid kana-section-grid" data-category-grid="${cat.id}"></div>
                `;

                const sectionGrid = section.querySelector("[data-category-grid]");

                visibleChars.forEach((character) => {
                    const item = getDetail(character, type);
                    const button = document.createElement("button");
                    button.type = "button";
                    button.className = "kana-card";
                    button.innerHTML = `<strong>${character}</strong><span>${item.reading}</span>`;
                    button.addEventListener("click", () => {
                        grid.querySelectorAll(".is-selected").forEach((card) => card.classList.remove("is-selected"));
                        button.classList.add("is-selected");
                        show(character);
                    });

                    sectionGrid.append(button);

                    if (!firstMatchedButton) {
                        firstMatchedButton = { button, character };
                    }
                });

                grid.append(section);
            });

            if (totalMatches === 0) {
                const emptyEl = document.createElement("div");
                emptyEl.className = "kana-empty-state";
                emptyEl.innerHTML = `<p>Tidak ada karakter yang cocok dengan pencarian “${query}”.</p>`;
                grid.append(emptyEl);
            } else if (firstMatchedButton && !query) {
                firstMatchedButton.button.classList.add("is-selected");
                show(firstMatchedButton.character);
            } else if (firstMatchedButton && query) {
                firstMatchedButton.button.classList.add("is-selected");
                show(firstMatchedButton.character);
            }
        };

        search?.addEventListener("input", render);
        render();
    }

    window.KanaData = {
        getCharacters,
        getDetail,
        hiraRows,
        kataRows,
        roman,
        kataRoman,
        categoriesConfig
    };

    document.addEventListener("DOMContentLoaded", initLesson);
})();
