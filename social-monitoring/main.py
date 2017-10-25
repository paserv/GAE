import logging

from flask import Flask, render_template, request
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import taskqueue

from bean import SocialProfileStats, SocialProfile, TopTen, Topic,\
    SocialNetwork, SocialProfile, Test
from google.appengine.api.modules.modules import get_hostname

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


#ADMIN CONTROLLER
##############################################################################
##############################################################################
@app.route('/admin')
def admin():
    user = users.get_current_user()
    if user:
        if users.is_current_user_admin():
            return render_template('admin.html')
        else:
            return 'You are not an administrator.'
    else:
        return'You are not logged in.'
    
@app.route('/admin/add-social-network')
def addSocialNetwork():
    return render_template('add-social-network.html')

@app.route('/admin/added-social-network', methods=['POST'])
def addedSocialNetwork():
    name = request.form['name']
    socialNetwork = SocialNetwork(key = ndb.Key('SocialNetwork', name))
    socialNetwork.name = name
    socialNetwork.put()
    return render_template('ok.html')

@app.route('/admin/add-page-to-monitor')
def addPageToMonitor():
    possibleAncestors = SocialNetwork.query().order(SocialNetwork.key)
    return render_template('add-page-to-monitor.html', socialNetworks = possibleAncestors)

@app.route('/admin/added-page-to-monitor', methods=['POST'])
def addedPageToMonitor():
    name = request.form['name']
    url = request.form['url']
    ancestor = request.form['type']
    pageToMonitor = SocialProfile(key = ndb.Key('SocialProfile', name, parent = ndb.Key('SocialNetwork', ancestor)))
    pageToMonitor.url = url
    pageToMonitor.put()
    return render_template('ok.html')

##############################################################################
##############################################################################



#CRON HANDLER
##############################################################################
##############################################################################
@app.route('/cron')
def cron():
    pageToMonitor = SocialProfile.query()
    #facebookHostname = get_hostname(module='twitter', version='v1')
    for currentPage in pageToMonitor:
        module = currentPage.key.parent().get().name
        screen_name = currentPage.key
        taskqueue.add(url='/stats', target=module, params={'parent': currentPage.key, 'name': screen_name})
    return '', 200
##############################################################################
##############################################################################



#UTILS
##############################################################################
##############################################################################
@app.route('/view')
def view():
    stats = SocialProfileStats.query()
    return render_template('test.html', stats = stats)


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
##############################################################################
##############################################################################

@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/submitted', methods=['POST'])
def submitted_form():
    likes = int(request.form['likes'])
    shares = int(request.form['shares'])
    
    counterFB = SocialProfile(key = ndb.Key('SocialProfile', 'facebook'))
    counterFB.likes = likes
    counterFB.shares = shares
    counterFB.put()
    
    stats = SocialProfile(parent = ndb.Key('SocialProfile', 'facebook'));
    stats.likes = likes
    stats.shares = shares
    stats.put()
    
    tt = TopTen(parent = ndb.Key('TrendingTopic', 'facebook'));
    tt.topics = [Topic(name='paolo', occurrence=10), Topic(name='servillo', occurrence=130), Topic(name='assa', occurrence=810)]
    tt.put()
    
    my_stats = SocialProfile.query(ancestor=ndb.Key('SocialProfile', 'facebook')).order(-SocialProfile.date).fetch(10)
    for currentStat in my_stats:
        likes = likes + currentStat.likes
        shares = shares + currentStat.shares
        
    return render_template('submitted_form.html', likes=likes, shares=shares)
   