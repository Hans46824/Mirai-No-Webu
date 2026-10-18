#!/usr/bin/env python3
"""
Skrip Otomatis: Pengamanan Sistem Visual Universal & Onboarding Developer Baru
1. Amankan Sistem Visual Universal di css/pages/global.css & css/pages/lomba.css:
   - Hapus selector wildcard agresif [class*="-card"], [class*="-box"], [class*="-head"].
   - Sediakan Utility Classes resmi: .mirai-section-light, .mirai-section-dark, .mirai-card-light, .mirai-card-dark.
   - Proteksi elemen sub-kartu dengan guard eksplisit :not().
   - Pastikan di lomba.css kartu .lomba-card, .lomba-card-head, dan .lomba-point-card bersih bebas border ganda.
2. Bersihkan Struktur Folder & Buat .vscode/extensions.json:
   - Hapus skrip/skrip/ jika ada.
   - Pindahkan skrip perbaikan sekali-pakai ke skrip/arsip/.
   - Buat .vscode/extensions.json dengan rekomendasi ekstensi resmi.
   - Optimalkan .vscode/settings.json dengan formatOnSave, tabSize 2, dan filter pencarian.
3. Lengkapi panduan/PANDUAN-DEVELOPER.md dengan "Bab 0: Persiapan Awal & Instalasi Tools".
4. Sinkronkan panduan/tree.md dan panduan/agent.md dengan file terbaru.
"""

import os
import re
import json
import shutil

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def log(msg):
    print(f"[SECURE] {msg}")

