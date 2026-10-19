/**
 * File: js/kana.js
 * Fungsi: Pengelola modul tabel aksara Kana (Hiragana & Katakana), filter Gojuuon/Dakuon/Yoon, pencarian, dan audio pelafalan.
 * Penggunaan: kamus/index.html dan kamus/kanji.html.
*/

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

function getStrokeCount(character) {
  if (!character) return 0;
  if (window.MIRAI_STROKE_DATA && window.MIRAI_STROKE_DATA[character]?.paths?.length) {
    return window.MIRAI_STROKE_DATA[character].paths.length;
  }
  const chars = Array.from(character);
  if (window.MIRAI_STROKE_DATA) {
    let total = 0;
    for (const ch of chars) {
    total += window.MIRAI_STROKE_DATA[ch]?.paths?.length || 0;
    }
    if (total > 0) return total;
  }
  return 3;
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

  const strokes = getStrokeCount(character);
  const example = examples[character] || [character, reading || "bunyi", "contoh penggunaan"];
  return { character, reading: reading || "bunyi gabungan", example, strokes };
}

function initLesson() {
  const type = document.body.dataset.kanaPage;
  if (!type) return;

  const grid = document.querySelector("[data-kana-grid]");
  const detail = document.querySelector("[data-kana-detail]");
  const search = document.querySelector("[data-kana-lesson-search]");
  let player;
  let selectedKanaChar = null;

  function show(character) {
    selectedKanaChar = character;
    const item = getDetail(character, type);
    player?.destroy();
    detail.innerHTML = `
                <p class="card-number">${type.toUpperCase()} / ${item.reading} • ${item.strokes} Goresan</p>
                <div class="selected-kana">${character}</div>
                <div class="kana-detail-audio-actions" style="display:flex; gap:8px; align-items:center;">
                    <button type="button" class="btn-kana-audio" data-speak-char="${character}" title="Lafalkan huruf ${character} (Normal)">
                        <span>🔊</span>
                    </button>
                    <button type="button" class="btn-kana-audio btn-audio-slow" data-speak-char-slow="${character}" title="Lafalkan huruf ${character} perlahan (Slow-Mo)">
                        <span>🐢</span>
                    </button>
                </div>
                <h3>Goresan Karakter (${item.strokes} Goresan)</h3>
                <p>Ikuti arah setiap goresan, lalu ulangi perlahan dengan tanganmu.</p>
                <div data-stroke-player></div>
                <h4>Contoh kata</h4>
                <div class="word-examples">
                    <p><b>${item.example[0]}</b><span>${item.example[1]}</span>${item.example[2]} <button type="button" class="mini-audio-btn" data-speak-word="${item.example[0]}" title="Dengarkan pelafalan ${item.example[0]}">🔊</button> <button type="button" class="mini-audio-btn btn-audio-slow" data-speak-word-slow="${item.example[0]}" title="Dengarkan pelan ${item.example[0]}">🐢</button></p>
                </div>
            `;
    detail.querySelector("[data-speak-char]")?.addEventListener("click", () => {
      window.speakText ? window.speakText(character, "ja-JP", false) : speakJapanese(character);
    });
    detail.querySelector("[data-speak-char-slow]")?.addEventListener("click", () => {
      window.speakText ? window.speakText(character, "ja-JP", true) : speakJapanese(character);
    });
    detail.querySelectorAll("[data-speak-word]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const word = btn.dataset.speakWord;
        window.speakText ? window.speakText(word, "ja-JP", false) : speakJapanese(word);
      });
    });
    detail.querySelectorAll("[data-speak-word-slow]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const word = btn.dataset.speakWordSlow;
        window.speakText ? window.speakText(word, "ja-JP", true) : speakJapanese(word);
      });
    });
    player = window.createStrokePlayer(detail.querySelector("[data-stroke-player]"), character, item.strokes, {
      showClear: true,
      mode: type,
      onSelectCharacter: (char) => show(char),
      onClear: () => renderBlankState()
    });
  }

  const renderBlankState = () => {
    player?.destroy();
    selectedKanaChar = null;
    grid.querySelectorAll(".kana-card.is-selected").forEach((btn) => btn.classList.remove("is-selected"));
    detail.innerHTML = `
      <div data-stroke-player></div>
    `;
    player = window.createStrokePlayer(detail.querySelector("[data-stroke-player]"), null, 0, {
      showClear: true,
      mode: type,
      onSelectCharacter: (char) => show(char),
      onClear: () => renderBlankState()
    });
  };

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
      if (selectedKanaChar === character) {
        renderBlankState();
      } else {
        grid.querySelectorAll(".is-selected").forEach((card) => card.classList.remove("is-selected"));
        button.classList.add("is-selected");
        show(character);
        window.speakText ? window.speakText(character, "ja-JP") : speakJapanese(character);
      }
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
    } else if (query && firstMatchedButton) {
      firstMatchedButton.button.classList.add("is-selected");
      show(firstMatchedButton.character);
    } else if (!query && !detail.querySelector(".unified-canvas-stage")) {
      renderBlankState();
    }
  };

  search?.addEventListener("input", render);
  render();
}


