from flask_sqlalchemy import SQLAlchemy
import os
import traceback
import configparser

db = SQLAlchemy()

def init_database(app, config, project_dir):
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.getboolean('Database', 'SQLALCHEMY_TRACK_MODIFICATIONS')
    if config.get('Database', 'db_system') == 'sqlite':
        db_url = 'sqlite:///' + os.path.join(project_dir, config.get('sqlite', 'db_name'))
    elif config.get('Database', 'db_system') == 'mysql':
        db_url = config.get('mysql', 'url')
    else:
        raise Exception('cannot read Database.db_system config')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    with app.app_context():
        db.init_app(app)
        db.create_all()
        db.session.commit()

class user_data(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    fullname = db.Column(db.String(80))
    is_admin = db.Column(db.Boolean, nullable=False)

    def __init__(self, user_name, user_pass):
        self.username = user_name
        self.password = user_pass
        self.is_admin = False

def add_account(user_name, user_pass):
    try:
        db.session.add(user_data(user_name, user_pass))
        db.session.commit()
        print(user_name + ' added to DB')
        return True
    except:
        traceback.print_exc()
        return False

def edit_fullname(user_name, new_fullname):
    try:
        user_data.query.filter(user_data.username == user_name).update({user_data.fullname: new_fullname})
        db.session.commit()
        print(user_name + ' changed name to ' + new_fullname)
        return True
    except:
        traceback.print_exc()
        return False

def password_match(user_name, user_pass):
    match_case_count = user_data.query.filter(user_data.username == user_name, user_data.password == user_pass).count()
    return (match_case_count > 0)

def get_user_name_list():
    user_name_list = []
    for data in user_data.query.all():
        user_name_list.append(data.username)
    #print(user_name_list)
    return user_name_list

def delete_user(user_name):
    user_data.query.filter(user_data.username == user_name).delete()
    db.session.commit()
    print(user_name + ' delete')
    return True

def get_user_is_admin(user_name):
    is_admin = user_data.query.filter(user_data.username == user_name).one().is_admin
    return is_admin

def get_user_id(user_name):
    return user_data.query.filter(user_data.username == user_name).one().id

def get_user_data_list():
    return user_data.query.all()

def group_set_user_is_admin(user_name_list):
    user_data.query.filter(user_data.username != 'root').update({user_data.is_admin: False}, synchronize_session=False)
    user_data.query.filter(user_data.username.in_(user_name_list)).update({user_data.is_admin: True}, synchronize_session=False)
    db.session.commit()
    return True
