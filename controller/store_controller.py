# store/controllers/store_controller.py
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from model.Dao.store_dao import CartDAO, OrderDAO, PurchaseDAO
from model.music.music_models import Song, Album
from django.urls import reverse
from django.utils import timezone


class CartController:
    @staticmethod
    def get_cart(user_id):
        """Obtiene todos los items del carrito (canciones y álbumes)"""
        return CartDAO.get_user_cart(user_id)

    @staticmethod
    def add_song_to_cart(request, song_id):
        """Añade una canción al carrito"""
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para añadir al carrito")
            return redirect('login')

        try:
            song = get_object_or_404(Song, id=song_id)

            if hasattr(song, 'stock') and song.stock < 1:
                messages.error(request, f"No hay stock disponible de {song.title}")
                return redirect('music_detail_id', id=song_id)

            success, message = CartDAO.add_song_to_cart(request.user.id, song_id)
            messages.success(request, message) if success else messages.info(request, message)
            return redirect('music_detail_id', id=song_id)

        except Exception as e:
            messages.error(request, f"Error al añadir al carrito: {str(e)}")
            return redirect('music_detail_id', id=song_id)

    @staticmethod
    def add_album_to_cart(request, album_id):
        """Añade un álbum al carrito"""
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para añadir al carrito")
            return redirect('login')

        try:
            album = get_object_or_404(Album, id=album_id)
            success, message = CartDAO.add_album_to_cart(request.user.id, album_id)
            messages.success(request, message) if success else messages.info(request, message)
            return redirect('album_detail', album_id=album_id)

        except Exception as e:
            messages.error(request, f"Error al añadir al carrito: {str(e)}")
            return redirect('album_detail', album_id=album_id)

    @staticmethod
    def remove_from_cart(request, item_id, item_type):
        """Elimina un item (canción o álbum) del carrito"""
        success = CartDAO.remove_from_cart(request.user.id, item_id, item_type)
        if success:
            messages.success(request, "Ítem eliminado del carrito")
        else:
            messages.error(request, "No se encontró el ítem en el carrito")
        return redirect('cart_view')

    @staticmethod
    def update_quantity(request, item_id, item_type, new_quantity):
        """Actualiza la cantidad de un item en el carrito"""
        if new_quantity <= 0:
            return CartController.remove_from_cart(request, item_id, item_type)

        if item_type == 'song':
            success = CartDAO.update_song_quantity(request.user.id, item_id, new_quantity)
        else:
            success = CartDAO.update_album_quantity(request.user.id, item_id, new_quantity)

        if success:
            messages.success(request, "Cantidad actualizada")
        else:
            messages.error(request, "No se pudo actualizar la cantidad")
        return redirect('cart_view')

    @staticmethod
    def calculate_cart_total(user_id):
        """Calcula el total del carrito"""
        cart_items = CartDAO.get_user_cart(user_id)
        return sum(item.subtotal for item in cart_items)

    @staticmethod
    def clear_cart(request):
        """Vacía todo el carrito del usuario"""
        count = CartDAO.clear_user_cart(request.user.id)
        if count > 0:
            messages.success(request, "Carrito vaciado")
        else:
            messages.info(request, "El carrito ya estaba vacío")
        return redirect('cart_view')


class OrderController:
    @staticmethod
    def create_order_from_cart(user_id):
        """Crea una orden a partir del carrito actual"""
        cart_items = CartDAO.get_user_cart(user_id)
        if not cart_items:
            return None

        total = sum(item.subtotal for item in cart_items)
        order_id = OrderDAO.create_order(user_id, total)

        # Convertir items del carrito a formato para la orden
        order_items = [{
            'item_id': item.song_id if item.item_type == 'song' else item.album_id,
            'item_type': item.item_type,
            'price': item.song_price if item.item_type == 'song' else item.album_price,
            'quantity': item.quantity
        } for item in cart_items]

        if OrderDAO.add_items_to_order(order_id, order_items):
            return order_id
        return None

    @staticmethod
    def get_order_details(order_id):
        """Obtiene los detalles de una orden específica"""
        return OrderDAO.get_order_by_id(order_id)

    @staticmethod
    def get_user_orders(user_id):
        """Obtiene todas las órdenes del usuario"""
        return OrderDAO.get_user_orders(user_id)


class PurchaseController:
    @staticmethod
    def process_purchase(request):
        """Procesa el checkout y realiza la compra"""
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para realizar una compra")
            return redirect('login')

        cart_items = CartDAO.get_user_cart(request.user.id)
        if not cart_items:
            messages.error(request, "Tu carrito está vacío")
            return redirect('cart_view')

        if request.method == 'POST':
            try:
                # Crear la orden
                order_id = OrderController.create_order_from_cart(request.user.id)
                if not order_id:
                    raise Exception("No se pudo crear la orden")

                # Preparar items para la compra
                purchase_items = [{
                    'item_id': item.song_id if item.item_type == 'song' else item.album_id,
                    'item_type': item.item_type,
                    'price': item.song_price if item.item_type == 'song' else item.album_price,
                    'quantity': item.quantity
                } for item in cart_items]

                # Crear registro de compra
                purchase_id = PurchaseDAO.create_purchase(
                    user_id=request.user.id,
                    order_id=order_id,
                    payment_method=request.POST.get('payment_method', 'tarjeta'),
                    total_price=sum(item.subtotal for item in cart_items),
                    items=purchase_items
                )

                # Vaciar carrito
                CartDAO.clear_user_cart(request.user.id)

                messages.success(request, "Compra realizada con éxito")
                return redirect('order_confirmation', order_id=order_id)

            except Exception as e:
                messages.error(request, f"Error al procesar la compra: {str(e)}")
                return redirect('checkout')

        # Mostrar página de pago (GET) - Actualizado para usar pago.html
        total = sum(item.subtotal for item in cart_items)
        payment_methods = [
            {'value': 'credit_card', 'label': 'Tarjeta de crédito'},
            {'value': 'paypal', 'label': 'PayPal'},
            {'value': 'bank_transfer', 'label': 'Transferencia bancaria'},
        ]

        return render(request, 'pago.html', {
            'order_id': 'US-' + str(timezone.now().strftime("%Y%m%d")),
            'order_date': timezone.now().strftime("%d/%m/%Y %H:%M"),
            'status': 'Pendiente de pago',
            'cart_items': cart_items,
            'total': total,
            'payment_methods': payment_methods
        })

    @staticmethod
    def get_purchase_history(user_id):
        """Obtiene el historial de compras del usuario"""
        return PurchaseDAO.get_user_purchases(user_id)

    @staticmethod
    def get_purchase_details(purchase_id):
        """Obtiene los detalles de una compra específica"""
        return PurchaseDAO.get_purchase_by_id(purchase_id)