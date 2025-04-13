from django.shortcuts import render
from model.music.music_models import Song
from controller.music_controller import SongController

def inicio(request):
    return render(request, 'core/inicio.html')    #must contain core/ , the path is core/inicio

def contacto(request):
    return render(request, 'core/contacto.html')  #must contain core/ , the path is core/contacto


def novedades(request):
    recent_songs = SongController.get_all_songs(ordered=True)[:15]
    return render(request, "novedades.html", {"songs": recent_songs})