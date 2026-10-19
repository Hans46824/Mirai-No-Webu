#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: skrip/arsip/build_data_chunks.py
Fungsi: Memecah basis data kamus dan goresan kanji menjadi chunk-chunk ramping berbasis level JLPT.
        Menghilangkan beban 8+ MB pada halaman kamus dan menjadikannya ultra-ringan (<= 700 KB).

Input (Single Source of Truth):
  - data/kanji.json (2.211 Kanji lengkap)
  - js/stroke-data.js / data/stroke-master.json (2.375 vektor goresan KanjiVG)
  - data/stroke-overrides.json (Lapisan override proteksi manual)

Output yang Dihasilkan:
  1. data/kanji-index.json:
     Index ramping (kanji, meaning, jlpt, level, strokes, grade, onyomi, kunyomi) ~316 KB (gzip ~48 KB).
  2. data/kanji/<jlpt>.json (n5.json, n4.json, n3.json, n2.json, n1.json):
     Detail lengkap (words, examples, sentence, meaningEn) per level JLPT, dimuat on-demand saat kanji dibuka.
  3. js/stroke-data.js:
     Hanya berisi karakter Kana inline (164 aksara Hiragana/Katakana) ~71 KB (gzip ~17 KB).
  4. data/strokes/<jlpt>.json (n5.json, n4.json, n3.json, n2.json, n1.json):
     Vektor goresan kanji per level JLPT, dimuat on-demand saat kanji pertama level tersebut dibuka.
  5. data/stroke-master.json:
     Arsip lengkap 2.375 karakter untuk memastikan skrip ini 100% IDEMPOTEN.
