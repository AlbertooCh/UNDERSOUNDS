# store/dto/store_dto.py
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class CartItemDTO:
    id: int = None
    user_id: int = None
    song_id: int = None
    song_title: str = None
    song_price: float = None
    quantity: int = 1
    subtotal: float = None
    added_at: datetime = None

@dataclass
class OrderDTO:
    id: int = None
    user_id: int = None
    total: float = None
    status: str = None
    created_at: datetime = None
    updated_at: datetime = None
    items: List[CartItemDTO] = None

    @property
    def total(self):
        return sum(item.subtotal for item in self.items) if self.items else 0

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
    song_id: int = None
    song_title: str = None
    price: float = None
    quantity: int = 1
    subtotal: float = None