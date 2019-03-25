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


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():

    #if not current_user.is_authenticated:
    #    return flask.redirect('/login')

    if flask.request.method == 'GET':
        return flask.render_template('pages/search.html')

    elif flask.request.method == 'POST':

        query = 'email or domain'
        error = ''
        num_results = ''
        num_accounts_in_db = ''
        results = []
        limit = 10000

        try:
            query = flask.request.form['query']
            credshed = CredShed()
            num_accounts_in_db = credshed.db.account_count()

            start_time = datetime.now()
            results = list(credshed.search(query, limit=limit))
            if len(results) == limit:
                error = 'Displaying first {:,} results'.format(limit)

            end_time = datetime.now()
            time_elapsed = (end_time - start_time)
            num_accounts_in_db = 'Searched {:,} accounts in {} seconds'.format(num_accounts_in_db, str(time_elapsed)[:-4])
            num_results = '{:,} results for "{}"'.format(len(results), query)

        except CredShedError as e:
            error = str(e)
        except KeyError:
            query = ''

        return flask.render_template('pages/search_results.html',\
            query=query, results=results, num_accounts=num_accounts_in_db, num_results=num_results, error=error)



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