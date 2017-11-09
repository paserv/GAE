import model
from google.appengine.ext import ndb

def save_csv_to_store(csv_file):
    for line in csv_file.splitlines():
        fields = line.split(';')
        entity = model.Comuni(key = ndb.Key('Comuni', fields[1]))
        entity.cod_com_alfanumerico = fields[0]
        entity.put()
        
def get_istat_code(comune):
    key = ndb.Key('Comuni', comune)
    entity = key.get()
    return entity.cod_com_alfanumerico
    #result[comune.key.string_id()] = ''
