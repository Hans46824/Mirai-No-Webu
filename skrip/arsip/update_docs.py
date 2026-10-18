#!/usr/bin/env python3
"""
File: skrip/arsip/update_docs.py
Fungsi: Memperbarui panduan/agent.md dan panduan/tree.md dengan dokumentasi fitur terbaru:
 1. Studio Penerjemah Adaptif Otomatis (Jepang ⇄ Indonesia) tanpa tombol tukar manual.
 2. Redesain Tata Letak Laptop/Desktop Studio Terjemahan (Dual-card grid simetris & lapang).
 3. Penghapusan seksi contoh cepat di penerjemah.
 4. Virtual Keyboard Melayang yang Bebas Digeser (Draggable) & Diubah Ukuran (Resizable) dengan batasan viewport boundaries.
 5. Redesain Generator Nama Jepang & KTA Digital (responsif HP & laptop, hapus contoh nama cepat).
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]

def update_agent_md():
    agent_path = ROOT / "panduan" / "agent.md"
    content = agent_path.read_text(encoding="utf-8")

    namegen_doc = """
### D. Redesain Generator Nama Jepang & Kartu Anggota (KTA Osatsu)
1. **Tata Letak 2 Kolom Seimbang (Laptop/Desktop) & Stacked (Mobile)**:
   - Panel Generator Nama (`#panelNameGen`) menggunakan CSS Grid 2 kolom (`grid-template-columns: minmax(0, 1fr) minmax(0, 1.25fr)` dengan `min-width: 0`).
   - Breakpoint responsif pada lebar <= 960px memastikan di layar tablet atau laptop dengan split screen, formulir input dan kartu hasil tertumpuk rapi tanpa saling mendesak atau meluap ke luar layar.
2. **Penghapusan Contoh Nama Cepat**:
   - Seksi "Contoh Nama Cepat" telah dihapus sepenuhnya dari formulir identitas, kode skrip event listener (`js/translator.js`), dan CSS. Pengguna dapat langsung mengetik nama apa pun di kotak input.
3. **Kartu Tanda Anggota (KTA) Digital Responsif**:
   - Tampilan KTA digital (`.member-card-wrap`) menggunakan tipografi dan padding adaptif dengan fungsi `clamp()` sehingga tetap proporsional dan tidak terpotong dari layar HP terkecil (360px) hingga monitor desktop besar.
   - Ateji Kanji ditampilkan dalam grid horizontal kompak 3 kolom dengan detail bacaan dan makna filosofis yang rapi.
4. **Ruang Bebas Tombol Melayang**:
   - Seksi studio memiliki `padding-bottom: 90px !important;` sehingga tombol aksi utama tidak akan tertutup oleh tombol melayang (Sora, goresan, to-top).
"""

    if "### D. Redesain Generator Nama Jepang & Kartu Anggota (KTA Osatsu)" not in content:
        if "### C. Checklist Rilis & Validasi Pra-Commit" in content:
            parts = content.split("### C. Checklist Rilis & Validasi Pra-Commit")
            content = parts[0] + namegen_doc + "\n### C. Checklist Rilis & Validasi Pra-Commit" + parts[1]
        else:
            content = content.rstrip() + "\n" + namegen_doc
        agent_path.write_text(content, encoding="utf-8")
        print("✓ panduan/agent.md berhasil diperbarui dengan dokumentasi KTA & Namegen.")
    else:
        print("ℹ panduan/agent.md sudah memuat dokumentasi KTA & Namegen.")

def update_stroke_studio_docs():
    agent_path = ROOT / "panduan" / "agent.md"
    content = agent_path.read_text(encoding="utf-8")

    stroke_studio_doc = """
## 14. Studio Goresan Interaktif 3 Kotak (Goresan)

### A. Penamaan Universal: "Goresan"
- Seluruh istilah "Urutan Goresan" disederhanakan secara konsisten menjadi **"Goresan"** (pada tombol mengambang `#quickStrokeBtn`, modal header kamus kanji, dan kartu detail kana).

### B. Arsitektur Studio 3 Kotak Interaktif (Multi-Panel Calligraphy Studio)
1. **Kotak 1: Acuan Resmi Goresan**:
   - Menampilkan animasi vektor standar KanjiVG atau Kana langkah demi langkah.
   - Kontrol navigasi presisi: Putar/Jeda (`data-stroke-play`), Putar Ulang (`data-stroke-replay`), Mundur 1 Langkah (`data-stroke-prev`), Maju 1 Langkah (`data-stroke-next`), dan Pengatur Kecepatan (`data-stroke-speed`).
