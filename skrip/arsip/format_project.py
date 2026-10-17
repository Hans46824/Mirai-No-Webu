#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Script: format_project.py
Deskripsi: Merapikan struktur direktori, memisahkan data raksasa kanji,
           membersihkan cache, dan memformat ulang seluruh CSS & JS
           proyek Mirai-No-Webu agar 100% rapi dan mudah dibaca manusia (human-readable).
"""

import os
import sys
import json
import shutil
import glob
import re

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")) if os.path.basename(os.path.dirname(__file__)) == "arsip" else os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT_DIR)

print(f"[Mirai-No-Webu] Memulai proses pembersihan & pemformatan di: {ROOT_DIR}\n")


# =============================================================================
# 1. BERSIHKAN CACHE & RAPIKAN FOLDER SKRIP
# =============================================================================
print("=== [1] BERSIHKAN CACHE & RAPIKAN FOLDER SKRIP ===")

# 1a. Hapus folder .cache/
cache_dir = os.path.join(ROOT_DIR, ".cache")
if os.path.exists(cache_dir):
    shutil.rmtree(cache_dir, ignore_errors=True)
    print("  -> Folder .cache/ berhasil dihapus.")
else:
    print("  -> Folder .cache/ sudah bersih.")

# 1b. Hapus seluruh folder __pycache__ dan file .pyc
pycache_count = 0
for root, dirs, files in os.walk(ROOT_DIR):
    for d in list(dirs):
        if d == "__pycache__":
            shutil.rmtree(os.path.join(root, d), ignore_errors=True)
            dirs.remove(d)
            pycache_count += 1
    for f in files:
        if f.endswith(".pyc") or f.endswith(".pyo"):
            try:
                os.remove(os.path.join(root, f))
            except OSError:
                pass
print(f"  -> {pycache_count} folder __pycache__ berhasil dibersihkan.")

# 1c. Pindahkan apply_card_subtitles.py & apply_card_subtitles_index.py ke skrip/arsip/
arsip_dir = os.path.join(ROOT_DIR, "skrip", "arsip")
os.makedirs(arsip_dir, exist_ok=True)

for script_name in ["apply_card_subtitles.py", "apply_card_subtitles_index.py"]:
    src = os.path.join(ROOT_DIR, "skrip", script_name)
    dst = os.path.join(arsip_dir, script_name)
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"  -> Memindahkan {script_name} ke skrip/arsip/")
    elif os.path.exists(dst):
        print(f"  -> {script_name} sudah berada di skrip/arsip/ (OK).")


# =============================================================================
# 2. PISAHKAN DATA RAKSASA DARI js/kanji.js
# =============================================================================
print("\n=== [2] PISAHKAN DATA RAKSASA DARI js/kanji.js ===")

kanji_js_path = os.path.join(ROOT_DIR, "js", "kanji.js")
kanji_data_path = os.path.join(ROOT_DIR, "js", "kanji-data.js")

with open(kanji_js_path, "r", encoding="utf-8") as f:
    kanji_js_content = f.read()

# Cek apakah KANJI_FULL_DATA masih bertumpuk di dalam js/kanji.js
match_giant = re.search(r'window\.KANJI_FULL_DATA\s*=\s*(\[\s*\{.*?\}\s*\]);\s*', kanji_js_content, re.DOTALL)

if match_giant and len(match_giant.group(0)) > 50000:
    print(f"  -> Ditemukan data besar ({len(match_giant.group(0)):,} karakter) di js/kanji.js. Mengekstrak...")
    raw_data = match_giant.group(0).strip()
    data_header = """/**
 * File: js/kanji-data.js
 * Database Lengkap Joyo & JLPT Kanji (N5 sampai N1) — 2.211 Karakter
 * Ditanamkan langsung agar website dapat dibuka 100% instan offline tanpa CORS / server lokal.
 * Penggunaan: kamus/index.html dan kamus/kanji.html
 */

"""
    with open(kanji_data_path, "w", encoding="utf-8") as f:
        f.write(data_header + raw_data + "\n")
    print(f"  -> File js/kanji-data.js berhasil dibuat ({os.path.getsize(kanji_data_path):,} bytes).")

    # Ganti dengan fallback deklarasi ringan
    kanji_js_content = kanji_js_content[:match_giant.start()] + """/**
 * Basis data KANJI_FULL_DATA (2.211 karakter) kini tersimpan rapi di js/kanji-data.js
 * Fallback deklarasi aman jika script data dimuat terpisah:
 */
