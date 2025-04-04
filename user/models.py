# user/music_models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from music.music_models import Song  # Safe import: music doesn't depend on user

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('artist', 'Artist'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    credit_card_number = models.CharField(max_length=16, blank=True, null=True)
    credit_card_expiry = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Artist-specific fields (optional if you want)
    artist_name = models.CharField(max_length=255, blank=True, null=True)
    artist_type = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    genre = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
