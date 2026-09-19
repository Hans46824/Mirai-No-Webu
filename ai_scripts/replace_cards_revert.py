import re

with open('/home/hans/Mirai-No-Webu/index.html', 'r') as f:
    content = f.read()

start = content.find('<div class="start-grid">')
end = content.find('</section>', start) # Finds the end of the journey-section

new_html = '''<div class="start-grid"><a class="start-card" href="kelas-dasar.html"><img class="card-corner-chibi" src="images/mirai/icon/Al.png" alt=""><span>01</span><h3>Kelas Dasar</h3><p>Hiragana, katakana, dan fondasi belajar.</p><b>→</b></a><a class="start-card" href="kelas-lanjutan.html"><img class="card-corner-chibi" src="images/mirai/icon/Lo.png" alt=""><span>02</span><h3>Kelas Lanjutan</h3><p>Kanji dan pemahaman bahasa yang lebih dalam.</p><b>→</b></a><a class="start-card" href="kamus.html"><img class="card-corner-chibi" src="images/mirai/icon/Fu.png" alt=""><span>03</span><h3>Kamus</h3><p>Cari kana, kanji, arti, bacaan, dan contoh.</p><b>→</b></a></div>'''

if start != -1 and end != -1:
    # Notice that we want to keep the closing </div> of section if any, but the end is just the </section>
    content = content[:start] + new_html + content[end:]
    with open('/home/hans/Mirai-No-Webu/index.html', 'w') as f:
        f.write(content)
    print("Replacement successful.")
else:
    print("Could not find start-grid boundaries.")