const MiraiWeakKana = {
  getAll() {
    try {
    const raw = localStorage.getItem("mirai_weak_kana");
    if (!raw) return {};
    const parsed = JSON.parse(raw);
    return typeof parsed === "object" && parsed !== null ? parsed : {};
    } catch (e) {
    return {};
    }
  },
  recordMistake(character, romaji = "", scriptType = "hiragana") {
    if (!character) return;
    try {
    const data = this.getAll();
    if (!data[character]) {
    data[character] = {
      character,
      romaji: romaji || "",
      script: scriptType,
      count: 1,
      lastMistake: Date.now()
    };
    } else {
    data[character].count = (data[character].count || 1) + 1;
    data[character].lastMistake = Date.now();
    if (romaji) data[character].romaji = romaji;
    if (scriptType) data[character].script = scriptType;
    }
    localStorage.setItem("mirai_weak_kana", JSON.stringify(data));
    } catch (e) {
    console.warn("Gagal menyimpan mirai_weak_kana:", e);
    }
  },
  recordCorrect(character) {
    if (!character) return;
    try {
    const data = this.getAll();
    if (data[character]) {
    data[character].count = (data[character].count || 1) - 1;
    if (data[character].count <= 0) {
      delete data[character];
    }
    localStorage.setItem("mirai_weak_kana", JSON.stringify(data));
    }
    } catch (e) {}
  },
  getList(scriptType = null) {
    const all = this.getAll();
    const list = Object.values(all);
    if (!scriptType) return list;
    return list.filter((item) => !item.script || item.script === scriptType);
  },
  getCharacters(scriptType = null) {
    return this.getList(scriptType).map((item) => item.character);
  },
  clear() {
    try {
    localStorage.removeItem("mirai_weak_kana");
    } catch (e) {}
  }
};

window.MiraiWeakKana = MiraiWeakKana;


