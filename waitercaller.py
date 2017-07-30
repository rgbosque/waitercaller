import config
from flask import Flask, render_template, request, url_for, redirect
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user

from user import User
from mockdbhelper import MockDBHelper as DBHelper
from passwordhelper import PasswordHelper
from bitlyhelper import BitlyHelper

from forms import RegistrationForm, LoginForm, CreateTableForm, DeleteTableForm

app = Flask(__name__)
app.secret_key = 'THIS IS A SECRET KEY!'  # use for add-on
login_manager = LoginManager(app)
DB = DBHelper()
PH = PasswordHelper()
BH = BitlyHelper()


@app.route('/')
def home():
    return render_template("home.html", loginform=LoginForm(), registrationform=RegistrationForm())


@app.route('/login', methods=['POST'])
def login():
    form = LoginForm(request.form)
    if form.validate():
        stored_user = DB.get_user(form.loginemail.data)
        if stored_user and PH.validate_password(form.loginpassword.data,
                                                stored_user['salt'],
                                                stored_user['hashed']):
            user = User(form.loginemail.data)
            login_user(user, remember=True)
            return redirect(url_for('account'))
        form.loginemail.errors.append("Email or password invalid")
    return render_template("home.html", loginform=form, registrationform=RegistrationForm())

    #
    # email = request.form.get('email')
    # password = request.form.get('password')
    # stored_user = DB.get_user(email)
    # if stored_user and PH.validate_password(password,
    #                                         stored_user['salt'],
    #                                         stored_user['hashed']):
    #     user = User(email)
    #     login_user(user, remember=True)
    #     return redirect(url_for('account'))
    # return home()


@login_manager.user_loader
def load_user(user_id):
    ''' This callback is used to reload the user object
        from the user ID stored in the session '''

    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        if DB.get_user(form.email.data):
            form.email.errors.append("Email address already registered")
            return render_template('home.html', loginform=LoginForm(), registrationform=form)
        salt = PH.get_salt()
        hashed = PH.get_hash(form.password2.data + salt)
        DB.add_user(form.email.data, salt, hashed)
        return render_template("home.html", loginform=LoginForm(), registrationform=form,
                               onloadmessage="Registration successfull. Please log in.")

        # return redirect(url_for("home"))
    # return render_template("home.html", registrationform=form)
    return render_template("home.html", loginform=LoginForm(), registrationform=form)
    # email = request.form.get('email')
    # pw1 = request.form.get('password')
    # pw2 = request.form.get('password2')
    # if not pw1 == pw2:
    #     return redirect(url_for('home'))
    # if DB.get_user(email):
    #     return redirect(url_for('home'))
    # salt = PH.get_salt()
    # hashed = PH.get_hash(pw1 + salt)
    # DB.add_user(email, salt, hashed)
    # return redirect(url_for('home'))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/account")
@login_required
def account():
    tables = DB.get_table(current_user.get_id())
    return render_template("account.html",
                           createtableform=CreateTableForm(),
                           deletetableform=DeleteTableForm(),
                           tables=tables)


@app.route("/account/createtable", methods=['POST'])
@login_required
def account_createtable():
    form = CreateTableForm(request.form)
    if request.method == "POST" and form.validate():
        tableid = DB.add_table(form.tablenumber.data, current_user.get_id())
        new_url = BH.shorten_url(config.base_url + "newrequest/" + tableid)
        DB.update_table(tableid, new_url)
        return redirect(url_for('account'))

    return render_template('account.html',
                           deletetableform=DeleteTableForm(),
                           createtableform=form,
                           tables=DB.get_table(current_user.get_id()))
    # tablename = request.form.get("tablenumber")
    # tableid = DB.add_table(tablename, current_user.get_id())
    # long_url = config.base_url + "newrequest/" + tableid
    # new_url = BH.shorten_url(long_url)
    # DB.update_table(tableid, new_url)
    #
    # return redirect(url_for('account'))


@app.route("/account/deletetable", methods=["POST"])
@login_required
def account_deletetable():
    form = DeleteTableForm(request.form)
    print form.tableid.data
    if form.validate():
        DB.delete_table(form.tableid.data)
        return redirect(url_for('account'))
        # return render_template('account.html', deletetableform=form,
        # tables=DB.get_table(current_user.get_id()))

    return render_template('account.html',
                           createtableform=CreateTableForm(),
                           deletetableform=form,
                           tables=DB.get_table(current_user.get_id()))
    # tableid = request.args.get("tableid")
    # DB.delete_table(tableid)
    #
    # return redirect(url_for('account'))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
