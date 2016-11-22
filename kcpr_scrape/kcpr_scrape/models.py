from sqlalchemy import create_engine, Column, String, DateTime, Integer
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

import settings

Base = declarative_base()

def connect_db():
    """ Connects to database using settings.py configuration.
        Returns sqlalchemy instance
    """
    return create_engine(URL(**settings.DATABSE))

def create_tables(engine):
    Base.metadata.create_all(bind=engine)


class Song(Base):
    """Song information"""
    __tablename__ = 'songs'

    id = Column('id', Integer, primary_key=True)
    title = Column('title', String)
    artist = Column('artist', String)
    album = Column('album', String)
    air_time = Column('air_time', DateTime)



    def __repr__(self):
        return "<Song( title=%S, artist=%s, album=%s, air_time=%s>" \
         % (self.title, self.artist, self.album, self.air_time)

