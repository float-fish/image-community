from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import pymysql
from config import config_map
import random

db = SQLAlchemy()
mail = Mail()


def create_app(dev_name):
    app = Flask(__name__)
    config_class = config_map.get(dev_name)
    app.config.from_object(config_class)

    db.init_app(app)
    mail.init_app(app)

    from .view import auth
    app.register_blueprint(auth.auth)

    return app

def send_mail(receiver):
    msg = Message("Your verification code", sender="923557344@qq.com", recipients=[receiver])
    code = random.randint(100000, 999999)
    msg.body = 'Your verification code is:\n'+str(code)+"\nPlease don't share this code with anyone."
    mail.send(msg)
    return code