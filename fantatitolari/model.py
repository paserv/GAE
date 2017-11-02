from google.appengine.ext import ndb

class User(ndb.Model):
    ident = ndb.StringProperty(indexed=False)
    
class TeamPlayer(ndb.Model):
    ident = ndb.StringProperty(indexed=False)
    
class Team(ndb.Model):
    ident = ndb.StringProperty(indexed=False)