from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('mapa/', views.mapa, name='mapa'),
    path('letrang-mm/', views.letrang_m, name='letrang_m'),
    path('letrang-ii/', views.letrang_i, name='letrang_i'),
    path('letrang-oo/', views.letrang_o, name='letrang_o'),
    path('letrang-bb/', views.letrang_b, name='letrang_b'),
    path('letrang-ee/', views.letrang_e, name='letrang_e'),
    path('api/save-progress/', views.save_progress, name='save_progress'),
    path('api/validate-handwriting/', views.validate_handwriting, name='validate_handwriting'),
]
