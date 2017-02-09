from news_classify.model.news import News
from mongoengine import *
connect('django_mongodb_news')
# news = News(
#     news_title='hello',
#     news_content='mongodb'
# )
# news.news_ctg = 'edu'
# news.save()
for news in News.objects:
    print news.news_title