# coding=utf-8

from mongoengine import *


class News(Document):
    news_title = StringField()
    news_url = StringField()
    news_content = StringField()
    news_time = StringField()
    news_ctg = StringField()

    news_title_fenci = StringField() #直接分词结果，未去停用词
    news_title_fenci_noSTW = StringField() #分词后去停用词
    news_content_fenci = StringField() #直接分词结果，未去停用词
    news_content_fenci_noSTW = StringField() #分词后去停用词
