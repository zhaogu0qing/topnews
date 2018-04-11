# coding:utf8
"""
Created by zhaoguoqing on 18/2/16
"""
from threading import Thread
import subprocess


def spider():
    subprocess.call('python /root/final_design/spider/jike/jike_topic_spider.py')


def run_spider():
    thr = Thread(target=spider, args=[])
    thr.start()
    return thr

