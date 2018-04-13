# coding:utf-8
"""
author: zhaoguoqing
filename: 新浪_7_14.py
createtime: 2017/7/14 9:45
"""
import datetime
import requests
import pymongo
from bs4 import BeautifulSoup
import re
import sys

GET_NUM = 300   # 每天各栏目返回新闻数

reload(sys)
sys.setdefaultencoding('utf-8')

reload(sys)
sys.setdefaultencoding('utf-8')

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.zgq

demand = {
    '国内新闻': '90',
    '国际新闻': '91',
    '社会新闻': '92',
    '军事新闻': '93',
    '体育新闻': '94',
    '娱乐新闻': '95',
    '科技新闻': '96',
    '财经新闻': '97',
    '股市新闻': '98',
    '美股新闻': '99'
}


def api_parser(api_url):
    """解析api, 返回url解析"""
    jso = requests.get(api_url).content
    """去掉var jsonData="""
    jso = jso[14:-1]
    """js格式转为标准json格式"""
    jso = re.sub(r'(,?)(\w+?)\s+?:', r'\1"\2" :', jso)
    """json转为python dict"""
    jso = eval(jso)
    # jso = jso.decode('utf-8')
    for i in jso['list']:
        title, url = i['title'].decode('gbk').encode('utf-8'), i['url']
        match = re.search(r'https?://([a-zA-Z]+)\..*?/(\d+-\d+-\d+)/.*?', url)
        if match:
            n_type = match.group(1)
            n_date = match.group(2)
        else:
            n_type = n_date = None

        print title, url, n_type, n_date

        res = requests.get(url)
        if res.status_code == 200:
            html = res.content
        else:
            print 'network error, %d' % res.status_code
            continue
        body = BeautifulSoup(html, 'html.parser').body
        content = body.find('div', {'id': 'artibody'}) or body.find('div', {'id': 'article'})
        img_list = []
        imgs = content.find_all('img')
        for img in imgs:
            src = img.get('src')
            img_list.append(src)
        if not content:
            print 'parse error'
            continue
        for s in content.find_all('script'):
            s.decompose()

        print 'succ'
        # print content

        item = {
            'source': 'sina',
            'imgs': img_list,
            'title': title,
            'url': url,
            'n_type': n_type,
            'n_date': n_date,
            'crawl_date': datetime.datetime.now(),
            # 'html': html.encode('utf-8'),
            'content': content.encode('utf-8'),
        }
        try:
            db.news.insert(item)
        except Exception, e:
            print e


def main():
    for d in demand:
        api_url = 'http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?col=' \
                  + demand[d] + '&num=' + str(GET_NUM)
        api_parser(api_url)


if __name__ == '__main__':
    main()
