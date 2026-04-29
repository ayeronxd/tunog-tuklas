"""
inject_settings.py
Adds the Tunog Tuklas settings system to all letrang_*.html lesson files.
Run once from the project root:  python inject_settings.py
"""

import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(BASE, 'core', 'templates', 'core')
STATIC_PATH = "{% static 'core/settings.js' %}"

LESSON_FILES = [
    'letrang_m.html',
    'letrang_b.html',
    'letrang_e.html',
    'letrang_i.html',
    'letrang_o.html',
]

# ── CSS block to inject at end of the </style> just before </head> ────────────
SETTINGS_CSS = """
        /* ── SETTINGS MODAL (Tunog Tuklas) ── */
        .settings-overlay {
            position: fixed; inset: 0; z-index: 25000;
            background: rgba(0,0,0,0.65);
            display: none;
            align-items: center;
            justify-content: center;
            backdrop-filter: blur(6px);
        }
        .settings-overlay.open { display: flex; }
        .settings-panel {
            background: linear-gradient(160deg, #fff9c4 0%, #fce4ec 50%, #e3f2fd 100%);
            border-radius: 32px;
            border: 5px solid #2c2f33;
            box-shadow: 0 14px 0 #2c2f33, 0 20px 50px rgba(0,0,0,0.25);
            width: 92%;
            max-width: 460px;
            overflow: hidden;
            animation: settingsIn 0.45s cubic-bezier(0.175,0.885,0.32,1.275) forwards;
        }
        @keyframes settingsIn {
            from { transform: scale(0.6) rotate(-4deg); opacity: 0; }
            to   { transform: scale(1) rotate(0deg);   opacity: 1; }
        }
        .settings-header {
            background: linear-gradient(135deg, #7c4dff, #e040fb);
            padding: 18px 24px;
            display: flex; align-items: center; justify-content: space-between;
            border-bottom: 4px solid #2c2f33;
        }
        .settings-header h2 {
            font-family: 'Nunito', sans-serif; font-weight: 900;
            font-size: 1.5rem; color: #fff; margin: 0;
            text-shadow: 2px 2px 0 rgba(0,0,0,0.3);
        }
        .settings-close-btn {
            width: 42px; height: 42px; border-radius: 50%;
            border: 3px solid rgba(255,255,255,0.7);
            background: rgba(255,255,255,0.25);
            color: #fff; font-size: 1.3rem; font-weight: 900;
            cursor: pointer; display: flex; align-items: center; justify-content: center;
            transition: all 0.15s; line-height: 1;
        }
        .settings-close-btn:hover { background: rgba(255,255,255,0.45); }
        .settings-body { padding: 22px 24px; display: flex; flex-direction: column; gap: 18px; max-height: 80vh; overflow-y: auto; }
        .settings-row {
            background: #fff;
            border: 3px solid #2c2f33;
            border-radius: 20px;
            padding: 14px 18px;
            box-shadow: 0 4px 0 #2c2f33;
        }
        .settings-row-label {
            font-family: 'Nunito', sans-serif; font-weight: 900;
            font-size: 1.05rem; color: #2c2f33;
            display: flex; align-items: center; gap: 8px;
            margin-bottom: 10px;
        }
        .settings-row-label .s-icon { font-size: 1.4rem; }
        .tt-slider {
            -webkit-appearance: none; appearance: none;
            width: 100%; height: 14px;
            border-radius: 20px;
            outline: none; cursor: pointer;
            border: 3px solid #2c2f33;
        }
        .tt-slider.volume-slider  { background: linear-gradient(90deg, #4CAF50 var(--vol-pct,80%), #ddd var(--vol-pct,80%)); }
        .tt-slider.brightness-slider { background: linear-gradient(90deg, #FDD835 var(--br-pct,50%), #ddd var(--br-pct,50%)); }
        .tt-slider::-webkit-slider-thumb {
            -webkit-appearance: none; appearance: none;
            width: 28px; height: 28px; border-radius: 50%;
            background: #fff; border: 4px solid #2c2f33;
            box-shadow: 0 3px 0 #2c2f33;
            cursor: pointer;
        }
        .slider-val {
            font-family: 'Nunito', sans-serif; font-weight: 900;
            font-size: 1.1rem; color: #555;
            min-width: 44px; text-align: right;
        }
        .tt-toggle-row { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
        .tt-toggle-label { font-family: 'Nunito', sans-serif; font-weight: 800; font-size: 0.95rem; color: #555; }
        .tt-switch {
            position: relative; display: inline-block;
            width: 64px; height: 34px; flex-shrink: 0;
        }
        .tt-switch input { opacity: 0; width: 0; height: 0; }
        .tt-switch-slider {
            position: absolute; inset: 0;
            background: #ccc; border-radius: 34px;
            border: 3px solid #2c2f33;
            cursor: pointer;
            transition: background 0.3s;
        }
        .tt-switch-slider::before {
            content: '';
            position: absolute;
            width: 22px; height: 22px;
            left: 3px; top: 50%; transform: translateY(-50%);
            background: #fff; border-radius: 50%;
            border: 2px solid #2c2f33;
            transition: left 0.3s;
        }
        .tt-switch input:checked + .tt-switch-slider { background: #7c4dff; }
        .tt-switch input:checked + .tt-switch-slider::before { left: 33px; }
        .tt-fullscreen-btn {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #FF9800, #F44336);
            border: 3px solid #2c2f33;
            border-radius: 14px;
            box-shadow: 0 4px 0 #2c2f33;
            font-family: 'Nunito', sans-serif; font-weight: 900;
            font-size: 1rem; color: #fff;
            cursor: pointer; transition: all 0.15s;
            display: flex; align-items: center; justify-content: center; gap: 8px;
        }
        .tt-fullscreen-btn:active { transform: translateY(4px); box-shadow: 0 0 0 #2c2f33; }
        #tt-pixel-overlay {
            position: fixed; inset: 0; z-index: 99999;
            pointer-events: none; display: none;
            image-rendering: pixelated;
            background: repeating-linear-gradient(
                0deg, rgba(0,0,0,0.04) 0px, rgba(0,0,0,0.04) 1px, transparent 1px, transparent 3px
            ),
            repeating-linear-gradient(
                90deg, rgba(0,0,0,0.04) 0px, rgba(0,0,0,0.04) 1px, transparent 1px, transparent 3px
            );
        }
        body.tt-low-graphics *,
        body.tt-low-graphics *::before,
        body.tt-low-graphics *::after {
            animation-duration: 0.001ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.001ms !important;
        }
        body.tt-pixelated { image-rendering: pixelated; }
        body.tt-pixelated img, body.tt-pixelated canvas { image-rendering: pixelated; }
        /* ── Settings gear button on lesson header ── */
        .btn-lesson-settings {
            background: rgba(255,255,255,0.25);
            border: 3px solid rgba(255,255,255,0.6);
            border-radius: 50%;
            width: 44px; height: 44px;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.3rem;
            cursor: pointer;
            transition: all 0.15s;
            flex-shrink: 0;
        }
        .btn-lesson-settings:hover { background: rgba(255,255,255,0.45); }
        .btn-lesson-settings:active { transform: translateY(2px); }
"""

