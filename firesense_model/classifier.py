import os
import tensorflow as tf
from tensorflow import keras
import numpy as np
from directory_manager import parent_dir


def load_model(path):
    return tf.keras.models.load_model(path)


def classify(image_path, model):
    class_names = ['not a fire', 'a fire']
    img = keras.preprocessing.image.load_img(image_path, target_size=(30, 30))
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    print(np.argmax(score))
    label = class_names[np.argmax(score)]
    confidence = 100 * np.max(score)
    return label, confidence


def main():
    fire_directory = os.path.join(parent_dir(os.getcwd()), 'assets', 'testing', 'fire_images')
    fire_directory = os.path.join(parent_dir(os.getcwd()), 'assets', 'training', 'fire_images')
    non_fire_directory = os.path.join(parent_dir(os.getcwd()), 'assets', 'testing', 'non_fire_images')
    non_fire_directory = os.path.join(parent_dir(os.getcwd()), 'assets', 'training', 'non_fire_images')

    model_path = os.path.join(parent_dir(os.getcwd()), 'firesense_model', 'model')
    model = load_model(model_path)
    img = os.path.join(non_fire_directory, 'non_fire.1.png')
    classification, score = classify(img, model)
    message = "This image is most likely {} with a {:.2f}% confidence."
    print("\n---------------------------------\n" + message.format(classification, score))


# For testing purposes only - this module will need to be imported into firedetect.py to use it.
if __name__ == "__main__":
    main()
