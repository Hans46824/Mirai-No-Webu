#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: skrip/arsip/reduce_lomba_pages.py
Deskripsi:
  Mengurangi jumlah halaman lomba di lomba/index.html dari 6 halaman (18 kegiatan)
  menjadi 3 halaman (9 kegiatan terkurasi) sementara poster resmi sedang dipersiapkan.
"""

import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def reduce_lomba_cards():
    lomba_file = os.path.join(BASE_DIR, "lomba", "index.html")
    with open(lomba_file, "r", encoding="utf-8") as f:
        content = f.read()

    orig_content = content

    # 1. Potong kartu event dari Halaman 4 sampai sebelum Empty State
    cut_pattern = r'\n\s*<!--\s*==================== HALAMAN 4 \(SEMUA\) ====================\s*-->[\s\S]*?(?=\n\s*<!-- Empty State jika filter tidak menemukan hasil -->)'
    if re.search(cut_pattern, content):
        content = re.sub(cut_pattern, "\n", content)
        print(" [OK] Kartu kegiatan 10–18 (Halaman 4–6) berhasil dihapus dari lomba/index.html.")
    else:
        print(" [WARNING] Pola cut_pattern tidak cocok secara persis, mencoba fallback...")
        start_marker = "<!-- ==================== HALAMAN 4 (SEMUA) ==================== -->"
        end_marker = "<!-- Empty State jika filter tidak menemukan hasil -->"
        if start_marker in content and end_marker in content:
            p1 = content.split(start_marker)[0]
            p2 = content.split(end_marker)[1]
            content = p1 + "\n                " + end_marker + p2
            print(" [OK] Fallback string split berhasil memangkas kartu 10–18.")

    # 2. Perbarui meta description
    content = content.replace(
        "Katalog 18 kompetisi akademik, seni, dan cosplay SMA se-Jawa Timur & Nasional.",
        "Katalog 9 agenda kompetisi akademik, seni, dan cosplay SMA se-Jawa Timur & Nasional."
    )

    if content != orig_content:
        with open(lomba_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(" [OK] Berkas lomba/index.html berhasil diperbarui menjadi 3 halaman.")
    else:
        print(" [INFO] Tidak ada perubahan pada lomba/index.html.")

def update_documentation():
    # Update README.md
    readme_path = os.path.join(BASE_DIR, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            c = f.read()
        new_c = c.replace("# Informasi 18 lomba & festival jejepangan", "# Informasi agenda lomba & festival jejepangan (3 halaman)")
        if new_c != c:
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(new_c)
            print(" [OK] README.md diperbarui.")

    # Update panduan/agent.md
    agent_path = os.path.join(BASE_DIR, "panduan", "agent.md")
    if os.path.exists(agent_path):
        with open(agent_path, "r", encoding="utf-8") as f:
            c = f.read()
        new_c = c.replace("Informasi 18 lomba & festival jejepangan", "Informasi 9 agenda lomba & festival jejepangan (3 halaman)")
        if new_c != c:
            with open(agent_path, "w", encoding="utf-8") as f:
                f.write(new_c)
            print(" [OK] panduan/agent.md diperbarui.")

    # Update panduan/tree.md
    tree_path = os.path.join(BASE_DIR, "panduan", "tree.md")
    if os.path.exists(tree_path):
        with open(tree_path, "r", encoding="utf-8") as f:
            c = f.read()
        new_c = c.replace("# Informasi 18 lomba & festival jejepangan", "# Informasi agenda lomba & festival jejepangan (3 halaman)")
        if new_c != c:
            with open(tree_path, "w", encoding="utf-8") as f:
                f.write(new_c)
            print(" [OK] panduan/tree.md diperbarui.")

    # Update panduan/CONTEKAN-TAG.md
    contekan_path = os.path.join(BASE_DIR, "panduan", "CONTEKAN-TAG.md")
    if os.path.exists(contekan_path):
        with open(contekan_path, "r", encoding="utf-8") as f:
            c = f.read()
        new_c = c.replace("Papan info 18 lomba/event jejepangan", "Papan info 9 agenda lomba/event jejepangan (3 halaman)")
        if new_c != c:
            with open(contekan_path, "w", encoding="utf-8") as f:
                f.write(new_c)
            print(" [OK] panduan/CONTEKAN-TAG.md diperbarui.")

def main():
    print("=== MIRAI NO HANA: Penyesuaian Katalog Lomba Menjadi 3 Halaman ===")
    reduce_lomba_cards()
    update_documentation()
    print("=== Selesai dengan sukses ===")

if __name__ == "__main__":
    main()

