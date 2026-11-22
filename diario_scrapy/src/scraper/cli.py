import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def run_diario():
    sync_environment()
    subprocess.run(
        [
            sys.executable,
            "-m",
            "scrapy",
            "crawl",
            "diario",
        ],
        cwd=ROOT,
        check=True,
    )


def sync_database():
    subprocess.run(
        [
            sys.executable,
            "src/scraper/database/init_db.py",
        ],
        cwd=ROOT,
        check=True,
    )


def sync_storage():
    subprocess.run(
        [
            sys.executable,
            "src/scraper/storage/init_storage.py",
        ],
        cwd=ROOT,
        check=True,
    )


def sync_environment():
    sync_database()
    sync_storage()