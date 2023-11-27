# 从应用程序之中导入flask app
from application import app


# TODO 使用Migrate管理迁移数据库

@app.route('/', methods=['GET', 'POST'])
def hello_world():  # put application's code here
    """
    :return: "hello-world" 测试接口
    """
    return "hello-world"


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
