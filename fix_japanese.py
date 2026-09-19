with open('/home/hans/Mirai-No-Webu/index.html', 'r') as f:
    content = f.read()

old = '<p class="hero-subtitle">ようこそ</p>'
new = '<p class="hero-subtitle" style="font-size: clamp(2rem, 5vw, 4rem); font-weight: 800; letter-spacing: 0px; color: #fff; margin-bottom: 5px; text-shadow: 2px 4px 10px rgba(0,0,0,0.5);">ようこそ</p>'

content = content.replace(old, new)

with open('/home/hans/Mirai-No-Webu/index.html', 'w') as f:
    f.write(content)
