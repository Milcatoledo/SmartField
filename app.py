
import os
import uuid
import logging
from models import predict
import base64
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'smartfield-secret-key-2024')

# Configurar SocketIO
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode='eventlet',
    ping_timeout=int(os.environ.get('WEBSOCKET_PING_TIMEOUT', 60)),
    ping_interval=int(os.environ.get('WEBSOCKET_PING_INTERVAL', 25))
)

# Configuración de directorios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

logger.info(f"Base directory: {BASE_DIR}")
# logger.info(f"Upload folder: {UPLOAD_FOLDER}")
# logger.info(f"Models directory: {MODELS_DIR}")

# Rutas Flask
@app.route("/")
def home():
    """Página principal"""
    return render_template("index.html")

@app.route("/stream")
def stream():
    """Página de streaming WebSocket"""
    return render_template("stream.html")

@app.route("/selectSource")
def source():
    """Página de selección de fuente"""
    return render_template("selectSource.html")

@app.route("/api/models")
def api_models():
    """API para obtener modelos disponibles"""
    try:
        models_available = {
            'acm': 'ACM_ponchi_73%_0.9_final.keras',
            'mobilenet': 'mobilenet_cacao__84%_0.68_final.keras',
            'resnet': 'resnet_cacao_89%_0.48_final.keras',
            'xception': 'xception_cacao_89%_0.43_final.keras'
        }
        return jsonify({
            'status': 'success',
            'models': models_available
        })
    except Exception as e:
        logger.error(f"Error obteniendo modelos: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route("/api/health")
def api_health():
    """Endpoint de salud para monitoreo"""
    try:
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '2.0.0'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500







# ==================== WEBSOCKET EVENTS ====================

@socketio.on('connect')
def handle_connect():
    """Maneja conexiones WebSocket"""
    logger.info("Nueva conexión WebSocket")
    emit('connection_confirmed', {
        'status': 'connected',
        'available_models': ['acm', 'mobilenet', 'resnet', 'xception']
    })


@socketio.on('disconnect')
def handle_disconnect():
    """Maneja desconexiones WebSocket"""
    logger.info("Desconexión WebSocket")


@socketio.on('image_frame')
def handle_image_frame(data):
    """Recibe y procesa frames de imagen (funcionalidad básica)"""
    try:
        logger.info("Frame recibido via WebSocket")
        
        # Validar datos
        if 'image' not in data or 'model' not in data:
            emit('error', {'message': 'Datos incompletos'})
            return
        
        # Por ahora, enviar confirmación simple
        emit('analysis_result', {
            'category': 'Etapa 1',  # Resultado simulado
            'percentages': [0.7, 0.2, 0.05, 0.05],
            'model_name': data['model'],
            'confidence': 0.7,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error procesando frame: {e}")
        emit('error', {'message': f'Error procesando imagen: {str(e)}'})


@socketio.on('ping')
def handle_ping():
    """Responde a ping para mantener conexión"""
    emit('pong')


# ==================== INICIO DE LA APLICACIÓN ====================

if __name__ == "__main__":
    logger.info("Iniciando SmartField con soporte WebSocket...")
    
    # Configuración para desarrollo/producción
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    
    logger.info(f"Servidor ejecutándose en {host}:{port}")
    logger.info(f"Modo debug: {debug_mode}")
    
    # Iniciar servidor con SocketIO
    socketio.run(
        app,
        host=host,
        port=port,
        debug=debug_mode,
        use_reloader=False  # Evitar problemas con threading
    )
