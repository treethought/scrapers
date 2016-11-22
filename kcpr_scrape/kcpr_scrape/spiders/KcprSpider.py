# -*- coding: utf-8 -*-
from scrapy import Spider
import scrapy
from scrapy.loader import XPathItemLoader
from scrapy.loader.processors import MapCompose, Join
from kcpr_scrape.items import *


class KcprspiderSpider(Spider):
    name = "kcprspider"
    allowed_domains = ["kcpr.org"]
    start_urls = (
        'http://www.kcpr.org/',
    )

    now_playing_xpath = '//*[@id="spinitron-nowplaying"]'
    # now_playing_xpath = '//*[@id="main"]'

    item_fields = {
        'track_name': '//p/text()',
        'artist': '//*[@id="spinitron-nowplaying"]/p[1]/span[3]/b',
        'album': '//*[@id="spinitron-nowplaying"]/p[2]/span[4]/b',
        'time_aired': '//*[@id="spinitron-nowplaying"]/p[1]/span[1]',
    }

    def parse(self, response):
        """Iterates over recent songs and loads field xpaths into item loader"""

        selector = scrapy.Selector()

        try:

            for recent_song in response.selector.xpath(self.now_playing_xpath):
                loader = XPathItemLoader(
                    KcprSongItem(), selector=recent_song)  # load recent song xpaths \
                # to populate
                # Kcprsongitem
                loader.deault_input_processor = MapCompose(str.strip)
                loader.default_output_processor = Join()

                """iterate with .items() over item_fields{} and add xpaths to loader"""
                try:
                    for field in self.item_fields.keys():
                        loader.add_xpath(field, self.item_fields[field])
                        loader.load_item()
                    yield item
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
