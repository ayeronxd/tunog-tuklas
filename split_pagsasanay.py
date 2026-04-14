import os
import re

filepath = 'core/templates/core/letrang_o.html'
with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()

# Update Star Count limit
html = html.replace('<span id="starCount">0</span> / 5', '<span id="starCount">0</span> / 7')

# We need to find the specific block for Unit 2 (Pagsasanay)
# and replace it with three separate units.
# The current Unit 2 starts with: <div class="unit-slide" id="unit-2">
# and ends right before: <!-- ═══════════════════════════════════\n             UNIT 2: Gawain 1 – Starting /m/

start_marker = '<div class="unit-slide" id="unit-2">'
end_marker = '            <!-- ═══════════════════════════════════\n             UNIT 2: Gawain 1'

start_idx = html.find(start_marker)
end_idx = html.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Could not find the Pagsasanay block.")
    exit(1)

# New Pagsasanay HTML split into 3 units
new_pagsasanay = r"""            <!-- ===============================
             UNIT 2: Pagsasanay - Malaking O
            ================================ -->
            <div class="unit-slide" id="unit-2">
                <div class="section-card">
                    <div class="section-badge badge-purple">📝 Pagsasanay</div>
                    <div class="pagsasanay-label text-center mt-3" style="font-size: 1.5rem; font-weight: 700; color: #333; margin-bottom: 5px;">A. Sumulat ng pitong (7) malalaking O.</div>
                    
                    <div class="draw-pad-wrapper" style="margin-top:20px;">
                        <style>
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
                        </style>
                        <div class="manuscript-paper" id="frameExA" style="height: 200px;">
                            <div class="canvas-ghost" id="ghostExA" style="flex-direction: column;">
                                <div class="ghost-row center">
                                    <span class="ghost-letter">O</span><span class="ghost-letter">O</span><span class="ghost-letter">O</span><span class="ghost-letter">O</span>
                                </div>
                                <div class="ghost-row center">
                                    <span class="ghost-letter">O</span><span class="ghost-letter">O</span><span class="ghost-letter">O</span>
                                </div>
                            </div>
                            <canvas id="canvasExA" class="coloring-canvas" height="200" style="width: 100%; height: 100%; position: absolute; top:0; left:0; z-index: 2;"></canvas>
                        </div>

                        <!-- Toolbar -->
                        <div class="pad-toolbar mt-3">
                            <button class="pad-tool-btn undo-btn" onclick="undoStroke('exA')">↩ Burahin huli</button>
                            <button class="pad-tool-btn erase" onclick="clearCanvas('exA')">🗑 I-clear</button>
                            <button class="pad-tool-btn done-draw" onclick="markDone('exA')">✓ Tapos na!</button>
                        </div>
                        <div class="color-row">
                            <span style="font-size:0.8rem;font-weight:800;color:#aaa;">Kulay:</span>
                            <div class="color-swatch active" style="background:#4A90E2;" onclick="setColor('exA','#4D96FF',this)"></div>
                            <div class="color-swatch" style="background:#F44336;" onclick="setColor('exA','#FF6B9D',this)"></div>
                            <div class="color-swatch" style="background:#4CAF50;" onclick="setColor('exA','#6BCB77',this)"></div>
                            <div class="color-swatch" style="background:#FF9F43;" onclick="setColor('exA','#FF9F43',this)"></div>
                            <div class="color-swatch" style="background:#C77DFF;" onclick="setColor('exA','#C77DFF',this)"></div>
                            <div class="color-swatch" style="background:#2C2F33;" onclick="setColor('exA','#2C2F33',this)"></div>
                        </div>
                        <div class="brush-row">
                            <span style="font-size:0.8rem;font-weight:800;color:#aaa;">Laki ng panulat:</span>
                            <div class="brush-btn active" onclick="setBrush('exA',5,this)"><div class="brush-dot" style="width:6px;height:6px;"></div></div>
                            <div class="brush-btn" onclick="setBrush('exA',10,this)"><div class="brush-dot" style="width:11px;height:11px;"></div></div>
                            <div class="brush-btn" onclick="setBrush('exA',18,this)"><div class="brush-dot" style="width:18px;height:18px;"></div></div>
                        </div>
                        <div class="pad-done-tick" id="doneTick-exA">✅ Napakahusay! Sinulatan mo na lahat ng malaking O!</div>
                    </div>
                </div>
            </div>

            <!-- ===============================
             UNIT 3: Pagsasanay - Maliit na o
            ================================ -->
            <div class="unit-slide" id="unit-3">
                <div class="section-card">
                    <div class="section-badge badge-purple">📝 Pagsasanay</div>
                    <div class="pagsasanay-label text-center mt-3" style="font-size: 1.5rem; font-weight: 700; color: #333; margin-bottom: 5px;">B. Sumulat ng walong (8) maliliit na o.</div>
                    
                    <div class="draw-pad-wrapper" style="margin-top:20px;">
                        <div class="manuscript-paper" id="frameExB" style="height: 200px;">
                            <div class="canvas-ghost" id="ghostExB" style="flex-direction: column;">
                                <div class="ghost-row bottom">
                                    <span class="ghost-letter">o</span><span class="ghost-letter">o</span><span class="ghost-letter">o</span><span class="ghost-letter">o</span>
                                </div>
                                <div class="ghost-row bottom">
                                    <span class="ghost-letter">o</span><span class="ghost-letter">o</span><span class="ghost-letter">o</span><span class="ghost-letter">o</span>
                                </div>
                            </div>
                            <canvas id="canvasExB" class="coloring-canvas" height="200" style="width: 100%; height: 100%; position: absolute; top:0; left:0; z-index: 2;"></canvas>
                        </div>

                        <!-- Toolbar -->
                        <div class="pad-toolbar mt-3">
                            <button class="pad-tool-btn undo-btn" onclick="undoStroke('exB')">↩ Burahin huli</button>
                            <button class="pad-tool-btn erase" onclick="clearCanvas('exB')">🗑 I-clear</button>
                            <button class="pad-tool-btn done-draw" onclick="markDone('exB')">✓ Tapos na!</button>
                        </div>
                        <div class="color-row">
                            <span style="font-size:0.8rem;font-weight:800;color:#aaa;">Kulay:</span>
                            <div class="color-swatch active" style="background:#4A90E2;" onclick="setColor('exB','#4D96FF',this)"></div>
                            <div class="color-swatch" style="background:#F44336;" onclick="setColor('exB','#FF6B9D',this)"></div>
                            <div class="color-swatch" style="background:#4CAF50;" onclick="setColor('exB','#6BCB77',this)"></div>
                            <div class="color-swatch" style="background:#FF9F43;" onclick="setColor('exB','#FF9F43',this)"></div>
                            <div class="color-swatch" style="background:#C77DFF;" onclick="setColor('exB','#C77DFF',this)"></div>
                            <div class="color-swatch" style="background:#2C2F33;" onclick="setColor('exB','#2C2F33',this)"></div>
                        </div>
                        <div class="brush-row">
                            <span style="font-size:0.8rem;font-weight:800;color:#aaa;">Laki ng panulat:</span>
                            <div class="brush-btn active" onclick="setBrush('exB',5,this)"><div class="brush-dot" style="width:6px;height:6px;"></div></div>
                            <div class="brush-btn" onclick="setBrush('exB',10,this)"><div class="brush-dot" style="width:11px;height:11px;"></div></div>
                            <div class="brush-btn" onclick="setBrush('exB',18,this)"><div class="brush-dot" style="width:18px;height:18px;"></div></div>
                        </div>
                        <div class="pad-done-tick" id="doneTick-exB">✅ Magaling! Sinulatan mo na ang maliit na o!</div>
                    </div>
                </div>
            </div>

            <!-- ===============================
             UNIT 4: Pagsasanay - Pairs
            ================================ -->
            <div class="unit-slide" id="unit-4">
                <div class="section-card">
                    <div class="section-badge badge-purple">📝 Pagsasanay</div>
                    <div class="pagsasanay-label text-center mt-3" style="font-size: 1.5rem; font-weight: 700; color: #333; margin-bottom: 5px;">C. Pagsamahin sa guhit ang siyam (9) malaki at maliit na letrang Oo.</div>
                    
                    <div class="draw-pad-wrapper" style="margin-top:20px;">
                        <div class="manuscript-paper" id="frameExC" style="height: 300px;">
                            <div class="canvas-ghost" id="ghostExC" style="flex-direction: column;">
                                <div class="ghost-row bottom">
                                    <div class="oo-group"><span class="ghost-letter big">O</span><span class="ghost-letter small">o</span></div>
                                    <div class="oo-group"><span class="ghost-letter big">O</span><span class="ghost-letter small">o</span></div>
                                    <div class="oo-group"><span class="ghost-letter big">O</span><span class="ghost-letter small">o</span></div>
                                </div>
                                <div class="ghost-row bottom">
                                    <div class="oo-group"><span class="ghost-letter big">O</span><span class="ghost-letter small">o</span></div>
                                    <div class="oo-group"><span class="ghost-letter big">O</span><span class="ghost-letter small">o</span></div>
                                    <div class="oo-group"><span class="ghost-letter big">O</span><span class="ghost-letter small">o</span></div>
                                </div>
                                <div class="ghost-row bottom">
                                    <div class="oo-group"><span class="ghost-letter big">O</span><span class="ghost-letter small">o</span></div>
                                    <div class="oo-group"><span class="ghost-letter big">O</span><span class="ghost-letter small">o</span></div>
                                    <div class="oo-group"><span class="ghost-letter big">O</span><span class="ghost-letter small">o</span></div>
                                </div>
                            </div>
                            <canvas id="canvasExC" class="coloring-canvas" height="300" style="width: 100%; height: 100%; position: absolute; top:0; left:0; z-index: 2;"></canvas>
                        </div>

                        <!-- Toolbar -->
                        <div class="pad-toolbar mt-3">
                            <button class="pad-tool-btn undo-btn" onclick="undoStroke('exC')">↩ Burahin huli</button>
                            <button class="pad-tool-btn erase" onclick="clearCanvas('exC')">🗑 I-clear</button>
                            <button class="pad-tool-btn done-draw" onclick="markDone('exC')">✓ Tapos na!</button>
                        </div>
                        <div class="color-row">
                            <span style="font-size:0.8rem;font-weight:800;color:#aaa;">Kulay:</span>
                            <div class="color-swatch active" style="background:#4A90E2;" onclick="setColor('exC','#4D96FF',this)"></div>
                            <div class="color-swatch" style="background:#F44336;" onclick="setColor('exC','#FF6B9D',this)"></div>
                            <div class="color-swatch" style="background:#4CAF50;" onclick="setColor('exC','#6BCB77',this)"></div>
                            <div class="color-swatch" style="background:#FF9F43;" onclick="setColor('exC','#FF9F43',this)"></div>
                            <div class="color-swatch" style="background:#C77DFF;" onclick="setColor('exC','#C77DFF',this)"></div>
                            <div class="color-swatch" style="background:#2C2F33;" onclick="setColor('exC','#2C2F33',this)"></div>
                        </div>
                        <div class="brush-row">
                            <span style="font-size:0.8rem;font-weight:800;color:#aaa;">Laki ng panulat:</span>
                            <div class="brush-btn active" onclick="setBrush('exC',5,this)"><div class="brush-dot" style="width:6px;height:6px;"></div></div>
                            <div class="brush-btn" onclick="setBrush('exC',10,this)"><div class="brush-dot" style="width:11px;height:11px;"></div></div>
                            <div class="brush-btn" onclick="setBrush('exC',18,this)"><div class="brush-dot" style="width:18px;height:18px;"></div></div>
                        </div>
                        <div class="pad-done-tick" id="doneTick-exC">✅ Napakahusay! Natapos mo na lahat!</div>
                    </div>
                </div>
            </div>
"""

