# coding=utf8

import pycurl
import StringIO
from collections import defaultdict
import cPickle
import sys
import news_classify.util.global_set as global_set
import jieba
import jieba.posseg as pseg
from lxml import etree
from lxml.html import document_fromstring
import time
from news_classify.model.news import News
from mongoengine import *
import multiprocessing
import gensim

reload(sys)
sys.setdefaultencoding("utf-8")
connect('django_mongodb_news')


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


# 仅生成分词
def jieba_fenci(text):
    term = text.split('\n')
    s = ""
    for i in term:
        s += i
    seg_list = jieba.cut(s)
    return seg_list


# 生成分词及其词性
def jieba_pseg(text):
    term = text.split('\n')
    s = ""
    for i in term:
        s += i
    word_flag_dict = pseg.cut(s)
    return word_flag_dict


# 加载停用词表
def load_stopwords(file_dir):
    f = open(file_dir, 'rb')
    stopwords = []
    for word in f:
        word = word.split('\n')[0]
        stopwords.append(word.encode('utf-8'))
    f.close()
    return stopwords


def crawler(news_site, news_start_end_time, page_numbers, news_ctg):
    news_data = defaultdict()
    news_list = []
    base_url = news_site
    star_end_time = news_start_end_time
    page_num = page_numbers
    tags = news_ctg.split(',')
    for ctg in tags:
        ctg_url = base_url + '/' + 'articles_news_' + ctg + '/'
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


def fenci():
    for news in News.objects:
        news_title = news.news_title.decode('utf-8')
        news_content = news.news_content.decode('utf-8')
        news.news_title_fenci = " ".join(jieba_fenci(news_title)).encode('utf-8')
        news.news_content_fenci = " ".join(jieba_fenci(news_content)).encode('utf-8')
        news.save()


def stopwords_filter():
    stopwords_file_dir = global_set.DATA_FILE_DIR + "direct_use/stopwords_csdn_shijieba2009.txt"
    stopwords = load_stopwords(stopwords_file_dir)
    for news in News.objects:
        news_title_fenci = news.news_title_fenci.encode('utf-8')
        news_content_fenci = news.news_content_fenci.encode('utf-8')
        title = []
        content = []
        for word in news_title_fenci.split(" "):
            if word not in stopwords:
                title.append(word)

        for word in news_content_fenci.split(" "):
            if word not in stopwords:
                content.append(word)
        news.news_title_fenci_noSTW = " ".join(title).encode('utf-8')
        news.news_content_fenci_noSTW = " ".join(content).encode('utf-8')
        news.save()


def word_pesg():
    stopwords_file_dir = global_set.DATA_FILE_DIR + "direct_use/stopwords_csdn_shijieba2009.txt"
    stopwords = load_stopwords(stopwords_file_dir)
    word_flag_vocab = defaultdict()
    for news in News.objects:
        news_title = news.news_title.decode('utf-8')
        news_content = news.news_content.decode('utf-8')
        for word, flag in jieba_pseg(news_title):
            if word not in stopwords:
                word_flag_vocab[word] = flag

        for word, flag in jieba_pseg(news_content):
            if word not in stopwords:
                word_flag_vocab[word] = flag

    cPickle.dump([word_flag_vocab], open(global_set.DATA_FILE_DIR + "enable_generate/word_flag_vocab.p", "wb"))


def text_corpus():
    news_corpus_dir = global_set.DATA_FILE_DIR + "enable_generate/news_corpus.txt"
    news_corpus = open(news_corpus_dir, "a")
    for news in News.objects:
        one_news_text = news.news_title_fenci_noSTW.decode('utf-8') + " " + \
                        news.news_title_fenci_noSTW.decode('utf-8')
        news_corpus.write(one_news_text.encode('utf-8') + "\n")
    news_corpus.close()


def train_word2vec(sg, sentences_dir, size, window, negative, hs, sample):
    sentences_dir = global_set.DATA_FILE_DIR + sentences_dir
    sentences = gensim.models.word2vec.Text8Corpus(sentences_dir)
    model = gensim.models.Word2Vec(sentences, sg=sg, size=size, window=window, negative=negative, hs=hs,
                                   sample=sample, workers=multiprocessing.cpu_count())
    model.save(global_set.DATA_FILE_DIR + 'enable_generate/news_corpus_word2vec')
    # model.save_word2vec_format(global_set.DATA_FILE_DIR + 'news_corpus_word2vec' + '.vector', binary=True)


if __name__ == "__main__":
    model = gensim.models.Word2Vec.load("/home/zhang/PycharmProjects/django-web-zhang-git/data_file/news_corpus_word2vec")
    print model.most_similar(u'月')
