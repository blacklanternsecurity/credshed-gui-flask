# credshed-gui
Flask web app front-end for [credshed](https://github.com/blacklanternsecurity/credshed)

![credshed-gui-screenshot](https://user-images.githubusercontent.com/20261699/60762868-33d44580-a02e-11e9-8294-200c711328f5.png)


## Usage:
~~~
$ ./credshed-gui.py --help
usage: credshed-gui.py [-h] [-ip IP] [-p PORT] [-d]

Front-end GUI for CredShed

optional arguments:
  -h, --help            show this help message and exit
  -ip IP, --ip IP       IP address on which to listen (default: 127.0.0.1)
  -p PORT, --port PORT  port on which to listen (default: 5007)
  -d, --debug           enable debugging
~~~


## Dev / Debugging Setup:
1. Clone github repo into `/opt`
    ~~~
    $ cd /opt
    $ sudo git clone --recursive https://github.com/blacklanternsecurity/credshed-gui
    ~~~
1. Follow instructions in the [credshed](https://github.com/blacklanternsecurity/credshed) README to set up backend
    - NOTE: the `credshed` repo has already been cloned into `/opt/credshed-gui/lib/credshed` in the previous step
1. Install python3.7 and Flask dependencies:
    ~~~
    $ sudo apt install python3.7 python3.7-pip
    $ python3.7 -m pip install -r requirements.txt
    ~~~
1. Run the app:
    - `./credshed-gui.py`
1. Browse to [http://localhost:5007](http://localhost:5007)


## Production Setup:
1. Clone github repo into `/opt`
    ~~~
    $ cd /opt
    $ sudo git clone --recursive https://github.com/blacklanternsecurity/credshed-gui
    $ sudo chown root:www-data /opt/credshed-gui
    $ sudo chmod 770 /opt/credshed-gui
    ~~~
1. Follow instructions in the [credshed](https://github.com/blacklanternsecurity/credshed) README to set up backend
    - NOTE: the `credshed` repo has already been cloned into `/opt/credshed-gui/lib/credshed` in the previous step
1. Install uWSGI and its associated Python module:
    ~~~
    $ sudo apt install uwsgi python3.7 python3.7-dev python3.7-pip
    $ python3.7 -m pip install -r requirements.txt
    ~~~
    - NOTE: On Debian, the testing repo must be enabled for python3.7-dev:
        - add the following to /etc/apt/sources.list and run `apt update` to enable the "testing" repo:
            ~~~
            deb http://ftp.us.debian.org/debian/ buster main contrib non-free
            deb-src http://ftp.us.debian.org/debian/ buster main contrib non-free
            ~~~
1. Make sure uWSGI component is working:
    - `$ uwsgi --socket 127.0.0.1:8000 --protocol=http -w credshed-gui:app`
    - Browse to http://127.0.0.1:8000 and verify that you see the CredShed login page
    - `ctrl+c` to stop
1. Install, enable, and start CredShed uWSGI service:
    ~~~
    $ sudo ln -s /opt/credshed-gui/webserver/credshed-gui.service /etc/systemd/system/credshed-gui.service
    $ sudo systemctl enable credshed-gui
    $ sudo systemctl start credshed-gui
    ~~~
1. Edit `webserver/nginx.conf` to have correct FQDN, e.g. `credshed.example.com`
1. Install, enable and start Nginx service:
    ~~~
    $ sudo apt install nginx
    $ sudo ln -s /opt/credshed-gui/webserver/nginx.conf /etc/nginx/sites-available/credshed.example.com.conf
    $ sudo systemctl enable nginx
    $ sudo systemctl start nginx
    ~~~
1. Install LetsEncrypt Certificate and enable HTTPS (Optional but Recommended):
    1. Add certbot repo and install
        ~~~
        $ sudo apt install software-properties-common # "add-apt-repository" not installed by default on Debian
        $ sudo add-apt-repository ppa:certbot/certbot
        $ sudo apt-get update
        $ sudo apt-get install python-certbot-nginx
        ~~~
    1. Request Cert:
        ~~~
        $ sudo certbot --nginx -d credshed.example.com
        ~~~
    1. Reload Nginx:
        ~~~
        $ sudo systemctl reload nginx
        ~~~