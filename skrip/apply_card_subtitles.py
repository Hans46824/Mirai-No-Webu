#!/usr/bin/env python3
import re
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

# 1. toko/index.html (Cara Pemesanan cards)
toko_replacements = [
    (
        '<div class="step-icon-wrap">🛒</div>\n                    <h4>Pilih Produk</h4>',
        '<div class="step-icon-wrap">🛒</div>\n                    <span class="card-sub-jp">商品選択</span>\n                    <h4>Pilih Produk</h4>'
    ),
    (
        '<div class="step-icon-wrap">📋</div>\n                    <h4>Isi Formulir</h4>',
        '<div class="step-icon-wrap">📋</div>\n                    <span class="card-sub-jp">フォーム入力</span>\n                    <h4>Isi Formulir</h4>'
    ),
    (
        '<div class="step-icon-wrap">💵</div>\n                    <h4>Pembayaran Kas</h4>',
        '<div class="step-icon-wrap">💵</div>\n                    <span class="card-sub-jp">部費・代金支払</span>\n                    <h4>Pembayaran Kas</h4>'
    ),
    (
        '<div class="step-icon-wrap">📦</div>\n                    <h4>Ambil Pesanan</h4>',
        '<div class="step-icon-wrap">📦</div>\n                    <span class="card-sub-jp">商品受取</span>\n                    <h4>Ambil Pesanan</h4>'
    )
]

# 2. kegiatan/index.html (Divisi, Proker, Fasilitas)
kegiatan_replacements = [
    (
        '<img src="../images/mirai/logo/comingsoon.jpg" alt="Logo Divisi Bahasa">\n        <h3>Divisi Bahasa</h3>',
        '<img src="../images/mirai/logo/comingsoon.jpg" alt="Logo Divisi Bahasa">\n        <span class="card-sub-jp">言語部門</span>\n        <h3>Divisi Bahasa</h3>'
    ),
    (
        '<img src="../images/mirai/logo/comingsoon.jpg" alt="Logo Divisi Cosplay">\n        <h3>Divisi Cosplay</h3>',
        '<img src="../images/mirai/logo/comingsoon.jpg" alt="Logo Divisi Cosplay">\n        <span class="card-sub-jp">コスプレ部門</span>\n        <h3>Divisi Cosplay</h3>'
    ),
    (
        '<img src="../images/mirai/logo/comingsoon.jpg" alt="Logo Divisi Desain">\n        <h3>Divisi Desain</h3>',
        '<img src="../images/mirai/logo/comingsoon.jpg" alt="Logo Divisi Desain">\n        <span class="card-sub-jp">デザイン部門</span>\n        <h3>Divisi Desain</h3>'
    ),
    (
        '<img src="../images/mirai/logo/comingsoon.jpg" alt="Logo Divisi KWU">\n        <h3>Divisi KWU</h3>',
        '<img src="../images/mirai/logo/comingsoon.jpg" alt="Logo Divisi KWU">\n        <span class="card-sub-jp">起業部門</span>\n        <h3>Divisi KWU</h3>'
    ),
    (
        '<img src="images/KTN.png" alt="Logo Kimi To Nippon">\n        <h3>Kimi To Nippon</h3>',
        '<img src="images/KTN.png" alt="Logo Kimi To Nippon">\n        <span class="card-sub-jp">君と日本</span>\n        <h3>Kimi To Nippon</h3>'
    ),
    (
        '<img src="images/NGR.png" alt="Logo Nihon Go Rajio">\n        <h3>Nihon Go Rajio</h3>',
        '<img src="images/NGR.png" alt="Logo Nihon Go Rajio">\n        <span class="card-sub-jp">日本語ラジオ</span>\n        <h3>Nihon Go Rajio</h3>'
    ),
    (
        '<img src="images/Mirainokonbini.png" alt="Logo Mirai no Konbini">\n        <h3>Mirai no Konbini</h3>',
        '<img src="images/Mirainokonbini.png" alt="Logo Mirai no Konbini">\n        <span class="card-sub-jp">未来のコンビニ</span>\n        <h3>Mirai no Konbini</h3>'
    ),
    (
        '<img src="images/Ramadhan.jpeg" alt="Logo Ramadhan Shukufuku">\n        <h3>Ramadhan Shukufuku</h3>',
        '<img src="images/Ramadhan.jpeg" alt="Logo Ramadhan Shukufuku">\n        <span class="card-sub-jp">ラマダン祝福</span>\n        <h3>Ramadhan Shukufuku</h3>'
    ),
    (
        '<img src="../images/mirai/logo/comingsoon.jpg" alt="Logo Nihon Tomodachi">\n        <h3>Nihon Tomodachi</h3>',
        '<img src="../images/mirai/logo/comingsoon.jpg" alt="Logo Nihon Tomodachi">\n        <span class="card-sub-jp">日本の友達</span>\n        <h3>Nihon Tomodachi</h3>'
    ),
    (
        '<h3>Ruang Pertemuan &amp; <span>Pembelajaran</span></h3>',
        '<span class="card-sub-jp">教室と学習施設</span>\n          <h3>Ruang Pertemuan &amp; <span>Pembelajaran</span></h3>'
    ),
    (
        '<h3>Belajar di mana pun,<br><span>dan kapanpun.</span></h3>',
        '<span class="card-sub-jp">デジタル学習ポータル</span>\n          <h3>Belajar di mana pun,<br><span>dan kapanpun.</span></h3>'
    ),
    (
        '<h3>Pakaian, Aksesori &amp;<br><span>Identitas Resmi Klub</span></h3>',
        '<span class="card-sub-jp">公式制服と所属証</span>\n          <h3>Pakaian, Aksesori &amp;<br><span>Identitas Resmi Klub</span></h3>'
    )
]