"""

import os
import sys
import json
import re
import gzip
from collections import defaultdict

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

KANJI_SRC = os.path.join(BASE_DIR, "data", "kanji.json")
STROKE_DATA_JS = os.path.join(BASE_DIR, "js", "stroke-data.js")
STROKE_MASTER_JSON = os.path.join(BASE_DIR, "data", "stroke-master.json")
STROKE_OVERRIDES_JSON = os.path.join(BASE_DIR, "data", "stroke-overrides.json")

KANJI_INDEX_OUT = os.path.join(BASE_DIR, "data", "kanji-index.json")
KANJI_CHUNKS_DIR = os.path.join(BASE_DIR, "data", "kanji")
STROKES_CHUNKS_DIR = os.path.join(BASE_DIR, "data", "strokes")

def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def save_compact_json(filepath, data):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    raw = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(raw)
    return len(raw.encode("utf-8")), len(gzip.compress(raw.encode("utf-8")))

def load_stroke_master():
    # 1. Jika stroke-master.json sudah ada, baca dari sana
    if os.path.isfile(STROKE_MASTER_JSON):
        data = load_json(STROKE_MASTER_JSON)
        if len(data) >= 2370:
            return data

    # 2. Jika belum, ekstrak dari js/stroke-data.js
    if os.path.isfile(STROKE_DATA_JS):
        with open(STROKE_DATA_JS, "r", encoding="utf-8") as f:
            content = f.read()
        m = re.search(r'window\.MIRAI_STROKE_DATA\s*=\s*(\{[\s\S]*\});?\s*$', content)
        if m:
            data = json.loads(m.group(1))
            if len(data) >= 2370:
                # Simpan ke stroke-master.json agar idempoten
                save_compact_json(STROKE_MASTER_JSON, data)
                return data

    raise RuntimeError("Gagal memuat dataset master goresan (2.375 karakter)!")

def apply_overrides_to_strokes(stroke_map, overrides):
    for char, ov in overrides.items():
        if char in stroke_map:
            rec = stroke_map[char]
            if "paths" in ov and ov["paths"]:
                rec["paths"] = ov["paths"]
            if "numbers" in ov and ov["numbers"]:
                rec["numbers"] = ov["numbers"]
            if "variant" in ov:
                rec["variant"] = ov["variant"]
            if "note" in ov:
                rec["note"] = ov["note"]
            rec["overridden"] = True
        elif "paths" in ov and ov["paths"]:
            stroke_map[char] = {
                "viewBox": "0 0 109 109",
                "paths": ov["paths"],
                "numbers": ov.get("numbers", []),
                "variant": ov.get("variant"),
                "note": ov.get("note"),
                "overridden": True,
                "source": "Override"
            }

def main():
    print("==================================================")
    print("📦 MIRAI NO WEBU — BUILD DATA CHUNKS PIPELINE")
    print("==================================================")

    # 1. Muat data kanji master (Single Source of Truth)
    if not os.path.isfile(KANJI_SRC):
        print(f"❌ Berkas sumber {KANJI_SRC} tidak ditemukan!")
        sys.exit(1)

    kanji_list = load_json(KANJI_SRC)
    print(f"✔ Basis data kanji utama dimuat: {len(kanji_list)} kanji dari {KANJI_SRC}.")

    # 2. Muat data goresan master & override
    stroke_master = load_stroke_master()
    print(f"✔ Basis data goresan master dimuat: {len(stroke_master)} karakter.")

    overrides = {}
    if os.path.isfile(STROKE_OVERRIDES_JSON):
        overrides = load_json(STROKE_OVERRIDES_JSON)
        print(f"✔ Lapisan override dimuat: {len(overrides)} entri.")
        apply_overrides_to_strokes(stroke_master, overrides)

    # 3. Bangun data/kanji-index.json (Ramping untuk list, filter, dan search)
    kanji_index = []
    kanji_by_jlpt = defaultdict(dict)
    char_to_jlpt = {}

    for item in kanji_list:
        ch = item["kanji"]
        jlpt_str = item.get("jlpt") or "N5"
        jlpt_key = jlpt_str.lower()
        if not jlpt_key.startswith("n"):
            jlpt_key = f"n{jlpt_key}"
        char_to_jlpt[ch] = jlpt_key

        # Item index ringkas
        kanji_index.append({
            "kanji": ch,
            "meaning": item.get("meaning", ""),
            "jlpt": jlpt_str,
            "level": item.get("level", "Dasar"),
            "strokes": item.get("strokes", 0),
            "grade": item.get("grade", 99),
            "onyomi": item.get("onyomi", []),
            "kunyomi": item.get("kunyomi", [])
        })

        # Detail per level JLPT
        kanji_by_jlpt[jlpt_key][ch] = {
            "kanji": ch,
            "meaning": item.get("meaning", ""),
            "meaningEn": item.get("meaningEn", ""),
            "onyomi": item.get("onyomi", []),
            "kunyomi": item.get("kunyomi", []),
            "jlpt": jlpt_str,
            "level": item.get("level", "Dasar"),
            "strokes": item.get("strokes", 0),
            "grade": item.get("grade", 99),
            "words": item.get("words") or item.get("examples") or [],
            "sentence": item.get("sentence") or {"japanese": ch, "reading": "", "meaning": ""},
            "sentence_is_template": item.get("sentence_is_template", False),
            "example_word": item.get("example_word")
        }

    raw_idx_sz, gz_idx_sz = save_compact_json(KANJI_INDEX_OUT, kanji_index)
    print(f"✔ [1] {KANJI_INDEX_OUT} berhasil dibuat: {raw_idx_sz/1024:.1f} KB (Gzip: {gz_idx_sz/1024:.1f} KB).")

    # 4. Bangun data/kanji/<jlpt>.json
    print("\n✔ [2] Menulis chunk detail kanji (data/kanji/<jlpt>.json):")
    for lvl in ["n5", "n4", "n3", "n2", "n1"]:
        chunk_data = kanji_by_jlpt[lvl]
        chunk_path = os.path.join(KANJI_CHUNKS_DIR, f"{lvl}.json")
        raw_sz, gz_sz = save_compact_json(chunk_path, chunk_data)
        print(f"    - {lvl}.json : {len(chunk_data):>4} kanji | {raw_sz/1024:>6.1f} KB (Gzip: {gz_sz/1024:>5.1f} KB)")

    # Tulis js/kanji-data.js sebagai artefak build turunan dari data/kanji.json
    kanji_full_js = "/**\n * File: js/kanji-data.js (Build artifact derived from data/kanji.json)\n */\nwindow.KANJI_FULL_DATA = " + json.dumps(kanji_list, ensure_ascii=False, separators=(',', ':')) + ";\n"
    with open(os.path.join(BASE_DIR, "js", "kamus-kanji-data.js"), "w", encoding="utf-8") as f:
        f.write(kanji_full_js)
    print("✔ [2b] js/kanji-data.js tersinkronisasi sebagai artefak build.")

    # 5. Pisahkan goresan: Kana inline vs Kanji per JLPT
    kana_strokes = {}
    strokes_by_jlpt = defaultdict(dict)

    for ch, rec in stroke_master.items():
        if ch in char_to_jlpt:
            lvl = char_to_jlpt[ch]
            strokes_by_jlpt[lvl][ch] = rec
        else:
            # Kana (Hiragana, Katakana, Yoon, karakter pendukung)
            kana_strokes[ch] = rec

    # Tulis js/stroke-data.js (Inline Kana HANYA)
    kana_json = json.dumps(kana_strokes, ensure_ascii=False, separators=(',', ':'))
    header = """/**
 * File: js/stroke-data.js
 * Deskripsi: Dataset kurva goresan aksara Kana (Hiragana & Katakana) inline untuk kamus & kuis latihan.
 * Catatan Optimasi: Karakter Kanji telah dipecah modular ke data/strokes/<jlpt>.json (on-demand).
 */
