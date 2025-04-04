# controller/songs.py
from django.http import JsonResponse, HttpRequest, HttpResponse
from model.dto.song_dto import SongDTO
from model.factory.song_factory import SongFactory
from model.music.music_models import Song
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class SongController:
    @staticmethod
    def create_song(request: HttpRequest) -> HttpResponse:
        try:
            # 1. Validación básica
            if not request.method == 'POST':
                return JsonResponse({'error': 'Método no permitido'}, status=405)

            # 2. Convertir request a DTO usando Factory
            song_data = request.POST.dict() or request.json()
            song_dto = SongFactory.create_from_request_data(song_data)

            # 3. Persistir usando DAO
            created_song = Song.create(song_dto)

            # 4. Responder con DTO creado
            return JsonResponse({
                'id': created_song.id,
                'title': created_song.title,
                'artist': created_song.artist_name,
                'status': 'created'
            }, status=201)

        except Exception as e:
            logger.error(f"Error creating song: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)

    @staticmethod
    def get_song(request: HttpRequest, song_id: int) -> HttpResponse:
        try:
            # 1. Obtener canción usando DAO
            song_dto = Song.get_by_id(song_id)

            # 2. Formatear respuesta
            return JsonResponse({
                'id': song_dto.id,
                'title': song_dto.title,
                'album': song_dto.album_title,
                'price': float(song_dto.price),
                'release_date': song_dto.release_date.isoformat(),
                'links': {
                    'self': f'/songs/{song_dto.id}',
                    'album_cover': song_dto.album_cover_path
                }
            })

        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=404)
        except Exception as e:
            logger.error(f"Error fetching song {song_id}: {str(e)}")
            return JsonResponse({'error': 'Server error'}, status=500)

    @staticmethod
    def list_songs(request: HttpRequest) -> HttpResponse:
        try:
            # 1. Obtener parámetros de filtrado
            genre = request.GET.get('genre')
            min_price = float(request.GET.get('min_price', 0))

            # 2. Obtener todas las canciones usando DAO
            songs = Song.get_all()

            # 3. Filtrar (mejor hacerlo en DAO para eficiencia)
            filtered_songs = [
                song for song in songs
                if (not genre or song.genre == genre)
                   and float(song.price) >= min_price
            ]

            # 4. Formatear respuesta
            return JsonResponse({
                'count': len(filtered_songs),
                'results': [{
                    'id': song.id,
                    'title': song.title,
                    'artist': song.artist_name,
                    'price': float(song.price)
                } for song in filtered_songs]
            })

        except Exception as e:
            logger.error(f"Error listing songs: {str(e)}")
            return JsonResponse({'error': 'Server error'}, status=500)

    @staticmethod
    def update_song(request: HttpRequest, song_id: int) -> HttpResponse:
        try:
            # 1. Validar método
            if request.method not in ['PUT', 'PATCH']:
                return JsonResponse({'error': 'Método no permitido'}, status=405)

            # 2. Obtener canción existente
            existing_song = Song.get_by_id(song_id)

            # 3. Actualizar datos
            update_data = request.POST.dict() or request.json()
            for field, value in update_data.items():
                if hasattr(existing_song, field):
                    setattr(existing_song, field, value)

            # 4. Persistir cambios
            updated_song = Song.update(existing_song)

            return JsonResponse({
                'status': 'updated',
                'song_id': updated_song.id
            })

        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=404)
        except Exception as e:
            logger.error(f"Error updating song {song_id}: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)

    @staticmethod
    def delete_song(request: HttpRequest, song_id: int) -> HttpResponse:
        try:
            Song.delete(song_id)
            return JsonResponse({
                'status': 'deleted',
                'song_id': song_id
            }, status=204)

        except Exception as e:
            logger.error(f"Error deleting song {song_id}: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)