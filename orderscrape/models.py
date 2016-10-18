from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

from orderscrape import settings

Base = declarative_base()

def db_connect():
    """Connects to databse URL created using settings.py.
        Returns sqlalchemy engine isntance."""

    return create_engine(URL(**settings.DATABASE))


def create_tables(engine):
    """Creates Base tables metadata."""

    return Base.metadata.create_all(bind=engine)


class Order(Base):
    """Database model for Order data"""
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    order_num = Column(Integer)
    day = Column(String)
    date = Column(String)
    payment = Column(String)
    restaurant = Column(String)
    address = Column(String)
    customer = Column(String)
    delivery_time = Column(String)
    pickup_time = Column(String)
    time_delivered = Column(String)
    subtotal = Column(Float)
    tax = Column(Float)
    delivery_charge = Column(Float)
    tip = Column(Float)
    total = Column(Float)
        