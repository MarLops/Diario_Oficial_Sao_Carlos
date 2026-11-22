from scraper.utils.items import (
    ModelItem,
    StorageItem,
)
import scrapy
from scraper.spiders.diario.models import Diario


class DiarioItem(ModelItem):

    model = Diario

    date = scrapy.Field()
    journal = scrapy.Field()
    pdf = scrapy.Field()
    pdf_url = scrapy.Field()

class DiarioFileItem(StorageItem):

    storage_name = "diario"