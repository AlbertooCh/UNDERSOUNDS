from django.urls import path
from view.user.views import (
    login_view,
    logout_view,
    register_fan,
    register_artist,
    perfil,
    configuracion,
    historial_compras,
    mis_obras,
    upload_avatar,
    update_profile,
    delete_account,
    deactivate_account,
    change_password,
    order_history,
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
    path('user/historial_compras/', order_history, name='historial_compras'),
    path('upload-avatar/', upload_avatar, name='upload_avatar'),
    path('update_profile/', update_profile, name='update_profile'),
    path('delete_account/', delete_account, name='delete_account'),
    path('deactivate_account/', deactivate_account, name='deactivate_account'),
    path('change_password/', change_password, name='change_password'),

]