'''
https://mail.python.org/archives/list/python-dev@python.org/2020/10/?count=200&page=2
首先获取每个月份的topic的url
'''
import scrapy
import json
import random
from fake_useragent import UserAgent
import pymongo
from python_dev_new.items import python_threadItem
class PythonDevThreadsSpider(scrapy.Spider):
    name = 'python_dev_threads'
    allowed_domains = ['mail.python.org']
    # start_urls = ['http://mail.python.org/']
    ua = UserAgent()
    cnt = 0
    def start_requests(self):
        start_y = 2019
        start_m = 6
        last_y = 2021
        last_m = 6
        for y in range(start_y, last_y+1):
            for m in range(1, 13):
                if y == start_y and m < start_m:
                    continue
                if y == last_y and m > last_m:
                    continue
                ym = '{}/{}/'.format(y, m)
                # print(ym)
                # https://mail.python.org/archives/list/python-dev@python.org/2019/7/?count=200
                url = 'https://mail.python.org/archives/list/python-dev@python.org/'+ ym +'?count=200'
                yield scrapy.Request(url,  meta={"ym": ym},callback=self.parse, headers = {
                        "User-Agent" :  self.ua.random,
                        'Accept-Language': 'en',
                    })

    def parse(self, response):
        print('-' * 50)
        print(self.cnt)
        self.cnt += 1
        print('-' * 50)
        for t in response.css('.thread'):
            subject = t.css('.thread-title a::text').extract()[-1].replace('\n', '').strip()
            name = t.css('.thread-title +::text')[-1].extract().replace('\n', '').strip()
            url = 'https://mail.python.org/' + t.css('.thread-title a::attr("href")').extract()[0]
            date = t.css('.threa-date::attr(title)').extract()[0]
            item = python_threadItem()
            item['subject'] = subject
            item['name'] = name
            item['url'] = url
            item['date'] = date
            yield item
        next_url = response.css('.paginator .page-item')[-1].css('a::attr(href)').extract()[0]
        if next_url == '#':
            return
        next_url = response.url.split('?')[0] + next_url
        yield scrapy.Request(next_url,  callback=self.parse, headers = {
                        "User-Agent" :  self.ua.random,
                        'Accept-Language': 'en',
                    })