# Kumpulan Skrip Pembantu Pengembang (Otomasi Python)

Folder ini berisi sekumpulan skrip otomasi Python (`.py`) yang digunakan oleh pengembang / AI asisten untuk pemeliharaan dan pembaruan massal kode di balik layar:

## Fungsi Skrip-Skrip:
- **`apply_card_expand.py`**: Skrip idempoten pembaruan mode interaktif tap-to-expand pada kartu Beranda dan Tentang.
- **`add_nametag.py`**: Skrip penambahan atribut nametag katakana pengurus.
- **`fix_heroes.py`**: Skrip perbaikan tata letak seksi hero banner.
- **`fix_index_links.py`**: Skrip perbaikan tautan beranda utama.
- **`fix_japanese.py`**: Skrip sinkronisasi glif dan teks aksara Jepang.
- **`fix_sora.py` & `fix_sora2.py`**: Skrip penyempurnaan integrasi widget obrolan Sora.
- **`move_menu_btn.py`**: Skrip penyesuaian posisi tombol menu navigasi mobile.
- **`replace_cards.py` & `replace_cards_revert.py`**: Skrip pembaruan tata letak kartu modul.
- **`replace_sidebar_text.py`**: Skrip pembaruan teks bilah navigasi samping.
- **`replace_sora_grid.py`**: Skrip penataan tata letak grid kartu maskot Sora.
- **`validate_stroke_data.py`**: Skrip validator independen untuk dataset goresan KanjiVG (`js/stroke-data.js`). Memeriksa validitas viewBox, struktur XML/SVG, format koordinat kurva, urutan goresan, konsistensi metadata, dan menghasilkan manifest cakupan (`data/stroke-coverage-manifest.json`).
- **`fetch_kanjivg_strokes.py`**: Pipeline pengambilan dan parsing resmi XML/SVG KanjiVG dengan penggabungan bertahap (incremental merge), proteksi dataset lama (staging), dan validasi pra-terap otomatis.
- **`update_carousel.py` & `update_carousel_js.py`**: Skrip pembaruan logika slider/carousel poster.
- **`update_index_hero.py` & `update_kelas.py`**: Skrip pemeliharaan berkas tampilan beranda dan kelas.

> [!NOTE]
> **Catatan Pengembang**: Skrip-skrip ini **hanya dijalankan di terminal lokal saat proses pengembangan**, dan **TIDAK dijalankan di peramban pengguna** (website berjalan mandiri dengan HTML, CSS, dan JavaScript).

