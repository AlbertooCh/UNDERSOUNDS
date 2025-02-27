from django.shortcuts import render

def login(request):
    return render(request, 'inicio_sesion.html')

def register(request):
    return render(request, 'registro.html')

def perfil(request):
    return render(request, 'perfil.html')
# Create your views here.
