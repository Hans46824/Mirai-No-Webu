with open('/home/hans/Mirai-No-Webu/index.html', 'r') as f:
    content = f.read()

old_html = '<h1 class="hero-title">MIRAI NO <span>WEBU</span></h1>'
new_html = '<p class="hero-subtitle">ようこそ</p>\n                <h1 class="hero-title"><span style="color: var(--pink);">MIRAI NO WEBU</span></h1>'

content = content.replace(old_html, new_html)

with open('/home/hans/Mirai-No-Webu/index.html', 'w') as f:
    f.write(content)

print("Updated index.html")
