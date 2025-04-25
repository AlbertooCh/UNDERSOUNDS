from django.db import models

from model.music.music_models import Song
from user.models import User


class Comments(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_comments')
    comment = models.TextField(max_length=255)
    rating = models.DecimalField(max_digits=5, decimal_places=2, default='0.00')
    song_id = models.ForeignKey(Song, on_delete=models.CASCADE)

    class Meta:
        app_label = 'music'

    def __str__(self):
        return f"{self.song_id} - {self.comment}"