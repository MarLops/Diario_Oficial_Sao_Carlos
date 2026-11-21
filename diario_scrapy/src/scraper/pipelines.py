from scraper.database.session import get_session


class SQLAlchemyPipeline:

    def open_spider(self, spider):

        self.session = get_session()

        if not hasattr(spider, "model"):
            raise AttributeError(
                f"{spider.name} does not define a model"
            )

        self.model = spider.model

        spider.logger.info(
            "Using database model: %s",
            self.model.__name__
        )


    def process_item(self, item, spider):

        try:

            data = dict(item)

            obj = self.model(
                **data
            )

            self.session.add(obj)

            self.session.commit()

            spider.logger.info(
                "Saved item: %s",
                data
            )

        except Exception as e:

            self.session.rollback()

            spider.logger.error(
                "Database error: %s",
                e
            )

        return item


    def close_spider(self, spider):

        self.session.close()

        spider.logger.info(
            "Database session closed"
        )