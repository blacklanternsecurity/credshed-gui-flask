#!/usr/bin/env python3.7

import sys
import json
import random
import string
from pathlib import Path
from hashlib import sha3_512
from flask_login import login_manager


class User:

    def __init__(self):

        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False


    def get_id(self):

        return '1'



def validate_login(form):

    valid_login = False

    # if parameters exist
    if all([p in form for p in ['username', 'password']]):
        username = form['username']
        password = form['password']
        # and values are sensible
        if username.isalnum() and len(password) > 0:
            # and creds are valid
            valid_login = user_lookup(username, password)
    
    if valid_login:
        sys.stderr.write('[+] Valid login:\n')
        sys.stderr.write('      - Username: {}\n'.format(username))
        sys.stderr.write('      - Password: {}\n'.format(password))
    else:
        sys.stderr.write('[+] Invalid login\n')

    return valid_login


def user_lookup(username, password):
    '''
    DB lookup goes here
    please don't hard-code credentials
    '''

    password_hash = sha3_512(password.encode()).hexdigest()

    try:
        with open('db/users.db', 'r') as db_file:
            db = json.load(db_file)
            if username in db:
                if db[username] == password_hash:
                    return True

    except (EOFError, FileNotFoundError):
        default_username, default_password = create_default_user()
        sys.stderr.write('[+] Created default user:\n')
        sys.stderr.write('      - Username: {}\n'.format(default_username))
        sys.stderr.write('      - Password: {}\n'.format(default_password))

    return False


def create_default_user():

    db_folder = Path('db')
    db_folder.mkdir(exist_ok=True)

    with open('db/users.db', 'w') as db_file:

        db = dict()

        # admin / random 14-character password
        default_username = 'admin'
        default_password = ''.join(random.choices(string.ascii_letters + string.digits, k=14))

        db[default_username] = sha3_512(default_password.encode()).hexdigest()
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

    print('SECRET KEY: {}'.format(str(secret_key)))
    return secret_key