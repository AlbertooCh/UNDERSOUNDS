from django.urls import path
from controller.songs import SongController
from view.music import views  # Solo para las vistas que no son CRUD

urlpatterns = [
    # Vistas de catálogo (mantenidas en view/)
    path('catalogo/', views.catalogo, name='catalogo'),
    path('music_detail/', views.music_detail_redirect, name='music_detail'),
    path('music_detail/<int:id>/', views.music_detail, name='music_detail_id'),
    path('artist_detail/', views.artist_detail, name='artist_detail'),
    path('artist/panel/', views.artist_panel, name='artist_panel'),

    # Nuevas rutas CRUD usando SongController
    path('music/add/', SongController.create_song, name='add_song'),
    path('music/edit/<int:song_id>/', SongController.update_song, name='edit_song'),
    path('music/delete/<int:song_id>/', SongController.delete_song, name='delete_song'),
    path('artist_detail/', views.artist_detail, name='artist_detail'),

    # Ruta adicional para API REST (opcional)
    path('api/songs/', SongController.list_songs, name='api_song_list'),
    path('api/songs/<int:song_id>/', SongController.get_song, name='api_song_detail'),
]