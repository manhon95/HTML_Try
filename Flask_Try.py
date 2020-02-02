from flask import Flask, request, render_template, redirect, url_for, make_response, session, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import DB_Conn_Try
import os

#-------------------------------------Init----------------------------------------
app = Flask(__name__)
app.secret_key = os.urandom(16)

login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'home'

class User(UserMixin):
    pass

@login_manager.user_loader  
def user_loader(user_id):
    if user_id not in DB_Conn_Try.get_user_id_list()[1]:
        return None
    user = User()
    user.id = user_id
    return user


#-------------------------------------App-----------------------------------------


@app.route('/', methods=['GET'])
def handle():
    return redirect(url_for('home'))


@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/sign_up', methods=['POST'])
def sign_up():
    user_id = request.form.get('user_id')
    user_pass = request.form.get('password')
    if DB_Conn_Try.add_account(user_id, user_pass):
        user = User()
        user.id = user_id
        login_user(user)
        flash('New account created successfully.')
        return redirect(url_for('home'))
    else:
        return "Add account Fail"


@app.route('/login', methods=['POST'])
def login():
    user_id = request.form.get('user_id')
    user_pass = request.form.get('password')
    if DB_Conn_Try.password_match(user_id, user_pass):
        user = User()
        user.id = user_id
        login_user(user)
        flash('Logged in successfully.')
        return redirect(url_for('home'))
    else:
        return "Login Fail"


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    print('logout')
    print(current_user.id + ' logout')
    logout_user()
    return redirect(url_for('home'))


@app.route('/delete', methods=['GET'])
@login_required
def delete_user():
    DB_Conn_Try.delete_user(current_user.id)
    logout_user()
    return redirect(url_for('home'))


@app.route('/user_edit', methods=['GET', 'POST'])
@login_required
def user_edit():
    if request.method == 'GET':
        return render_template('user_edit.html')
    user_name = request.form.get('user_name')
    DB_Conn_Try.edit_account(current_user.id, user_name)
    return render_template('user_edit.html')


@app.route('/view_data', methods=['GET', 'POST'])
@login_required
def view_data():
    if request.method == 'GET':
        return 'somedata'


#-------------------------------------Run-----------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
