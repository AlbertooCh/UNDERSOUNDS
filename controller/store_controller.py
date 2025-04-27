# store/controllers/store_controller.py
from django.contrib import messages
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from model.Dao.store_dao import CartDAO, OrderDAO, PurchaseDAO
from model.Dto.store_dto import CartItemDTO, OrderDTO, PurchaseDTO
from model.music.music_models import Song
from model.store.store_models import CartItem, Order, Purchase, PurchaseDetail, OrderItem
from django.urls import reverse


class CartController:
    @staticmethod
    def get_cart(user_id):
        return CartDAO.get_user_cart(user_id)

    @staticmethod
    def add_to_cart(request, song_id):
        """
        Maneja la adición al carrito y redirecciona
        Args:
            request: HttpRequest con el usuario
            song_id: ID de la canción a añadir
        Returns:
            HttpResponseRedirect
        """
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para añadir al carrito")
            return redirect('login')

        try:
            song = get_object_or_404(Song, id=song_id)

            # Verificar stock si es necesario
            if hasattr(song, 'stock') and song.stock < 1:
                messages.error(request, f"No hay stock disponible de {song.title}")
                return redirect('music_detail_id', id=song_id)

            # Añadir al carrito (devuelve tupla (success, message))
            success, message = CartDAO.add_to_cart(request.user.id, song_id)

            if success:
                messages.success(request, message)
            else:
                messages.info(request, message)  # Usamos info en lugar de error para duplicados

            return redirect('music_detail_id', id=song_id)

        except Song.DoesNotExist:
            messages.error(request, "La canción no existe")
            return redirect('inicio')
        except Exception as e:
            messages.error(request, f"Error al añadir al carrito: la canción ya está añadida")
            return redirect('music_detail_id', id=song_id)

    @staticmethod
    def remove_from_cart(request, song_id):
        success = CartDAO.remove_from_cart(request.user.id, song_id)
        if success:
            messages.success(request, "Canción eliminada del carrito")
        else:
            messages.error(request, "No se encontró la canción en el carrito")
        return redirect('carrito')

    @staticmethod
    def update_quantity(request, song_id, new_quantity):
        if new_quantity <= 0:
            return CartController.remove_from_cart(request, song_id)

        success = CartDAO.update_cart_item_quantity(request.user.id, song_id, new_quantity)
        if success:
            messages.success(request, "Cantidad actualizada")
        else:
            messages.error(request, "No se pudo actualizar la cantidad")
        return success

    @staticmethod
    def calculate_cart_total(user_id):
        cart_items = CartDAO.get_user_cart(user_id)
        return sum(item.subtotal for item in cart_items)

    @staticmethod
    def clear_cart(request):
        count = CartDAO.clear_user_cart(request.user.id)
        if count > 0:
            messages.success(request, "Carrito vaciado")
        else:
            messages.info(request, "El carrito ya estaba vacío")
        return count


class OrderController:
    @staticmethod
    def create_order_from_cart(user_id):
        cart_items = CartDAO.get_user_cart(user_id)
        if not cart_items:
            return None

        total = sum(item.subtotal for item in cart_items)
        order_id = OrderDAO.create_order(user_id, total)
        return order_id

    @staticmethod
    def get_user_orders(user_id):
        return OrderDAO.get_user_orders(user_id)


class PurchaseController:
    @staticmethod
    def process_purchase(request):
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para realizar una compra")
            return redirect('login')

        cart_items = CartDAO.get_user_cart(request.user.id)
        if not cart_items:
            messages.error(request, "Tu carrito está vacío")
            return redirect('carrito')

        if request.method == 'POST':
            # 1. Crear la orden
            order_id = OrderDAO.create_order(request.user.id)

            # 2. Convertir items del carrito a items de orden
            order_items = [{
                'song_id': item.song_id,
                'price': item.song_price,
                'quantity': item.quantity
            } for item in cart_items]

            OrderDAO.add_items_to_order(order_id, order_items)


            # 3. Crear la compra (registro financiero)
            purchase_id = PurchaseDAO.create_purchase(
                user_id=request.user.id,
                order_id=order_id,
                payment_method=request.POST.get('payment_method', 'tarjeta'),
                total_price=sum(item.subtotal for item in cart_items),
                items=order_items
            )

            # 4. Vaciar el carrito
            CartDAO.clear_user_cart(request.user.id)

            # 5. Redirigir a confirmación
            return redirect('order_confirmation', order_id=order_id)

        # Mostrar formulario de pago (GET)
        total = sum(item.subtotal for item in cart_items)
        return render(request, 'pago.html', {
            'cart_items': cart_items,
            'total': total
        })

    @staticmethod
    def get_purchase_history(user_id):
        return PurchaseDAO.get_user_purchases(user_id)