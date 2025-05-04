# views.py
from datetime import date
from django.db.models import Q, Count, Subquery, OuterRef, IntegerField
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaulttags import comment
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import logging

from controller.music_controller import SongController, AlbumController, FavoriteController
from controller.user_controller import UserController
from model.Dto.music_dto import SongDTO, AlbumDTO
from model.Dao.music_dao import AlbumDAO
from model.music.comments_model import Comments
from model.music.forms import SongForm, AlbumForm
from django.http import JsonResponse
from model.music.music_models import Song, Album, Favorite
from model.store.store_models import CartItem, Order, Purchase, OrderItem
import json


def music_detail_redirect(request):
    song_id = request.GET.get("id")
    return redirect("music_detail_id", id=song_id)

def music_detail(request, id):
    try:
        song_dto = SongController.get_song(id)
        if not song_dto:
            return render(request, '404.html', status=404)

        User = get_user_model()
        artist = User.objects.filter(artist_name=song_dto.artist_name).first()

        song = {
            'id': song_dto.id,
            'title': song_dto.title,
            'artist_name': song_dto.artist_name,
            'artist_id': artist.id if artist else None,
            'genre': song_dto.genre,
            'price': song_dto.price,
            'artist': artist,
            'release_date': song_dto.release_date,
            'song_cover': song_dto.song_cover,
            'song_file': song_dto.song_file,
            'album_id': song_dto.album_id,
        }

        # Comentarios y ratings
        comments_ratings = list(Comments.objects.filter(song_id=id))
        comments_ratings.reverse()
        rating = sum(c.rating for c in comments_ratings) / len(comments_ratings) if comments_ratings else 0

        # Estado de compra/carrito/favoritos
        in_cart = False
        in_order = False
        is_favorite = False
        artist_songs = []

        if request.user.is_authenticated:
            # Verificar si está en el carrito (con protección contra None)
            in_cart = CartItem.objects.filter(
                user=request.user,
                song__id=id
            ).exists()

            # Verificar si ya fue comprado
            in_order = PurchaseDetail.objects.filter(
                purchase__user=request.user,
                song__id=id
            ).exists()

            # Verificar si es favorito
            is_favorite = FavoriteController.is_item_favorited(
                request.user.id,
                'song',
                id
            )

            # Canciones del artista
            if artist:
                artist_songs = UserController.get_artist_with_songs(artist.id).songs.all()

        context = {
            'song': song,
            'comments': comments_ratings,
            'in_cart': in_cart,
            'in_order': in_order,
            'artist_songs': artist_songs,
            'album_id': song_dto.album_id,
            'is_favorite': is_favorite,
            'rating': rating
        }
        return render(request, 'music/music_detail.html', context)

    except Exception as e:
        logger.error(f"Error en music_detail: {str(e)}", exc_info=True)
        return render(request, '500.html', status=500)


