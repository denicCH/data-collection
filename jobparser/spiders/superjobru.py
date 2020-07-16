import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from datetime import datetime

class SuperjobruSpider(scrapy.Spider):
    name = 'Superjobru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response:HtmlResponse):
        next_page = response.css('a.f-test-button-dalshe::attr(href)').extract_first()

        vacansy_links = response.css('a.icMQ_._6AfZ9::attr(href)').extract()
        for link in vacansy_links:
            yield response.follow(link, callback=self.vacansy_parse)

        yield response.follow(next_page, callback=self.parse)



    def vacansy_parse(self, response:HtmlResponse):
        name_vac = response.css('h1._3mfro.rFbjy.s1nFK._2JVkc::text').extract_first()
        salary_vac = " ".join(response.xpath("//div[@class='_3Qutk']//div[@class='_3MVeX']//span[contains(@class,'_3mfro _2Wp8I')]/text()").extract())
        text_vac = " ".join(response.xpath("//span[contains(@class,'_2LeqZ')]/descendant::text()").extract())
        link_vac = response.url
        date_pars = datetime.today()


        yield JobparserItem(name=name_vac, salary=salary_vac, text_vac=text_vac, link_vac=response.url)

























