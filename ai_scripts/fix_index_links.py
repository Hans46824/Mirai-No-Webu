with open('/home/hans/Mirai-No-Webu/index.html', 'r') as f:
    content = f.read()

content = content.replace('href="kelas-dasar.html"', 'href="kelas.html#dasar"')
content = content.replace('href="kelas-lanjutan.html"', 'href="kelas.html#lanjutan"')

with open('/home/hans/Mirai-No-Webu/index.html', 'w') as f:
    f.write(content)
