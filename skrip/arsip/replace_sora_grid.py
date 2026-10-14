import re

with open('/home/hans/Mirai-No-Webu/tentang.html', 'r') as f:
    content = f.read()

start_marker = '<div class="sora-grid">'
end_marker = '</div>\n        </section>\n\n        <!-- PAPAN PRESTASI'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_html = '''<div class="sora-full-carousel">
                <style>.no-scroll-bar::-webkit-scrollbar { display: none; } .no-scroll-bar { -ms-overflow-style: none; scrollbar-width: none; }</style>
                <div class="no-scroll-bar" style="width: 100%; height: 500px; max-height: 70vh; border-radius: 22px; overflow-x: auto; overflow-y: hidden; display: block; white-space: nowrap; font-size: 0; box-shadow: 0 12px 35px rgba(233, 30, 99, 0.15); border: 2px solid var(--pink-border); scroll-behavior: smooth; cursor: grab;" onmousedown="this.style.cursor='grabbing';" onmouseup="this.style.cursor='grab';">
                    <img src="images/mirai/sora/soracarousel.png" alt="Profil Lengkap Asora Aokita" style="height: 100%; width: auto; max-width: none; display: inline-block;">
                </div>
            </div>'''
    
    content = content[:start_idx] + new_html + content[end_idx:]
    with open('/home/hans/Mirai-No-Webu/tentang.html', 'w') as f:
        f.write(content)
    print("Replaced successfully!")
else:
    print("Could not find boundaries")
