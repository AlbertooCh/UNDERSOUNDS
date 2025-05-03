# store/factory/store_factory.py
from model.store.store_models import CartItem, Order, Purchase, PurchaseDetail, OrderItem
from model.Dto.store_dto import CartItemDTO, OrderDTO, PurchaseDTO, PurchaseDetailDTO, OrderItemDTO

class StoreFactory:
    @staticmethod
    def create_cart_item_dto_from_model(cart_item: CartItem) -> CartItemDTO:
        if cart_item.song:
            # Obtener el artista de la canción
            artist_name = "Artista desconocido"
            if cart_item.song.artists.exists():  # Asumiendo relación ManyToMany
                artist = cart_item.song.artists.first()
                artist_name = artist.get_full_name() or artist.username

            return CartItemDTO(
                id=cart_item.id,
                user_id=cart_item.user.id,
                song_id=cart_item.song.id,
                song_title=cart_item.song.title,
                song_price=float(cart_item.song.price),
                quantity=cart_item.quantity,
                subtotal=float(cart_item.subtotal()),
                added_at=cart_item.added_at,
                item_type='song',
                artist_name=artist_name,
                cover_url=cart_item.song.song_cover.url if cart_item.song.song_cover else None
            )
        elif cart_item.album:
            # Obtener el artista del álbum
            artist_name = "Artista desconocido"
            if cart_item.album.artists.exists():  # Asumiendo relación ManyToMany
                artist = cart_item.album.artists.first()
                artist_name = artist.get_full_name() or artist.username

            return CartItemDTO(
                id=cart_item.id,
                user_id=cart_item.user.id,
                album_id=cart_item.album.id,
                album_title=cart_item.album.title,
                album_price=float(cart_item.album.price),
                quantity=cart_item.quantity,
                subtotal=float(cart_item.subtotal()),
                added_at=cart_item.added_at,
                item_type='album',
                artist_name=artist_name,
                cover_url=cart_item.album.album_cover.url if cart_item.album.album_cover else None
            )

    @staticmethod
    def create_order_dto_from_model(order: Order) -> OrderDTO:
        return OrderDTO(
            id=order.id,
            user_id=order.user.id,
            total=float(order.total_amount),
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at,
            items=[StoreFactory.create_order_item_dto_from_model(item) for item in order.items.all()]
        )

    @staticmethod
    def create_order_item_dto_from_model(item: OrderItem) -> OrderItemDTO:
        if item.item_type == 'song' and item.song:
            return OrderItemDTO(
                id=item.id,
                order_id=item.order.id,
                item_type='song',
                song_id=item.song.id,
                song_title=item.song.title,
                price=float(item.price),
                quantity=item.quantity,
                subtotal=float(item.subtotal())
            )
        elif item.item_type == 'album' and item.album:
            return OrderItemDTO(
                id=item.id,
                order_id=item.order.id,
                item_type='album',
                album_id=item.album.id,
                album_title=item.album.title,
                price=float(item.price),
                quantity=item.quantity,
                subtotal=float(item.subtotal())
            )

    @staticmethod
    def create_purchase_dto_from_model(purchase: Purchase) -> PurchaseDTO:
        return PurchaseDTO(
            id=purchase.id,
            user_id=purchase.user.id,
            total_price=float(purchase.total_price),
            purchase_date=purchase.purchase_date,
            payment_method=purchase.payment_method,
            details=[StoreFactory.create_purchase_detail_dto_from_model(d) for d in purchase.details.all()]
        )

    @staticmethod
    def create_purchase_detail_dto_from_model(detail: PurchaseDetail) -> PurchaseDetailDTO:
        if detail.song:
            return PurchaseDetailDTO(
                id=detail.id,
                purchase_id=detail.purchase.id,
                item_type='song',
                song_id=detail.song.id,
                song_title=detail.song.title,
                price=float(detail.price),
                quantity=detail.quantity,
                subtotal=float(detail.subtotal())
            )
        elif detail.album:
            return PurchaseDetailDTO(
                id=detail.id,
                purchase_id=detail.purchase.id,
                item_type='album',
                album_id=detail.album.id,
                album_title=detail.album.title,
                price=float(detail.price),
                quantity=detail.quantity,
                subtotal=float(detail.subtotal())
            )