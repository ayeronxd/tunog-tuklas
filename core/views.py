import json
import base64
import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from core.models import Level, UserLevelProgress

def index(request):
    """View for the landing page."""
    return render(request, 'core/index.html')

@login_required
def mapa(request):
    """View for the map page. Calculates user progress dynamically."""
    user_account = request.user.account
    levels = Level.objects.all().order_by('order')
    
    # Get all progress records for this user
    user_progress = UserLevelProgress.objects.filter(account=user_account)
    progress_dict = {p.level_id: p for p in user_progress}
    
    # Calculate total stars
    total_earned_stars = sum(p.stars_earned for p in user_progress)
    max_possible_stars = levels.count() * 5

    # Build rendering data for the template
    map_nodes = []
    
    # Logic to determine the "Current Active" node.
    # The active node is the FIRST node that is NOT completed.
    found_active = False

    for index, level in enumerate(levels):
        prog = progress_dict.get(level.id)
        
        # By default, Level 0 (Index 0) is always unlocked if no progress exists yet
        is_unlocked = prog.is_unlocked if prog else (index == 0)
        is_completed = prog.is_completed if prog else False
        stars = prog.stars_earned if prog else 0
        
        node_status = "locked"
        
        if is_completed:
            node_status = "completed"
        elif is_unlocked:
            if not found_active:
                node_status = "active"
                found_active = True
            else:
                # Technically unlocked but waiting for previous to finish? 
                 # We'll treat it as active or just unlocked based on UI needs. 
                 # For Tunog Tuklas, only one is "Dito ka na" (Orange) at a time.
                node_status = "unlocked_pending"
                
        # Handle the edge case where they unlocked it, but haven't played, 
        # and we need to automatically unlock the FIRST node for brand new players.
        if index == 0 and not is_completed and not found_active:
             node_status = "active"
             found_active = True

        # Map pos_left (range ~10-490) to pixel position on 5500px canvas
        # Reserve 250px padding on each side: usable range 250–5250px
        CANVAS_WIDTH = 5500
        CANVAS_PAD = 250
        POS_MIN, POS_MAX = 10, 490
        pos_left_px = int(
            CANVAS_PAD + (level.pos_left - POS_MIN) / (POS_MAX - POS_MIN) * (CANVAS_WIDTH - 2 * CANVAS_PAD)
        )
        # SVG Y coordinate: viewBox height is 700 units
        svg_x = pos_left_px
        svg_y = int(level.pos_top / 100 * 700)

        map_nodes.append({
            'id': level.id,
            'name': level.name.replace("Letrang ", ""),
            'pos_top': level.pos_top,
            'pos_left': level.pos_left,
            'pos_left_px': pos_left_px,
            'svg_x': svg_x,
            'svg_y': svg_y,
            'status': node_status,
            'stars': stars
        })

    # ── Build SVG path connecting every node to the next with smooth cubic beziers ──
    # Control points pull horizontally (1/3 of horizontal distance) to make organic S-curves
    svg_path_d = ""
    for i, node in enumerate(map_nodes):
        x, y = node['svg_x'], node['svg_y']
        if i == 0:
            svg_path_d += f"M {x} {y}"
        else:
            prev = map_nodes[i - 1]
            px, py = prev['svg_x'], prev['svg_y']
            dx = (x - px) / 3
            cp1x, cp1y = round(px + dx), py
            cp2x, cp2y = round(x - dx), y
            svg_path_d += f" C {cp1x} {cp1y} {cp2x} {cp2y} {x} {y}"

    # If all levels are completed, the last one might just stay completed, no active node.
    active_node = next((n for n in map_nodes if n['status'] == 'active'), None)
    active_node_scroll_px = active_node['pos_left_px'] if active_node else 0

    # Get a list of all completed letter names to sync with localStorage.
    # We take the first character of the name and uppercase it (e.g., "Ii" -> "I", "Mm" -> "M")
    completed_letters = [n['name'][0].upper() for n in map_nodes if n['status'] == 'completed' and n['name']]

    context = {
        'map_nodes': map_nodes,
        'svg_path_d': svg_path_d,
        'total_stars': total_earned_stars,
        'max_stars': max_possible_stars,
        'active_node': active_node,
        'active_node_scroll_px': active_node_scroll_px,
        'completed_letters': completed_letters,
    }
    
    return render(request, 'core/mapa.html', context)

@login_required
def letrang_m(request):
    """View for the Letrang Mm interactive lesson page."""
    level = Level.objects.filter(name__icontains='M').first()
    context = {'level_id': level.id if level else ''}
    return render(request, 'core/letrang_m.html', context)

@login_required
def letrang_i(request):
    """View for the Letrang Ii interactive lesson page."""
    level = Level.objects.filter(name__icontains='I').first()
    context = {'level_id': level.id if level else ''}
    return render(request, 'core/letrang_i.html', context)

@login_required
def letrang_o(request):
    """View for the Letrang Oo interactive lesson page."""
    level = Level.objects.filter(name__icontains='O').first()
    context = {'level_id': level.id if level else ''}
    return render(request, 'core/letrang_o.html', context)

@login_required
def letrang_b(request):
    """View for the Letrang Bb interactive lesson page."""
    level = Level.objects.filter(name__icontains='B').first()
    context = {'level_id': level.id if level else ''}
    return render(request, 'core/letrang_b.html', context)

@login_required
def letrang_e(request):
    """View for the Letrang Ee interactive lesson page."""
    level = Level.objects.filter(name__icontains='E').first()
    context = {'level_id': level.id if level else ''}
    return render(request, 'core/letrang_e.html', context)

