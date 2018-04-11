# -*- coding: utf-8 -*-
"""
@Time    : 2018/2/7 11:12
@Author  : zhaoguoqing600689
@File    : __init__.py.py
@Software: PyCharm
"""
from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from ..models import Permission


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
