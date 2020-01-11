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
1. Clone github repo
    ~~~
    $ git clone --recursive https://github.com/blacklanternsecurity/credshed-gui
    ~~~
1. Follow instructions in the [credshed](https://github.com/blacklanternsecurity/credshed) README to set up backend
    - NOTE: the `credshed` repo has already been cloned into `./lib/credshed` in the previous step
1. Install python3 and Flask dependencies:
    ~~~
    $ sudo apt install python3 python3-pip
    $ python3 -m pip install -r requirements.txt
    ~~~
1. Run the app:
    - `./credshed-gui.py`
1. Browse to [http://localhost:5007](http://localhost:5007)


## Production Setup:
1. Clone github repo into `/opt`
    ~~~
    $ cd /opt
    $ sudo git clone --recursive https://github.com/blacklanternsecurity/credshed-gui
    $ sudo chown -R user:user /opt/credshed-gui # replace "user" with a low-privileged user who will be running the app
    $ sudo chmod 770 /opt/credshed-gui
    ~~~
1. Follow instructions in the [credshed](https://github.com/blacklanternsecurity/credshed) README to set up backend
    - NOTE: the `credshed` repo has already been cloned into `/opt/credshed-gui/lib/credshed` in the previous step
1. Install uWSGI and its associated Python module:
    ~~~
    $ sudo apt install uwsgi uwsgi-plugin-python3 python3 python3-dev python3-pip
    $ python3 -m pip install -r requirements.txt
    ~~~
    - NOTE: On Debian, the testing repo must be enabled for python3-dev:
        - add the following to /etc/apt/sources.list and run `apt update` to enable the "testing" repo:
            ~~~
            deb http://ftp.us.debian.org/debian/ buster main contrib non-free
            deb-src http://ftp.us.debian.org/debian/ buster main contrib non-free
            ~~~
1. Make sure uWSGI component is working:
    - `$ uwsgi --plugins=python3 --socket 127.0.0.1:5007 --protocol=http -w credshed-gui:app`
    - Browse to http://127.0.0.1:5007 and verify that you see the CredShed login page
    - `ctrl+c` to stop
1. Install, enable, and start CredShed uWSGI service:
    - FIRST, edit `--uid=user` `--gid=user` in `credshed-gui.service` to reflect the low-privileged user that will be running the app
    ~~~
    $ sudo ln -s /opt/credshed-gui/webserver/credshed-gui.service /etc/systemd/system/credshed-gui.service
    $ sudo systemctl enable credshed-gui
    $ sudo systemctl start credshed-gui
    ~~~
1. Edit `webserver/nginx.conf` to have correct FQDN, e.g. `credshed.example.com`
    - Also input the proper path for your SSL certificates or delete the SSL section if you plan on using LetsEncrypt
1. Install, enable and start Nginx service:
    ~~~
    $ sudo apt install nginx
    $ sudo ln -s /opt/credshed-gui/webserver/nginx.conf /etc/nginx/sites-available/credshed.example.com.conf
    $ sudo systemctl enable nginx
    $ sudo systemctl start nginx
    ~~~
1. Install LetsEncrypt Certificate and enable HTTPS (Optional):
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
1. Log in
    - An account is automatically generated and printed to the screen after the first login attempt
    - You can also add/remove users by editing `db/users.db`.  It uses simple JSON in the format:
    ~~~
    {
        "username": [<userid>, "<password sha512sum>"],
        ...
    }
    ~~~