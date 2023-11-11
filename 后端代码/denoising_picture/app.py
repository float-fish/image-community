from flask import jsonify, request
from sqlalchemy import text
from init import app, db, send_mail


@app.route('/', methods=['GET', 'POST'])
def hello_world():  # put application's code here
    # print(send_mail('3242295133@qq.com'))
    return 'Hello World!'


@app.route('/register_email', methods=['POST'])
def register():  # put application's code here
    register_data = request.get_json()
    email = str(register_data.get('email'))

    # 检查数据库email是否有相同
    cursor = db.session.execute(text("select COUNT(*) as num from t_user where email ='" + email+"'"))
    nums = cursor.fetchone()[0]
    print(nums)
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


if __name__ == '__main__':
    app.run()
