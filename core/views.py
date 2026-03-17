from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    """View for the landing page."""
    return render(request, 'core/index.html')

@login_required
def mapa(request):
    """View for the map page."""
    return render(request, 'core/mapa.html')
