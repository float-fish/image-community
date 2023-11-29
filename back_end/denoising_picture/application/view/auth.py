#!/usr/bin/env python3.11.4
""" 对前端页面实现用户基本操作的api接口

Copyright 2023 Yu Shengjie.
License(GPL)
Author: Yu Shengjie
"""
import os

from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

from application import db, send_mail
from .user_personal.Userclass import UserSystem
from ..model import User, HeadPicture

bp = Blueprint('auth', __name__, url_prefix='/user')

user_system = UserSystem()


@bp.route('/register_email', methods=['POST'])
def register_email():
    """ 视图函数--发送注册的邮箱验证码

    :return:
    code 返回的HTTP状态码
    msg  返回的消息数据
    mail_code 返回的验证码的值
    """
    register_data = request.get_json()
    email = register_data.get('email')
    # 检测请求格式
    if not email:
        return jsonify(code=400, msg='登录请求参数不完整'), 400

    # 发送验证码
    [code, msg, mail_code] = user_system.mail_verify(email)
    return jsonify(code=code, msg=msg, mail_code=mail_code), code


@bp.route('/register', methods=['POST'])
def register():
    """视图函数--将用户注册进入用户数据库

    :arg
     email:用户注册邮箱
     password:用户注册密码
     username:用户名

    :return:
     code 返回的HTTP状态码
     msg  返回的消息数据
    """
    # 接收参数
    json_data = request.get_json()
    email = json_data.get('email')
    username = json_data.get('username')
    password = json_data.get('password')
    if not all([email, password, username]):
        return jsonify(code=400, msg='登录请求参数不完整'), 400

    # 添加头像默认数据
    head = HeadPicture(head_picture_path='/static/user/avatar/default.JPG')  # TODO 之后应避免这种硬编码
    head_id = head.head_picture_id

    # 添加用户进入数据库
    user = User(email=email, user_name=username, user_password=generate_password_hash(password),
                head_picture_id=head_id)
    # TODO 之后应该在数据库里面default这个picture_id
    db.session.add(user)
    db.session.commit()

    # 生成用户的图片存放文件
    user_id = User.query.filter_by(email=email).first().user_id
    origin_path = f'/static/user/{user_id}/origin'
    process_path = f'/static/user/{user_id}/process'

    # 增加用户的文件夹
    if not os.path.exists(origin_path):
        os.makedirs(origin_path)
    if not os.path.exists(process_path):
        os.makedirs(process_path)

    return jsonify(code=200, msg='用户注册成功')


@bp.route('/login', methods=['POST'])
def user_login():
    """视图函数--用户登录的后台检测

    :arg
     email:用户输入的邮箱账号
     password:用户输入的密码

    :return:
     code 返回的HTTP状态码
     msg  返回的消息数据
    """
    # 接收参数
    json_data = request.get_json()
    email = json_data.get('email')
    password = json_data.get('password')

    # 参数接收有误
    if not all([email, password]):
        return jsonify(
            {
                "code": 400,
                'msg': '请求参数错误',
            }
        ), 400

    # 用户输入数据的检测
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify(
            {
                "code": 404,
                'msg': '用户未找到',
                'verification': {
                    'account': False,
                }
            }
        ), 200
    if check_password_hash(user.user_password, password):
        session['user_id'] = user.user_id
        print(session.get('user_id'))
        response = jsonify(
            {
                "code": 200,
                'msg': '用户登录成功!',
                'verification': {
                    'account': True,
                    'password': True,

                },
                'user_id': user.user_id
            }
        )
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response
    else:
        return jsonify(
            {
                "code": 403,
                'msg': '密码错误',
                'verification': {
                    'account': True,
                    'password': False
                }
            }
        ), 200


@bp.route('/logout', methods=['GET'])
def user_logout():
    """视图函数--用户退出登录

    :return:
     code 返回的HTTP状态码
     msg  返回的消息数据
    """
    # 清除用户的相关数据
    session.clear()
    return jsonify(code=200, msg='成功退出账户')


