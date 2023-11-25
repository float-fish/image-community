APP_ENV = 'develop'


class BaseConfig(object):
    # 数据库的配置

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SECRET_KEY = "sdsdasfwrws"

    # QQ邮箱的配置
    # MAIL_DEBUG = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465  # 端口
    MAIL_USE_SSL = True  # 重要，qq邮箱需要使用SSL
    MAIL_USE_TLS = False  # 不需要使用TLS
    MAIL_USERNAME = '923557344@qq.com'  # 填邮箱
    MAIL_PASSWORD = 'wuqbwtzigllfbfbg'  # 填授权码


class DevelopmentConfig(BaseConfig):
    APP_DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:ysj500236@localhost:3306/processed_picture"


class ProductionConfig(BaseConfig):
    pass


config_map = {
    'develop': DevelopmentConfig,
    'product': ProductionConfig
}
