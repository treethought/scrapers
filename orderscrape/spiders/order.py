# -*- coding: utf-8 -*-
import re
import scrapy
from orderscrape.items import OrderscrapeItem
from .private import *


class OrderSpider(scrapy.Spider):
    name = "orders"
    allowed_domains = ["d.mealclub.com"]
    start_urls = (
        'http://d.mealclub.com/login.php',
    )

    order_urls_xpath = './/tr[1]/th/a/@href'
    order_tables = '//body/div[2]/table'            # think this works
# '    //*[@id="content"]/table[1]/tbody/tr[2]/td'

    def parse(self, response):
        return [scrapy.FormRequest.from_response(response,
                                                 formdata={
                                                     'username': USERNAME, 'password': PASSWORD},
                                                 callback=self.parse_delivery_page)]

    def parse_delivery_page(self, response):
        """Scprapes the xpath for each field in delivery_fields
            and calls parse_order on the order page.
        """

        deliveries_xpath = '//*[@id="content"]/form'

        delivery_fields = {
            'restaurant': './/tr[6]/td/text()',
            'delivery_time': './/tr[4]/td/text()',
            'pickup_time': './/tr[5]/td/text()',
            'address': './/tr[7]/td/text()',
        }

        numpay_xpath = './/tr[3]/td/strong/text()'

        for delivery in response.xpath(deliveries_xpath):
            i = OrderscrapeItem()

            """ Number Order and payment method outsiide iterator
                because they share the same xpath and need to be split.
            """
            numpay = delivery.xpath(numpay_xpath).extract()[0].split(' - ')
            i['order_num'], i['payment'] = numpay[0], numpay[1].strip()

            """ Remaining fields have own xpath and are
                scraped for each delivery table.
            """
            for field, field_xpath in delivery_fields.items():
                raw = delivery.xpath(field_xpath).extract()[0]
                i[field] = raw .replace('\xa0', '').strip()   # remove unicode

            # yield a request for the created order_url by adding it to the
            # current url
            """Send request for each "View Order" url."""

            root_url = response.url.strip('/')
            order_url = delivery.xpath(self.order_urls_xpath).extract()[0]
            url = root_url + order_url
            request = scrapy.Request(url,
                                     callback=self.parse_order,
                                     meta={'i': i})
            request.meta['i']
            yield request
        # return i

    def parse_order(self, response):
        """Scrapes xpath for the 2 tables per order page."""

        i = response.meta['i']

        """Info Table: Scrapes Customer and splits the time_delivered
        selector into time, date, and day. Outside of iterator because of splitting.
        """
        customer_xpath = '//body/div[2]/table[1]/tr[2]/td/text()'
        time_delivered_xpath = '//body/div[2]/table[1]/tr[6]/td/text()'

        # extract time, day, and date delivered from same table row
        time_delivered_full = response.xpath(time_delivered_xpath).extract()[0]

        i['time_delivered'] = time_delivered_full[:11]  # indices refer to
        i['day'] = time_delivered_full[12:15]           # the seperation of:
        i['date'] = time_delivered_full[16:]       # "12:00:00 PM Wed 04/20/16"
        i['customer'] = response.xpath(customer_xpath).extract()[0]

        """Selects the payments table and each field's xpath extends from it.
            Assign each xpath to the field's Item key..
        """
        pay_table = response.xpath('//body/div[2]/table[2]')

        pay_fields = {    # each path extends of the pay_table's xpath
            'subtotal': './/tr[contains(., "Subtotal")]/td/text()',
            'tax': './/tr[contains(., "Tax")]/td/text()',
            'delivery_charge': './/tr[contains(., "Delivery Charge")]/td/text()',
            'tip': './/tr[contains(., "Driver Tip")]/td/text()',
            'total': './/tr[contains(., "Order Total")]/td/text()'
        }

        for field, field_xpath in pay_fields.items():
            i[field] = pay_table.xpath(field_xpath).extract()[0].strip('$')

        pay_table = response.xpath('//body/div[2]/table[2]')

        # yield i
        return i
