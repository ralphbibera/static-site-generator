import os
import shutil


def recursive_copy(source: str, destination: str):
    if not os.path.exists(destination):
        os.makedirs(destination)
    else:
        shutil.rmtree(destination)

    for path in os.listdir(source):
        if os.path.isfile(os.path.join(source, path)):
            shutil.copy2(os.path.join(source, path), os.path.join(destination, path))
        else:
            recursive_copy(os.path.join(source, path), os.path.join(destination, path))
