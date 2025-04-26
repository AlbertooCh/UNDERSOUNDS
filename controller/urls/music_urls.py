from django.urls import path
from django.contrib.auth.decorators import login_required
from view.music import views

urlpatterns = [
    # Catálogo y detalles
    path('catalogo/', views.catalogo, name='catalogo'),
    path('music_detail/', views.music_detail_redirect, name='music_detail'),
    path('music_detail/<int:id>/', views.music_detail, name='music_detail_id'),

    # Artista
    path('artist_detail/', login_required(views.artist_detail), name='artist_detail'),
    path('artist/panel/', login_required(views.artist_panel), name='artist_panel'),

    # CRUD de canciones (protegidas por login y rol de artista)
    path('music/add/', login_required(views.add_song), name='add_song'),
    path('music/edit/<int:song_id>/', login_required(views.edit_song), name='edit_song'),
    path('music/delete/<int:song_id>/', login_required(views.delete_song), name='delete_song'),
    path('save-song/', views.save_song, name='save_song'),
    path('delete-song/', views.delete_song, name='delete_song'),
    path('add_comment/<int:song_id>/', login_required(views.add_comment), name='add_comment'),

]