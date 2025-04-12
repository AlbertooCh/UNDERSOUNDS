from django.urls import path
from view.user.views import (
    login_view,
    logout_view,
    register_fan,
    register_artist,
    perfil,
    configuracion,
    historial_compras,
    mis_obras
)
from django.shortcuts import render

urlpatterns = [
    # Autenticación
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Registros
    path('register/', register_fan, name='register'),
    path('register/artist/', register_artist, name='artist_register'),

    # Perfil y áreas privadas
    path('perfil/', perfil, name='perfil'),
    path('user/configuracion/', configuracion, name='configuracion'),
    path('user/historial_compras/', historial_compras, name='historial_compras'),
    path('user/mis_obras/', mis_obras, name='mis_obras'),

    # Home temporal (puedes cambiarlo luego por una vista específica)
    path('', lambda request: render(request, 'home.html'), name='home'),
]