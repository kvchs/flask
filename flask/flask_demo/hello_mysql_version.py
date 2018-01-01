from flask import Flask
from flask import request
from flask import make_response
from flask import redirect
from flask import abort
from flask_script import Manager
from flask_moment import Moment
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from datetime import datetime
#from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import session, redirect, url_for, flash
import os
import _mysql
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


#ENGINE=create_engine("mysql+pymysql://root@127.0.0.1:3306/digchouti?charset=utf8", max_overflow=5)
engine = create_engine('mysql+pymysql://root:123456@localhost/data_charley', encoding='utf-8', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
sql_session = Session()



#Base.metadata.create_all(engine)
# basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# app.config['SQLALCHEMY_COMMIN_ON_TEARDOWN'] = True
# db = SQLAlchemy(app)
app.config['SECRET_KEY'] = "this is my secret"
#manager = Manager(apppp)
#app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get("name")
        if old_name is not None and old_name != form.name.data:
            flash("Looks like you have changed your name!")
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get("name"))


# @app.route('/user/<id>')
# def get_user(id):
#     user = load_user(id)
#     if not user:
#         abort(404)
#     return '<h2>Hello ,%s<h2>' % user.name


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_find(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


class NameForm(FlaskForm):
    name = StringField("what is your name?", validators=[DataRequired()])
    submit = SubmitField('Submit')


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)


    def __repr__(self):
        return '<Role %r>' % self.name


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, index=True)

    def __repr__(self):
        return '<User %r>' % self.username


# user = User(id='2', username="charley")
# sql_session.add(user)
# sql_session.commit()



if __name__ == "__main__":
    app.run(debug=True)