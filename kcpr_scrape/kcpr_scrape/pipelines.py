# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from models import Song, connect_db, create_tables


class SongPipeline(object):
    """Pipeline for storing scraped items into database"""

    def __init__(self):
        """Initializes database connection and sessionmaker"""

        engine = connect_db()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """ Saves songs to the database.
        Called for every item pipeline component.
         """

        session = self.Session()  # instantiates a Session, establish connection \
        song = Song(**item)       # unpack scraped item (from spider) within Delivery model

        try:
            session.add(song)
            session.commit
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
