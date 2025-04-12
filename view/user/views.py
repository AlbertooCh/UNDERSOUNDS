# user/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from controller.user_controller import UserController
from model.user.forms import FanRegisterForm, ArtistRegisterForm


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
    return render(request, 'perfil.html', {'user': user})


@login_required
def configuracion(request):
    return render(request, 'configuracion.html')


@login_required
def historial_compras(request):
    return render(request, 'historial_compras.html')


@login_required
def mis_obras(request):
    return render(request, 'mis_obras.html')