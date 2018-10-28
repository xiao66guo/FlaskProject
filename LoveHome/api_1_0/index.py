# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'


from . import api
from LoveHome import redis_store

@api.route('/', methods=['get', 'post'])
def index():
    redis_store.set('name', 'laowang')
    return 'index222'

