from model.Dto.music_dto import SongDTO, AlbumDTO, FavoriteDTO, FavoriteItemDTO
from model.music.music_models import Song, Album, Favorite
from user.models import User

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
        )

class FavoriteFactory:
    @staticmethod
    def dto_to_model(favorite_dto: FavoriteDTO) -> Favorite:
        return Favorite(
            user_id=favorite_dto.user_id,
            song_id=favorite_dto.song_id,
            album_id=favorite_dto.album_id,
            artist_id=favorite_dto.artist_id
        )

    @staticmethod
    def model_to_dto(favorite: Favorite) -> FavoriteDTO:
        return FavoriteDTO(
            id=favorite.id,
            user_id=favorite.user_id,
            song_id=favorite.song_id,
            album_id=favorite.album_id,
            artist_id=favorite.artist_id,
            created_at=favorite.created_at
        )

    @staticmethod
    def model_to_item_dto(favorite: Favorite) -> FavoriteItemDTO:
        if favorite.song:
            item = {
                'id': favorite.song.id,
                'title': favorite.song.title,
                'artist_name': favorite.song.artist_name,
                'cover_url': favorite.song.song_cover.url if favorite.song.song_cover else None
            }
            item_type = 'song'
        elif favorite.album:
            item = {
                'id': favorite.album.id,
                'title': favorite.album.title,
                'artist_name': favorite.album.artist_name,
                'cover_url': favorite.album.album_cover.url if favorite.album.album_cover else None
            }
            item_type = 'album'
        elif favorite.artist_id:
            # Obtenemos el artista usando get_user_model()
            artist = User.objects.get(id=favorite.artist_id)
            item = {
                'id': artist.id,
                'name': artist.username,
                'avatar_url': artist.avatar.url if artist.avatar else None
            }
            item_type = 'artist'
        else:
            raise ValueError("Invalid favorite item")

        return FavoriteItemDTO(
            id=favorite.id,
            type=item_type,
            item=item,
            created_at=favorite.created_at
        )