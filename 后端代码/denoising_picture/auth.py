from flask import Blueprint, request, jsonify
from init import db, send_mail
from sqlalchemy import text

bp = Blueprint('auth', __name__)


@bp.route('/register_email', methods=['POST'])
def register():  # put application's code here
    register_data = request.get_json()
    email = register_data.get('email')

    # 检查数据库email是否有相同
    cursor = db.session.execute(text("select COUNT(*) as num from t_user where email = :email"),
                                {'email': email}).fetchone()
    nums = cursor[0]
    same_email = True if nums == 0 else False
    # 发送email到对应邮箱之中
    code = 000000
    if same_email != 0:
        code = send_mail(email)
    callback = {
        'code': code,
        'email_use': same_email
    }
    return jsonify(callback)
