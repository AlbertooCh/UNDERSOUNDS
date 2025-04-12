from dataclasses import dataclass
from datetime import date
from django.core.files import File

@dataclass
class SongDTO:
    def __init__(self, title, artist_name, id=None, artist_id=None, **kwargs):
        self.id = id
        self.title = title
        self.artist_name = artist_name
        self.artist_id = artist_id  # Nuevo campo
        self.album_title = kwargs.get('album_title', '')
        self.genre = kwargs.get('genre', '')
        self.price = kwargs.get('price', 0.0)
        self.release_date = kwargs.get('release_date')
        self.album_cover = kwargs.get('album_cover')
        self.song_file = kwargs.get('song_file')