"""
Configuración para la aplicación SmartField.
"""

import os

class Config:
    """Configuración base para la aplicación."""
    
    # Configuración de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Configuración de modelos
    MODELS_DIR = os.environ.get('MODELS_DIR') or 'models'
    DEFAULT_MODEL = os.environ.get('DEFAULT_MODEL') or 'cacao_model'
    
    # Configuración de imágenes
    IMAGE_SIZE = (224, 224)  # Tamaño de imagen para modelos
    SUPPORTED_FORMATS = ['jpg', 'jpeg', 'png', 'bmp', 'gif']
    
    # Configuración de clases de madurez
    MATURITY_CLASSES = {
        'cacao': [
            {
                'name': 'Etapa 1',
                'color': 'text-red-600',
                'border_color': 'border-red-500',
                'description': 'Fruto no listo para cosecha'
            },
            {
                'name': 'Etapa 2',
                'color': 'text-yellow-600',
                'border_color': 'border-yellow-500',
                'description': 'Fruto en proceso de maduración'
            },
            {
                'name': 'Etapa 3',
                'color': 'text-green-700',
                'border_color': 'border-green-600',
                'description': 'Fruto listo para cosecha'
            },
            {
                'name': 'Etapa 4',
                'color': 'text-purple-600',
                'border_color': 'border-purple-500',
                'description': 'Fruto pasado de punto óptimo'
            }
        ]
    }
    
    # Configuración de logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FILE = os.environ.get('LOG_FILE') or 'smartfield.log'
    
    # Configuración de desarrollo
    DEBUG = os.environ.get('FLASK_DEBUG') or True
    
class ProductionConfig(Config):
    """Configuración para producción."""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY must be set in production")

class DevelopmentConfig(Config):
    """Configuración para desarrollo."""
    DEBUG = True

class TestingConfig(Config):
    """Configuración para testing."""
    TESTING = True
    DEBUG = True

# Configuración por defecto
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
