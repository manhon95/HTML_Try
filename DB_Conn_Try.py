import sqlite3

def add_account(user_id, user_pass):
    try:
        db = sqlite3.connect('DB_Try.db')
        db.execute("insert into account('ac_id', 'ac_pass') values (:user_id, :user_pass)", {'user_id':user_id, 'user_pass':user_pass})
        db.commit()
        db.close()
        print(user_id + ' added to DB')
        return True
    except:
        db.close()
        return False

def edit_account(user_id, new_username):
    db = sqlite3.connect('DB_Try.db')
    db.execute("update account set ac_name = :new_username where ac_id = :user_id", {'new_username':new_username, 'user_id':user_id})
    db.commit()
    db.close()
    print(user_id + ' changed name to ' + new_username)
    return True

def password_match(user_id, user_pass):
    db = sqlite3.connect('DB_Try.db')
    match_case_count = db.execute("select count(*) from account where ac_id = :user_id and ac_pass = :user_pass", {'user_id':user_id, 'user_pass':user_pass}).fetchall()[0][0]
    db.close()
    return (match_case_count > 0)

def get_user_name(user_id):
    db = sqlite3.connect('DB_Try.db')
    info = db.execute("select ac_name from account where ac_id = :user_id", {'user_id':user_id}).fetchall()
    print(user_id + ' get from DB')
    db.close()
    return True, info

def get_user_id_list():
    db = sqlite3.connect('DB_Try.db')
    user_id_list_raw = db.execute("select ac_id from account;").fetchall()
    user_id_list = []
    for user_id in user_id_list_raw:
        user_id_list.append(str(user_id[0]))
    print('user_id_list:')
    print(user_id_list)
    db.close()
    return True, user_id_list

def delete_user(user_id):
    db = sqlite3.connect('DB_Try.db')
    db.execute("delete from account where ac_id = :user_id", {'user_id':user_id})
    db.commit()
    db.close()
    print(user_id + ' delete')
    return True