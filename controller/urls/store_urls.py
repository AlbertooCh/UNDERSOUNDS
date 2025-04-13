from django.urls import path
from view.store import views
from controller.store_controller import CartController, PurchaseController


urlpatterns = [
    path('carrito/', views.carrito, name='carrito'),
    path('cart/add/<int:song_id>/', CartController.add_to_cart, name='add_to_cart'),
    path('update_cart_quantity/<int:song_id>/', CartController.update_quantity, name='update_cart_quantity'),
    path('cart/remove/<int:song_id>/', CartController.remove_from_cart, name='remove_from_cart'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('pago/', PurchaseController.process_purchase, name='pago'),
]