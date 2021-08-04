from classifier import *

# CONSTANTS ------------------------------------------------------------------------------------------------------------
FIRE_TEST = os.path.join(parent_dir(os.getcwd()), 'assets', 'testing', 'fire_images')
FIRE_TRAIN = os.path.join(parent_dir(os.getcwd()), 'assets', 'training', 'fire_images')
NON_FIRE_TEST = os.path.join(parent_dir(os.getcwd()), 'assets', 'testing', 'non_fire_images')
NON_FIRE_TRAIN = os.path.join(parent_dir(os.getcwd()), 'assets', 'training', 'non_fire_images')
# ----------------------------------------------------------------------------------------------------------------------


def test(model, path):
    if path == FIRE_TEST or path == FIRE_TRAIN:
        correct_class = 'a fire'
    else:
        correct_class = 'not a fire'
    correct_count = 0
    num_imgs = count_files(path)
    for i in range(1, num_imgs+1):
        img = os.path.join(path, f'{i}.jpg')
        classification, score = classify(img, model)
        # print(classification)
        if classification == correct_class:
            correct_count += 1
            # print("correct classification")
    accuracy = correct_count / num_imgs
    return accuracy


def rename_all():
    rename_files(FIRE_TRAIN)
    rename_files(FIRE_TEST)
    rename_files(NON_FIRE_TRAIN)
    rename_files(NON_FIRE_TEST)


def main():
    model = load_model(MODEL)
    rename_all()
    print("\nAll filenames are now in the correct format\n")
    fire_train_accuracy = round(test(model, FIRE_TRAIN)*100, 2)
    fire_test_accuracy = round(test(model, FIRE_TEST) * 100, 2)
    non_fire_train_accuracy = round(test(model, NON_FIRE_TRAIN)*100, 2)
    non_fire_test_accuracy = round(test(model, NON_FIRE_TEST)*100, 2)
    print("\n--------------------------")
    print(f"Fire Training Dataset Accuracy: {fire_train_accuracy}%")
    print(f"Fire Testing Dataset Accuracy: {fire_test_accuracy}%")
    print(f"Non Fire Training Dataset Accuracy: {non_fire_train_accuracy}%")
    print(f"Non Fire Testing Dataset Accuracy: {non_fire_test_accuracy}%")


if __name__ == "__main__":
    main()
