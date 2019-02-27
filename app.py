#!/usr/bin/env python3.7

# import the Flask class from the flask module
from flask import Flask, render_template, request

# create the application object
app = Flask(__name__)

# use decorators to link the function to a url
@app.route('/')
def home():
    return render_template('pages/home.html')


# use decorators to link the function to a url
@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
    	return render_template('pages/search_results.html', query=request.form['query'])

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)