def catalogo(request):
    # Obtener parámetros de filtrado
    query = request.GET.get('q')
    genre = request.GET.get('genre')
    artist = request.GET.get('artist')
    recent = request.GET.get('recent')
    fecha_ant = request.GET.get('fechaAnt')
    fecha_post = request.GET.get('fechaPost')
    show_type = request.GET.get('type')  # 'songs' o 'albums'

    # Inicializar querysets
    songs = []
    albums = []

    # Lógica para filtrar canciones
    if show_type != 'albums':  # Si no estamos mostrando solo álbumes
        songs = SongController.get_all_songs()

        if query or fecha_ant or fecha_post:
            songs = SongController.filter_songs_by_date_range(fecha_ant, fecha_post, query)
        elif genre:
            songs = SongController.filter_songs_by_genre(genre)
        elif artist:
            songs = SongController.filter_songs_by_artist(artist)
        elif recent:
            try:
                recent_date = date.fromisoformat(recent)
                songs = SongController.get_songs_recent(recent_date)
            except ValueError:
                pass

    # Lógica para filtrar álbumes
    if show_type != 'songs':  # Si no estamos mostrando solo canciones
        albums = AlbumController.get_all_albums()

        if query:
            albums = AlbumController.filter_albums_by_query(query)
        elif genre:
            albums = AlbumController.filter_albums_by_genre(genre)
        elif artist:
            albums = AlbumController.filter_albums_by_artist(artist)
        elif recent:
            try:
                recent_date = date.fromisoformat(recent)
                albums = AlbumController.get_albums_recent(recent_date)
            except ValueError:
                pass


    return render(request, "catalogo.html", {
        "songs": songs,
        "albums": albums,
        "show_type": show_type  # Para saber qué mostrar en el template
    })


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
                genre=form.cleaned_data['genre'],
                price=float(form.cleaned_data['price']),
                release_date=form.cleaned_data['release_date'],
                song_cover=request.FILES.get('song_cover'),
                song_file=request.FILES.get('song_file'),
                artist_id=request.user.id,
                album_id=None  # Canción independiente
            )

            # Usamos el controller para crear la canción
            song = SongController.create_song_with_artist(
                song_dto=song_dto,
                artist_id=request.user.id
            )

            if song:
                messages.success(request, "Canción independiente añadida exitosamente.")
                return redirect('artist_panel')
            else:
                messages.error(request, "Error al añadir la canción.")
    else:
        form = SongForm()

    return render(request, 'music/song_form.html', {
        'form': form,
        'action': 'Añadir',
        'user': request.user,
        'is_independent': True
    })

@login_required
def add_song_to_album(request, album_id):
    # Verificar que el usuario es artista y dueño del álbum
    if not request.user.is_authenticated or request.user.role != 'artist':
        messages.error(request, "Solo los artistas pueden añadir canciones")
        return redirect('home')

    album = AlbumController.get_album(album_id)
    if not album or album.artist_name != request.user.artist_name:
        messages.error(request, "Álbum no encontrado o no tienes permisos")
        return redirect('artist_panel')

    if request.method == 'POST':
        # Crear DTO con los datos del formulario
        song_dto = SongDTO(
            title=request.POST.get('title'),
            artist_name=request.user.artist_name,
            genre=request.POST.get('genre'),
            price=float(request.POST.get('price')),
            release_date=request.POST.get('release_date'),
            song_cover=request.FILES.get('song_cover'),
            song_file=request.FILES.get('song_file'),
            artist_id=request.user.id,
            album_id=album_id
        )

        # Crear la canción
        song = SongController.create_song_with_artist_and_album(
            song_dto=song_dto,
            artist_id=request.user.id,
            album_id=album_id
        )

        if song:
            messages.success(request, "Canción añadida al álbum exitosamente.")
            return redirect('edit_album', album_id=album_id)
        else:
            messages.error(request, "Error al añadir la canción.")

    # Si es GET o hay errores, mostrar el formulario en edit_album
    return redirect('edit_album', album_id=album_id)

