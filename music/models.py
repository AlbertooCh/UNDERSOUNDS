# music/models.py
from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=255)
    artist_name = models.CharField(max_length=100)
    album_title = models.CharField(max_length=255)
    genre = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    release_date = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.artist_name}"
