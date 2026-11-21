from pathlib import Path


class LocalStorage:


    def __init__(
        self,
        base_path="data/storage"
    ):

        self.base_path = Path(base_path)

        # Make sure storage folder exists
        self.base_path.mkdir(
            parents=True,
            exist_ok=True
        )


    def save(
        self,
        source,
        filename,
        content
    ):

        folder = (
            self.base_path
            / source
            / "pdf"
        )


        # Create:
        # data/storage/diario/pdf/
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