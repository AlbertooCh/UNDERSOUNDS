import json
import os

from django.shortcuts import render, get_object_or_404

from undersounds import settings
from .models import Music

def music_list(request):
    songs = Music.objects.all()
    return render(request, "music_list.html", {"songs": songs})

def music_detail(request, song_id):
    song = get_object_or_404(Music, id=song_id)
    return render(request, "music_detail.html", {"song": song})
def catalogo(request):
    return render(request, "catalogo.html")


def catalog(request):
    # Ruta al archivo JSON
    json_path = os.path.join(settings.BASE_DIR, 'Tracks.json')

    # Cargar datos del JSON
    with open(json_path, 'r', encoding='utf-8') as file:
        canciones = json.load(file)

    # Pasar datos al contexto de la plantilla
    context = {
        'canciones': canciones
    }
    return render(request, 'catalog.html', context)
