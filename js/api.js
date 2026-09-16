/**
 * MiraiData - Unified API & Data Service for MIRAI NO HANA
 * Provides consistent data, reading, Indonesian meaning, and stroke-order
 * across Kanji, Hiragana, and Katakana with persistent localStorage caching.
 */
(() => {
    const KANJI_API_BASE = "https://kanjiapi.dev/v1";
    let kanaDataCache = null;

    window.MiraiData = {
        /**
         * Translate English meaning/gloss into Bahasa Indonesia
         */
        async translate(text) {
            if (window.MiraiTranslator) {
                return window.MiraiTranslator.translateText(text);
            }
            return text;
        },

        translateSync(text) {
            if (window.MiraiTranslator) {
                return window.MiraiTranslator.translateSync(text);
            }
            return text;
        },

        /* =========================================================================
           KANJI API (KanjiAPI.dev)
           ========================================================================= */

        /**
         * Fetch list of kanji characters for a given JLPT level (5 to 1)
         */
        async getKanjiList(levelNum) {
            const cacheKey = `mnh_kapi_jlpt_${levelNum}`;
            try {
                const cached = localStorage.getItem(cacheKey);
                if (cached) {
                    const parsed = JSON.parse(cached);
                    if (Array.isArray(parsed) && parsed.length > 0) return parsed;
                }
            } catch (e) {}

            try {
                const res = await fetch(`${KANJI_API_BASE}/kanji/jlpt-${levelNum}`);
                if (!res.ok) throw new Error(`HTTP ${res.status}`);
                const data = await res.json();
                if (Array.isArray(data)) {
                    try {
                        localStorage.setItem(cacheKey, JSON.stringify(data));
                    } catch (e) {}
                    return data;
                }
            } catch (err) {
                console.warn(`[MiraiData] Gagal mengambil list JLPT N${levelNum}:`, err);
            }
            return [];
        },

        /**
         * Fetch kanji detail with Indonesian translation
         */
        async getKanjiDetail(character) {
            if (!character) return null;
            const cacheKey = `mnh_kapi_detail_${character}`;

            // Check persistent cache
            try {
                const cached = localStorage.getItem(cacheKey);
                if (cached) {
                    const parsed = JSON.parse(cached);
                    // Ensure Indonesian translation is present
                    if (parsed && parsed.meaningsId && parsed.meaningsId.length > 0) {
                        return parsed;
                    }
                }
            } catch (e) {}

            try {
                const res = await fetch(`${KANJI_API_BASE}/kanji/${encodeURIComponent(character)}`);
                if (!res.ok) throw new Error(`HTTP ${res.status}`);
                const raw = await res.json();

                // Translate English meanings into Indonesian
                const rawMeanings = raw.meanings || [];
                const translatedMeanings = await Promise.all(
                    rawMeanings.map((m) => this.translate(m))
                );

                const detail = {
                    kanji: raw.kanji,
                    grade: raw.grade,
                    stroke_count: raw.stroke_count,
                    meaningsEn: rawMeanings,
                    meanings: translatedMeanings,
                    meaningsId: translatedMeanings,
                    kun_readings: raw.kun_readings || [],
                    on_readings: raw.on_readings || [],
                    name_readings: raw.name_readings || [],
                    jlpt: raw.jlpt ? `N${raw.jlpt}` : null,
                    unicode: raw.unicode
                };

                try {
                    localStorage.setItem(cacheKey, JSON.stringify(detail));
                } catch (e) {}

                return detail;
            } catch (err) {
                console.warn(`[MiraiData] Gagal mengambil detail kanji ${character}:`, err);
                return null;
            }
        },

        /**
         * Fetch words for a kanji with Indonesian translation
         */
        async getKanjiWords(character) {
            if (!character) return [];
            const cacheKey = `mnh_kapi_words_${character}`;

            try {
                const cached = localStorage.getItem(cacheKey);
                if (cached) {
                    const parsed = JSON.parse(cached);
                    if (Array.isArray(parsed) && parsed.length > 0) return parsed;
                }
            } catch (e) {}

            try {
                const res = await fetch(`${KANJI_API_BASE}/words/${encodeURIComponent(character)}`);
                if (!res.ok) return [];
                const raw = await res.json();
                const words = [];

                for (const item of raw) {
                    const variant = item.variants?.[0];
                    const rawGloss = item.meanings?.[0]?.glosses?.slice(0, 2)?.join(", ");
                    if (variant && rawGloss) {
                        const translatedGloss = await this.translate(rawGloss);
                        words.push({
                            word: variant.written || variant.pronounced,
                            reading: variant.pronounced,
                            meaningEn: rawGloss,
                            meaning: translatedGloss
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
        },

        /* =========================================================================
           KANA API (Hiragana & Katakana)
           ========================================================================= */

        /**
         * Fetch all structured kana data (Hiragana / Katakana) from data/kana.json
         */
        async getKanaData() {
            if (kanaDataCache) return kanaDataCache;
            const cacheKey = "mnh_kana_full_dataset";
            try {
                const cached = localStorage.getItem(cacheKey);
                if (cached) {
                    kanaDataCache = JSON.parse(cached);
                    return kanaDataCache;
                }
            } catch (e) {}

            try {
                const res = await fetch("data/kana.json");
                if (res.ok) {
                    kanaDataCache = await res.json();
                    try {
                        localStorage.setItem(cacheKey, JSON.stringify(kanaDataCache));
                    } catch (e) {}
                    return kanaDataCache;
                }
            } catch (err) {
                console.warn("[MiraiData] Gagal memuat data/kana.json:", err);
            }
            return { hiragana: [], katakana: [] };
        },

        async getKanaList(scriptType = "hiragana") {
            const data = await this.getKanaData();
            return data[scriptType] || [];
        },

        async getKanaDetail(character, scriptType = "hiragana") {
            const list = await this.getKanaList(scriptType);
            return list.find((item) => item.character === character) || null;
        },

        /* =========================================================================
           STROKE ORDER API (Unified KanjiVG for Kanji, Hiragana, and Katakana)
           ========================================================================= */

        /**
         * Unified stroke path loader from KanjiVG CDN for Kanji and Kana alike
         */
        async getStrokeData(character) {
            if (window.getStrokeDataAsync) {
                return window.getStrokeDataAsync(character);
            }
            return null;
        }
    };
})();

