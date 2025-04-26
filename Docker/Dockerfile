# Utilizamos una imagen base de Python. Puedes elegir la versión que necesites.
FROM python:3.11-slim-buster

# Establecemos el directorio de trabajo dentro del contenedor.
WORKDIR /UNDERSOUNDS

# Copiamos nuestro código en el contenedor

COPY ../ .

# Instalamos las dependencias de la aplicación.
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m pip install Pillow

# Exponemos el puerto en el que la aplicación Django escuchará (por defecto es el 8000).
EXPOSE 8000

# Comando para ejecutar la aplicación Django.

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]