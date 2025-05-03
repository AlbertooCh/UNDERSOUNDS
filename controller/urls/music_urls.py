from django.urls import path
from django.contrib.auth.decorators import login_required
from view.music import views

urlpatterns = [
    # Catálogo y detalles
    path('catalogo/', views.catalogo, name='catalogo'),
    path('music_detail/', views.music_detail_redirect, name='music_detail'),
    path('music_detail/<int:id>/', views.music_detail, name='music_detail_id'),

    # Artista
    path('artist_detail/<str:artist_name>/', views.artist_detail, name='artist_detail'),
    path('artist/panel/', login_required(views.artist_panel), name='artist_panel'),

    # CRUD de canciones (protegidas por login y rol de artista)
    path('music/add_song/', login_required(views.add_song), name='add_song'),
    path('music/add_album/', login_required(views.add_album), name='add_album'),
    path('album/<int:album_id>/edit/', views.edit_album, name='edit_album'),
    path('album/<int:album_id>/add_song/', views.add_song_to_album, name='add_song_to_album'),
    path('album/<int:album_id>/', views.album_detail, name='album_detail'),
    path('album/<int:album_id>/delete/', views.delete_album, name='delete_album'),
    path('song/<int:song_id>/remove-from-album/<int:album_id>/', views.remove_song_from_album, name='remove_song_from_album'),
    path('music/edit/<int:song_id>/', login_required(views.edit_song), name='edit_song'),
    path('music/delete/<int:song_id>/', login_required(views.delete_song), name='delete_song'),
    path('save-song/', views.save_song, name='save_song'),
    path('delete-song/', views.delete_song, name='delete_song'),
    path('add_comment/<int:song_id>/', login_required(views.add_comment), name='add_comment'),

]