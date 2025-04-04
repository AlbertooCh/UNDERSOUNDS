from django.core.exceptions import ObjectDoesNotExist
from model.music.music_models import Song
from model.dto.song_dto import SongDTO

class SongDAO:
    @staticmethod
    def create(song_dto: SongDTO) -> SongDTO:
        song = Song.objects.create(
            title=song_dto.title,
            artist_name=song_dto.artist_name,
            album_title=song_dto.album_title,
            genre=song_dto.genre,
            price=song_dto.price,
            release_date=song_dto.release_date,
            album_cover=song_dto.album_cover_path,
            song_file=song_dto.song_file_path
        )
        return SongDTO.from_model(song)

    @staticmethod
    def get_by_id(song_id: int) -> SongDTO:
        try:
            song = Song.objects.get(pk=song_id)
            return SongDTO.from_model(song)
        except ObjectDoesNotExist:
            raise ValueError(f"Song with id {song_id} does not exist")

    @staticmethod
    def update(song_dto: SongDTO) -> SongDTO:
        song = Song.objects.get(pk=song_dto.id)
        for field, value in song_dto.__dict__.items():
            if field != 'id' and hasattr(song, field):
                setattr(song, field, value)
        song.save()
        return SongDTO.from_model(song)

    @staticmethod
    def delete(song_id: int) -> None:
        Song.objects.filter(pk=song_id).delete()

    @staticmethod
    def get_all() -> list[SongDTO]:
        return [SongDTO.from_model(song) for song in Song.objects.all()]