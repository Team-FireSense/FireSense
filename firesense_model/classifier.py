import tensorflow as tf
from tensorflow import keras
import numpy as np
from directory_manager import *


# CONSTANTS ------------------------------------------------------------------------------------------------------------
CLASS_NAMES = ['not a fire', 'a fire']
MODEL = os.path.join(parent_dir(os.getcwd()), 'firesense_model', 'model')
MESSAGE = "This image is most likely {} with a {:.2f}% confidence."
# ----------------------------------------------------------------------------------------------------------------------


def load_model(path):
    return tf.keras.models.load_model(path)


def classify(image_path, model):
    # Process Images
    img = keras.preprocessing.image.load_img(image_path, target_size=(30, 30))
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch

    # Make predictions, judge confidence level
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    # Get human-readable classes and confidence
    label = CLASS_NAMES[np.argmax(score)]
    confidence = 100 * np.max(score)
    return label, confidence


def main():
    model = load_model(MODEL)
    while True:
        img_path = input("\nEnter file path of image to classify: ")
        classification, score = classify(img_path, model)
        msg = MESSAGE.format(classification, score)
        print(msg + f"\n---------------------------------\n")


# For testing purposes only - this module will need to be imported into firedetect.py to use it.
if __name__ == "__main__":
    main()
