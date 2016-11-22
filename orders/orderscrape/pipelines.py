# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from orderscrape.models import Order, db_connect, create_tables


class OrderScrapePipeline(object):
    def __init__(self):
        """Initialize database connection and sessionmaker"""

        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)

    def get_or_create(self, session, model, item):
        instance = session.query(model).filter_by(**item).first()
        if instance:
            print('already exists')
            return instance
        else:
            instance = model(**item)
            session.add(instance)
            session.commit()
            return instance


    def process_item(self, item, spider):
        """Saves order into the database

        This method is called for every item pipeline component.

        """
        session = self.Session()
        # Order = Order(**item)                 # unpack item data into Order database model

        # instance = session.query(Order).filter_by(title=item['title'], artist=item['artist']).first()
        # if instance:
        # instance = session.query
        try:
            self.get_or_create(session, Order, item)
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
  