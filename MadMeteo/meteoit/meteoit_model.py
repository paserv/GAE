class DayMeteo():
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

    @staticmethod
    def labels():
        return ['ora', 'label', 'temperatura', 'pressione', 'precipitazioni', 'umidita', 'vento']
    
    def toList(self):
        return [self.ora, self.label, self.temperatura, self.pressione, self.precipitazioni, self.umidita, self.vento]
        
class WeekMeteo():
    giorno = None
    label_giorno = None
    urlIcona = None
    minime = None
    massime = None
        