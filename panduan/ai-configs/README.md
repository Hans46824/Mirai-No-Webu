# Konfigurasi AI Assistant (Cursor, Copilot, Claude, Codex)

Folder ini menyimpan berkas aturan instruksi otomatis (*AI rules & system prompts*) untuk editor dan asisten cerdas yang digunakan oleh pengembang Mirai no Webu:

## Berkas yang Tersedia:
1. **`.cursorrules`**: Konfigurasi otomatis untuk editor **Cursor AI**. Jika Anda menggunakan Cursor, salin berkas ini ke *root* direktori proyek atau ke `.cursor/rules/`.
2. **`copilot-instructions.md`**: Konfigurasi instruksi sistem untuk **GitHub Copilot**. Jika Anda menggunakan ekstensi Copilot di VS Code atau GitHub, salin berkas ini ke `.github/copilot-instructions.md`.
3. **Claude Code / CLAUDE.md**: Jika menggunakan Claude Code CLI, Anda dapat merujuk atau menautkan aturan dari `panduan/agent.md` atau berkas ini.
4. **Antigravity AI**: Pengguna Google Antigravity secara otomatis membaca `panduan/agent.md` dan `panduan/CONTEKAN-TAG.md` sebagai sumber kebenaran tunggal (*Single Source of Truth*).

> [!NOTE]
> Berkas-berkas ini disimpan di folder `panduan/ai-configs/` agar *root* direktori proyek tetap bersih (*Clean Root Standard*) dan memudahkan pengurus klub dalam memelihara struktur repositori.
