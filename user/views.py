from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FanRegisterForm, ArtistRegisterForm
from django.contrib.auth import authenticate, login
from user.models import User


def login_view(request):
    return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        user = User.objects.create_user(username=username, email=email, password=password)
        return redirect("login")
    return render(request, "user/register.html")

def register_artist(request):
    if request.method == 'POST':
        form = ArtistRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro como artista exitoso!')
            return redirect('home')
    else:
        form = ArtistRegisterForm()
    return render(request, 'user/artist_register.html', {'form': form})


def perfil(request):
    return render(request, 'perfil.html')
# Create your views here.

def configuracion(request):
    return render(request, 'configuracion.html')

def historial_compras(request):
    return render(request, 'historial_compras.html')
def mis_obras(request):
    return render(request, 'mis_obras.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect("home")


def register_fan(request):
    if request.method == 'POST':
        form = FanRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido.')
            return redirect('home')  # change to your homepage
    else:
        form = FanRegisterForm()
    return render(request, 'user/register.html', {'form': form})


def register_artist(request):
    if request.method == 'POST':
        form = ArtistRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro como artista exitoso!')
            return redirect('home')
    else:
        form = ArtistRegisterForm()
    return render(request, 'user/artist_register.html', {'form': form})