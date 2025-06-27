"""
Script de ejemplo para crear un modelo de prueba para SmartField.

Este script crea un modelo simple de TensorFlow/Keras que puede ser usado
para probar la funcionalidad de la aplicación SmartField.

NOTA: Este es solo un modelo de prueba con datos sintéticos.
Para un modelo real, necesitarás datos reales etiquetados.
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
import os

def create_sample_model():
    """Crea un modelo de ejemplo para clasificación de madurez."""
    
    # Crear modelo simple
    model = keras.Sequential([
        keras.layers.Input(shape=(224, 224, 3)),
        
        # Bloque convolucional 1
        keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Dropout(0.25),
        
        # Bloque convolucional 2
        keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Dropout(0.25),
        
        # Bloque convolucional 3
        keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Dropout(0.25),
        
        # Capas densas
        keras.layers.GlobalAveragePooling2D(),
        keras.layers.Dense(512, activation='relu'),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(4, activation='softmax')  # 4 clases de madurez
    ])
    
    # Compilar modelo
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def create_synthetic_data(num_samples=1000):
    """Crea datos sintéticos para entrenamiento de prueba."""
    
    # Generar imágenes sintéticas (224x224x3)
    X = np.random.rand(num_samples, 224, 224, 3).astype(np.float32)
    
    # Generar etiquetas aleatorias (4 clases)
    y = keras.utils.to_categorical(
        np.random.randint(0, 4, num_samples), 
        num_classes=4
    )
    
    return X, y

def train_sample_model():
    """Entrena un modelo de ejemplo con datos sintéticos."""
    
    print("Creando modelo de ejemplo...")
    model = create_sample_model()
    
    print("Generando datos sintéticos...")
    X_train, y_train = create_synthetic_data(800)
    X_val, y_val = create_synthetic_data(200)
    
    print("Resumen del modelo:")
    model.summary()
    
    print("\nEntrenando modelo (esto es solo para demostración)...")
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=3,  # Pocas épocas para demo
        batch_size=32,
        verbose=1
    )
    
    return model, history

def save_model(model, filename='cacao_model_demo.keras'):
    """Guarda el modelo en formato .keras."""
    
    # Crear directorio models si no existe
    if not os.path.exists('models'):
        os.makedirs('models')
    
    filepath = os.path.join('models', filename)
    model.save(filepath)
    print(f"\nModelo guardado en: {filepath}")
    
    return filepath

def test_model_loading(filepath):
    """Prueba cargar el modelo guardado."""
    
    print(f"\nProbando carga del modelo desde: {filepath}")
    try:
        loaded_model = keras.models.load_model(filepath)
        print("✓ Modelo cargado exitosamente")
        
        # Probar predicción con imagen sintética
        test_image = np.random.rand(1, 224, 224, 3).astype(np.float32)
        prediction = loaded_model.predict(test_image, verbose=0)
        
        print(f"✓ Predicción de prueba: {prediction}")
        print(f"✓ Clase predicha: {np.argmax(prediction[0])}")
        
        return True
    except Exception as e:
        print(f"✗ Error cargando modelo: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== Creador de Modelo de Prueba para SmartField ===\n")
    
    # Crear y entrenar modelo
    model, history = train_sample_model()
    
    # Guardar modelo
    filepath = save_model(model)
    
    # Probar carga del modelo
    test_model_loading(filepath)
    
    print("\n=== Modelo de Prueba Creado ===")
    print("Ahora puedes:")
    print("1. Ejecutar 'python app.py' para iniciar la aplicación")
    print("2. Ir a http://localhost:5000/analysis")
    print("3. Subir una imagen para probar el análisis")
    print("\nNOTA: Este es un modelo de prueba con datos sintéticos.")
    print("Para resultados reales, entrena con datos reales etiquetados.")

"""
Para usar este script:

1. Instalar dependencias:
   pip install tensorflow numpy

2. Ejecutar script:
   python create_sample_model.py

3. El modelo se guardará en models/cacao_model_demo.keras

4. Ejecutar la aplicación:
   python app.py

5. Probar en http://localhost:5000/analysis
"""
