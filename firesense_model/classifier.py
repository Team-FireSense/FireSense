from firesense_model/firesense_model_generator import *
import os
import tensorflow as tf
from tensorflow import keras


def load_model(path):
    return tf.keras.models.load_model(path)


def classify(image_path):
    img_array = get_image_ndarray(image_path)
    labels = ['fire', 'no fire']
    classification = labels[0]
    return classification


if __name__ == "__main__":
    model = load_model()
    img = ""
