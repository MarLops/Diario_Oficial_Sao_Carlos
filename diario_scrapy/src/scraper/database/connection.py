import os

from sqlalchemy import create_engine


DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    "data/database/sqlite.db"
)


DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


engine = create_engine(
    DATABASE_URL,
    echo=False
)