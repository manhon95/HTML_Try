from flask import Flask, request, render_template, redirect, url_for, make_response, session, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import DB_Conn_Try
import os
import configparser

project_dir = os.path.abspath(os.path.dirname(__file__))
config = configparser.ConfigParser()
config.read('config.ini')

#-------------------------------------Init flask app----------------------------------------
app = Flask(__name__)
app.secret_key = os.urandom(16)

DB_Conn_Try.init_database(app, project_dir)

login_manager = LoginManager(app)
login_manager.session_protection = config.get('Login_Manager', 'session_protection')
login_manager.login_view = 'home' #unauthenticated user will redirect to home() if they access to @login_required page

class User(UserMixin):
    #'User' class inherits 'UserMixin' class from flask-login which contain 4 properties and method:is_authenticated, is_active, is_anonymous and get_id()
    def __init__(self):
        self.is_admin = False #here we add a new property is_admin to identify if a user is admin or not
    pass

@login_manager.user_loader  
def user_loader(user_name):
    if user_name not in DB_Conn_Try.get_user_name_list():    #if user_name is not in our database
        print('user loadfail')
        return None
    user = User()                                           #else create a new user object and initialize its name, id and is_admin properties
    user.id = user_name                                     #flask-login module must use user.id as identification, user.name will return error
    user.is_admin = DB_Conn_Try.get_user_is_admin(user_name)
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
    user_name = request.form.get('user_name')
    user_pass = request.form.get('password')
    user_pass2 = request.form.get('password2')
    try:
        user_name_list = DB_Conn_Try.get_user_name_list()
        sign_up_requirements = {'Username is already used!': (user_name not in user_name_list),     #login fail if Current user_name list already contain the new user_name
                                'Password not match!': (user_pass == user_pass2)}                   #login fail if 'password' field not match 'confirm password' field
        if all(sign_up_requirements.values()):
                DB_Conn_Try.add_account(user_name, user_pass)
                user = User()
                user.id = user_name
                login_user(user)
                flash('New account created successfully.')
        else:
            fail_msg = ''
            for req in sign_up_requirements:
                if not sign_up_requirements[req]:
                    fail_msg += req + '\n'
            flash(fail_msg)
    except Exception as e:
        print(e)
        flash('Cannot create account')
    return redirect(url_for('home'))


@app.route('/login', methods=['POST'])
def login():
    user_name = request.form.get('user_name')
    user_pass = request.form.get('password')
    try:
        if DB_Conn_Try.password_match(user_name, user_pass):
            user = User()
            user.id = user_name
            login_user(user)
            flash('Logged in successfully!')
        else:
            flash('Incorrect username/password!')
    except Exception as e:
        print(e)
        flash('Logged in fail!')
    return redirect(url_for('home'))


@app.route('/logout', methods=['GET'])
@login_required
def logout():                                       #TODO: try and print error msg
    print(current_user.id + ' logout')
    logout_user()
    flash('You logged out!')
    return redirect(url_for('home'))


@app.route('/delete', methods=['GET'])
@login_required
def delete_user():                                  #TODO: try and print error msg
    print(current_user.id + ' deleted')
    DB_Conn_Try.delete_user(current_user.id)        
    logout_user()
    flash('Account deleted!')
    return redirect(url_for('home'))


@app.route('/user_edit', methods=['GET', 'POST'])
@login_required
def user_edit():
    if request.method == 'GET':
        return render_template('user_edit.html')    
    new_fullname = request.form.get('fullname')
    if DB_Conn_Try.edit_fullname(current_user.id, new_fullname):
        flash('Changed fullname to ' + new_fullname + '!')
    else:
        flash('Changed fail.')
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
