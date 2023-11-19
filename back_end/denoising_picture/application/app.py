from application.view import personal, auth
from . import app

app.register_blueprint(auth.bp)
app.register_blueprint(personal.bp)


@app.route('/', methods=['GET', 'POST'])
def hello_world():  # put application's code here
    # print(send_mail('3242295133@qq.com'))
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
