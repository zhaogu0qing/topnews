# coding:utf8
"""
Created by zhaoguoqing on 18/2/12
"""
from flask import Blueprint

api = Blueprint('api', __name__)

from . import authentication, posts, users, comments, errors
