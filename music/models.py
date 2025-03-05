from django.db import models
from django.conf import settings

# Create your models here.
class Music(models.Model):
    title = models.CharField(max_length=255)
    artist_name = models.CharField(max_length=255)
    album_title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    release_date = models.DateField()

    def __str__(self):
        return f"{self.title} by {self.artist_name}"

class UserCollection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    song = models.ForeignKey(Music, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('user', 'song')
