# model/controllers/user_controller.py
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.backends import ModelBackend
from model.Dao.user_dao import UserDAO
from model.Factory.user_factory import UserFactory
from model.Dto.user_dto import UserDTO
from user.models import User

class UserController:
    @staticmethod
    def login(request, username_or_email, password):
        user = UserDAO.authenticate(username_or_email, password)
        if user:
            # Asegurar que el backend está asignado
            if not hasattr(user, 'backend'):
                user.backend = f'{ModelBackend.__module__}.{ModelBackend.__qualname__}'
                user.save(update_fields=['backend'])
            auth_login(request, user, backend=user.backend)  # Login explícito con backend
            return UserFactory.create_from_model(user)
        return None

    @staticmethod
    def logout(request):
        auth_logout(request)

    @staticmethod
    def register_fan(request, username, email, password, **kwargs):
        user_dto = UserFactory.create_fan(username, email, password, **kwargs)
        user = UserDAO.create(user_dto)
        if user:
            auth_login(request, user, backend=user.backend)
            return UserFactory.create_from_model(user)
        return None

    @staticmethod
    def register_artist(request, username, email, password, artist_name, **kwargs):
        user_dto = UserFactory.create_artist(username, email, password, artist_name, **kwargs)
        user = UserDAO.create(user_dto)
        if user:
            auth_login(request, user, backend=user.backend)
            return UserFactory.create_from_model(user)
        return None

    @staticmethod
    def handle_oauth_user(request, email, **kwargs):
        """Maneja el registro/login de usuarios OAuth"""
        user_dto = UserFactory.create_for_oauth(email, **kwargs)
        user, created = UserDAO.get_or_create_oauth_user(user_dto)
        if user:
            auth_login(request, user, backend=user.backend)
            return UserFactory.create_from_model(user)
        return None

    @staticmethod
    def get_current_user(request):
        if request.user.is_authenticated:
            # Asegurar que el backend está asignado
            if not hasattr(request.user, 'backend'):
                request.user.backend = f'{ModelBackend.__module__}.{ModelBackend.__qualname__}'
                request.user.save(update_fields=['backend'])
            return UserFactory.create_from_model(request.user)
        return None

    @staticmethod
    def update_profile(user_id, **kwargs):
        user = UserDAO.get_by_id(user_id)
        if user:
            user_dto = UserFactory.create_from_model(user)
            for key, value in kwargs.items():
                if hasattr(user_dto, key):
                    setattr(user_dto, key, value)
            return UserDAO.update(user_dto)
        return None

    @staticmethod
    def get_artist_with_songs(user_id):
        user = UserDAO.get_by_id(user_id)
        if user and user.role == 'artist':
            user_dto = UserFactory.create_from_model(user)
            user_dto.songs = user.songs.all()
            user_dto.albums = user.albums.all()
            return user_dto
        return None

    @staticmethod
    def add_song_to_artist(artist_id, song_id):
        artist = UserDAO.get_by_id(artist_id)
        if artist and artist.role == 'artist':
            artist.songs.add(song_id)
            return True
        return False

    @staticmethod
    def add_album_to_artist(album_id, artist_id):
        artist = UserDAO.get_by_id(artist_id)
        if artist and artist.role == 'artist':
            artist.albums.add(album_id)
            return True

    @staticmethod
    def get_user_settings(user_id):
        user = UserDAO.get_by_id(user_id)
        return UserFactory.create_from_model(user) if user else None

    @staticmethod
    def update_user_profile(user_id, **kwargs):
        return UserDAO.update_profile(user_id, **kwargs)

    @staticmethod
    def update_user_password(user_id, current_password, new_password):
        return UserDAO.change_password(user_id, current_password, new_password)

    @staticmethod
    def upload_avatar(user_id, avatar_file):
        return UserDAO.update_profile(user_id, avatar=avatar_file)

    @staticmethod
    def change_password(user_id, current_password, new_password):
        user = UserDAO.get_by_id(user_id)
        if user and user.check_password(current_password):
            user.set_password(new_password)
            # Mantener el backend después de cambiar la contraseña
            user.backend = getattr(user, 'backend', f'{ModelBackend.__module__}.{ModelBackend.__qualname__}')
            user.save()
            return True
        return False