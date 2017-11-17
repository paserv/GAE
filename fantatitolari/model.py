from google.appengine.ext import ndb

class User(ndb.Model):
    ident = ndb.StringProperty(indexed=False)
    
class TeamPlayer(ndb.Model):
    ident = ndb.StringProperty(indexed=False)
    
class Team(ndb.Model):
    ident = ndb.StringProperty(indexed=False)
    
class Anagrafica(ndb.Model):
    ident = ndb.IntegerProperty(indexed=False)
    role = ndb.StringProperty(indexed=False)
    name = ndb.StringProperty(indexed=False)
    team = ndb.StringProperty(indexed=False)
    quot = ndb.StringProperty(indexed=False)
    iconUrl = ndb.StringProperty(indexed=False)
    teamUrl = ndb.StringProperty(indexed=False)
    statsUrl = ndb.StringProperty(indexed=False)
    playerLabel = ndb.StringProperty(indexed=False)