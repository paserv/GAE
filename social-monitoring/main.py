import logging

from flask import Flask, render_template, request
from google.appengine.api import users

app = Flask(__name__)


@app.route('/')
def hello():
    user = users.get_current_user()
    if user:
        nickname = user.nickname()
        logout_url = users.create_logout_url('/')
        greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(nickname, logout_url)
    else:
        login_url = users.create_login_url('/')
        greeting = '<a href="{}">Sign in</a>'.format(login_url)
    return greeting


@app.route('/admin')
def admin():
    user = users.get_current_user()
    if user:
        if users.is_current_user_admin():
            return 'You are an administrator.'
        else:
            return 'You are not an administrator.'
    else:
        return'You are not logged in.'

@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/submitted', methods=['POST'])
def submitted_form():
    name = request.form['name']
    email = request.form['email']
    site = request.form['site_url']
    comments = request.form['comments']
    return render_template('submitted_form.html', name=name, email=email, site=site, comments=comments)
   
    
@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500