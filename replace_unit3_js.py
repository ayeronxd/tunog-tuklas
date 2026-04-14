import sys

file_path = "c:/Users/User/OneDrive/Desktop/tunog-tuklas/core/templates/core/letrang_o.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "// ── Interactive Coloring Canvases (Gawain 2) ──"
end_marker = "// ── Unit 4 & 5: Interactive Canvas Drawing Pads ──"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Could not find JS markers. Exiting.")
    sys.exit(1)

new_js = """// ── Pagsasanay (Unit 3/2) Drawing Pads ──
            window.act2CurrentColor = '#4A90E2';
            window.act2BrushSize = 5;
            window.act2IsEraser = false;

            window.setAct2Color = function(swatch) {
                document.querySelectorAll('#colorPalette .color-swatch').forEach(s => s.classList.remove('active'));
                swatch.classList.add('active');
                window.act2CurrentColor = swatch.dataset.color;
                
                if (window.act2IsEraser) {
                    window.toggleAct2Eraser(); // turn off eraser
                }
                
                ['exA', 'exB', 'exC'].forEach(id => {
                    if (pads[id]) {
                        pads[id].color = window.act2CurrentColor;
                        updateCursor(id, window.act2CurrentColor);
                    }
                });
            };

            window.setAct2BrushSize = function(val) {
                window.act2BrushSize = val;
                ['exA', 'exB', 'exC'].forEach(id => {
                    if (pads[id]) {
                        pads[id].brush = parseInt(val);
                        updateCursor(id, pads[id].color); // cursor size is fixed in visual for now or we could omit
                    }
                });
            };

            window.toggleAct2Eraser = function() {
                window.act2IsEraser = !window.act2IsEraser;
                const btn = document.getElementById('btnEraser');
                if (window.act2IsEraser) {
                    btn.classList.add('active-tool');
                    ['exA', 'exB', 'exC'].forEach(id => {
                        if (pads[id]) {
                            pads[id].color = '#ffffff';
                            updateCursor(id, '#ffffff'); // pseudo-eraser cursor
                        }
                    });
                } else {
                    btn.classList.remove('active-tool');
                    ['exA', 'exB', 'exC'].forEach(id => {
                        if (pads[id]) {
                            pads[id].color = window.act2CurrentColor;
                            updateCursor(id, window.act2CurrentColor);
                        }
                    });
                }
            };

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

# We also need to add initPad('exA'), initPad('exB'), initPad('exC') to the bottom initPad section
init_pad_marker = "initPad('upper');\n            initPad('lower');\n            initPad('p1');\n            initPad('p2');\n            initPad('p3');"
new_init_pad = init_pad_marker + "\n            initPad('exA');\n            initPad('exB');\n            initPad('exC');"

new_content = content[:start_idx] + new_js + content[end_idx:]
new_content = new_content.replace(init_pad_marker, new_init_pad)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)
print("Updated Unit 3 JS")
