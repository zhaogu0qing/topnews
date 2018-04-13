# coding:utf8
"""
Created by zhaoguoqing on 18/1/14

获取一个主题

"""
import sys
import requests
from pymongo import MongoClient

reload(sys)
sys.setdefaultencoding('utf-8')

connDb = MongoClient('mongodb://localhost:27017')
db = connDb.zgq

fav_topics = [
    
    '56298db1daf87d13002c8b20',  # 每天一张老照片
    #'56d2fabe7cb3331100467e2b',  # 值得一看的长文章
    #'54dc0600e4b07c889cd5136f',  # 有豆瓣8.0分以上的新电影
]


def get_one_topic_content(topic_id):
    detail_api = 'https://app.jike.ruguoapp.com/1.0/messages/showDetail?topicId=' + topic_id
    res = requests.get(detail_api)
    if res.status_code == 200:
        res_data = res.json()
        messages = res_data['messages']
        for message in messages:
            item = {}
            for k, v in message.items():
                item[k] = v
            print item['updatedAt']
            print item['content']
            print '\n'
            try:
                db.jike.insert(item)
            except Exception, e:
                print e

    else:
        print 'network error %d' % res.status_code


def main():
    for f_topic in fav_topics:
        get_one_topic_content(f_topic)
    top_topics = db.jike_topic.find({'is_crawl': True})
    for top_topic in top_topics:
        get_one_topic_content(top_topic['id'])

if __name__ == '__main__':
    main()













