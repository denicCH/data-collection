# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem
import re
import json
from urllib.parse import urlencode
from copy import deepcopy
from scrapy.pipelines.images import ImagesPipeline


class InstagramSpider(scrapy.Spider):
    # атрибуты класса
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = ''
    insta_pwd = ''
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_user = ['denisch100', 'kati__mart']  # Пользователь, у которого собираем посты. Можно указать список ,
    user = {
        'photo': "",
        '_id': "",
        'subscriber': [],  # подписчики
        'subscriptions': [],  # подписок
        'full_name': "",
        'username': ''
    }


    graphql_url = 'https://www.instagram.com/graphql/query/?'
    # subscribers hash для получения данных о подписчиках
    # subscriptions на кого подписан
    query_hash = {"subscribers": "c76146de99bb02f6415203be841dd25a", "subscriptions": "d04b0a864b4b54837c0d870b0e77e076"}

    def parse(self, response: HtmlResponse):  # Первый запрос на стартовую страницу
        csrf_token = self.fetch_csrf_token(response.text)  # csrf token забираем из html
        yield scrapy.FormRequest(  # заполняем форму для авторизации
            self.inst_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username': self.insta_login, 'enc_password': self.insta_pwd},
            headers={'X-CSRFToken': csrf_token}
        )

    def wq(self, item, response, user):
        # user = deepcopy(user)
        # item = deepcopy(item)
        user['username'] = item
        yield response.follow(f'/{item}', callback=self.user_data_parse, cb_kwargs={'username': item, 'user': user})  # Переходим на желаемую страницу пользователя

    def user_parse(self, response: HtmlResponse):
        j_body = json.loads(response.text)

        if j_body['authenticated']:  # Проверяем ответ после авторизации
            for item in self.parse_user:
                # user = self.user.copy()
                print(1)
                # yield next(self.wq(item, response, user))
                yield response.follow(f'/{item}', callback=self.user_data_parse, cb_kwargs={'username': item,
                                                                                            'user': deepcopy(self.user)})  # Переходим на желаемую страницу пользователя



    def user_data_parse(self, response: HtmlResponse, username, user):
        user["photo"] = response.xpath('//meta[@property="og:image"]/@content').extract_first()
        full_name = response.xpath('//meta[@property="og:title"]/@content').extract_first()
        user['full_name'] = re.findall(r'(.+)?\s\(@', full_name)[0] if full_name else ""
        user['_id'] = self.fetch_user_id(response.text)



        variables = {'id': user['_id'],  # Формируем словарь для передачи даных в запрос
                     'first': 50}  # получаем 50 подписчиков)


        for key in self.query_hash:
            item_query_hash = self.query_hash[key]
            url_friends = f'{self.graphql_url}query_hash={item_query_hash}&{urlencode(variables)}'  # Формируем ссылку для получения данных о подписчиках
            yield response.follow(
                url_friends,
                callback=self.user_friends_parse,
                cb_kwargs={'variables': deepcopy(variables), 'username': username, 'user': user, 'query_hash': item_query_hash}
                # variables ч/з deepcopy во избежание гонок
            )


    def user_friends_parse(self, response: HtmlResponse, variables, username, user, query_hash):  # Принимаем ответ. Не забываем про параметры от cb_kwargs
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_followed_by').get('page_info') if self.query_hash['subscribers'] == query_hash  else j_data.get('data').get('user').get('edge_follow').get('page_info')


        if page_info.get('has_next_page'):  # Если есть следующая страница
            variables['after'] = page_info['end_cursor']  # Новый параметр для перехода на след. страницу  22212229670
            url_friends = f'{self.graphql_url}query_hash={query_hash}&{urlencode(variables)}'
            yield response.follow(
                url_friends,
                callback=self.user_friends_parse,
                cb_kwargs={'variables': deepcopy(variables), 'username': username, 'user': user, 'query_hash': query_hash}
            )


        friends = j_data.get('data').get('user').get('edge_followed_by').get('edges') if self.query_hash['subscribers'] == query_hash else j_data.get('data').get('user').get('edge_follow').get('edges')

        for friend in friends:  # Перебираем подписчиков, собираем данные
            user_id = friend['node']['id']
            subscriber = []  # подписчики
            subscriptions = []  # подписок
            if self.query_hash["subscribers"] == query_hash:
                user['subscriptions'] += [user_id]
                subscriber += [user["_id"]]
            else:
                user['subscriber'] += [user_id]
                subscriptions += [user["_id"]]



            item = InstaparserItem(
                subscriber=subscriber,  # подписчики
                subscriptions=subscriptions,  # подписок
                username=friend['node']['username'],
                full_name=friend['node']['full_name'],
                _id=user_id,
                photo=friend['node']['profile_pic_url']
            )
            yield item  # В пайплайн
        if not (page_info.get('has_next_page')):
            item = InstaparserItem(**user)
            #print(f'username={username}')
            yield item


    # Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    # Получаем id желаемого пользователя
    def fetch_user_id(self, text):
        matched = re.search(r'profilePage_(\d+)', text).groups()
        return matched[0] if matched else None
