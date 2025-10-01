
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
TEMP_DIR = os.path.join(BASE_DIR, "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

logger.info(f"Base directory: {BASE_DIR}")

def save_base64_image_temp(base64_string):
    """Guarda imagen base64 temporalmente para análisis"""
    try:
        if base64_string.startswith("data:image/"):
            header, encoded = base64_string.split(",", 1)
        else:
            encoded = base64_string
            
        filename = f"temp_{uuid.uuid4().hex[:8]}.jpg"
        temp_path = os.path.join(TEMP_DIR, filename)
        
        with open(temp_path, "wb") as f:
            f.write(base64.b64decode(encoded))
            
        return temp_path
    except Exception as e:
        logger.error(f"Error guardando imagen temporal: {e}")
        return None
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
    """Página de selección de fuente - redirige a home"""
    return render_template("index.html")

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
    """Recibe y procesa frames de imagen con análisis real"""
    try:
        logger.info(f"Frame recibido via WebSocket - Keys: {list(data.keys()) if isinstance(data, dict) else 'No dict'}")
        
        # Si solo viene imagen, reenviarla a TODOS los clientes para mostrar
        if 'image' in data and 'model' not in data:
            logger.info("Reenviando imagen a clientes web")
            image_size = len(data['image']) if 'image' in data else 0
            logger.info(f"Tamaño de imagen: {image_size} caracteres")
            
            socketio.emit('image_received', {
                'image': data['image'],
                'timestamp': datetime.now().isoformat()
            })
            logger.info("Imagen reenviada exitosamente")
            return
        
        # Si viene imagen y modelo, procesar análisis
        if 'image' not in data or 'model' not in data:
            logger.warning(f"Datos incompletos para análisis - Keys: {list(data.keys()) if isinstance(data, dict) else 'No dict'}")
            socketio.emit('error', {'message': 'Datos incompletos para análisis'})
            return
        
        # Usar modelo real Xception
        logger.info("Procesando análisis con modelo Xception")
        
        # Guardar imagen temporalmente
        temp_image_path = save_base64_image_temp(data['image'])
        if not temp_image_path:
            socketio.emit('error', {'message': 'Error procesando imagen'})
            return
            
        try:
            # Usar función predict del archivo models.py con modelo Xception
            category, percentages, model_used = predict('xception', temp_image_path)
            confidence = max(percentages) if percentages else 0.0
            
            logger.info(f"Resultado del modelo: {category} (confianza: {confidence})")
            
        except Exception as e:
            logger.error(f"Error en predicción: {e}")
            category = "Error en análisis"
            confidence = 0.0
            percentages = [0.0, 0.0, 0.0, 0.0]
        
        finally:
            # Limpiar archivo temporal
            if temp_image_path and os.path.exists(temp_image_path):
                try:
                    os.remove(temp_image_path)
                except Exception as e:
                    logger.warning(f"No se pudo eliminar archivo temporal: {e}")
        
        analysis_payload = {
            'category': category,
            'percentages': percentages,
            'model_name': 'Xception Cacao (89%)',
            'confidence': confidence,
            'timestamp': datetime.now().isoformat()
        }
        
        socketio.emit('analysis_result', analysis_payload)
        logger.info(f"Resultado de análisis enviado: {category} con {confidence*100:.1f}%")
        
    except Exception as e:
        logger.error(f"Error procesando frame: {e}")
        socketio.emit('error', {'message': f'Error procesando imagen: {str(e)}'})


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
