import re

with open(r'c:\Users\User\Desktop\tunog-tuklas\core\templates\core\mapa.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_css = \"\"\"/*  Fantasy Cartoon Map Regions  */
        :root {
            --region-magic: #76FF03;
            --region-candy: #FF4081;
            --region-crystal: #00E5FF;
            --region-castle: #FFD54F;
        }

        html, body {
            margin: 0 !important;
            padding: 0 !important;
            width: 100% !important;
            height: 100% !important;
            overflow: hidden !important;
        }

        #map-app {
            display: flex;
            flex-direction: column;
            height: 100vh;
            overflow: hidden;
            background: #87CEEB; /* Bright sky blue */
        }

        /*  PREMIUM HEADER  */
        .map-header {
            position: relative;
            z-index: 1000;
            flex-shrink: 0;
            background: #ff5252;
            box-shadow: 0 4px 0 #ba000d;
            border-bottom: 4px solid #2c2f33;
            padding: 10px 20px;
        }

        .header-banderitas {
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            height: 30px;
            background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 25" preserveAspectRatio="none"><path d="M0,0 L10,20 L20,0 L30,20 L40,0 L50,20 L60,0 L70,20 L80,0 L90,20 L100,0" fill="%23FFEB3B" stroke="%232c2f33" stroke-width="2"/><path d="M5,0 L15,15 L25,0 L35,15 L45,0 L55,15 L65,0 L75,15 L85,0 L95,15" fill="%234CAF50" stroke="%232c2f33" stroke-width="2"/></svg>');
            background-size: 150px 30px;
            z-index: 999;
            pointer-events: none;
        }

        /*  SCROLL AREA  */
        .map-scroll-area {
            flex: 1;
            overflow-x: scroll;
            overflow-y: hidden;
            position: relative;
            cursor: grab;
            scrollbar-width: thin;
        }

        .map-scroll-area:active {
            cursor: grabbing;
        }

        .map-canvas {
            width: 5500px;
            height: 100%;
            position: relative;
            background: linear-gradient(180deg, #64B5F6 0%, #E1F5FE 60%, #FFF9C4 100%);
        }

        /*  OVERLAYS  */
        .scenery-layer {
            position: absolute;
            inset: 0;
            pointer-events: none;
            z-index: 1;
        }
        
        .terrain-svg {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 5500px;
            height: 65%;
            overflow: visible;
        }

        /*  THEMED NODES: MAGICAL BUTTONS  */
        .map-node .node-circle {
            border: 6px solid #2c2f33;
            box-shadow: 0 8px 0 #2c2f33, inset 0 -6px 0 rgba(0,0,0,0.2), inset 0 6px 0 rgba(255,255,255,0.4);
            width: 85px;
            height: 85px;
            font-size: 2.22rem;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 900;
            color: white;
            text-shadow: 0 3px 0 rgba(0,0,0,0.3);
            position: relative;
            overflow: hidden;
        }

        /*  MAGIC FOREST (was Coastal)  */
        .node-coastal .node-circle {
            background: #4CAF50;
        }

        /*  CANDY LAND (was Rural)  */
        .node-rural .node-circle {
            background: #E91E63;
        }

        /*  CRYSTAL SKY (was Highland)  */
        .node-highland .node-circle {
            background: #00BCD4;
        }

        /*  ROYAL CASTLE (was Town)  */
        .node-town .node-circle {
            background: #FF9800;
        }

        /*  ACTIVE: Glowing Star Button  */
        .node-active .node-circle {
            transform: scale(1.15);
            background: #FFEB3B !important;
            border-color: #2c2f33 !important;
            color: #E65100;
            box-shadow: 0 10px 0 #2c2f33, inset 0 -6px 0 rgba(0,0,0,0.1), 0 0 20px rgba(255,235,59,0.8) !important;
        }

        .node-completed .node-circle {
            background: #8BC34A !important;
            border-color: #2c2f33 !important;
            box-shadow: 0 6px 0 #2c2f33, inset 0 -4px 0 rgba(0,0,0,0.2) !important;
            color: #F1F8E9;
        }

        .node-completed::after {
            content: "\2713";
            position: absolute;
            top: -6px;
            right: -6px;
            background: #33691E;
            color: white;
            width: 25px;
            height: 25px;
            border-radius: 50%;
            font-size: 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 3px solid #2c2f33;
            font-weight: 900;
        }

        .node-locked .node-circle {
            background: #90A4AE !important;
            border-color: #2c2f33 !important;
            box-shadow: 0 6px 0 #2c2f33, inset 0 -4px 0 rgba(0,0,0,0.2) !important;
            color: #ECEFF1;
        }

        .node-locked .lock-icon {
            position: absolute;
            bottom: -4px;
            right: -4px;
            background: #455A64;
            color: white;
            width: 25px;
            height: 25px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 3px solid #2c2f33;
            font-size: 1rem;
        }

        /* Mascot Styles */
        .tarsier-guide {
            position: absolute;
            width: 80px;
            height: 80px;
            pointer-events: none;
            z-index: 60;
            transition: all 0.5s cubic-bezier(0.19, 1, 0.22, 1);
            animation: bounceMascot 2s ease-in-out infinite;
        }

        @keyframes bounceMascot {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-15px); }
        }

        @keyframes floatCloud {
            0%, 100% { transform: translateX(0); }
            50% { transform: translateX(30px); }
        }

        @keyframes floatBalloon {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }

        @keyframes swing {
            0%, 100% { transform: rotate(-5deg); }
            50% { transform: rotate(5deg); }
        }

        /*  SVG TRAIL (Dashed Cartoon Line)  */
        .path-glow, .path-shadow, .path-active, .path-inactive, .path-highlight { fill: none; }
        
        .path-shadow {
            stroke: #2c2f33;
            stroke-width: 25;
            stroke-linecap: round;
            stroke-linejoin: round;
            transform: translateY(6px);
        }

        .path-inactive {
            stroke: #FFFFFF;
            stroke-width: 15;
            stroke-linecap: round;
            stroke-linejoin: round;
            stroke-dasharray: 20 20;
        }

        .path-active {
            stroke: #FFEB3B;
            stroke-width: 15;
            stroke-linecap: round;
            stroke-linejoin: round;
            stroke-dasharray: 20 20;
            animation: dashScroll 1s linear infinite;
        }
        
        .path-glow {
            stroke: #FF9800;
            stroke-width: 25;
            stroke-linecap: round;
            stroke-linejoin: round;
        }

        .path-highlight { display: none; }

        @keyframes dashScroll {
            to { stroke-dashoffset: -40; }
        }

        /*  MAP NODES: base shared styles  */
        .map-node {
            position: absolute;
            transform: translate(-50%, -50%);
            cursor: pointer;
            transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .map-node:hover {
            transform: translate(-50%, -50%) scale(1.12);
        }
        .map-nodes-layer {
            position: absolute;
            inset: 0;
            z-index: 5;
        }
        \"\"\"

new_scenery = \"\"\"                <div class="scenery-layer" aria-hidden="true">
                    <!-- Whimsical Sky Elements (Sun, clouds, balloons) -->
                    <div style="position:absolute;top:5%;left:250px;font-size:9rem;animation:swing 4s ease-in-out infinite;filter:drop-shadow(0 0 20px #FFEB3B);z-index: 0;"></div>
                    <div style="position:absolute;top:15%;left:1000px;font-size:6rem;animation:floatBalloon 6s ease-in-out infinite;"></div>
                    <div style="position:absolute;top:10%;left:2400px;font-size:7rem;animation:floatCloud 8s ease-in-out infinite;"></div>
                    <div style="position:absolute;top:18%;left:3600px;font-size:6.5rem;animation:floatBalloon 7s ease-in-out infinite;"></div>
                    <div style="position:absolute;top:8%;left:4900px;font-size:8rem;animation:floatBalloon 9s ease-in-out infinite;"></div>
                    <div style="position:absolute;top:12%;left:5200px;font-size:5rem;animation:floatCloud 10s ease-in-out infinite;"></div>

                    <svg class="terrain-svg" viewBox="0 0 5500 400" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
                        <!-- Cartoon Back Hills -->
                        <path fill="#4CAF50" stroke="#2c2f33" stroke-width="4" d="M0,200 Q300,50 600,200 T1200,200 T1800,200 L1800,400 L0,400 Z" opacity="0.8"/>
                        <path fill="#E91E63" stroke="#2c2f33" stroke-width="4" d="M1200,200 Q1500,50 1800,200 T2400,200 T3000,200 L3000,400 L1200,400 Z" opacity="0.8"/>
                        <path fill="#00BCD4" stroke="#2c2f33" stroke-width="4" d="M2600,200 Q2900,50 3200,200 T3800,200 T4400,200 L4400,400 L2600,400 Z" opacity="0.8"/>
                        <path fill="#FF9800" stroke="#2c2f33" stroke-width="4" d="M4000,200 Q4300,50 4600,200 T5200,200 T5800,200 L5800,400 L4000,400 Z" opacity="0.8"/>

                        <!-- Cartoon Front Hills (Thick dark borders for 2D RPG/cartoon style) -->
                        <path fill="#8BC34A" stroke="#2c2f33" stroke-width="6" d="M-50,280 Q250,150 500,280 T1000,280 T1500,280 L1500,400 L-50,400 Z" />
                        <path fill="#F06292" stroke="#2c2f33" stroke-width="6" d="M1300,280 Q1600,150 1900,280 T2400,280 T2900,280 L2900,400 L1300,400 Z" />
                        <path fill="#26C6DA" stroke="#2c2f33" stroke-width="6" d="M2700,280 Q3000,150 3300,280 T3800,280 T4300,280 L4300,400 L2700,400 Z" />
                        <path fill="#FFB74D" stroke="#2c2f33" stroke-width="6" d="M4100,280 Q4400,150 4700,280 T5200,280 T5700,280 L5700,400 L4100,400 Z" />
                        
                        <!-- Connecting Ground Strip -->
                        <path fill="#795548" d="M0,380 L5500,380 L5500,400 L0,400 Z" />
                    </svg>

                    <!--  MAGIC FOREST decorations (Giant trees, mushrooms, tiny houses) -->
                    <span style="position:absolute;bottom:42%;left:100px;font-size:7rem;"></span>
                    <span style="position:absolute;bottom:45%;left:400px;font-size:8rem;"></span>
                    <span style="position:absolute;bottom:35%;left:700px;font-size:6rem;animation:bounceMascot 4s infinite;"></span>
                    <span style="position:absolute;bottom:48%;left:900px;font-size:7rem;"></span>
                    <span style="position:absolute;bottom:40%;left:1150px;font-size:5rem;"></span>

                    <!--  CANDY LAND decorations (Candies, cakes, ice cream) -->
                    <span style="position:absolute;bottom:42%;left:1450px;font-size:8rem;"></span>
                    <span style="position:absolute;bottom:46%;left:1750px;font-size:7rem;animation:floatBalloon 5s infinite;"></span>
                    <span style="position:absolute;bottom:38%;left:2100px;font-size:6.5rem;"></span>
                    <span style="position:absolute;bottom:48%;left:2400px;font-size:8rem;"></span>
                    <span style="position:absolute;bottom:35%;left:2650px;font-size:5rem;"></span>

                    <!--  CRYSTAL SKY decorations (Snow, magic clouds, stars) -->
                    <span style="position:absolute;bottom:42%;left:2900px;font-size:8rem;"></span>
                    <span style="position:absolute;bottom:48%;left:3250px;font-size:6.5rem;animation:bounceMascot 3s infinite;"></span>
                    <span style="position:absolute;bottom:35%;left:3600px;font-size:6rem;"></span>
                    <span style="position:absolute;bottom:45%;left:3900px;font-size:7.5rem;"></span>
                    <span style="position:absolute;bottom:40%;left:4200px;font-size:5rem;animation:swing 4s infinite;"></span>

                    <!--  ROYAL CASTLE decorations (Castles, crowns, magic) -->
                    <span style="position:absolute;bottom:46%;left:4400px;font-size:9rem;"></span>
                    <span style="position:absolute;bottom:38%;left:4750px;font-size:6.5rem;animation:bounceMascot 5s infinite;"></span>
                    <span style="position:absolute;bottom:48%;left:5100px;font-size:8rem;"></span>
                    <span style="position:absolute;bottom:40%;left:5350px;font-size:7rem;"></span>
                </div>\"\"\"

start_css = html.find(\"/*  Scenic Discovery Regions  */\")
end_css_str = \".map-path-svg {\"
end_css = html.find(end_css_str)
if start_css != -1 and end_css != -1:
    html = html[:start_css] + new_css + html[end_css:]
else:
    print('Failed to find CSS block')

start_scenery = html.find('<div class=\"scenery-layer\" aria-hidden=\"true\">')
end_scenery_str = '<!--  SVG PATH  -->'
end_scenery = html.find(end_scenery_str)
if start_scenery != -1 and end_scenery != -1:
    html = html[:start_scenery] + new_scenery + html[end_scenery:]
else:
    print('Failed to find scenery block')

html = html.replace('<path class=\"path-shadow\" fill=\"none\" d=\"{{ svg_path_d }}\" />', '<path class=\"path-shadow\" d=\"{{ svg_path_d }}\" />')
html = html.replace('<path class=\"path-glow\" fill=\"none\" filter=\"url(#glow)\" d=\"{{ svg_path_d }}\" />', '<path class=\"path-glow\" fill=\"none\" d=\"{{ svg_path_d }}\" />')
html = html.replace('<path class=\"path-active\" fill=\"none\" d=\"{{ svg_path_d }}\" />', '<path class=\"path-active\" d=\"{{ svg_path_d }}\" />')

with open(r'c:\Users\User\Desktop\tunog-tuklas\core\templates\core\mapa.html', 'w', encoding='utf-8') as f:
    f.write(html)