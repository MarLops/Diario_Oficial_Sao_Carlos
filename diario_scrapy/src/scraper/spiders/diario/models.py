from sqlalchemy import Column, Integer, String

from scraper.database.base import Base


class Diario(Base):

    __tablename__ = "diario"

    id = Column(
        Integer,
        primary_key=True
    )

    date = Column(
        String,
        nullable=False
    )

    journal = Column(
        String,
        unique=True,
        nullable=False
    )

    pdf = Column(
        String,
        nullable=False
    )