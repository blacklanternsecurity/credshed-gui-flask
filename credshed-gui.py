#!/usr/bin/env python3

# by TheTechromancer

# flask classes
import flask
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

# credshed
from lib.credshed.credshed import *
from lib.credshed.credshed.lib import logger
from lib.credshed.credshed.lib import validation

# other
import sys
import string
import logging
import argparse
from time import sleep
from lib.export_csv import *
from datetime import datetime
import lib.security as security


# set up logging
log = logging.getLogger('credshed.gui')


# create the application object
app = flask.Flask(__name__)
login_manager = LoginManager(app)

# secret key
app.secret_key = security.get_secret_key()


class WebSafeAccount():
    '''
    Takes care of non-css-friendly characters in Account._id

    And yes, the web front-end was an afterthought.
    '''

    def __init__(self, account):

        self.account = str(account)
        self._id = self.make_safe_id(account._id)


    def __str__(self):

        return self.account


    def make_safe_id(self, _id):

        _id = _id.replace('|', '-_-_-')
        _id = _id.replace('/', '_____')
        _id = _id.replace('+', '-----')
        _id = _id.replace('.', '__-__')
        return _id


    @staticmethod
    def convert_safe_id(_id):

        _id = _id.replace('-_-_-', '|')
        _id = _id.replace('_____', '/')
        _id = _id.replace('-----', '+')
        _id = _id.replace('__-__', '.')
        return _id



@app.route('/')
def home():
    if current_user.is_authenticated:
        return flask.redirect('/search')
    return flask.redirect('/login')


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():

    if flask.request.method == 'GET':
        return flask.render_template('pages/search.html')

    elif flask.request.method == 'POST':

        query = 'email or domain'
        search_report = ''
        error = ''
        results = []
        limit = 1000

        try:
            query = flask.request.form['query'].strip()
            log.info('Query "{}" by {}'.format(query, current_user.username))
            response = flask.jsonify(credshed_search(query, limit=limit))
            response.set_cookie('last_credshed_search', flask.escape(query))
            return response

        except (KeyError, CredShedError) as e:
            log.error(f'Error executing search: {e}')
            response = flask.jsonify({'search_report': f'Error executing search: {e}', 'error': True})
            response.status_code = 400
            return response


@app.route('/count', methods=['POST'])
@login_required
def count():

    return flask.jsonify({'count': 123})



def credshed_search(query, limit=0):
    '''
    returns (search_report, results)
    '''

    accounts = []
    search_report = []

    credshed = CredShed()
    num_accounts_in_db = credshed.db.account_count()

    query_type = validation.validate_query_type(query)
    search_report.append(f'Searching by {query_type}')

    num_results = 0
    start_time = datetime.now()

    for account in credshed.search(query, query_type=query_type, limit=limit):
        accounts.append({k: flask.escape(v) for k,v in account.json.items()})

    if len(accounts) == limit:
        search_report.append('Results for "{}" limited to {:,}'.format(flask.escape(query), limit))
    else:
        search_report.append('{:,} results for "{}"'.format(credshed.count(query), query))

    end_time = datetime.now()
    time_elapsed = (end_time - start_time)
    search_report.append('Searched {:,} accounts in {} seconds'.format(num_accounts_in_db, str(time_elapsed)[:-4]))

    json_response = {
        'search_report': search_report,
        'accounts': accounts
    }

    return json_response



@app.route('/login', methods=['GET', 'POST'])
def login():

    if flask.request.method == 'GET':
        return flask.render_template('pages/login.html')

    elif flask.request.method == 'POST':
        if 'username' in flask.request.form:
            user = security.validate_login(flask.request.form)
            if not user.is_anonymous:
                login_user(user)
            return flask.redirect('/')

        else:
            sleep(3)
            return flask.redirect('/login')



@app.route('/metadata/<account_id>', methods=['GET'])
@login_required
def metadata(account_id):

    credshed = CredShed(metadata=True)
    account_id = WebSafeAccount.convert_safe_id(account_id)
    account_metadata = credshed.db.fetch_account_metadata(account_id)

    if account_metadata:
        return '<ul>{}</ul>'.format('\n'.join(['<li>{}</li>'.format(flask.escape(str(s))) for s in account_metadata]))
    else:
        return ''




@app.route('/export_csv')
@login_required
def export_csv():

    try:
        query = flask.request.args.get('query')
        if query is not None:
            query = query.strip()
        else:
            query = ''

        credshed = CredShed()
        accounts = credshed.search(query)

        query_str = ''.join([c for c in query if c.lower() in string.ascii_lowercase])
        filename = 'credshed_{}_{date:%Y%m%d-%H%M%S}.csv'.format( query_str, date=datetime.now() )

        return flask.Response(flask.stream_with_context(iter_csv(accounts)), content_type='text/csv', \
            headers={'Content-Disposition': f'attachment; filename={filename}'})

    except CredShedError as e:
        log.error(str(e))


@app.route('/logout')
def logout():
    logout_user()
    return flask.redirect('/')


@login_manager.user_loader
def load_user(user_id):
    user = security.user_lookup_by_id(user_id)
    return user



if __name__ == '__main__':

    default_host = '127.0.0.1'
    default_port = 5007

    parser = argparse.ArgumentParser(description="Front-end GUI for CredShed")
    parser.add_argument('-ip', '--ip',      default=default_host,           help='IP address on which to listen (default: {})'.format(default_host))
    parser.add_argument('-p', '--port',     default=default_port, type=int, help='port on which to listen (default: {})'.format(default_port))
    parser.add_argument('-d', '--debug',    action='store_true',            help='enable debugging')
 
    try:

        options = parser.parse_args()

        # start the server with the 'run()' method
        log.info(f'Running on http://{options.ip}:{options.port}')
        app.run(host=options.ip, port=options.port, debug=options.debug)

    except (argparse.ArgumentError, AssertionError) as e:
        log.critical(e)
        sys.exit(2)

    except KeyboardInterrupt:
        log.error('Interrupted')
        sys.exit(1)