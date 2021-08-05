import os


def parent_dir(path):
    return os.path.abspath(os.path.join(path, os.pardir))


def rename_files(path, name=''):
    files = os.listdir(path)
    for index, file in enumerate(files):
        try:
            os.rename(os.path.join(path, file), os.path.join(path, name.join([str(index+1), '.jpg'])))
        except FileExistsError:
            continue


def count_files(path):
    return len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])


def main():
    path = os.path.join(FIRESENSE, 'assets', 'training', 'fire_images')
    rename_files(path)


FIRESENSE = parent_dir(os.getcwd())
if __name__ == "__main__":
    main()
