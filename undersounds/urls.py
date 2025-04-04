"""
URL configuration for undersounds project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from view import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('inicio/', views.inicio, name='inicio'),
    path('contacto/', views.contacto, name='contacto'),
    path('admin/', admin.site.urls),
    path('music/', include('controller.urls.music_urls')),
    path('novedades/', views.novedades, name='novedades'),
    path('', include('controller.urls.music_urls')),
    path('', include('controller.urls.user_urls')),
    path('', include('controller.urls.store_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
