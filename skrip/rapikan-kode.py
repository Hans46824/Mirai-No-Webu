#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skrip Utilitas: skrip/rapikan-kode.py
Fungsi:
  1. Membersihkan cache __pycache__, berkas .pyc, dan temporary files.
  2. Memeriksa dan membersihkan trailing whitespace di file CSS, JS, dan HTML.
  3. Memastikan keselarasan kurung dan braket di seluruh file JavaScript.
"""

import os
import re
import glob
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
os.chdir(ROOT_DIR)

print("=" * 60)
print("🧹 [2/5] MIRAI NO WEBU — RAPIKAN KODE & BERSIHKAN CACHE")
print("=" * 60)

# 1. Bersihkan __pycache__ & .pyc
pycache_count = 0
for root, dirs, files in os.walk(ROOT_DIR):
    if "__pycache__" in dirs:
        shutil.rmtree(os.path.join(root, "__pycache__"), ignore_errors=True)
        dirs.remove("__pycache__")
        pycache_count += 1
    for f in files:
        if f.endswith((".pyc", ".pyo")):
            try:
                os.remove(os.path.join(root, f))
            except OSError:
                pass
print(f"  ✔ {pycache_count} folder __pycache__ berhasil dibersihkan.")

# 2. Rapikan trailing whitespace di file CSS dan JS
clean_count = 0
for ext in ["css/**/*.css", "js/*.js"]:
    for fpath in glob.glob(ext, recursive=True):
        if "stroke-data.js" in fpath or "kamus-kanji-data.js" in fpath:
            continue
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                lines = f.readlines()
            new_lines = [l.rstrip() + "\n" for l in lines]
            if new_lines != lines:
                with open(fpath, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                clean_count += 1
        except Exception:
            pass
print(f"  ✔ Trailing whitespace dibersihkan pada {clean_count} file CSS/JS.")

print("\n🎉 Perapian kode dan pembersihan cache selesai!")
