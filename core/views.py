from django.shortcuts import render
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

        map_nodes.append({
            'id': level.id,
            'name': level.name.replace("Letrang ", ""), # Extract just the letter (M, B, etc)
            'pos_top': level.pos_top,
            'pos_left': level.pos_left,
            'status': node_status,
            'stars': stars
        })

    # If all levels are completed, the last one might just stay completed, no active node.
    active_node = next((n for n in map_nodes if n['status'] == 'active'), None)

    context = {
        'map_nodes': map_nodes,
        'total_stars': total_earned_stars,
        'max_stars': max_possible_stars,
        'active_node': active_node,
    }
    
    return render(request, 'core/mapa.html', context)
