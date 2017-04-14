from flask import Flask, request
from google.appengine.ext import ndb

from bean import SocialProfileStats

app = Flask(__name__)

#TASK HANDLER
##############################################################################
##############################################################################
@app.route('/stats/facebook', methods=['POST'])
def getFacebookStats():
    parent = request.form['parent']
    url = request.form['url']
#     parent = 'assa'
    stats = SocialProfileStats(parent = ndb.Key('SocialProfile', parent))
    stats.likes = 123
    stats.shares = 321
    stats.put()
    return '', 200
##############################################################################
##############################################################################