from flask import Flask, render_template, request, url_for, redirect
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from user import User
from mockdbhelper import MockDBHelper as DBHelper
from passwordhelper import PasswordHelper

app = Flask(__name__)
app.secret_key = 'THIS IS A SECRET KEY!'
login_manager = LoginManager(app)
DB = DBHelper()
PH = PasswordHelper()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/account')
@login_required
def account():
    return "You are logged in"


@app.route('/login', methods=['POST', 'GET'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    # user_password = DB.get_user(email)
    stored_user = DB.get_user(email)
    # if user_password == password:
    if stored_user and PH.validate_password(password,
                                            stored_user['salt'],
                                            stored_user['hashed']):
        user = User(email)
        login_user(user, remember=True)
        return redirect(url_for('account'))
    return home()


@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    email = request.form.get('email')
    pw1 = request.form.get('password')
    pw2 = request.form.get('password2')
    if not pw1 == pw2:
        return redirect(url_for('home'))
    if DB.get_user(email):
        return redirect(url_for('home'))
    salt = PH.get_salt()
    hashed = PH.get_hash(pw1 + salt)
    DB.add_user(email, salt, hashed)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
