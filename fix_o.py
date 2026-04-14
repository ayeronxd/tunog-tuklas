import os

filepath = 'core/templates/core/letrang_o.html'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = """                            </div>

                            <div class="text-center mt-4 pt-3 mb-3">
                                <button class="btn btn-primary px-5 py-3 rounded-pill fw-bold shadow-sm" id="check-act2"
                                    style="background:linear-gradient(135deg,var(--purple),#6a00f4); border:none; font-size:1.2rem;" onclick="checkUnit2Writing()">
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
""".splitlines(keepends=True)

# Replace lines 1612 to 2067 (indices 1611:2067)
lines[1611:2067] = new_lines

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('Fixed letrang_o.html')
