#!/usr/bin/env python3.7

# by TheTechromancer

# flask classes
import flask
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

# cred shed
from lib.credshed import *

# other
import sys
from time import sleep
import lib.security as security



# create the application object
app = flask.Flask(__name__)
login_manager = LoginManager(app)

# secret key
app.secret_key = security.get_secret_key()



@app.route('/')
def home():
    if current_user.is_authenticated:
        return flask.redirect('/search')
    return flask.redirect('/login')


@login_required
@app.route('/search', methods=['GET', 'POST'])
def search():
    query = 'email or domain'
    if flask.request.method == 'GET':
        return flask.render_template('pages/search.html', query=query)
    elif flask.request.method == 'POST':
        credshed = CredShed()
        query = flask.request.form['query']
        results = '\n'.join([str(result) for result in credshed._search(query)])
        return flask.render_template('pages/search_results.html', query=query, results=results)



@login_required
@app.route('/admin')
def admin():
    return flask.render_template('pages/admin.html')



@app.route('/login', methods=['GET', 'POST'])
def login():

    if flask.request.method == 'GET':
        return flask.render_template('pages/login.html')

    elif flask.request.method == 'POST':
        if security.validate_login(flask.request.form):
            login_user(security.User())
            return flask.redirect('/')

        else:
            sleep(3)
            return flask.redirect('/login')



@app.route('/logout')
def logout():
    logout_user()
    return flask.redirect('/')


@login_manager.user_loader
def load_user(user_id):
    return security.User()


# start the server with the 'run()' method
if __name__ == '__main__':

    app.run(host='127.0.0.1', debug=True)