from scraper.database.base import Base
from scraper.database.connection import engine


# Import every spider model here
from scraper.spiders.diario.models import Diario
from scraper.spiders.diario_tce_sp.models import DiarioTCESP


def create_database():

    Base.metadata.create_all(
        engine
    )


if __name__ == "__main__":

    create_database()

    print(
        "Database created"
    )