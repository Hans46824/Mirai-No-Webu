# 📝 Daftar Kanji yang Memerlukan Terjemahan Bahasa Indonesia

> Dokumen ini memuat daftar Kanji yang nilai artinya (`meaning`) masih sama persis dengan arti Bahasa Inggris (`meaningEn`).
> Sesuai pedoman pengembangan, asisten AI **DILARANG menebak** terjemahan ini.
> Silakan pengurus / pengembang klub mengisi kolom rekomendasi terjemahan di bawah ini secara manual.

**Total Karakter yang Perlu Diterjemahkan**: 6 karakter

| No | Kanji | Unicode | JLPT | Goresan | Onyomi | Kunyomi | Arti Inggris Saat Ini | Contoh Kata | Rekomendasi Terjemahan Indonesia |
| :---: | :---: | :---: | :---: | :---: | :--- | :--- | :--- | :--- | :--- |
| 1 | **反** | `U+53CD` | **N3** | 4 | タン, ハン, ホ, ホン | -かえ.る, かえ.す, かえ.る, そ.らす, そ.る | `Anti-` | 反 (はん)<br>反り (そり) | *(Diisi manual oleh pengurus)* |
| 2 | **柊** | `U+67CA` | **N1** | 9 | シュ, シュウ | ひいらぎ | `Holly` | 柊 (ひいらぎ) | *(Diisi manual oleh pengurus)* |
| 3 | **桐** | `U+6850` | **N1** | 10 | トウ, ドウ | きり | `Paulownia` | 桐 (きり) | *(Diisi manual oleh pengurus)* |
| 4 | **楓** | `U+6953` | **N1** | 13 | フウ | かえで | `Maple` | 楓 (かえで) | *(Diisi manual oleh pengurus)* |
| 5 | **瑠** | `U+7460` | **N1** | 14 | リュウ, ル | - | `Lapis Lazuli` | 瑠璃 (るり) | *(Diisi manual oleh pengurus)* |
| 6 | **藤** | `U+85E4` | **N1** | 18 | トウ, ドウ | ふじ | `Wisteria` | 藤 (ふじ) | *(Diisi manual oleh pengurus)* |

---
### Catatan Panduan Pengurus:
1. Setelah Anda menentukan terjemahan yang tepat untuk ke-6 kanji di atas, perbarui nilai field `"meaning"` pada kanji terkait di `data/kanji.json`.
2. Jalankan `python3 skrip/arsip/build_data_chunks.py` untuk menyinkronkan kembali chunk data lokal kamus.
