#!/usr/bin/env python3.11.4
""" 对前端页面实现管理员基本操作的api接口

Copyright 2023 Yu Shengjie.
License(GPL)
Author: Yu Shengjie
"""
import os

from flask import Blueprint, session, jsonify, request
from .. import model, db
from werkzeug.security import check_password_hash, generate_password_hash

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.post('/login')
def admin_login():
    """ 视图函数--管理员登录验证

    :arg
        account:管理员的账号
        password:管理员密码
    :return:
        code 返回的HTTP状态码
        msg  返回的消息数据
        status 用户登录的状态
         account 账户是否正确
         password 密码是否正确
    """

    # 获取数据
    data = request.get_json()
    account = data.get('account')
    password = data.get('password')
    if not all([account, password]):
        return jsonify(code=400, msg='请求参数不完整'), 400
    admin = model.Admin.query.filter_by(admin_account=account).first()

    # 检验管理员的账号密码是否匹配
    if not admin:
        return jsonify(
            {
                "code": 404,
                "msg": "未找到管理员账号",
                "status":
                    {
                        "account": False
                    }
            }
        ), 404
    if password == admin.admin_password:
        session['admin_name'] = admin.admin_name
        return jsonify(
            {
                "code": 200,
                "msg": "成功登录管理员账号",
                "status":
                    {
                        "account": True,
                        "password": True
                    }
            }
        )
    else:
        return jsonify(
            {
                "code": 403,
                "msg": "密码错误",
                "status":
                    {
                        "account": True,
                        "password": False
                    }
            }
        ), 403


@admin_bp.get('/logout')
def admin_logout():
    """ 视图函数--管理员登出

    :return:
        code 返回的HTTP状态码
        msg  返回的消息数据
    """
    session.clear()
    return jsonify(
        {
            "code": 200,
            "msg": "成功退出管理账号"
        }
    )


@admin_bp.route('/user', methods=['GET', 'POST'])
def admin_query_user():
    """ 视图函数--查询所有用户的信息

    :return:
        code 返回的HTTP状态码
        msg  返回的消息数据
        data 用户的信息
         user_id 用户的id
         user_name 用户名
         user_email 用户的邮箱
    """
    # data = request.get_json()
    # page = data.get('page')
    # users = model.User.query.paginate(page=page, per_page=8)

    # 获取所有用户数据
    users = model.User.query.all()

    users_id = []
    users_name = []
    users_email = []
    for user in users:
        users_id.append(user.user_id)
        users_name.append(user.user_name)
        users_email.append(user.email)

    return jsonify(
        {
            "code": 200,
            "msg": "成功返回用户列表",
            "data": {
                "users_id": users_id,
                "users_name": users_name,
                "users_email": users_email
            }
        }
    )


@admin_bp.post('/user/search')
def fuzzy_search():
    """ 视图函数--用户名的模糊搜索

    :arg
        user_name:前台提供的关键词
    :return:
        code 返回的HTTP状态码
        msg  返回的消息数据
        data 用户的信息
         user_id 用户的id
         user_name 用户名
         user_email 用户的邮箱
    """
    data = request.get_json()
    keyword = data.get('user_name')
    keyword = f'%{keyword}%'
    users = model.User.query.filter(model.User.user_name.like(keyword)).all()

    users_id = []
    users_name = []
    users_email = []
    for user in users:
        users_id.append(user.user_id)
        users_name.append(user.user_name)
        users_email.append(user.email)

    return jsonify(
        {
            "code": 200,
            "msg": "成功返回用户列表",
            "data": {
                "users_id": users_id,
                "users_name": users_name,
                "users_email": users_email
            }
        }
    )


@admin_bp.get('/user/<int:user_id>')
def admin_query_byid(user_id: int):
    """
    视图函数--管理查询具体用户的信息

    :param user_id: 用户的id号
    :return:
        code 返回的HTTP状态码
        msg  返回的消息数据
        data 用户的信息
         user_id 用户的id
         user_name 用户名
         user_email 用户的邮箱
    """
    user = model.User.query.get(user_id)
    user_id = user.user_id
    user_name = user.user_name
    user_email = user.email
    return jsonify(
        {
            "code": 200,
            "msg": "成功返回用户列表",
            "data": {
                "user_id": user_id,
                "user_name": user_name,
                "user_email": user_email
            }
        }
    )


@admin_bp.delete('/user/<int:user_id>')
def admin_del_user(user_id: int):
    """
    视图函数--管理员删除用户
    :param user_id:要删除用户的id号
    :return:
        code 返回的HTTP状态码
        msg  返回的消息数据
    """
    user = model.User.query.get(user_id)
    if not user:
        return jsonify(code=400, msg=f'用户号为{user_id}的用户不存在'), 400
    print([user.old_images, user.new_images])
    # try:
    #     for p in [user.old_images, user.new_images]:
    #         os.remove(os.getcwd() + p.picture_path)
    # except OSError:
    #     return jsonify(code=400, msg='用户图库的路径有误')
    db.session.delete(user)
    db.session.commit()
    return jsonify(code=200, msg="成功删除用户")


@admin_bp.post('/user/<int:user_id>')
def admin_change_user(user_id: int):
    """
    视图函数--管理员改变用户的信息
    :param user_id:用户的id号
    :return:
    """
    user = model.User.query.get(user_id)
    if not user:
        return jsonify(code=404, msg=f'找不到对应用户号为{user_id}的用户'), 404
    if request.is_json:
        data = request.get_json()
    else:
        return jsonify(code=400, msg='错误的数据类型!应该发送JSON数据'), 400
    user_name = user.user_name
    if 'user_name' in data:
        user_name = data.get('user_name')
    sex = user.sex
    if 'sex' in data:
        sex = data.get('sex')
    telephone = user.telephone
    if 'telephone' in data:
        telephone = data.get('telephone')
    user.user_name = user_name
    user.sex = sex
    user.telephone = telephone
    db.session.add(user)
    db.session.commit()
    return jsonify(code=200, msg=f'成功修改用户{user}的信息')


@admin_bp.post('user/setpassword/<int:user_id>')
def admin_setpassword(user_id: int):
    user = model.User.query.get(user_id)
    if not user:
        return jsonify(code=404, msg=f'找不到对应用户号为{user_id}的用户'), 404
    if request.is_json:
        data = request.get_json()
    else:
        return jsonify(code=400, msg='错误的数据类型!应该发送JSON数据'), 400
    password = data.get('password')
    password_hash = generate_password_hash(password)
    user.user_password = password_hash
    db.session.add(user)
    db.session.commit()
    return jsonify(code=200, msg=f'用户{user}密码已经成功修改')