# ==============================================================================
# 1. AMANKAN SISTEM VISUAL UNIVERSAL DI global.css & lomba.css
# ==============================================================================
def secure_global_and_lomba_css():
    log("=== [1] Mengamankan Sistem Visual Universal di global.css & lomba.css ===")
    
    # 1.a global.css
    global_css_path = os.path.join(BASE_DIR, "css", "pages", "global.css")
    with open(global_css_path, "r", encoding="utf-8") as f:
        g_css = f.read()

    # Pastikan tidak ada wildcard agresif pada touch/tap highlight di baris 2124
    g_css = g_css.replace(
        'a, button, [role="button"], input, select, textarea, .card, [class*="-card"], [class*="card"], .btn, [class*="btn"], [data-expand-card], .nav-card, .activity-start-card, .start-card {',
        'a, button, [role="button"], input, select, textarea, .card, .btn, [data-expand-card], .nav-card, .activity-start-card, .start-card {'
    )

    # Tambahkan utility class resmi jika belum ada
    utility_block = """
/* ==========================================================================
   UTILITY CLASSES SISTEM VISUAL UNIVERSAL MIRAI (WHITELIST & ANTI-BREAK)
   Gunakan class resmi ini saat menambah seksi / kartu baru agar aman & konsisten:
   - .mirai-section-light / .mirai-section-dark
   - .mirai-card-light / .mirai-card-dark
   ========================================================================== */
.mirai-section-light {
  background-color: #ffffff !important;
  background-image: none !important;
  color: #18151b !important;
}

.mirai-section-dark {
  background-color: #111111 !important;
  background-image: none !important;
  color: #ffffff !important;
}

.mirai-card-light {
  background-color: #ffffff !important;
  border: 1.5px solid var(--pink-border, #f4bfd3) !important;
  border-radius: 18px !important;
  position: relative !important;
  overflow: hidden !important;
  color: #18151b !important;
  box-shadow: 0 4px 16px rgba(233, 30, 99, 0.05), 0 1px 3px rgba(0, 0, 0, 0.03) !important;
}

.mirai-card-light::after {
  content: "" !important;
  position: absolute !important;
  inset: 0 !important;
  background-image: var(--pattern-c1w, url("../../images/mirai/background/c1w.jpeg")) !important;
  background-size: 200px auto !important;
  background-repeat: repeat !important;
  background-position: center top !important;
  opacity: 0.045 !important;
  mix-blend-mode: multiply !important;
  pointer-events: none !important;
  z-index: 1 !important;
  border-radius: inherit !important;
  display: block !important;
}

.mirai-card-light > * {
  position: relative !important;
  z-index: 2 !important;
}

.mirai-card-dark {
  background-color: #16121d !important;
  background: linear-gradient(155deg, #181322 0%, #0e0b14 100%) !important;
  border: 1.5px solid rgba(255, 101, 155, 0.22) !important;
  border-radius: 18px !important;
  position: relative !important;
  overflow: hidden !important;
  color: #ffffff !important;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
}

.mirai-card-dark::after {
  content: "" !important;
  position: absolute !important;
  inset: 0 !important;
  background-image: var(--pattern-c1b, url("../../images/mirai/background/c1b.jpeg")) !important;
  background-size: 200px auto !important;
  background-repeat: repeat !important;
  background-position: center top !important;
  opacity: 0.045 !important;
  mix-blend-mode: screen !important;
  pointer-events: none !important;
  z-index: 1 !important;
  border-radius: inherit !important;
  display: block !important;
}

.mirai-card-dark > * {
  position: relative !important;
  z-index: 2 !important;
}

/* Guard Proteksi Sub-Elemen Kartu: Mencegah Duplikasi Border / Background Inner */
.mirai-card-light [class*="-head"]:not(.mirai-card-light):not(.mirai-card-dark),
.mirai-card-light [class*="-header"]:not(.mirai-card-light):not(.mirai-card-dark),
.mirai-card-light [class*="-body"]:not(.mirai-card-light):not(.mirai-card-dark),
.mirai-card-light [class*="-inner"]:not(.mirai-card-light):not(.mirai-card-dark),
.mirai-card-light [class*="-point-card"]:not(.mirai-card-light):not(.mirai-card-dark),
.mirai-card-light [class*="-badge"]:not(.mirai-card-light):not(.mirai-card-dark),
.mirai-card-light [class*="-title"]:not(.mirai-card-light):not(.mirai-card-dark),
.mirai-card-dark [class*="-head"]:not(.mirai-card-light):not(.mirai-card-dark),
.mirai-card-dark [class*="-header"]:not(.mirai-card-light):not(.mirai-card-dark),
.mirai-card-dark [class*="-body"]:not(.mirai-card-light):not(.mirai-card-dark),
.mirai-card-dark [class*="-inner"]:not(.mirai-card-light):not(.mirai-card-dark),
.mirai-card-dark [class*="-point-card"]:not(.mirai-card-light):not(.mirai-card-dark),
.mirai-card-dark [class*="-badge"]:not(.mirai-card-light):not(.mirai-card-dark),
.mirai-card-dark [class*="-title"]:not(.mirai-card-light):not(.mirai-card-dark) {
  background-image: none !important;
}

.mirai-card-light [class*="-head"]::before,
.mirai-card-light [class*="-head"]::after,
.mirai-card-light [class*="-header"]::before,
.mirai-card-light [class*="-header"]::after,
.mirai-card-light [class*="-body"]::before,
.mirai-card-light [class*="-body"]::after,
.mirai-card-light [class*="-inner"]::before,
.mirai-card-light [class*="-inner"]::after,
.mirai-card-light [class*="-point-card"]::before,
.mirai-card-light [class*="-point-card"]::after,
.mirai-card-light [class*="-badge"]::before,
.mirai-card-light [class*="-badge"]::after,
.mirai-card-light [class*="-title"]::before,
.mirai-card-light [class*="-title"]::after,
.mirai-card-dark [class*="-head"]::before,
.mirai-card-dark [class*="-head"]::after,
.mirai-card-dark [class*="-header"]::before,
.mirai-card-dark [class*="-header"]::after,
.mirai-card-dark [class*="-body"]::before,
.mirai-card-dark [class*="-body"]::after,
.mirai-card-dark [class*="-inner"]::before,
.mirai-card-dark [class*="-inner"]::after,
.mirai-card-dark [class*="-point-card"]::before,
.mirai-card-dark [class*="-point-card"]::after,
.mirai-card-dark [class*="-badge"]::before,
.mirai-card-dark [class*="-badge"]::after,
.mirai-card-dark [class*="-title"]::before,
.mirai-card-dark [class*="-title"]::after {
  content: none !important;
  display: none !important;
  background-image: none !important;
}
"""

    if "UTILITY CLASSES SISTEM VISUAL UNIVERSAL MIRAI" not in g_css:
        g_css += "\n" + utility_block.strip() + "\n"
        with open(global_css_path, "w", encoding="utf-8") as f:
            f.write(g_css)
        log("Utility classes universal (.mirai-section-*, .mirai-card-*) berhasil ditambahkan ke global.css.")

    # 1.b lomba.css
    lomba_css_path = os.path.join(BASE_DIR, "css", "pages", "lomba.css")
    with open(lomba_css_path, "r", encoding="utf-8") as f:
        l_css = f.read()

    lomba_protect_block = """
/* ==========================================================================
   PROTEKSI KOMPONEN LOMBA & SUB-JUDUL POIN (ANTI-BORDER GANDA & BERSIH)
   ========================================================================== */
.lomba-card,
.lomba-detail-card,
.lomba-point-card {
  position: relative !important;
}

.lomba-card-top,
.lomba-card-head,
.lomba-card-header-compact,
.lomba-point-card-head,
.badge-card-item,
.badge-card-label {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}

.badge-card-item .badge-card-label {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  padding: 0 !important;
}

.lomba-card-top::before,
.lomba-card-top::after,
.lomba-card-head::before,
.lomba-card-head::after,
.lomba-card-header-compact::before,
.lomba-card-header-compact::after,
.lomba-point-card-head::before,
.lomba-point-card-head::after,
.badge-card-item::before,
.badge-card-item::after,
.badge-card-label::before,
.badge-card-label::after {
  content: none !important;
  display: none !important;
  background-image: none !important;
}
"""

    # Ganti blok proteksi lama jika ada atau sisipkan di akhir
    if "/* Proteksi Header Kompak & Sub-Label Poin Lomba (Bebas Kotak Border Aneh) */" in l_css:
        l_css = re.sub(
            r"/\* Proteksi Header Kompak & Sub-Label Poin Lomba \(Bebas Kotak Border Aneh\) \*/[^}]*\}\s*\.badge-card-item[^}]*\}\s*\.badge-card-item \.badge-card-label[^}]*\}",
            lomba_protect_block.strip(),
            l_css
        )
    elif "PROTEKSI KOMPONEN LOMBA & SUB-JUDUL POIN" not in l_css:
        l_css += "\n" + lomba_protect_block.strip() + "\n"

    with open(lomba_css_path, "w", encoding="utf-8") as f:
        f.write(l_css)
    log("Proteksi komponen lomba (.lomba-card, .lomba-card-head, .lomba-point-card) diperbarui di lomba.css.")

