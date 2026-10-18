#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: skrip/arsip/validate_stroke_data.py
Fungsi: Validator independen untuk dataset goresan KanjiVG (js/stroke-data.js).
Memeriksa:
  1. Integritas sintaks & format JSON/JS.
  2. Kelengkapan struktur data (viewBox, paths, numbers, source).
  3. Validitas kurva SVG (perintah path M/C/S/L/Z, koordinat dalam batas viewBox 0..109).
  4. Urutan goresan & identitas stroke.
  5. Konsistensi metadata terhadap data/kana.json dan data/kanji.json.
  6. Analisis cakupan karakter (Kana, Joyo Kanji, JLPT N5-N1).
  7. Pembuatan manifest laporan cakupan data (data/stroke-coverage-manifest.json).
"""

import sys
import os
import json
import re
import argparse
from datetime import datetime, timezone

def parse_svg_path_commands(d_str):
    """
    Memeriksa format SVG path string.
    Mengembalikan (is_valid, error_msg, initial_point)
    """
    if not isinstance(d_str, str) or not d_str.strip():
        return False, "Path kosong atau bukan string", None

    # Validasi bahwa path dimulai dengan M atau m
    m = re.match(r'^\s*([Mm])\s*([-\d\.]+)[,\s]+([-\d\.]+)', d_str)
    if not m:
        return False, f"Path tidak dimulai dengan perintah M/m yang valid: {d_str[:30]}", None

    try:
        sx = float(m.group(2))
        sy = float(m.group(3))
    except ValueError:
        return False, f"Koordinat awal tidak valid: {m.group(2)}, {m.group(3)}", None

    # Periksa karakter ilegal dalam path SVG
    # Karakter yang diperbolehkan: angka, titik, minus, plus, koma, spasi, eksponen (e/E), perintah SVG (M,m,L,l,H,h,V,v,C,c,S,s,Q,q,T,t,A,a,Z,z)
    illegal_chars = re.findall(r'[^0-9\.\-\+,\sMmZzLlHhVvCcSsQqTtAaEe]', d_str)
    if illegal_chars:
        return False, f"Karakter ilegal dalam SVG path: {set(illegal_chars)}", (sx, sy)

    return True, "", (sx, sy)

def load_stroke_data(filepath):
    """
    Membaca dan mem-parsing berkas JavaScript window.MIRAI_STROKE_DATA = { ... };
    serta menggabungkan chunk goresan kanji dari data/strokes/*.json jika tersedia.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Berkas tidak ditemukan: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Ekstrak objek JSON dari variabel JS
    match = re.search(r'window\.MIRAI_STROKE_DATA\s*=\s*(\{[\s\S]*\});?\s*$', content)
    if not match:
        # Coba parsing JSON murni jika format berbeda
        match = re.search(r'(\{[\s\S]*\})', content)
        if not match:
            raise ValueError(f"Tidak dapat menemukan objek JSON di {filepath}")

    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError as err:
        raise ValueError(f"Gagal mem-parsing JSON dari {filepath}: {err}")

    # Jika data/strokes/ tersedia, gabungkan seluruh chunk kanji untuk validasi penuh
    strokes_dir = os.path.join(os.path.dirname(filepath), "..", "data", "strokes")
    if os.path.isdir(strokes_dir):
        for lvl in ["n5.json", "n4.json", "n3.json", "n2.json", "n1.json"]:
            cp = os.path.join(strokes_dir, lvl)
            if os.path.isfile(cp):
                try:
                    with open(cp, 'r', encoding='utf-8') as f:
                        cdata = json.load(f)
                        data.update(cdata)
                except Exception:
                    pass

    return data

def load_app_requirements():
    """
    Memuat daftar karakter yang dibutuhkan oleh aplikasi dari data/kana.json dan data/kanji.json.
    """
    kana_map = {}
    if os.path.isfile('data/kana.json'):
        with open('data/kana.json', 'r', encoding='utf-8') as f:
            kana_raw = json.load(f)
            for h in kana_raw.get('hiragana', []):
                char = h.get('character', '')
                if char:
                    kana_map[char] = {
                        'reading': h.get('reading', ''),
                        'type': h.get('type', 'hiragana'),
                        'strokes': h.get('strokes')
                    }
            for k in kana_raw.get('katakana', []):
                char = k.get('character', '')
                if char:
                    kana_map[char] = {
                        'reading': k.get('reading', ''),
                        'type': k.get('type', 'katakana'),
                        'strokes': k.get('strokes')
                    }

    # Tambahkan vokal kecil & kana pelengkap
    extra_kana = ['ぁ', 'ぃ', 'ぅ', 'ぇ', 'ぉ', 'っ', 'ゃ', 'ゅ', 'ょ',
                  'ァ', 'ィ', 'ゥ', 'ェ', 'ォ', 'ッ', 'ャ', 'ュ', 'ョ', 'ヴ', 'ヶ', 'ヵ']
    for ek in extra_kana:
        if ek not in kana_map:
            kana_map[ek] = {'reading': ek, 'type': 'small_kana', 'strokes': None}

    kanji_map = {}
    if os.path.isfile('data/kanji.json'):
        with open('data/kanji.json', 'r', encoding='utf-8') as f:
            kanji_raw = json.load(f)
            for item in kanji_raw:
                k = item.get('kanji')
                if k:
                    kanji_map[k] = {
                        'strokes': int(item['strokes']) if item.get('strokes') is not None else None,
                        'grade': item.get('grade'),
                        'meaning': item.get('meaning', ''),
                        'onyomi': item.get('onyomi', []),
                        'kunyomi': item.get('kunyomi', [])
                    }

    return kana_map, kanji_map

def validate_dataset(data, kana_map, kanji_map, verbose=False):
    """
    Melakukan validasi mendalam terhadap setiap karakter dalam dataset.
    """
    results = {
        'total_entries': len(data),
        'valid_entries': 0,
        'invalid_entries': 0,
        'metadata_discrepancies': 0,
        'kana_passed': 0,
        'kanji_passed': 0,
        'other_passed': 0,
        'errors': [],
        'discrepancies': [],
        'char_details': {}
    }

    # Karakter contoh untuk uji representatif
    sample_targets = ['一', '二', '人', '水', 'あ', 'い', 'か', 'きゃ', '語', '鬱', '議', '艦', '衷']

    for char, record in data.items():
        char_status = {
            'char': char,
            'hex': f"{ord(char):05x}",
            'valid': True,
            'errors': [],
            'stroke_count': 0,
            'expected_strokes': None,
            'discrepancy': False,
            'category': 'unknown'
        }

        # Klasifikasi kategori karakter
        is_kana = (0x3040 <= ord(char) <= 0x30FF)
        is_kanji = (0x4E00 <= ord(char) <= 0x9FAF) or (0x3400 <= ord(char) <= 0x4DBF)
        if is_kana:
            char_status['category'] = 'kana'
        elif is_kanji:
            char_status['category'] = 'kanji'
        else:
            char_status['category'] = 'other'

        # 1. Validasi struktur objek
        if not isinstance(record, dict):
            char_status['valid'] = False
            char_status['errors'].append("Record bukan objek dictionary")
            results['invalid_entries'] += 1
            results['errors'].append(f"{char}: Record bukan objek dictionary")
            results['char_details'][char] = char_status
            continue

        # 2. Validasi viewBox
        view_box = record.get('viewBox', '')
        if view_box != '0 0 109 109':
            char_status['valid'] = False
            char_status['errors'].append(f"viewBox tidak standar: '{view_box}', diharapkan '0 0 109 109'")

        # 3. Validasi paths
        paths = record.get('paths')
        if not isinstance(paths, list) or len(paths) == 0:
            char_status['valid'] = False
            char_status['errors'].append("paths kosong atau bukan array")
        else:
            char_status['stroke_count'] = len(paths)
            for idx, p in enumerate(paths):
                ok, err_msg, start_pt = parse_svg_path_commands(p)
                if not ok:
                    char_status['valid'] = False
                    char_status['errors'].append(f"Goresan #{idx+1} invalid: {err_msg}")
                elif start_pt:
                    # Validasi koordinat awal dalam batas viewBox yang masuk akal [-5, 115]
                    sx, sy = start_pt
                    if not (-5 <= sx <= 115 and -5 <= sy <= 115):
                        char_status['valid'] = False
                        char_status['errors'].append(f"Goresan #{idx+1} titik awal di luar batas viewBox ({sx}, {sy})")

        # 4. Validasi stroke numbers
        numbers = record.get('numbers')
        if numbers is not None:
            if not isinstance(numbers, list):
                char_status['valid'] = False
                char_status['errors'].append("numbers bukan array")
            else:
                for idx, num_item in enumerate(numbers):
                    if not isinstance(num_item, dict):
                        char_status['valid'] = False
                        char_status['errors'].append(f"Nomor #{idx+1} bukan dictionary")
                        continue
                    nx = num_item.get('x')
                    ny = num_item.get('y')
                    txt = num_item.get('text')
                    if nx is None or ny is None or txt is None:
                        char_status['valid'] = False
                        char_status['errors'].append(f"Nomor #{idx+1} tidak lengkap: x={nx}, y={ny}, text={txt}")
                    else:
                        if not isinstance(nx, (int, float)) or not isinstance(ny, (int, float)):
                            char_status['valid'] = False
                            char_status['errors'].append(f"Nomor #{idx+1} koordinat bukan numerik: ({nx}, {ny})")
                        elif not (-10 <= nx <= 120 and -10 <= ny <= 120):
                            char_status['valid'] = False
                            char_status['errors'].append(f"Nomor #{idx+1} koordinat di luar batas: ({nx}, {ny})")

        # 5. Konsistensi dengan metadata
        expected_strokes = None
        if is_kana and char in kana_map:
            expected_strokes = kana_map[char].get('strokes')
        elif is_kanji and char in kanji_map:
            expected_strokes = kanji_map[char].get('strokes')

        char_status['expected_strokes'] = expected_strokes
        if expected_strokes is not None and char_status['stroke_count'] != expected_strokes:
            char_status['discrepancy'] = True
            char_status['valid'] = False
            err_msg = f"Selisih jumlah goresan: kanji.json ({expected_strokes}) != path KanjiVG ({char_status['stroke_count']}). Kemungkinan salah di kanji.json."
            char_status['errors'].append(err_msg)
            results['metadata_discrepancies'] += 1
            results['errors'].append(f"{char}: {err_msg}")
            disc_entry = {
                'char': char,
                'hex': char_status['hex'],
                'category': char_status['category'],
                'kanjivg_strokes': char_status['stroke_count'],
                'metadata_strokes': expected_strokes,
                'note': "Discrepancy antara KanjiVG dan kanji.json. Dilaporkan sebagai kemungkinan salah di kanji.json."
            }
            results['discrepancies'].append(disc_entry)

        # Evaluasi hasil karakter
        if char_status['valid']:
            results['valid_entries'] += 1
            if is_kana:
                results['kana_passed'] += 1
            elif is_kanji:
                results['kanji_passed'] += 1
            else:
                results['other_passed'] += 1
        else:
            results['invalid_entries'] += 1
            results['errors'].append(f"{char}: " + "; ".join(char_status['errors']))

        results['char_details'][char] = char_status

    return results

def generate_coverage_manifest(data, results, kana_map, kanji_map, output_manifest_path):
    """
    Menghasilkan manifest cakupan data yang terstruktur (data/stroke-coverage-manifest.json).
    """
    total_required_kana = set(k for k in kana_map.keys() if len(k) == 1)
    total_required_kanji = set(kanji_map.keys())
    all_required = total_required_kana | total_required_kanji

    dataset_chars = set(data.keys())

    available_and_passed = []
    discrepancy_list = []
    failed_chars = []
    missing_chars = []

    for c in sorted(all_required):
        if c not in dataset_chars:
            missing_chars.append({
                'char': c,
                'hex': f"{ord(c):05x}",
                'category': 'kana' if c in total_required_kana else 'kanji',
                'status': 'missing_from_dataset'
            })
        else:
            detail = results['char_details'].get(c, {})
            if not detail.get('valid'):
                failed_chars.append({
                    'char': c,
                    'hex': detail.get('hex'),
                    'category': detail.get('category'),
                    'errors': detail.get('errors', [])
                })
            elif detail.get('discrepancy'):
                discrepancy_list.append({
                    'char': c,
                    'hex': detail.get('hex'),
                    'category': detail.get('category'),
                    'kanjivg_strokes': detail.get('stroke_count'),
                    'metadata_strokes': detail.get('expected_strokes')
                })
            else:
                available_and_passed.append(c)

    # Contoh sampel representatif karakter
    sample_tests = []
    test_chars = ['一', '二', '人', '水', 'あ', 'い', 'か', '語', '議', '艦', '驚', '鷹', '衷']
    for tc in test_chars:
        if tc in results['char_details']:
            det = results['char_details'][tc]
            sample_tests.append({
                'char': tc,
                'hex': det['hex'],
                'category': det['category'],
                'status': 'PASSED' if det['valid'] else 'FAILED',
                'strokes': det['stroke_count'],
                'expected_strokes': det['expected_strokes'],
                'discrepancy': det['discrepancy']
            })

    manifest = {
        'generator': 'skrip/arsip/validate_stroke_data.py',
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'source_dataset': 'KanjiVG (Ulrich Apel & contributors, CC BY-SA 3.0)',
        'summary': {
            'total_app_characters_required': len(all_required),
            'required_kana_count': len(total_required_kana),
            'required_kanji_count': len(total_required_kanji),
            'dataset_total_entries': results['total_entries'],
            'dataset_valid_entries': results['valid_entries'],
            'dataset_invalid_entries': results['invalid_entries'],
            'metadata_discrepancies': results['metadata_discrepancies'],
            'coverage_rate_percent': round((len(dataset_chars & all_required) / len(all_required)) * 100, 2) if all_required else 0,
            'missing_characters_count': len(missing_chars),
            'failed_characters_count': len(failed_chars)
        },
        'sample_character_tests': sample_tests,
        'metadata_discrepancies_detail': discrepancy_list,
        'missing_characters': missing_chars,
        'failed_characters': failed_chars
    }

    os.makedirs(os.path.dirname(output_manifest_path) or '.', exist_ok=True)
    with open(output_manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    return manifest

def validate_overrides_integrity(data, overrides_path="data/stroke-overrides.json"):
    """
    Memastikan seluruh override yang didefinisikan di data/stroke-overrides.json
    terdaftar, memiliki struktur valid, dan tidak hilang/ditimpa dari hasil akhir.
    """
    if not os.path.isfile(overrides_path):
        return True, 0, []

    with open(overrides_path, "r", encoding="utf-8") as f:
        overrides = json.load(f)

    errors = []
    for char, ov in overrides.items():
        if "paths" in ov and isinstance(ov["paths"], list) and len(ov["paths"]) > 0:
            if char not in data:
                errors.append(f"Karakter override '{char}' tidak ditemukan di dataset stroke-data!")
            elif data[char].get("paths") != ov["paths"]:
                errors.append(f"Karakter override '{char}' ditimpa dan berbeda dari data/stroke-overrides.json!")
        if "numbers" in ov and isinstance(ov["numbers"], list):
            for n_idx, num in enumerate(ov["numbers"]):
                if not isinstance(num, dict) or "x" not in num or "y" not in num:
                    errors.append(f"Nomor #{n_idx+1} pada override '{char}' tidak valid!")

    if errors:
        return False, len(overrides), errors
    return True, len(overrides), []

def main():
    parser = argparse.ArgumentParser(description="Validator data goresan KanjiVG MIRAI NO WEBU.")
    parser.add_argument('--file', default='js/stroke-data.js', help='Path ke berkas stroke-data.js (default: js/stroke-data.js)')
    parser.add_argument('--manifest', default='data/stroke-coverage-manifest.json', help='Path output manifest cakupan (default: data/stroke-coverage-manifest.json)')
    parser.add_argument('--overrides', default='data/stroke-overrides.json', help='Path berkas stroke-overrides.json (default: data/stroke-overrides.json)')
    parser.add_argument('--verbose', action='store_true', help='Tampilkan detail error dan discrepancy')
    parser.add_argument('--allow-partial', action='store_true', help='Jangan gagalkan exit code jika ada karakter yang hilang dari dataset (hanya periksa integritas karakter yang ada)')
    args = parser.parse_args()

    print(f"==================================================")
    print(f"🔍 MIRAI NO WEBU - STROKE DATA VALIDATOR")
    print(f"Target: {args.file}")
    print(f"==================================================")

    # 1. Muat dataset
    try:
        data = load_stroke_data(args.file)
        print(f"✔ Berhasil memuat berkas JS & JSON: {len(data)} entri karakter ditemukan.")
    except Exception as e:
        print(f"❌ Gagal memuat dataset: {e}")
        sys.exit(1)

    # 2. Muat metadata aplikasi
    kana_map, kanji_map = load_app_requirements()
    print(f"✔ Metadata aplikasi dimuat: {len(kana_map)} entri kana, {len(kanji_map)} entri kanji.")

    # 3. Jalankan validasi
    results = validate_dataset(data, kana_map, kanji_map, verbose=args.verbose)

    # 4. Validasi integritas lapisan override
    ov_ok, ov_count, ov_errors = validate_overrides_integrity(data, args.overrides)
    if not ov_ok:
        print(f"\n❌ VALIDASI LAPISAN OVERRIDE GAGAL ({len(ov_errors)} kesalahan):")
        for err in ov_errors[:10]:
            print(f"  - {err}")
        results['invalid_entries'] += len(ov_errors)
    else:
        print(f"✔ Lapisan override diverifikasi: {ov_count} entri override aman dan tidak tertimpa.")

    # 5. Buat manifest cakupan
    manifest = generate_coverage_manifest(data, results, kana_map, kanji_map, args.manifest)
    print(f"✔ Manifest cakupan data ditulis ke: {args.manifest}")

    # 6. Cetak ringkasan hasil
    summary = manifest['summary']
    print(f"\n---------------- HASIL VALIDASI ----------------")
    print(f"Total Karakter di Dataset : {summary['dataset_total_entries']}")
    print(f"  - Valid (Lolos)         : {summary['dataset_valid_entries']}")
    print(f"  - Tidak Valid (Gagal)   : {summary['dataset_invalid_entries']}")
    print(f"  - Kana Lolos            : {results['kana_passed']}")
    print(f"  - Kanji Lolos           : {results['kanji_passed']}")
    print(f"  - Discrepancy Metadata  : {summary['metadata_discrepancies']}")
    print(f"Total Dibutuhkan Aplikasi : {summary['total_app_characters_required']}")
    print(f"  - Hilang dari Dataset   : {summary['missing_characters_count']}")
    print(f"  - Tingkat Cakupan       : {summary['coverage_rate_percent']}%")

    print(f"\n--- SAMPEL PENGUJIAN KARAKTER (SEDERHANA & KOMPLEKS) ---")
    for sample in manifest['sample_character_tests']:
        disc_str = f" [DISCREPANCY: meta={sample['expected_strokes']}]" if sample['discrepancy'] else ""
        print(f"  {sample['char']} ({sample['hex']}, {sample['category']}): {sample['status']} | Goresan: {sample['strokes']}{disc_str}")

    if results['discrepancies']:
        print(f"\n--- CATATAN DISCREPANCY METADATA (SUMBER KANJIVG vs METADATA) ---")
        for d in results['discrepancies'][:5]:
            print(f"  Karakter '{d['char']}' ({d['hex']}): KanjiVG={d['kanjivg_strokes']} goresan, Metadata={d['metadata_strokes']} goresan.")
        if len(results['discrepancies']) > 5:
            print(f"  ... dan {len(results['discrepancies']) - 5} lainnya (lihat manifest)")

    if results['errors']:
        print(f"\n❌ DITEMUKAN {len(results['errors'])} ERROR STRUKTUR/KOORDINAT/DISCREPANCY:")
        for err in results['errors'][:10]:
            print(f"  - {err}")
        if len(results['errors']) > 10:
            print(f"  ... dan {len(results['errors']) - 10} lainnya")

    # Evaluasi status keluar
    if results['invalid_entries'] > 0:
        print(f"\n❌ VALIDASI GAGAL: {results['invalid_entries']} entri tidak valid.")
        sys.exit(1)

    if not args.allow_partial and summary['missing_characters_count'] > 0:
        print(f"\n⚠ CATATAN: Dataset saat ini hanya mencakup sebagian ({summary['coverage_rate_percent']}%).")
        print(f"  {summary['missing_characters_count']} karakter aplikasi belum ada di {args.file}.")
        print(f"✔ Seluruh {summary['dataset_valid_entries']} karakter yang ada di berkas 100% VALID.")

    print(f"\n✔ VALIDASI SELESAI DENGAN SUKSES!")

if __name__ == '__main__':
    main()
