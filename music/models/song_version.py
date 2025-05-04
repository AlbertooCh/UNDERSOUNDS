from django.db import models

class SongVersion(models.Model):
    song = models.ForeignKey('music.Song', on_delete=models.CASCADE, related_name='versions')
    title = models.CharField(max_length=255)
    artist_name = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    release_date = models.DateField()
    song_cover = models.FileField(upload_to='songs/versions/', blank=True, null=True)
    song_file = models.FileField(upload_to='songs/versions/', blank=True, null=True)
    saved_at = models.DateTimeField(auto_now_add=True)
