from model.Dto.music_dto import SongDTO
from model.music.music_models import Song

class SongFactory:
    @staticmethod
    def create_from_dto(song_dto):
        """Crea un modelo Song a partir de un DTO"""
        song = Song()
        song.title = song_dto.title
        song.artist_name = song_dto.artist_name
        song.album_title = song_dto.album_title
        song.genre = song_dto.genre
        song.price = song_dto.price
        song.release_date = song_dto.release_date
        song.album_cover = song_dto.album_cover
        song.song_file = song_dto.song_file
        return song

    @staticmethod
    def create_dto_from_model(song):
        """Crea un DTO a partir de un modelo Song"""
        return SongDTO(
            id=song.id,
            title=song.title,
            artist_name=song.artist_name,
            album_title=song.album_title,
            genre=song.genre,
            price=song.price,
            release_date=song.release_date,
            album_cover=song.album_cover,
            song_file=song.song_file
        )