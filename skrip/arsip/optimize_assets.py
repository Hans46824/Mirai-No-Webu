#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: skrip/arsip/optimize_assets.py
Deskripsi:
  1. Font non-blocking: memastikan <link rel="preconnect"> dan Google Fonts lengkap di <head> semua file HTML.
  2. Script non-blocking: menambahkan atribut defer ke tag <script src="..."> agar browser mem-parsing HTML tanpa terhenti.
  3. Image optimizations:
     - Menambahkan loading="lazy" dan decoding="async" untuk gambar di bawah layar awal (below-the-fold).
     - Menghitung dan menyematkan atribut width dan height asli pada tag <img> via PIL/SVG parser untuk mencegah Cumulative Layout Shift (CLS).
"""

import os
import re
import glob
from PIL import Image

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

FONT_LINK = '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Noto+Serif+JP:wght@600;700;800;900&family=Noto+Sans+JP:wght@500;700;800;900&display=swap" rel="stylesheet">'

def get_image_dimensions(html_file, src):
    """Mendapatkan dimensi (width, height) file gambar lokal."""
    if not src or src.startswith("data:") or src.startswith("http://") or src.startswith("https://"):
        return None, None

    # Bersihkan query params (?v=...)
    clean_src = src.split("?")[0].split("#")[0]
    html_dir = os.path.dirname(html_file)
    img_path = os.path.normpath(os.path.join(html_dir, clean_src))

    if not os.path.isfile(img_path):
        # Coba dari root BASE_DIR
        alt_path = os.path.normpath(os.path.join(BASE_DIR, clean_src.lstrip("/")))
        if os.path.isfile(alt_path):
            img_path = alt_path
        else:
            return None, None

    if clean_src.lower().endswith(".svg"):
        try:
            with open(img_path, "r", encoding="utf-8") as f:
                svg_txt = f.read()
            vb_match = re.search(r'viewBox=["\']([-\d\.]+)[\s,]+([-\d\.]+)[\s,]+([-\d\.]+)[\s,]+([-\d\.]+)["\']', svg_txt)
            if vb_match:
                w = int(round(float(vb_match.group(3))))
                h = int(round(float(vb_match.group(4))))
                return w, h
            w_match = re.search(r'width=["\']([\d\.]+)px?["\']', svg_txt)
            h_match = re.search(r'height=["\']([\d\.]+)px?["\']', svg_txt)
            if w_match and h_match:
                return int(round(float(w_match.group(1)))), int(round(float(h_match.group(1))))
        except Exception:
            pass
        return None, None

    try:
        with Image.open(img_path) as im:
            return im.size[0], im.size[1]
    except Exception:
        return None, None

def optimize_html_file(html_file):
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()

    orig_content = content

    # 1. Pastikan Google Font lengkap di <head>
    if "fonts.googleapis.com" in content:
        # Ganti variasi font link lama dengan link font lengkap
        content = re.sub(
            r'<link\s+href="https://fonts\.googleapis\.com/css2\?[^"]+"\s+rel="stylesheet">',
            FONT_LINK,
            content
        )
        # Pastikan gstatic preconnect ada crossorigin
        content = re.sub(
            r'<link\s+rel=["\']?preconnect["\']?\s+href=["\']https://fonts\.gstatic\.com["\'](?!\s*crossorigin)>',
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
            content
        )

    # 2. Tambahkan defer pada tag <script src="...">
    def defer_replacer(match):
        tag = match.group(0)
        if "defer" in tag or "async" in tag:
            return tag
        # Sisipkan defer sebelum src
        return tag.replace("<script ", "<script defer ")

    content = re.sub(r'<script\s+src="[^"]+"[^>]*>', defer_replacer, content)

    # 3. Optimasi tag <img> (loading="lazy", decoding="async", width, height)
    # Temukan semua tag <img>
    img_matches = list(re.finditer(r'<img\s+([^>]+)>', content, re.IGNORECASE))
    
    # Deteksi posisi lipatan awal (misal 2 gambar pertama di header/navbar atau brand)
    for idx, match in enumerate(img_matches):
        full_tag = match.group(0)
        attrs = match.group(1)

        src_match = re.search(r'src=["\']([^"\']+)["\']', attrs)
        if not src_match:
            continue
        src = src_match.group(1)

        is_above_fold = (idx == 0 and ("brand" in attrs or "logo" in src)) or ("nav" in attrs and idx < 2)

        new_attrs = attrs

        # Tambahkan loading="lazy" & decoding="async" jika di bawah lipatan
        if not is_above_fold:
            if "loading=" not in new_attrs:
                new_attrs += ' loading="lazy"'
            if "decoding=" not in new_attrs:
                new_attrs += ' decoding="async"'
        else:
            if "decoding=" not in new_attrs:
                new_attrs += ' decoding="async"'

        # Kecualikan foto slider independen yang mengandalkan CSS aspect-ratio dinamis
        is_slider_img = "indep-portrait" in attrs or "indep-landscape" in attrs or "independent-slider" in full_tag

        # Periksa width & height
        has_width = bool(re.search(r'\bwidth=["\']?\d+', new_attrs))
        has_height = bool(re.search(r'\bheight=["\']?\d+', new_attrs))

        if not is_slider_img and not (has_width and has_height):
            w, h = get_image_dimensions(html_file, src)
            if w and h:
                if not has_width:
                    new_attrs += f' width="{w}"'
                if not has_height:
                    new_attrs += f' height="{h}"'

        # Normalisasi spasi ekstra
        new_tag = f'<img {new_attrs.strip()}>'
        content = content.replace(full_tag, new_tag)

    if content != orig_content:
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

def main():
    print("==================================================")
    print("🚀 MIRAI NO WEBU — ASSET OPTIMIZER")
    print("==================================================")
    html_files = sorted(glob.glob(os.path.join(BASE_DIR, "**", "*.html"), recursive=True))
    modified_count = 0
    total_scanned = 0

    for hf in html_files:
        if ".git" in hf or "node_modules" in hf or "skrip/laporan" in hf:
            continue
        total_scanned += 1
        rel_path = os.path.relpath(hf, BASE_DIR)
        mod = optimize_html_file(hf)
        if mod:
            modified_count += 1
            print(f"  ✔ Dioptimalkan: {rel_path}")

    print(f"\nSelesai! {modified_count} dari {total_scanned} berkas HTML berhasil dioptimasi.")

if __name__ == "__main__":
    main()

