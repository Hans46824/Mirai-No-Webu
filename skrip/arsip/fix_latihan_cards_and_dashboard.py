#!/usr/bin/env python3
"""
File: skrip/arsip/fix_latihan_cards_and_dashboard.py
Fungsi:
 1. Mengembalikan kartu latihan kana dan latihan gabungan di kelas/latihan.html dengan memperbaiki Temporal Dead Zone (TDZ) pada bootKanaApp() dan mengembalikan variabel allLevelIds di js/script.js.
 2. Menghapus dashboard progress (.user-stats-bar) di hero kelas/latihan.html sesuai instruksi pengguna.
 3. Memastikan js/progress.js tidak membatalkan atribut hidden pada span statistik.
 4. Memperbarui skrip/arsip/test_progress_engine.py agar sesuai dengan status terhapusnya dashboard progress.
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]

def fix_script_js():
    path = ROOT / "js" / "script.js"
    content = path.read_text(encoding="utf-8")

    # 1. Hapus pemanggilan bootKanaApp awal sebelum deklarasi rows/voiced/combos (cegah TDZ)
    early_boot_pattern = re.compile(
        r'if \(document\.readyState === "loading"\) \{\s*document\.addEventListener\("DOMContentLoaded", bootKanaApp\);\s*\} else \{\s*bootKanaApp\(\);\s*\}',
        re.MULTILINE
    )
    if early_boot_pattern.search(content):
        content = early_boot_pattern.sub("// Boot Kana Quest dipanggil di akhir berkas setelah seluruh konstanta selesai dimuat", content)
        print("✓ Early boot check di js/script.js dipindahkan ke akhir berkas (TDZ fixed).")

    # 2. Kembalikan allLevelIds di initKanaQuest
    target_needle = "const totalLevels = rows.length + voiced.length + combos.length;\n"
    if "const allLevelIds = Array.from({ length: totalLevels }" not in content:
        content = content.replace(
            target_needle,
            target_needle + "const allLevelIds = Array.from({ length: totalLevels }, (_, index) => index + 1);\n"
        )
        print("✓ allLevelIds berhasil dikembalikan di initKanaQuest().")

    # 3. Pastikan bootKanaApp dipanggil di akhir berkas js/script.js
    bottom_boot_code = """
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", bootKanaApp);
} else {
  bootKanaApp();
}
"""
    if "bootKanaApp();" not in content[-300:]:
        content = content.rstrip() + "\n" + bottom_boot_code
        print("✓ bootKanaApp() listener terpasang di akhir berkas js/script.js.")

    path.write_text(content, encoding="utf-8")

def fix_latihan_html():
    path = ROOT / "kelas" / "latihan.html"
    content = path.read_text(encoding="utf-8")

    # Hapus .user-stats-bar dari quest-hero
    hero_pattern = re.compile(
        r'<section class="quest-hero"><div><p class="page-hero-eyebrow"><span class="jp-kanji"[^>]*>仮名練習</span></p><h1>Latihan<br><span>Kana</span></h1>\s*<div class="user-stats-bar">.*?</div>\s*<span data-level-xp hidden>0</span><span data-xp-bar hidden></span></div>',
        re.DOTALL
    )
    clean_hero = '<section class="quest-hero"><span data-review-count hidden>0</span><span data-streak hidden>1</span><span data-user-level hidden>1</span><span data-total-xp hidden>0</span><span data-level-xp hidden>0</span><span data-xp-bar hidden></span><div><p class="page-hero-eyebrow"><span class="jp-kanji" lang="ja">仮名練習</span></p><h1>Latihan<br><span>Kana</span></h1></div>'
    
    if hero_pattern.search(content):
        content = hero_pattern.sub(clean_hero, content)
        print("✓ .user-stats-bar berhasil dihapus dari hero kelas/latihan.html.")
    else:
        # Fallback jika pola sedikit berbeda
        stats_bar_pattern = re.compile(r'<div class="user-stats-bar">.*?</div>\s*', re.DOTALL)
        if stats_bar_pattern.search(content):
            content = stats_bar_pattern.sub("", content)
            print("✓ .user-stats-bar berhasil dihapus dari kelas/latihan.html (fallback).")

    path.write_text(content, encoding="utf-8")

def fix_progress_js():
    path = ROOT / "js" / "progress.js"
    content = path.read_text(encoding="utf-8")

    # Hapus el.removeAttribute("hidden") pada [data-streak], [data-user-level], dll.
    content = re.sub(r'(\s*)el\.removeAttribute\("hidden"\);', r'', content)
    print("✓ el.removeAttribute('hidden') dinonaktifkan di js/progress.js agar elemen tersembunyi tetap tersembunyi.")
    path.write_text(content, encoding="utf-8")

def update_test_progress_engine():
    path = ROOT / "skrip" / "arsip" / "test_progress_engine.py"
    content = path.read_text(encoding="utf-8")

    # Ubah assertion di test_progress_engine.py agar memverifikasi penghapusan user-stats-bar
    old_test_block = """        # data-streak dan data-user-level TIDAK boleh hidden
        if '<span data-streak hidden>' in latihan_str:
            errors.append("data-streak masih memiliki atribut hidden di kelas/latihan.html!")
        else:
            checks_passed += 1

        if '<span data-user-level hidden>' in latihan_str:
            errors.append("data-user-level masih memiliki atribut hidden di kelas/latihan.html!")
        else:
            checks_passed += 1

        if 'user-stats-bar' not in latihan_str:
            errors.append("user-stats-bar tidak ditemukan di kelas/latihan.html!")
        else:
            checks_passed += 1"""

    new_test_block = """        # Dashboard progress (user-stats-bar) harus sudah bersih dihapus dari kelas/latihan.html
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
            checks_passed += 1"""

    if old_test_block in content:
        content = content.replace(old_test_block, new_test_block)
        print("✓ Assertions di skrip/arsip/test_progress_engine.py berhasil diperbarui.")
        path.write_text(content, encoding="utf-8")

if __name__ == "__main__":
    print("=== MEMPERBAIKI KARTU LATIHAN & MENGHAPUS DASHBOARD PROGRESS ===")
    fix_script_js()
    fix_latihan_html()
    fix_progress_js()
    update_test_progress_engine()
    print("=== SELESAI ===")

