# music/dao/song_dao.py
from datetime import datetime
from django.core.files import File
from django.core.exceptions import ObjectDoesNotExist
from model.music.music_models import Song, Album, Favorite
from django.db import models
from model.Dto.music_dto import SongDTO, AlbumDTO, FavoriteDTO
from model.Factory.music_factory import SongFactory

class SongDAO:
    @staticmethod
    def create(song_dto):
        try:
            song = Song(
                title=song_dto.title,
                artist_name=song_dto.artist_name,
                genre=song_dto.genre,
                price=song_dto.price,
                release_date=song_dto.release_date,
                song_cover=song_dto.song_cover,
                song_file=song_dto.song_file,
                album_id=song_dto.album_id
            )
            song.save()
            # Devuelve el DTO con el ID actualizado
            return SongFactory.create_dto_from_model(song)  # <-- Esta es la clave
        except Exception as e:
            print(f"Error creating song: {e}")
            return None

    @staticmethod
    def get_by_id(song_id):
        """Obtiene una canción por su ID"""
        try:
            song = Song.objects.get(id=song_id)
            return SongFactory.create_dto_from_model(song)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_all():
        """Obtiene todas las canciones"""
        songs = Song.objects.all()
        return [SongFactory.create_dto_from_model(song) for song in songs]

    @staticmethod
    def update(song_dto):
        """Actualiza una canción existente"""
        try:
            song = Song.objects.get(id=song_dto.id)
            song.title = song_dto.title
            song.artist_name = song_dto.artist_name
            song.genre = song_dto.genre
            song.price = song_dto.price
            song.release_date = song_dto.release_date
            if song_dto.song_cover:
                song.song_cover = song_dto.song_cover
            if song_dto.song_file:
                song.song_file = song_dto.song_file
            song.save()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def delete(song_id):
        """Elimina una canción por su ID"""
        try:
            song = Song.objects.get(id=song_id)
            song.delete()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def filter_by_artist(artist_name):
        """Filtra canciones por nombre de artista"""
        songs = Song.objects.filter(artist_name__icontains=artist_name)
        return [SongFactory.create_dto_from_model(song) for song in songs]

    @staticmethod
    def filter_by_genre(genre):
        """Filtra canciones por género"""
        songs = Song.objects.filter(genre__iexact=genre)
        return [SongFactory.create_dto_from_model(song) for song in songs]


    @staticmethod
    def search(query):
        """Busca canciones por título, artista o álbum"""
        songs = Song.objects.filter(
            models.Q(title__icontains=query) |
            models.Q(artist_name__icontains=query) |
            models.Q(genre__icontains=query)
        )
        return [SongFactory.create_dto_from_model(song) for song in songs]

    @staticmethod
    def filter_by_date_range(fecha_ant=None, fecha_post=None, query=None):
        """
        Filtra canciones por rango de fechas y opcionalmente por texto (título, artista, etc.).
        """
        songs = Song.objects.all()  # Start with all songs

        if fecha_ant:
            fecha_ant = datetime.strptime(fecha_ant, '%Y-%m-%d').date()
            print(f"Filtering: release_date >= {fecha_ant}")  # Debugging
            songs = songs.filter(release_date__gte=fecha_ant)
        if fecha_post:
            fecha_post = datetime.strptime(fecha_post, '%Y-%m-%d').date()
            songs = songs.filter(release_date__lte=fecha_post)

        if query:
            songs = songs.filter(
                models.Q(title__icontains=query) |
                models.Q(artist_name__icontains=query) |
                models.Q(album_title__icontains=query) |
                models.Q(genre__icontains=query)
            )

        print(f"Query: {songs.query}")  # Very important debugging!
        results = [SongFactory.create_dto_from_model(song) for song in songs]
        print(f"Results count: {len(results)}")  # Debugging
        return results

class AlbumDAO:
    @staticmethod
    def create_album(album_dto: AlbumDTO):
        album = Album(
            title=album_dto.title,
            artist_name=album_dto.artist_name,
            genre=album_dto.genre,
            release_date=album_dto.release_date,
            price=album_dto.price,
        )

        if album_dto.album_cover:
            album.album_cover.save(
                album_dto.album_cover.name,
                File(album_dto.album_cover),
                save=True
            )

        album.save()
        return album

    @staticmethod
    def get_album_by_id(album_id):
        try:
            return Album.objects.get(pk=album_id)
        except Album.DoesNotExist:
            return None

    @staticmethod
    def update_album(album_id, album_dto: AlbumDTO):
        album = AlbumDAO.get_album_by_id(album_id)
        if album:
            album.title = album_dto.title
            album.artist_name = album_dto.artist_name
            album.genre = album_dto.genre
            album.release_date = album_dto.release_date
            album.price = album_dto.price

            if album_dto.album_cover:
                album.album_cover.save(
                    album_dto.album_cover.name,
                    File(album_dto.album_cover),
                    save=True
                )

            album.save()
            return album
        return None

    @staticmethod
    def delete_album(album_id):
        album = AlbumDAO.get_album_by_id(album_id)
        if album:
            album.delete()
            return True
        return False

    @staticmethod
    def add_song_to_album(album_id, song_id):
        try:
            album = Album.objects.get(pk=album_id)
            song = Song.objects.get(pk=song_id)
            song.album = album
            song.save()
            return True
        except (Album.DoesNotExist, Song.DoesNotExist):
            return False

    @staticmethod
    def remove_song_from_album(song_id, album_id):
        try:
            song = Song.objects.get(pk=song_id, album_id=album_id)
            song.album = None
            song.save()
            return True
        except Song.DoesNotExist:
            return False


class FavoriteDAO:
    @staticmethod
    def create_favorite(favorite_dto: FavoriteDTO) -> FavoriteDTO:
        favorite = Favorite.objects.create(
            user_id=favorite_dto.user_id,
            song_id=favorite_dto.song_id,
            album_id=favorite_dto.album_id,
            artist_id=favorite_dto.artist_id
        )
        return FavoriteDTO(
            id=favorite.id,
            user_id=favorite.user_id,
            song_id=favorite.song_id,
            album_id=favorite.album_id,
            artist_id=favorite.artist_id,
            created_at=favorite.created_at
        )

    @staticmethod
    def get_user_favorites(user_id: int):
        # Modificamos para usar user_id directamente
        return Favorite.objects.filter(user_id=user_id).select_related('song', 'album')

    @staticmethod
    def delete_favorite(favorite_dto: FavoriteDTO) -> bool:
        try:
            filters = {
                'user_id': favorite_dto.user_id,
                'song_id': favorite_dto.song_id,
                'album_id': favorite_dto.album_id,
                'artist_id': favorite_dto.artist_id
            }
            # Eliminamos None values para que no interfieran con la búsqueda
            filters = {k: v for k, v in filters.items() if v is not None}

            favorite = Favorite.objects.get(**filters)
            favorite.delete()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def is_item_favorited(user_id: int, **kwargs):
        # Aseguramos que el user_id siempre esté incluido
        kwargs['user_id'] = user_id
        # Eliminamos posibles valores None
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        return Favorite.objects.filter(**kwargs).exists()