html = html[:start_idx] + new_pagsasanay + html[end_idx:]

# Next, we must shift the unit IDs down for the remaining units
html = html.replace('<div class="unit-slide" id="unit-5">', '<div class="unit-slide" id="unit-7">')
html = html.replace('<div class="unit-slide" id="unit-4">', '<div class="unit-slide" id="unit-6">')
html = html.replace('<div class="unit-slide" id="unit-3">', '<div class="unit-slide" id="unit-5">')

# Shift any button references if necessary
html = html.replace('checkFillBlanksAct5()', 'checkFillBlanksAct7()')

# Update script logic
script_start = html.find('const UNIT_NAMES =')
if script_start != -1:
    old_units = "const UNIT_NAMES = ['Kilalanin Natin', 'Pagsulat', 'Pagsasanay', 'Gawain 1', 'Pagsasanay', 'Sagutin Natin'];"
    new_units = "const UNIT_NAMES = ['Kilalanin Natin', 'Pagsulat', 'Malaking O', 'Maliit na o', 'Oo', 'Gawain 1', 'Pagsasanay', 'Sagutin Natin'];"
    html = html.replace(old_units, new_units)
    
    # State update
    import re
    # The original state had up to 5, sometimes manually crafted or generated. 
    # Let's replace the whole state definition dynamically.
    state_pattern = r'const state = \{[^}]*\};'
    match = re.search(state_pattern, html)
    if match:
        new_state = r"""const state = {
                0: { score: 0, checked: false },
                1: { score: 0, checked: false },
                2: { score: 0, checked: false },
                3: { score: 0, checked: false },
                4: { score: 0, checked: false },
                5: { score: 0, checked: false },
                6: { score: 0, checked: false },
                7: { score: 0, checked: false },
                'blanks': { score: 0, checked: false }
            };"""
        html = html.replace(match.group(0), new_state)

