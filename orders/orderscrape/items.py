# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class OrderscrapeItem(Item):

    order_num = Field()
    day = Field()
    date = Field()
    payment = Field()
    restaurant = Field()
    address = Field()
    customer = Field()
    delivery_time = Field()
    pickup_time = Field()
    time_delivered = Field()
    subtotal = Field()
    tax = Field()
    delivery_charge = Field()
    tip = Field()
    total = Field()
