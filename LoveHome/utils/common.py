# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'


from werkzeug.routing import BaseConverter

# 定义正则路由转换器
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]


