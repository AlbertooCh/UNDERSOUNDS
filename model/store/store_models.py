# model/store/store_models.py
from django.utils import timezone
from django.db import models
from django.conf import settings
from user.models import User
from model.music.music_models import Song, Album  # Añadir import de Album


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='in_carts', null=True, blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='in_carts', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'store'
        unique_together = [('user', 'song'), ('user', 'album')]  # Modificado para soportar ambos

    def subtotal(self):
        if self.song:
            return self.quantity * self.song.price
        elif self.album:
            return self.quantity * self.album.price
        return 0

    def __str__(self):
        if self.song:
            return f"{self.song.title} ({self.quantity})"
        elif self.album:
            return f"Álbum: {self.album.title} ({self.quantity})"
        return "Ítem inválido"


class OrderItem(models.Model):
    ITEM_TYPE_CHOICES = [
        ('song', 'Canción'),
        ('album', 'Álbum'),
    ]

    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField(
        max_length=10,
        choices=ITEM_TYPE_CHOICES,
        default='song'  # Valor por defecto para migraciones existentes
    )
    song = models.ForeignKey(Song, on_delete=models.PROTECT, null=True, blank=True)
    album = models.ForeignKey(Album, on_delete=models.PROTECT, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        app_label = 'store'

    def save(self, *args, **kwargs):
        # Auto-determina el tipo basado en qué relación está establecida
        if self.song_id and not self.item_type:
            self.item_type = 'song'
        elif self.album_id and not self.item_type:
            self.item_type = 'album'
        super().save(*args, **kwargs)

    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        if self.item_type == 'song' and self.song:
            return f"{self.song.title} (x{self.quantity}) in Order #{self.order.id}"
        elif self.item_type == 'album' and self.album:
            return f"Álbum: {self.album.title} (x{self.quantity}) in Order #{self.order.id}"
        return f"OrderItem #{self.id} (Tipo: {self.item_type})"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)  # Nuevo campo útil para pagos
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Mejoramos el cálculo

    @property
    def total(self):
        """Mantengo esta property por compatibilidad, pero usamos total_amount como campo real"""
        return self.total_amount or sum(item.subtotal() for item in self.items.all())

    class Meta:
        app_label = 'store'
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

    def update_total(self):
        """Actualiza el total_amount basado en los items"""
        self.total_amount = sum(item.subtotal() for item in self.items.all())
        self.save()


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, blank=True)
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    is_album_purchase = models.BooleanField(default=False)  # Nuevo campo

    class Meta:
        app_label = 'store'
        ordering = ['-purchase_date']

    def __str__(self):
        return f"Purchase #{self.id} - {self.user.username}"


class PurchaseDetail(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="details")
    song = models.ForeignKey(Song, on_delete=models.PROTECT, null=True, blank=True)  # Hacer opcional
    album = models.ForeignKey(Album, on_delete=models.PROTECT, null=True, blank=True)  # Nuevo campo
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        app_label = 'store'

    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        if self.song:
            return f"{self.song.title} (x{self.quantity}) in Purchase #{self.purchase.id}"
        elif self.album:
            return f"Álbum: {self.album.title} (x{self.quantity}) in Purchase #{self.purchase.id}"
        return "Ítem inválido"


# Nueva clase para manejar compras de álbumes completos
class AlbumPurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='album_purchases')
    album = models.ForeignKey(Album, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    purchase_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        app_label = 'store'
        unique_together = ('user', 'album')  # Evita compras duplicadas

    def __str__(self):
        return f"{self.user.username} - {self.album.title}"