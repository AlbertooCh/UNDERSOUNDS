from django.shortcuts import render

# Create your views here.
def carrito(request):
    return render(request, "store/carrito.html")

def pago(request):
    return render(request, "store/pago.html")
