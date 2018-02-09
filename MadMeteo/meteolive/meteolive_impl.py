from bs4 import BeautifulSoup
from abstract_meteo import AbstractMeteo
import data_controller as dc
from meteolive_model import DayMeteo
from google.appengine.api import urlfetch
import urllib
import sys, traceback

class ImplMeteoLive(AbstractMeteo):
    base_url = 'http://www.meteolive.it/previsione-meteo/italia/'
    name = 'meteolive'
    
    def get_query_url(self, comune, day):
        regione = dc.get_regione(comune)
        nome_regione = urllib.quote_plus(regione)
        nome_comune = urllib.quote_plus(comune)

        return {
            '0': self.base_url + nome_regione + '/' + nome_comune + '/oggi/',
            '1': self.base_url + nome_regione + '/' + nome_comune + '/1/',
            '2': self.base_url + nome_regione + '/' + nome_comune + '/2/',
            '3': self.base_url + nome_regione + '/' + nome_comune + '/3/',
            '4': self.base_url + nome_regione + '/' + nome_comune + '/4/',
            '5': self.base_url + nome_regione + '/' + nome_comune + '/5/',
            '6': self.base_url + nome_regione + '/' + nome_comune + '/6/',
        }.get(day)
        
    def get_meteo_by_day(self, comune, day):
        result = {}
        result[self.name] = []
        try:
            url = self.get_query_url(comune, day)
            request = urlfetch.fetch(url)
            if request.status_code == 200:
                html_data = request.content
                parsed_html = BeautifulSoup(html_data, "lxml")
                
                box_previsioni = parsed_html.body.find('div', attrs={'id':'box-previsioni-content'})
                rows = box_previsioni.find_all('tr')
                iterrows = iter(rows)
                next(iterrows)
                for row in iterrows:
                    currMeteo = DayMeteo()
                    cols = row.find_all('td')
                    currMeteo.ora = cols[0].text
                    currMeteo.label = cols[1].text
                    currMeteo.temperatura_descr = cols[2].find('small').text
                    currMeteo.temperatura = cols[2].text.replace(currMeteo.temperatura_descr, '')
                    currMeteo.umidita_descr = cols[3].find('small').text
                    currMeteo.umidita = cols[3].text.replace(currMeteo.umidita_descr, '')
                    currMeteo.precipitazioni = cols[4].text
                    currMeteo.vento_descr = cols[5].find('small').text
                    currMeteo.vento = cols[5].text.replace(currMeteo.vento_descr, '') + ' Km/h'
                    currMeteo.visibilita_descr = cols[7].find('small').text
                    currMeteo.visibilita = cols[7].text.replace(currMeteo.visibilita_descr, '')
                    currMeteo.pressione = cols[8].text + ' mbar'
                    result[self.name].append(currMeteo.__dict__)
        except:
            traceback.print_exc(file=sys.stdout)
        finally:             
            return result
    