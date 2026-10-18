#!/usr/bin/env python3
"""
File: skrip/arsip/generate_pwa_icons.py
Fungsi: Menghasilkan ikon PWA standar 192x192 dan 512x512 dari logo resmi MNH1.png.
"""

from pathlib import Path
from PIL import Image

ROOT_DIR = Path(__file__).resolve().parents[2]
LOGO_PATH = ROOT_DIR / "images" / "mirai" / "logo" / "MNH1.png"
OUTPUT_DIR = ROOT_DIR / "images" / "mirai" / "logo"

def create_pwa_icon(size):
    # Buat kanvas persegi dengan warna latar Obsidian Mirai (#141018)
    bg_color = (20, 16, 24, 255)
    canvas = Image.new("RGBA", (size, size), bg_color)

    # Muat logo MNH1.png
    logo = Image.open(LOGO_PATH).convert("RGBA")

    # Hitung ukuran logo agar proporsional di dalam kanvas (padding ~18% untuk maskable icon)
    target_width = int(size * 0.76)
    aspect_ratio = logo.height / logo.width
    target_height = int(target_width * aspect_ratio)

    resized_logo = logo.resize((target_width, target_height), Image.Resampling.LANCZOS)

    # Letakkan di tengah kanvas
    x = (size - target_width) // 2
    y = (size - target_height) // 2

    canvas.paste(resized_logo, (x, y), resized_logo)

    out_file = OUTPUT_DIR / f"icon-{size}.png"
    canvas.save(out_file, "PNG", optimize=True)
    print(f"✔ Ikon PWA berhasil dibuat: {out_file} ({size}x{size})")

if __name__ == "__main__":
    create_pwa_icon(192)
    create_pwa_icon(512)

