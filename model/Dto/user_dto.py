# model/Dto/user_dto.py
from datetime import datetime


class UserDTO:
    def __init__(self, id=None, username=None, email=None, password=None, role='user',backend=None, **kwargs):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.backend = backend or 'django.contrib.auth.backends.ModelBackend'

        # Resto de campos...
        self.avatar = kwargs.get('avatar', 'avatars/usuario.png')
        self.credit_card_number = kwargs.get('credit_card_number', None)
        self.credit_card_expiry = kwargs.get('credit_card_expiry', None)
        self.bio = kwargs.get('bio', '')
        self.genre = kwargs.get('genre', '')
        self.country = kwargs.get('country', '')
        self.artist_name = kwargs.get('artist_name', None)
        self.artist_type = kwargs.get('artist_type', None)
        self.created_at = kwargs.get('created_at', datetime.now())

    def to_dict(self):
        data ={
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'avatar': self.avatar,
            'bio': self.bio,
            'genre': self.genre,
            'country': self.country,
            'artist_name': self.artist_name,
            'artist_type': self.artist_type,
            'role': self.role

        }
        if hasattr(self, 'backend'):
            data['backend'] = self.backend
        return data
