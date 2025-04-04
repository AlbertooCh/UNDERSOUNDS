from model.dto.song_dto import SongDTO
from model.music.music_models import Song
class SongFactory:
    @staticmethod
    def create_song(
        title: str,
        artist_name: str,
        album_title: str,
        genre: str,
        price: float,
        release_date,
        album_cover_path: str = None,
        song_file_path: str = None
    ) -> SongDTO:
        return SongDTO(
            id=None,
            title=title,
            artist_name=artist_name,
            album_title=album_title,
            genre=genre,
            price=price,
            release_date=release_date,
            album_cover_path=album_cover_path,
            song_file_path=song_file_path
        )

    @staticmethod
    def create_from_request_data(data: dict) -> SongDTO:
        return SongDTO(
            id=data.get('id'),
            title=data['title'],
            artist_name=data['artist_name'],
            album_title=data['album_title'],
            genre=data['genre'],
            price=float(data['price']),
            release_date=data['release_date'],
            album_cover_path=data.get('album_cover'),
            song_file_path=data.get('song_file')
        )