# music/controllers/song_controller.py
from model.Dao.music_dao import SongDAO
from model.Dto.music_dto import SongDTO
from django.core.files.uploadedfile import InMemoryUploadedFile
from model.Dao.user_dao import UserDAO
from controller.user_controller import UserController
from model.Factory.music_factory import SongFactory
from model.music.music_models import Song

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
    def get_all_songs(ordered=False):
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
    def upload_album_cover(song_id, cover_image: InMemoryUploadedFile):
        """
        Maneja la subida de la portada del álbum
        """
        song_dto = SongDAO.get_by_id(song_id)
        if not song_dto:
            return False

        song_dto.album_cover = cover_image
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

    @staticmethod
    def get_songs_by_artist(artist_id):
        songs = Song.objects.filter(artist_id=artist_id)  # Asegúrate de usar el campo correcto
        return [SongFactory.create_from_model(song) for song in songs]