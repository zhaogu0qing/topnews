# coding:utf8
"""
Created by zhaoguoqing on 18/2/22
"""
import jieba
from pymongo import MongoClient
from bs4 import BeautifulSoup
from numpy import *
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

client = MongoClient('mongodb://zgq:1234@47.93.186.132:27017/admin')
db = client.zgq
stopwords = [line.strip().decode('utf-8') for line in open('stopwords.txt').readlines()]
theta = 0.5
xClusterID = 1


def cut_words(in_text_list):
    res_list = []
    for _line in in_text_list:
        _line = [ln.decode('utf-8') for ln in _line.splitlines() if ln.strip()]
        str_line = ''.join(_line)
        seg_list = jieba.cut(str_line, cut_all=False)  # 精确模式
        lst = list(seg_list)
        for seg in lst[:]:  # 注意这里要使用切片，不然删除了元素之后，index改变
            if seg in stopwords:
                lst.remove(seg)
        output = ' '.join(list(lst))  # 空格拼接
        res_list.append(output)
    return res_list


def getTfidfMat(lst):  # 测试函数
    # 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
    vectorizer = CountVectorizer()
    # 该类会统计每个词语的tf-idf权值
    transformer = TfidfTransformer()
    # 第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
    tfidf = transformer.fit_transform(vectorizer.fit_transform(lst))
    # 获取词袋模型中的所有词语
    word = vectorizer.get_feature_names()
    # 将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
    weight = tfidf.toarray()
    # 词频cp=vectorizer.fit_transform(lst)
    # 词频cp=cp.toarray()
    # for i in range(len(weight)):
    #     for j in range(len(word)):
    #         print word[j],cp[i][j],'#',
    #     print '\n'
    return weight


if __name__ == "__main__":

    news_list = []
    news_cursor = db.news.find({'is_process': {'$exists': False}}, {'content': 1, '_id': 1}).limit(10)
    for news in news_cursor:
        news_text = BeautifulSoup(news['content'], 'html.parser').get_text().strip()
        news_list.append(news_text)
    for news in news_list:  # 读出未分类的新闻
        # 更新weightMat
        corpus = []
        trClusterID = []

        news_cursor = db.news.find({'is_process': 1}, {'content': 1, '_id': 0, 'ClusterID': 1}).limit(10)
        for n in news_cursor:
            corpus.append(n['content'])
            trClusterID.append(n['ClusterID'])

        segedTxtlst = cut_words(corpus)
        vectorizer = TfidfVectorizer()
        trainTfidf = vectorizer.fit_transform(segedTxtlst)
        weightMat = trainTfidf.toarray()  # 得到语料库的VSM
        # 更新weightMat结束

        temContent = []
        temContent.append(news['content'])
        segedInLst = cut_words(temContent)  # 对该新闻分词
        testTfidf = vectorizer.transform(segedInLst)
        testVec = testTfidf.toarray()  # 得到基于tf-idf的文档向量
        # 计算testVec和weightMat每一行的余弦相似度
        xx = cosine_similarity(testVec, weightMat)
        ndxx = array(xx)
        max = ndxx.max()
        if (max > theta):
            indxx = argmax(ndxx)  # 最大值在weightMat的index已经找到
            print indxx
            # db.news.update({'_id': news['_id']}, {'$set': {'is_process': 1, 'ClusterID': trClusterID[indxx]}})
        else:  #
            # 不大于某阈值就新建一个分类
            # ms.ExecNonQuery("UPDATE corpora set ClusterID='%s',isProcessed=1 WHERE ID=%s" % (xClusterID, ID0))
            print xClusterID
            xClusterID += 1
            # 已经把一条新闻聚到某个簇了，下面要更新一下weightMat
