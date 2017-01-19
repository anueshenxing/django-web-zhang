# coding=utf-8

from mongoengine import *


class News(Document):
    news_title = StringField()
    news_url = StringField()
    news_content = StringField()
    news_time = StringField()
    news_ctg = StringField()