# ── HTML for the settings button (replaces the header-stars div) ─────────────
# We keep header-stars and ADD the settings button next to it
SETTINGS_BTN_SNIPPET = """        <button class="btn-lesson-settings" onclick="openSettings()" title="Mga Setting" id="btn-settings">⚙️</button>"""

# ── Settings modal HTML ───────────────────────────────────────────────────────
SETTINGS_MODAL_HTML = """
    <!-- ══ SETTINGS MODAL ══ -->
    <div class="settings-overlay" id="settings-modal">
        <div class="settings-panel">
            <div class="settings-header">
                <h2>⚙️ Mga Setting</h2>
                <button class="settings-close-btn" onclick="closeSettings()">✕</button>
            </div>
            <div class="settings-body">
                <!-- 🔊 Volume -->
                <div class="settings-row">
                    <div class="settings-row-label"><span class="s-icon">🔊</span> Lakas ng Tunog</div>
                    <div style="display:flex;align-items:center;gap:12px;">
                        <input type="range" id="tt-vol-slider" class="tt-slider volume-slider"
                            min="0" max="100" step="1" value="80"
                            oninput="onVolChange(this.value)">
                        <span class="slider-val" id="tt-vol-label">80%</span>
                    </div>
                </div>
                <!-- ☀️ Brightness -->
                <div class="settings-row">
                    <div class="settings-row-label"><span class="s-icon">☀️</span> Liwanag ng Screen</div>
                    <div style="display:flex;align-items:center;gap:12px;">
                        <input type="range" id="tt-br-slider" class="tt-slider brightness-slider"
                            min="50" max="150" step="1" value="100"
                            oninput="onBrChange(this.value)">
                        <span class="slider-val" id="tt-br-label">100%</span>
                    </div>
                </div>
                <!-- 🎮 Low Graphics -->
                <div class="settings-row">
                    <div class="settings-row-label"><span class="s-icon">🎮</span> Kalidad ng Laro</div>
                    <div class="tt-toggle-row">
                        <span class="tt-toggle-label">I-off ang mga Galaw (Low Graphics)</span>
                        <label class="tt-switch">
                            <input type="checkbox" id="tt-lowgfx-toggle" onchange="onLowGfxChange(this.checked)">
                            <span class="tt-switch-slider"></span>
                        </label>
                    </div>
                </div>
                <!-- 🟫 Pixelated -->
                <div class="settings-row">
                    <div class="settings-row-label"><span class="s-icon">🟫</span> Pixel Mode</div>
                    <div class="tt-toggle-row">
                        <span class="tt-toggle-label">Retro / Pixel na Hitsura</span>
                        <label class="tt-switch">
                            <input type="checkbox" id="tt-pixel-toggle" onchange="onPixelChange(this.checked)">
                            <span class="tt-switch-slider"></span>
                        </label>
                    </div>
                </div>
                <!-- ⛶ Fullscreen -->
                <div class="settings-row">
                    <div class="settings-row-label"><span class="s-icon">⛶</span> Full Screen</div>
                    <button class="tt-fullscreen-btn" id="tt-fs-btn" onclick="toggleFullscreen()">⛶ I-bukas ang Full Screen</button>
                </div>
            </div>
        </div>
    </div>
    <!-- Pixel overlay -->
    <div id="tt-pixel-overlay"></div>
"""

