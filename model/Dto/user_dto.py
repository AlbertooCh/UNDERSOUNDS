# model/Dto/user_dto.py
from datetime import datetime

class UserDTO:
    def __init__(self, id=None, username=None, email=None, password=None, role='user',
                 credit_card_number=None, credit_card_expiry=None,
                 artist_name=None, artist_type=None, bio=None,
                 genre=None, country=None, created_at=None, songs=[]):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.credit_card_number = credit_card_number
        self.credit_card_expiry = credit_card_expiry
        self.artist_name = artist_name
        self.artist_type = artist_type
        self.bio = bio
        self.genre = genre
        self.country = country
        self.created_at = created_at or datetime.now()
        self.songs = songs

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'credit_card_number': self.credit_card_number,
            'credit_card_expiry': self.credit_card_expiry,
            'artist_name': self.artist_name,
            'artist_type': self.artist_type,
            'bio': self.bio,
            'genre': self.genre,
            'country': self.country,
            'created_at': self.created_at
        }