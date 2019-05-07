#!/usr/bin/env python3.7

# by TheTechromancer

'''
TODO:
    Improve CSV escaping
'''

# flask classes
import flask
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

# credshed
from lib.credshed.credshed import *

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
        search_report = ''
        error = ''
        results = []
        limit = 10

        try:
            query = flask.request.form['query'].strip()
            search_report, results = credshed_search(query, limit=limit)

        except CredShedError as e:
            error = str(e)
        except KeyError:
            query = ''

        return flask.render_template('pages/search_results.html',\
            query=query, results=results, search_report=search_report, error=error)


def credshed_search(query, limit=0):
    '''
    returns (search_report, results)
    '''

    search_report = []
    credshed = CredShed(metadata=False)
    num_accounts_in_db = credshed.db.account_count()

    if Account.is_email(query):
        query_type = 'email'
        search_report.append('Searching by email')
    elif re.compile(r'^([a-zA-Z0-9_\-\.]*)\.([a-zA-Z]{2,8})$').match(query):
        query_type = 'domain'
        search_report.append('Searching by domain')
    else:
        raise CredShedError('Invalid query')

    num_results = 0
    start_time = datetime.now()
    if limit:
        results = list(credshed.search(query, query_type=query_type, limit=limit))
        num_results = len(results)
        if num_results == limit:
            search_report.append('Displaying first {:,} results for "{}"'.format(limit, query))
        else:
            search_report.append('{:,} results for "{}"'.format(num_results, query))
    else:
        results = credshed.search(query, query_type=query_type, limit=limit)

    end_time = datetime.now()
    time_elapsed = (end_time - start_time)
    search_report.append('Searched {:,} accounts in {} seconds'.format(num_accounts_in_db, str(time_elapsed)[:-4]))

    return (search_report, results)



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


@app.route('/export_csv')
@login_required
def export_csv():

    search_report = []
    results = []

    try:
        query = flask.request.args.get('query')
        if query is not None:
            query = query.strip()
        else:
            query = ''
        search_report, results = credshed_search(query, limit=0)

    except CredShedError as e:
        error = str(e)

    def stream_file():
        yield 'Email,Username,Password,Misc\n'.encode('utf-8')
        for r in results:
            account = (','.join(['"{}"'.format(c.replace(',', '""","""').replace('""', '\\"')\
                ) for c in str(r).split(':')]) + '\n').encode('utf-8')
            yield account

    return flask.Response(flask.stream_with_context(stream_file()), content_type='text/csv', \
        headers={'Content-Disposition': 'attachment; filename=credshed_export.csv'})


@app.route('/logout')
def logout():
    logout_user()
    return flask.redirect('/')


@login_manager.user_loader
def load_user(user_id):
    return security.User()


# start the server with the 'run()' method
if __name__ == '__main__':

    app.run(host='127.0.0.1')