# Replace Javascript logic for ExA, ExB, ExC
checkUnit2Func = r"""
            window.checkUnit2Writing = function () {
                let allValid = true;
                const pids = ['exA', 'exB', 'exC'];
                pids.forEach(pid => {
                    const v = validateDrawing(pid);
                    if (!v.valid) {
                        allValid = false;
                        const capId = pid.charAt(0).toUpperCase() + pid.slice(1);
                        const frame = document.getElementById('frame' + capId);
                        frame.style.border = '4px solid #f44336';
                        setTimeout(() => { frame.style.border = '1px solid #ddd'; }, 700);
                    }
                });

                const banner = document.getElementById('feedback-act2');
                const icon = document.getElementById('feedback-icon-2');
                const text = document.getElementById('feedback-text-2');
                banner.classList.add('show');

                if (allValid) {
                    if (!state[2].checked) {
                        state[2].checked = true;
                        state[2].score = 1;
                        const cur = parseInt(document.getElementById('starCount').textContent);
                        document.getElementById('starCount').textContent = cur + 1;
                        launchConfetti();
                        updateNextBtn();
                    }
                    banner.classList.remove('error-fb');
                    banner.classList.add('correct-fb');
                    icon.innerHTML = '🌟';
                    text.innerHTML = 'Napakagaling! Nasulat mo ng tama ang lahat ng letra.';
                    document.getElementById('check-act2').disabled = true;
                } else {
                    banner.classList.remove('correct-fb');
                    banner.classList.add('error-fb');
                    icon.innerHTML = '❌';
                    text.innerHTML = 'May hindi pa tapos o kulang ang pagkasulat! Pakisiguro na masulatan lahat ng nakita mong letra (O / o / Oo).';
                }
            };
"""

