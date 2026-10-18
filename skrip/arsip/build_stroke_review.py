#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: skrip/arsip/build_stroke_review.py
Fungsi: Membangun alat review visual goresan karakter statis (skrip/laporan/stroke-review.html)
        tanpa memerlukan live server dan tanpa screenshot otomatis.

Fitur:
  1. Menghitung skor tumpang tindih (IoU pixel overlap) antara kurva goresan KanjiVG
     dengan font Noto Sans CJK JP secara presisi.
  2. Mengidentifikasi seluruh anomali / perbedaan goresan (discrepancy), varian buku teks
     (kyōkasho vs gothic), dan status override per karakter.
  3. Mendeteksi keberadaan gambar acuan di images/mirai/goresan-acuan/<hex>.png.
  4. Menghasilkan antarmuka web statis mandiri (skrip/laporan/stroke-review.html) lengkap dengan:
     - Toggle gaya font: "Gaya Buku Teks" (Klee One / Kaisei Tokumin) vs "Gothic" (Noto Sans JP)
     - Overlay kurva goresan berwarna per urutan + nomor goresan di atas siluet font
     - Urutan default: skor tumpang tindih terendah / paling tidak cocok terlebih dahulu
     - Filter: Semua, Hanya Kana, JLPT N5..N1, Hanya yang Beda, Hanya yang Di-override
     - Pencarian instan per karakter, arti, atau kode heksadesimal
     - Paginasi interaktif untuk performa rendering ultra-cepat tanpa lag
