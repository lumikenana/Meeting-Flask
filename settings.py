from redis import Redis


class BaseConf(object):
    DEBUG = False

    # session的secret_key以及session类型
    SECRET_KEY = 'AKSJGHKJ4WHGKJH34H5?><:o'
    SESSION_COOKIE_PATH = '/api'
    SESSION_TYPE = 'redis'

    # sqlalchemy连接数据库设置
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 15
    SQLALCHEMY_POOL_TIMEOUT = 15
    SQLALCHEMY_POOL_RECYCLE = -1
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevConf(BaseConf):
    DEBUG = True

    # session_redis配置数据库地址
    SESSION_REDIS = Redis(host='127.0.0.1', port=6379, db=0)

    # Redis Config
    REDIS_URL = "redis://localhost:6379/1"

    # 数据库连接地址
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://lipipi:35791597lxx.@127.0.0.1:3306/meetroomsystem?charset=utf8mb4'


class ProConf(BaseConf):
    pass
