with open('/home/hans/Mirai-No-Webu/tentang.html', 'r') as f:
    content = f.read()

old = '''                <article class="accessory-card">
                    <div class="accessory-thumb-wrap is-pin-wrap">
                        <img src="images/mirai/identitas/pin-clean.png" alt="Pin Enamel Logo NK" class="pin-full-img">
                    </div>
                    <h3>Pin Logo NK</h3>
                    <p>Pin bulat berhiaskan logo bunga sakura dan identitas SMA Wachid Hasyim 2.</p>
                </article>
            </div>'''

new = '''                <article class="accessory-card">
                    <div class="accessory-thumb-wrap is-pin-wrap">
                        <img src="images/mirai/identitas/pin-clean.png" alt="Pin Enamel Logo NK" class="pin-full-img">
                    </div>
                    <h3>Pin Logo NK</h3>
                    <p>Pin bulat berhiaskan logo bunga sakura dan identitas SMA Wachid Hasyim 2.</p>
                </article>

                <article class="accessory-card">
                    <div class="accessory-thumb-wrap">
                        <img src="images/mirai/identitas/nametag-katakana.jpeg" alt="Nametag Katakana">
                    </div>
                    <h3>Nametag Katakana</h3>
                    <p>Papan nama dengan tulisan nama anggota dalam huruf Katakana sebagai identitas klub.</p>
                </article>
            </div>'''

content = content.replace(old, new)

with open('/home/hans/Mirai-No-Webu/tentang.html', 'w') as f:
    f.write(content)
