from application.view import personal, auth, picture
from application import app


app.register_blueprint(auth.bp)
app.register_blueprint(personal.bp)
app.register_blueprint(picture.bp)


@app.route('/', methods=['GET', 'POST'])
def hello_world():  # put application's code here
    return "hello-world"


if __name__ == '__main__':
    app.run()
