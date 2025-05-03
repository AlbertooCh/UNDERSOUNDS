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
    album_id = models.IntegerField(blank=True, null=True, verbose_name="ID del álbum")

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
    description = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'music'  # ¡Esto es crucial!

    def __str__(self):
        return f"{self.title} - {self.artist_name}"

class Favorite(models.Model):
    user_id = models.IntegerField()  # Cambiamos de ForeignKey a IntegerField
    song = models.ForeignKey('music.Song', on_delete=models.CASCADE, null=True, blank=True)
    album = models.ForeignKey('music.Album', on_delete=models.CASCADE, null=True, blank=True)
    artist_id = models.IntegerField(null=True, blank=True)  # También cambiamos artist a artist_id
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_id', 'song', 'album', 'artist_id')
        app_label = 'music'  # o 'favorites' si creaste nueva app

    def __str__(self):
        if self.song:
            return f"User {self.user_id} likes song {self.song.title}"
        elif self.album:
            return f"User {self.user_id} likes album {self.album.title}"
        elif self.artist_id:
            return f"User {self.user_id} likes artist {self.artist_id}"
        return f"User {self.user_id}'s favorite"
