from flask import Blueprint, request, jsonify, abort, session, send_file
from application import db, send_mail
from .. import model
import os

bp = Blueprint('personal', __name__, url_prefix='/user/<int:id>')


@bp.get('/')
def return_information(id: int):
    user_information = model.User.query.filter_by(user_id=id).first()
    if not user_information:
        abort(404)
    else:
        picturepath = user_information.head.head_picture_path
        return jsonify(
            {
                'code': 200,
                'msg': '成功返回个人信息',
                'data': {
                    'email': user_information.email,
                    'user_name': user_information.user_name,
                    'sex': user_information.sex,
                    'telephone': user_information.telephone,
                    'url': picturepath
                }
            }
        )


@bp.post('/')
def change_information(id: int):
    personal_data = request.get_json()
    sex = personal_data.get('sex')
    tele = personal_data.get('telephone')
    user_name = personal_data.get('username')
    user_information = model.User.query.filter_by(user_id=id).first()
    user_information.sex = sex
    user_information.telephone = tele
    user_information.user_name = user_name
    db.session.add(user_information)
    db.session.commit()
    return jsonify(code=200, msg='成功修改个人信息')


@bp.post('/update_head_picture')
def change_head_picture(id: int):
    head = request.files['image']
    name = request.files['image'].name
    path = os.getcwd() + f'/statics/user/{id}/avatar'
    if not os.path.exists(path):
        os.mkdir(path)
    path += name
    head.save(path)
    user = model.User.query.filter_by(user_id=id).first()
    head_data = user.head
    old_path = head_data.head_picture_path
    head_data.head_picture_path = path
    os.remove(old_path)
    db.session.add(head_data)
    db.session.commit()
    return jsonify(code=200, msg="成功修改头像")


@bp.get('/verify_email')
def check_email(id: int):
    user = model.User.query.filter_by(user_id=id).first()
    email = user.email
    email_code = send_mail(email)
    return jsonify(code=200, msg='成功发送邮件', email_code=email_code)


@bp.post('/changepassword')
def change_password(id: int):
    new_data = request.get_json()
    new_pwd = new_data.get('password')
    user = model.User.query.filter_by(user_id=id).first()
    user.user_password = new_pwd
    db.session.add(user)
    db.session.commit()
    return jsonify(code=200, msg='成功修改密码')
