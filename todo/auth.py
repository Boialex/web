import json
from flask import session, redirect
from functools import wraps

with open('user.json') as users_file:
    g_users = json.load(users_file)

def is_user_in_db(login):
    return login in g_users

class User:
    def __init__(self, login):
        if login is not None and login in g_users:
            self.login = login
            self.password = g_users[login]['password']
            self.authorized = False
        else:
            self.authorized = False
    
    def is_authorized(self):
        return self.authorized


def authorize(login, password):
    if not is_user_in_db(login):
        return User(None)
    u = User(login)
    if u.password == password:
        u.authorized = True
        return u
    else:
        return User(None)
        
def get_user(login):
    if not is_user_in_db(login):
        return User(None)
    u = User(login)
    u.authorized = True
    return u

def get_current_user():
    return get_user(session.get('user_login', None))

def authorized(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        login = session.get('user_login', None)
        u = get_user(login)
        if u.is_authorized():
            return fn(*args, **kwargs)
        else:
            return redirect('/login')
    return wrapped

def not_authorized(fn):
    @wraps(fn)
    def wrapped():
        login = session.get('user_login', None)
        u = get_user(login)
        if not u.is_authorized():
            return fn()
        else:
            return redirect('/')
    return wrapped