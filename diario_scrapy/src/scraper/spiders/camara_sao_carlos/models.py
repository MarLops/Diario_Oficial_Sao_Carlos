from sqlalchemy import Column, Integer, String, DateTime, func

from scraper.database.base import Base



class DiarioCamaraSaoCarlosSP(Base):
    __tablename__ = "diario_camara_sao_carlos_sp"

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

    protocol = Column(
        String,
        nullable=False,
    )

    author = Column(
        String,
        nullable=False,
    )

    process = Column(
        String,
        nullable=False,
    )

    number = Column(
        String,
        nullable=False,
    )

    proposal = Column(
        String,
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