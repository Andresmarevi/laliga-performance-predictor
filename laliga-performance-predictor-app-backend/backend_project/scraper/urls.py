from django.urls import path
from . import views

urlpatterns = [
    path("player-info/", views.player_info, name="player_info"),
    path('api/player-season-stats/', views.player_season_stats, name='player_season_stats'),
    path('api/player-last-match-stats/', views.player_last_match_stats, name='player_last_match_stats'),
    path('api/predict-performance/', views.predict_performance, name='predict_performance'),
    path('api/player-performance-evolution/', views.player_performance_evolution, name='player_performance_evolution'),
]