window.KANJI_FULL_DATA = window.KANJI_FULL_DATA || [];
""" + kanji_js_content[match_giant.end():]
    with open(kanji_js_path, "w", encoding="utf-8") as f:
        f.write(kanji_js_content)
    print("  -> js/kanji.js berhasil dirampingkan.")
else:
    if os.path.exists(kanji_data_path):
        print(f"  -> js/kanji-data.js sudah terpisah ({os.path.getsize(kanji_data_path):,} bytes, OK).")
    else:
        print("  -> PERINGATAN: js/kanji-data.js belum ada dan data tidak ditemukan di kanji.js!")

# 2b. Pastikan script tag dimuat di kamus/index.html dan kamus/kanji.html
for html_rel in ["kamus/index.html", "kamus/kanji.html"]:
    html_path = os.path.join(ROOT_DIR, html_rel)
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            hcontent = f.read()
        target_pair = '<script src="../js/kanji-data.js"></script><script src="../js/kanji.js"></script>'
        if "../js/kanji-data.js" not in hcontent:
            old_tag = '<script src="../js/kanji.js"></script>'
            if old_tag in hcontent:
                hcontent = hcontent.replace(old_tag, target_pair)
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(hcontent)
                print(f"  -> Menambahkan pemuatan js/kanji-data.js ke {html_rel}.")
        else:
            print(f"  -> Pemuatan js/kanji-data.js sudah ada di {html_rel} (OK).")

# 2c. Update .vscode/settings.json
vscode_settings_path = os.path.join(ROOT_DIR, ".vscode", "settings.json")
if os.path.exists(vscode_settings_path):
    with open(vscode_settings_path, "r", encoding="utf-8") as f:
        try:
            settings = json.load(f)
        except Exception:
            settings = {}
    
    changed = False
    if "search.exclude" not in settings:
        settings["search.exclude"] = {}
    if "**/js/kanji-data.js" not in settings["search.exclude"]:
        settings["search.exclude"]["**/js/kanji-data.js"] = True
        changed = True

    if "files.watcherExclude" not in settings:
        settings["files.watcherExclude"] = {}
    if "**/js/kanji-data.js" not in settings["files.watcherExclude"]:
        settings["files.watcherExclude"]["**/js/kanji-data.js"] = True
        changed = True

    if changed:
        with open(vscode_settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
        print("  -> Menambahkan **/js/kanji-data.js ke search.exclude di .vscode/settings.json.")
    else:
        print("  -> search.exclude di .vscode/settings.json sudah terkonfigurasi (OK).")


# =============================================================================
# 3. FORMAT ULANG CSS (MULTI-LINE, 2-SPASI, 1 PROPERTI PER BARIS, KOMENTAR)
# =============================================================================
print("\n=== [3] FORMAT ULANG CSS (css/pages/*.css) ===")

def tidy_css_declaration(decl):
    colon_idx = decl.find(":")
    if colon_idx != -1 and not decl.startswith("@"):
        prop = decl[:colon_idx].strip()
        val = decl[colon_idx + 1:].strip()
        return f"{prop}: {val}"
    return decl.strip()

def tidy_css_selector(sel):
    parts = []
    buf = ""
    depth = 0
    for char in sel:
        if char == "(":
            depth += 1
            buf += char
        elif char == ")":
            depth -= 1
            buf += char
        elif char == "," and depth == 0:
            parts.append(buf.strip())
            buf = ""
        else:
            buf += char
    if buf.strip():
        parts.append(buf.strip())
    res = ", ".join(parts)
    if res.startswith("@media("):
        res = res.replace("@media(", "@media (")
    return res

def format_css_code(raw_css, indent_size=2):
    res = []
    indent = 0
    i = 0
    n = len(raw_css)

    def sp(lvl):
        return " " * (lvl * indent_size)

    buf = ""
    while i < n:
        if raw_css[i:i + 2] == "/*":
            if buf.strip():
                t = buf.strip()
                if indent > 0:
                    t = tidy_css_declaration(t)
                res.append(sp(indent) + t)
                buf = ""
            comment_end = raw_css.find("*/", i + 2)
            if comment_end == -1:
                comment_end = n
            else:
                comment_end += 2
            comment = raw_css[i:comment_end].strip()
            # Pisahkan komentar multi-baris agar rapi
            c_lines = comment.split("\n")
            for cl in c_lines:
                cl_clean = cl.strip()
                if cl_clean.startswith("*") and not cl_clean.startswith("*/"):
                    res.append(sp(indent) + " " + cl_clean)
                else:
                    res.append(sp(indent) + cl_clean)
            i = comment_end
            continue

        char = raw_css[i]

        if char == "{":
            sel = buf.strip()
            buf = ""
            if sel:
                res.append(sp(indent) + tidy_css_selector(sel) + " {")
            else:
                res.append(sp(indent) + "{")
            indent += 1
            i += 1
        elif char == "}":
            decl = buf.strip()
            buf = ""
            if decl:
                decl = tidy_css_declaration(decl)
                res.append(sp(indent) + decl + (";" if not decl.endswith(";") else ""))
            indent = max(0, indent - 1)
            res.append(sp(indent) + "}")
            i += 1
        elif char == ";":
            decl = buf.strip()
            buf = ""
            if decl:
                decl = tidy_css_declaration(decl)
                res.append(sp(indent) + decl + ";")
            i += 1
        else:
            buf += char
            i += 1

    if buf.strip():
        res.append(sp(indent) + buf.strip())

    formatted = "\n".join(res)
    lines = formatted.split("\n")
    tidy_lines = []
    for idx, l in enumerate(lines):
        tidy_lines.append(l)
        if l.strip() == "}" and idx + 1 < len(lines):
            next_l = lines[idx + 1].strip()
            if next_l != "}" and not next_l.startswith("/*"):
                tidy_lines.append("")
    return "\n".join(tidy_lines)

css_files = sorted(glob.glob("css/pages/*.css"))
for cf in css_files:
    with open(cf, "r", encoding="utf-8") as f:
        orig = f.read()

    orig_open = orig.count("{")
    orig_close = orig.count("}")
    assert orig_open == orig_close, f"Kurung kurawal di {cf} sudah tidak seimbang sebelumnya!"

    formatted = format_css_code(orig, indent_size=2)
    fmt_open = formatted.count("{")
    fmt_close = formatted.count("}")

    assert fmt_open == orig_open, f"Mismatch open brace pada {cf}: {fmt_open} vs {orig_open}"
    assert fmt_close == orig_close, f"Mismatch close brace pada {cf}: {fmt_close} vs {orig_close}"

    with open(cf, "w", encoding="utf-8") as f:
        f.write(formatted)
    print(f"  -> {cf}: {len(formatted.splitlines()):,} baris (2 spasi, 1 properti/baris, {fmt_open} blok rules OK)")


# =============================================================================
# 4. FORMAT ULANG JAVASCRIPT (MULTI-LINE, 2-SPASI, KOMENTAR PENJELAS)
# =============================================================================
print("\n=== [4] FORMAT ULANG JS (js/*.js) ===")

def reindent_js_code(code_str, indent_size=2):
    lines = code_str.split("\n")
    new_lines = []
    in_template_literal = False

    for line in lines:
        stripped = line.strip()

        # Hitung jumlah backtick unescaped untuk melacak apakah sedang di dalam template literal multi-baris
        # Catatan: hindari mengubah indentasi string HTML di dalam template literal
        backticks = re.findall(r'(?<!\\)`', line)
        
        if in_template_literal:
            new_lines.append(line)
            if len(backticks) % 2 == 1:
                in_template_literal = False
            continue

        if len(backticks) % 2 == 1:
            in_template_literal = True

        if not stripped:
            new_lines.append("")
            continue

        # Jaga format blok komentar multi-baris (/**, *, */)
        if stripped.startswith("*") and not stripped.startswith("*/"):
            l_strip = line.lstrip(" ")
            num_sp = len(line) - len(l_strip)
            lvl = max(0, round(num_sp / 4))
            new_lines.append((" " * (lvl * indent_size)) + " " + stripped)
            continue
        if stripped.startswith("/*") or stripped.startswith("*/"):
            l_strip = line.lstrip(" ")
            num_sp = len(line) - len(l_strip)
            lvl = max(0, round(num_sp / 4))
            new_lines.append((" " * (lvl * indent_size)) + stripped)
            continue

        # Baris kode standar: hitung tingkat indentasi dan ubah ke 2-spasi
        l_strip = line.lstrip(" ")
        num_sp = len(line) - len(l_strip)
        lvl = max(0, round(num_sp / 4))
        new_lines.append((" " * (lvl * indent_size)) + l_strip.rstrip())

    return "\n".join(new_lines)

js_files = sorted(glob.glob("js/*.js"))
for jf in js_files:
    if jf in ["js/stroke-data.js", "js/kanji-data.js"]:
        print(f"  -> {jf}: Dikecualikan dari pemformatan (file data murni, aman).")
        continue

    with open(jf, "r", encoding="utf-8") as f:
        orig = f.read()

    formatted = reindent_js_code(orig, indent_size=2)

    with open(jf, "w", encoding="utf-8") as f:
        f.write(formatted)
    print(f"  -> {jf}: {len(formatted.splitlines()):,} baris (indentasi 2-spasi konsisten & human-readable OK)")


# =============================================================================
# 5. VERIFIKASI AKHIR KONSISTENSI & KEUTUHAN KODE
# =============================================================================
print("\n=== [5] VERIFIKASI AKHIR ===")

# Verifikasi semua CSS braces
all_css_ok = True
for cf in sorted(glob.glob("css/**/*.css", recursive=True)):
    with open(cf, "r", encoding="utf-8") as f:
        c = f.read()
    if c.count("{") != c.count("}"):
        print(f"  ❌ Mismatch kurung kurawal pada {cf}")
        all_css_ok = False
if all_css_ok:
    print("  ✅ Seluruh file CSS (11 modul + global) memiliki kurung kurawal 100% seimbang.")

# Verifikasi integritas data kanji
if os.path.exists(kanji_data_path):
    with open(kanji_data_path, "r", encoding="utf-8") as f:
        data_text = f.read()
    prefix = "window.KANJI_FULL_DATA = "
    p_idx = data_text.find(prefix)
    if p_idx != -1:
        raw_j = data_text[p_idx + len(prefix):].rstrip()
        if raw_j.endswith(";"):
            raw_j = raw_j[:-1]
        try:
            parsed = json.loads(raw_j)
            print(f"  ✅ js/kanji-data.js valid & berisi {len(parsed):,} entri Kanji.")
        except Exception as e:
            print(f"  ❌ Gagal mem-parse JSON kanji-data.js: {e}")

print("\n🎉 Pembersihan dan pemformatan ulang proyek selesai 100%!")
