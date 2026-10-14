#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to fetch official SVG stroke paths and stroke numbers from KanjiVG
for all characters in data/kana.json and data/kanji.json,
write js/stroke-data.js, and calibrate js/stroke.js viewBox & positioning.
"""

import json
import re
import urllib.request
import concurrent.futures
import time

def get_characters():
    with open('data/kana.json', 'r', encoding='utf-8') as f:
        kana = json.load(f)
    with open('data/kanji.json', 'r', encoding='utf-8') as f:
        kanji = json.load(f)
    with open('js/stroke-data.js', 'r', encoding='utf-8') as f:
        stroke_content = f.read()

    chars = set()
    # 1. Kana (Hiragana & Katakana, including Yoon parts)
    for h in kana.get('hiragana', []):
        for c in h.get('character', ''):
            chars.add(c)
    for k in kana.get('katakana', []):
        for c in k.get('character', ''):
            chars.add(c)

    # 2. Kanji
    for kj in kanji:
        for c in kj.get('kanji', ''):
            chars.add(c)

    # 3. Existing stroke-data keys (to preserve small vowels like ヴ, ァ, etc.)
    for c in re.findall(r'\"([^\"]+)\"\s*:\s*\{', stroke_content):
        chars.add(c)

    return sorted(list(chars))

def fetch_one(ch):
    hex_code = f'{ord(ch):05x}'
    url = f'https://raw.githubusercontent.com/KanjiVG/kanjivg/master/kanji/{hex_code}.svg'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = resp.read().decode('utf-8')
        
        # Extract path d="..." attributes
        paths = re.findall(r'<path[^>]+d=\"([^\"]+)\"', data)
        
        # Extract stroke numbers: <text ... transform="matrix(1 0 0 1 x y)">num</text>
        raw_nums = re.findall(r'<text[^>]+transform=\"matrix\([^)]+\s+([\d\.]+)\s+([\d\.]+)\)\"[^>]*>([^<]+)</text>', data)
        numbers = [{'x': round(float(x), 2), 'y': round(float(y), 2), 'text': t.strip()} for x, y, t in raw_nums]

        if not paths:
            print(f"Warning: No paths found for {ch} ({hex_code})")
            return ch, None

        return ch, {
            'viewBox': '0 0 109 109',
            'paths': paths,
            'numbers': numbers,
            'source': 'KanjiVG'
        }
    except Exception as e:
        print(f"Error fetching {ch} ({hex_code}): {e}")
        return ch, None

def update_stroke_data_js(char_data_map):
    print("Writing updated js/stroke-data.js...")
    header = """/**
 * File: js/stroke-data.js
 * Fungsi: Vektor koordinat kurva goresan resmi KanjiVG untuk Kana & Kanji (viewBox: 0 0 109 109).
 * Penggunaan: Dimuat di kamus/index.html, kamus/kanji.html, dan kelas/latihan.html.
 */

window.MIRAI_STROKE_DATA = """
    
    # Dump JSON with compact separators
    json_str = json.dumps(char_data_map, ensure_ascii=False, indent=2)
    output = header + json_str + ";\n"

    with open('js/stroke-data.js', 'w', encoding='utf-8') as f:
        f.write(output)
    print(f"js/stroke-data.js successfully written ({len(output)} bytes)")

def update_stroke_js():
    print("Calibrating js/stroke.js to KanjiVG 0 0 109 109 standard...")
    with open('js/stroke.js', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update calculateStrokeNumbers to trust official KanjiVG numbers directly
    old_calc_pattern = r'function calculateStrokeNumbers\(paths,\s*officialNumbers\)\s*\{[\s\S]*?\n\}'
    new_calc = """function calculateStrokeNumbers(paths, officialNumbers) {
    function parseStart(d) {
        let sx = 25, sy = 25;
        const m = /^[Mm]\\s*([-\\d\\.]+)[,\\s]+([-\\d\\.]+)/.exec(d);
        if (m) {
            sx = parseFloat(m[1]);
            sy = parseFloat(m[2]);
        }
        return { sx, sy };
    }

    const hasOfficial = Array.isArray(officialNumbers) && officialNumbers.length >= paths.length;
    const placed = [];

    paths.forEach((d, i) => {
        const { sx, sy } = parseStart(d);
        let nx, ny;

        if (hasOfficial && officialNumbers[i] && typeof officialNumbers[i].x === 'number') {
            nx = officialNumbers[i].x;
            ny = officialNumbers[i].y;
        } else {
            nx = sx >= 12 ? sx - 6.5 : sx + 6;
            ny = sy >= 12 ? sy - 2.5 : sy + 7;
        }

        nx = Math.max(5, Math.min(104, nx));
        ny = Math.max(5, Math.min(104, ny));

        placed.push({
            x: nx,
            y: ny,
            text: (hasOfficial && officialNumbers[i]?.text) ? officialNumbers[i].text : String(i + 1)
        });
    });

    return placed;
}"""

    match = re.search(old_calc_pattern, content)
    if match:
        content = content[:match.start()] + new_calc + content[match.end():]
        print("Updated calculateStrokeNumbers in js/stroke.js")

    # 2. Ensure svg.setAttribute("viewBox", "0 0 109 109")
    content = content.replace('svg.setAttribute("viewBox", rec?.viewBox || "0 0 109 109");', 'svg.setAttribute("viewBox", "0 0 109 109");')

    # 3. Clean all stroke caches in localStorage
    old_cache_cleaner = 'if (k && (k.startsWith("mirai_stroke_v1_") || k.startsWith("mirai_stroke_v2_") || k.startsWith("mirai_stroke_v3_")))'
    new_cache_cleaner = 'if (k && k.startsWith("mirai_stroke_"))'
    if old_cache_cleaner in content:
        content = content.replace(old_cache_cleaner, new_cache_cleaner)
        print("Updated localStorage cache invalidation in js/stroke.js")

    with open('js/stroke.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print("js/stroke.js calibrated successfully")

def main():
    chars = get_characters()
    print(f"Fetching official KanjiVG SVG data for {len(chars)} unique characters...")
    t0 = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
        results = list(executor.map(fetch_one, chars))

    data_map = {}
    failed = []
    for ch, data in results:
        if data:
            data_map[ch] = data
        else:
            failed.append(ch)

    print(f"Fetched {len(data_map)} / {len(chars)} characters in {time.time()-t0:.2f}s")
    if failed:
        print(f"WARNING: Failed to fetch: {failed}")

    update_stroke_data_js(data_map)
    update_stroke_js()
    print("\nALL TASKS COMPLETED SUCCESSFULLY!")

if __name__ == '__main__':
    main()
