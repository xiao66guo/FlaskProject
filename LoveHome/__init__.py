# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import Config


app = Flask(__name__)
# 从对象中加载应用程序的配置
app.config.from_object(Config)
# 创建数据库
db = SQLAlchemy(app)
# redis
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
# 开启CSRF保护
CSRFProtect(app)
# 指定session的保存位置
Session(app)

