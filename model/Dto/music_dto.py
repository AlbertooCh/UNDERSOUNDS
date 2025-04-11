from dataclasses import dataclass
from datetime import date
from django.core.files import File

@dataclass
class SongDTO:
    id: int = None
    title: str = None
    artist_name: str = None
    album_title: str = None
    genre: str = None
    price: float = None
    release_date: date = None
    album_cover: File = None
    song_file: File = None