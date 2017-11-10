from bs4 import BeautifulSoup
from abstract_meteo import AbstractMeteo
import data_controller as dc
import json
from meteoit_model import DayMeteo
from google.appengine.api import urlfetch

class ImplMeteoIt(AbstractMeteo):
    base_url = 'http://www.meteo.it/meteo/'
    
    def get_query_url(self, comune, day):
        nome_comune = comune.split(' ')[0]
        istat_code = dc.get_istat_code(nome_comune)[-5:]
        return {
            '0': self.base_url + nome_comune.lower() + '-' + istat_code,
            '1': self.base_url + nome_comune.lower() + '-domani-' + istat_code,
            '2': self.base_url + nome_comune.lower() + '-dopodomani-' + istat_code,
            '3': self.base_url + nome_comune.lower() + '-3-giorni-' + istat_code,
            '4': self.base_url + nome_comune.lower() + '-4-giorni-' + istat_code,
            '5': self.base_url + nome_comune.lower() + '-5-giorni-' + istat_code,
            '6': self.base_url + nome_comune.lower() + '-6-giorni-' + istat_code,
        }.get(day)
        
    def get_meteo_by_day(self, comune, day):
        result = []
        try:
            url = self.get_query_url(comune, day)
            request = urlfetch.fetch(url)
            if request.status_code == 200:
                html_data = request.content
                parsed_html = BeautifulSoup(html_data, "html.parser")
                
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
                    currMeteo.giorno = day
                    currMeteo.ora = ore[i].find('h4').get_text(strip=True).strip()
                    currMeteo.label = labels[i].find('span').get_text(strip=True).strip()
                    currMeteo.temperatura = temperature[i + 1].get_text(strip=True).strip().encode('ascii','ignore')
                    currMeteo.precipitazioni = precipitazioni[i + 1].find('span').get_text(strip=True).strip()
                    currMeteo.vento = vento[i + 1].find('span').get_text(strip=True).strip()
                    currMeteo.umidita = umidita[i + 1].get_text(strip=True).strip()
                    currMeteo.pressione = pressione[i + 1].get_text(strip=True).strip()
                    #currMeteo.uv = uv[i + 1]['data-info']
                    result.append(currMeteo.__dict__)
        finally:
            return result
    
    def get_meteo_week(self, comune, when):
        return None

    