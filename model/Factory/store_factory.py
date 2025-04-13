# store/factory/store_factory.py
from model.store.store_models import CartItem, Order, Purchase, PurchaseDetail
from model.Dto.store_dto import CartItemDTO, OrderDTO, PurchaseDTO, PurchaseDetailDTO

class StoreFactory:
    @staticmethod
    def create_cart_item_dto_from_model(cart_item: CartItem) -> CartItemDTO:
        return CartItemDTO(
            id=cart_item.id,
            user_id=cart_item.user.id,
            song_id=cart_item.song.id,
            song_title=cart_item.song.title,
            song_price=float(cart_item.song.price),
            quantity=cart_item.quantity,
            subtotal=float(cart_item.subtotal()),
            added_at=cart_item.added_at
        )

    def create_order_dto_from_model(order: Order) -> OrderDTO:
        return OrderDTO(
            id=order.id,
            user_id=order.user.id,
            total=float(order.total),  # Ahora usa la propiedad
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at,
            items=[StoreFactory.create_order_item_dto_from_model(item) for item in order.items.all()]
        )

    @staticmethod
    def create_purchase_dto_from_model(purchase: Purchase) -> PurchaseDTO:
        details = purchase.details.all()
        return PurchaseDTO(
            id=purchase.id,
            user_id=purchase.user.id,
            total_price=float(purchase.total_price),
            purchase_date=purchase.purchase_date,
            payment_method=purchase.payment_method,
            details=[StoreFactory.create_purchase_detail_dto_from_model(d) for d in details]
        )

    @staticmethod
    def create_order_item_dto_from_model(item) -> CartItemDTO:
        return CartItemDTO(
            song_id=item.song.id,
            song_title=item.song.title,
            song_price=float(item.price),
            quantity=item.quantity,
            subtotal=float(item.subtotal())
        )

    @staticmethod
    def create_purchase_detail_dto_from_model(detail: PurchaseDetail) -> PurchaseDetailDTO:
        return PurchaseDetailDTO(
            id=detail.id,
            purchase_id=detail.purchase.id,
            song_id=detail.song.id,
            song_title=detail.song.title,
            price=float(detail.price),
            quantity=detail.quantity,
            subtotal=float(detail.subtotal())
        )

    @staticmethod
    def create_cart_item_from_dto(cart_item_dto: CartItemDTO) -> CartItem:
        cart_item = CartItem(
            user_id=cart_item_dto.user_id,
            song_id=cart_item_dto.song_id,
            quantity=cart_item_dto.quantity
        )
        return cart_item