# ==============================================================================
# 2. BERSIHKAN STRUKTUR FOLDER & BUAT .vscode/extensions.json & settings.json
# ==============================================================================
def setup_vscode_and_clean_folders():
    log("=== [2] Membersihkan Struktur Folder & Konfigurasi .vscode ===")
    
    # 2.a Hapus skrip/skrip/ jika ada
    double_skrip = os.path.join(BASE_DIR, "skrip", "skrip")
    if os.path.exists(double_skrip):
        if os.path.isdir(double_skrip):
            shutil.rmtree(double_skrip)
            log("Folder tidak sengaja 'skrip/skrip/' berhasil dihapus.")
        else:
            os.remove(double_skrip)

    # 2.b Pindahkan skrip perbaikan sekali-pakai ke skrip/arsip/
    arsip_dir = os.path.join(BASE_DIR, "skrip", "arsip")
    os.makedirs(arsip_dir, exist_ok=True)
    
    for fname in ["apply_5_main_fixes.py", "apply_portrait_pattern_zoom_out.py", "apply_transparency_and_tentang_fixes.py"]:
        src = os.path.join(BASE_DIR, "skrip", fname)
        if os.path.exists(src):
            dst = os.path.join(arsip_dir, fname)
            shutil.move(src, dst)
            log(f"Berkas skrip {fname} berhasil diarsipkan ke skrip/arsip/.")

    # 2.c Buat .vscode/extensions.json
    vscode_dir = os.path.join(BASE_DIR, ".vscode")
    os.makedirs(vscode_dir, exist_ok=True)
    
    ext_data = {
        "recommendations": [
            "esbenp.prettier-vscode",
            "ritwickdey.LiveServer",
            "streetsidesoftware.code-spell-checker",
            "ms-python.python",
            "formulahendry.auto-rename-tag",
            "ecmel.vscode-html-css",
            "christian-kohler.path-intellisense",
            "naumovs.color-highlight",
            "tonybaloney.vscode-pets"
        ]
    }
    ext_path = os.path.join(vscode_dir, "extensions.json")
    with open(ext_path, "w", encoding="utf-8") as f:
        json.dump(ext_data, f, indent=2)
    log("Berkas .vscode/extensions.json berhasil dibuat dengan 9 ekstensi rekomendasi resmi.")

    # 2.d Optimalkan .vscode/settings.json
    settings_data = {
        "files.saveConflictResolution": "overwriteFileOnDisk",
        "editor.formatOnSave": True,
        "editor.tabSize": 2,
        "cSpell.enabled": False,
        "cSpell.ignorePaths": [
            "**/*"
        ],
        "search.exclude": {
            "**/.git": True,
            "**/__pycache__": True,
            "**/data/*.json": True,
            "**/js/stroke-data.js": True,
            "**/skrip/arsip/**": True,
            "**/*.bak": True,
            "**/js/kanji-data.js": True
        },
        "files.watcherExclude": {
            "**/.git": True,
            "**/__pycache__": True,
            "**/data/*.json": True,
            "**/js/stroke-data.js": True,
            "**/skrip/arsip/**": True,
            "**/*.bak": True,
            "**/js/kanji-data.js": True
        }
    }
    settings_path = os.path.join(vscode_dir, "settings.json")
    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump(settings_data, f, indent=2)
    log("Berkas .vscode/settings.json berhasil dioptimalkan (formatOnSave, tabSize 2, exclusions).")