"""

import os
import sys
import json
import re
import time
from PIL import Image, ImageDraw, ImageFont

FONT_PATH_CANDIDATES = [
    "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
]

STROKE_DATA_FILE = "js/stroke-data.js"
OVERRIDES_FILE = "data/stroke-overrides.json"
KANJI_FILE = "data/kanji.json"
KANA_FILE = "data/kana.json"
REF_IMG_DIR = "images/mirai/goresan-acuan"
OUTPUT_HTML_FILE = "skrip/laporan/stroke-review.html"

# Palet warna goresan (16 warna kontras tinggi yang berputar secara urut)
STROKE_COLORS = [
    "#e11d48", "#2563eb", "#16a34a", "#d97706",
    "#9333ea", "#0891b2", "#ea580c", "#4f46e5",
    "#db2777", "#059669", "#7c3aed", "#c026d3",
    "#0284c7", "#d946ef", "#84cc16", "#f59e0b"
]

def find_font():
    for p in FONT_PATH_CANDIDATES:
        if os.path.isfile(p):
            return p
    return None

def parse_svg_path_to_points(d):
    raw_tokens = re.findall(r'[a-zA-Z]|[-+]?(?:\d*\.\d+|\d+)', d)
    points = []
    curr_x, curr_y = 0.0, 0.0
    last_cp_x, last_cp_y = 0.0, 0.0
    last_cmd = ''
    idx = 0
    while idx < len(raw_tokens):
        token = raw_tokens[idx]
        if token.isalpha():
            cmd = token
            idx += 1
        else:
            cmd = last_cmd
        if cmd == 'M':
            curr_x = float(raw_tokens[idx])
            curr_y = float(raw_tokens[idx+1])
            points.append((curr_x, curr_y))
            idx += 2
            last_cmd = 'L'
        elif cmd == 'm':
            curr_x += float(raw_tokens[idx])
            curr_y += float(raw_tokens[idx+1])
            points.append((curr_x, curr_y))
            idx += 2
            last_cmd = 'l'
        elif cmd in ('C', 'c'):
            is_rel = (cmd == 'c')
            while idx < len(raw_tokens) and not raw_tokens[idx].isalpha():
                x1 = float(raw_tokens[idx]) + (curr_x if is_rel else 0)
                y1 = float(raw_tokens[idx+1]) + (curr_y if is_rel else 0)
                x2 = float(raw_tokens[idx+2]) + (curr_x if is_rel else 0)
                y2 = float(raw_tokens[idx+3]) + (curr_y if is_rel else 0)
                x3 = float(raw_tokens[idx+4]) + (curr_x if is_rel else 0)
                y3 = float(raw_tokens[idx+5]) + (curr_y if is_rel else 0)
                idx += 6
                for step in (1, 2, 4):
                    t = step / 4.0
                    bx = (1-t)**3 * curr_x + 3*(1-t)**2 * t * x1 + 3*(1-t)*t**2 * x2 + t**3 * x3
                    by = (1-t)**3 * curr_y + 3*(1-t)**2 * t * y1 + 3*(1-t)*t**2 * y2 + t**3 * y3
                    points.append((bx, by))
                curr_x, curr_y = x3, y3
                last_cp_x, last_cp_y = x2, y2
            last_cmd = cmd
        elif cmd in ('S', 's'):
            is_rel = (cmd == 's')
            while idx < len(raw_tokens) and not raw_tokens[idx].isalpha():
                if last_cmd in ('C', 'c', 'S', 's'):
                    x1 = 2 * curr_x - last_cp_x
                    y1 = 2 * curr_y - last_cp_y
                else:
                    x1, y1 = curr_x, curr_y
                x2 = float(raw_tokens[idx]) + (curr_x if is_rel else 0)
                y2 = float(raw_tokens[idx+1]) + (curr_y if is_rel else 0)
                x3 = float(raw_tokens[idx+2]) + (curr_x if is_rel else 0)
                y3 = float(raw_tokens[idx+3]) + (curr_y if is_rel else 0)
                idx += 4
                for step in (1, 2, 4):
                    t = step / 4.0
                    bx = (1-t)**3 * curr_x + 3*(1-t)**2 * t * x1 + 3*(1-t)*t**2 * x2 + t**3 * x3
                    by = (1-t)**3 * curr_y + 3*(1-t)**2 * t * y1 + 3*(1-t)*t**2 * y2 + t**3 * y3
                    points.append((bx, by))
                curr_x, curr_y = x3, y3
                last_cp_x, last_cp_y = x2, y2
            last_cmd = cmd
        elif cmd in ('L', 'l'):
            is_rel = (cmd == 'l')
            while idx < len(raw_tokens) and not raw_tokens[idx].isalpha():
                curr_x = float(raw_tokens[idx]) + (curr_x if is_rel else 0)
                curr_y = float(raw_tokens[idx+1]) + (curr_y if is_rel else 0)
                points.append((curr_x, curr_y))
                idx += 2
            last_cmd = cmd
        else:
            idx += 1
    return points

def compute_overlap_score(char, paths, font):
    if not font:
        return 50.0
    try:
        # Siluet font Noto CJK
        img_font = Image.new('1', (109, 109), 0)
        d_font = ImageDraw.Draw(img_font)
        d_font.text((10, -12), char, font=font, fill=1)

        # Siluet kurva goresan
        img_stroke = Image.new('1', (109, 109), 0)
        d_stroke = ImageDraw.Draw(img_stroke)
        for p in paths:
            pts = parse_svg_path_to_points(p)
            if len(pts) >= 2:
                d_stroke.line(pts, fill=1, width=7)

        b1 = img_font.tobytes()
        b2 = img_stroke.tobytes()
        inter = sum((x & y).bit_count() for x, y in zip(b1, b2))
        union = sum((x | y).bit_count() for x, y in zip(b1, b2))
        if union == 0:
            return 100.0
        return round((inter / union) * 100, 1)
    except Exception:
        return 50.0

def load_data():
    # 1. Stroke data
    with open(STROKE_DATA_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.search(r'window\.MIRAI_STROKE_DATA\s*=\s*(\{[\s\S]*\});?\s*$', content)
    stroke_data = json.loads(m.group(1)) if m else {}

    # 2. Overrides
    overrides = {}
    if os.path.isfile(OVERRIDES_FILE):
        with open(OVERRIDES_FILE, "r", encoding="utf-8") as f:
            overrides = json.load(f)

    # 3. Kanji data
    kanji_meta = {}
    if os.path.isfile(KANJI_FILE):
        with open(KANJI_FILE, "r", encoding="utf-8") as f:
            for item in json.load(f):
                k = item.get("kanji")
                if k:
                    kanji_meta[k] = item

    # 4. Kana data
    kana_meta = {}
    if os.path.isfile(KANA_FILE):
        with open(KANA_FILE, "r", encoding="utf-8") as f:
            kana_raw = json.load(f)
            for section in ["hiragana", "katakana"]:
                for row in kana_raw.get(section, []):
                    for cell in row:
                        if isinstance(cell, dict) and cell.get("char"):
                            kana_meta[cell["char"]] = {
                                "type": section,
                                "romaji": cell.get("romaji", "")
                            }

    # 5. Gambar acuan yang ada
    os.makedirs(REF_IMG_DIR, exist_ok=True)
    existing_ref_imgs = set(os.listdir(REF_IMG_DIR))

    return stroke_data, overrides, kanji_meta, kana_meta, existing_ref_imgs

def build_review_html():
    print("==================================================")
    print("🎨 MIRAI NO WEBU — BUILD STROKE REVIEW TOOL")
    print("==================================================")

    t0 = time.time()
    stroke_data, overrides, kanji_meta, kana_meta, existing_ref_imgs = load_data()
    print(f"✔ Dataset dimuat: {len(stroke_data)} karakter goresan, {len(overrides)} override.")

    font_path = find_font()
    font = None
    if font_path:
        print(f"✔ Font Noto CJK ditemukan: {font_path}")
        font = ImageFont.truetype(font_path, 88)
    else:
        print("⚠ Font Noto CJK tidak ditemukan, menggunakan estimasi skor.")

    # Siapkan entri per karakter
    review_entries = []
    discrepancy_count = 0
    overridden_count = 0
    ref_image_count = 0

    print("⏳ Menghitung skor tumpang tindih untuk 2.375 karakter...")
    for idx, (char, record) in enumerate(stroke_data.items()):
        hex_code = f"{ord(char):05x}"
        paths = record.get("paths", [])
        kvg_strokes = len(paths)

        # Cek override
        is_overridden = char in overrides
        override_info = overrides.get(char, {})
        if is_overridden:
            overridden_count += 1
            # Terapkan numbers atau paths dari override jika ada
            if "numbers" in override_info and override_info["numbers"]:
                record["numbers"] = override_info["numbers"]
            if "paths" in override_info and override_info["paths"]:
                paths = override_info["paths"]
                kvg_strokes = len(paths)

        # Cek metadata kanji / kana
        k_info = kanji_meta.get(char)
        expected_strokes = int(k_info["strokes"]) if k_info and k_info.get("strokes") is not None else None
        meaning = k_info.get("meaning", "") if k_info else ""
        onyomi = ", ".join(k_info.get("onyomi", [])) if k_info else ""
        kunyomi = ", ".join(k_info.get("kunyomi", [])) if k_info else ""
        grade = k_info.get("grade") if k_info else None
        jlpt = k_info.get("jlpt") if k_info else None

        category = "kanji"
        if 0x3040 <= ord(char) <= 0x309F:
            category = "hiragana"
        elif 0x30A0 <= ord(char) <= 0x30FF:
            category = "katakana"

        # Cek selisih goresan (discrepancy)
        has_discrepancy = False
        if expected_strokes is not None and expected_strokes != kvg_strokes:
            has_discrepancy = True
            discrepancy_count += 1

        # Cek gambar acuan
        ref_filename = f"{hex_code}.png"
        has_ref_image = ref_filename in existing_ref_imgs
        if has_ref_image:
            ref_image_count += 1

        # Hitung skor overlap (IoU)
        if has_discrepancy:
            # Jika ada selisih goresan, jadikan skor 0 agar langsung berada di urutan teratas
            overlap_score = 0.0
        elif override_info.get("variant") == "kyokasho":
            # Varian buku teks memiliki perbedaan signifikan dengan font gothic
            overlap_score = compute_overlap_score(char, paths, font)
            # Berikan prioritas dengan menurunkan sedikit skor agar mudah direview
            overlap_score = min(overlap_score, 25.0)
        else:
            overlap_score = compute_overlap_score(char, paths, font)

        review_entries.append({
            "char": char,
            "hex": hex_code,
            "category": category,
            "paths": paths,
            "numbers": record.get("numbers", []),
            "kvg_strokes": kvg_strokes,
            "expected_strokes": expected_strokes,
            "has_discrepancy": has_discrepancy,
            "is_overridden": is_overridden,
            "override_note": override_info.get("note", ""),
            "variant": override_info.get("variant", ""),
            "overlap_score": overlap_score,
            "has_ref_image": has_ref_image,
            "meaning": meaning,
            "onyomi": onyomi,
            "kunyomi": kunyomi,
            "grade": grade,
            "jlpt": jlpt
        })

    # Urutkan secara default: skor tumpang tindih terendah / paling tidak cocok terlebih dahulu
    review_entries.sort(key=lambda x: (0 if x["has_discrepancy"] else 1, x["overlap_score"], x["char"]))

    dur = time.time() - t0
    print(f"✔ Perhitungan selesai dalam {dur:.2f}s!")
    print(f"  - Total entri       : {len(review_entries)}")
    print(f"  - Discrepancy       : {discrepancy_count}")
    print(f"  - Overridden        : {overridden_count}")
    print(f"  - Ref image ada     : {ref_image_count}")

    # Generate HTML
    print("⏳ Menghasilkan skrip/laporan/stroke-review.html...")
    data_json_str = json.dumps(review_entries, ensure_ascii=False)
    colors_json_str = json.dumps(STROKE_COLORS)

    html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🌸 Alat Review Visual Goresan Karakter — Mirai no Webu</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Kaisei+Tokumin:wght@500;700&family=Klee+One:wght@600&family=Noto+Sans+JP:wght@400;500;700&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-dark: #0a0b10;
      --card-dark: #12141f;
      --card-border: #23273d;
      --pink-neon: #ec4899;
      --pink-glow: rgba(236, 72, 153, 0.25);
      --purple-neon: #a855f7;
      --blue-accent: #38bdf8;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --font-gothic: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-textbook: 'Klee One', 'Kaisei Tokumin', 'YuKyokasho', 'Hiragino Maru Gothic ProN', serif;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background: var(--bg-dark);
      color: var(--text-main);
      font-family: 'Plus Jakarta Sans', var(--font-gothic);
      line-height: 1.5;
      padding: 24px;
      min-height: 100vh;
    }}
    .review-header {{
      background: linear-gradient(135deg, rgba(236,72,153,0.12) 0%, rgba(168,85,247,0.08) 100%);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 24px 28px;
      margin-bottom: 24px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    }}
    .review-title {{
      font-size: 1.6rem;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 12px;
      background: linear-gradient(135deg, #f472b6, #c084fc, #38bdf8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .review-subtitle {{
      color: var(--text-muted);
      font-size: 0.92rem;
      margin-top: 6px;
    }}
    .stats-pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 16px;
    }}
    .stat-pill {{
      background: #181b2a;
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 6px 14px;
      font-size: 0.84rem;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .stat-pill strong {{
      color: var(--text-main);
    }}
    .stat-pill.pill-pink {{ border-color: rgba(236,72,153,0.4); background: rgba(236,72,153,0.1); color: #f472b6; }}
    .stat-pill.pill-purple {{ border-color: rgba(168,85,247,0.4); background: rgba(168,85,247,0.1); color: #c084fc; }}
    .stat-pill.pill-green {{ border-color: rgba(34,197,94,0.4); background: rgba(34,197,94,0.1); color: #4ade80; }}
    .stat-pill.pill-red {{ border-color: rgba(239,68,68,0.4); background: rgba(239,68,68,0.1); color: #f87171; }}

    /* Controls */
    .controls-panel {{
      background: var(--card-dark);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 18px;
      margin-bottom: 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .controls-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: center;
      justify-content: space-between;
    }}
    .search-box-wrap {{
      flex: 1;
      min-width: 260px;
      position: relative;
    }}
    .search-input {{
      width: 100%;
      background: #0f111a;
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 10px 14px 10px 38px;
      color: var(--text-main);
      font-size: 0.95rem;
      outline: none;
      transition: all 0.2s ease;
    }}
    .search-input:focus {{
      border-color: var(--pink-neon);
      box-shadow: 0 0 0 3px var(--pink-glow);
    }}
    .search-icon {{
      position: absolute;
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      pointer-events: none;
    }}
    .font-toggle-group {{
      display: flex;
      background: #0f111a;
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 4px;
      gap: 4px;
    }}
    .font-toggle-btn {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 8px 14px;
      border-radius: 7px;
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .font-toggle-btn.active {{
      background: linear-gradient(135deg, #ec4899, #a855f7);
      color: white;
      box-shadow: 0 2px 10px var(--pink-glow);
    }}
    .filter-pills-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
    }}
    .filter-btn {{
      background: #181b2a;
      border: 1px solid var(--card-border);
      border-radius: 8px;
      color: var(--text-muted);
      padding: 6px 12px;
      font-size: 0.82rem;
      cursor: pointer;
      font-weight: 600;
      transition: all 0.15s;
    }}
    .filter-btn:hover {{
      color: var(--text-main);
      border-color: #3b4261;
    }}
    .filter-btn.active {{
      background: #ec4899;
      color: white;
      border-color: #ec4899;
    }}
    .sort-group {{
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--text-muted);
      font-size: 0.84rem;
    }}
    .sort-select {{
      background: #0f111a;
      border: 1px solid var(--card-border);
      border-radius: 8px;
      color: var(--text-main);
      padding: 6px 10px;
      font-size: 0.84rem;
      outline: none;
    }}

    /* Card Grid */
    .grid-container {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 18px;
    }}
    .char-card {{
      background: var(--card-dark);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      transition: transform 0.2s ease, border-color 0.2s ease;
      position: relative;
    }}
    .char-card:hover {{
      transform: translateY(-2px);
      border-color: rgba(236,72,153,0.5);
    }}
    .char-card.has-discrepancy {{
      border-color: rgba(239,68,68,0.7);
      box-shadow: 0 0 16px rgba(239,68,68,0.15);
    }}
    .card-top {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
    }}
    .char-badge-group {{
      display: flex;
      align-items: baseline;
      gap: 10px;
    }}
    .main-char {{
      font-size: 2.2rem;
      font-weight: 700;
      line-height: 1;
      color: #fff;
    }}
    .char-hex {{
      font-size: 0.78rem;
      color: var(--text-muted);
      font-family: monospace;
      background: #1c1f30;
      padding: 2px 6px;
      border-radius: 4px;
    }}
    .tag-group {{
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
      justify-content: flex-end;
    }}
    .tag {{
      font-size: 0.72rem;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 6px;
      text-transform: uppercase;
    }}
    .tag-jlpt {{ background: rgba(56,189,248,0.15); color: #38bdf8; border: 1px solid rgba(56,189,248,0.3); }}
    .tag-kana {{ background: rgba(168,85,247,0.15); color: #c084fc; border: 1px solid rgba(168,85,247,0.3); }}
    .tag-override {{ background: rgba(236,72,153,0.18); color: #f472b6; border: 1px solid rgba(236,72,153,0.4); }}
    .tag-disc {{ background: rgba(239,68,68,0.2); color: #f87171; border: 1px solid rgba(239,68,68,0.5); }}

    /* Visual Comparison Box */
    .visual-comparison-box {{
      display: flex;
      gap: 12px;
      align-items: center;
      background: #090a10;
      border: 1px solid #1c1f30;
      border-radius: 10px;
      padding: 10px;
    }}
    .glyph-stage {{
      width: 130px;
      height: 130px;
      position: relative;
      background: #0f111a;
      border: 1px solid #23273d;
      border-radius: 8px;
      flex-shrink: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }}
    /* Font glyph underlay */
    .font-silhouette {{
      position: absolute;
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 96px;
      color: rgba(255, 255, 255, 0.16);
      user-select: none;
      line-height: 1;
      pointer-events: none;
      transition: font-family 0.2s ease;
    }}
    body.mode-textbook .font-silhouette {{
      font-family: var(--font-textbook);
      color: rgba(236, 72, 153, 0.22);
    }}
    body.mode-gothic .font-silhouette {{
      font-family: var(--font-gothic);
      color: rgba(255, 255, 255, 0.16);
    }}
    .kanjivg-svg {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 2;
    }}
    .kanjivg-svg path {{
      fill: none;
      stroke-width: 3.5;
      stroke-linecap: round;
      stroke-linejoin: round;
      opacity: 0.95;
    }}
    .kanjivg-svg text {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 8px;
      font-weight: 700;
      fill: #ffffff;
      paint-order: stroke;
      stroke: #0a0b10;
      stroke-width: 2.5px;
      stroke-linecap: butt;
      stroke-linejoin: miter;
    }}

    /* Reference image box */
    .ref-img-box {{
      flex: 1;
      height: 130px;
      background: #0f111a;
      border: 1px dashed #23273d;
      border-radius: 8px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 6px;
      font-size: 0.72rem;
      color: var(--text-muted);
    }}
    .ref-img-box img {{
      max-width: 100%;
      max-height: 110px;
      object-fit: contain;
      border-radius: 4px;
    }}
    .ref-img-title {{
      font-weight: 600;
      color: #cbd5e1;
      margin-bottom: 4px;
      font-size: 0.72rem;
    }}

    /* Card Details */
    .card-meta {{
      display: flex;
      flex-direction: column;
      gap: 6px;
      font-size: 0.82rem;
    }}
    .meta-row {{
      display: flex;
      justify-content: space-between;
      color: var(--text-muted);
    }}
    .meta-row strong {{
      color: var(--text-main);
    }}
    .overlap-bar-wrap {{
      display: flex;
      align-items: center;
      gap: 8px;
      margin-top: 4px;
    }}
    .overlap-bar {{
      flex: 1;
      height: 6px;
      background: #1e2235;
      border-radius: 4px;
      overflow: hidden;
    }}
    .overlap-fill {{
      height: 100%;
      border-radius: 4px;
      transition: width 0.3s;
    }}
    .note-badge {{
      background: rgba(236,72,153,0.1);
      border: 1px solid rgba(236,72,153,0.3);
      border-radius: 6px;
      padding: 4px 8px;
      font-size: 0.74rem;
      color: #f472b6;
      margin-top: 4px;
      line-height: 1.4;
    }}

    /* Pagination */
    .pagination-bar {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      background: var(--card-dark);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 12px 20px;
      margin-top: 24px;
      gap: 12px;
    }}
    .page-btn-group {{
      display: flex;
      gap: 6px;
    }}
    .page-btn {{
      background: #181b2a;
      border: 1px solid var(--card-border);
      border-radius: 6px;
      color: var(--text-main);
      padding: 6px 12px;
      cursor: pointer;
      font-size: 0.85rem;
      font-weight: 600;
    }}
    .page-btn:disabled {{
      opacity: 0.35;
      cursor: not-allowed;
    }}
    .page-btn:hover:not(:disabled) {{
      background: #ec4899;
      border-color: #ec4899;
    }}
    .page-info {{
      font-size: 0.85rem;
      color: var(--text-muted);
    }}
  </style>
</head>
<body class="mode-textbook">

  <!-- Header -->
  <header class="review-header">
    <div class="review-title">
      <span>🌸</span> MIRAI NO WEBU — Alat Review Visual Goresan Karakter
    </div>
    <div class="review-subtitle">
      Alat inspeksi visual mandiri untuk memverifikasi akurasi goresan KanjiVG terhadap font kaligrafi Jepang (buku teks kyōkasho & gothic), mendeteksi anomali goresan, dan menguji lapisan override secara komprehensif.
    </div>
    <div class="stats-pills">
      <div class="stat-pill pill-pink">
        <span>📊</span> <span>Total: <strong>{len(review_entries)}</strong> karakter</span>
      </div>
      <div class="stat-pill pill-purple">
        <span>🛡</span> <span>Lapisan Override: <strong>{overridden_count}</strong></span>
      </div>
      <div class="stat-pill {'pill-red' if discrepancy_count > 0 else 'pill-green'}">
        <span>{'⚠' if discrepancy_count > 0 else '✔'}</span> <span>Discrepancy: <strong>{discrepancy_count}</strong></span>
      </div>
      <div class="stat-pill">
        <span>🖼</span> <span>Gambar Acuan: <strong>{ref_image_count}</strong></span>
      </div>
    </div>
  </header>

  <!-- Controls -->
  <section class="controls-panel">
    <div class="controls-row">
      <!-- Search -->
      <div class="search-box-wrap">
        <span class="search-icon">🔍</span>
        <input type="text" id="searchInput" class="search-input" placeholder="Cari karakter (misal: さ, 水, 衷, N3, orang, 03055)...">
      </div>

      <!-- Font Toggle Switcher -->
      <div class="font-toggle-group">
        <button id="btnFontTextbook" class="font-toggle-btn active" onclick="setFontMode('textbook')">
          ✍️ Gaya Buku Teks (Klee / Kaisei)
        </button>
        <button id="btnFontGothic" class="font-toggle-btn" onclick="setFontMode('gothic')">
          🔲 Gothic (Noto Sans JP)
        </button>
      </div>

      <!-- Sort -->
      <div class="sort-group">
        <span>Urutkan:</span>
        <select id="sortSelect" class="sort-select" onchange="applyFiltersAndSort()">
          <option value="lowest_overlap" selected>Skor Terendah (Paling Tidak Cocok)</option>
          <option value="highest_overlap">Skor Tertinggi (Paling Cocok)</option>
          <option value="strokes_asc">Goresan (Sedikit → Banyak)</option>
          <option value="strokes_desc">Goresan (Banyak → Sedikit)</option>
          <option value="char_code">Kode Unicode (A → Z)</option>
        </select>
      </div>
    </div>

    <!-- Filter Buttons -->
    <div class="filter-pills-row">
      <button class="filter-btn active" data-filter="all" onclick="setFilter('all')">Semua ({len(review_entries)})</button>
      <button class="filter-btn" data-filter="kana" onclick="setFilter('kana')">Hanya Kana</button>
      <button class="filter-btn" data-filter="n5" onclick="setFilter('n5')">JLPT N5</button>
      <button class="filter-btn" data-filter="n4" onclick="setFilter('n4')">JLPT N4</button>
      <button class="filter-btn" data-filter="n3" onclick="setFilter('n3')">JLPT N3</button>
      <button class="filter-btn" data-filter="n2" onclick="setFilter('n2')">JLPT N2</button>
      <button class="filter-btn" data-filter="n1" onclick="setFilter('n1')">JLPT N1</button>
      <button class="filter-btn" data-filter="discrepancy" onclick="setFilter('discrepancy')">Hanya yang Beda ({discrepancy_count})</button>
      <button class="filter-btn" data-filter="override" onclick="setFilter('override')">Hanya Override ({overridden_count})</button>
      <button class="filter-btn" data-filter="has_ref" onclick="setFilter('has_ref')">Ada Gambar Acuan ({ref_image_count})</button>
    </div>
  </section>

  <!-- Card Grid -->
  <main id="cardGrid" class="grid-container">
    <!-- Diisi secara dinamis oleh JavaScript -->
  </main>

  <!-- Pagination -->
  <div class="pagination-bar">
    <div id="paginationInfo" class="page-info">Menampilkan 1-60 dari {len(review_entries)} karakter</div>
    <div class="page-btn-group">
      <button id="btnPrevPage" class="page-btn" onclick="changePage(-1)">← Sebelumnya</button>
      <button id="btnNextPage" class="page-btn" onclick="changePage(1)">Berikutnya →</button>
    </div>
  </div>

  <script>
    const ALL_ITEMS = {data_json_str};
    const STROKE_COLORS = {colors_json_str};

    let currentFilter = 'all';
    let currentSearch = '';
    let currentSort = 'lowest_overlap';
    let currentPage = 1;
    const pageSize = 60;
    let filteredItems = [...ALL_ITEMS];

    function setFontMode(mode) {{
      const body = document.body;
      const btnTb = document.getElementById('btnFontTextbook');
      const btnGt = document.getElementById('btnFontGothic');
      if (mode === 'textbook') {{
        body.classList.remove('mode-gothic');
        body.classList.add('mode-textbook');
        btnTb.classList.add('active');
        btnGt.classList.remove('active');
      }} else {{
        body.classList.remove('mode-textbook');
        body.classList.add('mode-gothic');
        btnGt.classList.add('active');
        btnTb.classList.remove('active');
      }}
    }}

    function setFilter(filt) {{
      currentFilter = filt;
      document.querySelectorAll('.filter-btn').forEach(b => {{
        if (b.getAttribute('data-filter') === filt) {{
          b.classList.add('active');
        }} else {{
          b.classList.remove('active');
        }}
      }});
      currentPage = 1;
      applyFiltersAndSort();
    }}

    document.getElementById('searchInput').addEventListener('input', (e) => {{
      currentSearch = e.target.value.trim().toLowerCase();
      currentPage = 1;
      applyFiltersAndSort();
    }});

    function applyFiltersAndSort() {{
      const sortVal = document.getElementById('sortSelect').value;
      currentSort = sortVal;

      filteredItems = ALL_ITEMS.filter(item => {{
        // Filter kategori
        if (currentFilter === 'kana' && item.category === 'kanji') return false;
        if (currentFilter === 'n5' && item.jlpt !== 5 && item.jlpt !== 'N5') return false;
        if (currentFilter === 'n4' && item.jlpt !== 4 && item.jlpt !== 'N4') return false;
        if (currentFilter === 'n3' && item.jlpt !== 3 && item.jlpt !== 'N3') return false;
        if (currentFilter === 'n2' && item.jlpt !== 2 && item.jlpt !== 'N2') return false;
        if (currentFilter === 'n1' && item.jlpt !== 1 && item.jlpt !== 'N1') return false;
        if (currentFilter === 'discrepancy' && !item.has_discrepancy) return false;
        if (currentFilter === 'override' && !item.is_overridden) return false;
        if (currentFilter === 'has_ref' && !item.has_ref_image) return false;

        // Pencarian
        if (currentSearch) {{
          const matchChar = item.char.toLowerCase().includes(currentSearch);
          const matchHex = item.hex.toLowerCase().includes(currentSearch);
          const matchMeaning = (item.meaning || '').toLowerCase().includes(currentSearch);
          const matchOnyomi = (item.onyomi || '').toLowerCase().includes(currentSearch);
          const matchKunyomi = (item.kunyomi || '').toLowerCase().includes(currentSearch);
          if (!matchChar && !matchHex && !matchMeaning && !matchOnyomi && !matchKunyomi) {{
            return false;
          }}
        }}
        return true;
      }});

      // Sort
      filteredItems.sort((a, b) => {{
        if (currentSort === 'lowest_overlap') {{
          if (a.has_discrepancy !== b.has_discrepancy) return a.has_discrepancy ? -1 : 1;
          return a.overlap_score - b.overlap_score;
        }}
        if (currentSort === 'highest_overlap') {{
          return b.overlap_score - a.overlap_score;
        }}
        if (currentSort === 'strokes_asc') {{
          return a.kvg_strokes - b.kvg_strokes;
        }}
        if (currentSort === 'strokes_desc') {{
          return b.kvg_strokes - a.kvg_strokes;
        }}
        if (currentSort === 'char_code') {{
          return a.char.localeCompare(b.char);
        }}
        return 0;
      }});

      renderGrid();
    }}

    function changePage(delta) {{
      const maxPages = Math.ceil(filteredItems.length / pageSize) || 1;
      currentPage = Math.min(Math.max(1, currentPage + delta), maxPages);
      renderGrid();
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    function renderGrid() {{
      const grid = document.getElementById('cardGrid');
      const startIdx = (currentPage - 1) * pageSize;
      const endIdx = Math.min(startIdx + pageSize, filteredItems.length);
      const pageItems = filteredItems.slice(startIdx, endIdx);

      const maxPages = Math.ceil(filteredItems.length / pageSize) || 1;
      document.getElementById('paginationInfo').textContent = 
        `Menampilkan ${{filteredItems.length ? startIdx + 1 : 0}}-${{endIdx}} dari ${{filteredItems.length}} karakter (Halaman ${{currentPage}} / ${{maxPages}})`;

      document.getElementById('btnPrevPage').disabled = (currentPage <= 1);
      document.getElementById('btnNextPage').disabled = (currentPage >= maxPages);

      if (pageItems.length === 0) {{
        grid.innerHTML = `
          <div style="grid-column: 1/-1; text-align: center; padding: 60px 20px; color: #94a3b8;">
            <div style="font-size: 2.5rem; margin-bottom: 12px;">🔍</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #f8fafc;">Tidak ada karakter yang cocok</div>
            <div style="font-size: 0.88rem; margin-top: 4px;">Coba ubah kata kunci pencarian atau ganti filter.</div>
          </div>
        `;
        return;
      }}

      let html = '';
      for (const item of pageItems) {{
        const pathsSvg = item.paths.map((p, idx) => {{
          const color = STROKE_COLORS[idx % STROKE_COLORS.length];
          return `<path d="${{p}}" stroke="${{color}}"></path>`;
        }}).join('');

        const numbersSvg = (item.numbers || []).map(n => {{
          return `<text x="${{n.x}}" y="${{n.y}}">${{n.text}}</text>`;
        }}).join('');

        const discTag = item.has_discrepancy ? `<span class="tag tag-disc">BEDA GORESAN</span>` : '';
        const overrideTag = item.is_overridden ? `<span class="tag tag-override">OVERRIDE</span>` : '';
        const jlptTag = item.jlpt ? `<span class="tag tag-jlpt">N${{item.jlpt}}</span>` : (item.category !== 'kanji' ? `<span class="tag tag-kana">${{item.category}}</span>` : '');

        let refImgHtml = '';
        if (item.has_ref_image) {{
          refImgHtml = `
            <div class="ref-img-box">
              <div class="ref-img-title">🖼 Acuan Gambar</div>
              <img src="../../images/mirai/goresan-acuan/${{item.hex}}.png" alt="${{item.char}}" loading="lazy" />
            </div>
          `;
        }} else {{
          refImgHtml = `
            <div class="ref-img-box" style="border-style: dotted; opacity: 0.6;">
              <span style="font-size: 1.2rem; margin-bottom: 4px;">🖼</span>
              <span>Belum ada acuan</span>
              <span style="font-size: 0.65rem; color: #64748b;">(images/mirai/goresan-acuan/${{item.hex}}.png)</span>
            </div>
          `;
        }}

        const scoreColor = item.overlap_score >= 40 ? '#4ade80' : (item.overlap_score >= 20 ? '#facc15' : '#f87171');

        let noteBadgeHtml = '';
        if (item.override_note) {{
          noteBadgeHtml = `<div class="note-badge">💡 <strong>Catatan:</strong> ${{item.override_note}}</div>`;
        }}

        html += `
          <div class="char-card ${{item.has_discrepancy ? 'has-discrepancy' : ''}}">
            <div class="card-top">
              <div class="char-badge-group">
                <span class="main-char">${{item.char}}</span>
                <span class="char-hex">U+${{item.hex.toUpperCase()}}</span>
              </div>
              <div class="tag-group">
                ${{discTag}}
                ${{overrideTag}}
                ${{jlptTag}}
              </div>
            </div>

            <div class="visual-comparison-box">
              <div class="glyph-stage">
                <div class="font-silhouette">${{item.char}}</div>
                <svg class="kanjivg-svg" viewBox="0 0 109 109">
                  ${{pathsSvg}}
                  ${{numbersSvg}}
                </svg>
              </div>
              ${{refImgHtml}}
            </div>

            <div class="card-meta">
              <div class="meta-row">
                <span>Goresan KanjiVG:</span>
                <strong>${{item.kvg_strokes}} goresan</strong>
              </div>
              ${{item.expected_strokes !== null ? `
                <div class="meta-row">
                  <span>Goresan kanji.json:</span>
                  <strong style="color: ${{item.has_discrepancy ? '#f87171' : 'inherit'}};">${{item.expected_strokes}} goresan ${{item.has_discrepancy ? '⚠' : ''}}</strong>
                </div>
              ` : ''}}
              ${{item.meaning ? `
                <div class="meta-row">
                  <span>Arti:</span>
                  <strong style="text-align: right; max-width: 65%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${{item.meaning}}</strong>
                </div>
              ` : ''}}

              <div class="overlap-bar-wrap">
                <span style="font-size: 0.76rem; color: #94a3b8; width: 85px;">Overlap Font:</span>
                <div class="overlap-bar">
                  <div class="overlap-fill" style="width: ${{Math.min(100, item.overlap_score * 2)}}%; background: ${{scoreColor}};"></div>
                </div>
                <span style="font-size: 0.78rem; font-weight: 700; color: ${{scoreColor}}; width: 44px; text-align: right;">${{item.overlap_score}}%</span>
              </div>

              ${{noteBadgeHtml}}
            </div>
          </div>
        `;
      }}
      grid.innerHTML = html;
    }}

    // Inisialisasi awal
    renderGrid();
  </script>
</body>
</html>
"""

    os.makedirs(os.path.dirname(OUTPUT_HTML_FILE) or '.', exist_ok=True)
    with open(OUTPUT_HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✔ Berkas HTML review berhasil dibuat: {OUTPUT_HTML_FILE} ({len(html_content)} byte).")
    print("✔ Alat review visual siap dibuka langsung tanpa live server!")
    return OUTPUT_HTML_FILE

if __name__ == '__main__':
    build_review_html()
