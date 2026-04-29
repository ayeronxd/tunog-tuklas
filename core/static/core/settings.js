/**
 * Tunog Tuklas — Global Settings System
 * Manages: Volume, Brightness, Low Graphics, Pixelated Mode, Fullscreen
 * All settings are persisted in localStorage and applied on every page load.
 */
(function () {
    'use strict';

    // ── Storage Keys ─────────────────────────────────────────────────────────
    const KEYS = {
        volume:      'tt_volume',       // 0–100
        brightness:  'tt_brightness',   // 50–150 (percentage)
        lowGraphics: 'tt_low_graphics', // 'true' | 'false'
        pixelated:   'tt_pixelated',    // 'true' | 'false'
    };

    // ── Defaults ─────────────────────────────────────────────────────────────
    const DEFAULTS = {
        volume:      80,
        brightness:  100,
        lowGraphics: false,
        pixelated:   0,
    };

    // ── Read helpers ─────────────────────────────────────────────────────────
    function getVolume()      { return parseInt(localStorage.getItem(KEYS.volume)      ?? DEFAULTS.volume, 10); }
    function getBrightness()  { return parseInt(localStorage.getItem(KEYS.brightness)  ?? DEFAULTS.brightness, 10); }
    function getLowGraphics() { return localStorage.getItem(KEYS.lowGraphics) === 'true'; }
    function getPixelated()   { 
        let stored = localStorage.getItem(KEYS.pixelated);
        if (stored === 'true') return 100;
        if (stored === 'false') return 0;
        return parseInt(stored ?? DEFAULTS.pixelated, 10); 
    }

    // ── Apply helpers ─────────────────────────────────────────────────────────
    function applyBrightness(val) {
        document.documentElement.style.setProperty('--tt-brightness', (val / 100).toFixed(2));
        const wrapper = document.getElementById('tt-brightness-wrapper');
        if (wrapper) wrapper.style.filter = `brightness(${val / 100})`;
    }

    function applyLowGraphics(on) {
        document.body.classList.toggle('tt-low-graphics', on);
    }

    function applyPixelated(val) {
        val = parseInt(val, 10);
        document.body.classList.toggle('tt-pixelated', val > 0);
        const overlay = document.getElementById('tt-pixel-overlay');
        if (overlay) {
            overlay.style.display = val > 0 ? 'block' : 'none';
            if (val > 0) {
                const opacity = (0.02 + (val * 0.001)).toFixed(3);
                const size = val > 50 ? 2 : 1;
                const spacing = val > 50 ? 4 : 3;
                
                overlay.style.background = `
                    repeating-linear-gradient(0deg, rgba(0,0,0,${opacity}) 0px, rgba(0,0,0,${opacity}) ${size}px, transparent ${size}px, transparent ${spacing}px),
                    repeating-linear-gradient(90deg, rgba(0,0,0,${opacity}) 0px, rgba(0,0,0,${opacity}) ${size}px, transparent ${size}px, transparent ${spacing}px)
                `;
            }
        }
    }

    // ── Audio interception ───────────────────────────────────────────────────
    // Wrap native Audio so every `new Audio(src).play()` respects global volume
    const _NativeAudio = window.Audio;
    function PatchedAudio(src) {
        const inst = new _NativeAudio(src);
        const vol = getVolume() / 100;
        inst.volume = vol;
        return inst;
    }
    PatchedAudio.prototype = _NativeAudio.prototype;
    window.Audio = PatchedAudio;

    // ── Public API ────────────────────────────────────────────────────────────
    window.TTSettings = {
        getVolume, getBrightness, getLowGraphics, getPixelated,

        setVolume(val) {
            val = Math.max(0, Math.min(100, val));
            localStorage.setItem(KEYS.volume, val);
            // Already applied via PatchedAudio on next play(); nothing visual to update
        },
        setBrightness(val) {
            val = Math.max(50, Math.min(150, val));
            localStorage.setItem(KEYS.brightness, val);
            applyBrightness(val);
        },
        setLowGraphics(on) {
            localStorage.setItem(KEYS.lowGraphics, on ? 'true' : 'false');
            applyLowGraphics(on);
        },
        setPixelated(val) {
            val = Math.max(0, Math.min(100, parseInt(val, 10)));
            localStorage.setItem(KEYS.pixelated, val);
            applyPixelated(val);
        },

        /** Call this once on DOMContentLoaded to apply all saved settings. */
        applyAll() {
            applyBrightness(getBrightness());
            applyLowGraphics(getLowGraphics());
            applyPixelated(getPixelated());
        },
    };

    // ── Auto-apply on load ───────────────────────────────────────────────────
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => window.TTSettings.applyAll());
    } else {
        window.TTSettings.applyAll();
    }
})();
