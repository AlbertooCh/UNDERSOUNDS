from model.Dto.music_dto import SongDTO, AlbumDTO
from model.music.music_models import Song, Album

class SongFactory:
    @staticmethod
    def create_from_dto(song_dto):
        """Crea un modelo Song a partir de un DTO"""
        song = Song()
        song.title = song_dto.title
        song.artist_name = song_dto.artist_name
        song.genre = song_dto.genre
        song.price = song_dto.price
        song.release_date = song_dto.release_date
        song.song_cover = song_dto.song_cover
        song.song_file = song_dto.song_file
        return song

    @staticmethod
    def create_dto_from_model(song):
        """Crea un DTO a partir de un modelo Song"""

        return SongDTO(
            id=song.id,
            title=song.title,
            artist_name=song.artist_name,
            genre=song.genre,
            price=song.price,
            release_date=song.release_date,
            song_cover=song.song_cover,
            song_file=song.song_file
        )


class AlbumFactory:
    @staticmethod
    def create_album_from_dto(album_dto):
        return Album(
            title=album_dto.title,
            artist_name=album_dto.artist_name,
            genre=album_dto.genre,
            release_date=album_dto.release_date,
            album_cover=album_dto.album_cover,
            price=album_dto.price
        )

    @staticmethod
    def create_dto_from_album(album):
        return AlbumDTO(
            album_id=album.id,
            title=album.title,
            artist_name=album.artist_name,
            genre=album.genre,
            release_date=album.release_date,
            album_cover=album.album_cover,
            artist_id=getattr(album, 'artist_id', None),
            price=album.price
        )