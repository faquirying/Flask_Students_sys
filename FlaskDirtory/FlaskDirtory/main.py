import os

from flask import Flask
from flask import session
import pymysql

from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect   #  CSRFProtect在1.0之后移除

# 之前好多flask插件都存放在ext模块下
# 后来独立出来，我们以flask_session为例
# from flask_session import Session

pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.config.from_object('config.DebugConfig')

csrf = CSRFProtect(app)  # 开启CSRFProtect

models = SQLAlchemy(app)