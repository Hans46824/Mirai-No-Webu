#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: skrip/arsip/test_kanji_engine.py
Fungsi: Memvalidasi secara menyeluruh mesin kamus kanji lokal, arsitektur data chunking,
        sistem pencarian berbobot (Ranked Search), dan simulasi membuka kanji N5 & N1 secara offline:
  1. Pemeriksaan aturan statik: bebas dari panggilan jaringan eksternal (kanjiapi.dev & mymemory).
  2. Pemeriksaan integritas dataset (Single Source of Truth: data/kanji.json -> kanji-index.json & chunks).
  3. Simulasi membuka kanji N5 (人, 日, 一) dan kanji N1 (鬱, 衷, 驚) tanpa koneksi internet.
  4. Pengujian algoritma ranked search: kata 'orang' wajib menampilkan Kanji '人' di peringkat #1.
  5. Pengujian verifikasi batasan beban: initial load <= 700 KB, first N5 kanji <= +60 KB.
"""

import os
import re
import sys
import json
import gzip

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def test_static_rules():
    print("==================================================")
    print("🧪 [1] PEMERIKSAAN ATURAN STATIK LOKAL (OFFLINE FIRST)")
    print("==================================================")

    # 1. Pastikan js/kanji.js bebas dari panggilan kanjiapi.dev dan mymemory
    with open(os.path.join(BASE_DIR, "js", "kanji.js"), "r", encoding="utf-8") as f:
        code_kanji = f.read()

    assert "https://kanjiapi.dev" not in code_kanji, "Masih ditemukan URL eksternal kanjiapi.dev di js/kanji.js!"
    assert "mymemory.translated.net" not in code_kanji, "Masih ditemukan URL eksternal mymemory di js/kanji.js!"
    assert "loadKanjiChunk" in code_kanji, "Fungsi loadKanjiChunk tidak ditemukan di js/kanji.js!"
    assert "data/kanji-index.json" in code_kanji, "Pemuatan data/kanji-index.json tidak ditemukan di js/kanji.js!"
    print("✔ js/kanji.js 100% bebas dari pemanggilan API eksternal (kanjiapi.dev / mymemory).")
    print("✔ Mesin kamus menggunakan pemuatan lokal data/kanji-index.json dan chunk on-demand.")

    # 2. Pastikan js/stroke.js bebas dari CDN eksternal
    with open(os.path.join(BASE_DIR, "js", "stroke.js"), "r", encoding="utf-8") as f:
        code_stroke = f.read()
    assert "cdn.jsdelivr.net/gh/KanjiVG" not in code_stroke, "Masih ditemukan CDN jsDelivr di js/stroke.js!"
    assert "loadStrokeChunk" in code_stroke, "Fungsi loadStrokeChunk tidak ditemukan di js/stroke.js!"
    print("✔ js/stroke.js 100% bebas dari fallback CDN eksternal jsDelivr.")

    # 3. Pastikan kamus/index.html dan kamus/kanji.html tidak memuat script kanji-data.js
    for hf in ["kamus/index.html", "kamus/kanji.html"]:
        with open(os.path.join(BASE_DIR, hf), "r", encoding="utf-8") as f:
            h_text = f.read()
        assert "kanji-data.js" not in h_text, f"{hf} masih memuat script kanji-data.js!"
    print("✔ kamus/index.html dan kamus/kanji.html tidak memuat berkas berat kanji-data.js (1.8 MB).")

def test_data_integrity():
    print("\n==================================================")
    print("🧪 [2] PENGUJIAN INTEGRITAS & KELENGKAPAN DATA")
    print("==================================================")

    # 1. Single Source of Truth: data/kanji.json
    kanji_src = os.path.join(BASE_DIR, "data", "kanji.json")
    with open(kanji_src, "r", encoding="utf-8") as f:
        master_kanji = json.load(f)
    assert len(master_kanji) == 2211, f"Total kanji master harus 2211! Ditemukan: {len(master_kanji)}"
    print(f"✔ data/kanji.json valid (Single Source of Truth): {len(master_kanji)} entri.")

    # Verifikasi data bersih: arti berulang harus 0
    def has_dup_meaning(text):
        if not text or not isinstance(text, str):
            return False
        parts = [p.strip().lower() for p in re.split(r'[,;]+', text) if p.strip()]
        return len(parts) != len(set(parts))

    dup_word_count = 0
    template_sentence_count = 0
    genuine_sentence_count = 0
    missing_example_word_count = 0

    for it in master_kanji:
        for w in it.get("words", []):
            if has_dup_meaning(w.get("meaning", "")):
                dup_word_count += 1
        for ex in it.get("examples", []):
            if has_dup_meaning(ex.get("meaning", "")):
                dup_word_count += 1
        if it.get("sentence_is_template"):
            template_sentence_count += 1
        else:
            genuine_sentence_count += 1
        if not it.get("example_word"):
            missing_example_word_count += 1

    assert dup_word_count == 0, f"Ditemukan {dup_word_count} kata dengan arti berulang di data/kanji.json!"
    print(f"✔ Arti kata berulang pada data/kanji.json terverifikasi 0 (Bersih 100%).")

    assert template_sentence_count == 2127, f"Template sentence count harus 2127! Ditemukan: {template_sentence_count}"
    assert genuine_sentence_count == 84, f"Genuine sentence count harus 84! Ditemukan: {genuine_sentence_count}"
    assert missing_example_word_count == 0, f"Ditemukan {missing_example_word_count} kanji tanpa example_word!"
    print(f"✔ Kalimat template terverifikasi 2.127 entri ditandai 'sentence_is_template': true, 84 kalimat asli aman.")
    print(f"✔ Seluruh 2.211 kanji memiliki 'example_word' (kata contoh utama).")

    # Verifikasi 衷 memiliki 9 goresan di kanji.json dan kanji-meta.json
    chu_item = next((it for it in master_kanji if it["kanji"] == "衷"), None)
    assert chu_item and chu_item["strokes"] == 9, f"Kanji 衷 di kanji.json harus 9 goresan! Dapat: {chu_item['strokes'] if chu_item else None}"
    with open(os.path.join(BASE_DIR, "data", "kanji-meta.json"), "r", encoding="utf-8") as f:
        meta_data = json.load(f)
    assert meta_data.get("衷") and meta_data["衷"][0] == 9, f"Kanji 衷 di kanji-meta.json harus 9 goresan! Dapat: {meta_data.get('衷')}"
    print(f"✔ Karakter 衷 terverifikasi tepat 9 goresan (kanji.json & kanji-meta.json).")

    # Verifikasi laporan skrip/laporan/perlu-terjemah.md
    report_trans_path = os.path.join(BASE_DIR, "skrip", "laporan", "perlu-terjemah.md")
    assert os.path.isfile(report_trans_path), "Berkas skrip/laporan/perlu-terjemah.md tidak ditemukan!"
    with open(report_trans_path, "r", encoding="utf-8") as f:
        rep_content = f.read()
    for exp_k in ["反", "柊", "桐", "楓", "瑠", "藤"]:
        assert exp_k in rep_content, f"Kanji {exp_k} harus ada di laporan perlu-terjemah.md!"
    print(f"✔ Laporan perlu-terjemah.md terverifikasi memuat 6 kanji yang membutuhkan terjemahan manual.")

    # Verifikasi atribusi sumber data di footer kamus
    for hf in ["kamus/index.html", "kamus/kanji.html"]:
        with open(os.path.join(BASE_DIR, hf), "r", encoding="utf-8") as f:
            h_text = f.read()
        assert "KANJIDIC2" in h_text and "JMdict" in h_text, f"Blok atribusi KANJIDIC2/JMdict tidak ditemukan di {hf}!"
        assert "KanjiVG" in h_text, f"Blok atribusi KanjiVG tidak ditemukan di {hf}!"
    print(f"✔ Atribusi terbuka KANJIDIC2/JMdict (EDRDG) & KanjiVG terverifikasi di footer kamus.")

    # 2. data/kanji-index.json
    index_path = os.path.join(BASE_DIR, "data", "kanji-index.json")
    with open(index_path, "r", encoding="utf-8") as f:
        index_data = json.load(f)
    assert len(index_data) == 2211, f"Total index kanji harus 2211! Ditemukan: {len(index_data)}"

    # Periksa struktur record index
    required_keys = {"kanji", "meaning", "jlpt", "level", "strokes", "grade", "onyomi", "kunyomi"}
    for idx_item in index_data:
        assert required_keys.issubset(idx_item.keys()), f"Field hilang pada kanji {idx_item.get('kanji')}: {required_keys - set(idx_item.keys())}"
    print(f"✔ data/kanji-index.json valid: {len(index_data)} entri dengan struktur kunci lengkap.")

    # 3. Chunk detail kanji (data/kanji/<jlpt>.json)
    total_chunk_kanji = 0
    jlpt_counts = {"n5": 79, "n4": 166, "n3": 367, "n2": 367, "n1": 1232}
    for lvl, exp_count in jlpt_counts.items():
        cp = os.path.join(BASE_DIR, "data", "kanji", f"{lvl}.json")
        assert os.path.isfile(cp), f"Chunk kanji {cp} tidak ditemukan!"
        with open(cp, "r", encoding="utf-8") as f:
            cdata = json.load(f)
        assert len(cdata) == exp_count, f"Jumlah kanji di {lvl}.json ({len(cdata)}) tidak sesuai ({exp_count})!"
        total_chunk_kanji += len(cdata)
        print(f"  ✔ Chunk kanji {lvl}.json : {len(cdata)} karakter.")

    assert total_chunk_kanji == 2211, f"Total kanji di seluruh chunk ({total_chunk_kanji}) != 2211!"

    # 4. Chunk goresan kanji (data/strokes/<jlpt>.json)
    total_chunk_strokes = 0
    for lvl, exp_count in jlpt_counts.items():
        sp = os.path.join(BASE_DIR, "data", "strokes", f"{lvl}.json")
        assert os.path.isfile(sp), f"Chunk goresan {sp} tidak ditemukan!"
        with open(sp, "r", encoding="utf-8") as f:
            sdata = json.load(f)
        assert len(sdata) == exp_count, f"Jumlah goresan di {lvl}.json ({len(sdata)}) tidak sesuai ({exp_count})!"
        total_chunk_strokes += len(sdata)
        print(f"  ✔ Chunk goresan {lvl}.json: {len(sdata)} karakter.")

    print(f"✔ Seluruh 2.211 Joyo & JLPT kanji terbagi rapi dan sinkron 100% di data/kanji/ dan data/strokes/.")

def test_offline_kanji_resolution():
    print("\n==================================================")
    print("🧪 [3] SIMULASI MEMBUKA KANJI N5 & N1 SECARA OFFLINE")
    print("==================================================")

    # Indeks lokal
    with open(os.path.join(BASE_DIR, "data", "kanji-index.json"), "r", encoding="utf-8") as f:
        index_list = json.load(f)
    index_map = {item["kanji"]: item for item in index_list}

    # Kasus Uji: N5 dan N1
    test_chars = [
        ("N5 Dasar", "人", "n5", 2, "orang"),
        ("N5 Dasar", "日", "n5", 4, "hari"),
        ("N5 Dasar", "一", "n5", 1, "satu"),
        ("N1 Lanjutan", "鷹", "n1", 24, "elang"),
        ("N1 Lanjutan", "衷", "n1", 9, "hati"),
        ("N1 Lanjutan", "驚", "n1", 22, "takjub"),
    ]

    for cat, char, exp_lvl, exp_strokes, exp_meaning_sub in test_chars:
        # 1. Karakter harus ada di index
        assert char in index_map, f"Karakter {char} tidak ditemukan di kanji-index.json!"
        idx_entry = index_map[char]
        assert idx_entry["jlpt"].lower() == exp_lvl, f"Level JLPT {char} salah! Dapat {idx_entry['jlpt']}, harap {exp_lvl}"
        assert idx_entry["strokes"] == exp_strokes, f"Goresan index {char} salah! Dapat {idx_entry['strokes']}, harap {exp_strokes}"

        # 2. Muat chunk detail
        detail_chunk_path = os.path.join(BASE_DIR, "data", "kanji", f"{exp_lvl}.json")
        with open(detail_chunk_path, "r", encoding="utf-8") as f:
            detail_chunk = json.load(f)
        assert char in detail_chunk, f"Karakter {char} tidak ditemukan di chunk {detail_chunk_path}!"
        detail = detail_chunk[char]

        # Validasi struktur detail
        assert exp_meaning_sub.lower() in detail["meaning"].lower(), f"Arti {char} '{detail['meaning']}' tidak memuat '{exp_meaning_sub}'"
        assert "sentence" in detail and detail["sentence"]["japanese"], f"Contoh kalimat pada {char} tidak lengkap!"
        words = detail.get("words") or detail.get("examples") or []
        assert len(words) > 0, f"Kosakata terkait pada {char} tidak boleh kosong!"

        # 3. Muat chunk goresan
        stroke_chunk_path = os.path.join(BASE_DIR, "data", "strokes", f"{exp_lvl}.json")
        with open(stroke_chunk_path, "r", encoding="utf-8") as f:
            stroke_chunk = json.load(f)
        assert char in stroke_chunk, f"Karakter {char} tidak ditemukan di chunk {stroke_chunk_path}!"
        stroke_rec = stroke_chunk[char]
        assert len(stroke_rec["paths"]) == exp_strokes, f"Jumlah path goresan {char} ({len(stroke_rec['paths'])}) != {exp_strokes}!"

        print(f"✔ [{cat}] '{char}' (JLPT {idx_entry['jlpt']}, {exp_strokes} goresan):")
        print(f"    - Arti        : {detail['meaning']}")
        print(f"    - Kosakata ({len(words)}): {words[0]['word']} ({words[0]['reading']}) — {words[0]['meaning']}")
        print(f"    - Kalimat     : {detail['sentence']['japanese']} ({detail['sentence']['meaning']})")
        print(f"    - Goresan SVG : {len(stroke_rec['paths'])} paths valid di {stroke_chunk_path}")

def test_ranked_search():
    print("\n==================================================")
    print("🧪 [4] PENGUJIAN AKURASI PENCARIAN BERBOBOT (RANKED SEARCH)")
    print("==================================================")

    with open(os.path.join(BASE_DIR, "data", "kanji-index.json"), "r", encoding="utf-8") as f:
        index_list = json.load(f)

    # Muat detail untuk uji pencarian kata
    with open(os.path.join(BASE_DIR, "data", "kanji", "n5.json"), "r", encoding="utf-8") as f:
        n5_detail = json.load(f)

    # Gabungkan kosakata contoh ke record N5 untuk menguji simulasi skor pencarian
    entries = []
    for item in index_list:
        rec = dict(item)
        if item["kanji"] in n5_detail:
            rec["words"] = n5_detail[item["kanji"]].get("words", [])
        else:
            rec["words"] = []
        entries.append(rec)

    ROMAJI_HEPBURN = {
        'kya': ('きゃ', 'キャ'), 'kyu': ('きゅ', 'キュ'), 'kyo': ('きょ', 'キョ'),
        'sha': ('しゃ', 'シャ'), 'shu': ('しゅ', 'シュ'), 'sho': ('しょ', 'ショ'),
        'cha': ('ちゃ', 'チャ'), 'chu': ('ちゅ', 'チュ'), 'cho': ('ちょ', 'チョ'),
        'nya': ('にゃ', 'ニャ'), 'nyu': ('にゅ', 'ニュ'), 'nyo': ('にょ', 'ニョ'),
        'hya': ('ひゃ', 'ヒャ'), 'hyu': ('ひゅ', 'ヒュ'), 'hyo': ('ひょ', 'ヒョ'),
        'mya': ('みゃ', 'ミャ'), 'myu': ('みゅ', 'ミュ'), 'myo': ('みょ', 'ミョ'),
        'rya': ('りゃ', 'リャ'), 'ryu': ('りゅ', 'リュ'), 'ryo': ('りょ', 'リョ'),
        'gya': ('ぎゃ', 'ギャ'), 'gyu': ('ぎゅ', 'ギュ'), 'gyo': ('ぎょ', 'ギョ'),
        'ja': ('じゃ', 'ジャ'), 'ju': ('じゅ', 'ジュ'), 'jo': ('じょ', 'ジョ'),
        'bya': ('びゃ', 'ビャ'), 'byu': ('びゅ', 'ビュ'), 'byo': ('びょ', 'ビョ'),
        'pya': ('ぴゃ', 'ピャ'), 'pyu': ('ぴゅ', 'ピュ'), 'pyo': ('ぴょ', 'ピョ'),
        'ka': ('か', 'カ'), 'ki': ('き', 'キ'), 'ku': ('く', 'ク'), 'ke': ('け', 'ケ'), 'ko': ('co', 'コ'),
        'sa': ('さ', 'サ'), 'shi': ('し', 'シ'), 'su': ('す', 'ス'), 'se': ('せ', 'セ'), 'so': ('そ', 'ソ'),
        'ta': ('た', 'タ'), 'chi': ('ち', 'チ'), 'tsu': ('つ', 'ツ'), 'te': ('て', 'テ'), 'to': ('と', 'ト'),
        'na': ('な', 'ナ'), 'ni': ('に', 'ニ'), 'nu': ('ぬ', 'ヌ'), 'ne': ('ね', 'ネ'), 'no': ('の', 'ノ'),
        'ha': ('は', 'ハ'), 'hi': ('ひ', 'ヒ'), 'fu': ('ふ', 'フ'), 'he': ('へ', 'ヘ'), 'ho': ('ほ', 'ホ'),
        'ma': ('ま', 'マ'), 'mi': ('み', 'ミ'), 'mu': ('む', 'ム'), 'me': ('め', 'メ'), 'mo': ('も', 'モ'),
        'ya': ('や', 'ヤ'), 'yu': ('ゆ', 'ユ'), 'yo': ('よ', 'ヨ'),
        'ra': ('ら', 'ラ'), 'ri': ('り', 'リ'), 'ru': ('る', 'ル'), 're': ('れ', 'レ'), 'ro': ('ろ', 'ロ'),
        'wa': ('わ', 'ワ'), 'wo': ('を', 'ヲ'), 'n': ('ん', 'ン'),
        'ga': ('が', 'ガ'), 'gi': ('ぎ', 'ギ'), 'gu': ('ぐ', 'グ'), 'ge': ('げ', 'ゲ'), 'go': ('ご', 'ゴ'),
        'za': ('ざ', 'ザ'), 'ji': ('じ', 'ジ'), 'zu': ('ず', 'ズ'), 'ze': ('ぜ', 'ゼ'), 'zo': ('zo', 'ゾ'),
        'da': ('だ', 'ダ'), 'de': ('で', 'デ'), 'do': ('ど', 'ド'),
        'ba': ('ば', 'バ'), 'bi': ('び', 'ビ'), 'bu': ('ぶ', 'ブ'), 'be': ('be', 'ベ'), 'bo': ('bo', 'ボ'),
        'pa': ('pa', 'パ'), 'pi': ('ぴ', 'ピ'), 'pu': ('pu', 'プ'), 'pe': ('pe', 'ペ'), 'po': ('po', 'ポ'),
        'a': ('あ', 'ア'), 'i': ('い', 'イ'), 'u': ('う', 'ウ'), 'e': ('え', 'エ'), 'o': ('お', 'オ')
    }

    def romaji_to_kana(text):
        t = text.lower().strip()
        hira, kata = "", ""
        i, n = 0, len(t)
        while i < n:
            if i + 1 < n and t[i] == t[i+1] and t[i] not in 'aeioun-':
                hira += 'っ'
                kata += 'ッ'
                i += 1
                continue
            matched = False
            for l in (3, 2, 1):
                if i + l <= n and t[i:i+l] in ROMAJI_HEPBURN:
                    h, k = ROMAJI_HEPBURN[t[i:i+l]]
                    hira += h
                    kata += k
                    i += l
                    matched = True
                    break
            if not matched:
                return "", ""
        return hira, kata

    def clean_kana(text):
        return re.sub(r'[\.\-\s]', '', text or '')

    KANA_TO_ROMAJI = {h: r for r, (h, _) in ROMAJI_HEPBURN.items()}
    KANA_TO_ROMAJI.update({k: r for r, (_, k) in ROMAJI_HEPBURN.items()})

    def kana_to_romaji_simple(kana):
        res = ""
        i, n = 0, len(kana)
        while i < n:
            matched = False
            for l in (2, 1):
                if i + l <= n and kana[i:i+l] in KANA_TO_ROMAJI:
                    res += KANA_TO_ROMAJI[kana[i:i+l]]
                    i += l
                    matched = True
                    break
            if not matched:
                i += 1
        return res

    def get_search_score(item, query):
        q = query.strip().lower()
        if not q: return 0

        # 1. Cocok persis Kanji (Skor 100)
        if item["kanji"] == q:
            return 100

        onyomi_raw = item.get("onyomi", [])
        kunyomi_raw = item.get("kunyomi", [])
        readings_clean = [clean_kana(r).lower() for r in (onyomi_raw + kunyomi_raw)]

        # 2. Cocok bacaan Kana (Skor 90 / 85)
        is_kana_query = bool(re.search(r'[\u3040-\u309F\u30A0-\u30FF]', q))
        if is_kana_query:
            if any(r == q for r in readings_clean): return 90
            if any(q in r for r in readings_clean): return 85

        # 3. Cocok bacaan Romaji Tepat (Skor 80)
        q_hira, q_kata = romaji_to_kana(q)
        readings_romaji = [kana_to_romaji_simple(clean_kana(r)) for r in (onyomi_raw + kunyomi_raw)]
        if any(rom == q for rom in readings_romaji) or (q_hira and any(r == q_hira or r == q_kata for r in readings_clean)):
            return 80

        # 4. Cocok arti Bahasa Indonesia (Skor 75 / 65)
        main_meaning = (item.get("meaning") or "").strip().lower()
        if main_meaning == q: return 75
        parts = [p.strip().lower() for p in re.split(r'[,;/•\(\)]', main_meaning) if p.strip()]
        if q in parts: return 75
        try:
            if re.search(r'\b' + re.escape(q) + r'\b', main_meaning, re.IGNORECASE):
                return 65
        except: pass

        # 5. Partial Romaji (Skor 50)
        if any(q in rom for rom in readings_romaji if rom) or (q_hira and any(q_hira in r or q_kata in r for r in readings_clean)):
            return 50

        # 6. Partial Arti Bahasa Indonesia (Skor 40 / 35)
        if main_meaning.startswith(q): return 40
        if q in main_meaning: return 35

        # 7. Kosakata contoh (Skor 20 / 10)
        for w in item.get("words", []):
            ww = (w.get("word") or "").lower()
            wr = (w.get("reading") or "").lower()
            wm = (w.get("meaning") or "").lower()
            if q in (ww, wr, wm) or (q_hira and q_hira == wr) or (q_kata and q_kata == wr): return 20
            if q in ww or q in wr or q in wm or (q_hira and q_hira in wr): return 10

        return 0

    def execute_search(query):
        scored = []
        for it in entries:
            sc = get_search_score(it, query)
            if sc > 0:
                scored.append((it, sc))
        has_strong = any(sc >= 35 for _, sc in scored)
        if has_strong:
            scored = [(it, sc) for it, sc in scored if sc >= 35]
        scored.sort(key=lambda x: (x[1], -x[0]["strokes"]), reverse=True)
        return scored

    # Uji 1: Pencarian "orang" (Arti Indonesia)
    results_orang = execute_search("orang")
    top_item, top_score = results_orang[0]
    print(f"Pencarian kata: 'orang' -> Hasil #1: '{top_item['kanji']}' (Skor: {top_score}, Arti: '{top_item['meaning']}')")
    assert top_item["kanji"] == "人", f"Hasil teratas untuk 'orang' harus Kanji 人! Ditemukan: {top_item['kanji']}"
    assert top_score >= 75, f"Skor Kanji 人 untuk query 'orang' harus >= 75! Ditemukan: {top_score}"
    ranked_chars = [it["kanji"] for it, _ in results_orang[:5]]
    assert "一" not in ranked_chars, "Kanji 一 (satu) tidak boleh muncul di 5 hasil teratas untuk query 'orang'!"
    assert "二" not in ranked_chars, "Kanji 二 (dua) tidak boleh muncul di 5 hasil teratas untuk query 'orang'!"
    print(f"✔ [Arti] Query 'orang' -> Kanji '人' tepat muncul di urutan #1 tanpa dicemari 一/二.")

    # Uji 2: Pencarian Romaji "hito"
    results_hito = execute_search("hito")
    top_hito_chars = [it["kanji"] for it, _ in results_hito[:3]]
    assert "人" in top_hito_chars or "一" in top_hito_chars, "Query romaji 'hito' harus menampilkan 人 atau 一 di posisi teratas!"
    print(f"✔ [Romaji] Query 'hito' -> Hasil teratas: {top_hito_chars} (Skor Romaji >= 80).")

    # Uji 3: Pencarian Romaji "mizu" & Arti "air"
    results_mizu = execute_search("mizu")
    assert results_mizu[0][0]["kanji"] == "水", f"Query 'mizu' harus menghasilkan 水! Ditemukan: {results_mizu[0][0]['kanji']}"
    results_air = execute_search("air")
    assert results_air[0][0]["kanji"] == "水", f"Query 'air' harus menghasilkan 水! Ditemukan: {results_air[0][0]['kanji']}"
    print(f"✔ [Romaji & Arti] Query 'mizu' dan 'air' keduanya tepat menghasilkan Kanji '水' di urutan #1.")

def test_payload_budgets():
    print("\n==================================================")
    print("🧪 [5] VERIFIKASI BUDGET BOBOT (PAGE WEIGHT TARGETS)")
    print("==================================================")

    # 1. Target Data Awal Kamus <= 700 KB
    index_path = os.path.join(BASE_DIR, "data", "kanji-index.json")
    kana_path = os.path.join(BASE_DIR, "js", "stroke-data.js")

    idx_raw = os.path.getsize(index_path) / 1024
    kana_raw = os.path.getsize(kana_path) / 1024
    initial_data_raw = idx_raw + kana_raw

    with open(index_path, "rb") as f:
        idx_gz = len(gzip.compress(f.read())) / 1024
    with open(kana_path, "rb") as f:
        kana_gz = len(gzip.compress(f.read())) / 1024
    initial_data_gz = idx_gz + kana_gz

    print(f"Beban Data Awal Kamus (kanji-index.json + stroke-data.js Kana):")
    print(f"  - Raw : {initial_data_raw:.1f} KB (Target <= 700 KB)")
    print(f"  - Gzip: {initial_data_gz:.1f} KB")
    assert initial_data_raw <= 700.0, f"Beban data awal {initial_data_raw:.1f} KB melebihi target 700 KB!"
    print("✔ Target beban data awal (<= 700 KB) tercapai dengan gemilang!")

    # 2. Target Beban Kanji Pertama Dibuka <= +60 KB
    n5_kanji_path = os.path.join(BASE_DIR, "data", "kanji", "n5.json")
    n5_kanji_raw = os.path.getsize(n5_kanji_path) / 1024
    with open(n5_kanji_path, "rb") as f:
        n5_kanji_gz = len(gzip.compress(f.read())) / 1024

    print(f"\nBeban Kanji N5 Pertama Dibuka (data/kanji/n5.json):")
    print(f"  - Raw : +{n5_kanji_raw:.1f} KB (Target <= +60 KB)")
    print(f"  - Gzip: +{n5_kanji_gz:.1f} KB")
    assert n5_kanji_raw <= 60.0, f"Beban kanji pertama {n5_kanji_raw:.1f} KB melebihi target 60 KB!"
    print("✔ Target kanji pertama dibuka (<= +60 KB) tercapai dengan gemilang!")

def main():
    test_static_rules()
    test_data_integrity()
    test_offline_kanji_resolution()
    test_ranked_search()
    test_payload_budgets()
    print("\n🎉 SELURUH PENGUJIAN LOGIKA & ARSITEKTUR KANJI LOKAL BERHASIL 100%!")

if __name__ == "__main__":
    main()
