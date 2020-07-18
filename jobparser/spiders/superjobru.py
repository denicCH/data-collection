from typing import List

import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from datetime import datetime
import re

class SuperjobruSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains: List[str] = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response:HtmlResponse):
        next_page = response.css('a.f-test-button-dalshe::attr(href)').extract_first()
        vacansy_links = response.css('a.icMQ_._6AfZ9::attr(href)').extract()
        
        for link in vacansy_links:
            yield response.follow(link, callback=self.vacansy_parse)
        yield response.follow(next_page, callback=self.parse)


    def vacansy_parse(self, response:HtmlResponse):
        salary_vac = response.xpath("//div[@class='_3Qutk']//div[@class='_3MVeX']//span[contains(@class,'_3mfro _2Wp8I')]/text()")

        obj = {
            'name_vac' : response.css('h1._3mfro.rFbjy.s1nFK._2JVkc::text').extract_first(),
            'salary' : self.pats_salary_superjobru(salary_vac.extract()),
            'company' : "".join(response.xpath("//div[contains(@class,'f-test-address')]//span/text()").extract()),
            'text_vac' : " ".join(response.xpath("//span[contains(@class,'_2LeqZ')]/descendant::text()").extract()),
            'link_vac' : response.url,
            'date_pars' : datetime.today()

        }

        yield JobparserItem(**obj)

    def pats_salary_superjobru(self,q):
        q = [re.sub('^\s|\s$|(?:\xa0)', '', s) for s in q]
        obj = {'min': None,
               'max': None,
               'unit': ''
               }
        if len(q) == 1:
            return obj
        elif len(q) == 4:
            obj['min'] = float(q[0])
            obj['max'] = float(q[1])
            obj['unit'] = q[3]
        elif len(q) == 3:
            res = re.findall('[А-Яа-яё]+|\d+', q[2])
            obj['unit'] = res[1]
            obj['min'] = float(res[0]) if q[0].upper() == "от".upper() else None
            obj['max'] = float(res[0]) if q[0].upper() == "до".upper() else None
        return obj






















