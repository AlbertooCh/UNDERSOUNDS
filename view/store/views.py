from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from model.store.store_models import CartItem, Order, Purchase, PurchaseDetail
from model.music.music_models import Song
from controller.store_controller import PurchaseController, CartController, OrderController


# Create your views here.

@login_required
def order_confirmation(request, order_id):
    # Obtiene el pedido del usuario autenticado; se asume que el modelo Order tiene un campo
    # de fecha de compra, id y total
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_confirmation.html', {'order': order})

@login_required
def carrito(request):
    # Obtenemos los items del carrito para el usuario autenticado
    cart_items = CartItem.objects.filter(user=request.user)

    # Calculamos el total sumando los subtotales de cada ítem
    total = sum(item.subtotal() for item in cart_items)

    context = {
        'items': cart_items,
        'total': total,
    }
    return render(request, "carrito.html", context)


@login_required
def add_to_cart(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        song=song,
        defaults={'quantity': 1}
    )
    if not created:
        # Si ya existe, incrementamos la cantidad
        cart_item.quantity += 1
        cart_item.save()

    return redirect('carrito')


@login_required
def remove_from_cart(request, song_id):
    cart_item = CartItem.objects.filter(user=request.user, song__id=song_id).first()
    if cart_item:
        cart_item.delete()

    return redirect('carrito')


@login_required
def pago(request):
    # Obtenemos los items del carrito
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        # Si no hay items, redirigimos al catálogo o mostramos un mensaje
        return redirect('catalogo')

    total = sum(item.subtotal() for item in cart_items)

    if request.method == 'POST':
        # Una vez confirmado el pago, creamos la orden
        order = Order.objects.create(user=request.user, total=total)
        # Creación de los detalles de compra para cada ítem
        for item in cart_items:
            # Aquí se asume el modelo PurchaseDetail y que 'item.song.price' es el precio en el momento de la compra.
            PurchaseDetail.objects.create(
                purchase=order,
                song=item.song,
                price=item.song.price
            )

        # Eliminamos los items del carrito (si se desea limpiar después de la compra)
        cart_items.delete()

        # Redirigimos a una página de confirmación de pedido
        return redirect('order_confirmation', order_id=order.id)

    context = {
        'items': cart_items,
        'total': total,
    }
    return render(request, 'pago.html', context)

def purchase_success(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id, user=request.user)
    return render(request, 'order_confirmation.html', {'purchase': purchase})

