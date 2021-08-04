import cv2
import numpy as np
import os
import sys
import tensorflow as tf
from sklearn.model_selection import train_test_split
from directory_manager import parent_dir

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 2
TEST_SIZE = 0.4


def main():
    directory = os.path.join(parent_dir(os.getcwd()), "assets", "training")
    print(directory)
    # Get image arrays and labels for all image files
    images, labels = load_data(directory)

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    filename = "model"
    model.save(filename)
    print(f"\nModel saved to {filename}.")


def get_image_ndarray(path):
    # Read in the image
    img_array = cv2.imread(path)
    # print(img_array)
    # Convert the image into RGB format
    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
    # Reshape the image with dimensions (30, 30, 3)
    img_array = cv2.resize(img_array, dsize=(IMG_WIDTH, IMG_HEIGHT), interpolation=cv2.INTER_CUBIC)
    # print(type(img_array))
    # print("shape:", img_array.shape)
    return img_array


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = []
    labels = []
    label = 1
    for fire_img in range(1, 756):
        img_name = f"{fire_img}.png"
        img_path = os.path.join(data_dir, "fire_images", img_name)
        print(f"Loading image: {img_path}")
        print(f"Image label: {label}")
        img = get_image_ndarray(img_path)
        print(f"Shape: {img.shape}")  # should be (30, 30, 3)
        images.append(img)
        labels.append(label)
    label = 0
    for non_fire_img in range(1, 245):
        img_name = f"{non_fire_img}.png"
        img_path = os.path.join(data_dir, "non_fire_images", img_name)
        print(f"Loading image: {img_path}")
        print(f"Image label: {label}")
        img = get_image_ndarray(img_path)
        print(f"Shape: {img.shape}")  # should be (30, 30, 3)
        images.append(img)
        labels.append(label)
    print(len(images))
    print(len(labels))
    print("\nLoading of data now complete.")
    print("\n----------------------------------------------------\n")
    return (images, labels)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    layers = tf.keras.layers
    model = tf.keras.models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(128, (3, 3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(512, activation='relu'),
        layers.Dropout(.2),
        layers.Dense(256, activation='relu'),
        # layers.Dense(64, activation='relu'),
        layers.Dense(NUM_CATEGORIES, activation="sigmoid")
    ])

    # Train neural network
    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )
    return model


if __name__ == "__main__":
    main()
