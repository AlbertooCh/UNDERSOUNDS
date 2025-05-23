# user/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from controller.user_controller import UserController
from controller.music_controller import FavoriteController
from model.user.forms import FanRegisterForm, ArtistRegisterForm
from django.http import JsonResponse
from user.models import User
from model.Dao.user_dao import UserDAO
from model.Dao.store_dao import OrderDAO
from django.contrib.auth import logout as auth_logout
from model.music.music_models import Song
from model.store.store_models import Order
from django.core.exceptions import ValidationError

def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        user = UserController.login(request, username_or_email, password)

        if user:
            messages.success(request, f'Bienvenido {user.username}!')
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'login.html')


def register_fan(request):
    if request.method == 'POST':
        form = FanRegisterForm(request.POST)
        if form.is_valid():
            user = UserController.register_fan(
                request,
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            if user:
                messages.success(request, '¡Registro exitoso! Bienvenido.')
                return redirect('inicio')
    else:
        form = FanRegisterForm()
    return render(request, 'user/register.html', {'form': form})


def register_artist(request):
    if request.method == 'POST':
        form = ArtistRegisterForm(request.POST)
        if form.is_valid():
            user = UserController.register_artist(
                request,
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
                artist_name=form.cleaned_data['artist_name'],
                artist_type=form.cleaned_data['artist_type'],
                bio=form.cleaned_data['bio'],
                genre=form.cleaned_data['genre'],
                country=form.cleaned_data['country']

            )
            if user:
                messages.success(request, '¡Registro como artista exitoso!')
                return redirect('inicio')
    else:
        form = ArtistRegisterForm()
    return render(request, 'user/artist_register.html', {'form': form})


def logout_view(request):
    UserController.logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('inicio')


# Asegúrate de importar correctamente

@login_required
def perfil(request):
    user = UserController.get_current_user(request)

    if user and user.role == 'artist':
        user = UserController.get_artist_with_songs(request.user.id)
        seguidores = FavoriteController.get_artist_favorite_count(request.user.id)
    else:
        seguidores = None

    return render(request, 'perfil.html', {
        'user': request.user,
        'seguidores': seguidores
    })



@login_required
def configuracion(request):
    user_dto = UserController.get_user_settings(request.user.id)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            # Actualizar perfil
            UserController.update_user_profile(
                request.user.id,
                bio=request.POST.get('bio'),
                genre=request.POST.get('genre'),
                country=request.POST.get('country')
            )
            messages.success(request, 'Perfil actualizado correctamente')

        elif 'change_password' in request.POST:
            # Cambiar contraseña
            if UserController.update_user_password(
                    request.user.id,
                    request.POST.get('current_password'),
                    request.POST.get('new_password')
            ):
                messages.success(request, 'Contraseña cambiada correctamente')
            else:
                messages.error(request, 'La contraseña actual es incorrecta')

        elif 'update_avatar' in request.FILES:
            # Actualizar avatar
            UserController.upload_avatar(request.user.id, request.FILES['avatar'])
            messages.success(request, 'Avatar actualizado correctamente')

        elif 'update_notifications' in request.POST:
            # Actualizar notificaciones
            UserController.update_user_notifications(
                request.user.id,
                {
                    'email': request.POST.get('email_notifications') == 'on',
                    'releases': request.POST.get('release_notifications') == 'on',
                    'messages': request.POST.get('message_notifications') == 'on'
                }
            )
            messages.success(request, 'Preferencias de notificación actualizadas')

        return redirect('account_settings')

    return render(request, 'user/configuracion.html', {
        'user': user_dto
    })


@login_required
def historial_compras(request):
    return render(request, 'historial_compras.html')


@login_required
def mis_obras(request):
    return render(request, 'mis_obras.html')

@login_required
def upload_avatar(request):
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': 'Método no permitido. Se requiere POST.'
        }, status=405)  # 405 Method Not Allowed

    if not request.FILES.get('avatar'):
        return JsonResponse({
            'success': False,
            'message': 'No se proporcionó archivo de avatar.'
        }, status=400)

    try:
        avatar_file = request.FILES['avatar']

        # Validaciones básicas del archivo
        if avatar_file.size > 5 * 1024 * 1024:  # 5MB máximo
            raise ValidationError('El archivo es demasiado grande (máx. 5MB)')

        if not avatar_file.content_type.startswith('image/'):
            raise ValidationError('Solo se permiten archivos de imagen')

        # Procesar la actualización
        user = request.user
        user.avatar = avatar_file
        user.save()

        return JsonResponse({
            'success': True,
            'avatar_url': user.avatar.url,
            'message': 'Avatar actualizado correctamente'
        })

    except ValidationError as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

    except Exception as e:
        # Loggear el error para debugging (opcional)
        # logger.error(f"Error al actualizar avatar: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'Error interno del servidor'
        }, status=500)

@login_required
def update_profile(request):
    if request.method == 'POST':
        success = UserController.update_user_profile(
            request.user.id,
            username=request.POST.get('username'),
            bio=request.POST.get('bio')
        )
        return JsonResponse({
            'success': success,
            'new_username': request.POST.get('username') if success else None
        })
    return JsonResponse({'success': False}, status=400)


@login_required
def delete_account(request):
    if request.method == 'POST':
        UserDAO.delete(request.user.id)
        auth_logout(request)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required
def deactivate_account(request):
    if request.method == 'POST':
        UserDAO.delete(request.user.id)
        auth_logout(request)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required
def change_password(request):
    if request.method == 'POST':
        success = UserController.update_user_password(
            request.user.id,
            current_password=request.POST.get('current_password'),
            new_password=request.POST.get('new_password')
        )
        return JsonResponse({'success': success})
    return JsonResponse({'success': False}, status=400)

@login_required
def my_songs(request):
    user_songs = Song.objects.filter(artist=request.user)
    return render(request, 'user/mis_obras.html', {'user_songs': user_songs})

@login_required
def order_history(request):
    order = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'historial_compras.html', {'orders': order})
def oauth_callback(request):
    # Ejemplo para Google OAuth
    email = request.GET.get('email')  # Obtener email del callback
    user = UserController.handle_oauth_user(request, email)
    if user:
        return redirect('inicio')
    else:
        messages.error(request, 'Error en autenticación OAuth')
        return redirect('login')

