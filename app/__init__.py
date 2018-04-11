# -*- coding: utf-8 -*-
"""
@Time    : 2018/2/7 11:12
@Author  : zhaoguoqing600689
@File    : __init__.py.py
@Software: PyCharm
"""
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_ckeditor import CKEditor

from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
ckeditor = CKEditor()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)

    # if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
    #     from flask_sslify import SSLify
    #     sslify = SSLify(app)
    #     sslify.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .news import news as news_blueprint
    app.register_blueprint(news_blueprint, url_prefix='/news')

    from .api_1_0 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app

