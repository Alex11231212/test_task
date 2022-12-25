from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
from spiders.spider import AllSmartphonesSpider, OSVersionsSpider
import pandas as pd


runner = CrawlerRunner()


@defer.inlineCallbacks
def main():
    yield runner.crawl(AllSmartphonesSpider)
    yield runner.crawl(OSVersionsSpider)
    reactor.stop()

    with open('saved_pages/os_versions.csv', 'r',
              encoding='utf-8') as file:
        df = pd.read_csv(file)
        df.value_counts().to_csv('results.csv')


if __name__ == '__main__':
    main()
    reactor.run()