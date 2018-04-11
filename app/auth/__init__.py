# -*- coding: utf-8 -*-
"""
@Time    : 2018/2/7 13:08
@Author  : zhaoguoqing600689
@File    : __init__.py
@Software: PyCharm
"""
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
