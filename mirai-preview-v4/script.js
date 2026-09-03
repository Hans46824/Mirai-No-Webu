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
    { character: "あい", romaji: "ai", meaning: "cinta" },
    { character: "うえ", romaji: "ue", meaning: "atas" },
    { character: "たち", romaji: "tachi", meaning: "berdiri / kami" },
    { character: "うめ", romaji: "ume", meaning: "bunga/buah plum" },
    { character: "みず", romaji: "mizu", meaning: "air" },
    { character: "はな", romaji: "hana", meaning: "bunga" },
    { character: "かえ", romaji: "kae", meaning: "ganti / tukar" },
    { character: "やま", romaji: "yama", meaning: "gunung" },
    { character: "ねこ", romaji: "neko", meaning: "kucing" },
    { character: "いぬ", romaji: "inu", meaning: "anjing" },
    { character: "つき", romaji: "tsuki", meaning: "bulan" },
    { character: "さくら", romaji: "sakura", meaning: "bunga sakura" },
    { character: "ほん", romaji: "hon", meaning: "buku" },
    { character: "そら", romaji: "sora", meaning: "langit" },
    { character: "ゆき", romaji: "yuki", meaning: "salju" },
    { character: "あめ", romaji: "ame", meaning: "hujan" },
    { character: "かわ", romaji: "kawa", meaning: "sungai" },
    { character: "とり", romaji: "tori", meaning: "burung" },
    { character: "ひかり", romaji: "hikari", meaning: "cahaya" },
    { character: "まち", romaji: "machi", meaning: "kota" },
    { character: "おちゃ", romaji: "ocha", meaning: "teh hijau" },
    { character: "きょう", romaji: "kyou", meaning: "hari ini" },
    { character: "しゃしん", romaji: "shashin", meaning: "foto" },
    { character: "きゅう", romaji: "kyuu", meaning: "sembilan" }
];

