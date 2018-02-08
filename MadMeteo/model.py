from google.appengine.ext import ndb

class Comuni(ndb.Model):
    codice_istat = ndb.StringProperty(indexed=False)
    provincia = ndb.StringProperty(indexed=False)
    regione = ndb.StringProperty(indexed=False)
    prefisso = ndb.StringProperty(indexed=False)
    cap = ndb.StringProperty(indexed=False)
    abitanti = ndb.IntegerProperty(indexed=False)
    link_comuni_italiani = ndb.StringProperty(indexed=False)
    id_ilmeteoit = ndb.StringProperty(indexed=False)
    