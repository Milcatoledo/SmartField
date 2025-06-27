from flask import Flask, render_template, request, jsonify
import os
import logging
import time

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analysis")
def analysis():
    return render_template("analysis.html")

@app.route("/api/models", methods=['GET'])
def list_models():
    """Endpoint para listar modelos disponibles."""
    try:
        # Buscar archivos .keras en la carpeta models
        models_dir = 'models'
        models = []
        
        if os.path.exists(models_dir):
            for filename in os.listdir(models_dir):
                if filename.endswith('.keras'):
                    models.append(filename.replace('.keras', ''))
        
        return jsonify({
            'success': True,
            'models': models,
            'count': len(models)
        })
    except Exception as e:
        logger.error(f"Error listando modelos: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route("/api/predict", methods=['POST'])
def predict():
    """Endpoint principal para realizar predicciones."""
    try:
        # Verificar que se envió una imagen
        if 'image' not in request.json:
            return jsonify({
                'success': False,
                'error': 'No se proporcionó imagen'
            }), 400
        
        image_data = request.json['image']
        model_name = request.json.get('model', 'cacao_model')
        
        # Verificar que hay archivos de modelo
        models_dir = 'models'
        available_models = []
        
        if os.path.exists(models_dir):
            for filename in os.listdir(models_dir):
                if filename.endswith('.keras'):
                    available_models.append(filename.replace('.keras', ''))
        
        if not available_models:
            return jsonify({
                'success': False,
                'error': 'No hay modelos disponibles. Coloque archivos .keras en la carpeta models/ e instale TensorFlow (pip install tensorflow)'
            }), 500
        
        # Simular procesamiento (reemplazar con lógica real cuando TensorFlow esté disponible)
        logger.info(f"Simulando predicción con modelo: {model_name}")
        time.sleep(1)  # Simular tiempo de procesamiento
        
        # Resultado simulado (reemplazar con predicción real)
        import random
        results = [
            {'class': 'INMADURO', 'color': 'text-red-600', 'border_color': 'border-red-500', 'confidence': 0.85},
            {'class': 'PINTÓN', 'color': 'text-yellow-600', 'border_color': 'border-yellow-500', 'confidence': 0.78},
            {'class': 'PUNTO ÓPTIMO', 'color': 'text-green-700', 'border_color': 'border-green-600', 'confidence': 0.92},
            {'class': 'SOBREMADURO', 'color': 'text-purple-600', 'border_color': 'border-purple-500', 'confidence': 0.73}
        ]
        
        result = random.choice(results)
        result['model_used'] = model_name
        result['success'] = True
        result['note'] = 'Predicción simulada - Instale TensorFlow para usar modelos reales'
        
        logger.info(f"Predicción simulada: {result['class']} con confianza {result['confidence']:.2f}")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error en predicción: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}'
        }), 500

@app.route("/api/health", methods=['GET'])
def health_check():
    """Endpoint para verificar el estado de la aplicación y modelos."""
    try:
        models_dir = 'models'
        available_models = []
        
        if os.path.exists(models_dir):
            for filename in os.listdir(models_dir):
                if filename.endswith('.keras'):
                    available_models.append(filename.replace('.keras', ''))
        
        # Verificar si TensorFlow está instalado
        try:
            import tensorflow as tf
            tf_status = f"TensorFlow {tf.__version__} disponible"
            ml_ready = True
        except ImportError:
            tf_status = "TensorFlow no instalado - usando predicción simulada"
            ml_ready = False
        
        return jsonify({
            'success': True,
            'status': 'healthy',
            'models_loaded': len(available_models),
            'available_models': available_models,
            'tensorflow_status': tf_status,
            'ml_ready': ml_ready
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e)
        }), 500

if __name__ == "__main__":
    # Verificar que existe el directorio de modelos
    if not os.path.exists('models'):
        os.makedirs('models')
        logger.warning("Directorio 'models' creado. Coloque sus archivos .keras aquí.")
    
    print("=== SmartField - Aplicación de Análisis de Madurez ===")
    print("La aplicación está lista. Ve a http://localhost:5000")
    print("Para usar modelos ML reales, instala: pip install tensorflow")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
