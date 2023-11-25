from application import app


@app.route('/', methods=['GET', 'POST'])
def hello_world():  # put application's code here
    return "hello-world"


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
