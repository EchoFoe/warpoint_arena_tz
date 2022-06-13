from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'api/players', views.PlayerList, basename='player')
router.register(r'api/teams', views.TeamList, basename='team')
router.register(r'api/fractions', views.FractionList, basename='fraction')

app_name = 'gamers'

urlpatterns = [
    path('', views.home, name='home'),
    path('players_list/', views.players_list, name='players_list'),
    path('', include(router.urls,)),
    path('api/players/', views.PlayerList.as_view({'get': 'list'}), name='api_players'),
    path('api/departments/', views.TeamList.as_view({'get': 'list'}), name='api_teams'),
    path('api/projects/', views.FractionList.as_view({'get': 'list'}), name='api_fractions')
]
urlpatterns += router.urls
