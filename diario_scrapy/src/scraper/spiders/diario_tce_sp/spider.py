import scrapy
import calendar
from datetime import date, timedelta
from pathlib import Path
from scraper.spiders.diario_tce_sp.items import (
    DiarioTCESPItem,
    DiarioTCESPFileItem,
)


class DiarioTCESPSpider(scrapy.Spider):
    custom_settings = {
        "ROBOTSTXT_OBEY": False,
    }


    name = "diario_tce_sp"

    allowed_domains = [
        "doe.tce.sp.gov.br"
    ]


    start_urls = [
        "https://doe.tce.sp.gov.br"
    ]


    async def start(self):
        today = date.today()

        start_date = today - timedelta(days=30)
        end_date = today
        current_date = start_date

        while current_date <= end_date:

            for start_url in self.start_urls:
                url = (
                    f"{start_url}/json/file/"
                    f"{current_date.year}/"
                    f"{current_date.month:02d}/"
                    f"{current_date.day:02d}"
                )
                self.logger.info("Requesting: %s", url)
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_file,
                    cb_kwargs={"date_journal": current_date}
                )

            current_date = current_date + timedelta(days=1)


    def parse_file(self, 
                   response,
                   date_journal):
        publication = response.json()
        file_path = publication.get("file")
        # Skip if there is no PDF
        if file_path :
            pdf_url = f"{self.start_urls[0]}{file_path}"
            filename = Path(file_path).name

            yield scrapy.Request(
                url=pdf_url,
                callback=self.parse_pdf,
                cb_kwargs={
                    "journal": filename,
                    "date_journal": date_journal,
                    "filename": filename,
                    "pdf_url": pdf_url,
                },
            )

    def parse_pdf(
        self,
        response,
        journal,
        date_journal,
        filename,
        pdf_url
    ):

        self.logger.info(
            "Downloading PDF: %s",
            filename
        )


        # Save file
        yield DiarioTCESPFileItem(
            filename=filename,
            content=response.body
        )


        # Save database record
        yield DiarioTCESPItem(
            _id=f"{journal}",
            date=date_journal,
            journal=journal,
            pdf=f"{filename}",
            pdf_url=pdf_url
        )