# 3. divisi/index.html (Divisi cards)
divisi_replacements = [
    (
        '<img src="../images/mirai/logo/comingsoon.jpg" alt="Logo Divisi Bahasa">\n        <h3>Divisi Bahasa</h3>',
        '<img src="../images/mirai/logo/comingsoon.jpg" alt="Logo Divisi Bahasa">\n        <span class="card-sub-jp">言語部門</span>\n        <h3>Divisi Bahasa</h3>'
    ),
    (
        '<img src="../images/mirai/logo/comingsoon.jpg" alt="Logo Divisi Cosplay">\n        <h3>Divisi Cosplay</h3>',
        '<img src="../images/mirai/logo/comingsoon.jpg" alt="Logo Divisi Cosplay">\n        <span class="card-sub-jp">コスプレ部門</span>\n        <h3>Divisi Cosplay</h3>'
    ),
    (
        '<img src="../images/mirai/logo/comingsoon.jpg" alt="Logo Divisi Desain">\n        <h3>Divisi Desain</h3>',
        '<img src="../images/mirai/logo/comingsoon.jpg" alt="Logo Divisi Desain">\n        <span class="card-sub-jp">デザイン部門</span>\n        <h3>Divisi Desain</h3>'
    ),
    (
        '<img src="../images/mirai/logo/comingsoon.jpg" alt="Logo Divisi KWU">\n        <h3>Divisi Kewirausahaan</h3>',
        '<img src="../images/mirai/logo/comingsoon.jpg" alt="Logo Divisi KWU">\n        <span class="card-sub-jp">起業部門</span>\n        <h3>Divisi Kewirausahaan</h3>'
    )
]

# 4. index.html (Beranda navigation cards)
index_replacements = [
    (
        '<h2 class="about-card-title">Apa itu<br><span class="highlight">Mirai no Webu?</span></h2>',
        '<span class="card-sub-jp">ポータル紹介</span>\n                        <h2 class="about-card-title">Apa itu<br><span class="highlight">Mirai no Webu?</span></h2>'
    ),
    (
        '<h2 class="about-card-title">Tentang Klub<br><span class="highlight">Mirai no Hana</span></h2>',
        '<span class="card-sub-jp">クラブ紹介</span>\n                        <h2 class="about-card-title">Tentang Klub<br><span class="highlight">Mirai no Hana</span></h2>'
    ),
    (
        '<h2 class="feedback-card-title">Kritik &amp; Saran<br><span class="highlight">Pengunjung</span></h2>',
        '<span class="card-sub-jp">ご意見・ご要望</span>\n                        <h2 class="feedback-card-title">Kritik &amp; Saran<br><span class="highlight">Pengunjung</span></h2>'
    ),
    (
        '<span class="card-step-num">1</span>\n                    <h3>Kelas Dasar</h3>',
        '<span class="card-step-num">1</span>\n                    <span class="card-sub-jp">基礎クラス</span>\n                    <h3>Kelas Dasar</h3>'
    ),
    (
        '<span class="card-step-num">2</span>\n                    <h3>Kelas Lanjutan</h3>',
        '<span class="card-step-num">2</span>\n                    <span class="card-sub-jp">上級クラス</span>\n                    <h3>Kelas Lanjutan</h3>'
    ),
    (
        '<span class="card-step-num">3</span>\n                    <h3>Kamus</h3>',
        '<span class="card-step-num">3</span>\n                    <span class="card-sub-jp">辞書検索</span>\n                    <h3>Kamus</h3>'
    ),
    (
        '<span class="card-step-num">4</span>\n                    <h3>Kurikulum &amp; Tata Cara</h3>',
        '<span class="card-step-num">4</span>\n                    <span class="card-sub-jp">指導方針</span>\n                    <h3>Kurikulum &amp; Tata Cara</h3>'
    ),
    (
        '<h3>Program &amp; Fasilitas</h3>',
        '<span class="card-sub-jp">活動と施設</span>\n                    <h3>Program &amp; Fasilitas</h3>'
    ),
    (
        '<h3>Toko &amp; Merchandise</h3>',
        '<span class="card-sub-jp">公式購買部</span>\n                    <h3>Toko &amp; Merchandise</h3>'
    ),
    (
        '<h3>Papan Peringkat</h3>',
        '<span class="card-sub-jp">番付表</span>\n                    <h3>Papan Peringkat</h3>'
    ),
    (
        '<h3>Lomba &amp; Acara</h3>',
        '<span class="card-sub-jp">大会と行事</span>\n                    <h3>Lomba &amp; Acara</h3>'
    ),
    (
        '<h3>Rekomendasi</h3>',
        '<span class="card-sub-jp">おすすめ</span>\n                    <h3>Rekomendasi</h3>'
    ),
    (
        '<h3>Ruang Motivasi</h3>',
        '<span class="card-sub-jp">名言空間</span>\n                    <h3>Ruang Motivasi</h3>'
    ),
    (
        '<h3>Tentang Mirai no Hana</h3>',
        '<span class="card-sub-jp">クラブについて</span>\n                    <h3>Tentang Mirai no Hana</h3>'
    )
]

print("Executing script to apply card Japanese subtitles...")
update_file('toko/index.html', toko_replacements)
update_file('kegiatan/index.html', kegiatan_replacements)
update_file('divisi/index.html', divisi_replacements)
update_file('index.html', index_replacements)
print("Done!")

