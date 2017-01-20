# coding=utf-8
"""Django_web_zhang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import django
from django.conf.urls import url, include
from django.contrib import admin

import news_classify.views as news_views
from Django_web_zhang import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', news_views.index),
    # url(r'^news_classify/', include('news_classify.urls')),
    url(r'^staticfiles/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.STATICFILES_DIRS, 'show_indexes': True}),

    # ajax 异步获取数据
    url(r'^get_webkit_dep$', news_views.ajax_dict),

    # 关键词提取页面
    url(r'^keyword_extraction$', news_views.keywords_extraction),

    # 新闻分类
    url(r'^CNN_classifier$', news_views.CNN_classifier),
    url(r'^LSTM_classifier$', news_views.LSTM_classifier),
    url(r'^RNN_classifier$', news_views.RNN_classifier),

    # 新闻管理
    url(r'^news_data_gathering$', news_views.news_data_gathering),
    url(r'^news_data_preprocess$', news_views.news_data_preprocess),
    url(r'^word_to_vec$', news_views.word2vec),
    url(r'^ajax_gathering_news$', news_views.ajax_gathering_news),
    url(r'^ajax_fenci$', news_views.ajax_fenci),
    url(r'^ajax_stopwords_filter$', news_views.ajax_stopwords_filter),
    url(r'^ajax_word_pesg$', news_views.ajax_word_pesg),
    url(r'^ajax_text_corpus$', news_views.ajax_text_corpus),
    url(r'^ajax_train_word2vec$', news_views.ajax_train_word2vec),

    # 用户管理
    url(r'^user_manage$', news_views.manageUser),
]
