from datetime import datetime
from application import db, app


# 头像位置表
class HeadPicture(db.Model):
    __tablename__ = 't_head_picture'
    head_picture_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    head_picture_path = db.Column(db.String(255), nullable=False)

    users = db.relationship('User', back_populates='head')


# 用户表
class User(db.Model):
    __tablename__ = 't_user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    head_picture_id = db.Column(db.Integer, db.ForeignKey(HeadPicture.head_picture_id))
    email = db.Column(db.String(32), nullable=False, unique=True)
    user_password = db.Column(db.String(32), nullable=False)
    user_name = db.Column(db.String(15), nullable=False)
    sex = db.Column(db.Enum('男', '女'))
    telephone = db.Column(db.String(32))
    register_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    head = db.relationship('HeadPicture', back_populates='users')
    old_images = db.relationship('OriginPicture', back_populates='owner', cascade='all')
    new_images = db.relationship('ProcessPicture', back_populates='owner', cascade='all')


# 原始图片表
class OriginPicture(db.Model):
    __tablename__ = 't_origin_picture'
    picture_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    picture_path = db.Column(db.String(255), nullable=False)
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    picture_name = db.Column(db.String(15), nullable=False)
    collective_tag = db.Column(db.Boolean, nullable=False, default=False)
    owner_id = db.Column(db.Integer, db.ForeignKey(User.user_id))

    owner = db.relationship('User', back_populates='old_images')
    picture_process = db.relationship('ProcessPicture', back_populates='picture_from')


# 去噪图片表
class ProcessPicture(db.Model):
    __tablename__ = 't_process_picture'
    picture_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    picture_path = db.Column(db.String(255), nullable=False)
    generate_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    picture_name = db.Column(db.String(15), nullable=False)
    collective_tag = db.Column(db.Boolean, nullable=False, default=False)
    picture_accuracy = db.Column(db.Float, nullable=False)
    picture_clarity = db.Column(db.Float, nullable=False)
    origin_picture_id = db.Column(db.Integer, db.ForeignKey(OriginPicture.picture_id))
    owner_id = db.Column(db.Integer, db.ForeignKey(User.user_id))

    picture_from = db.relationship('OriginPicture', back_populates='picture_process')
    owner = db.relationship('User', back_populates='new_images')


# 管理员表

class Admin(db.Model):
    __tablename__ = 't_admin'
    admin_account = db.Column(db.String(32), primary_key=True)
    admin_password = db.Column(db.String(32), nullable=False)
    admin_name = db.Column(db.String(15), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
