from flask import Flask, request, render_template
import DB_Conn_Try

app = Flask(__name__)

#網頁執行/say_hello時，會導至index.html
@app.route('/say_hello', methods=['GET'])
def getdata():
    return render_template('index.html')

#index.html按下submit時，會取得前端傳來的username，並回傳"Hello, World! "+name
@app.route('/say_hello', methods=['POST'])
def submit():
    name = request.form.get('username')
    if DB_Conn_Try.add_account(name):
        return "Hello, " + name
    else:
        return "Add account Fail"

def get_ac_info():
    return True

@app.route('/shutdown', methods=['GET'])
def shutdown():
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(debug=True)
