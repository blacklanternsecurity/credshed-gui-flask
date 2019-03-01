#!/usr/bin/env python3.7

# by TheTechromancer

# flask classes
import flask
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

import sys
from time import sleep
import lib.auth as auth



# create the application object
app = flask.Flask(__name__)
login_manager = LoginManager(app)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'oknbvcxzaq234rfvbnm,lo987yhbvcxzaq2345tgb'



@app.route('/')
def home():
    return flask.render_template('pages/home.html')



@app.route('/search', methods=['POST'])
def search():
    if flask.request.method == 'POST':
        return flask.render_template('pages/search_results.html', query=flask.request.form['query'])



@app.route('/admin')
@login_required
def admin():
    return flask.render_template('pages/admin.html')



@app.route('/login', methods=['GET', 'POST'])
def login():

    if flask.request.method == 'GET':
        return flask.render_template('pages/login.html')

    elif flask.request.method == 'POST':
        if auth.validate_login(flask.request.form):
            login_user(auth.User())
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
    return auth.User()



# start the server with the 'run()' method
if __name__ == '__main__':

    app.run(host='127.0.0.1', debug=True)