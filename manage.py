# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# 当前应用程序的配置类
class Config(object):
    DEBUG = True
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost:3306/loveHome'
    # 关闭对数据库的修改跟踪
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)

# 从对象中加载应用程序的配置
app.config.from_object(Config)
# 创建数据库
db = SQLAlchemy(app)


@app.route('/')
def index():
    return 'index222'


if __name__ == '__main__':
    app.run()