# ── Settings JS ───────────────────────────────────────────────────────────────
SETTINGS_JS = """
    <script>
    // ═══════════════════════════════════════════════════════
    // SETTINGS MODAL CONTROLLER (Lesson Pages)
    // ═══════════════════════════════════════════════════════
    function openSettings() {
        var vol = window.TTSettings ? window.TTSettings.getVolume() : 80;
        var br  = window.TTSettings ? window.TTSettings.getBrightness() : 100;
        var lg  = window.TTSettings ? window.TTSettings.getLowGraphics() : false;
        var px  = window.TTSettings ? window.TTSettings.getPixelated() : false;
        var vs = document.getElementById('tt-vol-slider');
        var bs = document.getElementById('tt-br-slider');
        if (vs) { vs.value = vol; updateSliderBg(vs, vol, 0, 100); }
        if (bs) { bs.value = br;  updateSliderBg(bs, br, 50, 150); }
        var vl = document.getElementById('tt-vol-label');
        var bl = document.getElementById('tt-br-label');
        if (vl) vl.textContent = vol + '%';
        if (bl) bl.textContent = br  + '%';
        var lt = document.getElementById('tt-lowgfx-toggle');
        var pt = document.getElementById('tt-pixel-toggle');
        if (lt) lt.checked = lg;
        if (pt) pt.checked = px;
        updateFSBtn();
        document.getElementById('settings-modal').classList.add('open');
        document.body.style.overflow = 'hidden';
    }
    window.openSettings = openSettings;
    window.closeSettings = function() {
        document.getElementById('settings-modal').classList.remove('open');
        document.body.style.overflow = '';
    };
    function updateSliderBg(input, val, min, max) {
        var pct = ((val - min) / (max - min) * 100).toFixed(1) + '%';
        if (input.classList.contains('volume-slider'))     input.style.setProperty('--vol-pct', pct);
        if (input.classList.contains('brightness-slider')) input.style.setProperty('--br-pct',  pct);
    }
    window.onVolChange = function(val) {
        val = parseInt(val, 10);
        if (window.TTSettings) window.TTSettings.setVolume(val);
        var el = document.getElementById('tt-vol-label');
        if (el) el.textContent = val + '%';
        updateSliderBg(document.getElementById('tt-vol-slider'), val, 0, 100);
    };
    window.onBrChange = function(val) {
        val = parseInt(val, 10);
        if (window.TTSettings) window.TTSettings.setBrightness(val);
        var el = document.getElementById('tt-br-label');
        if (el) el.textContent = val + '%';
        updateSliderBg(document.getElementById('tt-br-slider'), val, 50, 150);
    };
    window.onLowGfxChange = function(checked) {
        if (window.TTSettings) window.TTSettings.setLowGraphics(checked);
    };
    window.onPixelChange = function(checked) {
        if (window.TTSettings) window.TTSettings.setPixelated(checked);
    };
    function updateFSBtn() {
        var btn = document.getElementById('tt-fs-btn');
        if (!btn) return;
        btn.textContent = document.fullscreenElement ? '⎋ Lumabas sa Full Screen' : '⛶ I-bukas ang Full Screen';
    }
    window.toggleFullscreen = function() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(function(){});
        } else {
            document.exitFullscreen().catch(function(){});
        }
    };
    document.addEventListener('fullscreenchange', updateFSBtn);
    </script>
"""

