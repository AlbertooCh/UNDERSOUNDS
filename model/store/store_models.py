# model/store/store_models.py
from django.db import models
from django.conf import settings
from user.models import User
from model.music.music_models import Song


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='in_carts')
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'store'
        unique_together = ('user', 'song')  # Evita duplicados

    def subtotal(self):
        return self.quantity * self.song.price

    def __str__(self):
        return f"{self.song.title} ({self.quantity})"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'store'
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        app_label = 'store'
        ordering = ['-purchase_date']

    def __str__(self):
        return f"Purchase #{self.id} - {self.user.username}"


class PurchaseDetail(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="details")
    song = models.ForeignKey(Song, on_delete=models.PROTECT)  # PROTECT para mantener historial
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        app_label = 'store'

    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.song.title} (x{self.quantity}) in Purchase #{self.purchase.id}"