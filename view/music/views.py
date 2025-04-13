# views.py
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from controller.music_controller import SongController
from model.Dto.music_dto import SongDTO
from model.music.forms import SongForm
from django.http import JsonResponse
from model.music.music_models import Song

def music_detail_redirect(request):
    song_id = request.GET.get("id")
    return redirect("music_detail_id", id=song_id)


def music_detail(request, id):
    song_dto = SongController.get_song(id)
    if not song_dto:
        return render(request, '404.html', status=404)

    # Convertimos el DTO a un diccionario para la plantilla
    song = {
        'id': song_dto.id,
        'title': song_dto.title,
        'artist_name': song_dto.artist_name,
        'album_title': song_dto.album_title,
        'genre': song_dto.genre,
        'price': song_dto.price,
        'release_date': song_dto.release_date,
        'album_cover': song_dto.album_cover,
        'song_file': song_dto.song_file
    }
    return render(request, 'music/music_detail.html', {'song': song})


def catalogo(request):
    query = request.GET.get('q')
    genre = request.GET.get('genre')
    artist = request.GET.get('artist')

    if query:
        songs = SongController.search_songs(query)
    elif genre:
        songs = SongController.filter_songs_by_genre(genre)
    elif artist:
        songs = SongController.filter_songs_by_artist(artist)
    else:
        songs = SongController.get_all_songs()

    return render(request, "catalogo.html", {"songs": songs})


@login_required
def add_song(request):
    # Verificar que el usuario es artista
    if not request.user.is_authenticated or request.user.role != 'artist':
        messages.error(request, "Solo los artistas pueden añadir canciones")
        return redirect('home')

    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            # Creamos el DTO desde el formulario
            song_dto = SongDTO(
                title=form.cleaned_data['title'],
                artist_name=request.user.artist_name,
                album_title=form.cleaned_data['album_title'],
                genre=form.cleaned_data['genre'],
                price=float(form.cleaned_data['price']),
                release_date=form.cleaned_data['release_date'],
                album_cover=request.FILES.get('album_cover'),
                song_file=request.FILES.get('song_file'),
                artist_id=request.user.id  # Nuevo campo para asociación
            )

            # Usamos el controller para crear la canción
            song = SongController.create_song_with_artist(
                song_dto=song_dto,
                artist_id=request.user.id
            )

            if song:
                messages.success(request, "Canción añadida exitosamente.")
                return redirect('artist_panel')
            else:
                messages.error(request, "Error al añadir la canción.")
    else:
        form = SongForm()

    return render(request, 'music/song_form.html', {
        'form': form,
        'action': 'Añadir',
        'user': request.user
    })


@login_required
def edit_song(request, song_id):
    song_dto = SongController.get_song(song_id)
    if not song_dto:
        return render(request, '404.html', status=404)

    if song_dto.artist_name != request.user.artist_name:
        return redirect('artist_panel')

    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            # Actualizamos el DTO con los datos del formulario
            updated_dto = SongDTO(
                id=song_id,
                title=form.cleaned_data['title'],
                artist_name=request.user.artist_name,
                album_title=form.cleaned_data['album_title'],
                genre=form.cleaned_data['genre'],
                price=form.cleaned_data['price'],
                release_date=form.cleaned_data['release_date'],
                album_cover=request.FILES.get('album_cover') or song_dto.album_cover,
                song_file=request.FILES.get('song_file') or song_dto.song_file
            )

            # Usamos el controller para actualizar
            success = SongController.update_song(updated_dto)

            if success:
                messages.success(request, "Canción actualizada.")
                return redirect('catalogo')
            else:
                messages.error(request, "Error al actualizar la canción.")
    else:
        # Prellenamos el formulario con los datos actuales
        initial_data = {
            'title': song_dto.title,
            'album_title': song_dto.album_title,
            'genre': song_dto.genre,
            'price': song_dto.price,
            'release_date': song_dto.release_date,
        }
        form = SongForm(initial=initial_data)

    return render(request, 'music/song_form.html', {
        'form': form,
        'action': 'Editar',
        'song': song_dto
    })


@login_required
def delete_song(request, song_id):
    song_dto = SongController.get_song(song_id)
    if not song_dto:
        return render(request, '404.html', status=404)

    if song_dto.artist_name != request.user.artist_name:
        return redirect('artist_panel')

    if request.method == 'POST':
        success = SongController.delete_song(song_id)
        if success:
            messages.success(request, "Canción eliminada.")
            return redirect('catalogo')
        else:
            messages.error(request, "Error al eliminar la canción.")

    return render(request, 'music/song_confirm_delete.html', {
        'song': song_dto
    })


@login_required
def artist_panel(request):
    if request.user.role != 'artist':
        return redirect('home')

    songs = SongController.filter_songs_by_artist(request.user.artist_name)
    return render(request, 'music/artist_panel.html', {
        'songs': songs
    })


@login_required
def artist_detail(request):
    if request.user.role != 'artist':
        return render(request, 'music/artist_not_found.html', {
            'artist_name': request.user.username
        })

    songs = SongController.filter_songs_by_artist(request.user.artist_name)

    if not songs:
        return render(request, 'music/artist_not_found.html', {
            'artist_name': request.user.artist_name
        })

    artist = {
        'name': request.user.artist_name,
        'age': 26,  # Puedes obtener esto de tu modelo de usuario
        'nationality': getattr(request.user, 'country', 'Desconocido'),
        'bio': getattr(request.user, 'bio', ''),
        'awards': ['Electronic Music Award']  # Datos de ejemplo
    }

    return render(request, 'music/artist_detail.html', {
        'artist': artist,
        'albums': songs,
    })


@login_required
def save_song(request):
    if request.method == 'POST':
        song_id = request.POST.get('song_id')
        try:
            if song_id:
                song = Song.objects.get(id=song_id, artist=request.user)
            else:
                song = Song(artist=request.user)

            song.title = request.POST.get('title')
            song.price = request.POST.get('price')
            song.duration = request.POST.get('duration')
            song.genre = request.POST.get('genre')
            song.description = request.POST.get('description')

            if 'cover_image' in request.FILES:
                song.cover_image = request.FILES['cover_image']
            if 'audio_file' in request.FILES:
                song.audio_file = request.FILES['audio_file']

            song.save()
            return JsonResponse({'success': True, 'message': 'Canción guardada correctamente'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)