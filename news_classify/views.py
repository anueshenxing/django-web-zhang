# coding=utf-8
import json

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
# Create your views here.
from django.template import loader


# def detail(request, question_id):
#     return HttpResponse("you're looking at question %s." % question_id)
#
# def results(request, question_id):
#     response = "You're looking at the result of question %s."
#     return HttpResponse(response % question_id)
#
# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)

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

def news_data_preprocess(request):
    return render_to_response("news_data_manage/news_data_preprocess.html")

def word2vec(request):
    return render_to_response("news_data_manage/word_to_vec.html")


# 用户管理
def manageUser(request):
    return render_to_response("user_manage/user_manage.html")
