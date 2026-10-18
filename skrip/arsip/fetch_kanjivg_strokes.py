#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: skrip/arsip/fetch_kanjivg_strokes.py
Fungsi: Mengambil, mem-parsing via XML/SVG, memvalidasi, dan memperbarui dataset goresan KanjiVG
        untuk seluruh karakter di data/kana.json dan data/kanji.json secara aman.

Fitur Keamanan & Arsitektur:
  1. Parser XML/SVG berbasis xml.etree.ElementTree (mematuhi hierarki StrokePaths & urutan -sN).
  2. Ekstraksi koordinat angka goresan presisi dari StrokeNumbers.
  3. Perlindungan dataset lama: hasil ditulis ke berkas pementasan (staging) js/stroke-data.tmp.js.
  4. Penggabungan bertahap (incremental merge): entri yang sudah valid tidak pernah dibuang jika fetch parsial.
  5. Validasi otomatis pra-terap sebelum menimpa berkas produksi js/stroke-data.js.
  6. Mempertahankan lisensi resmi KanjiVG (CC BY-SA 3.0, Ulrich Apel & kontributor) dan atribusi.
  7. Menghasilkan manifest cakupan data di data/stroke-coverage-manifest.json.
"""

import sys
import os
import json
import re
import zipfile
import urllib.request
import argparse
import time
from datetime import datetime, timezone
import xml.etree.ElementTree as ET

# Impor modul validator lokal jika tersedia di path
try:
    from validate_stroke_data import validate_dataset, load_app_requirements, generate_coverage_manifest, validate_overrides_integrity
except ImportError:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, script_dir)
    from validate_stroke_data import validate_dataset, load_app_requirements, generate_coverage_manifest, validate_overrides_integrity

KANJIVG_RELEASE_ZIP_URL = "https://github.com/KanjiVG/kanjivg/releases/download/r20260714/kanjivg-20260714-main.zip"
CACHE_DIR = ".cache/kanjivg"
CACHE_ZIP_PATH = os.path.join(CACHE_DIR, "kanjivg-20260714-main.zip")
STAGING_FILE = "js/stroke-data.tmp.js"
PROD_FILE = "js/stroke-data.js"
MANIFEST_FILE = "data/stroke-coverage-manifest.json"
OVERRIDES_FILE = "data/stroke-overrides.json"

HEADER_TEMPLATE = """/**
 * File: js/stroke-data.js
 * Lisensi & Atribusi:
 *   Data vektor kurva goresan bersumber dari proyek resmi KanjiVG (https://kanjivg.tagaini.net/).
 *   Hak Cipta (C) 2009-2026 Ulrich Apel dan para kontributor KanjiVG.
 *   Dilisensikan di bawah Creative Commons Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0).
 *   Lihat: https://creativecommons.org/licenses/by-sa/3.0/ dan data/STROKES-LICENSE.md
 *
 * Spesifikasi:
 *   - Sistem koordinat kanvas: viewBox="0 0 109 109"
 *   - Urutan goresan: tersortir secara kronologis berdasarkan indeks resmi KanjiVG
 *   - Penggunaan: kamus/index.html, kamus/kanji.html, kelas/latihan.html, dan latihan interaktif
 */

window.MIRAI_STROKE_DATA = """

def load_existing_stroke_data(filepath=PROD_FILE):
    """
    Membaca dataset yang sudah ada agar tidak ada data hilang jika pemrosesan parsial.
    """
    if not os.path.isfile(filepath):
        return {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        m = re.search(r'window\.MIRAI_STROKE_DATA\s*=\s*(\{[\s\S]*\});?\s*$', content)
        if m:
            return json.loads(m.group(1))
    except Exception as e:
        print(f"Peringatan: Gagal membaca {filepath}: {e}")
    return {}

def load_stroke_overrides(filepath=OVERRIDES_FILE):
    """
    Membaca berkas data/stroke-overrides.json untuk melindungi perbaikan manual
    dan memastikan pipeline tidak pernah menimpa penyesuaian yang disengaja.
    """
    if not os.path.isfile(filepath):
        return {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Peringatan: Gagal membaca file override {filepath}: {e}")
        return {}

def ensure_kanjivg_archive():
    """
    Memastikan arsip rilis resmi KanjiVG tersedia di direktori cache lokal.
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    if os.path.isfile(CACHE_ZIP_PATH) and os.path.getsize(CACHE_ZIP_PATH) > 1000000:
        return CACHE_ZIP_PATH

    print(f"Mengunduh arsip rilis resmi KanjiVG ({KANJIVG_RELEASE_ZIP_URL})...")
    req = urllib.request.Request(KANJIVG_RELEASE_ZIP_URL, headers={'User-Agent': 'Mozilla/5.0 (compatible; MiraiNoWebu/1.0)'})
    with urllib.request.urlopen(req, timeout=60) as resp, open(CACHE_ZIP_PATH, 'wb') as out:
        out.write(resp.read())
    print(f"Unduhan selesai: {os.path.getsize(CACHE_ZIP_PATH)} byte tersimpan di {CACHE_ZIP_PATH}")
    return CACHE_ZIP_PATH