@login_required
@require_POST
def save_progress(request):
    """AJAX endpoint to save user progress and stars for a level."""
    try:
        data = json.loads(request.body)
        level_id = data.get('level_id')
        stars = data.get('stars', 0)
        is_completed = data.get('is_completed', False)

        if not level_id:
            return JsonResponse({'status': 'error', 'message': 'Missing level_id'}, status=400)
            
        level = Level.objects.get(id=level_id)
        progress, _ = UserLevelProgress.objects.get_or_create(
            account=request.user.account,
            level=level
        )
        
        if stars > progress.stars_earned:
            progress.stars_earned = stars
            
        if is_completed:
            progress.is_completed = True
            
            # Unlock next level
            next_level = Level.objects.filter(order__gt=level.order).order_by('order').first()
            if next_level:
                next_prog, _ = UserLevelProgress.objects.get_or_create(
                    account=request.user.account,
                    level=next_level
                )
                next_prog.is_unlocked = True
                next_prog.save()
                
        progress.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# ── AI Handwriting Validator ──────────────────────────────────────────────────

HANDWRITING_SYSTEM_PROMPT = """You are a handwriting validator for kindergarten students (ages 4–7).

You will receive a canvas image and a target letter to validate.

=== VALID — Accept if: ===
- Drawing clearly resembles the target letter
- Core structure is present (lines, bumps, curves, loops)
- Student went outside the ghost guide — STILL VALID
- Letter is wobbly, lopsided, or child-sized — STILL VALID
- Minor extra marks or retry strokes — STILL VALID
- Mirrored letter (e.g. reversed b/d) — STILL VALID, note it

=== INVALID — Reject if: ===
- Pure random scribble with no letter shape
- Student completely filled/colored the ghost solid
- Drawing is a completely different letter/number/shape
- Canvas is empty or near-empty

=== RULES ===
- Be GENEROUS with genuine imperfect attempts
- Be STRICT only on: scribbles, solid fills, blank canvas
- Do NOT penalize for going outside the ghost boundary
- Do NOT penalize for shaky or slow strokes
- Do NOT penalize for retry marks on same canvas
- For b/d, p/q, n/u confusion — be extra generous

=== OUTPUT (JSON only, no extra text) ===
{
  "valid": true or false,
  "confidence": 0.0 to 1.0,
  "letter_detected": "letter the drawing looks like",
  "target_letter": "letter they should have written",
  "reason": "one sentence explanation",
  "encouragement": "warm fun message for the child",
  "encouragement_fil": "same message in Filipino/Tagalog",
  "tip": "one short tip if invalid, or null if valid"
}

=== CONFIDENCE GUIDE ===
0.9–1.0  clearly correct, well-formed
0.7–0.89 recognizable with minor issues
0.5–0.69 borderline but valid (messy)
0.3–0.49 attempted but hard to recognize
0.0–0.29 scribble or wrong shape

Passing threshold: confidence >= 0.45"""


@require_POST
def validate_handwriting(request):
    """
    AI handwriting validation endpoint using Gemini 2.0 Flash.
    Accepts: { image_b64: <data-url or raw base64>, target_letter: "B" }
    Returns: JSON matching the handwriting rubric schema.
    """
    try:
        data = json.loads(request.body)
        image_b64 = data.get('image_b64', '')
        target_letter = data.get('target_letter', '?')

        if not image_b64:
            return JsonResponse({'error': 'No image provided'}, status=400)

        # Strip the data URL prefix if present (data:image/png;base64,...)
        if ',' in image_b64:
            image_b64 = image_b64.split(',', 1)[1]

        api_key = os.getenv('GEMINI_API_KEY', '')
        if not api_key:
            # No key configured — return a permissive fallback
            return JsonResponse({
                'valid': True,
                'confidence': 0.75,
                'letter_detected': target_letter,
                'target_letter': target_letter,
                'reason': 'Validation skipped (no API key configured).',
                'encouragement': 'Great job drawing!',
                'encouragement_fil': 'Magaling! Patuloy ka!',
                'tip': None,
            })

        # Call Gemini
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=api_key)

            user_message = (
                f"The target letter is: '{target_letter}'\n"
                f"Please validate the child's handwriting in this canvas image."
            )

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[
                    types.Part.from_bytes(
                        data=base64.b64decode(image_b64),
                        mime_type='image/png'
                    ),
                    user_message,
                ],
                config=types.GenerateContentConfig(
                    system_instruction=HANDWRITING_SYSTEM_PROMPT,
                    response_mime_type='application/json',
                    temperature=0.1,
                ),
            )

            result_text = response.text.strip()
            # Strip markdown code fences if present
            if result_text.startswith('```'):
                result_text = result_text.split('\n', 1)[1]
                result_text = result_text.rsplit('```', 1)[0]

            result = json.loads(result_text)
            return JsonResponse(result)

        except Exception as gemini_err:
            # Gemini call failed (quota, network, etc.) — fallback to permissive pass
            print(f"[validate_handwriting] Gemini error: {gemini_err}")
            return JsonResponse({
                'valid': True,
                'confidence': 0.70,
                'letter_detected': target_letter,
                'target_letter': target_letter,
                'reason': 'AI validation unavailable, accepted by default.',
                'encouragement': 'Great job drawing!',
                'encouragement_fil': 'Magaling! Patuloy ka!',
                'tip': None,
            })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
