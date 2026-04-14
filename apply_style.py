import sys
import re

filepath = 'core/templates/core/letrang_o.html'
with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the style block
old_style = """                        <style>
                            .manuscript-paper {
                                background: repeating-linear-gradient(
                                    transparent, transparent 25px,
                                    #82b1ff 26px, transparent 27px,
                                    transparent 50px, #ff8a80 51px,
                                    transparent 52px, transparent 75px,
                                    #82b1ff 76px, transparent 77px, transparent 100px
                                );
                                border-radius: 8px; position: relative; width: 100%; border: 1px solid #ddd; overflow: hidden;
                            }
                            .canvas-ghost.row-ghosts { flex-direction: row; flex-wrap: wrap; justify-content: space-evenly; align-content: center; gap: 15px; }
                        </style>"""

new_style = """                        <style>
                            .manuscript-paper {
                                background: repeating-linear-gradient(
                                    transparent, transparent 25px,
                                    #82b1ff 26px, transparent 27px,
                                    transparent 50px, #ff8a80 51px,
                                    transparent 52px, transparent 75px,
                                    #82b1ff 76px, transparent 77px, transparent 100px
                                );
                                border-radius: 8px; position: relative; width: 100%; border: 1px solid #ddd; overflow: hidden;
                            }
                            .manuscript-paper > .canvas-ghost {
                                width: 100%; height: 100%; display: flex; flex-direction: column; position: absolute; top:0; left:0; pointer-events: none;
                            }
                            .manuscript-paper .ghost-row {
                                width: 100%; height: 100px;
                                display: flex; flex-direction: row; justify-content: space-evenly; align-items: flex-end;
                            }
                            .manuscript-paper .ghost-letter {
                                font-family: 'Bubblegum Sans', cursive !important;
                                color: #e0e0e0;
                                opacity: 0.6;
                                line-height: 0.8 !important;
                                margin: 0;
                            }
                            .manuscript-paper .ghost-letter.big {
                                font-size: 5rem !important;
                                transform: translateY(-30px);
                            }
                            .manuscript-paper .ghost-letter.small {
                                font-size: 3.8rem !important;
                                transform: translateY(-26px);
                            }
                            .oo-group {
                                display: flex; align-items: baseline; gap: 6px;
                            }
                        </style>"""

if old_style in html:
    html = html.replace(old_style, new_style)
    print("Replaced style block.")
else:
    print("Could not find style block to replace.")

# 2. Add 'big' class to all uppercase ghost letters in Pagsasanay A
html = html.replace('<div class="ghost-row center">\n                                    <span class="ghost-letter">O</span><span class="ghost-letter">O</span><span class="ghost-letter">O</span><span class="ghost-letter">O</span>\n                                </div>', 
                    '<div class="ghost-row center">\n                                    <span class="ghost-letter big">O</span><span class="ghost-letter big">O</span><span class="ghost-letter big">O</span><span class="ghost-letter big">O</span>\n                                </div>')

html = html.replace('<div class="ghost-row center">\n                                    <span class="ghost-letter">O</span><span class="ghost-letter">O</span><span class="ghost-letter">O</span>\n                                </div>', 
                    '<div class="ghost-row center">\n                                    <span class="ghost-letter big">O</span><span class="ghost-letter big">O</span><span class="ghost-letter big">O</span>\n                                </div>')

# In Pagsasanay B
html = html.replace('<div class="ghost-row bottom">\n                                    <span class="ghost-letter">o</span><span class="ghost-letter">o</span><span class="ghost-letter">o</span><span class="ghost-letter">o</span>\n                                </div>',
                    '<div class="ghost-row bottom">\n                                    <span class="ghost-letter small">o</span><span class="ghost-letter small">o</span><span class="ghost-letter small">o</span><span class="ghost-letter small">o</span>\n                                </div>')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html)
print('Done styling')
