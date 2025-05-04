from model.Dao.songVersion_dao import SongVersionDAO

class SongVersionDAO:
    @staticmethod
    def create_from_song(song):
        print(f"[DEBUG] Creating version for song: {song.title}")
        try:
            SongVersion.objects.create(
                song=song,
                title=song.title,
                artist_name=song.artist_name,
                genre=song.genre,
                price=song.price,
                release_date=song.release_date,
                song_cover=song.song_cover,
                song_file=song.song_file,
            )
            print("[DEBUG] Version saved successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to create version: {e}")
    @staticmethod
    def get_versions(song_id):
        return SongVersion.objects.filter(song_id=song_id).order_by('-saved_at')

    @staticmethod
    def update(song_dto):
        try:
            song = Song.objects.get(id=song_dto.id)

            # ✅ Save the previous version before updating
            SongVersionDAO.create_from_song(song)

            # Apply updates
            song.title = song_dto.title
            song.artist_name = song_dto.artist_name
            song.genre = song_dto.genre
            song.price = song_dto.price
            song.release_date = song_dto.release_date
            if song_dto.song_cover:
                song.song_cover = song_dto.song_cover
            if song_dto.song_file:
                song.song_file = song_dto.song_file

            song.save()
            return True
        except ObjectDoesNotExist:
            return False