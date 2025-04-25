# UNDERSOUNDS
Proyecto UNDERSOUNDS

Para la utilización de la página hay que seguir los siguientes comandos.

1- 
  python manage.py makemigrations
2-
  python manage.py migrate
3-
  python manage.py runserver

Los dos primeros pasos son necesarios la primera vez que se ejecuta el proyecto o al hacer un cambio en los modelos,
esto creará la base de datos.

Para el docker(tarda un rato segun la velocidad de internet)
Tener abierto el docker: 
1- docker build -t nombre .
2- En la aplicacion, en imagenes os aparecera la imagen dle proyecto, le dais ejecutar, poneis 0 para genera un puerto aleatorio.
3- aparecera la direccion debajo del nombre del contenedor en forma de enlace, clicais y os lleva directamente a la pagina
