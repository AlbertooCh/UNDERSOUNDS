from django.urls import path
from . import views

urlpatterns = [
    path('carrito/', views.carrito, name='carrito'),
    path('pago/', views.pago, name='pago'),
]