def parse_kanjivg_svg(svg_content):
    """
    Mem-parsing konten SVG KanjiVG menggunakan XML ElementTree secara struktural.
    Mengembalikan dict data atau None jika tidak valid.
    """
    try:
        root = ET.fromstring(svg_content)
    except ET.ParseError as err:
        return None, f"Kesalahan parsing XML: {err}"

    view_box = root.attrib.get('viewBox', '0 0 109 109')

    # Cari grup StrokePaths dan StrokeNumbers
    paths_group = None
    numbers_group = None

    for elem in root.iter():
        elem_id = elem.attrib.get('id', '')
        if 'StrokePaths' in elem_id:
            paths_group = elem
        elif 'StrokeNumbers' in elem_id:
            numbers_group = elem

    # 1. Ekstrak path kurva goresan
    path_entries = []
    search_root = paths_group if paths_group is not None else root
    for elem in search_root.iter():
        if elem.tag.endswith('path'):
            pid = elem.attrib.get('id', '')
            d = elem.attrib.get('d', '').strip()
            if d:
                # Ambil indeks goresan (-s1, -s2, ...)
                m = re.search(r'-s(\d+)$', pid)
                order_idx = int(m.group(1)) if m else len(path_entries) + 1
                path_entries.append((order_idx, pid, d))

    if not path_entries:
        return None, "Tidak ada elemen path goresan yang ditemukan"

    # Sortir berdasarkan indeks urutan resmi goresan
    path_entries.sort(key=lambda x: x[0])
    sorted_paths = [p[2] for p in path_entries]

    # 2. Ekstrak label angka dan koordinat transform
    numbers = []
    if numbers_group is not None:
        for elem in numbers_group.iter():
            if elem.tag.endswith('text'):
                trans = elem.attrib.get('transform', '')
                txt = (elem.text or '').strip()
                # Pola matrix(1 0 0 1 x y) atau matrix(1,0,0,1,x,y)
                m = re.search(r'matrix\s*\(\s*[^,\s]+\s*[, ]\s*[^,\s]+\s*[, ]\s*[^,\s]+\s*[, ]\s*[^,\s]+\s*[, ]\s*([-\d\.]+)\s*[, ]\s*([-\d\.]+)\s*\)', trans)
                if m and txt:
                    numbers.append({
                        'x': round(float(m.group(1)), 2),
                        'y': round(float(m.group(2)), 2),
                        'text': txt
                    })

    return {
        'viewBox': view_box,
        'paths': sorted_paths,
        'numbers': numbers,
        'source': 'KanjiVG'
    }, None

def fetch_single_from_network(hex_code, retries=3):
    """
    Fallback untuk mengambil satu berkas SVG dari repositori GitHub resmi jika diperlukan.
    """
    url = f"https://raw.githubusercontent.com/KanjiVG/kanjivg/master/kanji/{hex_code}.svg"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; MiraiNoWebu/1.0)'})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.read().decode('utf-8')
        except Exception:
            if attempt < retries - 1:
                time.sleep(1.0)
    return None

def write_staging_dataset(data_map, filepath=STAGING_FILE):
    """
    Menulis data ke berkas pementasan sementara.
    """
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    json_body = json.dumps(data_map, ensure_ascii=False, indent=2)
    content = HEADER_TEMPLATE + json_body + ";\n"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return len(content)

