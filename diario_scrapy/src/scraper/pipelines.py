from scraper.database.session import get_session

from scraper.storage.session import get_storage
from scraper.utils.items import StorageItem


class SQLAlchemyPipeline:

    def open_spider(self):
        self.session = get_session()

       

    def process_item(self, item, spider):
        try:
            if not hasattr(item, "model"):
                return item

            model = item.model

            data = dict(item)

            obj = model(
                **data
            )

            self.session.merge(obj)

            self.session.commit()

            spider.logger.info(
                "Saved item using model %s: %s",
                model.__name__,
                data,
            )

        except Exception:
            self.session.rollback()

            spider.logger.exception(
                "Database error"
            )

        return item

    def close_spider(self, spider):
        self.session.close()

        spider.logger.info(
            "Database session closed"
        )




class StoragePipeline:

    def open_spider(self):
        self.session = get_storage()

      

    def process_item(self, item, spider):

        if not isinstance(item, StorageItem):
            return item

        storage_name = item.storage_name
        self.session.set_storage(storage_name)

       
        self.session.save(
            filename=item["filename"],
            content=item["content"],
        )
       

        return item

    