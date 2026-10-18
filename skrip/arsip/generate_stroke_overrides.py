#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: skrip/arsip/generate_stroke_overrides.py
Fungsi: Menghitung ulang label angka goresan yang terlalu jauh (>12 satuan) dari titik awal,
        menerapkan pencegahan overlap (jarak minimal 7), dan menambahkan catatan varian
        gaya buku teks (kyōkasho) vs gothic untuk disimpan ke data/stroke-overrides.json
        serta js/stroke-overrides.js (untuk kompatibilitas offline 100% tanpa server).
"""

import os
import re
import json
import math

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STROKE_DATA_PATH = os.path.join(BASE_DIR, "js", "stroke-data.js")
OVERRIDES_JSON_PATH = os.path.join(BASE_DIR, "data", "stroke-overrides.json")
OVERRIDES_JS_PATH = os.path.join(BASE_DIR, "js", "stroke-overrides.js")

# Varian resmi gaya buku teks (kyōkasho) vs gothic
KNOWN_VARIANTS = {
    "さ": {
        "variant": "kyokasho",
        "note": "Gaya buku teks (kyōkasho). Di font gothic/cetak goresan bawah bisa tersambung."
    },
    "き": {
        "variant": "kyokasho",
        "note": "Gaya buku teks (kyōkasho). Di font gothic/cetak goresan bawah bisa tersambung."
    },
    "ぎ": {
        "variant": "kyokasho",
        "note": "Gaya buku teks (kyōkasho). Di font gothic/cetak goresan bawah bisa tersambung."
    },
    "ざ": {
        "variant": "kyokasho",
        "note": "Gaya buku teks (kyōkasho). Di font gothic/cetak goresan bawah bisa tersambung."
    },
    "ク": {
        "variant": "kyokasho",
        "note": "Gaya buku teks (kyōkasho). Goresan pertama berupa sapuan miring terpisah."
    },
    "女": {
        "variant": "kyokasho",
        "note": "Gaya buku teks (kyōkasho). Titik persilangan goresan pertama dan kedua berbeda dari font cetak."
    },
    "年": {
        "variant": "kyokasho",
        "note": "Gaya buku teks (kyōkasho). Urutan goresan resmi standar pendidikan Jepang."
    },
    "左": {
        "variant": "kyokasho",
        "note": "Gaya buku teks (kyōkasho). Goresan pertama adalah mendatar (berbeda dari 右 yang diawali garis miring)."
    },
    "り": {
        "variant": "kyokasho",
        "note": "Gaya buku teks (kyōkasho). Kedua goresan terpisah (pada font cetak sering bersambung)."
    },
    "そ": {
        "variant": "kyokasho",
        "note": "Gaya buku teks (kyōkasho). Ditulis dalam satu goresan berkelanjutan tanpa putus."
    }
}

def get_stroke_direction(d_str):
    """
    Mengekstrak titik awal (sx, sy) dan unit vektor tangen (tx, ty) dari kurva SVG.
    """
    tokens = re.findall(r'([A-Za-z]|[-+]?(?:[0-9]*\.[0-9]+|[0-9]+)(?:[eE][-+]?[0-9]+)?)', d_str)
    if not tokens:
        return None, None
    idx = 0
    if tokens[idx] in ('M', 'm'):
        cmd = tokens[idx]
        idx += 1
        sx = float(tokens[idx])
        sy = float(tokens[idx+1])
        idx += 2
    else:
        return None, None
    
    target_x, target_y = None, None
    if idx < len(tokens):
        next_cmd = tokens[idx]
        if next_cmd.isalpha():
            idx += 1
        else:
            next_cmd = 'L' if cmd == 'M' else 'l'
        c = next_cmd
        if c in ('C', 'Q', 'S'):
            target_x = float(tokens[idx])
            target_y = float(tokens[idx+1])
        elif c in ('c', 'q', 's'):
            target_x = sx + float(tokens[idx])
            target_y = sy + float(tokens[idx+1])
        elif c == 'L':
            target_x = float(tokens[idx])
            target_y = float(tokens[idx+1])
        elif c == 'l':
            target_x = sx + float(tokens[idx])
            target_y = sy + float(tokens[idx+1])
        elif c == 'H':
            target_x = float(tokens[idx])
            target_y = sy
        elif c == 'h':
            target_x = sx + float(tokens[idx])
            target_y = sy
        elif c == 'V':
            target_x = sx
            target_y = float(tokens[idx])
        elif c == 'v':
            target_x = sx
            target_y = sy + float(tokens[idx])
            
    if target_x is None or (target_x == sx and target_y == sy):
        target_x, target_y = sx + 1.0, sy
        
    dx = target_x - sx
    dy = target_y - sy
    length = math.hypot(dx, dy)
    tx, ty = (dx / length, dy / length) if length > 0 else (1.0, 0.0)
    return (sx, sy), (tx, ty)

def fix_numbers(paths, numbers):
    """
    Hitung ulang posisi label angka: bila jaraknya >12 dari titik awal goresan,
    geser ke samping luar goresan (offset 6 satuan sepanjang normal),
    dan cegah dua label saling menimpa (jarak minimal 7).
    """
    if not numbers or len(numbers) != len(paths):
        return numbers, False, 0
    
    modified = False
    new_numbers = [dict(num) for num in numbers]
    fixed_label_count = 0
    
    for idx, num in enumerate(new_numbers):
        st, tang = get_stroke_direction(paths[idx])
        if not st:
            continue
        dist = math.hypot(num['x'] - st[0], num['y'] - st[1])
        if dist > 12.0:
            modified = True
            fixed_label_count += 1
            tx, ty = tang
            # Dua vektor normal tegak lurus
            n1 = (-ty, tx)
            n2 = (ty, -tx)
            # Pilih vektor normal yang searah dengan posisi relatif awal nomor ke titik awal
            orig_dir = (num['x'] - st[0], num['y'] - st[1])
            dot1 = orig_dir[0] * n1[0] + orig_dir[1] * n1[1]
            dot2 = orig_dir[0] * n2[0] + orig_dir[1] * n2[1]
            norm = n1 if dot1 >= dot2 else n2
            
            # Geser 6 satuan sepanjang normal
            new_numbers[idx]['x'] = round(st[0] + 6.0 * norm[0], 2)
            new_numbers[idx]['y'] = round(st[1] + 6.0 * norm[1], 2)
            
    if not modified:
        return numbers, False, 0

    # Pencegahan overlap: jarak antar label minimal 7.0 satuan
    for _ in range(30):
        overlap_found = False
        for i in range(len(new_numbers)):
            for j in range(i + 1, len(new_numbers)):
                p1 = new_numbers[i]
                p2 = new_numbers[j]
                dx = p1['x'] - p2['x']
                dy = p1['y'] - p2['y']
                d = math.hypot(dx, dy)
                if d < 7.0:
                    overlap_found = True
                    if d < 1e-4:
                        dx, dy = 1.0, 0.0
                        d = 1.0
                    shift = (7.0 - d) / 2.0
                    ux, uy = dx / d, dy / d
                    p1['x'] = round(p1['x'] + ux * shift, 2)
                    p1['y'] = round(p1['y'] + uy * shift, 2)
                    p2['x'] = round(p2['x'] - ux * shift, 2)
                    p2['y'] = round(p2['y'] - uy * shift, 2)
        if not overlap_found:
            break

    # Batasi ke dalam viewBox [4, 105]
    for p in new_numbers:
        p['x'] = round(max(4.0, min(105.0, p['x'])), 2)
        p['y'] = round(max(6.0, min(105.0, p['y'])), 2)
        
    return new_numbers, True, fixed_label_count

def generate_overrides():
    print("Membaca stroke-data.js...")
    with open(STROKE_DATA_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.search(r'window\.MIRAI_STROKE_DATA\s*=\s*(\{[\s\S]*\});?\s*$', content)
    if not m:
        raise ValueError("Gagal menemukan window.MIRAI_STROKE_DATA di js/stroke-data.js")
    
    stroke_data = json.loads(m.group(1))
    print(f"Total karakter terdaftar di stroke-data: {len(stroke_data)}")

    overrides = {}
    total_labels_fixed = 0

    # 1. Tambahkan varian resmi
    for char, info in KNOWN_VARIANTS.items():
        overrides[char] = {
            "variant": info["variant"],
            "note": info["note"]
        }

    # 2. Hitung perbaikan label untuk karakter yang memiliki label > 12 satuan
    characters_fixed = 0
    for char, record in stroke_data.items():
        paths = record.get("paths", [])
        numbers = record.get("numbers", [])
        new_numbers, modified, count = fix_numbers(paths, numbers)
        if modified:
            characters_fixed += 1
            total_labels_fixed += count
            if char not in overrides:
                overrides[char] = {}
            overrides[char]["numbers"] = new_numbers

    # Simpan ke data/stroke-overrides.json
    os.makedirs(os.path.dirname(OVERRIDES_JSON_PATH), exist_ok=True)
    with open(OVERRIDES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(overrides, f, ensure_ascii=False, indent=2)
    print(f"✔ Berkas disimpan: {OVERRIDES_JSON_PATH} ({len(overrides)} karakter di-override).")

    # Simpan ke js/stroke-overrides.js untuk dukungan instan file:// offline
    js_header = """/**
 * File: js/stroke-overrides.js
 * Lapisan Override Kurasi Resmi untuk Urutan Goresan & Label Posisi KanjiVG.
 * Berfungsi menjaga perbaikan manual, varian gaya buku teks, dan posisi label angka
 * agar tidak pernah hilang saat sinkronisasi otomatis.
 * Penggunaan: kamus/index.html, kamus/kanji.html, kelas/latihan.html
 */

window.MIRAI_STROKE_OVERRIDES = """
    with open(OVERRIDES_JS_PATH, "w", encoding="utf-8") as f:
        f.write(js_header + json.dumps(overrides, ensure_ascii=False) + ";\n")
    print(f"✔ Berkas disimpan: {OVERRIDES_JS_PATH}")
    print(f"Ringkasan: {len(overrides)} karakter di-override, {characters_fixed} karakter label dirapikan ({total_labels_fixed} label).")

if __name__ == "__main__":
    generate_overrides()
