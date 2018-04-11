# -*- coding: utf-8 -*-
"""
@Time    : 2018/2/7 11:12
@Author  : zhaoguoqing600689
@File    : errors.py
@Software: PyCharm
"""
from flask import render_template
from . import main


@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
