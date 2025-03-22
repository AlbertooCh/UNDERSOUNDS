from django.db import models
from django.conf import settings
import os
import json

# Create your models here.

class Music(models.Model):
    song_name = models.CharField(max_length=100)
    artist_name = models.CharField(max_length=100)
    album_name = models.CharField(max_length=100)
    duration = models.CharField(max_length=10)
    genre = models.CharField(max_length=50)
    artist_photo = models.ImageField(upload_to='static/Photos/Cantantes/')
    album_photo = models.ImageField(upload_to='static/Photos/album/')
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField()


    def __str__(self):
        return self.song_name

class Artist(models.Model):
    artist_name = models.CharField(max_length=100)
    artist_photo = models.ImageField(upload_to='static/Photos/Cantantes/')
    description = models.TextField()
    age = models.IntegerField()
    nationality = models.CharField(max_length=50)
    awards = models.JSONField()


class UserCollection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    song = models.ForeignKey(Music, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('user', 'song')



