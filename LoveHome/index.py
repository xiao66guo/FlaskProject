# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

from flask import Blueprint


api = Blueprint('api', __name__)
@api.route('/', methods=['get', 'post'])
def index():

    return 'index222'

