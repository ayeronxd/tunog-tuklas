import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
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
