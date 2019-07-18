import hashlib
import os
import sqlite3

from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class login_form(FlaskForm):
    """login form for flask"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


def get_hash(password):
    """Get sha512 hash"""
    sha512 = hashlib.sha512()
    password = password.encode('utf-8')
    sha512.update(password)
    return sha512.hexdigest()


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.db = 'vuln_app.db'
# reset db to default
if os.path.exists(app.db):
    os.remove(app.db)
with sqlite3.connect(app.db) as conn:
    c = conn.cursor()
    c.execute("CREATE TABLE posts(author TEXT, body TEXT)")
    c.execute("CREATE TABLE users(username TEXT, password TEXT)")
    c.execute("INSERT INTO posts VALUES('test', 'Test')")
    c.execute("INSERT INTO users VALUES('test', '{}')".format(get_hash('test')))
    conn.commit()

# TODO add post capability
# TODO recognize when logged in or not


@app.route('/')
@app.route('/index')
def index():
    """home page for posts"""
    user = {'username': 'testuser'}
    # test without full db integration
    posts = [
        {
            'author': {'username': 'test'},
            'body': 'No db test'
        }
    ]
    # TODO add db integration to posts and user recognition
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """login page"""
    # this is an unsafe query
    queryFormat = 'SELECT * from users WHERE username = "{}" AND password = "{}"'
    form = login_form()
    # form submitted
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        db = sqlite3.connect(app.db)
        result = db.execute(queryFormat.format(username, get_hash(password)))
        if result.fetchone():
            rd = '/index'
        else:

            rd = '/login'
        db.close()
        return redirect(rd)
    # reached login page without submit
    return render_template('login.html', title='Login', form=form)
