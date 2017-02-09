# coding=utf8

import sys
import pycurl
import StringIO
import re
import time
from lxml import etree
from lxml.html import document_fromstring
import time
from mongoengine import connect, DynamicDocument, StringField, DictField
from pymongo import MongoClient


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


if __name__ == '__main__':
    url = "http://www.toutiao.com/i6290733545220473346/"
    buf = fetch(url)
    doc = document_fromstring(buf.getvalue().decode("utf-8"))
    news_title = doc.xpath("//h1[@class='article-title']/text()")[0]
    news_ctg = ""
    news_url = ""
    news_time = doc.xpath('//*[@id="article-main"]/div[1]/span[2]/text()')[0]
    content = doc.xpath(
        "//div[@class='article-content']//p/text()")  # if len(title) != 0 and len(tm) != 0 and len(content) != 0:

    if len(news_title) != 0:
        cc = ''
        if len(content) != 0:
            for c in content:
                cc = cc + c + '\n'
            print news_title
            print cc

    print news_time