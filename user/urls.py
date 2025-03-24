from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('perfil/', views.perfil, name='perfil'),
    path('user/configuracion/', views.configuracion, name='configuracion'),
    path('user/historial_compras/', views.historial_compras, name='historial_compras'),
    path('user/mis_obras/', views.mis_obras, name='mis_obras'),
]