from flask import Flask, request, render_template, redirect, url_for, make_response, session
import DB_Conn_Try

app = Flask(__name__)
app.secret_key = 'fkdjsafjdkfdlkjfadskjfadskljdsfklj'


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


#------------------------------------------------------------------------------------------------
#--------------------------------------Using cookies---------------------------------------------
#------------------------------------------------------------------------------------------------
@app.route('/user_cookies', methods=['GET', 'POST'])
def user_cookies():
    user_id = request.form.get('user_id')
    user_pass = request.form.get('password')
    if DB_Conn_Try.add_account(user_id, user_pass):
        resp = make_response(render_template('user.html', user_id = user_id))
        resp.set_cookie('user_id', user_id)
        return resp
    else:
        return "Add account Fail"


@app.route('/edit_cookies', methods=['POST'])
def edit_user_cookies():
    new_username = request.form.get('username')
    print(new_username)
    user_id = request.cookies.get('user_id')
    print(user_id)
    if DB_Conn_Try.edit_account(user_id, new_username):
        return render_template('user.html', user_id = user_id)
    else:
        return "Edit account Fail"


@app.route('/login_cookies', methods=['POST'])
def login_cookies():
    user_id = request.form.get('user_id')
    user_pass = request.form.get('password')
    if DB_Conn_Try.password_match(user_id, user_pass):
        resp = make_response(render_template('user.html', user_id = user_id))
        resp.set_cookie('user_id', user_id)
        return resp
    else:
        return "Login Fail"

#------------------------------------------------------------------------------------------------
#--------------------------------------Using sessions---------------------------------------------
#------------------------------------------------------------------------------------------------
@app.route('/user_sessions', methods=['GET', 'POST'])
def user_sessions():
    user_id = request.form.get('user_id')
    user_pass = request.form.get('password')
    if DB_Conn_Try.add_account(user_id, user_pass):
        session['user_id'] = user_id
        return render_template('user.html', user_id = user_id)
    else:
        return "Add account Fail"


@app.route('/edit_sessions', methods=['POST'])
def edit_user_sessions():
    user_id = session['user_id']
    new_username = request.form.get('username')
    print(new_username)
    print(user_id)
    if DB_Conn_Try.edit_account(user_id, new_username):
        return render_template('user.html', user_id = user_id)
    else:
        return "Edit account Fail"


@app.route('/login_sessions', methods=['POST'])
def login_sessions():
    user_id = request.form.get('user_id')
    user_pass = request.form.get('password')
    if DB_Conn_Try.password_match(user_id, user_pass):
        session['user_id'] = user_id
        return render_template('user.html', user_id = user_id)
    else:
        return "Login Fail"





if __name__ == '__main__':
    app.run(debug=True)
