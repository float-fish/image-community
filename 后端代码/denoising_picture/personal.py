from flask import Blueprint, request, jsonify, abort, session
from init import db, send_mail
from sqlalchemy import text

bp = Blueprint('personal', __name__, url_prefix='/user/<int:id>')


@bp.get('/')
def return_information(id: int):
    user_information = db.session.execute(text('select * from t_user where user_id = :user_id'),
                                          {'user_id': id}).fetchone()
    print(user_information)
    if not user_information:
        abort(404)
    else:
        return jsonify(
            {
                'code': 200,
                'message': 'success',
                'data': {
                    'email': user_information[2],
                    'user_name': user_information[4],
                    'sex': user_information[5],
                    'telephone': user_information[6]
                }
            }
        )


@bp.post('/')
def change_information(id: int):
    personal_data = request.get_json()
    sex = personal_data.get('')
    tele = personal_data['telephone']