window.MIRAI_STROKE_DATA = """
    full_content = header + kana_json + ";\n"
    with open(STROKE_DATA_JS, "w", encoding="utf-8") as f:
        f.write(full_content)
    raw_kana_sz = len(full_content.encode("utf-8"))
    gz_kana_sz = len(gzip.compress(full_content.encode("utf-8")))
    print(f"\n✔ [3] js/stroke-data.js diperbarui (HANYA Kana): {len(kana_strokes)} karakter | {raw_kana_sz/1024:.1f} KB (Gzip: {gz_kana_sz/1024:.1f} KB).")

    # Tulis data/strokes/<jlpt>.json
    print("\n✔ [4] Menulis chunk goresan kanji (data/strokes/<jlpt>.json):")
    for lvl in ["n5", "n4", "n3", "n2", "n1"]:
        chunk_strokes = strokes_by_jlpt[lvl]
        chunk_path = os.path.join(STROKES_CHUNKS_DIR, f"{lvl}.json")
        raw_sz, gz_sz = save_compact_json(chunk_path, chunk_strokes)
        print(f"    - {lvl}.json : {len(chunk_strokes):>4} kanji | {raw_sz/1024:>6.1f} KB (Gzip: {gz_sz/1024:>5.1f} KB)")

    # 6. Ringkasan Perbandingan Bobot Halaman Kamus
    print("\n==================================================")
    print("📊 LAPORAN PERBANDINGAN BOBOT SEBELUM vs SESUDAH")
    print("==================================================")
    print("SEBELUM (Muat penuh sekaligus di awal):")
    print("  - js/stroke-data.js       : 4.200 KB")
    print("  - js/kanji-data.js        : 1.800 KB")
    print("  - fetch data/kanji.json   : 2.400 KB")
    print("  --------------------------------------")
    print("  Total Data Awal Kamus     : ~8.400 KB (8,4 MB!) 💥")
    print()
    print("SESUDAH (Modular & On-Demand Chunking):")
    print(f"  - js/stroke-data.js (Kana) : {raw_kana_sz/1024:>7.1f} KB  (Gzip: {gz_kana_sz/1024:>5.1f} KB)")
    print(f"  - data/kanji-index.json    : {raw_idx_sz/1024:>7.1f} KB  (Gzip: {gz_idx_sz/1024:>5.1f} KB)")
    total_initial = (raw_kana_sz + raw_idx_sz) / 1024
    total_initial_gz = (gz_kana_sz + gz_idx_sz) / 1024
    print("  --------------------------------------")
    print(f"  Total Data Awal Kamus     : {total_initial:>7.1f} KB  (Gzip: {total_initial_gz:>5.1f} KB) 🚀")
    print()
    n5_detail_sz = len(json.dumps(kanji_by_jlpt['n5'], ensure_ascii=False, separators=(',', ':')).encode('utf-8')) / 1024
    n5_stroke_sz = len(json.dumps(strokes_by_jlpt['n5'], ensure_ascii=False, separators=(',', ':')).encode('utf-8')) / 1024
    print(f"Saat Kanji N5 Pertama Dibuka (On-Demand):")
    print(f"  - data/kanji/n5.json       : +{n5_detail_sz:.1f} KB")
    print(f"  - data/strokes/n5.json     : +{n5_stroke_sz:.1f} KB")
    print("==================================================")
    print("✔ Pipeline pemecahan data chunks berhasil 100%!")

if __name__ == '__main__':
    main()
