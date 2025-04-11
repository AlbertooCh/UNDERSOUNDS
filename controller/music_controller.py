# music/controllers/song_controller.py
from model.Dao.music_dao import SongDAO
from model.Dto.music_dto import SongDTO
from django.core.files.uploadedfile import InMemoryUploadedFile

class SongController:
    @staticmethod
    def create_song(title, artist_name, album_title, genre, price, release_date,
                   album_cover=None, song_file=None):
        """
        Crea una nueva canción
        """
        song_dto = SongDTO(
            title=title,
            artist_name=artist_name,
            album_title=album_title,
            genre=genre,
            price=price,
            release_date=release_date,
            album_cover=album_cover,
            song_file=song_file
        )
        return SongDAO.create(song_dto)

    @staticmethod
    def get_song(song_id):
        """
        Obtiene una canción por ID
        """
        return SongDAO.get_by_id(song_id)

    @staticmethod
    def get_all_songs():
        """
        Obtiene todas las canciones
        """
        return SongDAO.get_all()

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