# model/Dao/user_dao.py
from django.contrib.auth.hashers import make_password, check_password
from user.models import User
from model.Dto.user_dto import UserDTO
from django.contrib.auth.backends import ModelBackend


class UserDAO:
    @staticmethod
    def create(user_dto):
        user = User(
            username=user_dto.username,
            email=user_dto.email,
            password=make_password(user_dto.password),
            role=user_dto.role,
            credit_card_number=user_dto.credit_card_number,
            credit_card_expiry=user_dto.credit_card_expiry,
            artist_name=user_dto.artist_name,
            artist_type=user_dto.artist_type,
            bio=user_dto.bio,
            genre=user_dto.genre,
            country=user_dto.country
        )
        user.backend = f'{ModelBackend.__module__}.{ModelBackend.__qualname__}'  # Asignar backend
        user.save()
        return user

    @staticmethod
    def get_by_id(user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_by_username(username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_by_email(email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    @staticmethod
    def authenticate(username_or_email, password):
        user = UserDAO.get_by_username(username_or_email) or UserDAO.get_by_email(username_or_email)

        if user and check_password(password, user.password):
            # Asegurar que el backend está asignado
            if not hasattr(user, 'backend'):
                user.backend = f'{ModelBackend.__module__}.{ModelBackend.__qualname__}'
                user.save(update_fields=['backend'])
            return user
        return None

    @staticmethod
    def update(user_dto):
        user = UserDAO.get_by_id(user_dto.id)
        if user:
            # Actualiza solo los campos permitidos (excluyendo password y campos sensibles)
            for field in ['username', 'email', 'avatar', 'bio', 'genre', 'country', 'artist_name', 'artist_type']:
                if hasattr(user_dto, field):
                    setattr(user, field, getattr(user_dto, field))
            user.save()
            return user
        return None

    @staticmethod
    def delete(user_id):
        user = UserDAO.get_by_id(user_id)
        if user:
            user.delete()
            return True
        return False

    @staticmethod
    def update_profile(user_id, **kwargs):
        try:
            user = User.objects.get(pk=user_id)
            for field, value in kwargs.items():
                if hasattr(user, field):
                    setattr(user, field, value)
            user.save()
            return True
        except User.DoesNotExist:
            return False

    @staticmethod
    def change_password(user_id, current_password, new_password):
        user = User.objects.get(pk=user_id)
        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            return True
        return False

    @staticmethod
    def upload_avatar(user_id, avatar_file):
        try:
            user = User.objects.get(pk=user_id)
            user.avatar = avatar_file
            user.save()
            return True
        except User.DoesNotExist:
            return False

    @staticmethod
    def get_or_create_oauth_user(user_dto):
        try:
            user = User.objects.get(email=user_dto.email)
            created = False
        except User.DoesNotExist:
            user = User(
                username=user_dto.username,
                email=user_dto.email,
                is_active=True,
                backend=user_dto.backend
            )
            user.set_unusable_password()  # Usuarios OAuth no usan password
            user.save()
            created = True

        # Actualizar campos si es necesario
        for field in ['avatar', 'first_name', 'last_name']:
            if hasattr(user_dto, field):
                setattr(user, field, getattr(user_dto, field))
        user.save()

        return user, created