from PIL import Image
from io import BytesIO
from tensorflow.keras.models import load_model
import numpy as np

from tensorflow.keras.preprocessing import image as keras_image
import io
import tensorflow as tf

def preprocess_image(image, target_size=(224, 224)):
    try:
        print(type(image))
        img = Image.open(BytesIO(image))
        img_array = keras_image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0
        return img_array
    except Exception as e:
        raise ValueError(f"Error al procesar la imagen: {str(e)}")

def predict(model, image):
    models = "models/"
    models_names ={
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

# def load_models():
#     global MODELS

#     if MODELS is None:
#         acm = load_model("models/ACM_ponchi_73%_0.9_final.keras")
#         mobilenet = load_model("models/mobilenet_cacao__84%_0.68_final.keras")
#         resnet = load_model("models/resnet_cacao_89%_0.48_final.keras")
#         xception = load_model("models/xception_cacao_89%_0.43_final.keras")
#         MODELS = {
#             "acm": acm,
#             "mobilenet": mobilenet,
#             "resnet": resnet,
#             "xception": xception,
#         }
#         print("Models loaded successfully.")
#     return MODELS

