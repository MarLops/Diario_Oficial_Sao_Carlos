from pathlib import Path

from scraper.storage.base import Storage


class LocalStorage(Storage):

    base_path = "data/storage"

    def set_storage(
        self,
        storage_name
    ):
        self.base_path = Path(self.base_path)
        self.storage_name = storage_name
        self.base_path.mkdir(
            parents=True,
            exist_ok=True
        )

        self.folder = (
            self.base_path
            / storage_name
        )

        self.folder.mkdir(
            parents=True,
            exist_ok=True
        )


    def save(
        self,
        filename,
        content
    ):

        if not isinstance(content, bytes):
            raise TypeError(
                "Storage content must be bytes"
            )

        folder = self.folder
            
        

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        file_path = (
            folder
            / filename
        )

        file_path.write_bytes(
            content
        )

        return str(file_path)

    def close(self):

        pass