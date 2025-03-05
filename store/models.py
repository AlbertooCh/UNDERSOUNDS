from django.db import models

from music.models import Music


# Create your models here.
class Store(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Purchase by {self.user.username} on {self.purchase_date}"


class StoreDetails(models.Model):
    purchase = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='details')
    song = models.ForeignKey(Music, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
