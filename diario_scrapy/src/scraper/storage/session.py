import os

from scraper.storage.base import Storage
from scraper.storage.local import LocalStorage



def get_storage() -> Storage:
    storage_type = os.getenv("STORAGE_TYPE", "local").lower()

    if storage_type == "local":
        storage = LocalStorage()
    else:
        raise ValueError(f"Unknown storage type: {storage_type}")

    return storage