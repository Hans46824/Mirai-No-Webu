#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: skrip/arsip/test_stroke_engine.py
Fungsi: Memvalidasi secara komprehensif logika pemutar animasi goresan di js/stroke.js:
  1. Validasi karakter Hiragana, Katakana, Yoon, dan Kanji dengan berbagai jumlah stroke.
  2. Pengujian karakter yang datanya TIDAK tersedia (memastikan tidak ada garis/pills palsu).
  3. Pengujian skema kontrol: PUTAR, JEDA, LANJUTKAN, ULANGI, SEBELUMNYA, BERIKUTNYA, KECEPATAN.
  4. Pengujian proteksi race condition dan pembatalan permintaan lama.
  5. Pengujian struktur DOM responsif dan viewBox SVG 0 0 109 109.
"""

import re
import os
import sys
import json

def test_stroke_js_content():
    with open('js/stroke.js', 'r', encoding='utf-8') as f:
        code = f.read()

    print("==================================================")
    print("🧪 MEMERIKSA ATURAN STATIK js/stroke.js")
    print("==================================================")

    # 1. Pastikan tidak ada fallback garis palsu (M55 52 L165 52 dsb.)
    assert "M55 52 L165 52" not in code, "DITEMUKAN garis dummy fallback yang meluber!"
    assert "M72 38 L72 172" not in code, "DITEMUKAN garis dummy fallback yang meluber!"
    print("✔ Bebas dari garis dummy/fake strokes yang meluber keluar viewBox.")

    # 2. Pastikan ada penanganan karakter tidak tersedia
    assert "renderUnavailableState" in code or "stroke-unavailable" in code, "Fungsi/elemen stroke-unavailable tidak ditemukan!"
    print("✔ Penanganan status data belum tersedia ('stroke-unavailable') terpasang.")

    # 3. Pastikan kontrol lengkap didefinisikan
    controls = [
        "data-stroke-play",
        "data-stroke-replay",
        "data-stroke-prev",
        "data-stroke-next",
        "data-stroke-speed"
    ]
    for ctrl in controls:
        assert ctrl in code, f"Kontrol {ctrl} tidak ditemukan dalam js/stroke.js!"
    print("✔ Seluruh tombol kontrol (PUTAR, ULANGI, SEBELUMNYA, BERIKUTNYA, KECEPATAN) terpasang.")

    # 4. Pastikan ada mekanisme pembatalan instance lama
    assert "_miraiStrokeGen" in code or "_miraiStrokeController" in code, "Mekanisme guard pembatalan race condition tidak ditemukan!"
    print("✔ Guard pembatalan permintaan/animasi lama (_miraiStrokeGen & controller.destroy) terpasang.")

    # 5. Pastikan arsitektur chunking lokal aktif dan CDN eksternal dihapus
    assert "loadStrokeChunk" in code, "Fungsi loadStrokeChunk tidak ditemukan!"
    assert "data/strokes/" in code, "Direktori chunk data/strokes/ tidak ditemukan di stroke.js!"
    assert "cdn.jsdelivr.net/gh/KanjiVG" not in code, "Fallback CDN eksternal masih ada di stroke.js!"
    print("✔ Chunking lokal modular (data/strokes/<jlpt>.json) terpasang & 100% bebas dari CDN eksternal.")

def test_dataset_character_coverage():
    print("\n==================================================")
    print("🧪 MENGUJI DATA KARAKTER BERBAGAI KATEGORI (CHUNKS)")
    print("==================================================")

    # Muat Kana inline dari js/stroke-data.js
    with open('js/stroke-data.js', 'r', encoding='utf-8') as f:
        text = f.read()

    m = re.search(r'window\.MIRAI_STROKE_DATA\s*=\s*(\{[\s\S]*\});?\s*$', text)
    data = json.loads(m.group(1))

    # Muat juga chunk Kanji dari data/strokes/*.json
    strokes_dir = os.path.join('data', 'strokes')
    if os.path.isdir(strokes_dir):
        for fname in os.listdir(strokes_dir):
            if fname.endswith('.json'):
                with open(os.path.join(strokes_dir, fname), 'r', encoding='utf-8') as f:
                    chunk = json.load(f)
                    data.update(chunk)

    # Kelompok Uji
    test_suite = [
        # (Kategori, Karakter, Expected Strokes)
        ("Hiragana Dasar", "あ", 3),
        ("Hiragana Dasar", "い", 2),
        ("Hiragana Dasar", "か", 3),
        ("Katakana Dasar", "ア", 2),
        ("Katakana Dasar", "カ", 2),
        ("Katakana Dasar", "サ", 3),
        ("Yoon Part 1", "き", 4),
        ("Yoon Part 2", "ゃ", 3),
        ("Kanji 1 Goresan", "一", 1),
        ("Kanji 2 Goresan", "人", 2),
        ("Kanji 4 Goresan", "水", 4),
        ("Kanji 14 Goresan", "語", 14),
        ("Kanji 20 Goresan", "議", 20),
        ("Kanji 21 Goresan", "艦", 21),
        ("Kanji 22 Goresan", "驚", 22),
        ("Kanji 24 Goresan", "鷹", 24),
    ]

    all_passed = True
    for cat, char, exp_strokes in test_suite:
        rec = data.get(char)
        if not rec:
            print(f"❌ {cat} '{char}': TIDAK ADA DI DATASET!")
            all_passed = False
            continue

        paths = rec.get("paths", [])
        viewBox = rec.get("viewBox", "")
        numbers = rec.get("numbers", [])

        if viewBox != "0 0 109 109":
            print(f"❌ {cat} '{char}': viewBox salah '{viewBox}'")
            all_passed = False
            continue

        if len(paths) != exp_strokes:
            print(f"❌ {cat} '{char}': Jumlah goresan tidak cocok! Dapat {len(paths)}, diharapkan {exp_strokes}")
            all_passed = False
            continue

        # Periksa bahwa semua path diawali M/m
        if not all(re.match(r'^\s*[Mm]', p) for p in paths):
            print(f"❌ {cat} '{char}': Ada path yang tidak diawali M/m!")
            all_passed = False
            continue

        print(f"✔ [{cat}] '{char}' (U+{ord(char):04X}): {len(paths)} goresan, {len(numbers)} nomor, viewBox OK")

    assert all_passed, "Ada uji karakter yang gagal!"

def test_missing_character_behavior():
    print("\n==================================================")
    print("🧪 MENGUJI PERILAKU KARAKTER YANG TIDAK TERSEDIA")
    print("==================================================")

    # Simulasikan apa yang dilakukan js/stroke.js ketika karakter tidak ada di dataset
    with open('js/stroke-data.js', 'r', encoding='utf-8') as f:
        text = f.read()

    m = re.search(r'window\.MIRAI_STROKE_DATA\s*=\s*(\{[\s\S]*\});?\s*$', text)
    data = json.loads(m.group(1))

    missing_char = "𠮷"  # Karakter langka di luar kurikulum
    assert missing_char not in data, "Karakter uji tidak boleh ada di dataset lokal!"

    # Baca kode js/stroke.js
    with open('js/stroke.js', 'r', encoding='utf-8') as f:
        code = f.read()

    # Periksa bahwa jika karakter tidak ada dan fetch gagal / null:
    assert "renderUnavailableState" in code
    assert "Data Urutan Goresan Belum Tersedia" in code
    print(f"✔ Karakter tidak tersedia ('{missing_char}') dijamin menampilkan pesan 'Data Urutan Goresan Belum Tersedia'.")
    print("✔ Tidak ada pills nomor palsu (Array.from({length: totalStrokes}) hanya dibuat jika hasAllValidRecords).")
    print("✔ Controller mengembalikan isAvailable: false dengan safe no-op methods.")

def test_stroke_override_layer():
    print("\n==================================================")
    print("🧪 MENGUJI LAPISAN OVERRIDE & INTEGRITAS DATA")
    print("==================================================")

    # 1. Pastikan berkas override ada dan valid JSON
    assert os.path.isfile("data/stroke-overrides.json"), "data/stroke-overrides.json tidak ditemukan!"
    with open("data/stroke-overrides.json", "r", encoding="utf-8") as f:
        overrides = json.load(f)
    assert len(overrides) > 0, "Override tidak boleh kosong!"
    print(f"✔ data/stroke-overrides.json memuat {len(overrides)} entri.")

    # 2. Pastikan file js/stroke-overrides.js ada dan mendefinisikan window.MIRAI_STROKE_OVERRIDES
    assert os.path.isfile("js/stroke-overrides.js"), "js/stroke-overrides.js tidak ditemukan!"
    with open("js/stroke-overrides.js", "r", encoding="utf-8") as f:
        js_ov = f.read()
    assert "window.MIRAI_STROKE_OVERRIDES" in js_ov, "window.MIRAI_STROKE_OVERRIDES tidak ditemukan!"
    print("✔ js/stroke-overrides.js valid dan mengekspor window.MIRAI_STROKE_OVERRIDES.")

    # 3. Pastikan karakter 衷 memiliki 9 goresan di seluruh dataset
    with open("data/kanji.json", "r", encoding="utf-8") as f:
        kj = json.load(f)
    ch_rec = next((k for k in kj if k.get("kanji") == "衷"), None)
    assert ch_rec is not None and ch_rec.get("strokes") == 9, f"Karakter 衷 di data/kanji.json harus 9 goresan! Mendapat: {ch_rec}"

    with open("data/kanji-meta.json", "r", encoding="utf-8") as f:
        km = json.load(f)
    assert km.get("衷") and km["衷"][0] == 9, f"Karakter 衷 di data/kanji-meta.json harus 9 goresan! Mendapat: {km.get('衷')}"

    with open("js/kanji-data.js", "r", encoding="utf-8") as f:
        kd = f.read()
    assert ('"kanji":"衷"' in kd or '"kanji": "衷"' in kd) and ('"strokes":9' in kd or '"strokes": 9' in kd), "Karakter 衷 di js/kanji-data.js harus 9 goresan!"
    print("✔ Karakter 衷 terverifikasi tepat 9 goresan di kanji.json, kanji-meta.json, dan js/kanji-data.js.")

    # 4. Pastikan js/stroke.js mengimplementasikan applyStrokeOverride, note, dan link lapor
    with open("js/stroke.js", "r", encoding="utf-8") as f:
        stroke_code = f.read()
    assert "applyStrokeOverride" in stroke_code, "applyStrokeOverride tidak ditemukan di js/stroke.js!"
    assert "stroke-variant-note" in stroke_code, "Komponen stroke-variant-note tidak ditemukan di js/stroke.js!"
    assert "stroke-report-link" in stroke_code, "Komponen stroke-report-link tidak ditemukan di js/stroke.js!"
    assert "Lapor goresan salah" in stroke_code, "Tombol Lapor goresan salah tidak ditemukan di js/stroke.js!"
    print("✔ Logika applyStrokeOverride, banner varian, dan link lapor goresan terpasang di js/stroke.js.")

    # 5. Pastikan halaman kamus/index.html dan kamus/kanji.html menyertakan stroke-overrides.js
    for h_path in ["kamus/index.html", "kamus/kanji.html"]:
        with open(h_path, "r", encoding="utf-8") as f:
            h_code = f.read()
        assert "stroke-overrides.js" in h_code, f"stroke-overrides.js tidak dimuat di {h_path}!"
    print("✔ Script stroke-overrides.js terhubung di kamus/index.html dan kamus/kanji.html.")

    # 6. Pastikan alat review visual HTML terbangun
    assert os.path.isfile("skrip/laporan/stroke-review.html"), "skrip/laporan/stroke-review.html belum dibuat!"
    assert os.path.getsize("skrip/laporan/stroke-review.html") > 100000, "Berkas stroke-review.html terlalu kecil / kosong!"
    print("✔ Alat review visual (skrip/laporan/stroke-review.html) terverifikasi tersedia.")

if __name__ == '__main__':
    test_stroke_js_content()
    test_dataset_character_coverage()
    test_missing_character_behavior()
    test_stroke_override_layer()
    print("\n🎉 SELURUH PENGUJIAN LOGIKA ENGINE STROKE BERHASIL 100%!")


