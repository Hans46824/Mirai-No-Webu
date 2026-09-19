import os

base = '/home/hans/Mirai-No-Webu/'

# 1. kelas.html
with open(base + 'kelas.html', 'r') as f:
    c = f.read()
old = '<p class="eyebrow">MIRAI NO HANA / RUANG BELAJAR</p>\n<h1 class="page-title">Mulai<br><span>perjalananmu.</span>\n</h1>\n<p class="class-hero-copy">Pilih kelas yang sesuai dengan langkahmu, lalu belajar sedikit demi sedikit.</p>'
new = '<h1 class="page-title">Kelas<br><span>belajar</span>\n</h1>'
c = c.replace(old, new)
with open(base + 'kelas.html', 'w') as f:
    f.write(c)

# 2. kegiatan.html
with open(base + 'kegiatan.html', 'r') as f:
    c = f.read()
old = '<p class="eyebrow">MIRAI NO HANA / ORGANISASI</p>\n      <h1 class="page-title">Belajar, berkarya,<br><span>dan membuat cerita.</span></h1>\n      <p>Kegiatan adalah ruang untuk menerapkan rasa ingin tahu di luar materi kelas dan membangun klub bersama-sama.</p>'
new = '<h1 class="page-title">Kegiatan<br><span>Mirai no hana</span></h1>'
c = c.replace(old, new)
with open(base + 'kegiatan.html', 'w') as f:
    f.write(c)

# 3. tentang.html
with open(base + 'tentang.html', 'r') as f:
    c = f.read()
old = '<p class="eyebrow">TENTANG KAMI</p>\n                <h1 class="page-title">MIRAI NO HANA<br><span>NIHONGO KURABU</span></h1>'
new = '<h1 class="page-title">Tentang Klub<br><span>jepang kami</span></h1>'
c = c.replace(old, new)
with open(base + 'tentang.html', 'w') as f:
    f.write(c)

# 4. kamus.html
with open(base + 'kamus.html', 'r') as f:
    c = f.read()
old = '<p class="eyebrow">MIRAI NO HANA / KAMUS BELAJAR</p>\n<h1 class="page-title">Kamus<br><span>Jepang.</span>\n</h1>'
new = '<h1 class="page-title">Kamus<br><span>Jepang.</span>\n</h1>'
c = c.replace(old, new)
with open(base + 'kamus.html', 'w') as f:
    f.write(c)

# 5. index.html
with open(base + 'index.html', 'r') as f:
    c = f.read()
old = '<p class="hero-subtitle">SELAMAT DATANG DI</p>\n                <h1 class="hero-title">MIRAI NO WEBU</h1>'
new = '<h1 class="hero-title">MIRAI NO <span>WEBU</span></h1>'
# Wait, user said "yg beranda udh bagus jgn di usik oh ya beranda cukup di warani aja teksnya". Let's keep the subtitle just in case they meant only the title needed coloring and to leave the rest of beranda alone.
# No, they said "tetap semuanya di ahpus text mini jadi sasintext judlu besar pada backgorund ajaaa"
c = c.replace(old, new)
with open(base + 'index.html', 'w') as f:
    f.write(c)

print("Heroes updated.")
