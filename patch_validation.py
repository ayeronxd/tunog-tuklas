import re
import glob

new_function = """            function validateDrawing(id) {
                const p = pads[id];
                const ctx = p.ctx;
                const imgData = ctx.getImageData(0, 0, p.canvas.width, p.canvas.height).data;

                // 1. Read global ink to ensure canvas isn't empty
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

                // 3. Process each zone
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

                    if (zoneInk < 40) {
                        badZones++;
                        reasonMsg = `Kulang ang sinulat sa bahagi ${z+1}. Isulat ang ${expectedLetter} dito.`;
                        continue;
                    }

                    const bw = Math.max(1, maxX - minX);
                    const bh = Math.max(1, maxY - minY);

                    // Check for tiny dots
                    if (bw < 15 && bh < 15) {
                        badZones++;
                        reasonMsg = `Masyadong maliit ang guhit sa bahagi ${z+1}. Lakihan ang hugis!`;
                        continue;
                    }

                    // Strict squash ratio checks
                    const L = expectedLetter.toLowerCase();
                    let minRatio = 0.15;
                    let maxRatio = 4.0;
                    if (L === 'i') { maxRatio = 2.0; }
                    else if (L === 'o' || L === 'm') { minRatio = 0.3; maxRatio = 3.0; }
                    else { minRatio = 0.2; maxRatio = 3.5; }

                    const ratio = bw / bh;
                    if (ratio < minRatio || ratio > maxRatio) {
                        badZones++;
                        reasonMsg = `Hindi tama ang proporsyon ng guhit sa bahagi ${z+1}. Ayusin ang hugis ng ${expectedLetter}!`;
                        continue;
                    }

                    // --- Dynamic Template Matching ---
                    const maskC = document.createElement('canvas');
                    maskC.width = bw + 60; 
                    maskC.height = bh + 60;
                    const mctx = maskC.getContext('2d', { willReadFrequently: true });
                    
                    mctx.fillStyle = 'black';
                    mctx.fillRect(0, 0, maskC.width, maskC.height);

                    mctx.save();
                    mctx.font = `${fontWeight} 100px ${fontFamily}`;
                    mctx.textBaseline = 'top';
                    const tm = mctx.measureText(expectedLetter);
                    const textW = tm.width || 100;
                    const textH = (tm.actualBoundingBoxAscent || 75) + (tm.actualBoundingBoxDescent || 0);

                    const sX = bw / textW;
                    const sY = bh / textH;

                    mctx.translate(30, 30);
                    mctx.scale(sX, sY);

                    // Provide a generous forgiving stroke envelope proportionally
                    mctx.fillStyle = 'white';
                    mctx.strokeStyle = 'white';
                    mctx.lineJoin = 'round';
                    mctx.lineCap = 'round';
                    mctx.lineWidth = 45 / Math.max(0.5, Math.max(sX, sY)); 
                    
                    mctx.fillText(expectedLetter, 0, 0);
                    mctx.strokeText(expectedLetter, 0, 0);
                    mctx.restore();

                    const maskData = mctx.getImageData(0, 0, maskC.width, maskC.height).data;
                    let insideMask = 0;
                    let outsideMask = 0;
                    let maskArea = 0;

                    for (let y = minY; y <= maxY; y++) {
                        for (let x = minX; x <= maxX; x++) {
                            const alpha = imgData[(y * p.canvas.width + x) * 4 + 3];
                            if (alpha > 20) {
                                // Map user ink coordinates smoothly into the template
                                const mx = (x - minX) + 30;
                                const my = (y - minY) + 30;
                                const midx = (my * maskC.width + mx) * 4;
                                const isWhite = maskData[midx] > 50;
                                
                                if (isWhite) insideMask++;
                                else outsideMask++;
                            }
                        }
                    }

                    for (let i = 0; i < maskData.length; i += 4) {
                        if (maskData[i] > 50) maskArea++;
                    }

                    // Penalty thresholds
                    // If they drew outside the thick guide heavily, it's scribbling/bad shape.
                    if (outsideMask > insideMask * 0.70) {
                        badZones++;
                        reasonMsg = `Makalat o hindi hugis ${expectedLetter} ang nasa bahagi ${z+1}. Ayusin ang pagguhit!`;
                        continue;
                    }

                    // Completeness
                    if (insideMask < maskArea * 0.08) {
                        badZones++;
                        reasonMsg = `Kulang ang detalye ng ${expectedLetter} sa bahagi ${z+1}.`;
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
