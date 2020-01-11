#!/usr/bin/env python3

# by TheTechromancer

import sys
import json
import random
import string
from pathlib import Path
from hashlib import sha512
import logging as loggingWHY
from flask_login import login_manager

# set up logging
log = loggingWHY.getLogger('credshed.gui')
log.setLevel(loggingWHY.DEBUG)


class User:

    def __init__(self, user_id=66666666666666666666666666, username='anonymous'):

        self.is_authenticated = False
        self.is_active = False
        self.is_anonymous = True
        self.id = user_id
        self.username = username


    def get_id(self):

        return str(self.id)



def validate_login(form):

    user = User()

    # if parameters exist
    if all([p in form for p in ['username', 'password']]):
        username = form['username']
        password = form['password']
        # and values are sensible
        if username.isalnum() and len(password) > 0:
            # and creds are valid
            user = user_lookup(username, password)
    
    if user.is_anonymous:
        log.warning('Invalid login by username "{}"'.format(str(username)))

    return user



def user_lookup(username, password):
    '''
    DB lookup goes here
    please don't hard-code credentials
    '''

    user = User()

    password_hash = sha512(password.encode()).hexdigest()

    try:
        with open('db/users.db', 'r') as db_file:
            db = json.load(db_file)
            if username in db:
                if db[username][1] == password_hash:
                    user_id = db[username][0]
                    user = User(user_id, username)
                    user.is_authenticated = True
                    user.is_active = True
                    user.is_anonymous = False

    except (EOFError, FileNotFoundError):
        default_username, default_password = create_default_user()
        sys.stderr.write('[+] Created default user:\n')
        sys.stderr.write('      - Username: {}\n'.format(default_username))
        sys.stderr.write('      - Password: {}\n'.format(default_password))

    # return anonymous user if failed
    
    return user


def user_lookup_by_id(lookup_user_id):

    lookup_user_id = int(lookup_user_id)
    user = User()

    with open('db/users.db', 'r') as db_file:
        db = json.load(db_file)
        for (username, (user_id, password_hash)) in db.items():
            user_id = int(user_id)
            if lookup_user_id == user_id:
                user = User(user_id, username)
                user.is_authenticated = True
                user.is_active = True
                user.is_anonymous = False
                break

    # return anonymous user if not found
    return user


def create_default_user():

    db_folder = Path('db')
    db_folder.mkdir(exist_ok=True)

    with open('db/users.db', 'w') as db_file:

        db = dict()

        # admin / random 14-character password
        default_username = 'admin'
        default_password = ''.join(random.choices(string.ascii_letters + string.digits, k=14))

        db[default_username] = (0, sha512(default_password.encode()).hexdigest())
        json.dump(db, db_file)

    return (default_username, default_password)



def get_secret_key():

    db_folder = Path('db')
    db_folder.mkdir(exist_ok=True)

    try:
        with open(str(db_folder / 'flask_secret.key'), 'rb') as f:
            secret_key = f.read()
            if len(secret_key) != 32:
                raise EOFError

    except (FileNotFoundError, EOFError):
        with open(str(db_folder / 'flask_secret.key'), 'wb') as f:
            # random 32-character secret
            secret_key = ''.join(random.choices(string.ascii_letters + string.digits, k=32)).encode()
            f.write(secret_key)

    return secret_key