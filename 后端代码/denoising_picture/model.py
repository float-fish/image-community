from datetime import datetime
from init import db, app


# 用户表
class User(db.Model):
    __tablename__ = 't_user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    head_picture_id = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(32), nullable=False, unique=True)
    user_password = db.Column(db.String(32), nullable=False)
    user_name = db.Column(db.String(15), nullable=False)
    sex = db.Column(db.Enum('男', '女'))
    telephone = db.Column(db.String(32))
    register_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())


# 头像位置表
class HeadPicture(db.Model):
    __tablename__ = 't_head_picture'
    head_picture_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    head_picture_path = db.Column(db.String(255), nullable=False)


# 原始图片表
class OriginPicture(db.Model):
    __tablename__ = 't_origin_picture'
    picture_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    picture_path = db.Column(db.String(255), nullable=False)
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    picture_name = db.Column(db.String(15), nullable=False)
    collective_tag = db.Column(db.Boolean, nullable=False, default=False)
    owner_id = db.Column(db.Integer, nullable=False)


# 去噪图片表
class ProcessPicture(db.Model):
    __tablename__ = 't_process_picture'
    picture_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    picture_path = db.Column(db.String(255), nullable=False)
    generate_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    picture_name = db.Column(db.String(15), nullable=False)
    collective_tag = db.Column(db.Boolean, nullable=False, default=False)
    owner_id = db.Column(db.Integer, nullable=False)
    picture_accuracy = db.Column(db.Float, nullable=False)
    picture_clarity = db.Column(db.Float, nullable=False)
    origin_picture_id = db.Column(db.Integer, nullable=False)


# 管理员表

class Admin(db.Model):
    __tablename__ = 't_admin'
    admin_account = db.Column(db.String(32), primary_key=True)
    admin_password = db.Column(db.String(32), nullable=False)
    admin_name = db.Column(db.String(15), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
