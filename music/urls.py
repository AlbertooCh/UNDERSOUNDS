from django.urls import path
from django.views.generic import RedirectView

from . import views
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('catalogo/', views.catalogo, name='catalogo'),
    path('music_detail/', views.music_detail_redirect, name='music_detail'),  # optional
    path('music_detail/<int:id>/', views.music_detail, name='music_detail_id'),
    path('artist_detail/', views.artist_detail, name='artist_detail'),

    # CRUD Music
    path('music/add/', views.add_song, name='add_song'),
    path('music/edit/<int:song_id>/', views.edit_song, name='edit_song'),
    path('music/delete/<int:song_id>/', views.delete_song, name='delete_song'),
    path('artist/panel/', views.artist_panel, name='artist_panel'), # panel for artist to see his all songs

]
