from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('mapa/', views.mapa, name='mapa'),
    
    # ── MGA LETRA ──
    path('letrang-mm/', views.letrang_m, name='letrang_m'),
    path('letrang-ii/', views.letrang_i, name='letrang_i'),
    path('letrang-oo/', views.letrang_o, name='letrang_o'),
    path('letrang-bb/', views.letrang_b, name='letrang_b'),
    path('letrang-ee/', views.letrang_e, name='letrang_e'),
    path('letrang-uu/', views.letrang_u, name='letrang_u'),
    path('letrang-tt/', views.letrang_t, name='letrang_t'),
    path('letrang-kk/', views.letrang_k, name='letrang_k'),
    path('letrang-ll/', views.letrang_l, name='letrang_l'),
    path('letrang-yy/', views.letrang_y, name='letrang_y'),
    path('letrang-nn/', views.letrang_n, name='letrang_n'),
    path('letrang-gg/', views.letrang_g, name='letrang_g'),
    path('letrang-ngng/', views.letrang_ng, name='letrang_ng'),
    path('letrang-pp/', views.letrang_p, name='letrang_p'),
    path('letrang-rr/', views.letrang_r, name='letrang_r'),
    path('letrang-dd/', views.letrang_d, name='letrang_d'),

    # ── MGA LETRA (agdag) ──
    path('letrang-h/', views.letrang_h, name='letrang_h'),
    path('letrang-w/', views.letrang_w, name='letrang_w'),

    # ── APIs ──
    path('api/save-progress/', views.save_progress, name='save_progress'),
    path('api/validate-handwriting/', views.validate_handwriting, name='validate_handwriting'),
]