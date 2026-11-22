from scraper.storage.local import LocalStorage
import pathlib

def get_storage():

    pathlib.Path(LocalStorage.base_path).mkdir(exist_ok=True)


if __name__ == "__main__":

    get_storage()

    print(
        "Storage created"
    )