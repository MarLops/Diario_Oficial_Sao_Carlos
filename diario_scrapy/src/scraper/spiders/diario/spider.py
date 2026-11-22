import scrapy
import calendar
from datetime import date
from scraper.spiders.diario.items import (
    DiarioItem,
    DiarioFileItem,
)


class DiarioSpider(scrapy.Spider):



    name = "diario"

    allowed_domains = [
        "cidadao.saocarlos.sp.gov.br"
    ]


    start_urls = [
        "https://cidadao.saocarlos.sp.gov.br/"
        "servicos/jornal/include/publicacoes.php"
    ]

    async def start(self):

        today = date.today()

        start_date = today.replace(day=1)

        end_date = today.replace(
            day=calendar.monthrange(
                today.year,
                today.month
            )[1]
        )

        for start_url in self.start_urls:

            url = (
                f"{start_url}"
                "?calendario=true"
                "&permissao=0"
                f"&start={start_date}T00:00:00-03:00"
                f"&end={end_date}T23:59:59-03:00"
            )

            self.logger.info(
                "Requesting: %s",
                url
            )

            yield scrapy.Request(
                url=url,
                callback=self.parse
            )



    def parse(self, response):

        publications = response.json()

        self.logger.info(
            "Total publications found: %s",
            len(publications)
        )

        for publication in publications:

            journal = publication.get("title")
            date = publication.get("start")
            pdf = publication.get("description")

            if not journal or not pdf:
                continue


            pdf_url = (
                "https://cidadao.saocarlos.sp.gov.br/"
                f"servicos/jornal/{pdf}"
            )


            yield scrapy.Request(
                url=pdf_url,
                callback=self.parse_pdf,
                cb_kwargs={
                    "journal": journal,
                    "date": date,
                    "filename": pdf.replace("\\",'_').replace('/','_'),
                    "pdf_url":pdf_url
                }
            )


    def parse_pdf(
        self,
        response,
        journal,
        date,
        filename,
        pdf_url
    ):

        self.logger.info(
            "Downloading PDF: %s",
            filename
        )


        # Save file
        yield DiarioFileItem(
            filename=filename,
            content=response.body
        )


        # Save database record
        yield DiarioItem(
            _id=f"{journal}",
            date=date,
            journal=journal,
            pdf=f"{filename}",
            pdf_url=pdf_url
        )