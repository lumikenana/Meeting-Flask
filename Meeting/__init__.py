from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from .models import *
from flask_session import Session
from flask_redis import FlaskRedis

redis = FlaskRedis()
from .views.mt_account import mt_account
from .views.mt_room import mt_room
from .views.mt_base import mt_base
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings.DevConf")
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    # 初始化flask-session
    Session(app)
    # 初始化flask-sqlalchemy，根据settings文件配置数据库
    db.init_app(app)
    # 初始化redis数据库
    redis.init_app(app, decode_responses=True)
    # 在app中注册蓝图
    app.register_blueprint(mt_account)
    app.register_blueprint(mt_room)
    app.register_blueprint(mt_base)

    return app
