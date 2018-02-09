import model
from google.appengine.ext import ndb

def save_csv_to_store(csv_file):
    for line in csv_file.splitlines():
        fields = line.split(';')
        entity = model.Comuni(key = ndb.Key('Comuni', fields[1]))
        entity.codice_istat = fields[0]
        entity.provincia = fields[2]
        entity.regione = fields[3]
        entity.prefisso = fields[4]
        entity.cap = fields[5]
        entity.abitanti = int(fields[7])
        entity.link_comuni_italiani = fields[8]
        entity.id_ilmeteoit = fields[9]
        entity.put()
        
def get_istat_code(comune):
    key = ndb.Key('Comuni', comune)
    entity = key.get()
    return entity.codice_istat
    #result[comune.key.string_id()] = ''

def get_id_ilmeteo(comune):
    key = ndb.Key('Comuni', comune)
    entity = key.get()
    return entity.id_ilmeteoit

def get_regione(comune):
    key = ndb.Key('Comuni', comune)
    entity = key.get()
    return entity.regione