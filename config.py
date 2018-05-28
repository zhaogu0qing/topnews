# coding:utf8
"""
Created by zhaoguoqing on 18/2/8
"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '\x917\x1c\xf6\xffR\xd7\xe9c\xec\x93\x0c\x04g5>\x93\x14\xa3z\xe9;\\\x9e'
    BOOTSTRAP_SERVE_LOCAL = True
    FLASK_MAIL_SUBJECT_PREFIX = '[Top News]'
    FLASK_MAIL_SENDER = 'TopNews Admin <topnews_cn@163.com>'
    TOPNEWS_ADMIN = '1903601292@qq.com'
    TOPNEWS_POSTS_PER_PAGE = 10
    TOPNEWS_COMMENTS_PER_PAGE = 10
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'topnews_cn@163.com'
    MAIL_PASSWORD = 'watch1dog'

    SSL_DISABLE = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:ZGQdemysql@localhost/final_design'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:ZGQdemysql@123.206.33.158/final_design'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:ZGQdemysql@123.206.33.158/test'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:ZGQdemysql@localhost/final_design'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'prodution': ProductionConfig,

    'default': DevelopmentConfig,
}
