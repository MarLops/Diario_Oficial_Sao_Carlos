from scraper.utils.items import (
    ModelItem,
    StorageItem,
)
import scrapy
from scraper.spiders.diario_tce_sp.models import DiarioTCESP


class DiarioTCESPItem(ModelItem):

    model = DiarioTCESP

    date = scrapy.Field()
    journal = scrapy.Field()
    pdf = scrapy.Field()
    pdf_url = scrapy.Field()

class DiarioTCESPFileItem(StorageItem):

    storage_name = "tce_sp_diario"