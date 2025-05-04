from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from model.store.store_models import CartItem, Order, Purchase
from model.music.music_models import Song, Album
from user.models import User
from controller.store_controller import PurchaseController, CartController, OrderController
from model.Dto.store_dto import CartItemDTO
from model.Dao.store_dao import CartDAO


@login_required
def order_confirmation(request, order_id):
    """
    Vista de confirmación de compra que muestra los detalles basados en el modelo Purchase
    pero vinculado a un Order específico del usuario.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    purchase = get_object_or_404(Purchase, order=order)

    return render(request, 'order_confirmation.html', {
        'order': order,
        'purchase': purchase,
    })


@login_required
def carrito(request):
    """Vista del carrito de compras que muestra items de ambos tipos"""
    cart_items = CartController.get_cart(request.user.id)  # Esto ahora incluye artist_name y cover_url
    total = CartController.calculate_cart_total(request.user.id)

    context = {
        'items': cart_items,  # Ahora podemos pasar los DTOs directamente
        'total': total,
    }
    return render(request, "carrito.html", context)


@login_required
def add_song_to_cart(request, song_id):
    """Añade una canción al carrito"""
    return CartController.add_song_to_cart(request, song_id)


@login_required
def add_album_to_cart(request, album_id):
    """Añade un álbum al carrito"""
    return CartController.add_album_to_cart(request, album_id)


@login_required
def remove_from_cart(request, item_id, item_type):
    """Elimina un item del carrito (puede ser canción o álbum)"""
    return CartController.remove_from_cart(request, item_id, item_type)


@login_required
def update_cart_item(request, item_id, item_type):
    """Actualiza la cantidad de un item en el carrito"""
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 1))
        return CartController.update_quantity(request, item_id, item_type, new_quantity)
    return redirect('carrito')


def pago(request):
    if request.method == 'GET':
        cart_items = CartDAO.get_user_cart(request.user.id)
        total = sum(float(item.subtotal) for item in cart_items)
        context = {
            'cart_items': cart_items,
            'total': total,
            'payment_methods': [
                {'value': 'tarjeta', 'label': 'Tarjeta de crédito/débito'},
                {'value': 'paypal', 'label': 'PayPal'},
                {'value': 'bizum', 'label': 'Bizum'},
            ]
        }
        return render(request, 'pago.html', context)

    elif request.method == 'POST':
        return PurchaseController.process_purchase(request)

@login_required
def pago_view(request):
    if request.method == 'GET':
        cart_items = CartDAO.get_user_cart(request.user.id)
        total = sum(float(item.subtotal) for item in cart_items)

        context = {
            'cart_items': cart_items,
            'total': total,
            'payment_methods': [
                {'value': 'tarjeta', 'label': 'Tarjeta de crédito/débito'},
                {'value': 'paypal', 'label': 'PayPal'},
                {'value': 'bizum', 'label': 'Bizum'},
            ]
        }
        return render(request, 'pago.html', context)

    elif request.method == 'POST':
        return StoreController.process_purchase(request)

@login_required
def purchase_success(request, purchase_id):
    """Vista de éxito de compra (similar a order_confirmation pero por purchase_id)"""
    purchase = get_object_or_404(Purchase, id=purchase_id, user=request.user)
    return render(request, 'order_confirmation.html', {
        'purchase': purchase,
        'order': purchase.order  # Asumiendo que Purchase tiene relación con Order
    })


@login_required
def order_detail(request, order_id):
    """Detalle de una orden específica"""
    order = OrderController.get_order_details(order_id)
    if not order or order.user_id != request.user.id:
        return redirect('catalogo')

    return render(request, 'order_detail.html', {
        'order': order,
        'items': order.items  # Los items ya vienen incluidos en el OrderDTO
    })


@login_required
def purchase_history(request):
    """Historial de compras del usuario"""
    purchases = PurchaseController.get_purchase_history(request.user.id)
    return render(request, 'purchase_history.html', {
        'purchases': purchases
    })