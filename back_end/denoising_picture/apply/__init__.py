from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

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