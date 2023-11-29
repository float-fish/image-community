APP_ENV = 'develop'  # 当前的环境


class BaseConfig(object):
    """ 基本的配置环境
    """
    # 数据库的配置

    SQLALCHEMY_TRACK_MODIFICATIONS = True  # 数据库于
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # session的配置
    SECRET_KEY = "Dramatize6EPcv0fN_81Bj-nA"
    PERMANENT_SESSION_LIFETIME = 3600 * 24  # 设置过期时间为1天

    # TODO redis配置session

    # QQ邮箱的配置
    # MAIL_DEBUG = True
    MAIL_SERVER = 'smtp.qq.com'  # qq的smtp服务器
    MAIL_PORT = 465  # 端口
    MAIL_USE_SSL = True  # 重要，qq邮箱需要使用SSL
    MAIL_USE_TLS = False  # 不需要使用TLS
    MAIL_USERNAME = '923557344@qq.com'  # 填邮箱
    MAIL_PASSWORD = 'wuqbwtzigllfbfbg'  # 填授权码


class DevelopmentConfig(BaseConfig):
    """开发环境下的配置情况

    """
    APP_DEBUG = True
    USERNAME = 'root'  # 用户名
    PASSWORD = 'ysj500236'  # 登录密码
    HOST = 'localhost'  # 数据库IP地址
    PORT = '3306'  # 端口
    DATABASE = 'processed_picture'  # 数据库名
    SQLALCHEMY_DATABASE_URI = ("mysql+pymysql://{}:{}@{}:{}/{}"
                               .format(USERNAME, PASSWORD, HOST, PORT, DATABASE))

    HEAD_PICTURE_DEFAULT_PATH = '/static/user/avatar/default.JPG'


class ProductionConfig(BaseConfig):
    """正式生产环境下的配置情况"""
    pass


""" 配置的参数映射表 """
config_map = {
    'develop': DevelopmentConfig,
    'product': ProductionConfig
}
