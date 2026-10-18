#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: skrip/arsip/stamp_asset_versions.py
Fungsi: Menghitung hash konten (SHA-256 dipotong 8 karakter) untuk seluruh file .css dan .js lokal,
        lalu secara otomatis mengganti parameter ?v=<hash> pada seluruh tag <link rel="stylesheet">
        dan <script src="..."> di berkas HTML proyek.
Keuntungan:
  - Cache browser maksimal bila file tidak berubah.
  - Cache busting instan tanpa campur tangan manual ketika kode CSS/JS dimodifikasi.
  - Menggantikan parameter versi manual lama seperti ?v=20261011p.
"""

import os
import re
import glob
import hashlib

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Cache hash file untuk performa
file_hash_cache = {}

def get_file_content_hash(abs_path):
    """Menghitung 8 karakter pertama SHA-256 dari isi file."""
    if abs_path in file_hash_cache:
        return file_hash_cache[abs_path]
    if not os.path.isfile(abs_path):
        return None
    hasher = hashlib.sha256()
    with open(abs_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    h = hasher.hexdigest()[:8]
    file_hash_cache[abs_path] = h
    return h

def resolve_local_asset(html_file, asset_url):
    """Memetakan asset_url (CSS/JS) ke path absolut di filesystem lokal."""
    if not asset_url:
        return None
    # Lewati skema eksternal atau data URI
    if asset_url.startswith(("http://", "https://", "//", "data:")):
        return None

    # Bersihkan query string atau fragment yang sudah ada
    clean_url = asset_url.split("?")[0].split("#")[0]
    html_dir = os.path.dirname(html_file)

    # 1. Coba relatif terhadap lokasi file HTML
    candidate1 = os.path.normpath(os.path.join(html_dir, clean_url))
    if os.path.isfile(candidate1):
        return candidate1

    # 2. Coba relatif terhadap BASE_DIR (jika berawal dari slash atau root path)
    candidate2 = os.path.normpath(os.path.join(BASE_DIR, clean_url.lstrip("/")))
    if os.path.isfile(candidate2):
        return candidate2

    return None

def stamp_html_file(html_file):
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()

    orig_content = content

    # 1. Stamping <link rel="stylesheet" href="...">
    def link_replacer(match):
        full_tag = match.group(0)
        href_match = re.search(r'href=["\']([^"\']+)["\']', full_tag)
        if not href_match:
            return full_tag
        raw_href = href_match.group(1)
        abs_asset = resolve_local_asset(html_file, raw_href)
        if not abs_asset:
            return full_tag
        chash = get_file_content_hash(abs_asset)
        if not chash:
            return full_tag
        base_href = raw_href.split("?")[0]
        new_href = f"{base_href}?v={chash}"
        return full_tag.replace(raw_href, new_href)

    content = re.sub(r'<link\s+[^>]*rel=["\']?stylesheet["\']?[^>]*>', link_replacer, content)

    # 2. Stamping <script ... src="...">
    def script_replacer(match):
        full_tag = match.group(0)
        src_match = re.search(r'src=["\']([^"\']+)["\']', full_tag)
        if not src_match:
            return full_tag
        raw_src = src_match.group(1)
        abs_asset = resolve_local_asset(html_file, raw_src)
        if not abs_asset:
            return full_tag
        chash = get_file_content_hash(abs_asset)
        if not chash:
            return full_tag
        base_src = raw_src.split("?")[0]
        new_src = f"{base_src}?v={chash}"
        return full_tag.replace(raw_src, new_src)

    content = re.sub(r'<script\s+[^>]*src=["\'][^"\']+["\'][^>]*>', script_replacer, content)

    if content != orig_content:
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

def main():
    print("==================================================")
    print("🏷️  MIRAI NO WEBU — ASSET CONTENT HASH STAMPER")
    print("==================================================")

    # Pra-kalkulasi hash untuk inventaris asset lokal
    css_files = glob.glob(os.path.join(BASE_DIR, "css", "**", "*.css"), recursive=True)
    js_files = glob.glob(os.path.join(BASE_DIR, "js", "**", "*.js"), recursive=True)

    print(f"📦 Menghitung hash aset:")
    for path in sorted(css_files + js_files):
        rel = os.path.relpath(path, BASE_DIR)
        h = get_file_content_hash(path)
        sz = os.path.getsize(path) / 1024
        print(f"  - {rel:<35} : {h} ({sz:>6.1f} KB)")

    # Stamp ke seluruh file HTML
    html_files = sorted(glob.glob(os.path.join(BASE_DIR, "**", "*.html"), recursive=True))
    stamped_count = 0

    print("\n📝 Menerapkan version hash (?v=...) ke file HTML:")
    for hf in html_files:
        if ".git" in hf or "node_modules" in hf or "skrip/laporan" in hf:
            continue
        rel_html = os.path.relpath(hf, BASE_DIR)
        mod = stamp_html_file(hf)
        if mod:
            stamped_count += 1
            print(f"  ✔ Ter-stamp: {rel_html}")

    print(f"\n✔ Selesai! {stamped_count} berkas HTML berhasil diperbarui dengan hash aset terkini.")

if __name__ == "__main__":
    main()

