from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'
    label = 'user'  # This is crucial for the app label to be recognized correctly
    #Comentario para el push
