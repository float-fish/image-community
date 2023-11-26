from smtplib import SMTPDataError
from .user_personal.Userclass import UserSystem
from flask import Blueprint, request, jsonify, session, g
from application import db, send_mail
from werkzeug.security import generate_password_hash, check_password_hash
from ..model import User
import os

bp = Blueprint('auth', __name__, url_prefix='/user')

user_system = UserSystem()


@bp.route('/register_email', methods=['POST'])
def register_email():  # put application's code here
    register_data = request.get_json()
    email = register_data.get('email')
    # 检测请求格式
    if not email:
        return jsonify(code=400, msg='登录请求参数不完整'), 400
    [code, msg, mail_code] = user_system.mail_verify(email)
    return jsonify(code=code, msg=msg, mail_code=mail_code), code


@bp.route('/register', methods=['POST'])
def register():
    # 接收参数
    json_data = request.get_json()
    email = json_data.get('email')
    username = json_data.get('username')
    password = json_data.get('password')
    if not all([email, password, username]):
        return jsonify(code=400, msg='登录请求参数不完整'), 400

    # 添加用户进入数据库
    user = User(email=email, user_name=username, user_password=generate_password_hash(password), head_picture_id=1)
    # TODO 之后应该在数据库里面default这个picture_id
    db.session.add(user)
    db.session.commit()


    # origin_path = f'\\static\\user\\{user_id}\\'
    # 增加用户的文件夹
    # if not os.path.exists()

    return jsonify(code=200, msg='用户注册成功')


@bp.route('/login', methods=['POST'])
def user_login():
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

    # 用户检测
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
        ), 404
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
        ), 403


@bp.route('/logout', methods=['GET'])
def user_logout():
    session.clear()
    return jsonify(code=200, msg='成功退出账户')


@bp.get('/')
def return_information():
    email = session.get('email')
    user_name = session.get('user_name')
    sex = session.get('sex')
    tel = session.get('telephone')
    avatar = session.get('head_picture')

    return jsonify(
        {
            'code': 200,
            'msg': '成功返回个人信息',
            'data': {
                'email': email,
                'user_name': user_name,
                'sex': sex,
                'telephone': tel,
                'url': avatar,
            }
        }
    )


@bp.post('/')
def change_information():
    user_id = session.get('user_id')
    personal_data = request.get_json()
    if 'sex' in personal_data:
        sex = personal_data.get('sex')
    if 'telephone' in personal_data:
        tele = personal_data.get('telephone')
    if 'username' in personal_data:
        user_name = personal_data.get('username')

    user_information = User.query.filter_by(user_id=user_id).first()
    # TODO: 应该要有分别更改的选项
    user_information.sex = sex
    user_information.telephone = tele
    user_information.user_name = user_name
    db.session.add(user_information)
    db.session.commit()
    return jsonify(code=200, msg='成功修改个人信息')


@bp.post('/update_head_picture')
def change_head_picture():
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
        path = '\\static\\user\\avatar'
        if not os.path.exists(directory + path):
            os.makedirs(directory + path)
        path = path + '\\' + str(user_id) + '_' + name
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


@bp.get('/verify_email')
def email_check():
    user_id = session.get('user_id')
    user = User.query.filter_by(user_id=user_id).first()
    email = user.email
    email_code = send_mail(email)
    return jsonify(code=200, msg='成功发送邮件', email_code=email_code)


@bp.post('/changepassword')
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
    user_id = session.get('user_id')
    user = User.query.filter_by(user_id=user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(code=200, msg='用户已经成功的注销')
