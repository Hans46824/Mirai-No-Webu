(() => {
    const page = document.querySelector(".kanji-practice-page");
    if (!page) return;
    const question = page.querySelector("[data-kanji-question]");
    const answers = page.querySelector("[data-kanji-answers]");
    const feedback = page.querySelector("[data-kanji-feedback]");
    const level = page.querySelector("[data-kanji-practice-level]");
    const strokeHost = document.createElement("div");
    strokeHost.className = "kanji-practice-stroke";
    question.after(strokeHost);
    let entries = [];
    let current;
    const shuffle = (items) => items.sort(() => Math.random() - 0.5);
    const next = () => {
        const pool = entries.filter((item) => !level.value || item.jlpt === level.value);
        if (!pool.length) return;
        current = pool[Math.floor(Math.random() * pool.length)];
        strokeHost.innerHTML = `<h3>Urutan menulis</h3><div class="stroke-stage is-fallback"><span class="stroke-fallback-glyph">${current.kanji}</span></div><p class="stroke-source">Animasi karakter Kanji</p>`;
        const choices = shuffle([current, ...shuffle(pool.filter((item) => item.kanji !== current.kanji)).slice(0, 2)]);
        question.textContent = current.kanji;
        feedback.hidden = true;
        answers.innerHTML = choices.map((item) => `<button type="button" data-answer="${item.kanji}">${item.meaning}</button>`).join("");
        answers.querySelectorAll("button").forEach((button) => button.addEventListener("click", () => {
            const correct = button.dataset.answer === current.kanji;
            feedback.hidden = false;
            feedback.className = `feedback ${correct ? "is-good" : "is-bad"}`;
            feedback.innerHTML = correct ? `<strong>Benar!</strong><span>${current.kanji} = ${current.meaning}</span>` : `<strong>Belum tepat.</strong><span>Jawaban: ${current.kanji} = ${current.meaning}</span>`;
            answers.querySelectorAll("button").forEach((item) => { item.disabled = true; if (item.dataset.answer === current.kanji) item.classList.add("is-answer"); });
        }));
    };
    level.addEventListener("change", next);
    fetch("data/kanji.json").then((response) => response.json()).then((data) => {
        entries = data;
        const extra = {
            N4: "悪安医意運駅屋員遠横園音科夏家画回海界開楽館漢帰起牛京強教近銀計研公考黒合国菜思試持式室質写習集住重春初少暑場心真親図世整昔全送族待代題茶昼長低店転田電冬東答頭同道読売買発発半病品風服物文別便歩妹味明野用曜理料旅",
            N3: "愛案以囲位違移因印英越援演煙央奥王温化荷過解格確額寄技義逆久旧居許境均禁句群経潔件険現限減故個護効構講混査再災妻採際在財罪雑酸賛支志師資識似守収修述術準序招証常状条職制性政勢精製税責接設絶銭祖素総造像増則測属続卒損退態団断築張提程適敵統銅導徳独任燃能破判批肥非備評富布普復複仏編弁保報務防夢迷綿輸容預欲翌乱略留領路輪率和",
            N2: "圧依液営衛映延可価革株刊幹貫疑規貴騎儀偶遇隅契掲携系敬景劇激券検権現効厚恒鉱抗稿郊皇紅刻穀骨困砂採載裁策冊蚕至私磁謝尺若樹需宗就柔従充純処署諸除傷将障城蒸職伸審慎振震薪推寸瀬清盛績専泉洗宣銭善相総像憎蔵臓存宅担探誕段暖値宙著庁頂潮賃痛敵展討届難乳燃悩脳派拝背肺俳泊博迫阪版否彼悲費飛評描秒布婦武幅払粉雰並閉片補暮宝訪豊暴密夢迷訳郵優欲幼翌乱覧裏律臨例歴論",
            N1: "亜哀挨曖握宛嵐威萎尉椅彙茨咽淫唄鬱畏謁怨媛艶旺臆俺苛牙瓦楷潰諧蓋骸柿顎葛釜韓玩伎祈畿揮毀窟勲薫傾恵憬憾懇采斎債塞崎削搾錯桟暫祉歯諮璽漆遮蛇酌寿潤遵庶叙匠抄宵肖彰宰腎錘随髄脆斉隻戚堆戴滞卓託諾濁旦稚畜逐窒嫡衷聴陳鎮墜貞諦摘滴溺督凸頓曇弐尿煮妊捻粘把覇排賠培剥箸肌鉢伴帥阪斑泌漂苗頻敏瓶扶符侮沸紛癖募墨翻凡摩麻岬妙冥麺耗厄躍沃雷絡欄吏痢履璃慄零錬炉弄麓脇惑湾腕"
        };
        Object.entries(extra).forEach(([jlpt, characters]) => [...characters].forEach((kanji) => entries.push({ kanji, meaning: `karakter ${kanji} (${jlpt})`, jlpt })));
        next();
    }).catch(() => { question.textContent = "Data kanji belum tersedia."; });
})();
