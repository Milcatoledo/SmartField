import numpy as np
import cv2
from PIL import Image
import io
import base64


def preprocess_image_for_model(image_data, target_size=(224, 224), model_type='cacao'):
    """
    Preprocesa una imagen para el modelo de ML.
    
    Args:
        image_data: Datos de la imagen (bytes o base64)
        target_size: Tamaño objetivo para redimensionar (ancho, alto)
        model_type: Tipo de modelo ('cacao', 'generic', etc.)
    
    Returns:
        numpy.ndarray: Array de la imagen preprocesada
    """
    try:
        # Si los datos están en base64, decodificar
        if isinstance(image_data, str):
            # Eliminar el prefijo data:image/...;base64, si existe
            if image_data.startswith('data:image'):
                image_data = image_data.split(',')[1]
            image_data = base64.b64decode(image_data)
        
        # Convertir bytes a imagen PIL
        image = Image.open(io.BytesIO(image_data))
        
        # Convertir a RGB si es necesario
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Redimensionar la imagen
        image = image.resize(target_size)
        
        # Convertir a numpy array
        image_array = np.array(image, dtype=np.float32)
        
        # Normalizar según el tipo de modelo
        if model_type == 'cacao':
            # Normalización típica para modelos de clasificación de imágenes
            image_array = image_array / 255.0
        else:
            # Normalización estándar
            image_array = (image_array - 127.5) / 127.5
        
        # Añadir dimensión batch
        image_array = np.expand_dims(image_array, axis=0)
        
        return image_array
        
    except Exception as e:
        raise ValueError(f"Error al procesar la imagen: {str(e)}")


def postprocess_prediction(prediction, model_type='cacao'):
    """
    Postprocesa la predicción del modelo.
    
    Args:
        prediction: Predicción cruda del modelo
        model_type: Tipo de modelo
    
    Returns:
        dict: Resultado procesado con clase y confianza
    """
    try:
        if model_type == 'cacao':
            # Clases para cacao (ajusta según tu modelo)
            class_names = ['INMADURO', 'PINTÓN', 'PUNTO ÓPTIMO', 'SOBREMADURO']
            colors = ['text-red-600', 'text-yellow-600', 'text-green-700', 'text-purple-600']
            border_colors = ['border-red-500', 'border-yellow-500', 'border-green-600', 'border-purple-500']
        else:
            # Clases genéricas
            class_names = ['Clase 0', 'Clase 1', 'Clase 2', 'Clase 3']
            colors = ['text-blue-600', 'text-green-600', 'text-yellow-600', 'text-red-600']
            border_colors = ['border-blue-500', 'border-green-500', 'border-yellow-500', 'border-red-500']
        
        # Obtener la clase con mayor probabilidad
        predicted_class_index = np.argmax(prediction[0])
        confidence = float(prediction[0][predicted_class_index])
        
        # Asegurar que el índice esté dentro del rango
        if predicted_class_index >= len(class_names):
            predicted_class_index = 0
        
        result = {
            'class': class_names[predicted_class_index],
            'confidence': confidence,
            'color': colors[predicted_class_index],
            'border_color': border_colors[predicted_class_index],
            'all_probabilities': {
                class_names[i]: float(prediction[0][i]) 
                for i in range(min(len(class_names), len(prediction[0])))
            }
        }
        
        return result
        
    except Exception as e:
        # Resultado por defecto en caso de error
        return {
            'class': 'ERROR',
            'confidence': 0.0,
            'color': 'text-red-600',
            'border_color': 'border-red-500',
            'error': str(e)
        }


def validate_image(image_data):
    """
    Valida que los datos de imagen sean válidos.
    
    Args:
        image_data: Datos de la imagen
    
    Returns:
        bool: True si la imagen es válida
    """
    try:
        if isinstance(image_data, str):
            if image_data.startswith('data:image'):
                image_data = image_data.split(',')[1]
            image_data = base64.b64decode(image_data)
        
        image = Image.open(io.BytesIO(image_data))
        return True
    except:
        return False
