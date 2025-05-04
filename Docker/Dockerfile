# Use official Python base image
FROM python:3.13.2-slim-bullseye

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app
COPY requirements.txt /app/requirements.txt

# Copy the full project from the parent directory (UNDERSOUNDS root)
COPY .. /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install gunicorn Pillow

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Start using Gunicorn with correct module path
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "undersounds.wsgi:application"]

