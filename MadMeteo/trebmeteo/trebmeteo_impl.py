from bs4 import BeautifulSoup
from abstract_meteo import AbstractMeteo
from trebmeteo_model import DayMeteo
from google.appengine.api import urlfetch
import sys, traceback
import unicodedata

class ImplTreBMeteo(AbstractMeteo):
    base_url = 'https://www.3bmeteo.com/meteo/'
    name = 'trebmeteo'
    
    def get_query_url(self, comune, day):
        nome_com = comune.replace(' ', '+')
        nome_comune = unicodedata.normalize('NFKD', nome_com).encode('ASCII', 'ignore')
        return {
            '0': self.base_url + nome_comune.lower(),
            '1': self.base_url + nome_comune.lower() + '/dettagli_orari/1',
            '2': self.base_url + nome_comune.lower() + '/dettagli_orari/2',
            '3': self.base_url + nome_comune.lower() + '/dettagli_orari/3',
            '4': self.base_url + nome_comune.lower() + '/dettagli_orari/4',
            '5': self.base_url + nome_comune.lower() + '/dettagli_orari/5',
            '6': self.base_url + nome_comune.lower() + '/dettagli_orari/6',
        }.get(day)
        
    def get_meteo_by_day(self, comune, day):
        result = {}
        result[self.name] = []
        try:
            if day != '0':
                previousDay = str(int(day) - 1)
                previousDayPrev = self.get_meteo_by_page(comune, previousDay)
                result[self.name].extend(previousDayPrev[-6:])
            currentDayPrev = self.get_meteo_by_page(comune, day)
            result[self.name].extend(currentDayPrev[:-6])
        except:
            traceback.print_exc(file=sys.stdout)
        finally:             
            return result
    
    def get_meteo_by_page(self, comune, page):
        result = []
        try:
            url = self.get_query_url(comune, page)
            request = urlfetch.fetch(url)
            if request.status_code == 200:
                html_data = request.content
                parsed_html = BeautifulSoup(html_data, "lxml")
                
                rows = parsed_html.body.select('div.row-table.noPad')
                iterrows = iter(rows)
                next(iterrows)
                for row in iterrows:
                    currMeteo = DayMeteo()
                    currMeteo.ora = row.find('div', attrs={'class':'col-xs-1-4'}).get_text(strip=True).strip()
                    label = row.find('div', attrs={'class':'col-xs-2-4'})
                    if label:
                        currMeteo.label = row.find('div', attrs={'class':'col-xs-2-4'}).get_text(strip=True).strip()
                    temps = row.find_all('span', attrs={'class':'switchcelsius'})
                    currMeteo.temperatura_value = temps[0].get_text(strip=True).strip()[:-1]
                    currMeteo.temperatura = currMeteo.temperatura_value + u'\N{DEGREE SIGN}' + " C"
                    currMeteo.percepita = temps[1].get_text(strip=True).strip()
                    if len(temps) == 3:
                        currMeteo.temp_vento = temps[2].get_text(strip=True).strip()
                    currMeteo.precipitazioni = row.find('div', attrs={'class':'altriDati-precipitazioni'}).get_text(strip=True).strip()
                    currMeteo.precipitazioni_value = currMeteo.precipitazioni[:-3]
                    currMeteo.vento = row.find('div', attrs={'class':'altriDati-venti'}).get_text().strip().split(' ')[0] + ' Km/h'
                    currMeteo.umidita = row.find('div', attrs={'class':'altriDati-umidita'}).get_text(strip=True).strip()
                    qn = row.find('div', attrs={'class':'altriDati-QN'})
                    if qn:
                        currMeteo.neve = qn.get_text(strip=True).strip()
                    mare = row.find('div', attrs={'class':'altriDati-mare'})
                    if mare:
                        currMeteo.mare = mare.find('small').get_text(strip=True).strip()
                    onda = row.find('div', attrs={'class':'altriDati-onda'})
                    if onda:
                        currMeteo.onda = onda.get_text().strip()
                    currMeteo.pressione = row.find('div', attrs={'class':'altriDati-pressione'}).get_text(strip=True).strip() + ' mbar'
                    currMeteo.uv = row.find('div', attrs={'class':'altriDati-raggiuv'}).get_text(strip=True).strip().split('(')[1][:-1]
                    result.append(currMeteo.__dict__)
        except:
            traceback.print_exc(file=sys.stdout)
        finally:             
            return result
        
    def get_meteo_week(self, parsed_html):
        result = []
        return result
    