@login_required
def add_album(request):
    # Verificar que el usuario es artista
    if not request.user.is_authenticated or request.user.role != 'artist':
        messages.error(request, "Solo los artistas pueden añadir álbumes")
        return redirect('home')

    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            # Creamos el DTO desde el formulario
            album_dto = AlbumDTO(
                title=form.cleaned_data['title'],
                artist_name=request.user.artist_name,
                genre=form.cleaned_data['genre'],
                release_date=form.cleaned_data['release_date'],
                album_cover=request.FILES.get('cover_image'),
                artist_id=request.user.id,
                price=float(form.cleaned_data['price']),
            )

            # Usamos el controller para crear el álbum
            album = AlbumController.create_album_with_artist(
                album_dto=album_dto,
                artist_id=request.user.id
            )

            if album:
                messages.success(request, "Álbum creado exitosamente. Ahora puedes añadir canciones.")
                return redirect('edit_album', album_id=album.id)
            else:
                messages.error(request, "Error al crear el álbum.")
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = AlbumForm()

    return render(request, 'music/album_form.html', {
        'form': form,
        'action': 'Crear',
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
                genre=form.cleaned_data['genre'],
                price=form.cleaned_data['price'],
                release_date=form.cleaned_data['release_date'],
                song_cover=request.FILES.get('song_cover') or song_dto.song_cover,
                song_file=request.FILES.get('song_file') or song_dto.song_file,
                album_id=song_dto.album_id,
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
            return render(request, 'music/song_confirm_delete.html', {
                'song': song_dto
            })
        else:
            messages.error(request, "Error al eliminar la canción.")

    return render(request, 'music/song_confirm_delete.html', {
        'song': song_dto
    })

@login_required
def delete_album(request, album_id):
    album_dto = AlbumController.get_album(album_id)
    if not album_dto:
        return render(request, '404.html', status=404)

    if album_dto.artist_name != request.user.artist_name:
        return redirect('artist_panel')

    if request.method == 'POST':
        success = AlbumController.delete_album(album_id)
        if success:
            messages.success(request, "Álbum eliminado.")
            return redirect('catalogo')
        else:
            messages.error(request, "Error al eliminar el álbum.")

    return render(request, 'music/album_confirm_delete.html', {
        'album': album_dto
    })


# En views.py
@login_required
def artist_panel(request):
    if request.user.role != 'artist':
        return redirect('home')

    # Álbumes del artista con conteo de canciones usando Subquery
    albums = Album.objects.filter(
        artist_name=request.user.artist_name
    ).annotate(
        song_count=Subquery(
            Song.objects.filter(album_id=OuterRef('id'))
            .values('album_id')
            .annotate(c=Count('*'))
            .values('c'),
            output_field=IntegerField()
        )
    ).order_by('-release_date')

    # Canciones del artista
    songs = Song.objects.filter(
        artist_name=request.user.artist_name
    ).order_by('-release_date')

    album_titles = {album.id: album.title for album in albums}
    # Renderizado del template
    return render(request, 'music/artist_panel.html', {
        'songs': songs,
        'albums': albums,
        'user': request.user
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
            song.release_date = request.POST.get('release_date')

            if 'cover_image' in request.FILES:
                song.cover_image = request.FILES['cover_image']
            if 'audio_file' in request.FILES:
                song.audio_file = request.FILES['audio_file']

            song.save()
            return JsonResponse({'success': True, 'message': 'Canción guardada correctamente'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)


@login_required
def artist_detail(request, artist_name=None):
    User = get_user_model()

    # Determinar si es el perfil propio o de otro artista
    if artist_name:
        artist = get_object_or_404(User, Q(artist_name=artist_name) & Q(role='artist'))
        artist = UserController.get_artist_with_songs(artist.id)
        is_own_profile = request.user.id == artist.id
    else:
        if request.user.role != 'artist':
            return render(request, 'music/artist_not_found.html', {
                'artist_name': request.user.username
            })
        artist = UserController.get_artist_with_songs(request.user.id)
        is_own_profile = True
    is_favorite=Favorite.objects.filter(user_id=request.user.id, artist_id=artist.id).exists()
    # Preparar contexto simplificado
    context = {
        'artist': artist,  # Pasamos el objeto completo directamente
        'is_own_profile': is_own_profile,
        'songs': artist.songs.all(),  # Accedemos a las canciones desde el artista
        'is_favorite': is_favorite
    }

    return render(request, 'music/artist_detail.html', context)

@login_required
def add_commentSong(request, song_id):
    new_comment = None  # Initialize new_comment
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        comment_rating = request.POST.get('rating')
        if comment_text:
            try:
                song = Song.objects.get(pk=song_id)
                new_comment = Comments.objects.create(
                    user_id=request.user,
                    song_id=song,
                    rating=comment_rating,
                    comment=comment_text
                )
            except Song.DoesNotExist:
                # Handle the case where the song does not exist.
                return redirect(reverse('home'))  # Or some other appropriate error handling
    # new_comment will be None if it wasn't created
    if new_comment:
        return redirect(f"{reverse('music_detail_id', args=[song_id])}#comment-{new_comment.id}")
    else:
        return redirect(reverse('music_detail_id', args=[song_id]) + '?error=empty_comment')

@login_required
def delete_commentSong(request, comment_id):
    if request.method == 'POST':
        comentario = get_object_or_404(Comments, id=comment_id)
        song_id = comentario.song_id.id
        comentario.delete()
        return redirect(reverse('music_detail_id', args=[song_id]))
    else:
        return redirect(reverse('catalogo'))

@login_required
def add_commentAlbum(request, album_id):
    new_comment = None  # Initialize new_comment
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        comment_rating = request.POST.get('rating')
        if comment_text:
            try:
                album = Album.objects.get(pk=album_id)
                new_comment = Comments.objects.create(
                    user_id=request.user,
                    album_id_id=album.id,
                    rating=comment_rating,
                    comment=comment_text
                )
            except album.DoesNotExist:
                # Handle the case where the song does not exist.
                return redirect(reverse('home'))  # Or some other appropriate error handling
    # new_comment will be None if it wasn't created
    if new_comment:
        return redirect(f"{reverse('album_detail', args=[album_id])}#comment-{new_comment.id}")
    else:
        return redirect(reverse('album_detail', args=[album_id]) + '?error=empty_comment')

@login_required
def delete_commentAlbum(request, comment_id):
    if request.method == 'POST':
        comentario = get_object_or_404(Comments, id=comment_id)
        album_id = comentario.album_id.id
        comentario.delete()
        return redirect(reverse('music_detail_id', args=[album_id]))
    else:
        return redirect(reverse('catalogo'))

@login_required
def edit_album(request, album_id):
    # Verificar que el usuario es artista
    if not request.user.is_authenticated or request.user.role != 'artist':
        messages.error(request, "Solo los artistas pueden editar álbumes")
        return redirect('home')

    # Obtener el álbum y verificar propiedad
    album = get_object_or_404(Album, pk=album_id)
    if album.artist_name != request.user.artist_name:
        messages.error(request, "No tienes permiso para editar este álbum")
        return redirect('artist_panel')

    # Obtener canciones del álbum
    songs = Song.objects.filter(album_id=album.id).order_by('id')

    # Manejar actualización del álbum
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES or None)
        if form.is_valid():
            album_dto = AlbumDTO(
                title=form.cleaned_data['title'],
                artist_name=request.user.artist_name,
                genre=form.cleaned_data['genre'],
                release_date=form.cleaned_data['release_date'],
                album_cover=request.FILES.get('album_cover'),
                artist_id=request.user.id,
                album_id=album_id
            )

            updated_album = AlbumController.update_album(album_id, album_dto)
            if updated_album:
                messages.success(request, "Álbum actualizado correctamente")
                return redirect('edit_album', album_id=album_id)
            else:
                messages.error(request, "Error al actualizar el álbum")
        else:
            messages.error(request, "Por favor corrige los errores en el formulario")

    # Manejar añadir canción al álbum (desde el formulario integrado)
    elif request.method == 'POST' and 'add_song' in request.POST:
        song_dto = SongDTO(
            title=request.POST.get('title'),
            artist_name=request.user.artist_name,
            genre=request.POST.get('genre'),
            price=float(request.POST.get('price', 0)),
            release_date=request.POST.get('release_date'),
            song_cover=request.FILES.get('song_cover'),
            song_file=request.FILES.get('song_file'),
            artist_id=request.user.id,
            album_id=album_id
        )

        song = SongController.create_song_with_artist_and_album(
            song_dto=song_dto,
            artist_id=request.user.id,
            album_id=album_id
        )

        if song:
            messages.success(request, "Canción añadida al álbum exitosamente")
            return redirect('edit_album', album_id=album_id)
        else:
            messages.error(request, "Error al añadir la canción al álbum")

    # Si es GET o hay errores, mostrar el formulario
    initial_data = {
        'title': album.title,
        'genre': album.genre,
        'release_date': album.release_date.strftime('%Y-%m-%d'),
    }
    form = AlbumForm(initial=initial_data)

    return render(request, 'music/edit_album.html', {
        'form': form,
        'album': album,
        'songs': songs,
        'user': request.user
    })


def album_detail(request, album_id):
    album_dto = AlbumController.get_album(album_id)
    if not album_dto:
        return render(request, '404.html', status=404)

    songs = SongController.get_songs_by_album(album_id)

    valor = []
    for song in songs:  # Asegúrate de que el rating sea un número
        valor.append(song.price)

    if valor:
        price = sum(valor) / len(valor)
    else:
        price = 0



    context = {
        'album': album_dto,
        'songs': songs,
        'user': request.user,
        'price': price
    }
    return render(request, 'music/album_detail.html', context)


@login_required
def remove_song_from_album(request, song_id, album_id):
    if not request.user.is_authenticated or request.user.role != 'artist':
        messages.error(request, "Acción no permitida")
        return redirect('home')

    song = get_object_or_404(Song, pk=song_id)
    album = get_object_or_404(Album, pk=album_id)

    if song.artist_name != request.user.artist_name or album.artist_name != request.user.artist_name:
        messages.error(request, "No tienes permiso para esta acción")
        return redirect('artist_panel')

    if AlbumDAO.remove_song_from_album(song_id, album_id):
        messages.success(request, "Canción quitada del álbum")
    else:
        messages.error(request, "Error al quitar la canción del álbum")

    return redirect('edit_album', album_id=album_id)


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def add_favorite(request):
    try:
        data = json.loads(request.body)
        item_type = data.get('type')
        item_id = data.get('id')

        if not item_type or not item_id:
            return JsonResponse({'status': 'error', 'message': 'Type and ID are required'}, status=400)

        favorite = FavoriteController.add_favorite(request.user.id, item_type, item_id)
        return JsonResponse({
            'status': 'success',
            'favorite': {
                'id': favorite.id,
                'type': favorite.type,
                'item': favorite.item,
                'created_at': favorite.created_at.isoformat()
            }
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def remove_favorite(request):
    try:
        data = json.loads(request.body)
        item_type = data.get('type')
        item_id = data.get('id')

        if not item_type or not item_id:
            return JsonResponse({'status': 'error', 'message': 'Type and ID are required'}, status=400)

        success = FavoriteController.remove_favorite(request.user.id, item_type, item_id)
        if success:
            return JsonResponse({'status': 'success', 'message': 'Favorite removed'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Favorite not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@require_http_methods(["GET"])
@login_required
def list_favorites(request):
    try:
        favorites = FavoriteController.get_user_favorites(request.user.id)
        favorites_data = [{
            'id': fav.id,
            'type': fav.type,
            'item': fav.item,
            'created_at': fav.created_at.isoformat()
        } for fav in favorites]

        return JsonResponse({
            'status': 'success',
            'favorites': favorites_data
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@require_http_methods(["GET"])
@login_required
def check_favorite(request, item_type, item_id):
    try:
        is_favorited = FavoriteController.is_item_favorited(request.user.id, item_type, item_id)
        return JsonResponse({
            'status': 'success',
            'is_favorited': is_favorited
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
def favorites_view(request):
    favorites = FavoriteController.get_user_favorites(request.user.id)

    # Separar favoritos por tipo
    songs = []
    albums = []
    artists = []

    for fav in favorites:
        if fav.type == 'song' and fav.item:
            songs.append(fav.item)
        elif fav.type == 'album' and fav.item:
            albums.append(fav.item)
        elif fav.type == 'artist' and fav.item:
            artists.append(fav.item)

    return render(request, 'music/favoritos.html', {
        'songs': songs,
        'albums': albums,
        'artists': artists
    })