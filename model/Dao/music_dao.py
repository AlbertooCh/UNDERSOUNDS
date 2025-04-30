# music/dao/song_dao.py
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from model.music.music_models import Song
from django.db import models
from model.Dto.music_dto import SongDTO
from model.Factory.music_factory import SongFactory

class SongDAO:
    @staticmethod
    def create(song_dto):
        try:
            song = Song(
                title=song_dto.title,
                artist_name=song_dto.artist_name,
                album_title=song_dto.album_title,
                genre=song_dto.genre,
                price=song_dto.price,
                release_date=song_dto.release_date,
                album_cover=song_dto.album_cover,
                song_file=song_dto.song_file
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
            song.album_title = song_dto.album_title
            song.genre = song_dto.genre
            song.price = song_dto.price
            song.release_date = song_dto.release_date
            if song_dto.album_cover:
                song.album_cover = song_dto.album_cover
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
    def filter_by_album(album_title):
        """Filtra canciones por álbum"""
        songs = Song.objects.filter(album_title__icontains=album_title)
        return [SongFactory.create_dto_from_model(song) for song in songs]

    @staticmethod
    def search(query):
        """Busca canciones por título, artista o álbum"""
        songs = Song.objects.filter(
            models.Q(title__icontains=query) |
            models.Q(artist_name__icontains=query) |
            models.Q(album_title__icontains=query) |
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
            print(f"Filtering: release_date <= {fecha_post}")  # Debugging
            songs = songs.filter(release_date__lte=fecha_post)

        if query:
            print(f"Filtering: query = {query}")  # Debugging
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
