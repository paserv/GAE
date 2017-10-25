from flask import Flask, request
from google.appengine.ext import ndb
from TwitterAPI import TwitterAPI
from bean import SocialProfileStats

app = Flask(__name__)

consumer_key = 'f1mboyRyl229y3cXCFkKBJrLP'
consumer_secret = 'dNXHcIzQGk07fEVxPvgUt3ZfPNmxi4MYOYsyokdOQcAavnIvb1'
access_token_key = '90233211-WaN872hBupVTThJJBP5zPsSNvMSiw1w29OXvKj273'
access_token_secret = 'TrRzTLc1fpVmKslZy0bUOGcAVFvn1xbLieLF3Z47vNqrG'
proxy_url = '127.0.0.1:3128'

#TASK HANDLER
##############################################################################
##############################################################################
@app.route('/stats', methods=['POST'])
def getStats():
    parent = request.form['parent']
    screen_name = request.form['name']
    
    api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret, auth_type='oAuth1') #, proxy_url=proxy_url)
    r = api.request('users/show', {'screen_name':screen_name})
    j = r.response.json()
    
    stats = SocialProfileStats(parent = ndb.Key('SocialProfile', parent))
    stats.statuses_count = j['statuses_count']
    stats.friends_count = j['friends_count']
    stats.followers_count = j['followers_count']
    stats.favourites_count = j['favourites_count']
    stats.put()
    return '', 200
##############################################################################
##############################################################################