# -*- coding: utf-8 -*-
"""
@Time    : 2018/2/7 11:12
@Author  : zhaoguoqing600689
@File    : errors.py
@Software: PyCharm
"""
from flask import render_template, request, jsonify
from . import main


@main.errorhandler(403)
def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


@main.errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and not not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template('404.html'), 404


@main.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


