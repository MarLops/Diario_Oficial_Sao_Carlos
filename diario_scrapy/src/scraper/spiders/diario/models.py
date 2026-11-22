from sqlalchemy import Column, Integer, String, DateTime, func

from scraper.database.base import Base



class Diario(Base):
    __tablename__ = "diario"

    _id = Column(
        String,
        primary_key=True,
    )

    date = Column(
        String,
        nullable=False,
    )

    journal = Column(
        String,
        unique=True,
        nullable=False,
    )

    pdf = Column(
        String,
        nullable=False,
    )

    pdf_url = Column(
        String,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )