class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:ysj500236@localhost:3306/processed_picture'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'sdasldk123@#*$'

    MAIL_SERVER = "smtp.qq.com",
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = "923557344@qq.com",
    MAIL_PASSWORD = "wuqbwtzigllfbfbg"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass


config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig
}
