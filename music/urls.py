from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('catalogo/', views.catalogo, name='catalogo'),

]

