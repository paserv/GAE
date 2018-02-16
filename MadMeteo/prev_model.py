class AttributiLuogo():
    nome = None
    regione = None 
    
class AttributiPrecipitazioni():
    mm = None
    max = None
    min = None
    
    def __init__(self, mm, max_, min_):
        self.mm = mm
        self.max = max_
        self.min = min_
        
class AttributiVento():
    direzione = None
    velocita = None
    
    def __init__(self, direzione, velocita):
        self.direzione = direzione
        self.velocita = velocita

class PrevisioneOraria():
    da = None
    a = None
    icona = None
    label = None
    precipitazioni = None
    vento = None   
    temperatura = None
    pressione = None
    
    def __init__(self, da, a, icona, label, prec_mm, vento_direzione, vento_velocita, temperatura, pressione, prec_max = None, prec_min = None,):
        self.da = da
        self.a = a
        self.icona = icona
        self.label = label
        self.precipitazioni = AttributiPrecipitazioni(prec_mm, prec_max, prec_min)
        self.vento = AttributiVento(vento_direzione, vento_velocita)
        self.temperatura = temperatura
        self.pressione = pressione
        
class Previsioni():
    luogo = AttributiLuogo()
    previsioni = [] 
    
class Previsione():
    meteo = Previsioni()
    
    def __init__(self, nome, regione, previsioni):
        self.meteo.luogo.nome = nome
        self.meteo.luogo.regione = regione
        self.meteo.previsioni = previsioni
        
    def toJson(self):
        result = {}
        result["meteo"] = {}
        result["meteo"]["luogo"] = self.meteo.luogo.__dict__
        result["meteo"]["previsioni"] = []
        for curr in self.meteo.previsioni:
            currPrev = {}
            currPrev["da"] = curr.da
            currPrev["a"] = curr.a
            currPrev["icona"] = curr.icona
            currPrev["label"] = curr.label
            currPrev["precipitazioni"] = curr.precipitazioni.__dict__
            currPrev["vento"] = curr.vento.__dict__
            currPrev["temperatura"] = curr.temperatura
            currPrev["pressione"] = curr.pressione
            result["meteo"]["previsioni"].append(currPrev)
        return result
        
        