# Diário Scrapy

A Scrapy-based project to collect official documents from different sources.

Each document source is implemented as an independent spider module. Every spider contains its own:

- Spider implementation
- Scrapy Item definition
- SQLAlchemy database model

The project uses a generic database pipeline, where the Item defines which SQLAlchemy model should be used for persistence.

---

# Development Setup

## Requirements

Install:

- Python 3.12+
- uv

Verify installation:

```bash
python --version
uv --version
```

---

# Install Dependencies

Clone the repository:

```bash
git clone <repository>
cd diario_scrapy
```

Create the virtual environment and install dependencies:

```bash
uv sync
```

Activate the environment.

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

---

# Project Commands (uv)

The project provides reusable commands through `uv`.

List available commands:

```bash
uv run --list
```

Available commands:

```text
scraper-diario
sync-database
sync-storage
sync-environment
refresh
```

---

## Initialize Database

Create database tables:

```bash
uv run sync-database
```

This executes:

```text
src/scraper/database/init_db.py
```

Database location:

```text
data/database/
```

Example:

```text
data/database/diario.db
```

---

## Initialize Storage

Prepare document storage:

```bash
uv run sync-storage
```

This executes:

```text
src/scraper/storage/init_storage.py
```

Storage location:

```text
data/storage/
```

Example:

```text
data/storage/
└── diario/
    ├── 2026_01_01.pdf
    └── 2026_01_02.pdf
```

---

## Prepare Development Environment

Initialize database and storage:

```bash
uv run sync-environment
```

Execution flow:

```text
sync-environment
        |
        +--> Initialize Database
        |
        +--> Initialize Storage
```

---

## Run Diário Spider

Execute the Diário crawler:

```bash
uv run scraper-diario
```

Equivalent to:

```bash
scrapy crawl diario
```

Execution flow:

```text
scraper-diario
        |
        v
Scrapy Spider
        |
        +--> DiarioFileItem
        |       |
        |       +--> StoragePipeline
        |               |
        |               +--> data/storage/
        |
        +--> DiarioItem
                |
                +--> SQLAlchemyPipeline
                        |
                        +--> data/database/
```

---

## Full Refresh

Execute initialization and scraper:

```bash
uv run refresh
```

Execution flow:

```text
refresh
    |
    +--> sync-database
    |
    +--> sync-storage
    |
    +--> scraper-diario
```

---

# Development Data Storage

During development, all generated data is stored locally inside the `data` directory.

Structure:

```text
data/
│
├── database/
│   └── diario.db
│
└── storage/
    └── downloaded_documents/
```

---

# Project Structure

```text
diario_scrapy/
│
├── scrapy.cfg
├── pyproject.toml
│
├── data/
│   ├── database/
│   └── storage/
│
└── src/
    └── scraper/
        │
        ├── database/
        │   ├── base.py
        │   ├── session.py
        │   └── init_db.py
        │
        ├── storage/
        │   └── init_storage.py
        │
        └── spiders/
            │
            └── diario/
                ├── __init__.py
                ├── item.py
                ├── models.py
                └── spider.py
```

---

# Database Models

All SQLAlchemy models must inherit from the shared database `Base`.

Location:

```text
scraper/database/base.py
```

Example:

```python
from sqlalchemy import Column, String, DateTime, func

from scraper.database.base import Base


class Diario(Base):

    __tablename__ = "diario"

    _id = Column(
        String,
        primary_key=True
    )

    date = Column(
        String,
        nullable=False
    )

    journal = Column(
        String,
        nullable=False
    )

    pdf = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
```

Each spider owns its database model.

---

# Creating a New Spider

Create a new folder:

```text
scraper/spiders/<source_name>/
```

Example:

```text
scraper/spiders/diario/
```

Each spider folder contains:

```text
diario/
├── __init__.py
├── item.py
├── models.py
└── spider.py
```

---

# Creating the Model

Create the SQLAlchemy model:

```text
spiders/<source_name>/models.py
```

Example:

```python
from scraper.database.base import Base


class Document(Base):

    __tablename__ = "document"

    ...
```

The model must inherit from:

```python
Base
```

---

# Creating the Item

Create the Scrapy Item:

```text
spiders/<source_name>/item.py
```

Example:

```python
import scrapy

from scraper.spiders.diario.models import Diario


class DiarioItem(scrapy.Item):

    model = Diario

    _id = scrapy.Field()
    date = scrapy.Field()
    journal = scrapy.Field()
    pdf = scrapy.Field()
```

The pipeline uses:

```python
item.model
```

to identify the SQLAlchemy model.

---

# Creating the Spider

Create:

```text
spiders/<source_name>/spider.py
```

Example:

```python
import scrapy

from scraper.spiders.diario.item import DiarioItem


class DiarioSpider(scrapy.Spider):

    name = "diario"

    allowed_domains = [
        "cidadao.saocarlos.sp.gov.br"
    ]

    def parse(self, response):

        yield DiarioItem(
            _id="example",
            date="2026_01_01",
            journal="example",
            pdf="document.pdf"
        )
```

---

# Pipeline Flow

The pipeline is shared by all spiders.

Flow:

```text
Spider
   |
   | yield Item
   |
   v
Scrapy Item
   |
   +--> ModelItem
   |        |
   |        v
   |   SQLAlchemyPipeline
   |
   |
   +--> StorageItem
            |
            v
      StoragePipeline
```

---

# List Available Spiders

```bash
scrapy list
```

Example:

```text
diario
```

---

# Run Spider Directly

Without uv:

```bash
scrapy crawl diario
```

Using uv:

```bash
uv run scraper-diario
```

---

# Run With Logs

```bash
scrapy crawl diario -L INFO
```

---

# Export Data

```bash
scrapy crawl diario -o output.json
```

---

# Adding a New Document Source

Steps:

1. Create:

```text
scraper/spiders/new_source/
```

2. Add:

```text
new_source/
├── item.py
├── models.py
└── spider.py
```

3. Create SQLAlchemy model.

4. Create Item:

```python
model = YourModel
```

5. Create spider:

```python
class NewSourceSpider(scrapy.Spider):

    name = "new_source"
```

6. Check:

```bash
scrapy list
```

7. Run:

```bash
uv run new-source
```

---

# Design Principles

- Each document source is an independent spider module.
- Each spider owns its Item and database Model.
- Storage and database pipelines are separated.
- Database files are stored in `data/database`.
- Downloaded documents are stored in `data/storage`.
- Adding a new source does not require changing pipelines.
- Items define their destination:
  - `ModelItem` → SQLAlchemy database
  - `StorageItem` → File storage