const bunpouSentences = [
  {
    meaning: "Saya adalah murid / pelajar",
    romaji: "Watashi wa gakusei desu",
    kana: "わたし は がくせい です",
    kanaText: "わたしはがくせいです",
    tokensKana: ["わたし", "は", "がくせい", "です"],
    tokensRomaji: ["Watashi", "wa", "gakusei", "desu"],
    target: ["わたし", "は", "がくせい", "です"],
    tokens: ["わたし", "は", "がくせい", "です"]
  },
  {
    meaning: "Saya belajar bahasa Jepang",
    romaji: "Watashi wa nihongo o benkyou shimasu",
    kana: "わたし は にほんご を べんきょうします",
    kanaText: "わたしはにほんごをべんきょうします",
    tokensKana: ["わたし", "は", "にほんご", "を", "べんきょうします"],
    tokensRomaji: ["Watashi", "wa", "nihongo", "o", "benkyou shimasu"],
    target: ["わたし", "は", "にほんご", "を", "べんきょうします"],
    tokens: ["わたし", "は", "にほんご", "を", "べんきょうします"]
  },
  {
    meaning: "Ini adalah buku milik saya",
    romaji: "Kore wa watashi no hon desu",
    kana: "これ は わたし の ほん です",
    kanaText: "これはわたしのほんです",
    tokensKana: ["これ", "は", "わたし", "の", "ほん", "です"],
    tokensRomaji: ["Kore", "wa", "watashi", "no", "hon", "desu"],
    target: ["これ", "は", "わたし", "の", "ほん", "です"],
    tokens: ["これ", "は", "わたし", "の", "ほん", "です"]
  },
  {
    meaning: "Setiap hari saya minum air putih",
    romaji: "Mainichi mizu o nomimasu",
    kana: "まいにち みず を のみます",
    kanaText: "まいにちみずをのみます",
    tokensKana: ["まいにち", "みず", "を", "のみます"],
    tokensRomaji: ["Mainichi", "mizu", "o", "nomimasu"],
    target: ["まいにち", "みず", "を", "のみます"],
    tokens: ["まいにち", "みず", "を", "のみます"]
  },
  {
    meaning: "Besok saya pergi ke sekolah",
    romaji: "Ashita gakkou e ikimasu",
    kana: "あした がっこう へ いきます",
    kanaText: "あしたがっこうへいきます",
    tokensKana: ["あした", "がっこう", "へ", "いきます"],
    tokensRomaji: ["Ashita", "gakkou", "e", "ikimasu"],
    target: ["あした", "がっこう", "へ", "いきます"],
    tokens: ["あした", "がっこう", "へ", "いきます"]
  },
  {
    meaning: "Kucing itu ada di bawah meja",
    romaji: "Neko wa tsukue no shita ni imasu",
    kana: "ねこ は つくえ の した に います",
    kanaText: "ねこはつくえのしたにいます",
    tokensKana: ["ねこ", "は", "つくえ", "の", "した", "に", "います"],
    tokensRomaji: ["Neko", "wa", "tsukue", "no", "shita", "ni", "imasu"],
    target: ["ねこ", "は", "つくえ", "の", "した", "に", "います"],
    tokens: ["ねこ", "は", "つくえ", "の", "した", "に", "います"]
  },
  {
    meaning: "Makan ramen enak di restoran",
    romaji: "Resutoran de oishii raamen o tabemasu",
    kana: "レストラン で おいしい ラーメン を たべます",
    kanaText: "レストランでおいしいラーメンをたべます",
    tokensKana: ["レストラン", "で", "おいしい", "ラーメン", "を", "たべます"],
    tokensRomaji: ["Resutoran", "de", "oishii", "raamen", "o", "tabemasu"],
    target: ["レストラン", "で", "おいしい", "ラーメン", "を", "たべます"],
    tokens: ["レストラン", "で", "おいしい", "ラーメン", "を", "たべます"]
  },
  {
    meaning: "Saya suka anime dan manga Jepang",
    romaji: "Watashi wa anime to manga ga suki desu",
    kana: "わたし は アニメ と マンガ が すきです",
    kanaText: "わたしはアニメとマンガがすきです",
    tokensKana: ["わたし", "は", "アニメ", "と", "マンガ", "が", "すきです"],
    tokensRomaji: ["Watashi", "wa", "anime", "to", "manga", "ga", "suki desu"],
    target: ["わたし", "は", "アニメ", "と", "マンガ", "が", "すきです"],
    tokens: ["わたし", "は", "アニメ", "と", "マンガ", "が", "すきです"]
  },
  {
    meaning: "Hari ini cuacanya sangat dingin",
    romaji: "Kyou no tenki wa totemo samui desu",
    kana: "きょう の てんき は とても さむいです",
    kanaText: "きょうのてんきはとてもさむいです",
    tokensKana: ["きょう", "の", "てんき", "は", "とても", "さむいです"],
    tokensRomaji: ["Kyou", "no", "tenki", "wa", "totemo", "samui desu"],
    target: ["きょう", "の", "てんき", "は", "とても", "さむいです"],
    tokens: ["きょう", "の", "てんき", "は", "とても", "さむいです"]
  },
  {
    meaning: "Tolong baca buku bahasa Jepang ini",
    romaji: "Kono nihongo no hon o yonde kudasai",
    kana: "この にほんご の ほん を よんでください",
    kanaText: "このにほんごのほんをよんでください",
    tokensKana: ["この", "にほんご", "の", "ほん", "を", "よんでください"],
    tokensRomaji: ["Kono", "nihongo", "no", "hon", "o", "yonde kudasai"],
    target: ["この", "にほんご", "の", "ほん", "を", "よんでください"],
    tokens: ["この", "にほんご", "の", "ほん", "を", "よんでください"]
  }
];


function speakJapanese(text) {
  if (!text || !("speechSynthesis" in window)) return;
  try {
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "ja-JP";
    utterance.rate = 0.88;
    window.speechSynthesis.speak(utterance);
  } catch (e) {
    console.warn("Speech synthesis error:", e);
  }
}
window.speakJapanese = speakJapanese;

window.BunpouData = {
  sentences: bunpouSentences
};

window.KanaData = {
  getCharacters,
  getDetail,
  getStrokeCount,
  hiraRows,
  kataRows,
  roman,
  kataRoman,
  categoriesConfig,
  weakKana: MiraiWeakKana,
  bunpou: window.BunpouData,
  speak: speakJapanese
};

document.addEventListener("DOMContentLoaded", initLesson);
})();
