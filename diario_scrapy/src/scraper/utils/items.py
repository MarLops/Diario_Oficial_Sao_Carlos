from scraper.storage.base import Storage
import scrapy
from scraper.database.base import Base

class ModelItem(scrapy.Item):
    """
    Base Item for database persistence.
    """

    model:Base  = None

    _id = scrapy.Field()


    def __init__(self, *args, **kwargs):

        if self.model is None:
            raise ValueError(
                f"{self.__class__.__name__} must define model"
            )

        super().__init__(*args, **kwargs)

        if not self.get("_id"):
            raise ValueError(
                f"{self.__class__.__name__} requires a non-null _id"
            )


class StorageItem(scrapy.Item):
    """
    Base Item for file storage.
    """

    storage_name :str  = None

    filename = scrapy.Field()
    content = scrapy.Field()


    def __init__(self, *args, **kwargs):

        if self.storage_name is None:
            raise ValueError(
                f"{self.__class__.__name__} must define storage_name"
            )

        super().__init__(*args, **kwargs)

        if not self.get("filename"):
            raise ValueError(
                f"{self.__class__.__name__} requires filename"
            )

        if self.get("content") is None:
            raise ValueError(
                f"{self.__class__.__name__} requires content"
            )