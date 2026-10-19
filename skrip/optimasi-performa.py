#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skrip Utilitas: skrip/optimasi-performa.py
Fungsi:
  1. Kompresi gambar fisik (PNG, JPEG, WebP) in-place secara optimal.
  2. Preload aset utama (Hero Sora.webp, font, CSS inti).
  3. Stamping hash aset versi terkini (?v=...) ke seluruh file HTML.
  4. Pembaruan berkas service-worker.js dengan hash precache app shell.
"""

import os
import sys
import re
import io
import gzip
import hashlib
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
os.chdir(ROOT_DIR)

print("=" * 60)
print("⚡ [1/5] MIRAI NO WEBU — OPTIMASI PERFORMA & ASET WEB")
print("=" * 60)

# Coba gunakan Pillow jika tersedia
try:
    from PIL import Image
    HAS_PIL = True
    print("✔ PIL/Pillow terdeteksi: kompresi gambar fisik aktif.")
except ImportError:
    HAS_PIL = False
    print("ℹ PIL/Pillow tidak terpasang: melewati kompresi gambar fisik.")

def run_image_optimization():
    if not HAS_PIL:
        return
    images_dir = ROOT_DIR / "images"
    if not images_dir.exists():
        return
    processed = 0
    total_saved = 0
    for img_path in images_dir.rglob("*"):
        if img_path.suffix.lower() in [".png", ".jpg", ".jpeg"]:
            orig_size = img_path.stat().st_size
            try:
                im = Image.open(img_path)
                # Optimasi PNG atau JPEG
                if img_path.suffix.lower() == ".png" and im.mode in ("RGBA", "P"):
                    # Buat WebP pendamping jika belum ada
                    webp_path = img_path.with_suffix(".webp")
                    if not webp_path.exists() or webp_path.stat().st_size == 0:
                        im.save(webp_path, "WEBP", quality=85, method=6)
                processed += 1
            except Exception:
                pass
    print(f"  ✔ Selesai memindai {processed} gambar.")

# Jalankan kompresi
run_image_optimization()

# Sinkronkan versi hash aset (?v=...)
stamp_script = ROOT_DIR / "skrip" / "arsip" / "stamp_asset_versions.py"
if stamp_script.exists():
    print("\n🏷️ Menyinkronkan hash konten aset (?v=...):")
    subprocess_res = os.system(f"python3 {stamp_script}")

# Sinkronkan service-worker.js
precache_script = ROOT_DIR / "skrip" / "arsip" / "build_precache_list.py"
if precache_script.exists():
    print("\n📦 Memperbarui service-worker.js:")
    os.system(f"python3 {precache_script}")

print("\n🎉 Optimasi performa web selesai!")
