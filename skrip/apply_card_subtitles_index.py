#!/usr/bin/env python3
import os

def update_file(filepath, replacements):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath} (not found)")
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False
    for target, repl in replacements:
        if target in content and repl not in content:
            content = content.replace(target, repl, 1)
            changed = True
            print(f"  ✔ Updated in {filepath}: {target[:40]}...")
        else:
            print(f"  - Target already updated or missing in {filepath}: {target[:40]}...")

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Successfully wrote updates to {filepath}")
    else:
        print(f"ℹ No changes needed for {filepath}")

index_remaining = [
    (
        '<h2 class="about-card-title">Kenali Lebih Dekat<br><span class="highlight">Mirai no Hana.</span></h2>',
        '<span class="card-sub-jp">クラブ紹介</span>\n                        <h2 class="about-card-title">Kenali Lebih Dekat<br><span class="highlight">Mirai no Hana.</span></h2>'
    ),
    (
        '<h2 class="feedback-card-title">Kritik &amp;<br><span class="highlight">Saran.</span></h2>',
        '<span class="card-sub-jp">ご意見・ご要望</span>\n                    <h2 class="feedback-card-title">Kritik &amp;<br><span class="highlight">Saran.</span></h2>'
    ),
    (
        '<span class="card-step-num">1</span>\n                    <h3>Struktur Divisi</h3>',
        '<span class="card-step-num">1</span>\n                    <span class="card-sub-jp">部門構成</span>\n                    <h3>Struktur Divisi</h3>'
    ),
    (
        '<span class="card-step-num">2</span>\n                    <h3>Program Kerja</h3>',
        '<span class="card-step-num">2</span>\n                    <span class="card-sub-jp">年間企画</span>\n                    <h3>Program Kerja</h3>'
    ),
    (
        '<span class="card-step-num">3</span>\n                    <h3>Fasilitas</h3>',
        '<span class="card-step-num">3</span>\n                    <span class="card-sub-jp">部活施設</span>\n                    <h3>Fasilitas</h3>'
    ),
    (
        '<span class="card-step-num">4</span>\n                    <h3>Toko</h3>',
        '<span class="card-step-num">4</span>\n                    <span class="card-sub-jp">公式購買部</span>\n                    <h3>Toko</h3>'
    ),
    (
        '<span class="card-step-num">7</span>\n                    <h3>Lomba & Acara</h3>',
        '<span class="card-step-num">7</span>\n                    <span class="card-sub-jp">大会と行事</span>\n                    <h3>Lomba & Acara</h3>'
    )
]

update_file('index.html', index_remaining)

