#!/usr/bin/env python3.7

# by TheTechromancer

# flask classes
import flask
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

# credshed
from lib.credshed.credshed import *

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
log_file = '/var/log/credshed/credshed-gui.log'
log_level=logging.DEBUG
log_format='%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s'
try:
    logging.basicConfig(level=log_level, filename=log_file, format=log_format)
except (PermissionError, FileNotFoundError):
    logging.basicConfig(level=log_level, filename='credshed-gui.log', format=log_format)
    errprint('[!] Unable to create log file at {}, logging to current directory'.format(log_file))
log = logging.getLogger('credshed')
log.setLevel(log_level)


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
            search_report, results = credshed_search(query, limit=limit)
            results = [WebSafeAccount(result) for result in results]

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
            search_report.append('Results for "{}" limited to {:,}'.format(flask.escape(query), limit))
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
        log.error(str(e))

    query_str = ''.join([c for c in query if c.lower() in string.ascii_lowercase])
    filename = 'credshed_{}_{date:%Y%m%d-%H%M%S}.csv'.format( query_str, date=datetime.now() )

    return flask.Response(flask.stream_with_context(iter_csv(results)), content_type='text/csv', \
        headers={'Content-Disposition': 'attachment; filename={}'.format(filename)})


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
        app.run(host=options.ip, port=options.port, debug=options.debug)

    except (argparse.ArgumentError, AssertionError) as e:
        sys.stderr.write('\n[!] {}\n\n'.format(str(e)))
        sys.exit(2)

    except KeyboardInterrupt:
        sys.stderr.write('\n[!] Interrupted\n')
        sys.exit(1)