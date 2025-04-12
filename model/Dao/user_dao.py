# model/Dao/user_dao.py
from django.contrib.auth.hashers import make_password, check_password
from user.models import User
from model.Dto.user_dto import UserDTO


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
        # Try by username first
        user = UserDAO.get_by_username(username_or_email)
        if not user:
            # Try by email
            user = UserDAO.get_by_email(username_or_email)

        if user and check_password(password, user.password):
            return user
        return None

    @staticmethod
    def update(user_dto):
        user = UserDAO.get_by_id(user_dto.id)
        if user:
            for field, value in user_dto.to_dict().items():
                if field == 'password' and value:
                    user.password = make_password(value)
                elif field != 'created_at' and hasattr(user, field):
                    setattr(user, field, value)
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