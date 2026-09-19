with open('/home/hans/Mirai-No-Webu/tentang.html', 'r') as f:
    content = f.read()

old = '<div style="width: 100%; height: 100%; overflow-x: auto; overflow-y: hidden; display: block; white-space: nowrap; font-size: 0;">'
new = '<style>.no-scroll-bar::-webkit-scrollbar { display: none; } .no-scroll-bar { -ms-overflow-style: none; scrollbar-width: none; }</style>\n                    <div class="no-scroll-bar" style="width: 100%; height: 100%; overflow-x: auto; overflow-y: hidden; display: block; white-space: nowrap; font-size: 0; scroll-behavior: smooth; cursor: grab;" onmousedown="this.style.cursor=\'grabbing\';" onmouseup="this.style.cursor=\'grab\';">'

content = content.replace(old, new)
with open('/home/hans/Mirai-No-Webu/tentang.html', 'w') as f:
    f.write(content)
