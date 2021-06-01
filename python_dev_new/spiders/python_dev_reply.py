'''

专门获取比如
https://mail.python.org//archives/list/python-dev@python.org/thread/ARJLCFBZJYTDXHRMK6YP5SNAHD34HNR5/replies?sort=thread&last_view=
的回复的信息。


使用之前需要
1、start_requests中db名称和col名称
2、将setting.py中的数据库输出修改成自己想要的名字

因为本次请求返回的是text，所以用到了soup
'''


import scrapy
import json
import random
from fake_useragent import UserAgent
import pymongo
from python_dev_new.items import python_devItem
from bs4 import BeautifulSoup

class PythonDevThreadsSpider(scrapy.Spider):
    name = 'python_dev_reply'
    allowed_domains = ['mail.python.org']
    # start_urls = ['http://mail.python.org/']
    ua = UserAgent()
    cnt = 0
    def start_requests(self):
        client = pymongo.MongoClient("mongodb://admin:123456@127.0.0.1",27017)
        db = client["mailing_lists"]
        col = db["python_dev_new_topic"]
        for data in col.find():
            url = data['replyUrl']
            yield scrapy.Request(url, meta={'topic_data':data},callback=self.parse, headers = {
                    "User-Agent" :  self.ua.random,
                    'Accept-Language': 'en',
                })

    def parse(self, response):
        print('-' * 50)
        print(self.cnt)
        self.cnt += 1
        print('-' * 50)
        item = python_devItem()
        topic_data = response.meta['topic_data']
        item = topic_data
        item['replyMails'] = []
        d = json.loads(response.text)['replies_html']
        soup = BeautifulSoup(d)
        if  soup.body != None:
            for e in soup.body.contents:
                    if e == '\n':
                        continue
                    reply = {}
                    reply['mailID'] =  'https://mail.python.org' + e.find(name='div', attrs={'class':'messagelink'}).a['href']
                    reply['title'] = None
                    reply['replyAuthor'] = e.find(name='div', attrs={'class':'email-author'}).a.text
                    reply['replyAuthorEmail'] = None
                    reply['replyTime'] = e.find(name='div', attrs={'class':'email-date'}).find(name='div', attrs={'class':'time'}).span['title']
                    reply['replyContent'] = e.find(name='div', attrs={'class':'email-body'}).get_text()
                    item['replyMails'].append(reply)
        yield item
