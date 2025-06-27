import os
import tensorflow as tf
from tensorflow import keras
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelManager:
    """Gestor de modelos de ML para la aplicación."""
    
    def __init__(self, models_dir='models'):
        self.models_dir = models_dir
        self.models = {}
        self.load_available_models()
    
    def load_available_models(self):
        """Carga todos los modelos .keras disponibles en el directorio de modelos."""
        if not os.path.exists(self.models_dir):
            logger.warning(f"Directorio de modelos {self.models_dir} no existe")
            return
        
        for filename in os.listdir(self.models_dir):
            if filename.endswith('.keras'):
                model_name = filename.replace('.keras', '')
                model_path = os.path.join(self.models_dir, filename)
                try:
                    model = keras.models.load_model(model_path)
                    self.models[model_name] = {
                        'model': model,
                        'path': model_path,
                        'loaded': True
                    }
                    logger.info(f"Modelo {model_name} cargado exitosamente")
                except Exception as e:
                    logger.error(f"Error cargando modelo {model_name}: {str(e)}")
                    self.models[model_name] = {
                        'model': None,
                        'path': model_path,
                        'loaded': False,
                        'error': str(e)
                    }
    
    def get_model(self, model_name):
        """
        Obtiene un modelo específico.
        
        Args:
            model_name: Nombre del modelo
        
        Returns:
            tensorflow.keras.Model: El modelo cargado o None si no existe
        """
        if model_name in self.models and self.models[model_name]['loaded']:
            return self.models[model_name]['model']
        return None
    
    def list_available_models(self):
        """
        Lista todos los modelos disponibles.
        
        Returns:
            list: Lista de nombres de modelos disponibles
        """
        return [name for name, info in self.models.items() if info['loaded']]
    
    def predict(self, model_name, preprocessed_image):
        """
        Realiza una predicción usando el modelo especificado.
        
        Args:
            model_name: Nombre del modelo a usar
            preprocessed_image: Imagen preprocesada como numpy array
        
        Returns:
            numpy.ndarray: Predicción del modelo
        """
        model = self.get_model(model_name)
        if model is None:
            raise ValueError(f"Modelo {model_name} no disponible")
        
        try:
            prediction = model.predict(preprocessed_image)
            return prediction
        except Exception as e:
            logger.error(f"Error en predicción con modelo {model_name}: {str(e)}")
            raise
    
    def get_model_info(self, model_name):
        """
        Obtiene información sobre un modelo.
        
        Args:
            model_name: Nombre del modelo
        
        Returns:
            dict: Información del modelo
        """
        if model_name not in self.models:
            return None
        
        info = self.models[model_name].copy()
        if info['loaded'] and info['model']:
            model = info['model']
            info['input_shape'] = model.input_shape
            info['output_shape'] = model.output_shape
            info['num_parameters'] = model.count_params()
        
        # No incluir el objeto modelo en la respuesta
        info.pop('model', None)
        return info
    
    def reload_model(self, model_name):
        """
        Recarga un modelo específico.
        
        Args:
            model_name: Nombre del modelo a recargar
        
        Returns:
            bool: True si se recargó exitosamente
        """
        if model_name not in self.models:
            return False
        
        model_path = self.models[model_name]['path']
        try:
            model = keras.models.load_model(model_path)
            self.models[model_name] = {
                'model': model,
                'path': model_path,
                'loaded': True
            }
            logger.info(f"Modelo {model_name} recargado exitosamente")
            return True
        except Exception as e:
            logger.error(f"Error recargando modelo {model_name}: {str(e)}")
            self.models[model_name]['error'] = str(e)
            self.models[model_name]['loaded'] = False
            return False


# Instancia global del gestor de modelos
model_manager = ModelManager()
