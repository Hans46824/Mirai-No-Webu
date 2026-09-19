import os
import glob

target_dir = '/home/hans/Mirai-No-Webu'
old_text = '<p class="sidebar-footer-desc">Website Materi Klub/Ekstrakurikuler Jepang &quot;MIRAI NO HANA&quot; SMASYIMDUTA Sidoarjo.<br><br><span class="sidebar-footer-sub">*Website ini dikelola oleh kepengurusan Klub/Ekstrakurikuler Jepang &quot;MIRAI NO HANA&quot; dan tidak ada campur tangan oleh pihak sekolah.</span></p>'
new_text = '<p class="sidebar-footer-desc">Website Materi Klub Jepang MIRAI NO HANA SMASYIMDUTA Sidoarjo.<br><br><span class="sidebar-footer-sub">Website ini dikelola oleh kepengurusan Klub Jepang MIRAI NO HANA dan tidak ada campur tangan oleh pihak sekolah.</span></p>'

html_files = glob.glob(os.path.join(target_dir, '*.html'))

count = 0
for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_text in content:
        content = content.replace(old_text, new_text)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1

print(f"Replaced text in {count} files.")
