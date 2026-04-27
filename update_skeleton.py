import glob

new_function = """            function validateDrawing(id) {
                const p = pads[id];
                const ctx = p.ctx;
                const imgData = ctx.getImageData(0, 0, p.canvas.width, p.canvas.height).data;

                // 1. Ensure canvas isn't empty
                let totalInk = 0;
                for (let i = 0; i < imgData.length; i += 4) {
                    if (imgData[i + 3] > 20) totalInk++;
                }

                if (totalInk < 50) {
                    return { valid: false, reason: "Walang guhit pa. Subukang sumulat!" };
                }

                // 2. Identify ghost letter config
                const ghostContainer = document.getElementById('ghost' + (id === 'upper' ? 'Upper' : 'Lower'));
                const spans = ghostContainer ? ghostContainer.querySelectorAll('.ghost-letter') : [];
                if (spans.length === 0) return { valid: true };

                const expectedLetter = spans[0].textContent.trim();
                const numExpected = spans.length;
                const zoneW = p.canvas.width / numExpected;

                let badZones = 0;
                let reasonMsg = "";

                // 3. Process each zone independently
                for (let z = 0; z < numExpected; z++) {
                    const xStart = Math.floor(z * zoneW);
                    const xEnd = Math.floor((z + 1) * zoneW);
                    
                    let minX = p.canvas.width, maxX = 0;
                    let minY = p.canvas.height, maxY = 0;
                    let zoneInk = 0;

                    for (let y = 0; y < p.canvas.height; y++) {
                        for (let x = xStart; x < xEnd; x++) {
                            const alpha = imgData[(y * p.canvas.width + x) * 4 + 3];
                            if (alpha > 20) {
                                zoneInk++;
                                if (x < minX) minX = x;
                                if (x > maxX) maxX = x;
                                if (y < minY) minY = y;
                                if (y > maxY) maxY = y;
                            }
                        }
                    }

                    if (zoneInk < 30) {
                        badZones++;
                        reasonMsg = `Kulang ang guhit sa bahagi ${z+1}. Isulat ang ${expectedLetter} dito.`;
                        continue;
                    }

                    const bw = Math.max(1, maxX - minX);
                    const bh = Math.max(1, maxY - minY);

                    if (bw < 15 && bh < 15) {
                        badZones++;
                        reasonMsg = `Masyadong maliit ang guhit sa bahagi ${z+1}. Lakihan ang hugis!`;
                        continue;
                    }

                    // Strict shape proportion checks
                    let minRatio = 0.2;
                    let maxRatio = 4.0;
                    if (expectedLetter === 'i') { maxRatio = 1.0; } // 'i' is tall
                    else if (expectedLetter === 'I') { maxRatio = 1.0; }
                    else if (expectedLetter === 'o' || expectedLetter === 'O') { minRatio = 0.5; maxRatio = 2.0; }
                    else if (expectedLetter === 'm' || expectedLetter === 'M') { minRatio = 0.5; maxRatio = 3.0; }
                    else if (expectedLetter === 'b' || expectedLetter === 'B') { minRatio = 0.3; maxRatio = 1.5; }

                    const ratio = bw / bh;
                    if (ratio < minRatio || ratio > maxRatio) {
                        badZones++;
                        reasonMsg = `Hindi tama ang proporsyon ng guhit. Parang hindi ${expectedLetter} ang nasa bahagi ${z+1}!`;
                        continue;
                    }

                    const pad = 40; 
                    const maskC = document.createElement('canvas');
                    maskC.width = bw + pad * 2; 
                    maskC.height = bh + pad * 2;
                    const mctx = maskC.getContext('2d', { willReadFrequently: true });
                    
                    mctx.clearRect(0, 0, maskC.width, maskC.height);

                    mctx.save();
                    mctx.translate(pad, pad); // Center the skeleton
                    
                    mctx.strokeStyle = 'white';
                    mctx.lineCap = 'round';
                    mctx.lineJoin = 'round';
                    // Stroke acts as our envelope
                    mctx.lineWidth = Math.max(20, Math.min(bw, bh) * 0.40); 
                    
                    mctx.beginPath();
                    const w = bw;
                    const h = bh;

                    if (expectedLetter === 'M') {
                        mctx.moveTo(0, h);
                        mctx.lineTo(w*0.2, 0);
                        mctx.lineTo(w*0.5, h*0.7);
                        mctx.lineTo(w*0.8, 0);
                        mctx.lineTo(w, h);
                    } else if (expectedLetter === 'm') {
                        mctx.moveTo(0, h);
                        mctx.lineTo(0, h*0.2); // left leg up
                        mctx.bezierCurveTo(w*0.1, -h*0.1, w*0.4, -h*0.1, w*0.5, h*0.2);
                        mctx.lineTo(w*0.5, h); // mid leg down
                        mctx.moveTo(w*0.5, h*0.2); // back up mid leg
                        mctx.bezierCurveTo(w*0.6, -h*0.1, w*0.9, -h*0.1, w, h*0.2);
                        mctx.lineTo(w, h); // right leg down
                    } else if (expectedLetter === 'O' || expectedLetter === 'o') {
                        mctx.ellipse(w/2, h/2, w/2, h/2, 0, 0, 2 * Math.PI);
                    } else if (expectedLetter === 'I' || expectedLetter === 'i') {
                        mctx.moveTo(w*0.5, 0);
                        mctx.lineTo(w*0.5, h);
                        if (expectedLetter === 'i') {
                            mctx.moveTo(w*0.5, h*0.2);
                            mctx.lineTo(w*0.5, h);
                            mctx.moveTo(w*0.5, 0);
                            mctx.lineTo(w*0.5, h*0.1);
                        }
                    } else if (expectedLetter === 'B') {
                        mctx.moveTo(w*0.1, h);
                        mctx.lineTo(w*0.1, 0);
                        mctx.moveTo(w*0.1, 0);
                        mctx.bezierCurveTo(w*1.5, 0, w*1.5, h*0.5, w*0.1, h*0.5);
                        mctx.moveTo(w*0.1, h*0.5);
                        mctx.bezierCurveTo(w*1.5, h*0.5, w*1.5, h, w*0.1, h);
                    } else if (expectedLetter === 'b') {
                        mctx.moveTo(w*0.1, 0);
                        mctx.lineTo(w*0.1, h);
                        mctx.moveTo(w*0.1, h*0.4);
                        mctx.bezierCurveTo(w*1.5, h*0.4, w*1.5, h, w*0.1, h);
                    } else {
                        mctx.moveTo(0, h/2); mctx.lineTo(w, h/2);
                    }
                    mctx.stroke();
                    mctx.restore();

                    const maskData = mctx.getImageData(0, 0, maskC.width, maskC.height).data;
                    
                    let insidePixels = 0;
                    let outsidePixels = 0;

                    for (let py = minY; py <= maxY; py++) {
                        for (let px = minX; px <= maxX; px++) {
                            const alpha = imgData[(py * p.canvas.width + px) * 4 + 3];
                            if (alpha > 20) {
                                const mx = (px - minX) + pad;
                                const my = (py - minY) + pad;
                                
                                const midx = (my * maskC.width + mx) * 4;
                                if (maskData[midx + 3] > 100) {
                                    insidePixels++;
                                } else {
                                    outsidePixels++;
                                }
                            }
                        }
                    }

                    if (outsidePixels > insidePixels * 0.35) {
                        badZones++;
                        reasonMsg = `Hindi malinaw ang hugis ${expectedLetter} sa bahagi ${z+1}. Iwasan ang magulo na guhit!`;
                        continue;
                    }
                }

                if (badZones > 0) {
                    return { valid: false, reason: reasonMsg };
                }

                return { valid: true };
            }"""

import re
files = glob.glob('core/templates/core/letrang_*.html')
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Use re.sub with a lambda to prevent escape parsing in replacement string
    new_content = re.sub(
        r'([ \t]*)function validateDrawing\(id\).*?(?=\n[ \t]*window\.markDone = function)', 
        lambda m: m.group(1) + new_function, 
        content, 
        flags=re.DOTALL
    )
    
    if new_content != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Done {file}')
    else:
        print(f'Failed {file}')