def main():
    parser = argparse.ArgumentParser(description="Pembaruan dan ekstraksi data goresan resmi KanjiVG.")
    parser.add_argument('--limit', type=int, default=0, help='Batasi pemrosesan hanya untuk N karakter pertama (untuk pengetesan)')
    parser.add_argument('--staging-only', action='store_true', help='Hanya tulis berkas staging (js/stroke-data.tmp.js) tanpa mengganti file produksi')
    parser.add_argument('--dry-run', action='store_true', help='Uji pengambilan dan validasi tanpa menulis file apa pun ke disk')
    parser.add_argument('--apply', action='store_true', help='Terapkan ke produksi (js/stroke-data.js) setelah validasi 100%% lolos')
    args = parser.parse_args()

    print(f"==================================================")
    print(f"🌸 MIRAI NO WEBU - KANJIVG STROKE DATA PIPELINE")
    print(f"==================================================")

    # 1. Muat metadata aplikasi untuk mengetahui target karakter
    kana_map, kanji_map = load_app_requirements()
    target_chars = sorted(list(set(k for k in kana_map.keys() if len(k) == 1) | set(kanji_map.keys())))
    if args.limit > 0:
        target_chars = target_chars[:args.limit]
        print(f"⚠ Mode dibatasi: memproses {len(target_chars)} karakter pertama.")
    else:
        print(f"✔ Target karakter terdeteksi: {len(target_chars)} karakter ({len(kana_map)} kana, {len(kanji_map)} kanji).")

    # 2. Muat dataset lama untuk melindungi data jika fetch parsial
    existing_data = load_existing_stroke_data(PROD_FILE)
    print(f"✔ Dataset lama dimuat: {len(existing_data)} entri sudah ada.")

    # 2b. Muat lapisan override manual
    overrides = load_stroke_overrides(OVERRIDES_FILE)
    print(f"✔ Lapisan override dimuat: {len(overrides)} entri terdeteksi dari {OVERRIDES_FILE}.")

    # 3. Pastikan arsip rilis KanjiVG tersedia
    try:
        zip_path = ensure_kanjivg_archive()
    except Exception as e:
        print(f"❌ Gagal memuat arsip KanjiVG: {e}")
        sys.exit(1)

    # 4. Buka arsip dan ekstrak seluruh target karakter
    data_map = dict(existing_data)  # Salin data lama sebagai dasar perlindungan
    failed_chars = []
    success_count = 0

    t0 = time.time()
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zip_namelist = set(zf.namelist())

        for idx, char in enumerate(target_chars):
            hex_code = f"{ord(char):05x}"
            svg_filename = f"kanji/{hex_code}.svg"

            svg_text = None
            if svg_filename in zip_namelist:
                svg_text = zf.read(svg_filename).decode('utf-8')
            else:
                # Coba fallback individual jaringan jika tidak ada di arsip
                svg_text = fetch_single_from_network(hex_code)

            if not svg_text:
                if char not in data_map:
                    failed_chars.append((char, hex_code, "Berkas SVG tidak ditemukan di arsip maupun jaringan"))
                continue

            parsed, err = parse_kanjivg_svg(svg_text)
            if err or not parsed:
                if char not in data_map:
                    failed_chars.append((char, hex_code, err or "Parsing gagal"))
            else:
                data_map[char] = parsed
                success_count += 1

    dur = time.time() - t0
    print(f"✔ Pemrosesan selesai dalam {dur:.2f} detik: {success_count} karakter berhasil diproses dari KanjiVG.")
    if failed_chars:
        print(f"⚠ Karakter yang gagal didapatkan ({len(failed_chars)}):")
        for fch, fhex, ferr in failed_chars[:5]:
            print(f"  - {fch} ({fhex}): {ferr}")
        if len(failed_chars) > 5:
            print(f"  ... dan {len(failed_chars) - 5} lainnya.")

    # 4b. Terapkan lapisan override (override selalu menang atas data mentah KanjiVG)
    applied_overrides_count = 0
    for char, ov in overrides.items():
        if char in data_map:
            if "paths" in ov and ov["paths"]:
                data_map[char]["paths"] = list(ov["paths"])
            if "numbers" in ov and ov["numbers"]:
                data_map[char]["numbers"] = list(ov["numbers"])
            if "variant" in ov:
                data_map[char]["variant"] = ov["variant"]
            if "note" in ov:
                data_map[char]["note"] = ov["note"]
            data_map[char]["overridden"] = True
            applied_overrides_count += 1
        elif "paths" in ov and ov["paths"]:
            data_map[char] = {
                'viewBox': '0 0 109 109',
                'paths': list(ov['paths']),
                'numbers': list(ov.get('numbers', [])),
                'variant': ov.get('variant'),
                'note': ov.get('note'),
                'overridden': True,
                'source': 'Override'
            }
            applied_overrides_count += 1

    print(f"✔ Lapisan override diterapkan: {applied_overrides_count} karakter diproteksi/disesuaikan.")
    print(f"✔ Total karakter dalam dataset baru yang disiapkan: {len(data_map)} entri.")

    if args.dry_run:
        print("\n[DRY RUN] Tidak ada berkas yang ditulis ke disk.")
        sys.exit(0)

    # 5. Tulis ke berkas pementasan sementara (staging file)
    bytes_written = write_staging_dataset(data_map, STAGING_FILE)
    print(f"✔ Berkas staging berhasil ditulis: {STAGING_FILE} ({bytes_written} byte).")

    # 6. Jalankan validator terhadap berkas staging
    print(f"\n🔍 Menjalankan validator terhadap berkas staging ({STAGING_FILE})...")
    val_results = validate_dataset(data_map, kana_map, kanji_map)
    manifest = generate_coverage_manifest(data_map, val_results, kana_map, kanji_map, MANIFEST_FILE)

    # Periksa integritas lapisan override di data_map
    ov_ok, ov_count, ov_errors = validate_overrides_integrity(data_map, OVERRIDES_FILE)
    if not ov_ok:
        print(f"\n❌ VALIDASI INTEGRITAS OVERRIDE GAGAL ({len(ov_errors)} kesalahan):")
        for err in ov_errors[:10]:
            print(f"  - {err}")
        val_results['invalid_entries'] += len(ov_errors)
    else:
        print(f"✔ Integritas seluruh {ov_count} override terverifikasi dan terlindungi.")

    val_summary = manifest['summary']
    print(f"  - Total entri staging : {val_summary['dataset_total_entries']}")
    print(f"  - Entri valid         : {val_summary['dataset_valid_entries']}")
    print(f"  - Entri tidak valid   : {val_summary['dataset_invalid_entries']}")
    print(f"  - Tingkat cakupan     : {val_summary['coverage_rate_percent']}%")
    print(f"  - Discrepancy meta    : {val_summary['metadata_discrepancies']}")

    # 7. Evaluasi apakah aman untuk diterapkan ke produksi
    if val_summary['dataset_invalid_entries'] > 0:
        print(f"\n❌ VALIDASI STAGING GAGAL: {val_summary['dataset_invalid_entries']} entri tidak valid.")
        print(f"   Berkas produksi {PROD_FILE} DILINDUNGI dan TIDAK disentuh.")
        sys.exit(1)

    print(f"✔ Seluruh {val_summary['dataset_valid_entries']} entri dalam staging 100% VALID.")

    if args.staging_only:
        print(f"\n✔ Mode --staging-only aktif: Hasil pementasan disimpan di {STAGING_FILE}.")
        print(f"  Berkas produksi {PROD_FILE} belum diperbarui.")
        sys.exit(0)

    if args.apply:
        # Penggantian berkas secara atomik
        print(f"\n🚀 Menerapkan staging ({STAGING_FILE}) ke produksi ({PROD_FILE})...")
        os.replace(STAGING_FILE, PROD_FILE)
        print(f"✔ Dataset produksi {PROD_FILE} berhasil diperbarui secara atomik!")
        print(f"✔ Manifest laporan cakupan tersimpan di {MANIFEST_FILE}.")
    else:
        print(f"\n💡 File pementasan siap di {STAGING_FILE}.")
        print(f"   Jalankan dengan bendera '--apply' untuk memperbarui {PROD_FILE} secara permanen.")

if __name__ == '__main__':
    main()
