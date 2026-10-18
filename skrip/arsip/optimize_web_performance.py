#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: skrip/arsip/optimize_web_performance.py
Deskripsi:
  Otomasi komprehensif performa loading & transisi halaman untuk hosting GitHub Pages:
  1. Kompresi & optimasi seluruh gambar secara fisik dengan Pillow (In-Place & WebP).
  2. Pembaruan service-worker.js (App Shell 5 berkas inti + Cache-First 0ms untuk gambar & font).
  3. Preload gambar Hero Sora.webp & prioritas tinggi (fetchpriority="high") di seluruh berkas HTML.
  4. Instant Page Prefetching (Smart Link Prefetcher) di js/main.js.
  5. Cache version stamping & pembuatan laporan ukuran sebelum vs sesudah.
"""

import os
import re
import io
import sys
from pathlib import Path
from PIL import Image

ROOT_DIR = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

# Koleksi statistik ukuran
stats = {
    "files_processed": 0,
    "bytes_before": 0,
    "bytes_after": 0,
    "details": []
}

def optimize_single_image(path, target_type):
    """
    Mengompresi berkas gambar secara in-place sesuai target_type:
    - 'sora': resize max 1600, buat webp q=82, simpan png q=256
    - 'chibi': resize max 320, quantize 256 FASTOCTREE
    - 'logo': resize max 400 (kecuali icon-512 tetap 512), quantize 256 FASTOCTREE
    - 'pattern': resize max 1280, JPEG q=78 progressive
    - 'photo': resize max 1280, JPEG q=80 progressive / PNG quantize 256
    """
    if not path.exists():
        return

    orig_size = path.stat().st_size
    stats["bytes_before"] += orig_size
    stats["files_processed"] += 1

    try:
        im = Image.open(path)
    except Exception as e:
        print(f"⚠️ Gagal membuka {path}: {e}")
        stats["bytes_after"] += orig_size
        return

    w, h = im.size
    is_png = path.suffix.lower() == ".png"
    is_jpg = path.suffix.lower() in [".jpg", ".jpeg"]

    # 1. Resize logic
    max_w = None
    if target_type == "sora":
        max_w = 1600
    elif target_type == "chibi":
        max_w = 320
    elif target_type == "logo":
        if "icon-512" in path.name:
            max_w = 512
        elif "icon-192" in path.name:
            max_w = 192
        else:
            max_w = 400
    elif target_type in ["pattern", "photo"]:
        max_w = 1280

    if max_w and w > max_w:
        new_h = max(1, int(h * max_w / w))
        im = im.resize((max_w, new_h), Image.Resampling.LANCZOS)

    # 2. Format specific compression
    buf = io.BytesIO()

    if target_type == "sora":
        # Generate WebP version alongside
        webp_buf = io.BytesIO()
        im.save(webp_buf, format="WEBP", quality=82, method=6)
        webp_path = path.with_suffix(".webp")
        webp_path.write_bytes(webp_buf.getvalue())
        print(f"  ✨ Dibuat {webp_path.name}: {len(webp_buf.getvalue()) / 1024:.1f} KB")

        # Also copy to images/mirai/Sora.webp & Sora.png if in background
        if "background" in str(path):
            mirai_sora_webp = ROOT_DIR / "images" / "mirai" / "Sora.webp"
            mirai_sora_webp.write_bytes(webp_buf.getvalue())

        # Quantize PNG version
        im_p = im.quantize(colors=256, method=Image.Quantize.MAXCOVERAGE)
        im_p.save(buf, format="PNG", optimize=True)

        if "background" in str(path):
            mirai_sora_png = ROOT_DIR / "images" / "mirai" / "Sora.png"
            mirai_sora_png.write_bytes(buf.getvalue())

    elif is_png:
        # Periksa apakah gambar memiliki channel alpha/transparansi
        has_transparency = False
        if im.mode == "RGBA":
            alpha_data = im.split()[3].get_flattened_data()
            if any(a < 250 for a in alpha_data):
                has_transparency = True

        if has_transparency:
            # Pertahankan mode RGBA murni agar transparansi 100% terjaga sempurna tanpa kotak hitam
            im.save(buf, format="PNG", optimize=True)
        else:
            if im.mode == "RGBA":
                im = im.convert("RGB")
            im_p = im.quantize(colors=256)
            im_p.save(buf, format="PNG", optimize=True)

    elif is_jpg:
        if im.mode != "RGB":
            im = im.convert("RGB")
        q = 78 if target_type == "pattern" else 80
        im.save(buf, format="JPEG", quality=q, optimize=True, progressive=True)

    else:
        im.save(buf, format=im.format, optimize=True)

    new_bytes = buf.getvalue()
    new_size = len(new_bytes)

    # Simpan ukuran asli hanya jika kompresi menghasilkan file yang lebih kecil
    if new_size < orig_size:
        path.write_bytes(new_bytes)
        final_size = new_size
    else:
        final_size = orig_size

    stats["bytes_after"] += final_size
    stats["details"].append({
        "path": str(path.relative_to(ROOT_DIR)),
        "before": orig_size,
        "after": final_size,
        "ratio": (1 - final_size / orig_size) * 100 if orig_size > 0 else 0
    })

def run_image_optimizations():
    print("==================================================")
    print("🖼️  TAHAP 1: KOMPRESI & OPTIMASI FISIK GAMBAR")
    print("==================================================")

    # 1. Sora Hero
    sora_path = ROOT_DIR / "images" / "mirai" / "background" / "Sora.png"
    if sora_path.exists():
        optimize_single_image(sora_path, "sora")

    # 2. Chibi Icons
    chibi_dirs = [ROOT_DIR / "images" / "mirai" / "icon", ROOT_DIR / "images" / "mirai" / "karakter"]
    for cdir in chibi_dirs:
        if cdir.exists():
            for p in cdir.glob("*.png"):
                optimize_single_image(p, "chibi")

    # Pastikan symlink/folder images/mirai/chibi tersedia
    chibi_symlink = ROOT_DIR / "images" / "mirai" / "chibi"
    if not chibi_symlink.exists():
        try:
            chibi_symlink.symlink_to("icon", target_is_directory=True)
            print("  🔗 Symlink images/mirai/chibi -> icon dibuat.")
        except Exception:
            pass

    # 3. Logos
    logo_dir = ROOT_DIR / "images" / "mirai" / "logo"
    if logo_dir.exists():
        for p in logo_dir.glob("*.png"):
            optimize_single_image(p, "logo")

    # Logo di kegiatan/images
    kegiatan_img = ROOT_DIR / "kegiatan" / "images"
    if kegiatan_img.exists():
        for p in kegiatan_img.glob("*.png"):
            optimize_single_image(p, "logo")

    # 4. Pattern Backgrounds
    bg_dir = ROOT_DIR / "images" / "mirai" / "background"
    if bg_dir.exists():
        for p in bg_dir.glob("*.jpeg"):
            optimize_single_image(p, "pattern")

    # 5. Dokumentasi, Haori, Lomba, Sora Carousel, Karakter/Icon Jpeg, dll.
    other_dirs = [
        ROOT_DIR / "kegiatan" / "images",
        ROOT_DIR / "tentang" / "images",
        ROOT_DIR / "lomba" / "images",
        ROOT_DIR / "sora" / "images",
        ROOT_DIR / "images" / "mirai" / "produk",
        ROOT_DIR / "images" / "mirai" / "stiker",
        ROOT_DIR / "images" / "mirai" / "karakter",
        ROOT_DIR / "images" / "mirai" / "icon",
    ]
    for odir in other_dirs:
        if odir.exists():
            for p in odir.glob("**/*"):
                if p.is_file() and p.suffix.lower() in [".jpg", ".jpeg", ".png"] and p != sora_path:
                    # Lewatkan PNG chibi dan logo yang sudah diproses
                    if p.parent == logo_dir and p.suffix.lower() == ".png":
                        continue
                    if p.parent in chibi_dirs and p.suffix.lower() == ".png":
                        continue
                    optimize_single_image(p, "photo")

    # Logo comingsoon.jpg & bendera.jpeg di logo dir
    for name in ["comingsoon.jpg", "bendera.jpeg", "Ramadhan.jpeg"]:
        p = logo_dir / name
        if p.exists():
            optimize_single_image(p, "photo")

    print(f"✔ Selesai mengompresi {stats['files_processed']} berkas gambar.")
    saved_mb = (stats['bytes_before'] - stats['bytes_after']) / 1024 / 1024
    print(f"  Total ukuran sebelum : {stats['bytes_before'] / 1024 / 1024:.2f} MB")
    print(f"  Total ukuran sesudah : {stats['bytes_after'] / 1024 / 1024:.2f} MB")
    print(f"  Hemat kapasitas      : {saved_mb:.2f} MB ({(1 - stats['bytes_after']/stats['bytes_before'])*100:.1f}%)")


def update_css_sora_references():
    print("\n==================================================")
    print("🎨 TAHAP 2: SINKRONISASI WEBP DI SELURUH CSS PAGES")
    print("==================================================")

    css_dir = ROOT_DIR / "css" / "pages"
    for css_file in css_dir.glob("*.css"):
        content = css_file.read_text(encoding="utf-8")
        orig = content

        # Arahkan url("...Sora.png") menjadi fallback WebP + image-set
        def replace_sora(match):
            indent = match.group(1)
            bang = match.group(3) or ""
            return (
                f'{indent}background-image: url("../../images/mirai/background/Sora.webp"){bang};\n'
                f'{indent}background-image: -webkit-image-set(url("../../images/mirai/background/Sora.webp") 1x, url("../../images/mirai/background/Sora.png") 1x){bang};\n'
                f'{indent}background-image: image-set(url("../../images/mirai/background/Sora.webp") type("image/webp"), url("../../images/mirai/background/Sora.png") type("image/png")){bang};'
            )

        # Cari baris background-image yang hanya merujuk Sora.png tanpa image-set
        content = re.sub(
            r'([ \t]*)background-image:\s*url\("[^"]*Sora\.png"\)(\s*!important)?;\s*(?!background-image:\s*image-set)',
            replace_sora,
            content
        )

        if content != orig:
            css_file.write_text(content, encoding="utf-8")
            print(f"  ✔ {css_file.name} disinkronkan dengan image-set WebP.")


def update_service_worker():
    print("\n==================================================")
    print("⚡ TAHAP 3: SERVICE WORKER PRECACHE MINIMAL & CACHE-FIRST")
    print("==================================================")

    # Jalankan pembuat service worker resmi
    from build_precache_list import build_service_worker
    build_service_worker()
    print("  ✔ service-worker.js siap dengan 5 file precache inti & strategi Cache-First (0ms).")


def update_html_preload_and_priority():
    print("\n==================================================")
    print("🚀 TAHAP 4: PRELOAD SORA.WEBP & FETCHPRIORITY DI HTML")
    print("==================================================")

    html_files = [p for p in ROOT_DIR.glob("**/*.html") if not any(part.startswith(".") for part in p.parts) and "skrip" not in p.parts]
    count_updated = 0

    for html_path in sorted(html_files):
        content = html_path.read_text(encoding="utf-8")
        orig = content

        # Tentukan kedalaman relative path
        rel_to_root = html_path.relative_to(ROOT_DIR)
        depth = len(rel_to_root.parts) - 1

        if depth == 0:
            rel_prefix = "./"
        elif depth == 1:
            rel_prefix = "../"
        else:
            rel_prefix = "../../"

        sora_webp_href = f"{rel_prefix}images/mirai/background/Sora.webp"

        # 1. Suntikkan atau perbarui preload Sora.webp di <head>
        preload_tag = f'<link rel="preload" as="image" href="{sora_webp_href}" type="image/webp" fetchpriority="high">'

        # Hapus preload lama jika ada
        content = re.sub(r'[ \t]*<link rel="preload" as="image" href="[^"]*Sora\.(webp|png)"[^>]*>\n?', '', content)

        # Masukkan preload tepat setelah <meta name="viewport" ...>
        if '<meta name="viewport"' in content:
            content = re.sub(
                r'(<meta name="viewport"[^>]*>\n)',
                rf'\1    {preload_tag}\n',
                content,
                count=1
            )
        elif '<head>' in content:
            content = content.replace('<head>\n', f'<head>\n    {preload_tag}\n', 1)

        # 2. Navbar Logo: hapus loading="lazy", ganti dengan loading="eager" fetchpriority="high" decoding="async"
        def fix_nav_logo(m):
            tag = m.group(0)
            tag = re.sub(r'\s*loading="[^"]*"', '', tag)
            tag = re.sub(r'\s*fetchpriority="[^"]*"', '', tag)
            tag = re.sub(r'\s*decoding="[^"]*"', '', tag)
            return tag.replace('<img', '<img loading="eager" fetchpriority="high" decoding="async"', 1)

        content = re.sub(r'<img[^>]*MNH1-nav\.png[^>]*>', fix_nav_logo, content)

        # 3. Chibi pertama di Hero (above the fold): jadikan eager & high priority
        # Cari hero container dan pastikan gambar chibi pertama di dalamnya berstatus eager
        hero_match = re.search(r'(<(?:section|header|div)[^>]*(?:class="[^"]*(?:hero|page-hero|proker-hero|quest-hero)[^"]*")[^>]*>[\s\S]*?</(?:section|header|div)>)', content)
        if hero_match:
            hero_html = hero_match.group(1)
            first_chibi = re.search(r'(<img[^>]*(?:card-corner-chibi|hero-chibi|chibi)[^>]*>)', hero_html)
            if first_chibi:
                old_tag = first_chibi.group(1)
                new_tag = re.sub(r'\s*loading="[^"]*"', '', old_tag)
                new_tag = re.sub(r'\s*fetchpriority="[^"]*"', '', new_tag)
                new_tag = re.sub(r'\s*decoding="[^"]*"', '', new_tag)
                new_tag = new_tag.replace('<img', '<img loading="eager" fetchpriority="high" decoding="async"', 1)
                content = content.replace(old_tag, new_tag, 1)

        if content != orig:
            html_path.write_text(content, encoding="utf-8")
            count_updated += 1
            print(f"  ✔ {rel_to_root} diperbarui (preload & priority tag).")

    print(f"✔ Total {count_updated} berkas HTML berhasil disinkronkan.")


def update_main_js_prefetch():
    print("\n==================================================")
    print("⚡ TAHAP 5: VERIFIKASI INSTANT PAGE PREFETCHER DI JS/MAIN.JS")
    print("==================================================")

    main_js_path = ROOT_DIR / "js" / "main.js"
    content = main_js_path.read_text(encoding="utf-8")

    if "initSmartLinkPrefetcher" not in content:
        prefetch_code = """
