import os

import scrapy

from ozon_scraper.selenium_worker import all_smartphones_pages_saver, each_smartphone_pages_saver

# API_KEY = '48b35978-2475-45f9-8bc2-8912b28418cb'
#
#
# def get_scrapeops_url(url):
#     payload = {'api_key': API_KEY, 'url': url}
#     proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
#     return proxy_url


class AllSmartphonesSpider(scrapy.Spider):
    name = 'all_smartphones'
    path = 'saved_pages'
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    custom_settings = {
        'FEEDS': {
            "saved_pages/all_phones_links.csv": {
                "format": "csv",
                "overwrite": True
            }
        }
    }

    def start_requests(self):
        all_smartphones_pages_saver()
        for file in os.listdir(self.path):
            if file[0:4] == 'page':
                url = 'file://' + os.path.join(self.base_dir, self.path, file)
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for item in response.xpath(
                '//a[starts-with(@href, "/product/smartfon-") and starts-with(./span/span/text(), "Смартфон")]'):
            yield {'link': item.css('a::attr(href)').get()}


class OSVersionsSpider(scrapy.Spider):
    name = 'smartphones_info'
    path = 'saved_pages/saved_phones/'
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    custom_settings = {
        'FEEDS': {
            "saved_pages/os_versions.csv": {
                "format": "csv",
                "overwrite": True
            }
        }
    }

    def start_requests(self):
        each_smartphone_pages_saver()
        for file in os.listdir(self.path):
            url = 'file://' + os.path.join(self.base_dir, self.path, file)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        ios_version = response.xpath('//*[starts-with(text(), "iOS ")]/text()').get()
        android_version = response.xpath('//*[starts-with(text(), "Android ")]/text()').get()
        if ios_version or android_version:
            if ios_version is None:
                yield {'os_version': android_version[0:10]}
            else:
                yield {'os_version': ios_version}
