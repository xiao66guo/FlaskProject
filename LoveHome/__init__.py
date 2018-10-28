# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from config import config


# 创建SQLAlchemy的 db 对象
db = SQLAlchemy()

redis_store = None

# 利用工厂方法，根据传入的参数创建出指定参数所对应的参数
def create_app(config_name):
    app = Flask(__name__)
    # 从对象中加载应用程序的配置
    app.config.from_object(config[config_name])
    # 初始化APP
    db.init_app(app)
    # redis
    global redis_store
    redis_store = redis.StrictRedis(host=config[config_name].REDIS_HOST, port=config[config_name].REDIS_PORT)
    # 开启CSRF保护
    CSRFProtect(app)
    # 指定session的保存位置
    Session(app)
    # 注册蓝图
    from LoveHome.api_1_0 import api
    app.register_blueprint(api)

    from LoveHome.web_html import html
    app.register_blueprint(html)




    return app

