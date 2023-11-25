import os
from datetime import datetime
from smtplib import SMTPDataError
from sqlalchemy.exc import SQLAlchemyError

from application import mail, Message, db
from application.model import User
from werkzeug.security import generate_password_hash, check_password_hash
import random


class UserSystem(object):
    cur_user: User = None
    cur_email_code: str

    def mail_verify(self, email=None):
        exist_email = User.query.filter_by(email=email).first()
        if exist_email:
            code = 400
            msg = '邮箱已经存在'
            return [code, msg, None]
        if not email:
            email = self.cur_user.email
        try:
            self.cur_email_code = str(self.send_mail(email))
            # TODO: 邮箱验证码应该设置一个有效期
            code = 200
            msg = '成功发送邮箱'
            return [code, msg, self.cur_email_code]
        except SMTPDataError:
            code = 500
            msg = '邮件发送错误'
            return [code, msg, None]

    def register(self, email, username, user_password):
        try:
            user = User(email=email, user_name=username, user_password=generate_password_hash(user_password))
            db.session.add(user)
            db.session.commit()
            self.cur_user = user
            return [200, '注册成功']
        except SQLAlchemyError:
            db.session.rollback()
            self.cur_user = None
            return [500, '数据库处理错误']

    def login(self, email, user_password):
        user = User.query.filter_by(email=email).first()
        if not user:
            return [404, '用户未找到', False, False]
        if check_password_hash(user.user_password, user_password):
            self.cur_user = user
            return [200, '登录成功', True, True]
        else:
            return [403, '密码错误', True, False]

    def return_information(self):
        if self.cur_user:
            return self.cur_user
        else:
            return None

    def user_information_change(self, sex=None, tele=None, user_name=None):
        if sex:
            self.cur_user.sex = sex
        if tele:
            self.cur_user.telephone = tele
        if user_name:
            self.cur_user.user_name = user_name
        try:
            db.session.add(self.cur_user)
            db.session.commit()
            return [200, '信息修改成功']
        except SQLAlchemyError:
            db.session.rollback()
            return [500, '数据库操作异常']

    def upload_avatar(self, name, head):
        path = '/static/user/avatar/' + str(self.cur_user.user_id) + name
        head.save(os.getcwd() + path)
        user = User.query.filter_by(user_id=self.cur_user.user_id).first()
        head_data = user.head
        old_path = head_data.head_picture_path
        head_data.head_picture_path = path
        os.remove(old_path)
        db.session.add(head_data)
        db.session.commit()

    def change_password(self, user_password):
        pass

    @staticmethod
    def send_mail(receiver):
        msg = Message("Your verification code", sender="923557344@qq.com", recipients=[receiver])
        code = random.randint(100000, 999999)
        msg.body = 'Your verification code is:\n' + str(code) + "\nPlease don't share this code with anyone."
        msg.html = '''
        <h1>
        尊敬的{receiver}你好,
        </h1>
        <h3>
            欢迎来到 <b>自动驾驶去噪图片社区系统</b>!
        </h3>
        <p>
            您的验证码为 &nbsp;&nbsp; <b>{mailcode}</b> &nbsp;&nbsp;
        </p>
        
        <p>请勿将验证码泄露,分享给他人,感谢您的支持和理解</p>
        <p><small>{time}</small></p>
        '''.format(receiver=receiver, mailcode=code, time=datetime.now())
        mail.send(msg)
        return code
