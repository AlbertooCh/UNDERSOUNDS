from django.shortcuts import render

def carrito(request):
    return render(request, 'carrito.html')
# Create your views here.
def pago(request):
    return render(request, 'pago.html')
