from django.urls import path
from view.store import views

urlpatterns = [
    path('carrito/', views.carrito, name='carrito'),
    path('pago/', views.pago, name='pago'),
    path('add_to_cart/<int:song_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:song_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]