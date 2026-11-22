from scraper.storage.base import Storage
from scraper.storage.local import LocalStorage





def get_storage() -> Storage:

    session = LocalStorage()

    try:
        return session

    finally:
        session.close()