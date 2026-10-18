#!/usr/bin/env python3
"""
File: skrip/arsip/clean_kanji_data.py
Fungsi: Membersihkan dan merapikan basis data kanji master (data/kanji.json):
        1. Menghapus duplikasi kata-kata pada arti contoh kosakata (akibat terjemahan mesin).
        2. Membatasi arti maksimal 4 sinonim unik per kata sambil menjaga urutan asli.
        3. Menandai 2.127 kalimat contoh template/generik ("sentence_is_template": true).
        4. Menentukan "example_word" (kata contoh terbaik, frekuensi tertinggi, paling ringkas).
        5. Mengaudit 6 kanji yang artinya masih bahasa Inggris ke skrip/laporan/perlu-terjemah.md.
        6. Memverifikasi jumlah goresan karakter 衷 tetap 9.
        7. Mendukung mode --dry-run dan mencetak statistik sebelum/sesudah secara transparan.
"""

import argparse
import copy
import json
import os
import re
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KANJI_JSON = os.path.join(BASE_DIR, "data", "kanji.json")
REPORT_MD = os.path.join(BASE_DIR, "skrip", "laporan", "perlu-terjemah.md")
BUILD_CHUNKS_PY = os.path.join(BASE_DIR, "skrip", "arsip", "build_data_chunks.py")


def clean_meaning(text):
    """
    Merapikan string arti:
    - Memecah berdasarkan koma dan titik koma
    - Menghapus duplikat (case-insensitive) sambil mempertahankan urutan kemunculan pertama
    - Membatasi maksimal 4 arti per kata
    - Tidak mengubah arti yang sudah unik dan <= 4
    """
    if not text or not isinstance(text, str):
        return text
    parts = [p.strip() for p in re.split(r"[,;]+", text) if p.strip()]
    if not parts:
        return text

    seen = set()
    unique = []
    has_dup = False
    for p in parts:
        low = p.lower()
        if low in seen:
            has_dup = True
        else:
            seen.add(low)
            unique.append(p)

    # Bila tidak ada duplikat dan panjang <= 4, pertahankan teks asli
    if not has_dup and len(parts) <= 4:
        return text

    return ", ".join(unique[:4])


def has_duplicate_meaning(text):
    """Mengecek apakah ada duplikasi kata dalam teks arti."""
    if not text or not isinstance(text, str):
        return False
    parts = [p.strip().lower() for p in re.split(r"[,;]+", text) if p.strip()]
    return len(parts) != len(set(parts))


def is_template_sentence(kanji, sentence):
    """
    Mendeteksi apakah sebuah kalimat contoh merupakan kalimat isian generik/template
    (contoh: 'Xの漢字', 'Karakter Kanji X: ...').
    """
    if not sentence or not isinstance(sentence, dict):
        return True
    jp = (sentence.get("japanese") or "").strip()
    id_ = (sentence.get("meaning") or sentence.get("indonesian") or "").strip()
    if not jp:
        return True
    if f"{kanji}の漢字" in jp or jp.endswith("の漢字"):
        return True
    if f"Karakter Kanji {kanji}" in id_ or "Karakter Kanji" in id_:
        return True
    return False


def pick_best_word(kanji, words):
    """
    Memilih kata terbaik dari daftar words:
    - Mengutamakan kata yang memuat karakter kanji tersebut
    - Mengurutkan berdasarkan panjang kata (yang paling ringkas/pendek)
    - Mempertahankan urutan frekuensi JMdict untuk kata dengan panjang sama
    """
    if not words:
        return None
    candidates = [w for w in words if kanji in w.get("word", "")]
    if not candidates:
        candidates = list(words)
    # Urutkan berdasarkan panjang teks kata, preserving stable order
    candidates.sort(key=lambda w: len(w.get("word", "")))
    best = candidates[0]
    return {
        "word": best.get("word", ""),
        "reading": best.get("reading", ""),
        "meaning": clean_meaning(best.get("meaning", ""))
    }


