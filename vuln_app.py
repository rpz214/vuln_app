import hashlib
import os
import sqlite3

from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class login_form(FlaskForm):
    """login form for flask"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class user:
    # required for flask_login
    is_authenticated = True
    is_active = True
    is_anonymous = False

    def __init__(self, username):
        self.username = username

    def get_id(self):
        # required for flask_login
        return self.username


def get_hash(password):
    """Get sha512 hash"""
    # salting encourages safe sql queries so it is just avoided in this case
    sha512 = hashlib.sha512()
    password = password.encode('utf-8')
    sha512.update(password)
    return sha512.hexdigest()


app = Flask(__name__)
# key required for flask
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.db = 'vuln_app.db'
login = LoginManager(app)
login.login_view = 'login'
# reset db to default
if os.path.exists(app.db):
    os.remove(app.db)
# init db
with sqlite3.connect(app.db) as conn:
    c = conn.cursor()
    c.execute("CREATE TABLE posts(author TEXT, body TEXT)")
    c.execute("CREATE TABLE users(username TEXT, password TEXT)")
    c.execute("INSERT INTO posts VALUES('test', 'Test')")
    c.execute("INSERT INTO users VALUES('test', '{}')".format(get_hash('test')))
    conn.commit()

# TODO add post capability


@login.user_loader
def load_user(username):
    """load user by username"""
    return user(username)


@app.route('/')
@app.route('/index')
@login_required
def index():
    """home page for posts"""
    # test without full db integration
    posts = [
        {
            'author': {'username': 'test'},
            'body': 'No db test'
        }
    ]
    # TODO add db integration to posts
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """login page"""
    # this is an unsafe query
    queryFormat = 'SELECT * from users WHERE username = "{}" AND password = "{}"'
    # starting redirect
    rd = '/index'
    # redirect if authenticated already
    if current_user.is_authenticated:
        return redirect(rd)
    form = login_form()
    # form submitted
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        db = sqlite3.connect(app.db)
        result = db.execute(queryFormat.format(username, get_hash(password)))
        if result.fetchone():
            login_user(user(username))
        else:
            rd = '/login'
        db.close()
        return redirect(rd)
    # reached login page without submit
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    """logout function"""
    logout_user()
    return redirect('/index')
