import json
import os

from django.shortcuts import render, get_object_or_404

from undersounds import settings
from .models import Song

def music_detail(request):
    song = Music.objects.all()
    return render(request, 'music_detail.html', {'song': song})
def catalogo(request):
    return render(request, "catalogo.html")

def artist_detail(request):
    song = Music.objects.all()
    return render(request, 'artist_detail.html', {'song': song})

def artist_detail(request, artist_name):
    # Filter songs by artist
    songs = Song.objects.filter(artist_name=artist_name)

    if not songs.exists():
        return render(request, 'music/artist_not_found.html', {'artist_name': artist_name})

    artist = {
        'name': artist_name,
        'age': 26,  # Placeholder - you can pull this from a separate Artist model if needed
        'nationality': 'Canadiense',  # Same here
        'bio': 'Un productor de música electrónica y DJ.',
        'awards': ['Electronic Music Award']
    }

    context = {
        'artist': artist,
        'albums': songs,
    }
    return render(request, 'music/artist_detail.html', context)
