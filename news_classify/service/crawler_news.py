# coding=utf8

import pycurl
import StringIO
from collections import defaultdict
from lxml import etree
from lxml.html import document_fromstring
import time
from news_classify.model.news import News
from mongoengine import *


def fetch(link):
    buf = StringIO.StringIO()
    c = pycurl.Curl()
    # print link
    c.setopt(pycurl.URL, link)
    c.setopt(pycurl.WRITEFUNCTION, buf.write)
    c.perform()
    return buf


def tohtml(htmlelement):
    return etree.tostring(htmlelement, encoding='utf-8')


def tostring(htmlelement):
    return htmlelement.text_content().encode('utf-8')


def crawler(news_site, news_start_end_time, page_numbers, news_ctg):
    connect('django_mongodb_news')
    news_data = defaultdict()
    news_list = []
    base_url = news_site
    star_end_time = news_start_end_time
    page_num = page_numbers
    tags = news_ctg.split(',')
    for ctg in tags:
        ctg_url = base_url + '/' +'articles_news_' + ctg + '/'
        for count in range(1, page_numbers + 1):
            page_count_url = ctg_url + 'p' + str(count) + '/'
            news_list_buf = fetch(page_count_url)
            news_list_doc = document_fromstring(news_list_buf.getvalue().decode("utf-8"))
            news_urls = news_list_doc.xpath("//div[@class='info']//a/@href")
            for news_url in news_urls:
                news_url = base_url + news_url
                try:
                    news_buf = fetch(news_url)
                    news_doc = document_fromstring(news_buf.getvalue().decode("utf-8"))
                    news_title = news_doc.xpath("//h1[@class='article-title']/text()")[0]
                    news_ctg = ctg
                    news_time = news_doc.xpath('//*[@id="article-main"]/div[1]/span[2]/text()')[0]
                    news_content = news_doc.xpath(
                        "//div[@class='article-content']//p/text()")  # if len(title) != 0 and len(tm) != 0 and len(content) != 0:

                    cc = ''
                    if len(news_title) != 0:
                        if len(news_content) != 0:
                            for c in news_content:
                                cc = cc + c + '\n'
                            news_dict = defaultdict()
                            news_dict['news_title'] = news_title
                            news_dict['news_ctg'] = news_ctg
                            news_dict['news_time'] = news_time
                            news_dict['news_content'] = cc
                            news_dict['news_url'] = news_url
                            news_list.append(news_dict)
                            print news_title
                            news = News(
                                news_title=news_title,
                                news_ctg=news_ctg,
                                news_content=cc,
                                news_url=news_url,
                                news_time=news_time
                            )
                            news.save()

                except:
                    print news_url + u"该网址不能正常爬取"

                time.sleep(0.1)
    news_data['news'] = news_list
    return news_data
