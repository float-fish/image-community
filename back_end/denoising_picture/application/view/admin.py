from flask import Blueprint, session, jsonify, request
from .. import model, db
from werkzeug.security import check_password_hash

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.post('/login')
def admin_login():
    data = request.get_json()
    account = data.get('account')
    password = data.get('password')
    if not all([account, password]):
        return jsonify(code=400, msg='请求参数不完整'), 400
    admin = model.Admin.query.filter_by(admin_account=account).first()
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
        )
    if check_password_hash(admin.admin_password, password):
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
    session.clear()
    return jsonify(
        {
            "code": 200,
            "msg": "成功退出管理账号"
        }
    )


@admin_bp.post('user')
def admin_query_user():
    data = request.get_json()
    page = data.get('page')
    per_page = data.get('per_page')
    users = model.User.query.paginate(page=page, per_page=8)

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


@admin_bp.get('user/<int:user_id>')
def admin_query_byid(user_id: int):
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


@admin_bp.delete('user/<int:user_id>')
def admin_del_user(user_id: int):
    user = model.User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(code=200, msg="成功删除用户")


@admin_bp.post('user/<int:user_id>')
def admin_change_user(user_id: int):
    user = model.User.query.get(user_id)

