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
        'xception': 'xception_cacao_89%_0.43_final.keras'
    }

    img_array = preprocess_image(image_path)
    loaded_model = load_model(models_dir + models_names[model])

    predictions = loaded_model.predict(img_array)
    predicted_class_index = int(np.argmax(predictions))
    labels = ['0 - 2 meses', '2 - 4 meses', '4 - 6 meses', '> 6 meses']
    class_name = labels[predicted_class_index]
    return [class_name, predictions[0], models_names[model]]
