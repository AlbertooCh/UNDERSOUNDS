# music/controllers/song_controller.py
from datetime import date, datetime
from django.contrib.auth import get_user_model
from django.db.models import Q

from model.Dao.music_dao import SongDAO, AlbumDAO, FavoriteDAO
from model.Dto.music_dto import SongDTO, AlbumDTO, FavoriteDTO, FavoriteItemDTO
from django.core.files.uploadedfile import InMemoryUploadedFile
from model.Dao.user_dao import UserDAO
from user.models import User
from controller.user_controller import UserController
from model.Factory.music_factory import SongFactory, AlbumFactory, FavoriteFactory
from model.music.music_models import Song, Album, Favorite

class SongController:
    @staticmethod
    def create_song(title, artist_id, **kwargs):
        artist = UserDAO.get_by_id(artist_id)
        if not artist or artist.role != 'artist':
            return None

        song_dto = SongDTO(title=title, artist_name=artist.artist_name, **kwargs)
        created_song = SongDAO.create(song_dto)

        if created_song and created_song.id:  # Ahora created_song es un DTO con ID
            # Asocia la canción al artista
            if UserController.add_song_to_artist(artist_id, created_song.id):
                return created_song
            else:
                # Si falla la asociación, borra la canción
                SongDAO.delete(created_song.id)
        return None

    @staticmethod
    def get_song(song_id):
        """
        Obtiene una canción por ID
        """
        return SongDAO.get_by_id(song_id)

    @staticmethod
    def get_all_songs(ordered=True):
        """
        Obtiene todas las canciones
        :param ordered: Si True, devuelve ordenado por fecha descendente
        """
        songs = SongDAO.get_all()
        if ordered:
            return sorted(songs, key=lambda x: x.release_date, reverse=True)
        return songs

    @staticmethod
    def update_song(song_id, **kwargs):
        """
        Actualiza una canción existente
        """
        song_dto = SongDAO.get_by_id(song_id)
        if not song_dto:
            return False

        # Actualiza solo los campos proporcionados
        for field, value in kwargs.items():
            if hasattr(song_dto, field):
                setattr(song_dto, field, value)

        return SongDAO.update(song_dto)

    @staticmethod
    def delete_song(song_id):
        """
        Elimina una canción
        """
        return SongDAO.delete(song_id)

    @staticmethod
    def search_songs(query):
        """
        Busca canciones por término
        """
        return SongDAO.search(query)

    @staticmethod
    def filter_songs_by_genre(genre):
        """
        Filtra canciones por género
        """
        return SongDAO.filter_by_genre(genre)

    @staticmethod
    def filter_songs_by_artist(artist_name):
        """
        Filtra canciones por artista
        """
        return SongDAO.filter_by_artist(artist_name)

    @staticmethod
    def upload_song_file(song_id, song_file: InMemoryUploadedFile):
        """
        Maneja la subida del archivo de audio
        """
        song_dto = SongDAO.get_by_id(song_id)
        if not song_dto:
            return False

        song_dto.song_file = song_file
        return SongDAO.update(song_dto)

    @staticmethod
    def upload_song_cover(song_id, cover_image: InMemoryUploadedFile):
        """
        Maneja la subida de la portada del álbum
        """
        song_dto = SongDAO.get_by_id(song_id)
        if not song_dto:
            return False

        song_dto.song_cover = cover_image
        return SongDAO.update(song_dto)

    @staticmethod
    def create_song_with_artist(song_dto, artist_id):
        """
        Crea una canción y la asocia al artista automáticamente
        Devuelve la canción creada o None si falla
        """
        # Primero creamos la canción
        song = SongDAO.create(song_dto)
        if not song:
            return None

        # Luego la asociamos al artista
        if not UserController.add_song_to_artist(artist_id, song.id):
            # Si falla la asociación, borramos la canción creada
            SongDAO.delete(song.id)
            return None

        return song

    def create_song_with_artist_and_album(song_dto, artist_id, album_id):
        try:
            song = SongDAO.create(song_dto)
            if song:
                UserController.add_song_to_artist(artist_id, song.id)
                UserController.add_album_to_artist(album_id, artist_id)
                AlbumDAO.add_song_to_album(album_id, song.id)
                return song
            return None
        except Exception as e:
            print(f"Error creating song with artist and album: {e}")
            return None

    @staticmethod
    def get_songs_recent(recent_date):
        """
        Obtiene todas las canciones, con opción de filtrar por fecha reciente y ordenar.
        :param recent_date: (Opcional) Filtra las canciones publicadas después o en esta fecha (objeto date).
        :param ordered: Si True, devuelve ordenado por fecha descendente.
        """
        songs = SongDAO.get_all()
        if recent_date:
            songs = [song for song in songs if song.release_date and song.release_date.date() >= recent_date]
        return songs

    @staticmethod
    def get_songs_by_album(album_id):

        return SongDAO.filter_by_album(album_id)

    def filter_songs_by_date_range(fecha_ant, fecha_post, query):
        """
        Filtra canciones por rango de fechas y opcionalmente por un término de búsqueda.
        """
        try:
            if fecha_ant:
                datetime.strptime(fecha_ant, '%Y-%m-%d').date()  # Potential Error
            if fecha_post:
                datetime.strptime(fecha_post, '%Y-%m-%d').date()  # Potential Error

            songs = SongDAO.filter_by_date_range(fecha_ant, fecha_post, query)
            return songs
        except ValueError:
            # Handle invalid date formats gracefully
            return []  # Or raise an exception, log, etc.

