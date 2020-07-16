import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from datetime import datetime

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://izhevsk.hh.ru/search/vacancy?area=&st=searchVacancy&fromSearch=true&text=python']

    def parse(self, response:HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()

        vacansy_links = response.css('a.bloko-link.HH-LinkModifier::attr(href)').extract()
        for link in vacansy_links:
            yield response.follow(link, callback=self.vacansy_parse)

        yield response.follow(next_page, callback=self.parse)



    def vacansy_parse(self, response:HtmlResponse):
        name_vac = response.css('h1::text').extract_first()
        salary_vac = response.xpath("//span[@class='bloko-header-2 bloko-header-2_lite']/text()").extract()

        text_vac = " ".join(response.xpath("//div[contains(@data-qa,'vacancy-description')]/descendant::text()").extract())
        link_vac = response.url
        date_pars = datetime.today()

        yield JobparserItem(name=name_vac, salary=salary_vac, text_vac=text_vac, link_vac=link_vac, date_pars=date_pars)

























