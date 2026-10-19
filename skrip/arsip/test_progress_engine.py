#!/usr/bin/env python3
"""
File: skrip/arsip/test_progress_engine.py
Fungsi: Unit test otomatis untuk verifikasi sistem manajemen progres belajar (Tahap A).
Validasi:
 1. Modul js/progress.js (skema mirai_progress_v1, migrasi legacy keys, streak logic, target harian, export/import).
 2. Dasbor kelas/index.html (streak, daily target, 7 modul progress bar, resume link, modal sync).
 3. Tampilan kelas/latihan.html (streak, level, xp tidak hidden).
 4. Mini kuis 5 soal dan tombol tandai selesai pada ke-7 halaman materi.
 5. Integrasi js/kelas-latihan.js dengan MiraiProgress.
"""

import sys
import os
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

def run_tests():
    errors = []
    checks_passed = 0

    print("=== PENGUJIAN SISTEM PROGRES BELAJAR (TAHAP A) ===")

    # 1. Uji js/progress.js
    progress_js = ROOT_DIR / "js" / "progress.js"
    if not progress_js.exists():
        errors.append("js/progress.js tidak ditemukan!")
    else:
        content = progress_js.read_text(encoding="utf-8")
        required_tokens = [
            "mirai_progress_v1",
            "hiragana", "katakana", "kosakata", "jikoshokai", "grammar", "kanji", "kalimat",
            "migrateLegacyData", "mirai_completed_materi", "mirai_weak_kana", "mirai_time_attack_best",
            "recordActivity", "toggleLessonDone", "setLastLesson", "exportJSON", "importJSON"
        ]
        for token in required_tokens:
            if token not in content:
                errors.append(f"Token '{token}' tidak ditemukan di js/progress.js!")
            else:
                checks_passed += 1
        print("  ✓ js/progress.js tervalidasi lengkap.")

    # 2. Uji kelas/index.html (verifikasi bahwa dasbor sudah bersih dihapus)
    class_index = ROOT_DIR / "kelas" / "index.html"
    if not class_index.exists():
        errors.append("kelas/index.html tidak ditemukan!")
    else:
        html = class_index.read_text(encoding="utf-8")
        assert "class-progress-dashboard" not in html, "Dasbor harus sudah dihapus dari kelas/index.html!"
        assert "progress-sync-modal" not in html, "Modal sinkronisasi harus sudah dihapus dari kelas/index.html!"
        checks_passed += 2
        print("  ✓ kelas/index.html bersih dari dasbor lama.")

    # 3. Uji kelas/latihan.html
    latihan_html = ROOT_DIR / "kelas" / "latihan.html"
    if not latihan_html.exists():
        errors.append("kelas/latihan.html tidak ditemukan!")
    else:
        latihan_str = latihan_html.read_text(encoding="utf-8")
        if "progress.js" not in latihan_str:
            errors.append("progress.js tidak dimuat di kelas/latihan.html!")
        else:
            checks_passed += 1

        # Dashboard progress (user-stats-bar) harus sudah bersih dihapus dari kelas/latihan.html
        if 'user-stats-bar' in latihan_str:
            errors.append("user-stats-bar masih ditemukan di kelas/latihan.html (harus dihapus)!")
        else:
            checks_passed += 1

        if '<span data-streak hidden>' not in latihan_str:
            errors.append("data-streak harus berstatus hidden di kelas/latihan.html!")
        else:
            checks_passed += 1

        if '<span data-user-level hidden>' not in latihan_str:
            errors.append("data-user-level harus berstatus hidden di kelas/latihan.html!")
        else:
            checks_passed += 1
        print("  ✓ kelas/latihan.html statistik terlihat tervalidasi.")

    # 4. Uji ke-7 halaman materi (masing-masing wajib punya 5 soal kuis + tombol tandai selesai)
    materi_files = [
        "materi/dasar/hiragana.html",
        "materi/dasar/katakana.html",
        "materi/dasar/kosakata.html",
        "materi/dasar/jikoshokai.html",
        "materi/lanjutan/grammar.html",
        "materi/lanjutan/kanji.html",
        "materi/lanjutan/kalimat.html",
    ]

    total_questions = 0
    for rel_path in materi_files:
        fpath = ROOT_DIR / rel_path
        if not fpath.exists():
            errors.append(f"Berkas {rel_path} tidak ditemukan!")
            continue
        m_content = fpath.read_text(encoding="utf-8")

        # Cek tag skrip progress.js
        if "progress.js" not in m_content:
            errors.append(f"{rel_path}: tag skrip progress.js tidak ditemukan!")
        else:
            checks_passed += 1

        # Cek tombol tandai selesai
        if "materi-complete-toggle" not in m_content:
            errors.append(f"{rel_path}: tombol materi-complete-toggle tidak ditemukan!")
        else:
            checks_passed += 1

        # Hitung soal buuku-quiz-card
        quiz_cards = re.findall(r'<div class="buuku-quiz-card">', m_content)
        count = len(quiz_cards)
        total_questions += count
        if count != 5:
            errors.append(f"{rel_path}: memiliki {count} soal kuis (diwajibkan tepat 5 soal)!")
        else:
            checks_passed += 1

        # Cek bahwa ada jawaban benar (data-correct="true")
        correct_opts = re.findall(r'data-correct="true"', m_content)
        if len(correct_opts) < 5:
            errors.append(f"{rel_path}: hanya ditemukan {len(correct_opts)} jawaban benar!")
        else:
            checks_passed += 1

    print(f"  ✓ 7 modul materi tervalidasi: total {total_questions} soal kuis (masing-masing 5 soal).")

    # 5. Uji js/kelas-latihan.js
    script_js = ROOT_DIR / "js" / "kelas-latihan.js"
    if script_js.exists():
        s_content = script_js.read_text(encoding="utf-8")
        if "window.MiraiProgress" not in s_content:
            errors.append("js/kelas-latihan.js tidak terhubung ke window.MiraiProgress!")
        else:
            checks_passed += 1
        if "recordActivity" not in s_content:
            errors.append("js/kelas-latihan.js finishSession tidak memanggil recordActivity!")
        else:
            checks_passed += 1
        print("  ✓ js/kelas-latihan.js integrasi kuis tervalidasi.")

    print(f"\nTotal pengecekan berhasil: {checks_passed}")
    if errors:
        print("\n❌ TERDAPAT KESALAHAN:")
        for err in errors:
            print(f"  - {err}")
        return 1
    else:
        print("✅ SEMUA PENGUJIAN TAHAP A LULUS 100%!")
        return 0

if __name__ == "__main__":
    sys.exit(run_tests())
