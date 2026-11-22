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

## Database

The SQLite database is stored in:

```text
data/database/
```

Example:

```text
data/database/diario.db
```

This database contains the tables created from SQLAlchemy models.

## Document Storage

Downloaded files are stored in:

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

The storage layer is responsible for saving the original documents downloaded by spiders.

---

# Project Structure

Each spider is isolated inside its own folder.

Example:

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

To create a new document collector, create a new folder:

```text
scraper/spiders/<source_name>/
```

Example:

```text
scraper/spiders/diario/
```

Each spider folder must contain:

```text
diario/
├── __init__.py
├── item.py
├── models.py
└── spider.py
```

---

# Creating the Model

Create the SQLAlchemy model in:

```text
spiders/<source_name>/models.py
```

The model must inherit from:

```python
Base
```

Example:

```python
from scraper.database.base import Base


class Document(Base):

    __tablename__ = "document"

    ...
```

---

# Creating the Item

Create the Scrapy Item in:

```text
spiders/<source_name>/item.py
```

The Item must define the SQLAlchemy model using the `model` attribute.

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

to determine which database model should receive the data.

---

# Creating the Spider

Create the spider in:

```text
spiders/<source_name>/spider.py
```

The spider must inherit from:

```python
scrapy.Spider
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
            _id="example_2026_01_01",
            date="2026_01_01",
            journal="example",
            pdf="https://example.com/file.pdf"
        )
```

---

# Database Pipeline Flow

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
   | item.model
   |
   v
SQLAlchemy Model
   |
   v
data/database/database.sqlite
```

Example:

```python
class DiarioItem(scrapy.Item):

    model = Diario
```

means the data is saved using the `Diario` SQLAlchemy model.

---

# Initialize Database

Create database tables:

```bash
python -m scraper.database.init_db
```

The database file will be created under:

```text
data/database/
```

---

# List Available Spiders

To list all available spiders:

```bash
scrapy list
```

Example:

```text
diario
contracts
```

---

# Run a Spider

Run:

```bash
scrapy crawl diario
```

Replace `diario` with the spider name returned by:

```bash
scrapy list
```

---

# Run With Logs

```bash
scrapy crawl diario -L INFO
```

---

# Export Data

Export scraped data:

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

3. Create the SQLAlchemy model.

4. Create the Scrapy Item:

```python
model = YourModel
```

5. Create the spider:

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
scrapy crawl new_source
```

---

# Design Principles

- Each document source is an independent spider module.
- Each spider owns its Item and database Model.
- The pipeline is shared by all spiders.
- Database files are stored in `data/database`.
- Downloaded documents are stored in `data/storage`.
- Adding a new source does not require changing the pipeline.
- The Item defines the database destination through the `model` attribute.