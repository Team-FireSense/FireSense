from classifier import *


# CONSTANTS ------------------------------------------------------------------------------------------------------------
FIRE_TEST = os.path.join(directory_manager.parent_dir(os.getcwd()), 'assets', 'testing', 'fire_images')
FIRE_TRAIN = os.path.join(directory_manager.parent_dir(os.getcwd()), 'assets', 'training', 'fire_images')
NON_FIRE_TEST = os.path.join(directory_manager.parent_dir(os.getcwd()), 'assets', 'testing', 'non_fire_images')
NON_FIRE_TRAIN = os.path.join(directory_manager.parent_dir(os.getcwd()), 'assets', 'training', 'non_fire_images')
# ----------------------------------------------------------------------------------------------------------------------


def test(model, path):
    if path == FIRE_TEST or path == FIRE_TRAIN:
        correct_class = 'a fire'
    else:
        correct_class = 'not a fire'
    correct_count = 0
    num_imgs = directory_manager.count_files(path)
    print(f"\nTesting Images from {path} ...")
    for i in range(1, num_imgs+1):
        img = os.path.join(path, f'{i}.jpg')
        # print(f"Testing image: {img}")
        classification, score = classify(img, model)
        # print(classification)
        if classification == correct_class:
            correct_count += 1

            # print("correct classification")
    print("Testing Complete.")
    accuracy = correct_count / num_imgs
    return accuracy


def rename_all():
    directory_manager.rename_files(FIRE_TRAIN)
    directory_manager.rename_files(FIRE_TEST)
    directory_manager.rename_files(NON_FIRE_TRAIN)
    directory_manager.rename_files(NON_FIRE_TEST)


def main():
    model = load_model(MODEL)
    rename_all()
    print("\nAll filenames are in the correct format.")
    fire_train_accuracy = round(test(model, FIRE_TRAIN)*100, 2)
    print(f"Fire Training Dataset Accuracy: {fire_train_accuracy}%")
    fire_test_accuracy = round(test(model, FIRE_TEST) * 100, 2)
    print(f"Fire Testing Dataset Accuracy: {fire_test_accuracy}%")
    non_fire_train_accuracy = round(test(model, NON_FIRE_TRAIN)*100, 2)
    print(f"Non Fire Training Dataset Accuracy: {non_fire_train_accuracy}%")
    non_fire_test_accuracy = round(test(model, NON_FIRE_TEST)*100, 2)
    print(f"Non Fire Testing Dataset Accuracy: {non_fire_test_accuracy}%")
    print("\n--------------------------")


if __name__ == "__main__":
    main()