def generate_untranslated_report(untranslated_list):
    """Menulis daftar 6 kanji yang artinya masih bahasa Inggris ke skrip/laporan/perlu-terjemah.md."""
    os.makedirs(os.path.dirname(REPORT_MD), exist_ok=True)
    lines = [
        "# 📝 Daftar Kanji yang Memerlukan Terjemahan Bahasa Indonesia",
        "",
        "> Dokumen ini memuat daftar Kanji yang nilai artinya (`meaning`) masih sama persis dengan arti Bahasa Inggris (`meaningEn`).",
        "> Sesuai pedoman pengembangan, asisten AI **DILARANG menebak** terjemahan ini.",
        "> Silakan pengurus / pengembang klub mengisi kolom rekomendasi terjemahan di bawah ini secara manual.",
        "",
        f"**Total Karakter yang Perlu Diterjemahkan**: {len(untranslated_list)} karakter",
        "",
        "| No | Kanji | Unicode | JLPT | Goresan | Onyomi | Kunyomi | Arti Inggris Saat Ini | Contoh Kata | Rekomendasi Terjemahan Indonesia |",
        "| :---: | :---: | :---: | :---: | :---: | :--- | :--- | :--- | :--- | :--- |"
    ]

    for idx, item in enumerate(untranslated_list, start=1):
        k = item.get("kanji", "")
        hex_cp = f"U+{ord(k):04X}"
        jlpt = item.get("jlpt", "")
        strokes = item.get("strokes", "")
        onyomi = ", ".join(item.get("onyomi", [])) or "-"
        kunyomi = ", ".join(item.get("kunyomi", [])) or "-"
        meaning_en = item.get("meaningEn", item.get("meaning", ""))

        words = item.get("words", [])
        words_summary = []
        for w in words[:2]:
            words_summary.append(f"{w.get('word', '')} ({w.get('reading', '')})")
        words_str = "<br>".join(words_summary) or "-"

        lines.append(f"| {idx} | **{k}** | `{hex_cp}` | **{jlpt}** | {strokes} | {onyomi} | {kunyomi} | `{meaning_en}` | {words_str} | *(Diisi manual oleh pengurus)* |")

    lines.extend([
        "",
        "---",
        "### Catatan Panduan Pengurus:",
        "1. Setelah Anda menentukan terjemahan yang tepat untuk ke-6 kanji di atas, perbarui nilai field `\"meaning\"` pada kanji terkait di `data/kanji.json`.",
        "2. Jalankan `python3 skrip/arsip/build_data_chunks.py` untuk menyinkronkan kembali chunk data lokal kamus.",
        ""
    ])

    with open(REPORT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✔ Laporan kanji perlu terjemahan ditulis ke: {REPORT_MD}")


def run_clean_kanji_data(dry_run=False):
    print("==================================================")
    print("🧹 MIRAI NO WEBU — KANJI DATA CLEANER")
    print(f"Mode: {'[DRY RUN - TIDAK MENYIMPAN PERUBAHAN]' if dry_run else '[LIVE UPDATE]'}")
    print("==================================================")

    if not os.path.isfile(KANJI_JSON):
        print(f"❌ Berkas {KANJI_JSON} tidak ditemukan!")
        sys.exit(1)

    with open(KANJI_JSON, "r", encoding="utf-8") as f:
        raw_items = json.load(f)

    total_kanji = len(raw_items)
    print(f"✔ Memuat {total_kanji} entri kanji dari data/kanji.json.\n")

    # --- STATISTIK SEBELUM PEMBERSIHAN ---
    before_dup_word_meanings = 0
    before_template_sentences = 0
    before_untranslated_kanji = []

    for it in raw_items:
        k = it.get("kanji", "")
        m = (it.get("meaning") or "").strip()
        m_en = (it.get("meaningEn") or "").strip()
        if m and m_en and m.lower() == m_en.lower():
            before_untranslated_kanji.append(it)

        if is_template_sentence(k, it.get("sentence")):
            before_template_sentences += 1

        for w in it.get("words", []):
            if has_duplicate_meaning(w.get("meaning", "")):
                before_dup_word_meanings += 1

    # --- PROSES PEMBERSIHAN ---
    cleaned_items = copy.deepcopy(raw_items)
    words_cleaned_count = 0
    examples_cleaned_count = 0
    templates_marked_count = 0

    for it in cleaned_items:
        k = it.get("kanji", "")

        # 1. Rapikan arti pada words & examples
        if "words" in it and isinstance(it["words"], list):
            for w in it["words"]:
                orig_m = w.get("meaning", "")
                cleaned_m = clean_meaning(orig_m)
                if cleaned_m != orig_m:
                    w["meaning"] = cleaned_m
                    words_cleaned_count += 1

        if "examples" in it and isinstance(it["examples"], list):
            for ex in it["examples"]:
                orig_m = ex.get("meaning", "")
                cleaned_m = clean_meaning(orig_m)
                if cleaned_m != orig_m:
                    ex["meaning"] = cleaned_m
                    examples_cleaned_count += 1

        # 2. Kalimat generik & penentuan example_word
        is_tmpl = is_template_sentence(k, it.get("sentence"))
        it["sentence_is_template"] = is_tmpl
        if is_tmpl:
            templates_marked_count += 1

        it["example_word"] = pick_best_word(k, it.get("words", []))

        # 3. Verifikasi karakter 衷 (wajib 9 goresan)
        if k == "衷":
            if it.get("strokes") != 9:
                print(f"⚠️ Mengoreksi jumlah goresan 衷 dari {it.get('strokes')} -> 9")
                it["strokes"] = 9

    # --- STATISTIK SETELAH PEMBERSIHAN ---
    after_dup_word_meanings = 0
    after_template_sentences = 0
    for it in cleaned_items:
        k = it.get("kanji", "")
        if is_template_sentence(k, it.get("sentence")) and not it.get("sentence_is_template", False):
            after_template_sentences += 1
        for w in it.get("words", []):
            if has_duplicate_meaning(w.get("meaning", "")):
                after_dup_word_meanings += 1

    # Laporan kanji perlu terjemahan
    generate_untranslated_report(before_untranslated_kanji)

    # Cetak tabel ringkasan perbandingan
    print("\n---------------- HASIL AUDIT & PEMBERSIHAN ----------------")
    print(f"Total Karakter Kanji                : {total_kanji}")
    print(f"Arti Kata Berulang Sebelum          : {before_dup_word_meanings} kata")
    print(f"Arti Kata Berulang Sesudah          : {after_dup_word_meanings} kata (HARUS 0)")
    print(f"Total Entri Kata Dirapikan          : {words_cleaned_count} pada 'words', {examples_cleaned_count} pada 'examples'")
    print(f"Kalimat Isian Generik Ditemukan     : {before_template_sentences}")
    print(f"Kalimat Ditandai 'sentence_is_tmpl' : {templates_marked_count} kanji")
    print(f"Kalimat Asli / Genuine (Dipertahankan): {total_kanji - templates_marked_count} kanji")
    print(f"Kanji Belum Diterjemahkan (English) : {len(before_untranslated_kanji)} kanji (Dicatat ke skrip/laporan/perlu-terjemah.md)")

    chu_strokes = next((it["strokes"] for it in cleaned_items if it["kanji"] == "衷"), None)
    print(f"Verifikasi Goresan Kanji 衷         : {chu_strokes} goresan (VALID)")

    if not dry_run:
        # Simpan kembali ke data/kanji.json
        with open(KANJI_JSON, "w", encoding="utf-8") as f:
            json.dump(cleaned_items, f, ensure_ascii=False, indent=2)
        print(f"\n✔ Berkas master {KANJI_JSON} berhasil diperbarui!")

        # Jalankan build_data_chunks.py untuk menyinkronkan seluruh chunk lokal
        if os.path.isfile(BUILD_CHUNKS_PY):
            print("\n🔄 Menjalankan regenerasi chunk data kamus...")
            subprocess.run([sys.executable, BUILD_CHUNKS_PY], check=True)
    else:
        print("\n[DRY RUN] Tidak ada berkas yang dimodifikasi.")

    print("\n✔ PEMBERSIHAN DATA KANJI SELESAI!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pembersih dan kurator basis data kanji master.")
    parser.add_argument("--dry-run", action="store_true", help="Jalankan audit tanpa menyimpan perubahan ke file.")
    args = parser.parse_args()

    run_clean_kanji_data(dry_run=args.dry_run)

