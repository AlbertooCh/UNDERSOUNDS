# store/dao/store_dao.py
from django.core.exceptions import ObjectDoesNotExist
from model.store.store_models import CartItem, Order, Purchase, PurchaseDetail
from model.Dto.store_dto import CartItemDTO, OrderDTO, PurchaseDTO, PurchaseDetailDTO
from model.Factory.store_factory import StoreFactory


class CartDAO:
    @staticmethod
    def get_user_cart(user_id):
        cart_items = CartItem.objects.filter(user_id=user_id).select_related('song')
        return [StoreFactory.create_cart_item_dto_from_model(item) for item in cart_items]

    @staticmethod
    def add_to_cart(user_id, song_id, quantity=1):
        try:
            item = CartItem.objects.get(user_id=user_id, song_id=song_id)
            item.quantity += quantity
            item.save()
        except ObjectDoesNotExist:
            item = CartItem.objects.create(
                user_id=user_id,
                song_id=song_id,
                quantity=quantity
            )
        return item.id

    @staticmethod
    def remove_from_cart(user_id, song_id):
        deleted_count, _ = CartItem.objects.filter(user_id=user_id, song_id=song_id).delete()
        return deleted_count > 0

    @staticmethod
    def update_cart_item_quantity(user_id, song_id, new_quantity):
        if new_quantity <= 0:
            return CartDAO.remove_from_cart(user_id, song_id)

        updated_count = CartItem.objects.filter(
            user_id=user_id,
            song_id=song_id
        ).update(quantity=new_quantity)

        return updated_count > 0

    @staticmethod
    def clear_user_cart(user_id):
        deleted_count, _ = CartItem.objects.filter(user_id=user_id).delete()
        return deleted_count


class OrderDAO:
    @staticmethod
    def create_order(user_id, total, status='pending'):
        order = Order.objects.create(
            user_id=user_id,
            total=total,
            status=status
        )
        return order.id

    @staticmethod
    def get_order_by_id(order_id):
        try:
            order = Order.objects.get(id=order_id)
            return StoreFactory.create_order_dto_from_model(order)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_user_orders(user_id):
        orders = Order.objects.filter(user_id=user_id).order_by('-created_at')
        return [StoreFactory.create_order_dto_from_model(order) for order in orders]


class PurchaseDAO:
    @staticmethod
    def create_purchase(user_id, total_price, items, payment_method=None):
        purchase = Purchase.objects.create(
            user_id=user_id,
            total_price=total_price,
            payment_method=payment_method
        )

        for item in items:
            PurchaseDetail.objects.create(
                purchase=purchase,
                song_id=item['song_id'],
                price=item['price'],
                quantity=item.get('quantity', 1)
            )

        return purchase.id

    @staticmethod
    def get_purchase_by_id(purchase_id):
        try:
            purchase = Purchase.objects.get(id=purchase_id)
            return StoreFactory.create_purchase_dto_from_model(purchase)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_user_purchases(user_id):
        purchases = Purchase.objects.filter(user_id=user_id).order_by('-purchase_date')
        return [StoreFactory.create_purchase_dto_from_model(p) for p in purchases]