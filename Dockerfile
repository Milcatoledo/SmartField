# Dockerfile para SmartField
FROM python:3.11-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgthread-2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de proyecto
COPY . .

# Instalar dependencias directamente con pip (más simple)
RUN pip install --no-cache-dir \
    flask>=2.3.0 \
    flask-socketio>=5.3.0 \
    tensorflow>=2.13.0 \
    opencv-python-headless>=4.8.0 \
    pillow>=10.0.0 \
    numpy>=1.24.0 \
    python-dotenv>=1.0.0 \
    eventlet>=0.33.0 \
    python-socketio>=5.8.0 \
    requests>=2.31.0

# Crear directorios necesarios
RUN mkdir -p static/images models logs

# Crear usuario no-root para seguridad
RUN useradd --create-home --shell /bin/bash smartfield && \
    chown -R smartfield:smartfield /app

# Cambiar a usuario no-root
USER smartfield

# Exponer puerto
EXPOSE 5000

# Variables de entorno
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Comando de inicio
CMD ["python", "app.py"]