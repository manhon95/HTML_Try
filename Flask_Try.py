from flask import Flask, request, render_template, redirect, url_for, make_response, session, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import DB_Conn_Try
import os
import ConfigParser
 
config = ConfigParser.ConfigParser()
config.read('Config.ini')

#-------------------------------------Init----------------------------------------
app = Flask(__name__)
app.secret_key = os.urandom(16) 

login_manager = LoginManager(app)
login_manager.session_protection = config.get('Login_Manager', 'session_protection')
login_manager.login_view = 'home' #unauthenticated user will redirect to home() if they access to @login_required page

class User(UserMixin):
    #'User' class inherits 'UserMixin' class from flask-login which contain 4 properties and method:is_authenticated, is_active, is_anonymous and get_id()
    def __init__(self):
        self.is_admin = False #here we add a new property is_admin to identify if a user is admin or not
    pass

@login_manager.user_loader  
def user_loader(user_id):
    if user_id not in DB_Conn_Try.get_user_id_list()[1]:    #if user_id is not in our database
        return None
    user = User()                                           #else create a new user object and initialize its id and is_admin properties
    user.id = user_id
    user.is_admin = DB_Conn_Try.check_user_is_admin(user_id)
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
    user_pass2 = request.form.get('password2')
    user_id_list = DB_Conn_Try.get_user_id_list()
    if user_id_list[0]:
        if user_id not in user_id_list[1]:                          #login fail if Current user_id list already contain the new user_id
            if user_pass == user_pass2:                             #login fail if 'password' field not match 'confirm password' field
                if DB_Conn_Try.add_account(user_id, user_pass):
                    user = User()
                    user.id = user_id
                    login_user(user)
                    #flash('New account created successfully.')
                    return redirect(url_for('home'))
    return "Add account Fail"


@app.route('/login', methods=['POST'])
def login():
    user_id = request.form.get('user_id')
    user_pass = request.form.get('password')
    if DB_Conn_Try.password_match(user_id, user_pass):
        user = User()
        user.id = user_id
        login_user(user)
        #flash('Logged in successfully.')
        return redirect(url_for('home'))
    return "Login Fail"


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    print(current_user.id + ' logout')
    logout_user()
    return redirect(url_for('home'))


@app.route('/delete', methods=['GET'])
@login_required
def delete_user():
    print(current_user.id + ' deleted')
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
        if current_user.is_admin:           #view_data will identify if user is admin or not and show respective result
            return 'someadmindata'
        return 'somedata'


#-------------------------------------Run-----------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
