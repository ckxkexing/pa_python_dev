# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PythonDevNewItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class python_threadItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    subject = scrapy.Field()

class python_dev_topic_Item(scrapy.Item):
    mailID = scrapy.Field()
    title = scrapy.Field()
    topicContent = scrapy.Field()
    topicAuthorLogin = scrapy.Field()
    topicAuthorEmail = scrapy.Field()
    topicTime = scrapy.Field() 
    replyUrl = scrapy.Field()

class python_devItem(scrapy.Item):
    mailID = scrapy.Field()
    title = scrapy.Field()
    topicContent = scrapy.Field()
    topicAuthorLogin = scrapy.Field()
    topicAuthorEmail = scrapy.Field()
    topicTime = scrapy.Field() 
    replyUrl = scrapy.Field()
    replyMails = scrapy.Field()