def inject_file(filename):
    path = os.path.join(TEMPLATES, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False

    # 1. Add settings.js script tag after font-awesome link (before </head>)
    if STATIC_PATH not in content:
        content = content.replace(
            "    <link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css\">",
            "    <link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css\">\n    <script src=\"{% static 'core/settings.js' %}\"></script>"
        )
        changed = True
        print(f"  [+] Added settings.js script tag")

    # 2. Inject CSS before the last </style> in head (the one before </head>)
    if '.btn-lesson-settings' not in content:
        # Find the closing </style> that is followed by </head>
        # We inject before </style>\n</head>
        style_close = content.rfind('    </style>')
        if style_close != -1:
            content = content[:style_close] + SETTINGS_CSS + content[style_close:]
            changed = True
            print(f"  [+] Injected settings CSS")

    # 3. Add settings button next to header-stars
    if 'btn-lesson-settings' not in content:
        # Replace the header block: find header-stars and add button after closing div
        # Pattern: </div>\n    </header>  after the starCount span / X
        # More targeted: replace </div>\n    </header> following "header-stars"
        # Find header-stars closing </div> then </header>
        pattern = r'(<div class="header-stars">.*?</div>)\s*\n(\s*</header>)'
        replacement = r'\1\n' + SETTINGS_BTN_SNIPPET + r'\n\2'
        new_content = re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)
        if new_content != content:
            content = new_content
            changed = True
            print(f"  [+] Added settings button in header")
        else:
            print(f"  [!] Could not inject settings button (pattern not found)")

    # 4. Add modal HTML before </body>
    if 'settings-modal' not in content:
        content = content.replace('</body>', SETTINGS_MODAL_HTML + '\n</body>', 1)
        changed = True
        print(f"  [+] Added settings modal HTML")

    # 5. Add JS before </body>
    if 'SETTINGS MODAL CONTROLLER (Lesson Pages)' not in content:
        content = content.replace('</body>', SETTINGS_JS + '\n</body>', 1)
        changed = True
        print(f"  [+] Added settings JS")

    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  [OK] %s updated successfully.\n" % filename)
    else:
        print("  [--] %s already up to date, skipped.\n" % filename)


if __name__ == '__main__':
    # letrang_m.html was already processed; run remaining files
    remaining = [
        'letrang_b.html',
        'letrang_e.html',
        'letrang_i.html',
        'letrang_o.html',
    ]
    for lesson in remaining:
        print("Processing: %s" % lesson)
        inject_file(lesson)
    print("Done! All lesson files processed.")
