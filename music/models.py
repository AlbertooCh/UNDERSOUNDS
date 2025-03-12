from django.db import models
from django.conf import settings
import os
import json

# Create your models here.
class Music(models.Model):
    cant = models.IntegerField()
    title = models.CharField(max_length=255)
    album_title = models.CharField(max_length=255)
    duration = models.CharField(max_length=10)
    file = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} by {self.artist_name}"


class UserCollection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    song = models.ForeignKey(Music, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('user', 'song')



