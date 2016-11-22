# -*- coding: utf-8 -*-
from scrapy.item import Item, Field


class KcprSongItem(Item):
    """Container for scraped data."""

    track_name = Field()
    artist = Field()
    album = Field()
    time_aired = Field()

