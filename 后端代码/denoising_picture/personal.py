from flask import Blueprint, request, jsonify
from init import db, send_mail
from sqlalchemy import text

bp = Blueprint('personal', __name__, url_prefix='/<int:user_id>')

bp.route('/<int:user_id>', methods=['POST'])


def change_information(user_id: int):
    personal_data = request.get_json()
    sex = personal_data['sex']
    tele = personal_data['telephone']


