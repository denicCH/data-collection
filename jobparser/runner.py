from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser import settings
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.superjobru import SuperjobruSpider
from jobparser.spiders.labirintru import LabirintruSpider
from jobparser.spiders.book24ru import Book24ruSpider

if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    #  process.crawl(HhruSpider)
    # process.crawl(SuperjobruSpider)
    # process.crawl(LabirintruSpider)
    process.crawl(Book24ruSpider)

    process.start()
