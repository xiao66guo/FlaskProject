# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import config


# 创建SQLAlchemy的 db 对象
db = SQLAlchemy()


# 利用工厂方法，根据传入的参数创建出指定参数所对应的参数
def create_app(config_name):
    app = Flask(__name__)
    # 从对象中加载应用程序的配置
    app.config.from_object(config[config_name])
    # 初始化APP
    db.init_app(app)
    # redis
    redis_store = redis.StrictRedis(host=config[config_name].REDIS_HOST, port=config[config_name].REDIS_PORT)
    # 开启CSRF保护
    CSRFProtect(app)
    # 指定session的保存位置
    Session(app)

    return app

