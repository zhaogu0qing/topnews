# -*- coding: utf-8 -*-
"""
@Time    : 2018/2/7 11:12
@Author  : zhaoguoqing600689
@File    : __init__.py.py
@Software: PyCharm
"""
from flask import Blueprint

news = Blueprint('news', __name__)

from . import views
