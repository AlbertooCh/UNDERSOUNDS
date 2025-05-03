from django.urls import path
from view.store import views
from controller.store_controller import CartController, PurchaseController


urlpatterns = [
    path('carrito/', views.carrito, name='carrito'),
    path('add/song/<int:song_id>/', views.add_song_to_cart, name='add_song_to_cart'),
    path('add/album/<int:album_id>/', views.add_album_to_cart, name='add_album_to_cart'),
    path('remove/<str:item_type>/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<str:item_type>/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('pago/', PurchaseController.process_purchase, name='pago'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/confirm/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('purchase/history/', views.purchase_history, name='purchase_history'),
    path('purchase/success/<int:purchase_id>/', views.purchase_success, name='purchase_success'),
]