from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from leroymerlin_parser.spiders.leroymerru import AvitoruSpider
from leroymerlin_parser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(AvitoruSpider,search='Mercedes gle coupe',city='izhevsk')

    process.start()