# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'


from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_migrate import MigrateCommand, Migrate, Manager
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
# 创建一个manager对象
manager = Manager(app)
# 将APP与数据库db进行关联
Migrate(app, db)
# 添加迁移命令
manager.add_command('db', MigrateCommand)


@app.route('/',methods=['get', 'post'])
def index():
    session['name'] = 'xiaohau'
    return 'index222'


if __name__ == '__main__':
    manager.run()
