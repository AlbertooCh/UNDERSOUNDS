from django.urls import path
from view.store import views

urlpatterns = [
    path('carrito/', views.carrito, name='carrito'),
    path('pago/', views.pago, name='pago'),
]