#!/usr/bin/env python3.7

import sys
import pickle
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

    user = (username, sha3_512(password.encode()).hexdigest())

    try:
        with open('db/users.db', 'rb') as db_file:
            db = pickle.load(db_file)
            if user in db:
                return True

    except (EOFError, FileNotFoundError):
        create_default_user()

    return False


def create_default_user():
    '''
    DB lookup goes here
    please don't hard-code credentials
    '''

    db_folder = Path('db')
    if not db_folder.is_dir():
        db_folder.mkdir(exist_ok=True)

    with open('db/users.db', 'wb') as db_file:

        db = set()

        default_username = 'admin'
        default_password = ''.join(random.choices(string.ascii_letters + string.digits, k=14))

        db.add((default_username, sha3_512(default_password.encode()).hexdigest()))
        pickle.dump(db, db_file)

        sys.stderr.write('[+] Created default user:\n')
        sys.stderr.write('      - Username: {}\n'.format(default_username))
        sys.stderr.write('      - Password: {}\n'.format(default_password))