# -*- coding: utf-8 -*-
"""
@Time    : 2018/2/7 11:12
@Author  : zhaoguoqing600689
@File    : views.py
@Software: PyCharm
"""
from flask import redirect, flash, url_for
from flask import render_template
from flask_login import login_required
import pymongo
from bson import ObjectId
from . import news
from .forms import JikeTopicForm
from ..decorators import admin_required

client = pymongo.MongoClient('mongodb://admin_zgq:ZGQ_mongodb@123.206.33.158:27017/admin')
# client = pymongo.MongoClient('mongodb://admin_zgq:ZGQ_mongodb@localhost:27017/admin')
db = client.zgq


@news.route('/')
def news_index():
    all_news = []
    sina_news = db.news.find(
        {'source': 'sina', 'n_type': {'$ne': 'sports'}},
        {'html': 0}).sort([('n_date', -1)]).limit(20)
    for n in sina_news:
        all_news.append(n)
    nhk_news = db.news.find({'source': 'nhk'}, {'html': 0}).sort([('_id', -1)]).limit(10)
    for n in nhk_news:
        all_news.append(n)

    return render_template('index.html',
                           news=all_news)


@news.route('/new_detail/<string:news_id>')
def news_page(news_id):
    news = db.news.find_one({'_id': ObjectId(news_id)}, {'html': 0})
    return render_template('news/news_detail.html', news=news)


# photo
@news.route('/old_photo')
def get_old_photo():
    photos = db.jike.find({'topicId': 822}).sort([('_id', -1)]).limit(10)
    return render_template('news/photo.html', photos=photos)


# jike
@news.route('/jike')
def get_jike():
    # return redirect('8090:news/jike/topic/454')
    return redirect(url_for('.jike_topic', topicId=454))


@news.route('/jike/topic/<int:topicId>')
def jike_topic(topicId):
    topics = db.jike_topic.find({'is_crawl': True})
    current_topic = db.jike_topic.find_one({'topicId': topicId})
    current_topic_items = db.jike.find({'topicId': topicId}, {'_id': 0}).sort([('createdAt', -1)]).limit(20)
    return render_template('news/jike.html',
                           topics=topics,
                           current_topic=current_topic,
                           current_topic_items=current_topic_items)


@news.route('/jike/select-topic')
@login_required
@admin_required
def select_topic():
    topics = db.jike_topic.find({'topicId': {'$exists': True}, 'subscribersCount': {'$gt': 300000}})
    return render_template('news/select_topic.html', topics=topics)


@news.route('/jike/modify-topic/<int:topic_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def modify_topic(topic_id):
    topic = db.jike_topic.find_one({'topicId': topic_id})
    form = JikeTopicForm()
    if form.validate_on_submit():
        db.jike_topic.update({'topicId': topic_id}, {'$set': {'is_crawl': form.is_crawl.data}})
        flash('Topic状态已更新')
        return redirect(url_for('.get_jike'))
    form.is_crawl.data = topic.get('is_crawl')
    return render_template('news/edit_topic.html', form=form, topic=topic)
