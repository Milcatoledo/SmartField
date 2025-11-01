# Dockerfile optimizado para SmartField
FROM python:3.11-slim

# Instalar solo dependencias de runtime necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Crear directorio de trabajo
WORKDIR /app

# Copiar solo requirements primero para mejor cacheo
COPY requirements.txt .

# Instalar dependencias con binarios precompilados (versiones específicas)
RUN pip install --no-cache-dir --only-binary=all \
    flask==2.3.3 \
    flask-sock \
    flask-socketio==5.3.6 \
    tensorflow-cpu==2.20.0 \
    opencv-python-headless==4.8.1.78 \
    pillow==10.2.0 \
    numpy==1.26.0 \
    python-dotenv==1.0.1 \
    eventlet==0.33.3 \
    python-socketio==5.10.0 \
    requests==2.31.0

# Copiar solo archivos necesarios
COPY app.py models.py ./
COPY templates/ ./templates/
COPY static/ ./static/
COPY models/ ./models/

# Crear directorios necesarios
RUN mkdir -p static/images logs

# Crear usuario no-root para seguridad
RUN adduser --disabled-password --gecos '' smartfield && \
    chown -R smartfield:smartfield /app

# Cambiar a usuario no-root
USER smartfield

# Exponer puerto
EXPOSE 5000

# Variables de entorno optimizadas
ENV FLASK_APP=app.py \
    FLASK_ENV=production \
    PYTHONPATH=/app \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/api/health', timeout=5)"

# Comando de inicio
CMD ["python", "-u", "app.py"]