from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from user.models import User


def login(request):
    return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        user = User.objects.create_user(username=username, email=email, password=password)
        return redirect("login")
    return render(request, "register.html")


def perfil(request):
    return render(request, 'perfil.html')
# Create your views here.

def configuracion(request):
    return render(request, 'configuracion.html')

def historial_compras(request):
    return render(request, 'historial_compras.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect("home")