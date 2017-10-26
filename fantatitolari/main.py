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
        logout_url = users.create_logout_url('/')
        return render_template('home.html', logout_url = logout_url)
    else:
        login_url = users.create_login_url('/')
        return render_template('home.html', login_url = login_url)
