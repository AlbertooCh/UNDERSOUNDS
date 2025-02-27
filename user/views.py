from django.shortcuts import render

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def perfil(request):
    return render(request, 'perfil.html')
# Create your views here.
