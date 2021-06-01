'''

通过topic 的url获取所有的topic具体信息。
本来想直接获得回复reply的内容，但网页是ajax异步请求的，
于是还需要再单独获取reply，
这样做有一个好处在于有的reply时，方便获取。


'''

import scrapy
import json
import random
from fake_useragent import UserAgent
import pymongo
from python_dev_new.items import python_dev_topic_Item
class PythonDevThreadsSpider(scrapy.Spider):
    name = 'python_dev_topic'
    allowed_domains = ['mail.python.org']
    # start_urls = ['http://mail.python.org/']
    ua = UserAgent()
    cnt = 0
    def start_requests(self):
        client = pymongo.MongoClient("mongodb://admin:123456@127.0.0.1",27017)
        db = client["mailing_lists"]
        col = db["python_dev_new_thread"]
        for data in col.find():
            url = data['url']
            yield scrapy.Request(url, callback=self.parse, headers = {
                    "User-Agent" :  self.ua.random,
                    'Accept-Language': 'en',
                })

    def parse(self, response):
        print('-' * 50)
        print(self.cnt)
        self.cnt += 1
        print('-' * 50)
        mailID = 'https://mail.python.org' + response.css('.email-first .email-info .messagelink a::attr(href)').extract()[0]
        title = response.css('.thread-header h3::text').extract()[0]
        topicAuthorLogin = response.css('.email-first .email-author a::text').extract()[0]
        date = response.css('.email-first .email-date .time span::attr(title)').extract()[0]
        topicContent =  response.css('.email-first .email-body').extract()[0]
        item = python_dev_topic_Item()

        item['mailID'] = mailID
        item['title'] = title
        item['topicAuthorLogin'] = topicAuthorLogin
        item['topicContent'] = topicContent
        item['topicAuthorEmail'] = None
        item['topicTime'] = date
        item['replyUrl'] = response.url.split('?')[0] + 'replies?sort=thread&last_view='
        yield item