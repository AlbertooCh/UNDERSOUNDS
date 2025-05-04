from dataclasses import dataclass
from datetime import date, datetime
from django.core.files import File
from typing import Optional

@dataclass
class SongDTO:
    def __init__(self, title, artist_name, id=None, artist_id=None, **kwargs):
        self.id = id
        self.title = title
        self.artist_name = artist_name
        self.artist_id = artist_id  # Nuevo campo
        self.genre = kwargs.get('genre', '')
        self.price = kwargs.get('price', 0.0)
        self.release_date = kwargs.get('release_date')
        self.song_cover = kwargs.get('song_cover')
        self.song_file = kwargs.get('song_file')
        self.album_id = kwargs.get('album_id')

class AlbumDTO:
    def __init__(self, title: str, artist_name: str, genre: str,
                 release_date: datetime, price: float,  # Añadido price como float
                 album_cover=None, artist_id=None, album_id=None, **kwargs):
        self.album_id = album_id
        self.title = title
        self.artist_name = artist_name
        self.genre = genre
        self.price = price  # Campo price añadido
        self.release_date = release_date
        self.album_cover = album_cover
        self.artist_id = artist_id

    def to_dict(self):
        return {
            'album_id': self.album_id,
            'title': self.title,
            'artist_name': self.artist_name,
            'genre': self.genre,
            'price': self.price,  # Price incluido en el dict
            'release_date': self.release_date,
            'album_cover': self.album_cover,
            'artist_id': self.artist_id
        }

@dataclass
class FavoriteDTO:
    user_id: int
    song_id: Optional[int] = None
    album_id: Optional[int] = None
    artist_id: Optional[int] = None
    created_at: Optional[datetime] = None
    id: Optional[int] = None

@dataclass
class FavoriteItemDTO:
    id: int
    type: str  # 'song', 'album', 'artist'
    item: dict  # Los datos del item favorito
    created_at: datetime