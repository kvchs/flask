from flask import Flask
from flask import request
from flask import make_response
from flask import redirect
from flask import abort
from flask_script import Manager

app = Flask(__name__)
#manager = Manager(apppp)
#app = Flask(__name__)


@app.route('/')
def index():
    return redirect("http://www.baidu.com")
    #abort(404)


@app.route('/user/<id>')
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return '<h2>Hello ,%s<h2>' % user.name


@app.route('/user/<name>')
def user(name):
    return "<h2>Hello,%s!</h2>" % name


if __name__ == "__main__":
    app.run(debug=True)