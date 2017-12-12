from bs4 import BeautifulSoup
from abstract_meteo import AbstractMeteo
from trebmeteo_model import DayMeteo, WeekMeteo
from google.appengine.api import urlfetch
import datetime

class ImplTreBMeteo(AbstractMeteo):
    base_url = 'https://www.3bmeteo.com/meteo/'
    name = '3bmeteo'
    
    def get_query_url(self, comune, day):
        nome_comune = comune.replace(' ', '-')
        return {
            '0': self.base_url + nome_comune.lower(),
            '1': self.base_url + nome_comune.lower() + '/1',
            '2': self.base_url + nome_comune.lower() + '/2',
            '3': self.base_url + nome_comune.lower() + '/3',
            '4': self.base_url + nome_comune.lower() + '/4',
            '5': self.base_url + nome_comune.lower() + '/5',
            '6': self.base_url + nome_comune.lower() + '/6',
        }.get(day)
        
    def get_meteo_by_day(self, comune, day):
        result = {}
        result[self.name] = []
        try:
            url = self.get_query_url(comune, day)
            request = urlfetch.fetch(url)
            if request.status_code == 200:
                html_data = request.content
                parsed_html = BeautifulSoup(html_data, "html.parser")
                
                svgdefinition = parsed_html.body.find('svg', attrs={'style':'position:absolute', "width" : "0"})
                result['svgdefs'] = str(svgdefinition)
                
                #result['week'] = self.get_meteo_week(parsed_html)
                
                ore = parsed_html.body.find_all('div', attrs={'class':'pk_for_city'})
                
                labels = parsed_html.body.find_all('div', attrs={'class':'pk_for_city_weather'})
                
                temperature_col = parsed_html.body.find('ul', attrs={'class':'pk_temp'})
                temperature = temperature_col.find_all('div', attrs={'class':'pk_bvalign'})
                
                precipitazioni_col = parsed_html.body.find('ul', attrs={'class':'pk_precip'})
                precipitazioni = precipitazioni_col.find_all('div', attrs={'class':'pk_bvalign'})
                
                vento_col = parsed_html.body.find('ul', attrs={'class':'pk_vento'})
                vento = vento_col.find_all('div', attrs={'class':'pk_bvalign'})
                
                umidita_col = parsed_html.body.find('ul', attrs={'class':'pk_umidita'})
                umidita = umidita_col.find_all('div', attrs={'class':'pk_bvalign'})
                
                pressione_col = parsed_html.body.find('ul', attrs={'class':'pk_press'})
                pressione = pressione_col.find_all('div', attrs={'class':'pk_bvalign'})
                
                #uv_col = parsed_html.body.find('ul', attrs={'class':'pk_uv'})
                #uv = uv_col.find_all('div', attrs={'class':'pk_cuv'})
                
                for i in range(0, 24):
                    currMeteo = DayMeteo()
                    #currMeteo.giorno = day
                    currMeteo.ora = ore[i].find('h4').get_text(strip=True).strip()
                    currMeteo.label = labels[i].find('span').get_text(strip=True).strip()
                    currMeteo.svg = str(labels[i].find('svg'))
                    
                    currMeteo.temperatura = temperature[i + 1].get_text(strip=True).strip().encode('ascii','ignore')
                    currMeteo.precipitazioni = precipitazioni[i + 1].find('span').get_text(strip=True).strip()
                    currMeteo.vento = vento[i + 1].find('span').get_text(strip=True).strip()
                    currMeteo.umidita = umidita[i + 1].get_text(strip=True).strip()
                    currMeteo.pressione = pressione[i + 1].get_text(strip=True).strip()
                    #currMeteo.uv = uv[i + 1]['data-info']
                    result[self.name].append(currMeteo.__dict__)
        finally:             
            return result
    
    def get_meteo_week(self, parsed_html):
        result = []
        return result
    