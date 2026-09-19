with open('/home/hans/Mirai-No-Webu/kelas.html', 'r') as f:
    content = f.read()

content = content.replace('<section class="section learning-path"><p class="kicker">KELAS DASAR</p>', '<section class="section learning-path" id="dasar"><p class="kicker">KELAS DASAR</p>')
content = content.replace('<section class="section learning-path soft-section"><p class="kicker">KELAS LANJUTAN</p>', '<section class="section learning-path soft-section" id="lanjutan"><p class="kicker">KELAS LANJUTAN</p>')

with open('/home/hans/Mirai-No-Webu/kelas.html', 'w') as f:
    f.write(content)
print("Updated kelas.html")
