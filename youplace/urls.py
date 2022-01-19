from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('gm/', views.view_map_gm, name='view_map_gm'),
    path('jh/', views.view_map_jh, name='view_map_jh'),
    path('es/', views.view_map_es, name='view_map_es'),
]