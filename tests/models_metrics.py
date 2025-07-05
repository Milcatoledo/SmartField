import os
import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
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

y_trues_all = []
y_preds_all = []

acm = tf.keras.models.load_model('../models/ACM_ponchi_73%_0.9_final.keras')
mobilenet = tf.keras.models.load_model(
    '../models/mobilenet_cacao__84%_0.68_final.keras')
resnet = tf.keras.models.load_model(
    '../models/resnet_cacao_89%_0.48_final.keras')
xception = tf.keras.models.load_model(
    '../models/xception_cacao_89%_0.43_final.keras')

models_list = [acm, resnet, xception, mobilenet]

names = ["ACM_ponchi", "resnet_cacao", "xception_cacao", "mobilenet_cacao"]

for model in models_list:
    y_true_model = []
    y_pred_model = []
    for images, labels in val_ds:
        y_true_model.extend(np.argmax(labels.numpy(), axis=1))
        y_pred_model.extend(np.argmax(model.predict(images), axis=1))
    y_trues_all.append(y_true_model)
    y_preds_all.append(y_pred_model)

for i, name in enumerate(names):
    print(f"Reporte de Clasificación - {name}:\n")
    report = classification_report(
        y_trues_all[i], y_preds_all[i], target_names=class_names)
    print(report)
    print("-" * 50)

fig, axs = plt.subplots(1, len(models_list), figsize=(6*len(models_list), 5))
for i, (model, name) in enumerate(zip(models_list, names)):
    cm = confusion_matrix(y_trues_all[i], y_preds_all[i])
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm, display_labels=class_names)
    if len(models_list) == 1:
        ax = axs
    else:
        ax = axs[i]
    disp.plot(ax=ax, cmap='Blues', values_format='d')
    ax.set_title(f'Matriz de confusión - {name}')

plt.tight_layout()
plt.show()
