from scraper.utils.items import (
    ModelItem,
    StorageItem,
)
import scrapy
from scraper.spiders.camara_sao_carlos.models import DiarioCamaraSaoCarlosSP


class DiarioCamaraSaoCarlosItem(ModelItem):

    model = DiarioCamaraSaoCarlosSP

    date = scrapy.Field()
    journal = scrapy.Field()
    pdf = scrapy.Field()
    pdf_url = scrapy.Field()
    protocol = scrapy.Field()
    author = scrapy.Field()
    process = scrapy.Field()
    number = scrapy.Field()
    proposal = scrapy.Field()

class DiarioFileCamaraSaoCarlosItem(StorageItem):

    storage_name = "diario_camara_sao_carlos"