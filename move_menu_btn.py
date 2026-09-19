import os
import glob

base = '/home/hans/Mirai-No-Webu/'
html_files = glob.glob(os.path.join(base, '*.html'))

for fpath in html_files:
    with open(fpath, 'r') as f:
        content = f.read()
    
    if '<button class="menu-btn"' in content and '<header' in content:
        # Find the header block
        header_start = content.find('<header class="home-header">')
        if header_start != -1:
            header_end = content.find('</header>', header_start)
            if header_end != -1:
                header_block = content[header_start:header_end + len('</header>')]
                
                # If menu-btn is in header, remove it from header and put it right after header
                if '<button class="menu-btn"' in header_block:
                    import re
                    # Extract the menu-btn string
                    match = re.search(r'<button class="menu-btn"[^>]*>.*?</button>', header_block)
                    if match:
                        btn_str = match.group(0)
                        # Remove it from header
                        new_header_block = header_block.replace(btn_str, '')
                        # Put it after header
                        new_header_and_btn = new_header_block + '\n    ' + btn_str
                        content = content.replace(header_block, new_header_and_btn)
                        with open(fpath, 'w') as f:
                            f.write(content)
                        print(f"Moved menu-btn in {os.path.basename(fpath)}")
