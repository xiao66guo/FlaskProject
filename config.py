# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

import redis

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

    # 设置session保存的参数
    SESSION_TYPE = 'redis'
    # 设置session保存redis的相关链接信息，如果不进行设置会以默认的IP和端口进行处理
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 开启session签名
    SESSION_USE_SIGNER = True
    # 设置session的过期时间
    PERMANENT_SESSION_LIFETIME = 86400 * 2



