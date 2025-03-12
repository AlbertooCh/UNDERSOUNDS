from django.shortcuts import render

def inicio(request):
    return render(request, 'core/inicio.html')    #must contain core/ , the path is core/inicio

def contacto(request):
    return render(request, 'core/contacto.html')  #must contain core/ , the path is core/contacto

def novedades(request):
    return render(request, 'core/novedades.html') #must contain core/ , the path is core/novedades