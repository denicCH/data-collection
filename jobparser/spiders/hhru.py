import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from datetime import datetime
import re
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
        obj = {
            'name_vac' : response.css('h1::text').extract_first(),
            'salary' : self.pats_salary_hhru(response.xpath("//span[@class='bloko-header-2 bloko-header-2_lite']/text()").extract()),
            'company' : "".join(response.xpath("//div[contains(@class,'vacancy-company-name')]//span/text()").extract()),
            'text_vac' : " ".join(response.xpath("//div[contains(@data-qa,'vacancy-description')]/descendant::text()").extract()),
            'link_vac' : response.url,
            'date_pars' : datetime.today()

        }
        yield JobparserItem(**obj)

    def pats_salary_hhru(self, q: list):
        q = [re.sub('^\s|\s$|(?:\xa0)', '', s) for s in q]
        obj = {'min': None,
               'max': None,
               'unit': ''
               }
        if len(q) <= 1:
            return obj
        elif len(q) > 5:
            obj['min'] = float(q[1])
            obj['max'] = float(q[3])
            obj['unit'] = q[5]
        elif len(q) <= 5:
            obj['min'] = float(q[1]) if q[0].upper() == "от".upper() else None
            obj['max'] = float(q[1]) if q[0].upper() == "до".upper() else None
            obj['unit'] = q[3]
        return obj























