import sys

file_path = "c:/Users/User/OneDrive/Desktop/tunog-tuklas/core/templates/core/letrang_o.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "<!-- ═══════════════════════════════════\n             UNIT 3: Gawain 2 – Ending /m/\n        ═══════════════════════════════════ -->"
end_marker = "<!-- ═══════════════════════════════════\n             UNIT 2: Gawain 1 – Starting /m/\n        ═══════════════════════════════════ -->"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Could not find markers. Exiting.")
    sys.exit(1)

new_unit_html = """<!-- ═══════════════════════════════════
             UNIT 3: Pagsasanay 2 (Drawing)
        ═══════════════════════════════════ -->
            <div class="unit-slide" id="unit-2">
                <div class="section-card">
                    <div class="section-badge badge-purple">📝 Pagsasanay</div>

                    <!-- Layout similar to Gawain 2 with sidebar -->
                    <div class="gawain2-layout mt-3">
                        <div class="sidebar-tools">
                            <div class="color-palette-vert" id="colorPalette">
                                <div class="color-swatch active" style="background-color: #4A90E2;" data-color="#4A90E2" onclick="setAct2Color(this)"></div>
                                <div class="color-swatch" style="background-color: #F44336;" data-color="#F44336" onclick="setAct2Color(this)"></div>
                                <div class="color-swatch" style="background-color: #4CAF50;" data-color="#4CAF50" onclick="setAct2Color(this)"></div>
                                <div class="color-swatch" style="background-color: #FFEB3B;" data-color="#FFEB3B" onclick="setAct2Color(this)"></div>
                                <div class="color-swatch" style="background-color: #9C27B0;" data-color="#9C27B0" onclick="setAct2Color(this)"></div>
                                <div class="color-swatch" style="background-color: #2C2F33;" data-color="#2C2F33" onclick="setAct2Color(this)"></div>
                            </div>

                            <div class="brush-size-vert">
                                <i class="fa-solid fa-paintbrush"></i>
                                <div class="brush-slider-wrapper">
                                    <input type="range" id="brushSize" min="5" max="40" value="5" oninput="setAct2BrushSize(this.value)">
                                </div>
                            </div>

                            <div class="action-tools-vert">
                                <button class="tool-btn-vert" id="btnEraser" onclick="toggleAct2Eraser()">
                                    <i class="fa-solid fa-eraser"></i> Pambura
                                </button>
                            </div>
                        </div>

                        <div class="sidebar-card-main" style="text-align: left;">
                            <style>
                                .manuscript-paper {
                                    background: repeating-linear-gradient(
                                        transparent,
                                        transparent 25px,
                                        #82b1ff 26px,
                                        transparent 27px,
                                        transparent 50px,
                                        #ff8a80 51px,
                                        transparent 52px,
                                        transparent 75px,
                                        #82b1ff 76px,
                                        transparent 77px,
                                        transparent 100px
                                    );
                                    border-radius: 8px;
                                    position: relative;
                                    width: 100%;
                                    height: 100px; /* One line block */
                                    margin-bottom: 25px;
                                    border: 1px solid #ddd;
                                    overflow: hidden;
                                }
                                .canvas-ghost.row-ghosts {
                                    flex-direction: row;
                                    flex-wrap: wrap;
                                    justify-content: space-evenly;
                                    align-content: center;
                                    gap: 15px;
                                }
                                .pagsasanay-label {
                                    font-size: 1.2rem;
                                    font-weight: 700;
                                    color: #333;
                                    margin-bottom: 5px;
                                }
                            </style>

                            <!-- A. 7 Malalaking O -->
                            <div class="pagsasanay-label">A. Sumulat ng pitong (7) malalaking O.</div>
                            <div class="manuscript-paper" id="frameExA">
                                <div class="canvas-ghost row-ghosts" id="ghostExA">
                                    <span class="ghost-letter">O</span>
                                    <span class="ghost-letter">O</span>
                                    <span class="ghost-letter">O</span>
                                    <span class="ghost-letter">O</span>
                                    <span class="ghost-letter">O</span>
                                    <span class="ghost-letter">O</span>
                                    <span class="ghost-letter">O</span>
                                </div>
                                <canvas id="canvasExA" class="coloring-canvas" style="width: 100%; height: 100%; position: absolute; top:0; left:0;"></canvas>
                            </div>

                            <!-- B. 8 Maliliit na o -->
                            <div class="pagsasanay-label">B. Sumulat ng walong (8) maliliit na o.</div>
                            <div class="manuscript-paper" id="frameExB">
                                <div class="canvas-ghost row-ghosts" id="ghostExB" style="align-content: flex-end; padding-bottom: 25px;">
                                    <span class="ghost-letter" style="font-size:4rem; line-height: 1;">o</span>
                                    <span class="ghost-letter" style="font-size:4rem; line-height: 1;">o</span>
                                    <span class="ghost-letter" style="font-size:4rem; line-height: 1;">o</span>
                                    <span class="ghost-letter" style="font-size:4rem; line-height: 1;">o</span>
                                    <span class="ghost-letter" style="font-size:4rem; line-height: 1;">o</span>
                                    <span class="ghost-letter" style="font-size:4rem; line-height: 1;">o</span>
                                    <span class="ghost-letter" style="font-size:4rem; line-height: 1;">o</span>
                                    <span class="ghost-letter" style="font-size:4rem; line-height: 1;">o</span>
                                </div>
                                <canvas id="canvasExB" class="coloring-canvas" style="width: 100%; height: 100%; position: absolute; top:0; left:0;"></canvas>
                            </div>

                            <!-- C. 9 Pairs of Oo -->
                            <div class="pagsasanay-label">C. Pagsamahin sa guhit ang siyam (9) malaki at maliit na letrang Oo.</div>
                            <div class="manuscript-paper" id="frameExC" style="height: 200px;"> <!-- double height for two rows -->
                                <div class="canvas-ghost row-ghosts" id="ghostExC">
                                    <span class="ghost-letter" style="margin-right:20px;">Oo</span>
                                    <span class="ghost-letter" style="margin-right:20px;">Oo</span>
                                    <span class="ghost-letter" style="margin-right:20px;">Oo</span>
                                    <span class="ghost-letter" style="margin-right:20px;">Oo</span>
                                    <span class="ghost-letter" style="margin-right:20px;">Oo</span>
                                    <span class="ghost-letter" style="margin-right:20px;">Oo</span>
                                    <span class="ghost-letter" style="margin-right:20px;">Oo</span>
                                    <span class="ghost-letter" style="margin-right:20px;">Oo</span>
                                    <span class="ghost-letter" style="margin-right:20px;">Oo</span>
                                </div>
                                <canvas id="canvasExC" class="coloring-canvas" style="width: 100%; height: 100%; position: absolute; top:0; left:0;"></canvas>
                            </div>

                            <div class="text-center mt-4">
                                <button class="check-btn" id="check-act2"
                                    style="background:linear-gradient(135deg,var(--purple),#6a00f4);" onclick="checkUnit2Writing()">
                                    <i class="fa-solid fa-check-circle"></i> Suriin ang Aking mga Sinulat
                                </button>
                            </div>

                            <div class="feedback-banner" id="feedback-act2">
                                <span class="feedback-icon" id="feedback-icon-2"></span>
                                <span id="feedback-text-2"></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
"""

new_content = content[:start_idx] + new_unit_html + "\n            " + content[end_idx:]

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)
print("Updated Unit 3 HTML")
