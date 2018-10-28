# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect


# 当前应用程序的配置类
class Config(object):
    DEBUG = True
    SECRET_KEY = 'a39pOBTS06zJw7rK5+wq7uoD11WA7LWWGZyzYiE1ZxwV94P7NvWQGAaFGgX0p3Ih'

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost:3306/loveHome'
    # 关闭对数据库的修改跟踪
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis配置
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379


app = Flask(__name__)

# 从对象中加载应用程序的配置
app.config.from_object(Config)
# 创建数据库
db = SQLAlchemy(app)
# redis
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
# 开启CSRF保护
CSRFProtect(app)


@app.route('/',methods=['get', 'post'])
def index():

    return 'index222'


if __name__ == '__main__':
    app.run()
