#!/usr/bin/env python3.11.4
"""这是一个ORM模型文件

Copyright 2023 Yu Shengjie.
License(GPL)
Author: Yu Shengjie
"""
from datetime import datetime
from application import db, app


# TODO 增加to json的函数,简化json的传递

# 头像位置表
class HeadPicture(db.Model):
    """
    头像表
    属性:
     head_picture_id 头像编号
     head_picture_path 头像图片的相相对路径

     users:与头像表数据相关联的用户
    """
    __tablename__ = 't_head_picture'
    head_picture_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    head_picture_path = db.Column(db.String(255), nullable=False)

    users = db.relationship('User', back_populates='head')

    def __repr__(self):
        return '<Avatar %d>', self.head_picture_id


# 用户表
class User(db.Model):
    """
    用户表
    属性:
     user_id 用户编号
     head_picture_id 用户头像编号
     email  用户邮箱
     user_password 用户密码(哈希化)
     sex 性别
     telephone 电话号码
     register_time 注册时间

     head 用户关联的头像对象
     old_images 用户上传的原始图像
     new_images 用户生成的处理图像
    """
    __tablename__ = 't_user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    head_picture_id = db.Column(db.Integer, db.ForeignKey(HeadPicture.head_picture_id), default=1)
    email = db.Column(db.String(32), nullable=False, unique=True)
    user_password = db.Column(db.String(200), nullable=False)
    user_name = db.Column(db.String(15), nullable=False)
    sex = db.Column(db.Enum('男', '女'))
    telephone = db.Column(db.String(32))
    register_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    # TODO last_login_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    # TODO restrict_time

    head = db.relationship('HeadPicture', back_populates='users')
    old_images = db.relationship('OriginPicture', back_populates='owner', cascade='all')
    new_images = db.relationship('ProcessPicture', back_populates='owner', cascade='all')

    # TODO 设置密码,和密码生成hash,使用token来进行标识
    # def update_last_login(self):
    #     self.last_login_time = datetime.now()
    #     db.session.add(self)
    #     db.session.commit()

    def __repr__(self):
        return '<User %d:%r>' % (self.user_id, self.email)


# 原始图片表
class OriginPicture(db.Model):
    """
    原始图像表
    属性:
     picture_id 图片id
     picture_path 图片的生成路径
     update_time 上传的时间
     picture_name 图片名称
     collective_tag 收藏标志
     owner_id 所属用户id
    """
    __tablename__ = 't_origin_picture'
    picture_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    picture_path = db.Column(db.String(255), nullable=False)
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    picture_name = db.Column(db.String(50), nullable=False)  # TODO 更改下名字的长度
    collective_tag = db.Column(db.Boolean, nullable=False, default=False)
    owner_id = db.Column(db.Integer, db.ForeignKey(User.user_id))

    owner = db.relationship('User', back_populates='old_images')
    picture_process = db.relationship('ProcessPicture', back_populates='picture_from')

    def __repr__(self):
        return '<RawJpg %d>', self.picture_id


# 去噪图片表
class ProcessPicture(db.Model):
    """
        处理图像表
        属性:
         picture_id 图片id
         picture_path 图片的生成路径
         update_time 上传的时间
         picture_name 图片名称
         collective_tag 收藏标志
         picture_accuracy 图片的准确度

         owner_id 所属用户id
        """
    __tablename__ = 't_process_picture'
    picture_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    picture_path = db.Column(db.String(255), nullable=False)
    generate_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    picture_name = db.Column(db.String(50), nullable=False)  # TODO 更改下名字的长度
    collective_tag = db.Column(db.Boolean, nullable=False, default=False)
    picture_accuracy = db.Column(db.Float, nullable=False)
    picture_clarity = db.Column(db.Float, nullable=False)
    origin_picture_id = db.Column(db.Integer, db.ForeignKey(OriginPicture.picture_id), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    # TODO processmode 去噪模式的设置

    picture_from = db.relationship('OriginPicture', back_populates='picture_process')
    owner = db.relationship('User', back_populates='new_images')

    def __repr__(self):
        return '<ProcessedJpg %d>', self.picture_id


# 管理员表

class Admin(db.Model):
    __tablename__ = 't_admin'
    admin_account = db.Column(db.String(32), primary_key=True)
    admin_password = db.Column(db.String(32), nullable=False)
    admin_name = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return '<Admin %r>', self.admin_name


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
