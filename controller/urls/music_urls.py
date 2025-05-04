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
    path('add_comment/song/<int:song_id>/', login_required(views.add_commentSong), name='add_comment_to_song'),
    path('add_comment/album/<int:album_id>/', login_required(views.add_commentAlbum), name='add_comment_to_album'),
    path('delete_comment/<int:comment_id>/', login_required(views.delete_commentSong), name='delete_comment'),
    path('delete_comment_album/<int:comment_id>/', login_required(views.delete_commentAlbum), name='delete_comment_album'),

    path('favorites/add/', views.add_favorite, name='add_favorite'),
    path('favorites/remove/', views.remove_favorite, name='remove_favorite'),
    path('favorites/list/', views.list_favorites, name='list_favorites'),
    path('favorites/check/<str:item_type>/<int:item_id>/', views.check_favorite, name='check_favorite'),
    path('favoritos/', views.favorites_view, name='favoritos'),
    path('song/<int:song_id>/versions/', views.song_versions, name='song_versions'),
    path('song/<int:song_id>/restore/<int:version_id>/', views.restore_version, name='restore_version'),


]