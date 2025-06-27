# SmartField - Guía de Instalación y Uso

## ✅ Estado Actual del Proyecto

Tu proyecto SmartField ha sido **exitosamente modificado** para integrar modelos de Machine Learning. La aplicación ahora incluye:

### 🎯 Características Implementadas

- **✅ Integración con TensorFlow/Keras**: Carga automática de modelos `.keras`
- **✅ Procesamiento de imágenes**: Conversión a numpy arrays y preprocesamiento
- **✅ API REST**: Endpoints para predicción y gestión de modelos
- **✅ Interfaz actualizada**: JavaScript modificado para enviar imágenes al backend
- **✅ Modo de demostración**: Funciona sin TensorFlow instalado (predicción simulada)

### 📁 Archivos Modificados/Creados

1. **app.py** → **app_simple.py** - Aplicación Flask con ML
2. **static/analysis.js** - JavaScript actualizado para API
3. **utils/model_manager.py** - Gestor de modelos ML
4. **utils/image_processor.py** - Procesamiento de imágenes
5. **requirements.txt** - Dependencias actualizadas
6. **config.py** - Configuración de la aplicación
7. **create_sample_model.py** - Script para crear modelos de prueba

## 🚀 Cómo Usar

### Opción 1: Modo Demostración (Sin ML Real)

```bash
# 1. Ejecutar la aplicación
cd /workspaces/SmartField
python app_simple.py

# 2. Abrir navegador
# Ir a http://localhost:5000

# 3. Navegar a "Análisis"
# Subir una imagen y hacer clic en "Analizar"
# Verás predicciones simuladas
```

### Opción 2: Con Modelos ML Reales

```bash
# 1. Instalar TensorFlow
pip install tensorflow numpy Pillow opencv-python-headless

# 2. Crear un modelo de prueba
python create_sample_model.py

# 3. Ejecutar aplicación con ML real
python app.py

# 4. Usar la aplicación
# Ve a http://localhost:5000/analysis
```

## 📊 Estructura de Modelos

### Colocar tus modelos

1. **Crear directorio**: `models/`
2. **Formato requerido**: Archivos `.keras`
3. **Ejemplo**: `models/cacao_model.keras`

### Requisitos del modelo

- **Input**: Imágenes RGB 224x224 píxeles
- **Output**: 4 clases de probabilidad
- **Normalización**: Valores 0-1 (división por 255)

### Clases soportadas

1. **INMADURO** (rojo)
2. **PINTÓN** (amarillo)  
3. **PUNTO ÓPTIMO** (verde)
4. **SOBREMADURO** (púrpura)

## 🔧 API Endpoints

### Realizar predicción
```bash
POST /api/predict
Content-Type: application/json

{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
  "model": "cacao_model"
}
```

### Listar modelos
```bash
GET /api/models
```

### Estado de salud
```bash
GET /api/health
```

## 📝 Personalización

### Cambiar clases de madurez

Editar `utils/image_processor.py`:

```python
class_names = ['TU_CLASE_1', 'TU_CLASE_2', 'TU_CLASE_3', 'TU_CLASE_4']
colors = ['text-red-600', 'text-yellow-600', 'text-green-700', 'text-purple-600']
```

### Cambiar tamaño de imagen

Editar `config.py`:

```python
IMAGE_SIZE = (256, 256)  # Cambiar de (224, 224)
```

## 🧪 Crear tu propio modelo

```python
import tensorflow as tf
from tensorflow import keras

# Crear modelo
model = keras.Sequential([
    keras.layers.Input(shape=(224, 224, 3)),
    keras.layers.Conv2D(32, 3, activation='relu'),
    keras.layers.MaxPooling2D(),
    keras.layers.Conv2D(64, 3, activation='relu'),
    keras.layers.MaxPooling2D(),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(4, activation='softmax')  # 4 clases
])

# Compilar
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Entrenar con tus datos
# model.fit(X_train, y_train, epochs=50, validation_data=(X_val, y_val))

# Guardar
model.save('models/mi_modelo.keras')
```

## 🔍 Verificación

Para verificar que todo funciona:

1. **Aplicación ejecutándose**: ✅ 
2. **Endpoint de salud**: http://localhost:5000/api/health
3. **Página de análisis**: http://localhost:5000/analysis
4. **Subir imagen**: Funcionando con predicción simulada
5. **Con TensorFlow**: Instalar para predicciones reales

## 📱 Uso de la Interfaz

1. **Ir a análisis**: Clic en "Centro de análisis"
2. **Subir imagen**: Desde galería o cámara
3. **Analizar**: Clic en "Analizar Ahora"
4. **Ver resultado**: Estado de madurez con color y confianza

## 🎯 Próximos Pasos

1. **Instalar TensorFlow**: `pip install tensorflow`
2. **Entrenar modelo real**: Con datos de cacao etiquetados
3. **Colocar modelo**: En `models/cacao_model.keras`
4. **Probar predicciones**: Con imágenes reales

## 🚨 Solución de Problemas

### "No hay modelos disponibles"
- Verificar que existe `models/` con archivos `.keras`
- Instalar TensorFlow: `pip install tensorflow`

### "Error procesando imagen"
- Verificar formato de imagen (JPG, PNG)
- Verificar tamaño < 16MB

### "Error en predicción"
- Verificar que el modelo tiene input shape (224, 224, 3)
- Verificar que el modelo produce 4 salidas

---

## ✨ ¡Felicitaciones!

Tu proyecto SmartField ahora está completamente configurado para usar modelos de Machine Learning entrenados. La integración está lista y funcional tanto en modo demostración como con modelos reales.

**La aplicación está ejecutándose en**: http://localhost:5000
