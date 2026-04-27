import re
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

                const comp = window.getComputedStyle(spans[0]);
                const fontFamily = comp.fontFamily;
                const fontWeight = comp.fontWeight;

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
                        reasonMsg = `Kulang ang sinulat sa bahagi ${z+1}. Isulat ang ${expectedLetter} dito.`;
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
                    const L = expectedLetter.toLowerCase();
                    let minRatio = 0.2;
                    let maxRatio = 4.0;
                    if (L === 'i') { maxRatio = 1.0; } // 'i' must be tall
                    else if (L === 'o') { minRatio = 0.5; maxRatio = 2.0; } // circles
                    else if (L === 'm') { minRatio = 0.4; maxRatio = 2.5; } // M is wide
                    else if (L === 'b') { minRatio = 0.3; maxRatio = 1.5; }

                    const ratio = bw / bh;
                    if (ratio < minRatio || ratio > maxRatio) {
                        badZones++;
                        reasonMsg = `Hindi tama ang proporsyon ng guhit. Parang hindi ${expectedLetter} ang nasa bahagi ${z+1}!`;
                        continue;
                    }

                    // --- Dynamic Neighbourhood Template Matching ---
                    // By not rendering a massive stroke, we prevent blobs from passing. 
                    // Instead, we check the proximity of user ink to a pure letter silhouette.
                    const maskC = document.createElement('canvas');
                    maskC.width = bw; 
                    maskC.height = bh;
                    const mctx = maskC.getContext('2d', { willReadFrequently: true });
                    
                    mctx.clearRect(0, 0, maskC.width, maskC.height);

                    mctx.save();
                    mctx.font = `${fontWeight} 100px ${fontFamily}`;
                    mctx.textBaseline = 'top';
                    const tm = mctx.measureText(expectedLetter);
                    const textW = tm.width || 100;
                    const textH = (tm.actualBoundingBoxAscent || 75) + (tm.actualBoundingBoxDescent || 0);

                    const sX = bw / textW;
                    const sY = bh / textH;
                    mctx.scale(sX, sY);

                    // Draw thin white text (exact structural skeleton)
                    mctx.fillStyle = 'white';
                    mctx.fillText(expectedLetter, 0, 0);
                    mctx.restore();

                    const maskData = mctx.getImageData(0, 0, maskC.width, maskC.height).data;
                    
                    let insidePixels = 0;
                    let outsidePixels = 0;
                    
                    // Tolerance margin (e.g. 15% of height). If ink is further away than this, it's scribbling.
                    const margin = Math.max(6, Math.floor(bh * 0.15));

                    for (let y = minY; y <= maxY; y++) {
                        for (let x = minX; x <= maxX; x++) {
                            const alpha = imgData[(y * p.canvas.width + x) * 4 + 3];
                            if (alpha > 20) {
                                let isMatched = false;
                                const mx = x - minX;
                                const my = y - minY;
                                
                                // Quick neighborhood search
                                const startY = Math.max(0, my - margin);
                                const endY = Math.min(maskC.height - 1, my + margin);
                                const startX = Math.max(0, mx - margin);
                                const endX = Math.min(maskC.width - 1, mx + margin);
                                
                                searchLoop:
                                for (let cy = startY; cy <= endY; cy++) {
                                    for (let cx = startX; cx <= endX; cx++) {
                                        // Alpha channel of mask > 100 means pixel is drawn
                                        if (maskData[(cy * maskC.width + cx) * 4 + 3] > 100) {
                                            isMatched = true;
                                            break searchLoop;
                                        }
                                    }
                                }
                                
                                if (isMatched) insidePixels++;
                                else outsidePixels++;
                            }
                        }
                    }

                    // A random scribble inside an 'M' box hits the empty gaps beneath the M.
                    // Those "gap pixels" will register as outsidePixels. If outside exceeds 40% of inside, reject!
                    if (outsidePixels > insidePixels * 0.40) {
                        badZones++;
                        reasonMsg = `Hindi malinaw ang hugis ${expectedLetter} sa bahagi ${z+1}. Iwasan ang magulo na guhit!`;
                        continue;
                    }

                    // Ensure minimum ink thickness to actually form the letter (detects a single horizontal line that passed scaling)
                    let maskArea = 0;
                    for (let i = 0; i < maskData.length; i += 4) {
                        if (maskData[i+3] > 100) maskArea++;
                    }
                    if (insidePixels < maskArea * 0.20) {
                        badZones++;
                        reasonMsg = `Kulang pa ang detalye ng ${expectedLetter} (bahagi ${z+1}). Buuin ang hugis!`;
                        continue;
                    }
                }

                if (badZones > 0) {
                    return { valid: false, reason: reasonMsg };
                }

                return { valid: true };
            }"""

files = glob.glob('core/templates/core/letrang_*.html')
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = re.sub(
        r'([ \t]*)function validateDrawing\(id\).*?(?=\n[ \t]*window\.markDone = function)', 
        new_function + '\n\n', 
        content, 
        flags=re.DOTALL
    )
    
    if new_content != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Done {file}')
    else:
        print(f'Failed to replace in {file}')
