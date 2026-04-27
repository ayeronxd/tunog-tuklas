import re

with open(r"c:\Users\User\OneDrive\Desktop\tunog-tuklas\core\templates\core\letrang_b.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update totalUnits and UNIT_NAMES
html = re.sub(
    r"const UNIT_NAMES = \['Kilalanin Natin', 'Pagsulat ng Bb'\];",
    r"const UNIT_NAMES = ['Kilalanin Natin', 'Pagsulat ng Bb', 'Pagsasanay 1 A at B', 'Pagsasanay 1 C'];",
    html
)
html = re.sub(
    r"const totalUnits = 2;",
    r"const totalUnits = 4;",
    html
)
html = re.sub(
    r"const state = \{\n\s*1: \{ checked: false, score: 0 \},   // Pagsulat ng Bb\n\s*\};",
    r"const state = {\n                1: { checked: false, score: 0 },   // Pagsulat ng Bb\n                2: { checked: false, score: 0 },   // Pagsasanay 1 A at B\n                3: { checked: false, score: 0 },   // Pagsasanay 1 C\n            };",
    html
)

# 2. Add Unit 3 and Unit 4 HTML after Unit 1
unit3_html = """
            <!-- ═══════════════════════════════════════════
             UNIT 3: Pagsasanay 1 A at B
        ═══════════════════════════════════════════ -->
            <div class="unit-slide" id="unit-2">
                <div class="section-card">
                    <div class="section-badge badge-orange">📝 Pagsasanay 1</div>
                    <h2 class="activity-title mt-3" style="color:var(--orange);">A. Sumulat ng walong (8) malalaking B.</h2>
                    
                    <!-- Act3A (8 B's) -->
                    <div class="draw-pad-wrapper">
                        <div class="canvas-frame" id="frameAct3a" style="margin-top:14px;">
                            <div class="canvas-ghost" id="ghostAct3a" style="gap: 5%; font-size: 4rem;">
                                <span class="ghost-letter">B</span><span class="ghost-letter">B</span><span class="ghost-letter">B</span><span class="ghost-letter">B</span><span class="ghost-letter">B</span><span class="ghost-letter">B</span><span class="ghost-letter">B</span><span class="ghost-letter">B</span>
                            </div>
                            <canvas id="canvasAct3a" height="150"></canvas>
                        </div>
                        <div class="pad-toolbar">
                            <button class="pad-tool-btn undo-btn" onclick="undoStroke('act3a')">↩ Burahin huli</button>
                            <button class="pad-tool-btn erase" onclick="clearCanvas('act3a')">🗑 I-clear</button>
                            <button class="pad-tool-btn done-draw" onclick="markDone('act3a')">✓ Tapos na!</button>
                        </div>
                        <div class="color-row">
                            <span style="font-size:0.8rem;font-weight:800;color:#aaa;">Kulay:</span>
                            <div class="color-swatch active" style="background:#4D96FF;" onclick="setColor('act3a','#4D96FF',this)"></div>
                            <div class="color-swatch" style="background:#FF6B9D;" onclick="setColor('act3a','#FF6B9D',this)"></div>
                            <div class="color-swatch" style="background:#6BCB77;" onclick="setColor('act3a','#6BCB77',this)"></div>
                            <div class="color-swatch" style="background:#2C2F33;" onclick="setColor('act3a','#2C2F33',this)"></div>
                        </div>
                        <div class="brush-row">
                            <span style="font-size:0.8rem;font-weight:800;color:#aaa;">Laki:</span>
                            <div class="brush-btn active" onclick="setBrush('act3a',5,this)"><div class="brush-dot" style="width:6px;height:6px;"></div></div>
                            <div class="brush-btn" onclick="setBrush('act3a',10,this)"><div class="brush-dot" style="width:11px;height:11px;"></div></div>
                        </div>
                        <div class="pad-done-tick" id="doneTick-act3a">✅ Mahusay!</div>
                    </div>

                    <h2 class="activity-title mt-4" style="color:var(--pink);">B. Sumulat ng sampung (10) maliliit na b.</h2>
                    <!-- Act3B (10 b's) -->
                    <div class="draw-pad-wrapper">
                        <div class="canvas-frame" id="frameAct3b" style="margin-top:14px;">
                            <div class="canvas-ghost" id="ghostAct3b" style="gap: 4%; font-size: 3.5rem;">
                                <span class="ghost-letter">b</span><span class="ghost-letter">b</span><span class="ghost-letter">b</span><span class="ghost-letter">b</span><span class="ghost-letter">b</span><span class="ghost-letter">b</span><span class="ghost-letter">b</span><span class="ghost-letter">b</span><span class="ghost-letter">b</span><span class="ghost-letter">b</span>
                            </div>
                            <canvas id="canvasAct3b" height="150"></canvas>
                        </div>
                        <div class="pad-toolbar">
                            <button class="pad-tool-btn undo-btn" onclick="undoStroke('act3b')">↩ Burahin huli</button>
                            <button class="pad-tool-btn erase" onclick="clearCanvas('act3b')">🗑 I-clear</button>
                            <button class="pad-tool-btn done-draw" onclick="markDone('act3b')">✓ Tapos na!</button>
                        </div>
                        <div class="color-row">
                            <span style="font-size:0.8rem;font-weight:800;color:#aaa;">Kulay:</span>
                            <div class="color-swatch" style="background:#4D96FF;" onclick="setColor('act3b','#4D96FF',this)"></div>
                            <div class="color-swatch active" style="background:#FF6B9D;" onclick="setColor('act3b','#FF6B9D',this)"></div>
                            <div class="color-swatch" style="background:#6BCB77;" onclick="setColor('act3b','#6BCB77',this)"></div>
                            <div class="color-swatch" style="background:#2C2F33;" onclick="setColor('act3b','#2C2F33',this)"></div>
                        </div>
                        <div class="brush-row">
                            <span style="font-size:0.8rem;font-weight:800;color:#aaa;">Laki:</span>
                            <div class="brush-btn active" onclick="setBrush('act3b',5,this)"><div class="brush-dot" style="width:6px;height:6px;"></div></div>
                            <div class="brush-btn" onclick="setBrush('act3b',10,this)"><div class="brush-dot" style="width:11px;height:11px;"></div></div>
                        </div>
                        <div class="pad-done-tick" id="doneTick-act3b">✅ Magaling!</div>
                    </div>
                </div>
            </div>

            <!-- ═══════════════════════════════════════════
             UNIT 4: Pagsasanay 1 C
        ═══════════════════════════════════════════ -->
            <div class="unit-slide" id="unit-3">
                <div class="section-card">
                    <div class="section-badge badge-green">📝 Pagsasanay 1 C</div>
                    <h2 class="activity-title mt-3" style="color:var(--green);">C. Pagsamahin sa guhit ang apat (4) malaki at maliit na letrang Bb.</h2>
                    <p class="activity-instruction">Isulat ang magkatabing <strong>Bb</strong> nang apat na beses.</p>

                    <!-- Act4C (4 Bb's -> 8 letters) -->
                    <div class="draw-pad-wrapper">
                        <div class="canvas-frame" id="frameAct4c" style="margin-top:14px;">
                            <div class="canvas-ghost" id="ghostAct4c" style="gap: 5%; font-size: 4rem;">
                                <span class="ghost-letter" style="color:var(--blue)">B</span><span class="ghost-letter" style="color:var(--pink)">b</span>
                                <span class="ghost-letter" style="color:var(--blue)">B</span><span class="ghost-letter" style="color:var(--pink)">b</span>
                                <span class="ghost-letter" style="color:var(--blue)">B</span><span class="ghost-letter" style="color:var(--pink)">b</span>
                                <span class="ghost-letter" style="color:var(--blue)">B</span><span class="ghost-letter" style="color:var(--pink)">b</span>
                            </div>
                            <canvas id="canvasAct4c" height="150"></canvas>
                        </div>
                        <div class="pad-toolbar">
                            <button class="pad-tool-btn undo-btn" onclick="undoStroke('act4c')">↩ Burahin huli</button>
                            <button class="pad-tool-btn erase" onclick="clearCanvas('act4c')">🗑 I-clear</button>
                            <button class="pad-tool-btn done-draw" onclick="markDone('act4c')">✓ Tapos na!</button>
                        </div>
                        <div class="color-row" style="display:none;"></div>
                        <div class="brush-row">
                            <span style="font-size:0.8rem;font-weight:800;color:#aaa;">Laki:</span>
                            <div class="brush-btn active" onclick="setBrush('act4c',5,this)"><div class="brush-dot" style="width:6px;height:6px;"></div></div>
                            <div class="brush-btn" onclick="setBrush('act4c',10,this)"><div class="brush-dot" style="width:11px;height:11px;"></div></div>
                        </div>
                        <div class="pad-done-tick" id="doneTick-act4c">✅ Magaling!</div>
                    </div>
                </div>
            </div>
"""
# Insert before `</div><!-- end units-track -->`
if "unit-3" not in html:
    html = html.replace('</div><!-- end units-track -->', unit3_html + '\n        </div><!-- end units-track -->')

# 3. Patch JS logic
html = re.sub(
    r"\('canvas' \+ \(id === 'upper' \? 'Upper' \: 'Lower'\)\)",
    r"('canvas' + id.charAt(0).toUpperCase() + id.slice(1))",
    html
)
html = re.sub(
    r"\('frame' \+ \(id === 'upper' \? 'Upper' \: 'Lower'\)\)",
    r"('frame' + id.charAt(0).toUpperCase() + id.slice(1))",
    html
)
html = re.sub(
    r"\('ghost' \+ \(id === 'upper' \? 'Upper' \: 'Lower'\)\)",
    r"('ghost' + id.charAt(0).toUpperCase() + id.slice(1))",
    html
)
html = re.sub(
    r"color: id === 'upper' \? '#4D96FF' : '#FF6B9D',",
    r"color: (id === 'upper' || id === 'act3a') ? '#4D96FF' : (id === 'lower' || id === 'act3b') ? '#FF6B9D' : '#6BCB77',",
    html
)
html = re.sub(
    r"maxStrokes: id === 'upper' \? 4 : 3,",
    r"maxStrokes: (id === 'upper' ? 4 : (id === 'lower' ? 3 : 20)),",
    html
)

html = re.sub(
    r"tick\.innerHTML = id === 'upper' \? '✅ Napakahusay\! Sinulatan mo na ang malaking B\!' : '✅ Magaling\! Sinulatan mo na ang maliit na b\!';\n\s*tick\.scrollIntoView\(\{ behavior: 'smooth', block: 'nearest' \}\);",
    r"""tick.innerHTML = id === 'upper' ? '✅ Napakahusay! Sinulatan mo na ang malaking B!' : id === 'lower' ? '✅ Magaling! Sinulatan mo na ang maliit na b!' : '✅ Mahusay! Natapos mo ang pagsasanay!';
                tick.scrollIntoView({ behavior: 'smooth', block: 'nearest' });""",
    html
)

# 4. Patch completion logic for Units 2 and 3
html = re.sub(
    r"if \(pads\['upper'\]\.done && pads\['lower'\]\.done && !state\[1\]\.checked\) \{\n([ \t]*state\[1\].*?\n[ \t]*).*?launchConfetti\(\);\n\s*\}\n\s*updateNextBtn\(\);",
    r"""if (pads['upper'].done && pads['lower'].done && !state[1].checked) {\n\1launchConfetti();\n                }
                if (pads['act3a']?.done && pads['act3b']?.done && !state[2].checked) {
                    state[2].checked = true; state[2].score = 1;
                    const cur = parseInt(document.getElementById('starCount').textContent);
                    document.getElementById('starCount').textContent = cur + 1;
                    launchConfetti();
                }
                if (pads['act4c']?.done && !state[3].checked) {
                    state[3].checked = true; state[3].score = 1;
                    const cur = parseInt(document.getElementById('starCount').textContent);
                    document.getElementById('starCount').textContent = cur + 1;
                    launchConfetti();
                }
                updateNextBtn();""",
    html, flags=re.DOTALL
)

# 5. Add initPad for new units
html = re.sub(
    r"initPad\('upper'\);\n\s*initPad\('lower'\);",
    r"initPad('upper');\n            initPad('lower');\n            initPad('act3a');\n            initPad('act3b');\n            initPad('act4c');",
    html
)

# 6. Update allActivitiesDone function to include states 2 and 3
html = re.sub(
    r"function allActivitiesDone\(\) \{\s*return state\[1\]\.checked;\s*\}",
    r"function allActivitiesDone() { \n                return state[1].checked && state[2].checked && state[3].checked;\n            }",
    html
)

# 7. Update skip functionality to mark correct ones
html = re.sub(
    r"if \(currentUnit === 1\) state\[1\]\.checked = true;\n\s*if \(currentUnit === 2\) state\[2\]\.checked = true;\n\s*if \(currentUnit === 3\) state\[4\]\.checked = true;",
    r"if (currentUnit === 1) state[1].checked = true;\n                    if (currentUnit === 2) state[2].checked = true;\n                    if (currentUnit === 3) state[3].checked = true;",
    html
)

with open(r"c:\Users\User\OneDrive\Desktop\tunog-tuklas\core\templates\core\letrang_b.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Updated letrang_b.html")
