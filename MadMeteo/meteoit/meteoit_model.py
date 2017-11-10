from json import JSONEncoder

class DayMeteo(JSONEncoder):
    giorno = None
    ora = None
    urlIcona = None
    label = None
    temperatura = None
    precipitazioni = None
    vento = None
    umidita = None
    pressione = None
    uv = None
    
class WeekMeteo():
    giorno = None
    label_giorno = None
    urlIcona = None
    minime = None
    massime = None
        