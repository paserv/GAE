import logging

from flask import Flask, render_template, request
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import taskqueue

import bean
from bean import Author, Greeting, Stats, Counter, TrendingTopic, TopTen, Topic

app = Flask(__name__)


@app.route('/')
def hello():
    user = users.get_current_user()
    if user:
        nickname = user.nickname()
        logout_url = users.create_logout_url('/')
        greeting = 'Welcome, {}! (<a href="{}">sign out</a><a href="admin">Admin</a>)'.format(nickname, logout_url)
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

@app.route('/cron')
def cron():
    my_stats = Stats.query(ancestor=ndb.Key('Counter', 'facebook')).order(-Stats.date).fetch(10)
    likes = 0
    shares = 0
    for currentStat in my_stats:
        likes += currentStat.likes
        shares += currentStat.shares
    return render_template('submitted_form.html', likes=likes, shares=shares)

@app.route('/test', methods=['POST'])
def test():
    task = taskqueue.add(url='/stats/facebook',  name='first-try', target='worker', params={'likes': 123, 'shares': 321})
    
@app.route('/stats/facebook')
def exampleFB():
    stats = Stats(parent = ndb.Key('Counter', 'facebook'));
    stats.likes = 123
    stats.shares = 321
    stats.put()
    return render_template('form.html')

@app.route('/submitted', methods=['POST'])
def submitted_form():
    likes = int(request.form['likes'])
    shares = int(request.form['shares'])
    
    counterFB = Counter(key = ndb.Key('Counter', 'facebook'))
    counterFB.likes = likes
    counterFB.shares = shares
    counterFB.put()
    
    stats = Stats(parent = ndb.Key('Counter', 'facebook'));
    stats.likes = likes
    stats.shares = shares
    stats.put()
    
    tt = TopTen(parent = ndb.Key('TrendingTopic', 'facebook'));
    tt.topics = [Topic(name='paolo', occurrence=10), Topic(name='servillo', occurrence=130), Topic(name='assa', occurrence=810)]
    tt.put()
    
    my_stats = Stats.query(ancestor=ndb.Key('Counter', 'facebook')).order(-Stats.date).fetch(10)
    for currentStat in my_stats:
        likes = likes + currentStat.likes
        shares = shares + currentStat.shares
        
    return render_template('submitted_form.html', likes=likes, shares=shares)
   

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500