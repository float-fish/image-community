#!/usr/bin/env python3.11.4
"""这是一个ORM模型文件

Copyright 2023 Yu Shengjie.
License(GPL)
Author: Yu Shengjie
"""
from datetime import datetime

from werkzeug.security import generate_password_hash

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
    head_picture_id = db.Column(db.Integer, db.ForeignKey(HeadPicture.head_picture_id))
    email = db.Column(db.String(32), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    user_name = db.Column(db.String(20), nullable=False)
    sex = db.Column(db.Enum('男', '女'))
    telephone = db.Column(db.String(32))
    register_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    last_login_time = db.Column(db.DateTime, default=datetime.now())

    head = db.relationship('HeadPicture', back_populates='users', cascade='all')
    old_images = db.relationship('OriginPicture', back_populates='owner', cascade='all')
    new_images = db.relationship('ProcessPicture', back_populates='owner', cascade='all')
    upload_images = db.relationship('CommunityPicture', back_populates='uploader')
    comments = db.relationship('Comment', back_populates='commenter')

    def update_last_login(self):
        self.last_login_time = datetime.now()
        db.session.add(self)
        db.session.commit()

    @property
    def user_password(self):
        raise AttributeError('密码不可访问')

    @user_password.setter
    def user_password(self, password):
        self.password_hash = generate_password_hash(password)

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

     owner 所属的用户
     picture_process 图片关联的处理图片
    """
    __tablename__ = 't_origin_picture'
    picture_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    picture_path = db.Column(db.String(255), nullable=False)
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    picture_name = db.Column(db.String(50), nullable=False)
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
         picture_clarity  图片的清晰度
         owner_id 所属用户id

         picture_from 图片所属的原始图片
         owner 图片的所属用户
        """
    __tablename__ = 't_process_picture'
    picture_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    picture_path = db.Column(db.String(255), nullable=False)
    generate_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    picture_name = db.Column(db.String(50), nullable=False)
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
    """
    管理员
    属性:
     admin_account 管理员账户
     admin_password 管理员密码
     admin_name 管理员名字
    """
    __tablename__ = 't_admin'
    admin_account = db.Column(db.String(32), primary_key=True)
    admin_password = db.Column(db.String(32), nullable=False)
    admin_name = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return '<Admin %r>', self.admin_name


class CommunityPicture(db.Model):
    __tablename__ = 't_community_picture'
    picture_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    picture_path = db.Column(db.String(255), nullable=False)
    upload_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    picture_name = db.Column(db.String(50), nullable=False)
    favor = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    picture_tag = db.Column(db.String(15))
    upload_user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))

    uploader = db.relationship('User', back_populates='upload_images')
    comments = db.relationship('Comment', back_populates='linked_picture')

    def __repr__(self):
        return '<Community Picture %d:%s>' % (self.picture_id, self.picture_name)


class Comment(db.Model):
    __tablename__ = 't_comment'
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment_text = db.Column(db.Text, nullable=False)
    linked_picture_id = db.Column(db.Integer, db.ForeignKey(CommunityPicture.picture_id))
    comment_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    commenter_id = db.Column(db.Integer, db.ForeignKey(User.user_id))

    linked_picture = db.relationship('CommunityPicture', back_populates='comments')
    commenter = db.relationship('User', back_populates='comments')

    def __repr__(self):
        return '<user_id %d:Comment %d (picture:%d) ' % (self.commenter_id, self.comment_id, self.linked_picture_id)


class RestrictionRecord(db.Model):
    __tablename__ = 't_restriction_record'
    restriction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    end_time = db.Column(db.DateTime, nullable=False)
    restriction_user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))

    def __repr__(self):
        return ('<Restriction %d: user_id:%d start_time:%s end_time:%s>'
                % (self.restriction_id, self.restriction_user_id, self.start_time, self.end_time))


class PendingRecord(db.Model):
    __tablename__ = 't_pending_record'
    pending_id = db.Column(db.Integer, primary_key=True, autoincrement=True)


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
