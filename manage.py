# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

from flask_migrate import MigrateCommand, Migrate, Manager
from LoveHome import app, db


# 创建一个manager对象
manager = Manager(app)
# 将APP与数据库db进行关联
Migrate(app, db)
# 添加迁移命令
manager.add_command('db', MigrateCommand)


@app.route('/',methods=['get', 'post'])
def index():

    return 'index222'


if __name__ == '__main__':
    manager.run()
