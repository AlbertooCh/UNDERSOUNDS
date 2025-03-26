from django.urls import path
from django.views.generic import RedirectView

from . import views
from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('catalogo/', views.catalogo, name='catalogo'),
    path('music_detail/', views.music_detail, name='music_detail'),

]

