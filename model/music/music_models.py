# music/music_models.py
from django.db import models


class Song(models.Model):
    title = models.CharField(max_length=255)
    artist_name = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    release_date = models.DateTimeField()
    song_cover = models.ImageField(upload_to='song_covers/', blank=True, null=True)
    song_file = models.FileField(upload_to='songs/', blank=True, null=True)  # <-- New field
    album_id = models.ForeignKey('Album', on_delete=models.CASCADE, related_name='songs', blank=True, null=True)

    class Meta:
        app_label = 'music'  # ¡Esto es crucial!

    def __str__(self):
        return f"{self.title} - {self.artist_name}"

class Album(models.Model):
    title = models.CharField(max_length=255)
    artist_name = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    release_date = models.DateTimeField()
    album_cover = models.ImageField(upload_to='album_covers/', blank=True, null=True)

    class Meta:
        app_label = 'music'  # ¡Esto es crucial!

    def __str__(self):
        return f"{self.title} - {self.artist_name}"
