from flask import Flask, render_template, request, jsonify
import os
import logging
from config import config
from utils.model_manager import model_manager
from utils.image_processor import preprocess_image_for_model, postprocess_prediction, validate_image

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app(config_name='default'):
    """Factory function para crear la aplicación Flask."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    return app

app = create_app(os.environ.get('FLASK_ENV') or 'development')

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
        models = model_manager.list_available_models()
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

@app.route("/api/model/<model_name>/info", methods=['GET'])
def model_info(model_name):
    """Endpoint para obtener información de un modelo específico."""
    try:
        info = model_manager.get_model_info(model_name)
        if info is None:
            return jsonify({
                'success': False,
                'error': 'Modelo no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'model_info': info
        })
    except Exception as e:
        logger.error(f"Error obteniendo info del modelo {model_name}: {str(e)}")
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
        model_name = request.json.get('model', app.config['DEFAULT_MODEL'])  # Modelo por defecto
        
        # Validar imagen
        if not validate_image(image_data):
            return jsonify({
                'success': False,
                'error': 'Imagen inválida'
            }), 400
        
        # Verificar si el modelo existe
        if model_name not in model_manager.list_available_models():
            # Usar el primer modelo disponible si el especificado no existe
            available_models = model_manager.list_available_models()
            if not available_models:
                return jsonify({
                    'success': False,
                    'error': 'No hay modelos disponibles. Coloque archivos .keras en la carpeta models/'
                }), 500
            model_name = available_models[0]
            logger.info(f"Usando modelo por defecto: {model_name}")
        
        # Preprocesar imagen
        try:
            processed_image = preprocess_image_for_model(
                image_data, 
                target_size=app.config['IMAGE_SIZE'],
                model_type='cacao'
            )
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Error procesando imagen: {str(e)}'
            }), 400
        
        # Realizar predicción
        try:
            prediction = model_manager.predict(model_name, processed_image)
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Error en predicción: {str(e)}'
            }), 500
        
        # Postprocesar resultado
        result = postprocess_prediction(prediction, model_type='cacao')
        
        # Añadir información adicional
        result['model_used'] = model_name
        result['success'] = True
        
        logger.info(f"Predicción exitosa: {result['class']} con confianza {result['confidence']:.2f}")
        
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
        available_models = model_manager.list_available_models()
        return jsonify({
            'success': True,
            'status': 'healthy',
            'models_loaded': len(available_models),
            'available_models': available_models
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e)
        }), 500

if __name__ == "__main__":
    # Verificar que existe el directorio de modelos
    models_dir = app.config['MODELS_DIR']
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        logger.warning(f"Directorio '{models_dir}' creado. Coloque sus archivos .keras aquí.")
    
    app.run(debug=app.config['DEBUG'])