html = html.replace(checkUnit2Func, '')

# We will let markDone handle the scoring separately for exA, exB, exC just like upper/lower
markDone_match = html.find('if (id === \'upper\' || id === \'lower\')')
if markDone_match != -1:
    mark_done_code = r"""
                if (id === 'upper' || id === 'lower') {
                    if (pads['upper'] && pads['upper'].done && pads['lower'] && pads['lower'].done && !state[1].checked) {
                        state[1].checked = true;
                        state[1].score = 1;
                        const cur = parseInt(document.getElementById('starCount').textContent);
                        document.getElementById('starCount').textContent = cur + 1;
                        launchConfetti();
                        updateNextBtn();
                    }
                }
"""
    new_mark_done_code = r"""
                if (id === 'upper' || id === 'lower') {
                    if (pads['upper'] && pads['upper'].done && pads['lower'] && pads['lower'].done && !state[1].checked) {
                        state[1].checked = true;
                        state[1].score = 1;
                        const cur = parseInt(document.getElementById('starCount').textContent);
                        document.getElementById('starCount').textContent = cur + 1;
                        launchConfetti();
                        updateNextBtn();
                    }
                }
                
                if (id === 'exA' && !state[2].checked) {
                    state[2].checked = true;
                    state[2].score = 1;
                    const cur = parseInt(document.getElementById('starCount').textContent);
                    document.getElementById('starCount').textContent = cur + 1;
                    launchConfetti();
                    updateNextBtn();
                }
                
                if (id === 'exB' && !state[3].checked) {
                    state[3].checked = true;
                    state[3].score = 1;
                    const cur = parseInt(document.getElementById('starCount').textContent);
                    document.getElementById('starCount').textContent = cur + 1;
                    launchConfetti();
                    updateNextBtn();
                }
                
                if (id === 'exC' && !state[4].checked) {
                    state[4].checked = true;
                    state[4].score = 1;
                    const cur = parseInt(document.getElementById('starCount').textContent);
                    document.getElementById('starCount').textContent = cur + 1;
                    launchConfetti();
                    updateNextBtn();
                }
"""
    html = html.replace(mark_done_code, new_mark_done_code)

# Update scoring calculation total
html = html.replace('const totalScore = state[1].score + state[2].score + state[3].score + state[4].score + state[5].score', 'const totalScore = state[1].score + state[2].score + state[3].score + state[4].score + state[5].score + state[6].score + state[7].score')
html = html.replace('const maxScore = 5;', 'const maxScore = 7;')

# Replace unit 5 references
html = html.replace('function checkFillBlanksAct5()', 'function checkFillBlanksAct7()')
html = html.replace('!state[5].checked', '!state[7].checked')
html = html.replace('state[5].checked = true;', 'state[7].checked = true;')
html = html.replace('state[5].score = 1;', 'state[7].score = 1;')

# Replace unit 3 references (now unit 5)
html = html.replace('function checkAct1()', 'function checkAct5()')
html = html.replace('checkAct1()', 'checkAct5()')
html = html.replace('!state[3].checked', '!state[5].checked')
html = html.replace('state[3].checked = true;', 'state[5].checked = true;')
html = html.replace('state[3].score = 1;', 'state[5].score = 1;')

# Replace unit 4 references (now unit 6)
html = html.replace('!state[4].checked', '!state[6].checked')
html = html.replace('state[4].checked = true;', 'state[6].checked = true;')
html = html.replace('state[4].score = 1;', 'state[6].score = 1;')


with open('core/templates/core/letrang_o.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Option 1 setup complete.")
