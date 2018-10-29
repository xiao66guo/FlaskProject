# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

from LoveHome import create_app, db, models
from flask_migrate import MigrateCommand, Migrate, Manager

app = create_app('development')
# 创建一个manager对象
manager = Manager(app)
# 将APP与数据库db进行关联
Migrate(app, db)
# 添加迁移命令
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
