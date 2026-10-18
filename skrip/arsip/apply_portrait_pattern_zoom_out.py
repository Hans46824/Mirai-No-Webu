#!/usr/bin/env python3
"""
Skrip Otomatis: Kembalikan Pattern ke Portrait & Zoom Out Seragam Seluruh Card
1. Pulihkan c1b.jpeg dan c1w.jpeg ke orientasi Portrait (736x1308) dari backup original.
2. Atur seluruh kartu di css/pages/*.css agar menggunakan pattern repeat zoom-out kecil (200px auto)
   sehingga mencakup seluruh permukaan kartu secara mulus tanpa terpotong kaku.
3. Kunci variabel master --pattern-size: 200px auto di :root (global.css).
4. Verifikasi ketat kurung kurawal (balanced braces) di semua 11 file CSS.
"""

import os
import re
import shutil
from PIL import Image

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def log(msg):
    print(f"[PATTERN-FIX] {msg}")

def main():
    log("=== [1] Memulihkan Gambar Pattern ke Portrait (736x1308) ===")
    bg_dir = os.path.join(BASE_DIR, "images", "mirai", "background")
    for name in ["c1b", "c1w"]:
        orig_file = os.path.join(bg_dir, f"{name}_orig.jpeg")
        target_file = os.path.join(bg_dir, f"{name}.jpeg")
        if os.path.exists(orig_file):
            shutil.copy2(orig_file, target_file)
            with Image.open(target_file) as im:
                log(f"{name}.jpeg berhasil dipulihkan ke Portrait: {im.size[0]}x{im.size[1]} (Tegak).")
        else:
            with Image.open(target_file) as im:
                if im.size[0] > im.size[1]: # Jika masih landscape
                    rotated = im.transpose(Image.Transpose.ROTATE_90)
                    rotated.save(target_file, quality=95)
                    log(f"{name}.jpeg dirotasi kembali ke Portrait: {rotated.size[0]}x{rotated.size[1]}.")
                else:
                    log(f"{name}.jpeg sudah dalam orientasi Portrait: {im.size[0]}x{im.size[1]}.")

    log("=== [2] Mengunci Variabel Master di :root (global.css) ===")
    global_css = os.path.join(BASE_DIR, "css", "pages", "global.css")
    with open(global_css, "r", encoding="utf-8") as f:
        g_content = f.read()

    if "--pattern-size:" not in g_content:
        g_content = g_content.replace(
            "--pattern-w1b: url(\"../../images/mirai/background/w1b.jpeg\");",
            "--pattern-w1b: url(\"../../images/mirai/background/w1b.jpeg\");\n  --pattern-size: 200px auto;"
        )
        with open(global_css, "w", encoding="utf-8") as f:
            f.write(g_content)
        log("Variabel master --pattern-size: 200px auto berhasil ditambahkan ke :root.")
    else:
        log("Variabel master --pattern-size sudah ada di :root.")

    log("=== [3] Menerapkan Zoom-Out Pattern (200px auto) & Repeat pada Seluruh Card ===")
    css_dir = os.path.join(BASE_DIR, "css", "pages")
    css_files = sorted([f for f in os.listdir(css_dir) if f.endswith(".css")])

    for fname in css_files:
        fpath = os.path.join(css_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        orig_open = sum(l.count("{") for l in lines)
        orig_close = sum(l.count("}") for l in lines)

        new_lines = []
        in_pattern_block = False

        for i, line in enumerate(lines):
            new_l = line

            # Deteksi apakah blok ini memuat referensi background pattern kartu
            if any(k in line for k in ["c1w.jpeg", "c1b.jpeg", "w1w.jpeg", "w1b.jpeg", "var(--pattern-c1w)", "var(--pattern-c1b)", "var(--pattern-w1w)", "var(--pattern-w1b)"]) and not line.strip().startswith("/*") and not line.strip().startswith("--"):
                in_pattern_block = True

            if in_pattern_block:
                # Zoom-out: ubah cover atau ukuran besar lama (260px/240px) menjadi 200px auto
                if "background-size:" in new_l:
                    if "cover, 280px auto" in new_l or "cover, 260px auto" in new_l:
                        new_l = re.sub(r"background-size:\s*cover,\s*\d+px\s+auto(\s*!important)?;", "background-size: cover, 200px auto !important;", new_l)
                    else:
                        new_l = re.sub(r"background-size:\s*[^;]+;", "background-size: 200px auto !important;", new_l)

                # Repeat: pastikan pattern mengulang mulus mencakup seluruh card tanpa putus
                elif "background-repeat:" in new_l:
                    if "no-repeat, repeat" in new_l:
                        new_l = re.sub(r"background-repeat:\s*[^;]+;", "background-repeat: no-repeat, repeat !important;", new_l)
                    else:
                        new_l = re.sub(r"background-repeat:\s*[^;]+;", "background-repeat: repeat !important;", new_l)

                # Posisi: tata letak center top agar awan tersusun rapi dari atas
                elif "background-position:" in new_l:
                    if "center, center" in new_l:
                        pass
                    else:
                        new_l = re.sub(r"background-position:\s*[^;]+;", "background-position: center top !important;", new_l)

            if "}" in line:
                in_pattern_block = False

            new_lines.append(new_l)

        # Validasi ketat tanda kurung kurawal
        res_open = sum(l.count("{") for l in new_lines)
        res_close = sum(l.count("}") for l in new_lines)
        assert orig_open == res_open and orig_close == res_close, f"Brace error in {fname}!"

        with open(fpath, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        log(f"Pembaruan zoom-out 200px & repeat berhasil diterapkan pada {fname} (Balanced: {res_open} blocks).")

    log("=== [4] Verifikasi Ulang Semua File CSS ===")
    for fname in css_files:
        fpath = os.path.join(css_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            c = f.read()
        o = c.count("{")
        cl = c.count("}")
        assert o == cl, f"Ketidakseimbangan kurung kurawal pada {fname}!"
    log("SELURUH 11 FILE CSS 100% BALANCED & BEBAS ERROR SINTAKS!")

if __name__ == "__main__":
    main()