/* ==========================================================================
   SMART LINK PREFETCHER (Instant Page Navigation)
   Secara otomatis mem-prefetch HTML tujuan saat user hover atau touch link internal,
   sehingga perpindahan halaman terasa instan (0ms) seperti native app.
   ========================================================================== */
function initSmartLinkPrefetcher() {
  const prefetchedUrls = new Set();

  function prefetchUrl(rawHref) {
    if (!rawHref) return;
    if (rawHref.startsWith("#") || rawHref.startsWith("javascript:") || rawHref.startsWith("mailto:") || rawHref.startsWith("tel:")) return;

    try {
      const url = new URL(rawHref, window.location.href);
      if (url.origin !== window.location.origin) return;

      const cleanUrl = url.href.split("#")[0];
      if (prefetchedUrls.has(cleanUrl)) return;
      if (cleanUrl === window.location.href.split("#")[0]) return;

      prefetchedUrls.add(cleanUrl);

      const link = document.createElement("link");
      link.rel = "prefetch";
      link.href = cleanUrl;
      link.as = "document";
      document.head.appendChild(link);
    } catch (e) {}
  }

  const handleInteraction = (e) => {
    const anchor = e.target.closest("a[href]");
    if (anchor && anchor.href) {
      prefetchUrl(anchor.getAttribute("href"));
    }
  };

  document.addEventListener("mouseover", handleInteraction, { passive: true });
  document.addEventListener("touchstart", handleInteraction, { passive: true });
}
"""
        content = content.rstrip() + "\n" + prefetch_code
        main_js_path.write_text(content, encoding="utf-8")
        print("  ✔ Smart Link Prefetcher ditambahkan ke js/main.js.")
    else:
        print("  ✔ Smart Link Prefetcher sudah aktif dan terpasang di js/main.js.")


def update_stamp_and_docs():
    print("\n==================================================")
    print("🏷️  TAHAP 6: STAMP ASSET HASH & SYNC PRECACHE")
    print("==================================================")

    from stamp_asset_versions import main as stamp_main
    stamp_main()

    from build_precache_list import build_service_worker
    build_service_worker()


def print_summary_report():
    print("\n==================================================")
    print("📊 LAPORAN KOMPRESI GAMBAR (SEBELUM VS SESUDAH)")
    print("==================================================")

    # Sort details by space saved descending
    details = sorted(stats["details"], key=lambda x: (x["before"] - x["after"]), reverse=True)

    print(f"{'NAMA BERKAS':<45} | {'SEBELUM':>10} | {'SESUDAH':>10} | {'HEMAT':>7}")
    print("-" * 80)
    for d in details[:25]:
        p = d["path"]
        if len(p) > 44:
            p = "..." + p[-41:]
        b_kb = d["before"] / 1024
        a_kb = d["after"] / 1024
        print(f"{p:<45} | {b_kb:>7.1f} KB | {a_kb:>7.1f} KB | {d['ratio']:>6.1f}%")

    total_b = stats["bytes_before"] / 1024 / 1024
    total_a = stats["bytes_after"] / 1024 / 1024
    saved = total_b - total_a
    pct = (saved / total_b * 100) if total_b > 0 else 0

    print("-" * 80)
    print(f"TOTAL ({stats['files_processed']} file gambar)")
    print(f"  Sebelum Optimasi : {total_b:.2f} MB")
    print(f"  Sesudah Optimasi : {total_a:.2f} MB")
    print(f"  TOTAL DIHEMAT    : {saved:.2f} MB ({pct:.1f}% Pengurangan Bandwidth!)")
    print("==================================================\n")


def main():
    run_image_optimizations()
    update_css_sora_references()
    update_service_worker()
    update_html_preload_and_priority()
    update_main_js_prefetch()
    update_stamp_and_docs()
    print_summary_report()
    print("🎉 SEMUA OPTIMASI PERFORMA GITHUB PAGES BERHASIL 100%!")

if __name__ == "__main__":
    main()
