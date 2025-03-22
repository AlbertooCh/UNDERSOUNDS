import json
import os

from django.shortcuts import render, get_object_or_404

from undersounds import settings
from .models import Music

def music_detail(request):
    song = Music.objects.all()
    return render(request, 'music_detail.html', {'song': song})
def catalogo(request):
    return render(request, "catalogo.html")

def artist_detail(request):
    song = Music.objects.all()
    return render(request, 'artist_detail.html', {'song': song})
