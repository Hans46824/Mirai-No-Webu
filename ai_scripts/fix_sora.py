with open('/home/hans/Mirai-No-Webu/tentang.html', 'r') as f:
    content = f.read()

old = '''                <div class="sora-visual-card">
                    <span class="sora-visual-badge">★ SSR MASKOT RESMI</span>
                    <img src="images/mirai/background/Sora.png" alt="Asora Aokita (Sora) - Maskot Resmi">
                </div>'''

new = '''                <div class="sora-visual-card" style="position: relative;">
                    <span class="sora-visual-badge" style="z-index: 10;">★ SSR MASKOT RESMI</span>
                    <div style="width: 100%; height: 100%; overflow-x: auto; overflow-y: hidden; display: block; white-space: nowrap; font-size: 0;">
                        <img src="images/mirai/sora/soracarousel.png" alt="Asora Aokita (Sora) - Maskot Resmi" style="height: 100%; width: auto; max-width: none; display: inline-block;">
                    </div>
                </div>'''

content = content.replace(old, new)

with open('/home/hans/Mirai-No-Webu/tentang.html', 'w') as f:
    f.write(content)
