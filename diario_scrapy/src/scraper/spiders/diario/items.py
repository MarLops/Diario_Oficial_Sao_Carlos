import scrapy



class DiarioItem(scrapy.Item):
    date = scrapy.Field()
    journal = scrapy.Field()
    pdf = scrapy.Field()