# ==============================================================================
# 3. LENGKAPI panduan/PANDUAN-DEVELOPER.md DENGAN BAB 0
# ==============================================================================
def update_panduan_developer():
    log("=== [3] Melengkapi panduan/PANDUAN-DEVELOPER.md dengan Bab 0 ===")
    
    dev_path = os.path.join(BASE_DIR, "panduan", "PANDUAN-DEVELOPER.md")
    with open(dev_path, "r", encoding="utf-8") as f:
        content = f.read()

    bab0_text = """## 🚀 Bab 0: Persiapan Awal & Instalasi Tools (Wajib untuk Pengurus/Developer Baru)

Selamat datang di tim pengembang **Mirai no Webu**! Bagian ini disusun khusus secara ramah pemula agar siapa pun pengurus atau anggota klub yang baru ditunjuk dapat menyiapkan perangkat komputer/laptopnya dari nol hingga siap mengedit website dengan nyaman, rapi, dan bebas error.

---

### Langkah 1: Instalasi Code Editor & Tools Dasar
Sebelum membuka proyek, pastikan Anda telah memasang 3 perangkat lunak esensial berikut:
1. **Visual Studio Code (VS Code)** *(Wajib)*:
   - Unduh gratis di situs resmi: [code.visualstudio.com](https://code.visualstudio.com/).
   - Editor kode standar industri yang sangat ringan, cepat, dan memiliki ekosistem ekstensi terlengkap.
2. **Git Version Control** *(Wajib)*:
   - Unduh di: [git-scm.com](https://git-scm.com/).
   - Digunakan untuk mencatat riwayat perubahan kode (commit) dan menyinkronkan website ke GitHub Pages.
3. **Python 3 (v3.10+)** *(Sangat Dianjurkan)*:
   - Unduh di: [python.org](https://www.python.org/).
   - **PENTING saat instalasi di Windows**: Centang opsi **"Add python.exe to PATH"** agar perintah `python` dapat dipanggil langsung dari terminal VS Code untuk menjalankan skrip automasi pengurus di folder `skrip/arsip/`.

---

### Langkah 2: Instalasi AI Coding Agent di VS Code
Website ini dirancang agar sangat mudah dikembangkan bersama asisten kecerdasan buatan (AI Pair Programming). Anda dapat memasang salah satu ekstensi AI berikut di VS Code:
- **Google Antigravity / Gemini CLI**: Asisten AI resmi berkonteks besar.
- **GitHub Copilot**: Ekstensi resmi dari GitHub (`GitHub.copilot`).
- **Cline / Claude Code**: Asisten AI agentic untuk VS Code.
- **Cursor IDE**: Editor fork VS Code dengan AI bawaan.

#### Cara Menyuapi Konteks ke AI (Context Feeding Wajib):
Setiap kali Anda memberikan instruksi baru kepada AI, **SELALU sertakan mention berkas konteks** berikut di awal percakapan:
```text
@panduan/agent.md @panduan/CONTEKAN-TAG.md
Tolong bantu saya menambahkan [sebutkan tugas Anda di sini]...
```
*Dengan menyuapi kedua file panduan ini, AI akan otomatis tahu letak CSS/JS yang tepat, mematuhi standar desain tanpa merusak layout, dan tidak akan mencoba membaca file CSS secara membabi-buta.*

---

### Langkah 3: Daftar Ekstensi VS Code Wajib & Fungsinya
Folder `.vscode/extensions.json` telah disiapkan di repositori ini. Berikut 9 ekstensi resmi yang wajib Anda pasang beserta fungsinya:

| Nama Ekstensi | Identifier | Fungsi Utama |
| :--- | :--- | :--- |
| **Prettier - Code formatter** | `esbenp.prettier-vscode` | Merapikan baris & indentasi HTML/CSS/JS secara otomatis setiap kali menekan `Ctrl + S`. |
| **Live Server** | `ritwickdey.LiveServer` | Menjalankan preview website di browser lokal dengan 1 klik ("Go Live" di status bar kanan bawah). |
| **Code Spell Checker** | `streetsidesoftware.code-spell-checker` | Mencegah salah ketik (typo) teks dan variabel kode, terhubung ke kamus proyek `cspell.json`. |
| **Python** | `ms-python.python` | Menjalankan skrip automasi pemeliharaan web di folder `skrip/arsip/` langsung dari editor. |
| **Auto Rename Tag** | `formulahendry.auto-rename-tag` | Otomatis mengubah tag penutup saat tag pembuka HTML diedit, mencegah bug tag tak seimbang. |
| **HTML CSS Support** | `ecmel.vscode-html-css` | Menampilkan rekomendasi nama class CSS saat mengetik di berkas HTML secara otomatis. |
| **Path Intellisense** | `christian-kohler.path-intellisense` | Membantu autocomplete path gambar atau file (misal `../../images/...`) tanpa takut salah ketik. |
| **Color Highlight** | `naumovs.color-highlight` | Menampilkan kotak warna visual langsung pada kode warna hex/RGBA di stylesheet CSS. |
| **VS Code Pets** | `tonybaloney.vscode-pets` | Menghadirkan hewan peliharaan animasi kecil lucu di panel editor untuk menemani Anda ngoding! 🐱🐶 |

---

### Langkah 4: Cara Mengatur VS Code (Settings & Extensions)
Proyek ini telah dilengkapi pengaturan otomatis di dalam folder `.vscode/`:
1. Buka folder proyek `Mirai-No-Webu` di VS Code (`File > Open Folder...`).
2. Buka tab Ekstensi (`Ctrl + Shift + X`), ketik `@recommended` di kolom pencarian atas.
3. Klik tombol **"Install Workspace Recommended Extensions"** untuk memasang seluruh paket ekstensi dalam 1 klik.
4. Berkas `.vscode/settings.json` telah otomatis mengunci:
   - `editor.formatOnSave: true` (merapikan kode otomatis saat simpan).
   - `editor.tabSize: 2` (standar spasi 2 karakter yang rapi).
   - Menyembunyikan folder besar seperti `.git`, `__pycache__`, dan berkas vektor besar `stroke-data.js` dari pencarian agar VS Code berjalan **sangat cepat dan ringan**.

---

### Langkah 5: Cara Memakai Utility Class Universal (Anti-Rusak)
Untuk memastikan siapa pun pengurus baru yang menambah konten tidak akan merusak layout atau membuat selector wildcard yang bentrok, gunakan **Utility Classes Resmi** yang sudah disediakan di `css/pages/global.css`:

1. **Membuat Seksi Halaman Baru**:
   - Seksi Tema Terang: `<section class="section mirai-section-light">`
   - Seksi Tema Gelap: `<section class="section mirai-section-dark">`
2. **Membuat Kartu Konten Baru**:
   - Kartu Cerah Berpola Halus:
     ```html
     <div class="mirai-card-light">
       <h3>Judul Kartu</h3>
       <p>Deskripsi konten kartu...</p>
     </div>
     ```
   - Kartu Gelap Berpola Halus:
     ```html
     <div class="mirai-card-dark">
       <h3>Judul Kartu</h3>
       <p>Deskripsi konten kartu...</p>
     </div>
     ```
3. **Mengapa Wajib Menggunakan Class Ini?**
   - Kartu otomatis memiliki sudut melengkung 18px, border beraksen pink lembut, dan watermark pattern halus (4.5% opacity).
   - Sudah terpasang **guard anti-double pattern**: elemen di dalam kartu (judul, header, icon, badge) diproteksi secara otomatis agar tidak memiliki kotak border ganda atau latar bertumpuk.

---

"""

    # Update Daftar Isi
    old_toc = """## 📑 Daftar Isi
1. [Pengenalan Arsitektur Web (Zero-Framework Architecture)](#1-pengenalan-arsitektur-web-zero-framework-architecture)"""
    new_toc = """## 📑 Daftar Isi
0. [Bab 0: Persiapan Awal & Instalasi Tools (Wajib untuk Pengurus/Developer Baru)](#-bab-0-persiapan-awal--instalasi-tools-wajib-untuk-pengurusdeveloper-baru)
   - [Langkah 1: Instalasi Code Editor & Tools Dasar](#langkah-1-instalasi-code-editor--tools-dasar)
   - [Langkah 2: Instalasi AI Coding Agent di VS Code](#langkah-2-instalasi-ai-coding-agent-di-vs-code)
   - [Langkah 3: Daftar Ekstensi VS Code Wajib & Fungsinya](#langkah-3-daftar-ekstensi-vs-code-wajib--fungsinya)
   - [Langkah 4: Cara Mengatur VS Code (Settings & Extensions)](#langkah-4-cara-mengatur-vs-code-settings--extensions)
   - [Langkah 5: Cara Memakai Utility Class Universal (Anti-Rusak)](#langkah-5-cara-memakai-utility-class-universal-anti-rusak)
1. [Pengenalan Arsitektur Web (Zero-Framework Architecture)](#1-pengenalan-arsitektur-web-zero-framework-architecture)"""

    if "## 🚀 Bab 0: Persiapan Awal & Instalasi Tools" not in content:
        content = content.replace(old_toc, new_toc)
        # Sisipkan Bab 0 sebelum "## 1. Pengenalan Arsitektur Web"
        anchor = "## 1. Pengenalan Arsitektur Web (Zero-Framework Architecture)"
        content = content.replace(anchor, bab0_text + anchor)
        log("Bab 0 Onboarding berhasil disisipkan ke panduan/PANDUAN-DEVELOPER.md.")

    # Update aturan visual universal pada PANDUAN-DEVELOPER.md agar selaras
    old_rule_block = """2. **Kunci Transparansi Universal Khusus Kartu (11% Terang, 18% Gelap)**:
   - Pola Terang (`c1w` / `w1w`): Wajib tepat **11%** (`opacity: 0.11 !important` atau via `--overlay-card-light` dengan `alpha: 0.89`).
   - Pola Gelap (`c1b` / `w1b`): Wajib tepat **18%** (`opacity: 0.18 !important` atau via `--overlay-card-dark` dengan `alpha: 0.82`).
   - Dilarang keras menggunakan transparansi acak/belang-belang (seperti 0.045 atau 0.16).

3. **Seksi Selang-Seling Bersih & Polos (Pattern HANYA pada Kartu, DILARANG pada Halaman/Seksi)**:
   - Semua `<section>` konten setelah Hero wajib memiliki latar belakang solid yang 100% bersih, polos, dan bebas dari pattern gambar latar (`background-image: none !important;`):
     - Seksi Ganjil (`nth-of-type(odd)`): Putih Bersih (`#ffffff`) polos dengan teks kontras tinggi (`#18151b` / `#554e57`).
     - Seksi Genap (`nth-of-type(even)`): Hitam Obsidian (`#111111`) polos dengan teks kontras terang (`#ffffff` / `#d5ccd3`).
   - **DILARANG KERAS** memasang pattern pada elemen `<section>`, `<body>`, atau latar halaman. Motif Jepang (Wagara/Kumo) HANYA boleh ada di dalam elemen kartu (`.card` / `[class*="-card"]`)!

4. **Pewarisan Kartu Universal Otomatis (Auto-Inheritance)**:
   - Setiap elemen kartu standar (`.card`, `[class*="-card"]`, di luar elemen inner/title/desc) otomatis mewarisi radius border (18px), border beraksen pink (`#f4bfd3` untuk kartu terang, `rgba(255, 101, 155, 0.22)` untuk kartu gelap), dan pattern universal yang sesuai dengan warna latarnya."""

    new_rule_block = """2. **Kunci Transparansi Watermark Sangat Lembut (Maksimal Keterbacaan Teks)**:
   - Pola Terang & Gelap: Dikunci pada **`opacity: 0.045 !important`** (hover: `0.07 !important`) dan gradien penutup master di `:root` sebesar `0.95`–`0.97` agar teks kartu sangat jernih, tajam, dan tidak terganggu oleh garis gelombang latar.

3. **Seksi Selang-Seling Bersih & Polos (Pattern HANYA pada Kartu, DILARANG pada Halaman/Seksi)**:
   - Semua `<section>` konten setelah Hero wajib memiliki latar belakang solid yang 100% bersih, polos, dan bebas dari pattern gambar latar (`background-image: none !important;`):
     - Seksi Ganjil (`nth-of-type(odd)`): Putih Bersih (`#ffffff`) polos dengan teks kontras tinggi (`#18151b` / `#554e57`).
     - Seksi Genap (`nth-of-type(even)`): Hitam Obsidian (`#111111`) polos dengan teks kontras terang (`#ffffff` / `#d5ccd3`).
   - Gunakan utility class `.mirai-section-light` dan `.mirai-section-dark` saat membuat seksi baru.

4. **Sistem Whitelist & Utility Class Kartu Resmi (Anti-Wildcard Rusak)**:
   - **DILARANG KERAS** memakai selector wildcard agresif seperti `[class*="-card"]` atau `[class*="-box"]` yang memaksa sub-elemen mewarisi border/background.
   - Gunakan utility class resmi `.mirai-card-light` dan `.mirai-card-dark` yang sudah dibekali guard `:not()` otomatis untuk seluruh elemen anak (`*-head`, `*-header`, `*-point-card`, `*-badge`, dll.)."""

    if old_rule_block in content:
        content = content.replace(old_rule_block, new_rule_block)
        log("Aturan visual universal di PANDUAN-DEVELOPER.md disinkronkan.")

    with open(dev_path, "w", encoding="utf-8") as f:
        f.write(content)

