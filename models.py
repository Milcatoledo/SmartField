from PIL import Image
from io import BytesIO
from tensorflow.keras.models import load_model
import numpy as np

from tensorflow.keras.preprocessing import image as keras_image


def preprocess_image(image, target_size=(224, 224)):
    try:
        if isinstance(image, str):
            img = keras_image.load_img(image, target_size=target_size)
        elif isinstance(image, bytes):
            img = Image.open(BytesIO(image)).resize(target_size)
        elif hasattr(image, 'resize'):
            img = image.resize(target_size)
        else:
            raise ValueError(
                "Tipo de imagen no soportado para preprocesamiento")
        img_array = keras_image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0
        return img_array
    except Exception as e:
        raise ValueError(f"Error al procesar la imagen: {str(e)}")


def predict(model, image):
    models = "models/"
    models_names = {
        'acm': 'ACM_ponchi_73%_0.9_final.keras',
        'mobilenet': 'mobilenet_cacao__84%_0.68_final.keras',
        'resnet': 'resnet_cacao_89%_0.48_final.keras',
        'xception': 'xception_cacao_89%_0.43_final.keras'
    }

    img_array = preprocess_image(image, target_size=(224, 224))
    loaded_model = load_model(models + models_names[model])

    predictions = loaded_model.predict(img_array)
    predicted_class_index = int(np.argmax(predictions))
    labels = ['Etapa 1', 'Etapa 2', 'Etapa 3', 'Etapa 4']
    class_name = labels[predicted_class_index]
    return [class_name, predictions[0], models_names[model]]
