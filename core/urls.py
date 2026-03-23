from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('mapa/', views.mapa, name='mapa'),
    path('letrang-mm/', views.letrang_m, name='letrang_m'),
    path('letrang-ii/', views.letrang_i, name='letrang_i'),
    path('api/save-progress/', views.save_progress, name='save_progress'),
]
