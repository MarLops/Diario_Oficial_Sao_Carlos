import scrapy
import re
import os
from urllib.parse import urlparse, parse_qs
from datetime import date, datetime
from scraper.spiders.camara_sao_carlos.items import (
    DiarioCamaraSaoCarlosItem,
    DiarioFileCamaraSaoCarlosItem,
)

class DiarioCamaraSaoCarlosSpider(scrapy.Spider):
    custom_settings = {
        "ROBOTSTXT_OBEY": False,
    }
    name = "diario_camara_sao_carlos"

    total_page = 1

    allowed_domains = [
        "camarasaocarlos.sp.gov.br",
        "alfa-file.gtp.net.br"
    ]


    start_urls = [
        "https://camarasaocarlos.sp.gov.br"
    ]

    async def start(self):

        today = date.today()

        year = today.year
        page = 1
       

        for start_url in self.start_urls:
            page = 1
          
            while page <= self.total_page:
                url = (
                    f"{start_url}/"
                    "tramitacao/"
                    f"?ano={year}&numero="
                    "&protocolo=&processo=&autor=&ementa="
                    "&id_tipo=&ordem=D&ordem_tipo=D&"
                    f"pagina={page}&grupo=&exibir_busca=1"
                )

                    
                self.logger.info(
                    "Requesting: %s",
                    url
                )
                yield scrapy.Request(
                    url=url,
                    callback=self.parse
                )
                page += 1



    def parse(self, response):

        rows = response.css("div.table-responsive table tbody tr")
        for row in rows:
            href = row.css("td.text-right a::attr(href)").get()
            yield scrapy.Request(
                url=f'{self.start_urls[0]}{href}',
                callback=self.parse_page_protocol,
            )


    def parse_page_protocol(
        self,
        response,
    ):
        item = dict()
        url = response.url
        item['journal'] = url
        protocol_id = parse_qs(
            urlparse(response.url).query
        ).get("id", [None])[0]

        item['_id'] = protocol_id

        title = response.css("h2.mb-20::text").get(default="").strip()

        m = re.search(r"N[ºo]?\s*(\d+/\d+)", title)
        if m:
            item["number"] = m.group(1)  # 695/2026

        # Container with the information
        info = response.css("div.col-xs-12.mb-40")

        item["process"] = (
            info.xpath('.//p[strong[contains(.,"Processo")]]/text()')
            .get(default="")
            .replace("Nº", "")
            .strip()
        )

        item["protocol"] = (
            info.xpath('.//p[strong[contains(.,"Protocolo")]]/text()')
            .get(default="")
            .replace("Nº", "")
            .strip()
        )

        item["author"] = (
            info.xpath('.//p[strong[contains(.,"Autor")]]/text()')
            .get(default="")
            .strip()
        )

        item["date"] = datetime.strptime(
            info.xpath('.//p[strong[contains(.,"Data")]]/text()').get(default="").strip(),
            "%d/%m/%Y"
        ).date()

        item["proposal"] = (
            info.xpath('.//p[strong[contains(.,"Ementa")]]/text()')
            .get(default="")
            .strip()
        )

        # PDF URL
        item["pdf_url"] = info.css(
            'button[title*="PDF"]::attr(data-file)'
        ).get()

       
        yield scrapy.Request(
            url=item["pdf_url"],
            callback=self.parse_pdf,
            cb_kwargs={
                "item":item
            }
        )

    def parse_pdf(
            self,
            response,
            item
        ):
            url = response.url
            filename = os.path.basename(urlparse(url).path)
            # Save file
            yield DiarioFileCamaraSaoCarlosItem(
                filename=filename,
                content=response.body
            )
    
    
            # Save database record
            yield DiarioCamaraSaoCarlosItem(
                _id=item["_id"],
                date=item["date"],
                journal=item["journal"],
                pdf=filename,
                pdf_url=item["pdf_url"],
                protocol=item["protocol"],
                author=item["author"],
                process=item["process"],
                number=item["number"],
                proposal=item["proposal"]
            )


       