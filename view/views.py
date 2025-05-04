from django.shortcuts import render
from model.music.music_models import Song
from controller.music_controller import SongController
from controller.store_controller import OrderController

def inicio(request):
    return render(request, 'core/inicio.html')    #must contain core/ , the path is core/inicio

def contacto(request):
    return render(request, 'core/contacto.html')  #must contain core/ , the path is core/contacto


def populares(request):
    tipo = request.GET.get('type', 'songs')  # valor por defecto: songs
    ventas = OrderController.get_mas_vendidos()
    canciones_populares = ventas.get('top_songs', [])
    albums_populares = ventas.get('top_albums', [])

    # Debug para verificar qué se está cargando
    print("=== Vista Populares ===")
    print("Tipo solicitado:", tipo)
    print("Canciones populares:")
    for item in canciones_populares:
        print(f"  - {item['song'].title} (Ventas: {item['total_sales']})")

    print("Álbumes populares:")
    for item in albums_populares:
        print(f"  - {item['album'].title} (Ventas: {item['total_sales']})")

    context = {
        "show_type": tipo,
        "songs": [item['song'] for item in canciones_populares],
        "albums": [item['album'] for item in albums_populares],
    }

    return render(request, 'populares.html', context)
