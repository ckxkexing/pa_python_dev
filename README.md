# pa_python_dev
用scrapy写的用于爬取python_dev的新版[mailing list网站](https://mail.python.org/archives/list/python-dev@python.org/)内容。

分三步爬取所需要的内容，对应的是三只爬虫，位于spiders下。
## 使用环境

- scrapy
- fake_useragent
- pymongo
- beautifulsoup4

## 使用流程

- 进入pa_python_dev文件夹
- 显示三只爬虫命令: scrapy list
- 获取所需要的topic的url
  - 在spiders/python_dev_threads.py中，设定获取的时间范围
  - 在settings.py中设定好mongodb的参数，这是用于item输出的地址
  - pipelines.py中的账户密码也需要设置一下
  - 爬虫启动命令: scrapy crawl python_dev_threads
- 获取topic详细内容
  - 在python_dev_topic.py中，设定topic_url所在数据库集合位置
  - 在settings.py中设定本次输出到mongodb的参数
  - 爬虫启动命令: scrapy crawl python_dev_topic
- 获取每个topic的回复reply内容
  - 在python_dev_reply.py中，设定topic所在数据库集合位置
  - 在settings.py中设定本次输出到mongodb的参数
  - 爬虫启动命令: scrapy crawl python_dev_reply


  
