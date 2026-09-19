with open('/home/hans/Mirai-No-Webu/tentang.html', 'r') as f:
    content = f.read()

start_marker = '<div class="sora-full-carousel">'
end_marker = '</section>'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker, start_idx)

if start_idx != -1 and end_idx != -1:
    new_html = '''<div class="sora-full-carousel">
                <style>.no-scroll-bar::-webkit-scrollbar { display: none; } .no-scroll-bar { -ms-overflow-style: none; scrollbar-width: none; }</style>
                <div id="sora-scroll-box" class="no-scroll-bar" style="width: 100%; border-radius: 22px; overflow-x: auto; overflow-y: hidden; display: block; white-space: nowrap; font-size: 0; box-shadow: 0 12px 35px rgba(233, 30, 99, 0.15); border: 2px solid var(--pink-border); cursor: grab;">
                    <img src="images/mirai/sora/soracarousel.png" alt="Profil Lengkap Asora Aokita" style="width: max(100%, 1500px); height: auto; display: inline-block; pointer-events: none;">
                </div>
            </div>
            
            <script>
                const slider = document.getElementById('sora-scroll-box');
                let isDown = false;
                let startX;
                let scrollLeft;

                slider.addEventListener('mousedown', (e) => {
                    isDown = true;
                    slider.style.cursor = 'grabbing';
                    startX = e.pageX - slider.offsetLeft;
                    scrollLeft = slider.scrollLeft;
                });
                slider.addEventListener('mouseleave', () => {
                    isDown = false;
                    slider.style.cursor = 'grab';
                });
                slider.addEventListener('mouseup', () => {
                    isDown = false;
                    slider.style.cursor = 'grab';
                });
                slider.addEventListener('mousemove', (e) => {
                    if (!isDown) return;
                    e.preventDefault();
                    const x = e.pageX - slider.offsetLeft;
                    const walk = (x - startX) * 2; // Scroll-fast
                    slider.scrollLeft = scrollLeft - walk;
                });
            </script>
        '''
    
    content = content[:start_idx] + new_html + content[end_idx:]
    with open('/home/hans/Mirai-No-Webu/tentang.html', 'w') as f:
        f.write(content)
    print("Updated carousel with JS")
