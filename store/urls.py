from django.conf.urls import url
from . import views

urlpatterns = [
    path('carrito/', views.carrito, name='carrito'),
    path('pago/', views.pago, name='pago'),
]