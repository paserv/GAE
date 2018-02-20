from datetime import datetime

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

class IconConversion():
    iconDayDict = {
        "pioggia debole": "46.svg",
        "pioggia moderata": "46.svg",
        "coperto": "04.svg",
        "nuvoloso con pioggia debole": "46.svg",
        "nuvoloso": "04.svg",
        "nuvoloso con pioggia intensa": "10.svg",
        "sereno": "01d.svg",
        "poco nuvoloso": "03d.svg",
        "neve debole": "49.svg",
        "neve moderata": "49.svg",
        "piovaschi e schiarite": "40d.svg",
        "pioviggine": "46.svg",
        "variabile": "41d.svg",
        "rovesci e schiarite": "41d.svg",
        "pioggia": "10.svg",
        "parz nuvoloso": "03d.svg",
        "poche nubi": "02d.svg",
        "quasi sereno": "02d.svg",
        "sereno con veli": "02d.svg",
        "nevischio": "49.svg",
        "pioggia e neve debole": "47.svg",
        "neve": "50.svg",
        "velature sparse": "03d.svg",
        "temporale": "10.svg",
        "pioggia e schiarite": "41d.svg",
        "temporale e schiarite": "25d.svg",
        "nubi sparse": "03d.svg",
        "pioggia mista a neve": "47.svg",
        "nebbia": "15.svg",
        "pioggia intermittente": "46.svg",
        "possibile breve pioggia": "46.svg",
        "nuvoloso, possibile debole precipitazione": "46.svg",
        "pioggia debole o intermittente": "46.svg",
        "nuvoloso con possibili acquazzoni": "46.svg",
        "nubi sparse con un possibile breve acquazzone": "46.svg",
        "coperto, possibile debole precipitazione nei dintorni": "46.svg",
        "coperto, possibile debole precipitazione": "46.svg",
        "nuvoloso con possibili rovesci di pioggia": "46.svg",
        "pioggia debole o intermittente, ventoso": "46.svg",
        "pioggia intermittente, ventoso": "46.svg",
        "nuvoloso, ventoso": "04.svg",
        "molte nubi, possibile debole precipitazione nei dintorni": "04.svg",
        "pioggia mista a neve o neve bagnata": "47.svg",
        "neve bagnata": "50.svg",
        "possibile debole nevicata": "49.svg",
        "debole nevicata": "49.svg",
        "nubi sparse, possibile debole precipitazione": "46.svg",
        }

    iconNightDict = {
        "pioggia debole": "46.svg",
        "pioggia moderata": "46.svg",
        "coperto": "04.svg",
        "nuvoloso con pioggia debole": "46.svg",
        "nuvoloso": "04.svg",
        "nuvoloso con pioggia intensa": "10.svg",
        "sereno": "01n.svg",
        "poco nuvoloso": "03n.svg",
        "neve debole": "49.svg",
        "neve moderata": "49.svg",
        "piovaschi e schiarite": "40n.svg",
        "pioviggine": "46.svg",
        "variabile": "41n.svg",
        "rovesci e schiarite": "41n.svg",
        "pioggia": "10.svg",
        "parz nuvoloso": "03n.svg",
        "poche nubi": "02n.svg",
        "quasi sereno": "02n.svg",
        "sereno con veli": "02n.svg",
        "nevischio": "49.svg",
        "pioggia e neve debole": "47.svg",
        "neve": "50.svg",
        "velature sparse": "03n.svg",
        "temporale": "10.svg",
        "pioggia e schiarite": "41n.svg",
        "temporale e schiarite": "25n.svg",
        "nubi sparse": "03n.svg",
        "pioggia mista a neve": "47.svg",
        "nebbia": "15.svg",
        "pioggia intermittente": "46.svg",
        "possibile breve pioggia": "46.svg",
        "nuvoloso, possibile debole precipitazione": "46.svg",
        "pioggia debole o intermittente": "46.svg",
        "nuvoloso con possibili acquazzoni": "46.svg",
        "nubi sparse con un possibile breve acquazzone": "46.svg",
        "coperto, possibile debole precipitazione nei dintorni": "46.svg",
        "coperto, possibile debole precipitazione": "46.svg",
        "nuvoloso con possibili rovesci di pioggia": "46.svg",
        "pioggia debole o intermittente, ventoso": "46.svg",
        "pioggia intermittente, ventoso": "46.svg",
        "nuvoloso, ventoso": "04.svg",
        "molte nubi, possibile debole precipitazione nei dintorni": "04.svg",
        "pioggia mista a neve o neve bagnata": "47.svg",
        "neve bagnata": "50.svg",
        "possibile debole nevicata": "49.svg",
        "debole nevicata": "49.svg",
        "nubi sparse, possibile debole precipitazione": "46.svg",
        }
    
    mmdict = {
        "pioggia debole": { "label": "pioggia debole", "components": ["nuvola", "poca pioggia"]},
        "pioggia moderata": { "label": "pioggia debole", "components": ["nuvola", "poca pioggia"]},
        "coperto": { "label": "nuvoloso", "components": ["nuvola"]},
        "nuvoloso con pioggia debole": { "label": "pioggia debole", "components": ["nuvola", "poca pioggia"]},
        "nuvoloso": { "label": "nuvoloso", "components": ["nuvola"]},
        "nuvoloso con pioggia intensa": { "label": "pioggia", "components": ["nuvola", "pioggia"]},
        "sereno": { "label": "sereno", "components": ["sole"]},
        "poco nuvoloso": { "label": "poco nuvoloso", "components": ["sole", "nuvola"]},
        "neve debole": { "label": "poca neve", "components": ["nuvola", "poca neve"]},
        "neve moderata": { "label": "poca neve", "components": ["nuvola", "poca neve"]},
        "piovaschi e schiarite": { "label": "variabile", "components": ["sole", "nuvola", "poca pioggia"]},
        "pioviggine": { "label": "pioggia debole", "components": ["nuvola", "poca pioggia"]},
        "variabile": { "label": "variabile", "components": ["sole", "nuvola", "pioggia"]},
        "rovesci e schiarite": { "label": "variabile", "components": ["sole", "nuvola", "pioggia"]},
        "pioggia": { "label": "pioggia", "components": ["nuvola", "pioggia"]},
        "parz nuvoloso": { "label": "poco nuvoloso", "components": ["sole", "nuvola"]},
        "poche nubi": { "label": "quasi sereno", "components": ["sole", "nuvola piccola"]},
        "quasi sereno": { "label": "quasi sereno", "components": ["sole", "nuvola piccola"]},
        "sereno con veli": { "label": "quasi sereno", "components": ["sole", "nuvola piccola"]},
        "nevischio": { "label": "poca neve", "components": ["nuvola", "poca neve"]},
        "pioggia e neve debole": { "label": "pioggia e neve", "components": ["nuvola", "poca pioggia", "poca neve"]},
        "neve": { "label": "neve", "components": ["nuvola", "neve"]},
        "velature sparse": { "label": "poco nuvoloso", "components": ["sole", "nuvola"]},
        "temporale": { "label": "pioggia", "components": ["nuvola", "pioggia"]},
        "pioggia e schiarite": { "label": "variabile", "components": ["sole", "nuvola", "pioggia"]},
        "temporale e schiarite": { "label": "variabile", "components": ["sole", "nuvola", "pioggia", "fulmine"]},
        "nubi sparse": { "label": "poco nuvoloso", "components": ["sole", "nuvola"]},
        "pioggia mista a neve": { "label": "pioggia e neve", "components": ["nuvola", "poca pioggia", "poca neve"]},
        "nebbia": { "label": "nebbia", "components": ["nebbia"]},
        "pioggia intermittente": { "label": "pioggia debole", "components": ["nuvola", "poca pioggia"]},
        "possibile breve pioggia": { "label": "pioggia debole", "components": ["nuvola", "poca pioggia"]},
        "nuvoloso, possibile debole precipitazione": { "label": "pioggia debole", "components": ["nuvola", "poca pioggia"]},
        "pioggia debole o intermittente": { "label": "pioggia debole", "components": ["nuvola", "poca pioggia"]},
        "nuvoloso con possibili acquazzoni": { "label": "pioggia debole", "components": ["nuvola", "poca pioggia"]},
        "nubi sparse con un possibile breve acquazzone": { "label": "pioggia debole", "components": ["nuvola", "poca pioggia"]},
        "coperto, possibile debole precipitazione nei dintorni": { "label": "pioggia debole", "components": ["nuvola", "poca pioggia"]},
        "coperto, possibile debole precipitazione": { "label": "pioggia debole", "components": ["nuvola", "poca pioggia"]},
        "nuvoloso con possibili rovesci di pioggia": { "label": "pioggia debole", "components": ["nuvola", "poca pioggia"]},
        "pioggia debole o intermittente, ventoso": { "label": "pioggia debole", "components": ["nuvola", "poca pioggia"]},
        "pioggia intermittente, ventoso": { "label": "pioggia debole", "components": ["nuvola", "poca pioggia"]},
        "nuvoloso, ventoso": { "label": "nuvoloso", "components": ["nuvola"]},
        "molte nubi, possibile debole precipitazione nei dintorni": { "label": "nuvoloso", "components": ["nuvola"]},
        "pioggia mista a neve o neve bagnata": { "label": "pioggia e neve", "components": ["nuvola", "poca pioggia", "poca neve"]},
        "neve bagnata": { "label": "neve", "components": ["nuvola", "neve"]},
        "possibile debole nevicata": { "label": "poca neve", "components": ["nuvola", "poca neve"]},
        "debole nevicata": { "label": "poca neve", "components": ["nuvola", "poca neve"]},
        "nubi sparse, possibile debole precipitazione": { "label": "pioggia debole", "components": ["nuvola", "poca pioggia"]},
        }
    
    @staticmethod
    def isSunny(hour):
        myhour = hour[:-3]
        if myhour != '00':
            myhour = myhour.lstrip("0")
        myhour = int(myhour)       
        if (myhour > 6 and myhour < 20):
            return True
        return False
        
    @staticmethod
    def getIcon(label, hour):
        mylabel = label.lower().replace(u'\xa0', u' ')
        if IconConversion.isSunny(hour):
            if mylabel in IconConversion.iconDayDict:
                return IconConversion.iconDayDict[mylabel]
        else:
            if mylabel in IconConversion.iconNightDict:
                return IconConversion.iconNightDict[mylabel]
        return 'undefined.svg'
        
    @staticmethod
    def getMMLabel(label):
        mylabel = label.lower().replace(u'\xa0', u' ')
        if mylabel in IconConversion.mmdict:
            return IconConversion.mmdict[mylabel]['label']
        return 'undefined'
    