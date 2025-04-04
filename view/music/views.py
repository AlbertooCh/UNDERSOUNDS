from django.contrib.auth.decorators import login_required

from model.music.music_models import Song
from model.music.forms import SongForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404


def music_detail_redirect(request):
    song_id = request.GET.get("id")
    return redirect("music_detail_id", id=song_id)

def music_detail(request, id):
    song = get_object_or_404(Song, id=id)
    return render(request, 'music/music_detail.html', {'song': song})

def catalogo(request):
    songs = Song.objects.all()
    return render(request, "catalogo.html", {"songs": songs})

@login_required
def add_song(request):
    if request.user.role != 'artist':
        return redirect('home')  # Prevent fans/admins from adding songs

    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            song.artist_name = request.user.artist_name  # Set artist automatically
            song.save()
            messages.success(request, "Canción añadida exitosamente.")
            return redirect('artist_panel')
    else:
        form = SongForm()
    return render(request, 'music/song_form.html', {'form': form, 'action': 'Añadir'})

def edit_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    if song.artist_name != request.user.artist_name:
        return redirect('artist_panel')
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES, instance=song)
        if form.is_valid():
            form.save()
            messages.success(request, "Canción actualizada.")
            return redirect('catalogo')
    else:
        form = SongForm(instance=song)
    return render(request, 'music/song_form.html', {'form': form, 'action': 'Editar'})

def delete_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    if request.method == 'POST':
        song.delete()
        messages.success(request, "Canción eliminada.")
        return redirect('catalogo')
    return render(request, 'music/song_confirm_delete.html', {'song': song})

def artist_detail(request):
    song = Music.objects.all()
    return render(request, 'artist_detail.html', {'song': song})

@login_required
def artist_panel(request):
    if request.user.role != 'artist':
        return redirect('home')  # or show error

    songs = Song.objects.filter(artist_name=request.user.artist_name)
    return render(request, 'music/artist_panel.html', {'songs': songs})


@login_required
def artist_detail(request):
    if request.user.role != 'artist':
        return render(request, 'music/artist_not_found.html', {'artist_name': request.user.username})

    # Filter songs by the logged-in artist's name
    songs = Song.objects.filter(artist_name=request.user.artist_name)

    if not songs.exists():
        return render(request, 'music/artist_not_found.html', {'artist_name': request.user.artist_name})

    artist = {
        'name': request.user.artist_name,
        'age': 26,  # optional or fetch dynamically if you store it
        'nationality': request.user.country or 'Desconocido',
        'bio': request.user.bio or '',
        'awards': ['Electronic Music Award']  # optional static content
    }

    context = {
        'artist': artist,
        'albums': songs,
    }
    return render(request, 'music/artist_detail.html', context)

