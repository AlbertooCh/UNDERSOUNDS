# model/Factory/user_factory.py
from model.Dto.user_dto import UserDTO

class UserFactory:
    @staticmethod
    def create_from_model(user_model):
        return UserDTO(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            avatar=user_model.avatar.url if user_model.avatar else None,
            bio=user_model.bio,
            genre=user_model.genre,
            country=user_model.country,
            created_at=user_model.created_at,
            role=user_model.role,
            artist_name=user_model.artist_name,
            artist_type=user_model.artist_type
        )

    @staticmethod
    def create_fan(username, email, password, **kwargs):
        return UserDTO(
            username=username,
            email=email,
            password=password,
            role='user',
            **kwargs
        )

    @staticmethod
    def create_artist(username, email, password, artist_name, **kwargs):
        return UserDTO(
            username=username,
            email=email,
            password=password,
            role='artist',
            artist_name=artist_name,
            **kwargs
        )