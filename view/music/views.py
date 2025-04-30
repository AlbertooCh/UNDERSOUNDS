# views.py
from datetime import date
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaulttags import comment
from django.urls import reverse

from controller.music_controller import SongController
from controller.user_controller import UserController
from model.Dto.music_dto import SongDTO
from model.music.comments_model import Comments
from model.music.forms import SongForm
from django.http import JsonResponse
from model.music.music_models import Song
from model.store.store_models import CartItem, Order, Purchase, OrderItem


def music_detail_redirect(request):
    song_id = request.GET.get("id")
    return redirect("music_detail_id", id=song_id)


def music_detail(request, id):
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

    comments_ratings = list(Comments.objects.filter(song_id=id))
    comments_ratings.reverse()
    artist_songs = UserController.get_artist_with_songs(artist.id)

    order_data = None
    in_cart = False
    in_order = False

    if request.user.is_authenticated:
        # Obtener los items en el carrito del usuario
        items_in_cart = CartItem.objects.filter(user=request.user)

        # Obtener la última orden completada del usuario (o la orden actual si estás en proceso de compra)
        user_purchases = Purchase.objects.filter(user=request.user)
        order_data  = set()
        for purchase in user_purchases:
            if purchase.order:
                for item in purchase.order.items.all():
                    order_data.add(item.song)

        for items in items_in_cart:
            if (items.song.id == id):
                in_cart = True
                break;

        for order in order_data:
            if (order.id == id):
                in_order = True
                break;


    context = {
        'song': song,
        'comments': comments_ratings,
        'in_cart': in_cart,
        'in_order': in_order,
        'artist_songs': artist_songs.songs.all(),
        'album_id': song_dto.album_id
    }
    return render(request, 'music/music_detail.html', context)

def catalogo(request):
    query = request.GET.get('q')
    genre = request.GET.get('genre')
    artist = request.GET.get('artist')
    recent = request.GET.get('recent')
    fecha_ant = request.GET.get('fechaAnt')
    fecha_post = request.GET.get('fechaPost')

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
                genre=form.cleaned_data['genre'],
                price=float(form.cleaned_data['price']),
                release_date=form.cleaned_data['release_date'],
                song_cover=request.FILES.get('song_cover'),
                song_file=request.FILES.get('song_file'),
                artist_id=request.user.id  # Nuevo campo para asociación,
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

    # Preparar contexto simplificado
    context = {
        'artist': artist,  # Pasamos el objeto completo directamente
        'is_own_profile': is_own_profile,
        'songs': artist.songs.all()  # Accedemos a las canciones desde el artista
    }

    return render(request, 'music/artist_detail.html', context)

def add_comment(request, song_id):
    new_comment = None  # Initialize new_comment
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        if comment_text:
            try:
                song = Song.objects.get(pk=song_id)
                new_comment = Comments.objects.create(
                    user_id=request.user,
                    song_id=song,
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

def delete_comment(request, comment_id):
    if request.method == 'POST':
        comentario = Comments.get_object_or_404(Comments, id=comment_id)
        comentario.delete()
        return redirect(reverse('music_detail_id', args=[comment.song_id.id]))
    else:
        return redirect(reverse('music_detail_id', args=[comment.song_id.id]))
