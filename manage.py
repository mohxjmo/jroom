# -*- coding: utf-8 -*-
# @Time    : 2018/4/9 10:10
# @Author  : huxiajie
import flask_script
from flask_migrate import Migrate, MigrateCommand
from JRoom import app
from extensions import db
from models import House, Housepic, Payment, User, Manager, Userrecord, Rentrecord

# 初始化命令
manager = flask_script.Manager(app)

# 绑定
migrate = Migrate(app, db)

# 添加命令
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()