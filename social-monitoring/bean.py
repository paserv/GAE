from google.appengine.ext import ndb

class SocialNetwork(ndb.Model):
    name = ndb.StringProperty(indexed=False)

class SocialProfile(ndb.Model):
    url = ndb.StringProperty(indexed=False)
    likes = ndb.IntegerProperty(indexed=False)
    shares = ndb.IntegerProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    
class SocialProfileStats(ndb.Model):
    likes = ndb.IntegerProperty(indexed=False)
    shares = ndb.IntegerProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

class Test(ndb.Model):
    test = ndb.StringProperty(indexed=False)


class TrendingTopic(ndb.Model):
    topics = ndb.StringProperty(indexed=False)
    
class Topic(ndb.Model):
    name = ndb.StringProperty(indexed=False)
    occurrence = ndb.IntegerProperty(indexed=False)

class TopTen(ndb.Model):
    topics = ndb.StructuredProperty(Topic, repeated=True)
    
    
#         
# class Author(ndb.Model):
#     name = ndb.StringProperty(indexed=False)
#     email = ndb.StringProperty(indexed=False)
#     
#     
# class Greeting(ndb.Model):
#     author = ndb.StructuredProperty(Author, repeated=True)
#     content = ndb.StringProperty(indexed=False)
#     date = ndb.DateTimeProperty(auto_now_add=True)