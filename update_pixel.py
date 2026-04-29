import os

BASE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(BASE, 'core', 'templates', 'core')

FILES = [
    'mapa.html',
    'letrang_b.html',
    'letrang_e.html',
    'letrang_i.html',
    'letrang_m.html',
    'letrang_o.html',
]

old_html = """                    <!-- \U0001f7eb Pixel Mode -->
                    <div class="settings-row">
                        <div class="settings-row-label"><span class="s-icon">\U0001f7eb</span> Pixel Mode</div>
                        <div class="tt-toggle-row">
                            <span class="tt-toggle-label">Retro / Pixel na Hitsura</span>
                            <label class="tt-switch">
                                <input type="checkbox" id="tt-pixel-toggle" onchange="onPixelChange(this.checked)">
                                <span class="tt-switch-slider"></span>
                            </label>
                        </div>
                    </div>"""

new_html = """                    <!-- \U0001f7eb Pixel Mode -->
                    <div class="settings-row">
                        <div class="settings-row-label"><span class="s-icon">\U0001f7eb</span> Pixel Effect</div>
                        <div style="display:flex;align-items:center;gap:12px;">
                            <input type="range" id="tt-pixel-slider" class="tt-slider pixel-slider"
                                min="0" max="100" step="10" value="0"
                                oninput="onPixelChange(this.value)">
                            <span class="slider-val" id="tt-pixel-label">0%</span>
                        </div>
                    </div>"""

css_old = ".tt-slider.brightness-slider { background: linear-gradient(90deg, #FDD835 var(--br-pct,50%), #ddd var(--br-pct,50%)); }"
css_new = ".tt-slider.brightness-slider { background: linear-gradient(90deg, #FDD835 var(--br-pct,50%), #ddd var(--br-pct,50%)); }\n        .tt-slider.pixel-slider { background: linear-gradient(90deg, #7c4dff var(--px-pct,0%), #ddd var(--px-pct,0%)); }"

# Update settings JS block inside html
js_old = """        var px  = window.TTSettings ? window.TTSettings.getPixelated() : false;
        var vs = document.getElementById('tt-vol-slider');"""

js_new = """        var px  = window.TTSettings ? window.TTSettings.getPixelated() : 0;
        var vs = document.getElementById('tt-vol-slider');
        var ps = document.getElementById('tt-pixel-slider');
        if (ps) { ps.value = px; updateSliderBg(ps, px, 0, 100); }"""

js2_old = """        if (bl) bl.textContent = br  + '%';
        var lt = document.getElementById('tt-lowgfx-toggle');
        var pt = document.getElementById('tt-pixel-toggle');
        if (lt) lt.checked = lg;
        if (pt) pt.checked = px;"""

js2_new = """        if (bl) bl.textContent = br  + '%';
        var pl = document.getElementById('tt-pixel-label');
        if (pl) pl.textContent = px + '%';
        var lt = document.getElementById('tt-lowgfx-toggle');
        if (lt) lt.checked = lg;"""

js3_old = """        if (input.classList.contains('brightness-slider')) input.style.setProperty('--br-pct',  pct);
    }"""

js3_new = """        if (input.classList.contains('brightness-slider')) input.style.setProperty('--br-pct',  pct);
        if (input.classList.contains('pixel-slider'))      input.style.setProperty('--px-pct',  pct);
    }"""

js4_old = """    window.onPixelChange = function(checked) {
        if (window.TTSettings) window.TTSettings.setPixelated(checked);
    };"""

js4_new = """    window.onPixelChange = function(val) {
        val = parseInt(val, 10);
        if (window.TTSettings) window.TTSettings.setPixelated(val);
        var el = document.getElementById('tt-pixel-label');
        if (el) el.textContent = val + '%';
        updateSliderBg(document.getElementById('tt-pixel-slider'), val, 0, 100);
    };"""

def update_file(filename):
    path = os.path.join(TEMPLATES, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False

    # Normalize newlines for reliable replace
    content = content.replace('\\r\\n', '\\n')

    # CSS
    if css_old in content and css_new not in content:
        content = content.replace(css_old, css_new)
        changed = True

    # HTML
    import re
    # The old HTML might have tabs or spaces, let's use regex
    # Match the row containing "Pixel Mode" or "Retro / Pixel"
    pattern_html = re.compile(r'<!-- \S+ Pixel(ated)? Mode -->\s*<div class="settings-row">.*?Retro / Pixel na Hitsura.*?</div>\s*</div>', re.DOTALL)
    if pattern_html.search(content):
        content = pattern_html.sub(new_html, content)
        changed = True

    # JS
    if js_old in content:
        content = content.replace(js_old, js_new)
        changed = True
    if js2_old in content:
        content = content.replace(js2_old, js2_new)
        changed = True
    if js3_old in content:
        content = content.replace(js3_old, js3_new)
        changed = True
    if js4_old in content:
        content = content.replace(js4_old, js4_new)
        changed = True

    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filename}")
    else:
        print(f"Could not find exact patterns to replace in {filename}")

for filename in FILES:
    update_file(filename)
