import logging

from flask import Flask, render_template, request
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import taskqueue

app = Flask(__name__)

@app.route('/')
def welcome():
    user = users.get_current_user()
    if user:
        nickname = user.nickname()
        logout_url = users.create_logout_url('/')
        greeting = 'Welcome, {}! <br /><a href="{}">sign out</a><br /><a href="admin">Admin</a>'.format(nickname, logout_url)
    else:
        login_url = users.create_login_url('/')
        greeting = '<a href="{}">Sign in</a>'.format(login_url)
    return greeting