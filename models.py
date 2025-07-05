from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np


def preprocess_image(img_path, img_size=(224, 224)):
    img = image.load_img(img_path, target_size=img_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


def predict(model, image_path):
    models_dir = "models/"
    models_names = {
        'acm': 'ACM_ponchi_73%_0.9_final.keras',
        'mobilenet': 'mobilenet_cacao__84%_0.68_final.keras',
        'resnet': 'resnet_cacao_89%_0.48_final.keras',
        'xception': 'xception_cacao_89%_0.43_final.keras'
    }

    img_array = preprocess_image(image_path)
    loaded_model = load_model(models_dir + models_names[model])

    predictions = loaded_model.predict(img_array)
    predicted_class_index = int(np.argmax(predictions))
    labels = ['Etapa 1', 'Etapa 2', 'Etapa 3', 'Etapa 4']
    class_name = labels[predicted_class_index]
    return [class_name, predictions[0], models_names[model]]
