from django.shortcuts import render, get_object_or_404
from .models import Music

def music_list(request):
    songs = Music.objects.all()
    return render(request, "music_list.html", {"songs": songs})

def music_detail(request, song_id):
    song = get_object_or_404(Music, id=song_id)
    return render(request, "music_detail.html", {"song": song})
def catalogo(request):
    return render(request, "catalogo.html")