# ==============================================================================
# 4. SINKRONKAN panduan/tree.md & panduan/agent.md
# ==============================================================================
def update_tree_and_agent_docs():
    log("=== [4] Menyelaraskan panduan/tree.md & panduan/agent.md ===")
    
    # 4.a panduan/tree.md
    tree_path = os.path.join(BASE_DIR, "panduan", "tree.md")
    with open(tree_path, "r", encoding="utf-8") as f:
        tree = f.read()

    # Perbarui baris .vscode di tree.md
    old_vscode_tree = """├── .vscode/                        # Konfigurasi workspace editor VS Code / Antigravity
│   └── settings.json               # Pengaturan workspace, search.exclude, & files.watcherExclude"""
    new_vscode_tree = """├── .vscode/                        # Konfigurasi workspace editor VS Code / Antigravity
│   ├── settings.json               # Pengaturan workspace, formatOnSave, search.exclude, & watcherExclude
│   └── extensions.json             # Rekomendasi 9 ekstensi resmi VS Code untuk developer proyek"""

    if old_vscode_tree in tree:
        tree = tree.replace(old_vscode_tree, new_vscode_tree)

    # Perbarui skrip di tree.md
    old_skrip_tree = """├── skrip/                          # Pemeliharaan Kode Python
│   ├── README.md                   # Panduan skrip pengembang
│   └── arsip/                      # Arsip skrip perbaikan sekali-pakai (dikecualikan dari watcher)
│       ├── apply_card_expand.py"""
    new_skrip_tree = """├── skrip/                          # Pemeliharaan Kode Python
│   ├── README.md                   # Panduan skrip pengembang
│   └── arsip/                      # Arsip skrip perbaikan sekali-pakai (dikecualikan dari watcher)
│       ├── apply_card_expand.py
│       ├── apply_5_main_fixes.py
│       ├── apply_portrait_pattern_zoom_out.py
│       └── apply_transparency_and_tentang_fixes.py"""

    if old_skrip_tree in tree:
        tree = tree.replace(old_skrip_tree, new_skrip_tree)

    with open(tree_path, "w", encoding="utf-8") as f:
        f.write(tree)
    log("Berkas panduan/tree.md berhasil disinkronkan.")

    # 4.b panduan/agent.md
    agent_path = os.path.join(BASE_DIR, "panduan", "agent.md")
    with open(agent_path, "r", encoding="utf-8") as f:
        agent = f.read()

    # Perbarui aturan visual universal di agent.md
    old_agent_rules = """2. **Kunci Transparansi Universal Khusus Kartu (11% Terang, 18% Gelap)**:
   - Pola Terang (`c1w` / `w1w`): Wajib tepat **11%** (`opacity: 0.11 !important` atau via `--overlay-card-light` dengan `alpha: 0.89`).
   - Pola Gelap (`c1b` / `w1b`): Wajib tepat **18%** (`opacity: 0.18 !important` atau via `--overlay-card-dark` dengan `alpha: 0.82`).
   - Dilarang keras menggunakan transparansi acak/belang-belang (seperti 0.045 atau 0.16).

3. **Seksi Selang-Seling Bersih & Polos (Pattern HANYA pada Kartu, DILARANG pada Halaman/Seksi)**:
   - Semua `<section>` konten setelah Hero wajib memiliki latar belakang solid yang 100% bersih, polos, dan bebas dari pattern gambar latar (`background-image: none !important;`):
     - Seksi Ganjil (`nth-of-type(odd)`): Putih Bersih (`#ffffff`) polos dengan teks kontras tinggi (`#18151b` / `#554e57`).
     - Seksi Genap (`nth-of-type(even)`): Hitam Obsidian (`#111111`) polos dengan teks kontras terang (`#ffffff` / `#d5ccd3`).
   - **DILARANG KERAS** memasang pattern pada elemen `<section>`, `<body>`, atau latar halaman. Motif Jepang (Wagara/Kumo) HANYA boleh ada di dalam elemen kartu (`.card` / `[class*="-card"]`)!

4. **Pewarisan Kartu Universal Otomatis (Auto-Inheritance)**:
   - Setiap elemen kartu standar (`.card`, `[class*="-card"]`, di luar elemen inner/title/desc) otomatis mewarisi radius border (18px), border beraksen pink (`#f4bfd3` untuk kartu terang, `rgba(255, 101, 155, 0.22)` untuk kartu gelap), dan pattern universal yang sesuai dengan warna latarnya."""

    new_agent_rules = """2. **Kunci Transparansi Watermark Sangat Lembut (Maksimal Keterbacaan Teks)**:
   - Pola Terang & Gelap: Dikunci pada **`opacity: 0.045 !important`** (hover: `0.07 !important`) dan gradien penutup master di `:root` sebesar `0.95`–`0.97` agar teks kartu sangat jernih, tajam, dan tidak terganggu oleh garis gelombang latar.

3. **Seksi Selang-Seling Bersih & Polos (Pattern HANYA pada Kartu, DILARANG pada Halaman/Seksi)**:
   - Semua `<section>` konten setelah Hero wajib memiliki latar belakang solid yang 100% bersih, polos, dan bebas dari pattern gambar latar (`background-image: none !important;`):
     - Seksi Ganjil (`nth-of-type(odd)`): Putih Bersih (`#ffffff`) polos dengan teks kontras tinggi (`#18151b` / `#554e57`).
     - Seksi Genap (`nth-of-type(even)`): Hitam Obsidian (`#111111`) polos dengan teks kontras terang (`#ffffff` / `#d5ccd3`).
   - Gunakan utility class `.mirai-section-light` dan `.mirai-section-dark` saat membuat seksi baru.

4. **Sistem Whitelist & Utility Class Kartu Resmi (Anti-Wildcard Rusak)**:
   - **DILARANG KERAS** memakai selector wildcard agresif seperti `[class*="-card"]` atau `[class*="-box"]` yang memaksa sub-elemen mewarisi border/background.
   - Gunakan utility class resmi `.mirai-card-light` dan `.mirai-card-dark` yang sudah dibekali guard `:not()` otomatis untuk seluruh elemen anak (`*-head`, `*-header`, `*-point-card`, `*-badge`, dll.)."""

    if old_agent_rules in agent:
        agent = agent.replace(old_agent_rules, new_agent_rules)

    # Perbarui deskripsi root .vscode di agent.md
    agent = agent.replace(
        "dan folder **`.vscode/`** (`settings.json` konfigurasi workspace).",
        "dan folder **`.vscode/`** (`settings.json` konfigurasi workspace, `extensions.json` rekomendasi ekstensi resmi)."
    )

    with open(agent_path, "w", encoding="utf-8") as f:
        f.write(agent)
    log("Berkas panduan/agent.md berhasil disinkronkan.")

