#!/usr/bin/env python3

# by TheTechromancer

# misc
import logging
import argparse

# flask
from werkzeug.serving import run_simple
from flask import redirect, render_template

# credshed
from lib.app import *

# set up logging
log = logging.getLogger('credshed.gui')


@gui.route('/', methods=['GET'])
def home():

    return render_template('pages/search.html')



@gui.route('/login', methods=['GET'])
def login():

    return render_template('pages/login.html')


@gui.route('/search_stats', methods=['GET'])
def search_stats():

    return render_template('pages/search_stats.html')


@gui.route('/js/global.js', methods=['GET'])
def global_js():

    return render_template('js/global.js', base_api_url=base_api_url)



if __name__ == '__main__':

    default_host = '127.0.0.1'
    default_port = 5007

    parser = argparse.ArgumentParser(description="Front-end Web App for CredShed")
    parser.add_argument('-ip', '--ip',      default=default_host,           help=f'IP address on which to listen (default: {default_host})')
    parser.add_argument('-p', '--port',     default=default_port, type=int, help=f'port on which to listen (default: {default_port})')
    parser.add_argument('-u', '--api-url',  default=base_api_url,           help=f'Credshed API base URL')
    parser.add_argument('-d', '--debug',    action='store_true',            help='enable debugging')
 
    try:

        options = parser.parse_args()

        base_api_url = options.api_url

        if options.debug:
            gui.debug = True
            logging.getLogger('credshed').setLevel(logging.DEBUG)
        else:
            logging.getLogger('credshed').setLevel(logging.INFO)

        log.info(f'Running on http://{options.ip}:{options.port}')

        if options.debug:
            api.debug = True
        log.info('Starting credshed-api at "/api"')
        run_simple(hostname=options.ip, port=options.port, application=app, use_reloader=options.debug, use_debugger=options.debug)


    except (argparse.ArgumentError, AssertionError) as e:
        log.critical(e)
        exit(2)

    except KeyboardInterrupt:
        log.error('Interrupted')
        exit(1)