2. **Kotak 2: Kanvas Tulis Mandiri (Interaktif)**:
   - Kanvas lukis responsif (`<canvas class="user-draw-canvas">`) yang mendukung sentuhan (*touch*) dan *mouse* secara mulus.
   - Dilengkapi garis kisi panduan (*grid lines* 4 kuadran tradisional kaligrafi Jepang).
   - Tombol kontrol kanvas:
     - **Bantuan Bayangan** (*Ghost Outline* toggle) untuk memandu pemula.
     - **Batalkan** (*Undo* goresan terakhir).
     - **Hapus** (*Clear* kanvas untuk memulai dari awal).
3. **Kotak 3: Hasil & Putar Otomatis (Dual Replay Stage)**:
   - Begitu pengguna selesai menorehkan goresan di Kotak 2, cuplikan karya pengguna langsung muncul di Kotak 3 berdampingan dengan animasi acuan resmi.
   - **Putar Otomatis Langsung**: Animasi acuan di Kotak 3 langsung berputar secara otomatis tanpa perlu menekan tombol putar terlebih dahulu.
   - Dilengkapi tombol **Putar Ulang** khusus untuk mengulangi perbandingan visual sewaktu-waktu.

### C. Redesain Tombol "Lapor Goresan Salah"
- Link teks polos lama digantikan oleh tombol kapsul modern (`.stroke-report-pill.stroke-report-link`) dengan ikon bendera 🚩, border glassmorphism pink halus, dan posisi yang rapi di footer modal (`.stroke-footer-bar`).

### D. Tata Letak Responsif Multi-Device
- **Laptop & Desktop (>= 992px)**: Tampilan 3 kolom berdampingan (*3-box grid* sejajar) memberikan ruang lapang untuk referensi, latihan, dan perbandingan sekaligus.
- **Tablet (768px - 991px)**: Tampilan 2 kolom adaptif yang nyaman.
- **Mobile (< 768px)**: Dilengkapi tab navigasi cepat (*Semua Kotak*, *Acuan*, *Tulis*, *Bandingkan*) sehingga pengguna di ponsel berlayar kecil dapat berpindah kotak tanpa perlu scrolling berlebihan.
"""

    if "## 14. Studio Goresan Interaktif 3 Kotak (Goresan)" not in content:
        if "### C. Checklist Rilis & Validasi Pra-Commit" in content:
            parts = content.split("### C. Checklist Rilis & Validasi Pra-Commit")
            content = parts[0] + stroke_studio_doc + "\n### C. Checklist Rilis & Validasi Pra-Commit" + parts[1]
        else:
            content = content.rstrip() + "\n" + stroke_studio_doc
        agent_path.write_text(content, encoding="utf-8")
        print("✓ panduan/agent.md berhasil diperbarui dengan dokumentasi Studio Goresan.")
    else:
        print("ℹ panduan/agent.md sudah memuat dokumentasi Studio Goresan.")

def update_tree_md():
    tree_path = ROOT / "panduan" / "tree.md"
    content = tree_path.read_text(encoding="utf-8")

    if "fix_namegen_ui.py" not in content:
        content = content.replace(
            "│       ├── update_translator_and_keyboard.py # Otomasi penerjemah adaptif, tata letak laptop, & keyboard draggable/resizable\n",
            "│       ├── update_translator_and_keyboard.py # Otomasi penerjemah adaptif, tata letak laptop, & keyboard draggable/resizable\n│       ├── fix_namegen_ui.py       # Perbaikan tata letak & UI/UX Generator Nama Jepang & KTA digital\n"
        )
    if "update_stroke_studio.py" not in content:
        content = content.replace(
            "│       ├── fix_namegen_ui.py       # Perbaikan tata letak & UI/UX Generator Nama Jepang & KTA digital\n",
            "│       ├── fix_namegen_ui.py       # Perbaikan tata letak & UI/UX Generator Nama Jepang & KTA digital\n│       ├── update_stroke_studio.py # Studio Goresan Interaktif 3 kotak, kanvas mandiri, auto-play, & lapor goresan pill\n"
        )
        tree_path.write_text(content, encoding="utf-8")
        print("✓ panduan/tree.md berhasil diperbarui dengan update_stroke_studio.py.")
    else:
        print("ℹ panduan/tree.md sudah memuat update_stroke_studio.py.")

if __name__ == "__main__":
    update_agent_md()
    update_stroke_studio_docs()
    update_tree_md()
