# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

from flask import Flask


# 当前应用程序的配置类
class Config(object):
    DEBUG = True


app = Flask(__name__)
# 从对象中加载应用程序的配置
app.config.from_object(Config)


@app.route('/')
def index():
    return 'index222'


if __name__ == '__main__':
    app.run()
