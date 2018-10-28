# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'


from . import api


@api.route('/', methods=['get', 'post'])
def index():

    return 'index222'

