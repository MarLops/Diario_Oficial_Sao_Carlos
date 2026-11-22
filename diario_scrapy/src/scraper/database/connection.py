import os

from sqlalchemy import create_engine
from pathlib import Path

DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    "data/database/sqlite.db"
)
Path('data').mkdir(exist_ok=True)
(Path('data') / 'database').mkdir(exist_ok=True)


DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


engine = create_engine(
    DATABASE_URL,
    echo=False
)