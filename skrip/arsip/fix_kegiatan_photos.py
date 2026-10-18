#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: skrip/arsip/fix_kegiatan_photos.py
Deskripsi:
  1. Menghapus banner 'Ikuti Tes Kecocokan Divisi' dari kegiatan/index.html.
  2. Merapikan foto slider di kegiatan/index.html dan seluruh proker tanpa atribut width/height mentah.
  3. Mengunci aturan CSS .independent-slider img dengan height: auto !important.
  4. Mencegah optimize_assets.py menyematkan width/height mentah pada foto slider.
"""

import os
import re
import glob

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def clean_kegiatan_index():
    kegiatan_index = os.path.join(BASE_DIR, "kegiatan", "index.html")
    with open(kegiatan_index, "r", encoding="utf-8") as f:
        content = f.read()

    orig_content = content

    # 1. Hapus banner kuis divisi persis dari komentar sampai penutup div
    banner_pattern = r'\s*<!--\s*BANNER PINTASAN KUIS KECOCOKAN DIVISI\s*-->\s*<div class="divisi-quiz-banner[\s\S]*?</a>\s*</div>'
    content = re.sub(banner_pattern, "", content)

    # 2. Pastikan tag img slider tidak memiliki width dan height mentah
    def clean_slider_tag(match):
        tag = match.group(0)
        if "indep-portrait" in tag or "indep-landscape" in tag:
            tag = re.sub(r'\s+width=["\']\d+["\']', '', tag)
            tag = re.sub(r'\s+height=["\']\d+["\']', '', tag)
        return tag

    content = re.sub(r'<img\s+[^>]+>', clean_slider_tag, content)

    if content != orig_content:
        with open(kegiatan_index, "w", encoding="utf-8") as f:
            f.write(content)
        print(" [OK] kegiatan/index.html berhasil diperbarui: banner kuis dihapus & foto slider dirapikan.")
    else:
        print(" [INFO] kegiatan/index.html sudah bersih.")

def clean_all_proker_sliders():
    html_files = glob.glob(os.path.join(BASE_DIR, "kegiatan", "*.html"))
    for file_path in html_files:
        if os.path.basename(file_path) == "index.html":
            continue
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        orig_content = content

        def clean_slider_tag(match):
            tag = match.group(0)
            if "indep-portrait" in tag or "indep-landscape" in tag:
                tag = re.sub(r'\s+width=["\']\d+["\']', '', tag)
                tag = re.sub(r'\s+height=["\']\d+["\']', '', tag)
            return tag

        content = re.sub(r'<img\s+[^>]+>', clean_slider_tag, content)

        if content != orig_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f" [OK] Slider img dibersihkan di {os.path.basename(file_path)}")

def update_kegiatan_css():
    css_path = os.path.join(BASE_DIR, "css", "pages", "kegiatan-divisi.css")
    with open(css_path, "r", encoding="utf-8") as f:
        content = f.read()

    orig_content = content

    # 1. Pastikan .independent-slider img memiliki height: auto !important;
    img_rule = """.independent-slider img {
  scroll-snap-align: start;
  object-fit: cover;
  border-radius: 18px;
  flex-shrink: 0;
  border: 2px solid rgba(233, 30, 99, 0.14);
  box-shadow: 0 8px 24px rgba(72, 32, 52, 0.08);
  transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.35s ease, border-color 0.35s ease;
  user-select: none;
  -webkit-user-drag: none;
  height: auto !important;
}"""
    content = re.sub(r'\.independent-slider img\s*\{[^}]*\}', img_rule, content, count=1)

    # 2. Pastikan .indep-portrait dan .indep-landscape memiliki height: auto !important;
    ratio_rules = """.indep-portrait {
  width: 45%;
  aspect-ratio: 3 / 4;
  max-width: 210px;
  height: auto !important;
}

.indep-landscape {
  width: 85%;
  aspect-ratio: 16 / 9;
  max-width: 380px;
  height: auto !important;
}"""
    content = re.sub(
        r'\.indep-portrait\s*\{[^}]*\}\s*\.indep-landscape\s*\{[^}]*\}',
        ratio_rules,
        content,
        count=1
    )

    if content != orig_content:
        with open(css_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(" [OK] Aturan CSS .independent-slider dan aspek rasio foto diperbarui di css/pages/kegiatan-divisi.css")
    else:
        print(" [INFO] CSS kegiatan-divisi.css sudah sesuai.")

def update_optimize_assets_script():
    opt_script_path = os.path.join(BASE_DIR, "skrip", "arsip", "optimize_assets.py")
    if not os.path.exists(opt_script_path):
        return

    with open(opt_script_path, "r", encoding="utf-8") as f:
        content = f.read()

    orig_content = content

    target = "        # Periksa width & height\n        has_width = bool(re.search(r'\\bwidth=[\"\\']?\\d+', new_attrs))\n        has_height = bool(re.search(r'\\bheight=[\"\\']?\\d+', new_attrs))\n\n        if not (has_width and has_height):"
    
    replacement = """        # Kecualikan foto slider independen yang mengandalkan CSS aspect-ratio dinamis
        is_slider_img = "indep-portrait" in attrs or "indep-landscape" in attrs or "independent-slider" in full_tag

        # Periksa width & height
        has_width = bool(re.search(r'\\bwidth=[\"\\']?\\d+', new_attrs))
        has_height = bool(re.search(r'\\bheight=[\"\\']?\\d+', new_attrs))

        if not is_slider_img and not (has_width and has_height):"""

    if target in content:
        content = content.replace(target, replacement)
        with open(opt_script_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(" [OK] Pengecualian slider img ditambahkan ke skrip/arsip/optimize_assets.py")

def main():
    print("=== MIRAI NO HANA: Pemulihan Kumpulan Foto & Penghapusan Banner Kuis Divisi ===")
    clean_kegiatan_index()
    clean_all_proker_sliders()
    update_kegiatan_css()
    update_optimize_assets_script()
    print("=== Selesai dengan sukses ===")

if __name__ == "__main__":
    main()

