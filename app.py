import os
import uuid
import logging
from models import predict
import base64
import json
from flask import Flask, render_template, jsonify
from flask_sock import Sock
from datetime import datetime
import numpy as np

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'smartfield-secret-key-2024')

# Configurar WebSocket puro (no Socket.IO)
sock = Sock(app)

# Configuración de directorios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

logger.info(f"Base directory: {BASE_DIR}")

# Lista de clientes conectados
connected_clients = []

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


# ==================== WEBSOCKET PURO ====================

@sock.route('/ws')
def websocket_handler(ws):
    """Maneja conexiones WebSocket puras"""
    logger.info("Nueva conexión WebSocket")
    connected_clients.append(ws)
    
    try:
        # Enviar mensaje de bienvenida
        ws.send(json.dumps({
            'event': 'connected',
            'message': 'Conectado al servidor SmartField'
        }))
        
        while True:
            # Recibir mensaje
            message = ws.receive()
            if message is None:
                break
                
            logger.info(f"Mensaje recibido - Tamaño: {len(message)} bytes")
            
            try:
                # Parsear JSON
                data = json.loads(message)
                logger.info(f"JSON parseado - Keys: {list(data.keys())}")
                
                # Procesar según el evento
                event = data.get('event', 'unknown')
                
                if event == 'image_frame':
                    handle_image_frame(ws, data)
                elif event == 'ping':
                    ws.send(json.dumps({'event': 'pong'}))
                else:
                    logger.warning(f"Evento desconocido: {event}")
                    
            except json.JSONDecodeError as e:
                logger.error(f"Error parseando JSON: {e}")
                ws.send(json.dumps({
                    'event': 'error',
                    'message': 'JSON inválido'
                }))
            except Exception as e:
                logger.error(f"Error procesando mensaje: {e}")
                import traceback
                logger.error(traceback.format_exc())
                
    except Exception as e:
        logger.error(f"Error en WebSocket: {e}")
    finally:
        logger.info("Desconexión WebSocket")
        if ws in connected_clients:
            connected_clients.remove(ws)


def handle_image_frame(ws, data):
    """Procesa frames de imagen"""
    try:
        if 'image' not in data:
            logger.warning("Frame sin imagen")
            return
        
        image_data = data['image']
        logger.info(f"Imagen recibida - Tamaño: {len(image_data)} caracteres")
        
        # Reenviar a TODOS los clientes conectados
        broadcast_message = json.dumps({
            'event': 'image_received',
            'image': image_data,
            'timestamp': datetime.now().isoformat()
        })
        
        for client in connected_clients:
            try:
                client.send(broadcast_message)
            except Exception as e:
                logger.error(f"Error enviando a cliente: {e}")
        
        logger.info(f"Imagen reenviada a {len(connected_clients)} clientes")
        
        # Si viene con modelo, procesar análisis
        if 'model' in data:
            logger.info("Procesando análisis con modelo")
            temp_image_path = save_base64_image_temp(image_data)
            
            if temp_image_path:
                try:
                    category, percentages, model_used = predict('xception', temp_image_path)
                    confidence = float(np.max(percentages))
                    
                    result = json.dumps({
                        'event': 'analysis_result',
                        'category': category,
                        'percentages': percentages.tolist(),
                        'confidence': confidence,
                        'timestamp': datetime.now().isoformat()
                    })
                    
                    ws.send(result)
                    logger.info(f"Análisis enviado: {category}")
                    
                except Exception as e:
                    logger.error(f"Error en análisis: {e}")
                finally:
                    if os.path.exists(temp_image_path):
                        os.remove(temp_image_path)
                        
    except Exception as e:
        logger.error(f"Error procesando frame: {e}")
        import traceback
        logger.error(traceback.format_exc())


# ==================== INICIO DE LA APLICACIÓN ====================

if __name__ == "__main__":
    logger.info("Iniciando SmartField con WebSocket puro...")

    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    
    logger.info(f"Servidor ejecutándose en {host}:{port}")
    logger.info(f"Endpoint WebSocket: ws://{host}:{port}/ws")
    
    app.run(
        host=host,
        port=port,
        debug=True
    )