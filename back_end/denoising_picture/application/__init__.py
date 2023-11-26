from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_cors import CORS
import random
from config import APP_ENV, config_map

db = SQLAlchemy()
mail = Mail()

app = Flask(__name__)
app.config.from_object(config_map[APP_ENV])
app.secret_key = 'swyjqksmx'

CORS(app, resources=r'/*', supports_credentials=True)

db.init_app(app)
mail.init_app(app)


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