class AlbumController:
    @staticmethod
    def create_album_with_artist(album_dto: AlbumDTO, artist_id: int):
        try:
            album = AlbumDAO.create_album(album_dto)
            if album:
                # Aquí podrías añadir lógica adicional para relacionar con el artista
                return album
            return None
        except Exception as e:
            print(f"Error creating album: {e}")
            return None

    @staticmethod
    def get_album(album_id):
        return AlbumDAO.get_album_by_id(album_id)

    @staticmethod
    def update_album(album_id, album_dto: AlbumDTO):
        return AlbumDAO.update_album(album_id, album_dto)

    @staticmethod
    def delete_album(album_id):
        return AlbumDAO.delete_album(album_id)

    @staticmethod
    def get_album_dto(album_id):
        album = AlbumDAO.get_album_by_id(album_id)
        if album:
            return AlbumFactory.create_dto_from_album(album)
        return None

    @staticmethod
    def get_all_albums():
        """
        Retorna todos los álbumes ordenados por fecha de lanzamiento (más recientes primero)
        """
        return Album.objects.all().order_by('-release_date')

    @staticmethod
    def filter_albums_by_query(query):
        """
        Filtra álbumes por texto (busca en título, artista y género)
        Args:
            query (str): Texto de búsqueda
        Returns:
            QuerySet: Álbumes que coinciden con la búsqueda
        """
        if not query:
            return Album.objects.none()

        return Album.objects.filter(
            Q(title__icontains=query) |
            Q(artist_name__icontains=query) |
            Q(genre__icontains=query)
        ).order_by('-release_date')

    @staticmethod
    def filter_albums_by_genre(genre):
        """
        Filtra álbumes por género exacto (case insensitive)
        Args:
            genre (str): Género a filtrar
        Returns:
            QuerySet: Álbumes del género especificado
        """
        if not genre:
            return Album.objects.none()

        return Album.objects.filter(genre__iexact=genre).order_by('-release_date')

    @staticmethod
    def filter_albums_by_artist(artist):
        """
        Filtra álbumes por nombre de artista (case insensitive)
        Args:
            artist (str): Nombre del artista
        Returns:
            QuerySet: Álbumes del artista especificado
        """
        if not artist:
            return Album.objects.none()

        return Album.objects.filter(artist_name__iexact=artist).order_by('-release_date')

    @staticmethod
    def get_albums_recent(since_date):
        """
        Retorna álbumes lanzados desde la fecha especificada
        Args:
            since_date (date): Fecha mínima de lanzamiento
        Returns:
            QuerySet: Álbumes recientes ordenados por fecha
        """
        if not since_date:
            return Album.objects.none()

        # Asegurarse que since_date es un objeto date
        if isinstance(since_date, str):
            since_date = datetime.strptime(since_date, '%Y-%m-%d').date()

        return Album.objects.filter(release_date__gte=since_date).order_by('-release_date')


User = get_user_model()


class FavoriteController:
    @staticmethod
    def add_favorite(user_id: int, item_type: str, item_id: int) -> FavoriteItemDTO:
        filters = {'user_id': user_id}

        if item_type == 'song':
            item = Song.objects.get(id=item_id)
            filters['song_id'] = item_id
        elif item_type == 'album':
            item = Album.objects.get(id=item_id)
            filters['album_id'] = item_id
        elif item_type == 'artist':
            item = User.objects.get(id=item_id, role='artist')
            filters['artist_id'] = item_id
        else:
            raise ValueError("Invalid item type")

        if FavoriteDAO.is_item_favorited(**filters):
            raise ValueError("Item already in favorites")

        favorite_dto = FavoriteDTO(user_id=user_id, **{f"{item_type}_id": item_id})
        favorite = FavoriteDAO.create_favorite(favorite_dto)
        return FavoriteFactory.model_to_item_dto(Favorite.objects.get(id=favorite.id))

    @staticmethod
    def remove_favorite(user_id: int, item_type: str, item_id: int) -> bool:
        favorite_dto = FavoriteDTO(user_id=user_id, **{f"{item_type}_id": item_id})
        return FavoriteDAO.delete_favorite(favorite_dto)

    @staticmethod
    def get_user_favorites(user_id: int) -> list[FavoriteItemDTO]:
        favorites = FavoriteDAO.get_user_favorites(user_id)
        return [FavoriteFactory.model_to_item_dto(fav) for fav in favorites]

    @staticmethod
    def is_item_favorited(user_id: int, item_type: str, item_id: int) -> bool:
        return FavoriteDAO.is_item_favorited(user_id=user_id, **{f"{item_type}_id": item_id})

    @staticmethod
    def get_artist_favorite_count(artist_id: int) -> int:
        return FavoriteDAO.get_artist_favorite_count(artist_id)