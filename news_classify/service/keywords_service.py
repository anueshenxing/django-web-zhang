# coding=utf8


from collections import defaultdict
import cPickle
import news_classify.util.global_set as global_set
from news_classify.model.news import News
import cPickle
from collections import defaultdict
import numpy as np
from news_classify.util.tools import *
from news_classify.service.data_manage_service import jieba_fenci, load_stopwords
import json
from mongoengine import *

import sys

reload(sys)
sys.setdefaultencoding("utf-8")
connect('django_mongodb_news')


def CosineDist(arrA, arrB):
    """
        功能：cosine距离距离计算
        输入：两个一维数组
    """
    return np.dot(arrA, arrB) / (np.linalg.norm(arrA) * np.linalg.norm(arrB))


def built_word_connect(V, b, W):
    """
        功能:建立新闻内容中词的网络连接
        输入:
            V:新闻内容分词、去停用词过后的词ID表示
            b:建立连接的阈值
            W:词的标号 与向量的对应关系
        输出：词网络连接矩阵
    """
    n = len(V)  # 新闻内容中词的个数
    E = np.zeros((n, n), dtype=np.float32)
    for i in range(n):
        for j in range(i, n):
            Vi = int(V[i])  # 词的id
            Vj = int(V[j])  # 词的id
            arrA = np.asarray(W[Vi])
            arrB = np.asarray(W[Vj])
            cosine_dist = CosineDist(arrA, arrB)
            if i == j:
                E[i][j] = 1.
            if cosine_dist > b:
                E[i][j] = cosine_dist
                E[j][i] = cosine_dist

    return E

# 生成新闻内容语义复杂网络
def get_word_comlete_network(news_content):
    pre_dir = "/home/zhang/PycharmProjects/sentence_classification/data_file/"
    all_news_word_tf_idf_and_others_dir = pre_dir + "all_news_word_tf_idf_and_others.p"
    word_vec_dict_dir = pre_dir + "word_vec_dict.p"
    all_news_word_tf_idf_and_others = cPickle.load(open(all_news_word_tf_idf_and_others_dir, "rb"))
    word_vec_dict = cPickle.load(open(word_vec_dict_dir, "rb"))
    wordtoix, ixtoword = all_news_word_tf_idf_and_others[0], all_news_word_tf_idf_and_others[1]

    # 保存词的标号 与向量的对应关系
    W = word_vec_dict[0]

    news_content = news_content.decode('utf-8')
    stopwords_file_dir = global_set.DATA_FILE_DIR + "direct_use/stopwords_csdn_shijieba2009.txt"
    stopwords = load_stopwords(stopwords_file_dir)
    news_content_word_list = jieba_fenci(news_content)
    news_content_word_list_without_stopword = []
    V = []  # 将新闻内容的词用id表示

    # 去除分词过后的停用词
    for word in news_content_word_list:
        if word not in stopwords:
            news_content_word_list_without_stopword.append(word.encode('utf-8'))

    # 将新闻内容的词用id表示
    for word in news_content_word_list_without_stopword:
        V.append(wordtoix[word])
    # 两词的语义相似度大于b时，建立连接
    b = global_set.threshold_b
    E = built_word_connect(V, b, W)
    n = len(V)  # 新闻内容中词的个数

    webkit_dep = defaultdict()
    nodes = []
    links = []

    for i in range(n):
        node_dict = defaultdict()
        node_dict["category"] = 0
        node_dict["name"] = ixtoword[V[i]].encode("utf-8")
        nodes.append(node_dict)
        for j in range(i + 1, n):
            similarity = E[i][j]
            if similarity > 0.5:
                relate_dict = defaultdict()
                relate_dict["source"] = i
                relate_dict["target"] = j
                relate_dict["weight"] = 1
                links.append(relate_dict)

    webkit_dep["nodes"] = nodes
    webkit_dep["links"] = links
    with open(global_set.DATA_FILE_DIR + 'enable_generate/complete_network.json', 'wb') as f:
        json.dump(webkit_dep, f)
