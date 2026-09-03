window.initKanjiDictionary = async function initKanjiDictionary() {
    const dictionary = document.querySelector("[data-kanji-dictionary]");
    if (!dictionary) return;

    const grid = dictionary.querySelector("[data-kanji-grid]");
    const count = dictionary.querySelector("[data-kanji-count]");
    const empty = dictionary.querySelector("[data-kanji-empty]");
    const detail = dictionary.querySelector("[data-kanji-detail]");
    const search = dictionary.querySelector("[data-kanji-search]");
    const jlpt = dictionary.querySelector("[data-kanji-jlpt]");
    const level = dictionary.querySelector("[data-kanji-level]");
    let strokes = dictionary.querySelector("[data-kanji-strokes]");
    let entries = [];
    let player;

    if (!strokes) {
        const label = document.createElement("label");
        label.innerHTML = 'Goresan<select data-kanji-strokes><option value="">Semua</option><option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option><option value="7">7</option><option value="8">8</option><option value="9">9</option><option value="10">10</option></select>';
        dictionary.querySelector(".dictionary-controls").append(label);
        strokes = label.querySelector("select");
    }
    if (!dictionary.querySelector("[data-random-kanji]")) {
        const random = document.createElement("button");
        random.className = "btn";
        random.type = "button";
        random.dataset.randomKanji = "";
        random.textContent = "KANJI ACAK";
        dictionary.querySelector(".dictionary-controls").append(random);
    }

    try {
        const response = await fetch("data/kanji.json");
        if (!response.ok) throw new Error("Data kamus tidak tersedia.");
        entries = await response.json();
        const advanced = {
            N4: "悪安医意運駅屋員遠横園音科夏家画回海界開楽館漢帰起牛京強教近銀計研公考黒合国菜思試持式室質写習集住重春初少暑場心真親図世整昔全送族待代題茶昼長低店転田電冬東答頭同道読売買発発半病品風服物文別便歩妹味明野用曜理料旅",
            N3: "愛案以囲位違移因印英越援演煙央奥王温化荷過解格確額寄技義逆久旧居許境均禁句群経潔件険現限減故個護効構講混査再災妻採際在財罪雑酸賛支志師資識似守収修述術準序招証常状条職制性政勢精製税責接設絶銭祖素総造像増則測属続卒損退態団断築張提程適敵統銅導徳独任燃能破判批肥非備評富布普復複仏編弁保報務防夢迷綿輸容預欲翌乱略留領路輪率和",
            N2: "圧依液営衛映延可価革株釜刊幹貫疑規貴騎儀偶遇隅契掲携系敬景劇激穴券険検権限現効厚恒鉱抗稿郊皇紅刻穀骨困砂採載裁策冊蚕至私磁謝尺若樹需宗就柔従充純処署諸除傷将障城蒸職伸審慎振震薪推寸瀬清盛税責績専泉洗宣銭善相総像憎蔵臓存宅担探誕段暖値宙著庁頂潮賃痛敵展討届難乳燃悩脳派拝背肺俳泊博迫阪版否彼悲費飛評描秒布婦武幅払粉雰並閉片補暮宝訪豊暴密夢迷訳郵優欲幼翌乱覧裏律臨例歴論",
            N1: "亜哀挨曖握宛嵐威萎尉椅彙茨咽淫唄鬱畏謁怨媛艶旺臆俺苛牙瓦楷潰諧蓋骸柿顎葛釜韓玩伎祈畿揮毀畿窟勲薫傾恵憬憾懇采采斎債塞崎削搾錯桟暫祉歯諮璽漆遮蛇酌寿潤遵庶叙匠抄宵肖彰宰腎錘随髄脆斉隻戚堆戴滞卓託諾濁旦稚畜逐窒嫡衷聴陳鎮墜貞諦摘滴溺督凸頓曇弐尿煮妊捻粘把覇排賠培剥箸肌鉢伴帥阪斑泌漂苗頻敏瓶扶符侮沸紛癖募墨翻凡摩麻岬妙冥麺耗厄躍沃雷絡欄吏痢履璃慄零錬炉弄麓脇惑湾腕"
        };
        Object.entries(advanced).forEach(([jlpt, characters]) => {
            [...characters].forEach((kanji) => entries.push({ kanji, meaning: "karakter kanji", onyomi: [], kunyomi: [], jlpt, level: jlpt === "N4" ? "Menengah" : "Lanjutan", words: [], sentence: { japanese: kanji, reading: "", meaning: "" } }));
        });
    } catch (error) {
        count.textContent = "Data belum dapat dimuat. Jalankan situs melalui Live Server lalu coba lagi.";
        return;
    }

    function renderDetail(item) {
        player?.destroy();
            detail.innerHTML = `<div class="kanji-detail-head"><strong>${item.kanji}</strong><div><p class="card-number">${item.jlpt} / ${item.level} · ${item.strokes || window.MIRAI_STROKE_DATA?.[item.kanji]?.paths.length || "—"} GORESAN</p><h3>${item.meaning}</h3><p><b>Onyomi:</b> ${item.onyomi.join("、") || "—"}<br><b>Kunyomi:</b> ${item.kunyomi.join("、") || "—"}</p></div></div><h4>Urutan Menulis</h4><div data-stroke-player></div><h4>Kosakata</h4><ul>${item.words.map((word) => `<li><b>${word.word}</b> <span>${word.reading}</span> — ${word.meaning}</li>`).join("")}</ul><h4>Contoh kalimat</h4><p class="sentence"><b>${item.sentence.japanese}</b><br><span>${item.sentence.reading}</span><br>${item.sentence.meaning}</p>`;
        player = window.createStrokePlayer(detail.querySelector("[data-stroke-player]"), item.kanji, item.strokes || 4);
    }

    function visibleEntries() {
        const query = search.value.trim().toLowerCase();
        return entries.filter((item) => {
            const searchable = [item.kanji, item.meaning, ...item.onyomi, ...item.kunyomi, ...item.words.flatMap((word) => [word.word, word.reading, word.meaning])].join(" ").toLowerCase();
            const strokeCount = item.strokes || window.MIRAI_STROKE_DATA?.[item.kanji]?.paths.length || 0;
            return (!query || searchable.includes(query)) && (!jlpt.value || item.jlpt === jlpt.value) && (!level.value || item.level === level.value) && (!strokes?.value || strokeCount === Number(strokes.value));
        });
    }

    function render() {
        const visible = visibleEntries();
        grid.replaceChildren();
        count.textContent = `Menampilkan ${visible.length} kanji`;
        empty.hidden = visible.length > 0;
        visible.forEach((item) => {
            const button = document.createElement("button");
            button.type = "button";
            button.className = "kanji-card";
            button.innerHTML = `<strong>${item.kanji}</strong><span>${item.meaning}</span><em>${item.jlpt}</em>`;
            button.addEventListener("click", () => renderDetail(item));
            grid.append(button);
        });
        if (visible.length) renderDetail(visible[0]);
        else detail.innerHTML = "<p>Pilih pencarian lain untuk melihat detail karakter.</p>";
    }

    [search, jlpt, level, strokes].filter(Boolean).forEach((control) => {
        control.addEventListener("input", render);
        control.addEventListener("change", render);
    });
    dictionary.querySelector("[data-random-kanji]")?.addEventListener("click", () => {
        const visible = visibleEntries();
        if (visible.length) renderDetail(visible[Math.floor(Math.random() * visible.length)]);
    });
    render();
    setupTabs();
};

function setupTabs() {
    const practiceLink = document.querySelector(".dictionary-practice-link a");
    const dictionaryCta = document.querySelector(".dictionary-practice-link");
    if (dictionaryCta && !dictionaryCta.querySelector("[href=\"latihan-kanji.html\"]")) {
        const kanjiLink = document.createElement("a");
        kanjiLink.className = "btn";
        kanjiLink.href = "latihan-kanji.html";
        kanjiLink.textContent = "LATIHAN KANJI →";
        dictionaryCta.append(kanjiLink);
    }
    document.querySelectorAll("[data-script-tab]").forEach((tab) => {
        tab.addEventListener("click", () => {
            const mode = tab.dataset.scriptTab;
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
        });
    });

    const activeTab = document.querySelector("[data-script-tab].is-active");
    if (activeTab && activeTab.dataset.scriptTab !== "kanji") {
        renderKanaPanel(activeTab.dataset.scriptTab);
    }
}

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
