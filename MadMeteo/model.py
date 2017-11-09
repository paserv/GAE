from google.appengine.ext import ndb

class Comuni(ndb.Model):
    cod_com_alfanumerico = ndb.StringProperty(indexed=False)

    