# SmartField - Análisis de Madurez con ML

Una aplicación Flask que utiliza modelos de Machine Learning entrenados para analizar el estado de madurez de frutas (especialmente cacao) a través de imágenes.

## Características

- 🤖 **Integración con modelos TensorFlow/Keras**: Carga automática de modelos `.keras`
- 📸 **Captura de imágenes**: Desde cámara web o subida de archivos
- 🔍 **Análisis inteligente**: Predicción en tiempo real del estado de madurez
- 📊 **Interfaz intuitiva**: UI moderna y responsive
- 🛠️ **API REST**: Endpoints para integración con otros sistemas

## Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone <url-del-repositorio>
   cd SmartField
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Colocar modelos entrenados**:
   - Crear la carpeta `models/` si no existe
   - Colocar archivos `.keras` en la carpeta `models/`
   - Ejemplo: `models/cacao_model.keras`

4. **Ejecutar la aplicación**:
   ```bash
   python app.py
   ```

5. **Abrir en navegador**:
   - Ir a `http://localhost:5000`

## Estructura del Proyecto

```
SmartField/
├── app.py                 # Aplicación Flask principal
├── requirements.txt       # Dependencias Python
├── models/               # Modelos ML (.keras)
│   ├── cacao_model.keras
│   └── otros_modelos.keras
├── utils/                # Utilidades
│   ├── model_manager.py  # Gestor de modelos
│   ├── image_processor.py # Procesamiento de imágenes
│   └── __init__.py
├── static/               # Archivos estáticos
│   ├── analysis.js       # JavaScript para análisis
│   ├── index.css        # Estilos CSS
│   └── assets/          # Imágenes y recursos
├── templates/            # Templates HTML
│   ├── base.html
│   ├── index.html
│   └── analysis.html
└── README.md
```

## Uso

### Interfaz Web

1. **Página Principal**: Navegar a la página de análisis
2. **Subir Imagen**: Seleccionar desde galería o usar cámara
3. **Analizar**: Hacer clic en "Analizar Ahora"
4. **Resultado**: Ver el estado de madurez predicho

### API REST

#### Listar modelos disponibles
```bash
GET /api/models
```

#### Realizar predicción
```bash
POST /api/predict
Content-Type: application/json

{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEA...",
  "model": "cacao_model"
}
```

#### Estado de la aplicación
```bash
GET /api/health
```

## Configuración de Modelos

### Requisitos del Modelo

- **Formato**: `.keras` (TensorFlow/Keras)
- **Input**: Imágenes RGB de 224x224 píxeles
- **Output**: Probabilidades para clases de madurez
- **Normalización**: Valores entre 0-1 (dividir por 255)

### Clases de Madurez Soportadas

Por defecto, el sistema reconoce estas clases para cacao:
- `INMADURO` (rojo)
- `PINTÓN` (amarillo)
- `PUNTO ÓPTIMO` (verde)
- `SOBREMADURO` (púrpura)

### Personalización

Para personalizar las clases, editar el archivo `utils/image_processor.py`:

```python
# En la función postprocess_prediction
class_names = ['TU_CLASE_1', 'TU_CLASE_2', 'TU_CLASE_3', 'TU_CLASE_4']
colors = ['text-red-600', 'text-yellow-600', 'text-green-700', 'text-purple-600']
```

## Ejemplo de Entrenamiento de Modelo

```python
import tensorflow as tf
from tensorflow import keras

# Crear modelo simple
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

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Entrenar modelo con tus datos
# model.fit(x_train, y_train, epochs=10, validation_data=(x_val, y_val))

# Guardar modelo
model.save('models/mi_modelo.keras')
```

## Troubleshooting

### Error: "No hay modelos disponibles"
- Verificar que existan archivos `.keras` en la carpeta `models/`
- Verificar que los modelos sean compatibles con TensorFlow

### Error: "Error procesando imagen"
- Verificar que la imagen sea válida (JPG, PNG)
- Verificar que el tamaño del archivo sea menor a 16MB

### Error: "Error en predicción"
- Verificar que el modelo tenga el input shape correcto (224, 224, 3)
- Verificar que el modelo produzca output de 4 clases

## Tecnologías Utilizadas

- **Backend**: Flask, TensorFlow, NumPy, OpenCV, Pillow
- **Frontend**: HTML5, CSS3 (Tailwind), JavaScript (ES6+)
- **ML**: TensorFlow/Keras
- **Procesamiento**: NumPy, OpenCV, PIL

## Contribución

1. Fork el proyecto
2. Crear rama de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## Contacto

Para soporte o preguntas, crear un issue en el repositorio.