@bp.route('/<int:user_id>', methods=['GET', 'POST'])
def return_information(user_id: int):
    """ 视图函数--返回用户的个人信息

    :param user_id: 用户的id号
    :return:
        code 返回的HTTP状态码
        msg  返回的消息数据
        data 返回的个人信息数据
    """
    # user_id = session.get('user_id')
    # if 'user_id' in request.args:
    #     user_id = request.args.get('user_id')

    # 数据库查询用户
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        print('空用户错误!')
        return jsonify(code=400, msg=f'错误!id为{user_id}用户不存在!'), 400

    # 获取用户信息
    email = user.email
    user_name = user.user_name
    sex = user.sex
    tel = user.telephone
    avatar = user.head.head_picture_path
    return jsonify(
        {
            'code': 200,
            'msg': '成功返回个人信息',
            'data': {
                'email': email,
                'user_name': user_name,
                'sex': sex,
                'telephone': tel,
                'avatar_url': avatar,
            }
        }
    )


@bp.post('/')
def change_information():
    """ 视图函数--更改用户的个人信息

    :arg
        user_id:用户的id号
        sex: 用户的性别
        telephone: 用户的手机号码
        user_name: 用户的姓名
    :return:
        code 返回的HTTP状态码
        msg  返回的消息数据
    """
    # 获取数据
    user_id = session.get('user_id')
    personal_data = request.get_json()
    if 'user_id' in personal_data:
        user_id = personal_data.get('user_id')
    if not user_id:
        return jsonify(code=400, msg='用户id为空'), 400
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify(code=400, msg=f'用户id为{user_id}的用户不存在'), 400

    # 获取更改数据
    sex = user.sex
    if 'sex' in personal_data:
        sex = personal_data.get('sex')
    tele = user.telephone
    if 'telephone' in personal_data:
        tele = personal_data.get('telephone')
    user_name = user.user_name
    if 'username' in personal_data:
        user_name = personal_data.get('username')

    # 更改存入数据库
    user.sex = sex
    user.telephone = tele
    user.user_name = user_name
    db.session.add(user)
    db.session.commit()
    return jsonify(code=200, msg=f'成功修改个人用户{user}的信息')


@bp.post('/update_head_picture')
def change_head_picture():
    """ 视图函数--更改头像"""
    user_id = session.get('user_id')
    if len(request.files) == 0:
        print("文件是空的!!!")
        return jsonify(code=400, msg='empty picture'), 400
    for file in request.files.values():
        head = file
        name = file.filename
        print(name)
        allow_suffix = ['png', 'jpg', 'PNG', 'JPG']
        if name.split('.')[1] not in allow_suffix:
            return jsonify(code=400, msg='error files'), 400
        directory = os.getcwd()
        path = '/static/user/avatar'
        if not os.path.exists(directory + path):
            os.makedirs(directory + path)
        path = path + '/' + str(user_id) + '_' + name
        user = User.query.filter_by(user_id=user_id).first()
        if user.head:
            head_data = user.head
        else:
            return jsonify(code=400, msg=f'用户{user_id}的头像有误'), 400
        old_path = directory + head_data.head_picture_path
        head_data.head_picture_path = path
        db.session.add(head_data)
        db.session.commit()
        if head_data.head_picture_id != 1:
            os.remove(old_path)
        head.save(directory + path)
        return jsonify(code=200, msg="成功修改头像", path=path)


@bp.post('/verify_email')
def email_check():
    user_id = session.get('user_id')
    if 'user_id' in request.get_json().get('user_id'):
        user_id = request.get_json().get('user_id')
    user = User.query.filter_by(user_id=user_id).first()
    email = user.email
    email_code = send_mail(email)
    return jsonify(code=200, msg='成功发送邮件', email_code=email_code)


@bp.post('/forget_password')
@bp.post('/change_password')
def change_password():
    user_id = session.get('user_id')
    new_data = request.get_json()
    new_pwd = new_data.get('password')
    user = User.query.filter_by(user_id=user_id).first()
    user.user_password = generate_password_hash(new_pwd)
    db.session.add(user)
    db.session.commit()
    return jsonify(code=200, msg='成功修改密码')


@bp.delete('/')
def del_user():
    """ 视图函数--用户注销

    :return
        code 返回的HTTP状态码
        msg  返回的消息数据
    """
    user_id = session.get('user_id')
    user = User.query.filter_by(user_id=user_id)
    try:
        for p in [user.old_images, user.new_images]:
            os.remove(os.getcwd() + p.picture_path)
    except OSError:
        return jsonify(code=400, msg='用户图库的路径有误')
    db.session.delete(user)
    db.session.commit()
    return jsonify(code=200, msg='用户已经成功的注销')