const wordBankKatakana = [
    { character: "アニメ", romaji: "anime", meaning: "animasi / anime" },
    { character: "カメラ", romaji: "kamera", meaning: "kamera" },
    { character: "ホテル", romaji: "hoteru", meaning: "hotel" },
    { character: "タクシー", romaji: "takushii", meaning: "taksi" },
    { character: "ラジオ", romaji: "rajio", meaning: "radio" },
    { character: "パン", romaji: "pan", meaning: "roti" },
    { character: "テレビ", romaji: "terebi", meaning: "televisi" },
    { character: "ドア", romaji: "doa", meaning: "pintu" },
    { character: "バス", romaji: "basu", meaning: "bus" },
    { character: "ワイン", romaji: "wain", meaning: "anggur" },
    { character: "マンガ", romaji: "manga", meaning: "komik" },
    { character: "アイス", romaji: "aisu", meaning: "es krim" },
    { character: "ビル", romaji: "biru", meaning: "gedung" },
    { character: "ノート", romaji: "nooto", meaning: "buku catatan" },
    { character: "ペン", romaji: "pen", meaning: "pena / pulpen" },
    { character: "ケーキ", romaji: "keeki", meaning: "kue" },
    { character: "コーヒー", romaji: "koohii", meaning: "kopi" },
    { character: "ベッド", romaji: "beddo", meaning: "tempat tidur" },
    { character: "シャツ", romaji: "shatsu", meaning: "kaus / kemeja" },
    { character: "ジュース", romaji: "juusu", meaning: "jus" },
    { character: "チョコ", romaji: "choko", meaning: "cokelat" },
    { character: "キャンプ", romaji: "kyanpu", meaning: "kemah / kemping" }
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

    combos.forEach(([kanaList, readings], comboIndex) => {
        kanaList.forEach((character, index) => {
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

function buildWordQuestions(scriptType = "hiragana") {
    const bank = getWordBank(scriptType);
    const selected = shuffle([...bank]).slice(0, 4);

    return selected.map((item, index) => {
        const kind = index % 2 === 0 ? "romaji" : "kana";
        const distractors = shuffle(
            bank.filter((candidate) => candidate.character !== item.character)
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

function buildMatchQuestion(scriptType = "hiragana") {
    const bank = getWordBank(scriptType);
    const selected = shuffle([...bank]).slice(0, 5);
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
                meaning: pair.meaning
            }))),
            rightOptions: shuffle(pairs.map((pair) => ({
                id: pair.id,
                romaji: pair.romaji
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

    const wordQuestions = buildWordQuestions(scriptType);
    const matchQuestion = buildMatchQuestion(scriptType);

    return [...standardQuestions, ...wordQuestions, matchQuestion];
}

function initKanaQuest() {
    const saved = {
        xp: 0,
        streak: 1,
        review: [],
        hiragana: { unlocked: 99, completed: [], best: {} },
        katakana: { unlocked: 99, completed: [], best: {} }
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
            id: 16 + index,
            chars: chars.join(" "),
            label: readings.join(" ")
        }))
    ];

    const displayChars = (chars) => {
        const str = Array.isArray(chars) ? chars.join(" ") : String(chars);
        if (script === "katakana") {
            return [...str].map((char) => {
                const code = char.codePointAt(0);
                return (code >= 0x3041 && code <= 0x3096)
                    ? String.fromCodePoint(code + 0x60)
                    : char;
            }).join("");
        }
        return str;
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

        const progress = Math.min(100, Math.round((saved[script].unlocked - 1) / 25 * 100));
        $("[data-script-progress]").textContent = `${progress}%`;
        $("[data-script-progress-bar]").style.width = `${progress}%`;

        $("[data-level-grid]").innerHTML = allLevels.map((level) => {
            const unlocked = level.id <= saved[script].unlocked;
            const completed = saved[script].completed.includes(level.id);

            return `
                <article class="level-card ${unlocked ? "is-unlocked" : "is-locked"} ${completed ? "is-completed" : ""}">
                    <div class="level-card-top">
                        <span>${completed ? "✓ Completed" : unlocked ? "🔓 Unlocked" : "🔒 Locked"}</span>
                        <b>${level.id < 11 ? level.name || `LV ${level.id}` : `LV ${level.id}`}</b>
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
    };

    const modes = [
        { label: "LV 1–2", levels: [1, 2] },
        { label: "LV 1–3", levels: [1, 2, 3] },
        { label: "LV 1–5", levels: [1, 2, 3, 4, 5] },
        { label: "LV 1–10", levels: Array.from({ length: 10 }, (_, index) => index + 1) },
        { label: "LV 6–10", levels: [6, 7, 8, 9, 10] },
        { label: `Basic ${script}`, levels: Array.from({ length: 10 }, (_, index) => index + 1) },
        { label: "Dakuten & Handakuten", levels: [11, 12, 13, 14, 15] },
        { label: "Combination / Yōon", levels: Array.from({ length: 11 }, (_, index) => 16 + index) },
        { label: "SEMUA MATERI", levels: Array.from({ length: 26 }, (_, index) => index + 1) },
        { label: "RANDOM CHALLENGE", levels: Array.from({ length: Math.min(26, saved[script].unlocked) }, (_, index) => index + 1) }
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

    function startPractice(levels) {
        const unlockedLevels = levels.filter((level) => level <= saved[script].unlocked);
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
            streak: 0,
            best: 0,
            xp: 0,
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
                <div class="match-container">
                    <div class="match-grid">
                        <div class="match-col match-col-left">
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
                                    >
                                        <span class="match-kana-char">${option.character}</span>
                                        <small class="match-meaning">(${option.meaning})</small>
                                    </button>
                                `;
                            }).join("")}
                        </div>
                        <div class="match-col match-col-right">
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
                                    >
                                        <span class="match-romaji-char">${option.romaji}</span>
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

            $("[data-answer-grid]").querySelectorAll(`[data-match-id="${matchedId}"]`).forEach((button) => {
                button.classList.remove("is-selected");
                button.classList.add("is-matched");
                button.disabled = true;
            });

            const counterEl = $("[data-question-prompt] .match-counter");
            if (counterEl) {
                counterEl.textContent = `(${match.matchedIds.length}/${match.total} selesai)`;
            }

            const feedback = $("[data-feedback]");
            feedback.hidden = false;

            if (match.matchedIds.length >= match.total) {
                feedback.className = "feedback is-good";
                feedback.innerHTML = "<strong>Semua pasangan benar! 🎉</strong><span>Lanjut ke sesi berikutnya.</span>";

                currentSession.results[currentSession.index] = {
                    state: "is-correct",
                    question,
                    value: "match-complete"
                };

                currentSession.streak += 1;
                currentSession.best = Math.max(currentSession.best, currentSession.streak);
                currentSession.xp += 20;

                setTimeout(() => {
                    currentSession.index += 1;
                    if (currentSession.index >= currentSession.questions.length) {
                        finishPractice();
                    } else {
                        renderQuestion();
                    }
                }, 850);
            } else {
                feedback.className = "feedback is-good";
                feedback.innerHTML = `<strong>Cocok! ✨</strong><span>${match.matchedIds.length} dari ${match.total} pasangan selesai.</span>`;
            }

            return;
        }

        const wrongLeftId = match.selectedLeft;
        const wrongRightId = match.selectedRight;

        const wrongLeftBtn = $("[data-answer-grid]").querySelector(`[data-match-side='left'][data-match-id="${wrongLeftId}"]`);
        const wrongRightBtn = $("[data-answer-grid]").querySelector(`[data-match-side='right'][data-match-id="${wrongRightId}"]`);

        if (wrongLeftBtn) wrongLeftBtn.classList.add("is-wrong-match");
        if (wrongRightBtn) wrongRightBtn.classList.add("is-wrong-match");

        const message = $("[data-feedback]");
        message.hidden = false;
        message.className = "feedback is-bad";
        message.innerHTML = "<strong>Belum cocok.</strong><span>Coba pilih pasangan yang sesuai.</span>";

        setTimeout(() => {
            match.selectedLeft = null;
            match.selectedRight = null;
            if (wrongLeftBtn) wrongLeftBtn.classList.remove("is-selected", "is-wrong-match");
            if (wrongRightBtn) wrongRightBtn.classList.remove("is-selected", "is-wrong-match");
        }, 450);
    }

    function answerQuestion(value, state = "answered") {
        if (currentSession.results[currentSession.index]) {
            return;
        }

        const question = currentSession.questions[currentSession.index];
        const correct = state !== "skipped" && value === question.answer.character;

        currentSession.results[currentSession.index] = {
            state: state === "skipped" ? "skipped" : correct ? "is-correct" : "is-wrong",
            question,
            value: correct ? question.answer.romaji : value
        };

        currentSession.streak = correct ? currentSession.streak + 1 : 0;
        currentSession.best = Math.max(currentSession.best, currentSession.streak);

        const earned = correct ? 10 + Math.max(0, currentSession.streak - 2) * 2 : 0;
        currentSession.xp += earned;

        const feedback = $("[data-feedback]");
        feedback.hidden = false;
        feedback.className = `feedback ${correct ? "is-good" : state === "skipped" ? "is-skip" : "is-bad"}`;

        if (correct) {
            feedback.innerHTML = `<strong>Benar! 🎉</strong><span>+${earned} XP${currentSession.streak > 2 ? ` • 🔥 ${currentSession.streak} streak` : ""}</span>`;
        } else if (state === "skipped") {
            feedback.innerHTML = `<strong>Soal dilewati</strong><span>Jawaban benar: ${question.answer.character} = ${question.answer.romaji}</span>`;
        } else {
            feedback.innerHTML = `<strong>Salah, tetap semangat.</strong><span>Jawaban benar: ${question.answer.character} = ${question.answer.romaji}</span>`;
        }

        $("[data-answer-grid]").querySelectorAll("button").forEach((button) => {
            button.disabled = true;
            if (button.dataset.answer === question.answer.character) {
                button.classList.add("is-answer");
            }
        });

        setTimeout(() => {
            currentSession.index += 1;
            if (currentSession.index >= currentSession.questions.length) {
                finishPractice();
            } else {
                renderQuestion();
            }
        }, 750);
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
        const wrong = currentSession.results.filter((result) => result.state === "is-wrong");
        const correct = currentSession.results.filter((result) => result.state === "is-correct").length;
        const accuracy = Math.round((correct / currentSession.questions.length) * 100);
        const perfect = accuracy === 100 ? 25 : 0;
        const total = currentSession.xp + perfect;

        saved.xp += total;

        if (accuracy >= 70) {
            const highest = Math.max(...currentSession.levels);
            saved[script].unlocked = Math.min(16, Math.max(saved[script].unlocked, highest + 1));
            saved[script].completed = [...new Set([...saved[script].completed, ...currentSession.levels])];
        }

        wrong.forEach((result) => {
            if (!saved.review.includes(result.question.answer.character)) {
                saved.review.push(result.question.answer.character);
            }
        });

        save();
        $("[data-practice-view]").hidden = true;
        $("[data-result-view]").hidden = false;
        document.body.classList.remove("is-practicing");

        $("[data-result-xp]").textContent = `+${total} XP`;
        $("[data-result-accuracy]").textContent = `${accuracy}%`;
        $("[data-result-correct]").textContent = correct;
        $("[data-result-wrong]").textContent = wrong.length;
        $("[data-result-time]").textContent = formatTime(Date.now() - currentSession.started);
        $("[data-result-streak]").textContent = `Best streak: ${currentSession.best}`;
        $("[data-mistake-list]").innerHTML = wrong.length
            ? `<h3>Review Kesalahan</h3>${wrong.map((result) => `
                <p>
                    <strong>${result.question.answer.character}</strong>
                    → kamu menjawab “${result.value || "skip"}”
                    <span>Jawaban benar: ${result.question.answer.romaji}</span>
                </p>
            `).join("")}`
            : `<p class="perfect-note">Sempurna. Tidak ada kesalahan untuk direview.</p>`;
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
