/**
 * Tunog Tuklas — Global Audio Manager
 * Handles BGM playback, SFX triggering, and Volume Syncing.
 */
(function () {
    'use strict';

    const STATIC_AUDIO_URL = '/static/core/audio/'; 

    const sfx = {
        click: new Audio(STATIC_AUDIO_URL + 'Click-pop.mp3'),
        whoosh: new Audio(STATIC_AUDIO_URL + 'whoosh.mp3'),
        slide: new Audio(STATIC_AUDIO_URL + 'Slide.mp3'),
        correct: new Audio(STATIC_AUDIO_URL + 'correct.mp3'),
        failed: new Audio(STATIC_AUDIO_URL + 'failed.mp3'),
        congratulations: new Audio(STATIC_AUDIO_URL + 'congratulations.mp3') 
    };

    let currentBGM = null;
    let currentBGMName = '';

    function getMasterVolume() {
        return window.TTSettings ? (window.TTSettings.getVolume() / 100) : 0.8;
    }

    window.AudioManager = {
        // --- SOUND EFFECTS ---
        playSFX: function(name) {
            if (sfx[name]) {
                sfx[name].currentTime = 0; // Reset para pwede i-click nang mabilis
                sfx[name].volume = getMasterVolume();
                sfx[name].play().catch(e => console.log("SFX blocked:", e));
            }
        },

        // --- BACKGROUND MUSIC ---
        playBGM: function(filename) {
            if (currentBGMName === filename && currentBGM) return; 
            if (currentBGM) currentBGM.pause();
            
            currentBGM = new Audio(STATIC_AUDIO_URL + filename);
            currentBGM.loop = true;
            currentBGM.volume = getMasterVolume();
            currentBGMName = filename;
            
            const playPromise = currentBGM.play();
            if (playPromise !== undefined) {
                playPromise.catch(() => {
                    document.addEventListener('click', () => {
                        if(currentBGM.paused) currentBGM.play();
                    }, { once: true });
                });
            }
        },

        pauseBGM: function() {
            if (currentBGM) currentBGM.pause();
        },

        resumeBGM: function() {
            if (currentBGM && currentBGM.paused) {
                currentBGM.play().catch(e => console.log("BGM resume blocked:", e));
            }
        },

        updateVolume: function() {
            if (currentBGM) currentBGM.volume = getMasterVolume();
        }
    };

    // ── GINAWANG SMART CLICK INTERCEPTOR ──
    // Isinama natin ang '.choice-card', '.letter-token', at '.pad-tool-btn' para automatic silang tumunog!
    document.addEventListener('click', function(e) {
        const isSelectable = e.target.closest('.btn, button, .animal-card, .scroll-hint, .btn-close, .header-back-btn, .choice-card, .letter-token, .pad-tool-btn');
        if (isSelectable) {
            window.AudioManager.playSFX('click');
        }
    }, true);

})();