# store/dto/store_dto.py
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class CartItemDTO:
    id: int = None
    user_id: int = None
    song_id: Optional[int] = None
    album_id: Optional[int] = None
    song_title: Optional[str] = None
    album_title: Optional[str] = None
    song_price: Optional[float] = None
    album_price: Optional[float] = None
    quantity: int = 1
    subtotal: float = None
    added_at: datetime = None
    item_type: str = 'song'  # 'song' o 'album'
    artist_name: Optional[str] = None  # Nuevo campo
    cover_url: Optional[str] = None  # Nuevo campo para la imagen

@dataclass
class OrderItemDTO:
    id: int = None
    order_id: int = None
    item_type: str = 'song'  # 'song' o 'album'
    song_id: Optional[int] = None
    album_id: Optional[int] = None
    song_title: Optional[str] = None
    album_title: Optional[str] = None
    price: float = None
    quantity: int = 1
    subtotal: float = None

@dataclass
class OrderDTO:
    id: int = None
    user_id: int = None
    total: float = None
    status: str = None
    created_at: datetime = None
    updated_at: datetime = None
    items: List[OrderItemDTO] = None

@dataclass
class PurchaseDTO:
    id: int = None
    user_id: int = None
    total_price: float = None
    purchase_date: datetime = None
    payment_method: str = None
    details: List['PurchaseDetailDTO'] = None

@dataclass
class PurchaseDetailDTO:
    id: int = None
    purchase_id: int = None
    item_type: str = 'song'  # 'song' o 'album'
    song_id: Optional[int] = None
    album_id: Optional[int] = None
    song_title: Optional[str] = None
    album_title: Optional[str] = None
    price: float = None
    quantity: int = 1
    subtotal: float = None