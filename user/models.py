# user/music_models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from model.music.music_models import Song

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('artist', 'Artist'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    credit_card_number = models.CharField(max_length=16, blank=True, null=True)
    credit_card_expiry = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/usuario.png')
    backend = models.CharField(max_length=255, default='django.contrib.auth.backends.ModelBackend')


    # Artist-specific fields
    artist_name = models.CharField(max_length=255, blank=True, null=True)
    artist_type = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    genre = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    songs = models.ManyToManyField('music.Song', related_name='artists', blank=True)

    class Meta:
        app_label = 'user'

    def get_purchase_history(self):
        return self.purchases.all().order_by('-purchase_date')

