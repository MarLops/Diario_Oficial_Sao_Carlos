from abc import ABC, abstractmethod


class Storage(ABC):

    @abstractmethod
    def set_storage(
        self,
        storage_name
    ):
        pass

    @abstractmethod
    def save(
        self,
        filename: str,
        content: bytes
    ) -> str:
        pass


    @abstractmethod
    def close(self):
        pass