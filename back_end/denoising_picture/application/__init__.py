from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:ysj500236@localhost:3306/processed_picture"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "sdasldk123@#*$"

app.config.update(
    MAIL_SERVER="smtp.qq.com",
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME="923557344@qq.com",
    MAIL_PASSWORD="wuqbwtzigllfbfbg"
)

db = SQLAlchemy(app)

mail = Mail(app)


def send_mail(receiver):
    msg = Message("Your verification code", sender="923557344@qq.com", recipients=[receiver])
    code = random.randint(100000, 999999)
    msg.body = 'Your verification code is:\n' + str(code) + "\nPlease don't share this code with anyone."
    mail.send(msg)
    return code


from application.view import auth, admin
from application.view.user_picture import picture

app.register_blueprint(auth.bp)
app.register_blueprint(picture.bp)
app.register_blueprint(admin.admin_bp)
