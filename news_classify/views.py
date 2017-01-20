# coding=utf-8
import json
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from service.data_manage_service import *
# Create your views here.

def home_page(request):
    return render_to_response("news/home.html")

def ajax_dict(request):
    complete_network = json.load(open("/home/zhang/PycharmProjects/sentence_classify_zhang/data_file/webkei_dep.json", 'rb'))
    news_title = request.GET['news_title']
    news_content = request.GET['news_content']
    print news_title, news_content
    return JsonResponse(complete_network)

# 首页
def index(request):
    return render_to_response("index/index.html")

# 关键词提取
def keywords_extraction(request):
    return render_to_response("keywords_extraction/keywords_extraction.html")

# 新闻分类
def CNN_classifier(request):
    return render_to_response("news_data_classify/CNN_classifier.html")

def LSTM_classifier(request):
    return render_to_response("news_data_classify/LSTM_classifier.html")

def RNN_classifier(request):
    return render_to_response("news_data_classify/RNN_classifier.html")


# 新闻管理
def news_data_gathering(request):
    return render_to_response("news_data_manage/news_data_gathering.html")


#  爬取新闻数据
def ajax_gathering_news(request):
    news_site = request.GET['news_site']
    news_start_end_time = request.GET['news_start_end_time']
    page_numbers = int(request.GET['page_numbers'])
    news_ctg = request.GET['news_ctg']
    news_data = crawler(news_site, news_start_end_time, page_numbers, news_ctg)
    json_str = json.dumps(news_data)
    return JsonResponse(json.loads(json_str))

#  分词
def ajax_fenci(request):
    fenci()
    message = {"state": "success"}
    json_str = json.dumps(message)
    return JsonResponse(json.loads(json_str))

#  停用词过滤
def ajax_stopwords_filter(request):
    stopwords_filter()
    message = {"state": "success"}
    json_str = json.dumps(message)
    return JsonResponse(json.loads(json_str))

#  词性标注
def ajax_word_pesg(request):
    word_pesg()
    message = {"state": "success"}
    json_str = json.dumps(message)
    return JsonResponse(json.loads(json_str))

#  生成语料
def ajax_text_corpus(request):
    text_corpus()
    message = {"state": "success"}
    json_str = json.dumps(message)
    return JsonResponse(json.loads(json_str))

#  训练词向量
def ajax_train_word2vec(request):
    sg = int(request.GET['sg'])
    sentences_dir = request.GET['sentences_dir']
    size = int(request.GET['size'])
    window = int(request.GET['window'])
    negative = int(request.GET['negative'])
    hs = int(request.GET['hs'])
    sample = float(request.GET['sample'])

    train_word2vec(sg, sentences_dir, size, window, negative, hs, sample)
    message = {"state": "success"}
    json_str = json.dumps(message)
    return JsonResponse(json.loads(json_str))

def news_data_preprocess(request):
    return render_to_response("news_data_manage/news_data_preprocess.html")

def word2vec(request):
    return render_to_response("news_data_manage/word_to_vec.html")


# 用户管理
def manageUser(request):
    return render_to_response("user_manage/user_manage.html")