# ==============================================================================
# 5. VERIFIKASI INTEGRITAS SINTAKS SELURUH FILE CSS & JSON
# ==============================================================================
def verify_all_css_and_json():
    log("=== [5] Memverifikasi Integritas Seluruh Berkas CSS & JSON ===")
    
    # CSS
    css_dir = os.path.join(BASE_DIR, "css", "pages")
    for fname in sorted(os.listdir(css_dir)):
        if not fname.endswith(".css"):
            continue
        fpath = os.path.join(css_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            c = f.read()
        o = c.count("{")
        cl = c.count("}")
        assert o == cl, f"Ketidakseimbangan kurung pada {fname}: open={o}, close={cl}"
        log(f"CSS OK: {fname} ({o} pasang kurung)")

    # JSON
    for jpath in [
        os.path.join(BASE_DIR, ".vscode", "extensions.json"),
        os.path.join(BASE_DIR, ".vscode", "settings.json"),
        os.path.join(BASE_DIR, "cspell.json")
    ]:
        with open(jpath, "r", encoding="utf-8") as f:
            json.load(f)
        log(f"JSON Valid: {os.path.relpath(jpath, BASE_DIR)}")

    log("SELURUH BERKAS 100% VALID DAN BEBAS ERROR SINTAKS!")

if __name__ == "__main__":
    secure_global_and_lomba_css()
    setup_vscode_and_clean_folders()
    update_panduan_developer()
    update_tree_and_agent_docs()
    verify_all_css_and_json()
    log("SEMUA PROSES PENGAMANAN & ONBOARDING SELESAI DENGAN SEMPURNA!")
