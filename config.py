# -*- coding: utf-8 -*-
# @Time    : 2018/4/4 14:56
# @Author  : huxiajie
import os

# DEBUG
DEBUG = True

# DATABASE
DIALECT = 'mysql'
DRIVER = 'mysqldb'
USERNAME = 'root'
PASSWORD = '123456'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'jroom'
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                                       DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# SECRET_KEY
SECRET_KEY = os.urandom(24)
