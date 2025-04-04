from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class SongDTO:
    id: Optional[int]
    title: str
    artist_name: str
    album_title: str
    genre: str
    price: float
    release_date: date
    album_cover_path: Optional[str]
    song_file_path: Optional[str]

    @classmethod
    def from_model(cls, song):
        return cls(
            id=song.id,
            title=song.title,
            artist_name=song.artist_name,
            album_title=song.album_title,
            genre=song.genre,
            price=float(song.price),
            release_date=song.release_date,
            album_cover_path=str(song.album_cover) if song.album_cover else None,
            song_file_path=str(song.song_file) if song.song_file else None
        )