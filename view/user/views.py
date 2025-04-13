# user/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from controller.user_controller import UserController
from model.user.forms import FanRegisterForm, ArtistRegisterForm
from django.http import JsonResponse
from user.models import User
from model.Dao.user_dao import UserDAO
from model.Dao.store_dao import OrderDAO
from django.contrib.auth import logout as auth_logout
from model.music.music_models import Song
from model.store.store_models import Order

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
                artist_name=form.cleaned_data['artist_name']
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


@login_required
def perfil(request):
    user = UserController.get_current_user(request)
    if user and user.role == 'artist':
        user = UserController.get_artist_with_songs(request.user.id)
    return render(request, 'perfil.html', {'user': request.user})


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
    if request.method == 'POST' and request.FILES.get('avatar'):
        try:
            user = request.user
            user.avatar = request.FILES['avatar']
            user.save()
            return JsonResponse({
                'success': True,
                'avatar_url': user.avatar.url
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
    return JsonResponse({
        'success': False,
        'message': 'Solicitud inválida'
    }, status=400)

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
    if not request.user.is_authenticated:
        return redirect('login')

    # Versión con evaluación explícita
    orders = list(Order.objects.filter(user=request.user)
                  .select_related('user')
                  .prefetch_related('items__song')
                  .order_by('-created_at'))

    # Debug crítico
    print(f"Pedidos encontrados ({len(orders)}):", [o.id for o in orders])

    return render(request, 'historial_compras.html', {
        'orders': orders  # Asegúrate que coincide con el template
    })