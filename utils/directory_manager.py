import os


def parent_dir(path):
    return os.path.abspath(os.path.join(path, os.pardir))


def main():
    print(parent_dir(os.getcwd()))


if __name__ == "__main__":
    main()
