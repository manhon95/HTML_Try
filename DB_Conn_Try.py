import sqlite3

def add_account(username):
    db = sqlite3.connect('DB_Try.db')
    db.execute("insert into account('ac_name') values (:username)", {'username':username})
    db.commit()
    db.close()
    print(username + ' added to DB')
    return True

def get_account_info(username):
    db = sqlite3.connect('DB_Try.db')
    info = db.execute("select * from account where username = :username", {'username':username}).fetchall()
    print(username + ' get from DB')
    db.close()
    return True, info
