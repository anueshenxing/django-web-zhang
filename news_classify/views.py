# coding=utf-8
import json
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from service.crawler_news import *
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
    # print news_site
    # print news_start_end_time
    # print page_numbers
    # print news_ctg
    # print '----------------'
    news_data = crawler(news_site, news_start_end_time, page_numbers, news_ctg)
#     data = {
#     'name' : 'ACME',
#     'shares' : 100,
#     'price' : 542.23
# }
    # complete_network = json.load(open("/home/zhang/PycharmProjects/sentence_classify_zhang/data_file/webkei_dep.json", 'rb'))
    json_str = json.dumps(news_data)
    return JsonResponse(json.loads(json_str))

def news_data_preprocess(request):
    return render_to_response("news_data_manage/news_data_preprocess.html")

def word2vec(request):
    return render_to_response("news_data_manage/word_to_vec.html")


# 用户管理
def manageUser(request):
    return render_to_response("user_manage/user_manage.html")
