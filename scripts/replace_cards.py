import re

with open('/home/hans/Mirai-No-Webu/index.html', 'r') as f:
    content = f.read()

old_html = '<div class="start-grid"><a class="start-card" href="kelas.html"><img class="card-corner-chibi" src="images/mirai/icon/Al.png" alt=""><span>01</span><h3>Kelas Dasar</h3><p>Hiragana, katakana, dan fondasi belajar.</p><b>→</b></a><a class="start-card" href="kelas-lanjutan.html"><img class="card-corner-chibi" src="images/mirai/icon/Lo.png" alt=""><span>02</span><h3>Kelas Lanjutan</h3><p>Kanji dan pemahaman bahasa yang lebih dalam.</p><b>→</b></a><a class="start-card" href="kamus.html"><img class="card-corner-chibi" src="images/mirai/icon/Fu.png" alt=""><span>03</span><h3>Kamus</h3><p>Cari kana, kanji, arti, bacaan, dan contoh.</p><b>→</b></a></div>'

new_html = '''<div class="start-grid">
  <div class="start-card" tabindex="0">
    <div class="start-card-content">
      <img class="card-corner-chibi" src="images/mirai/icon/Al.png" alt="">
      <span>01</span>
      <h3>Kelas Dasar</h3>
      <p>Hiragana, katakana, dan fondasi belajar.</p>
      <b>→</b>
    </div>
    <div class="start-card-hover-menu">
      <a class="btn primary" href="kelas.html">Beranda Kelas</a>
      <a class="btn" href="latihan.html">Latihan Kana</a>
      <a class="btn" href="kamus.html?tab=hiragana">Kamus Hiragana</a>
      <a class="btn" href="kamus.html?tab=katakana">Kamus Katakana</a>
    </div>
  </div>
  <div class="start-card" tabindex="0">
    <div class="start-card-content">
      <img class="card-corner-chibi" src="images/mirai/icon/Lo.png" alt="">
      <span>02</span>
      <h3>Kelas Lanjutan</h3>
      <p>Kanji dan pemahaman bahasa yang lebih dalam.</p>
      <b>→</b>
    </div>
    <div class="start-card-hover-menu">
      <a class="btn primary" href="kelas-lanjutan.html">Beranda Kelas</a>
      <a class="btn" href="kamus.html?tab=kanji">Kamus Kanji</a>
      <a class="btn" href="materi/lanjutan/index.html">Materi Kanji</a>
    </div>
  </div>
  <div class="start-card" tabindex="0">
    <div class="start-card-content">
      <img class="card-corner-chibi" src="images/mirai/icon/Fu.png" alt="">
      <span>03</span>
      <h3>Kamus</h3>
      <p>Cari kana, kanji, arti, bacaan, dan contoh.</p>
      <b>→</b>
    </div>
    <div class="start-card-hover-menu">
      <a class="btn primary" href="kamus.html">Buka Kamus</a>
      <a class="btn" href="kamus.html?tab=hiragana">Hiragana</a>
      <a class="btn" href="kamus.html?tab=katakana">Katakana</a>
      <a class="btn" href="kamus.html?tab=kanji">Kanji</a>
    </div>
  </div>
</div>'''

if old_html in content:
    content = content.replace(old_html, new_html)
    with open('/home/hans/Mirai-No-Webu/index.html', 'w') as f:
        f.write(content)
    print("Replacement successful.")
else:
    print("Could not find the target HTML string.")
