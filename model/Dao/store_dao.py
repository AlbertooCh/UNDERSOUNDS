# store/dao/store_dao.py
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from model.store.store_models import CartItem, Order, Purchase, PurchaseDetail, OrderItem, AlbumPurchase
from model.Dto.store_dto import CartItemDTO, OrderDTO, PurchaseDTO, PurchaseDetailDTO
from model.Factory.store_factory import StoreFactory


class CartDAO:
    @staticmethod
    def get_user_cart(user_id):
        cart_items = CartItem.objects.filter(user_id=user_id).select_related('song', 'album')
        return [StoreFactory.create_cart_item_dto_from_model(item) for item in cart_items]

    @staticmethod
    def add_song_to_cart(user_id, song_id, quantity=1):
        try:
            item = CartItem.objects.get(user_id=user_id, song_id=song_id)
            item.quantity += quantity
            item.save()
            return (True, "Cantidad actualizada en el carrito")
        except CartItem.DoesNotExist:
            CartItem.objects.create(
                user_id=user_id,
                song_id=song_id,
                quantity=quantity
            )
            return (True, "Canción añadida al carrito")
        except Exception as e:
            return (False, str(e))

    @staticmethod
    def add_album_to_cart(user_id, album_id, quantity=1):
        try:
            item = CartItem.objects.get(user_id=user_id, album_id=album_id)
            item.quantity += quantity
            item.save()
            return (True, "Cantidad actualizada en el carrito")
        except CartItem.DoesNotExist:
            CartItem.objects.create(
                user_id=user_id,
                album_id=album_id,
                quantity=quantity
            )
            return (True, "Álbum añadido al carrito")
        except Exception as e:
            return (False, str(e))

    @staticmethod
    def remove_from_cart(user_id, item_id, item_type):
        if item_type == 'song':
            deleted_count, _ = CartItem.objects.filter(user_id=user_id, song_id=item_id).delete()
        else:
            deleted_count, _ = CartItem.objects.filter(user_id=user_id, album_id=item_id).delete()
        return deleted_count > 0

    @staticmethod
    def clear_user_cart(user_id):
        deleted_count, _ = CartItem.objects.filter(user_id=user_id).delete()
        return deleted_count


class OrderDAO:
    @staticmethod
    def create_order(user_id, total=0):
        order = Order.objects.create(user_id=user_id, total_amount=total)
        return order.id

    @staticmethod
    def add_items_to_order(order_id, items):
        try:
            with transaction.atomic():
                order = Order.objects.get(id=order_id)
                order_items = []

                for item in items:
                    order_item = OrderItem(
                        order=order,
                        price=item['price'],
                        quantity=item['quantity']
                    )

                    if item['item_type'] == 'song':
                        order_item.song_id = item['item_id']
                        order_item.item_type = 'song'
                    else:
                        order_item.album_id = item['item_id']
                        order_item.item_type = 'album'

                    order_items.append(order_item)

                OrderItem.objects.bulk_create(order_items)
                order.update_total()
                return True
        except Exception as e:
            print(f"Error adding items to order: {str(e)}")
            return False

    @staticmethod
    def get_user_orders(user_id):
        orders = Order.objects.filter(user_id=user_id).prefetch_related(
            'items__song',
            'items__album'
        ).order_by('-created_at')
        return [StoreFactory.create_order_dto_from_model(order) for order in orders]

    @staticmethod
    def get_order_by_id(order_id):
        try:
            order = Order.objects.get(id=order_id)
            return StoreFactory.create_order_dto_from_model(order)
        except ObjectDoesNotExist:
            return None
        except Exception as e:
            print(f"Error retrieving order: {str(e)}")
            return None


class PurchaseDAO:
    @staticmethod
    def create_purchase(user_id, total_price, items, payment_method, order_id=None):
        with transaction.atomic():
            purchase = Purchase.objects.create(
                user_id=user_id,
                total_price=total_price,
                payment_method=payment_method,
                order_id=order_id
            )

            # Crear detalles de compra
            purchase_details = []
            album_purchases = []

            for item in items:
                if item['item_type'] == 'song':
                    detail = PurchaseDetail(
                        purchase=purchase,
                        song_id=item['item_id'],
                        price=item['price'],
                        quantity=item['quantity']
                    )
                else:
                    detail = PurchaseDetail(
                        purchase=purchase,
                        album_id=item['item_id'],
                        price=item['price'],
                        quantity=item['quantity']
                    )
                    # Registrar compra de álbum completo
                    album_purchases.append(
                        AlbumPurchase(
                            user_id=user_id,
                            album_id=item['item_id'],
                            order_id=order_id,
                            price=item['price']
                        )
                    )

                purchase_details.append(detail)

            PurchaseDetail.objects.bulk_create(purchase_details)

            if album_purchases:
                AlbumPurchase.objects.bulk_create(album_purchases)

            return purchase.id

    @staticmethod
    def get_user_purchases(user_id):
        purchases = Purchase.objects.filter(user_id=user_id).prefetch_related(
            'details__song',
            'details__album'
        ).order_by('-purchase_date')
        return [StoreFactory.create_purchase_dto_from_model(p) for p in purchases]