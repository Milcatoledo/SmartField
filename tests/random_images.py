import random
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt

dataset_path = '/home/adre/Descargas/Cocoa Maturity Dataset Filtered.v1i.folder roboflow'
img_size = (224, 224)
batch_size = 32


val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    os.path.join(dataset_path, "valid"),
    image_size=img_size,
    batch_size=batch_size,
    label_mode='categorical'
)
class_names = val_ds.class_names


def preprocess_single_image(img_path, img_size):
    img = image.load_img(img_path, target_size=img_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


def select_random_images(dataset, num_images=3):
    all_images = []
    for images, labels in dataset:
        for i in range(images.shape[0]):
            img_np = images[i].numpy()
            label_index = np.argmax(labels[i].numpy())
            all_images.append((img_np, label_index))

    if num_images > len(all_images):
        print(
            f"Advertencia: Se solicitaron {num_images} imágenes, pero solo hay {len(all_images)}. Se usarán todas las imágenes disponibles.")
        selected_images = all_images
    else:
        selected_images = random.sample(all_images, num_images)

    return selected_images


def predict_with_all_models(image_data, models, model_names, class_names):
    if len(image_data.shape) == 3:
        image_data = np.expand_dims(image_data, axis=0)

    print(f"\n--- Predicciones para la imagen ---")
    for model, name in zip(models, model_names):
        predictions = model.predict(image_data, verbose=0)
        predicted_class_index = np.argmax(predictions)
        predicted_class_name = class_names[predicted_class_index]
        confidence = predictions[0][predicted_class_index] * 100

        print(f"Modelo: {name}")
        print(f"  Clase predicha: {predicted_class_name}")
        print(f"  Confianza: {confidence:.2f}%")


loaded_models = {
    "ACM_ponchi": tf.keras.models.load_model('../models/ACM_ponchi_73%_0.9_final.keras'),
    "mobilenet_cacao": tf.keras.models.load_model('../models/mobilenet_cacao__84%_0.68_final.keras'),
    "xception_cacao": tf.keras.models.load_model('../models/xception_cacao_89%_0.43_final.keras'),
    "resnet_cacao": tf.keras.models.load_model('../models/resnet_cacao_89%_0.48_final.keras')
}

selected_validation_images = select_random_images(val_ds, num_images=3)

for i, (image_np, true_label_index) in enumerate(selected_validation_images):
    true_label_name = class_names[true_label_index]
    print(f"\n===================================================")
    print(f"Imagen {i+1}/3:")
    print(f"Etiqueta verdadera: {true_label_name}")
    predict_with_all_models(image_np, list(
        loaded_models.values()), list(loaded_models.keys()), class_names)
    print(f"===================================================")

    plt.imshow(image_np.astype('uint8'))
    plt.title(f"Imagen {i+1} (True: {true_label_name})")
    plt.axis('off')
    plt.show()
