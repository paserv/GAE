from bs4 import BeautifulSoup
from abstract_meteo import AbstractMeteo
import data_controller as dc
from ilmeteo_model import DayMeteo
from google.appengine.api import urlfetch
import logging
import sys, traceback

class ImplIlMeteo(AbstractMeteo):
    base_url = 'https://www.ilmeteo.it/portale/meteo/previsioni1.php?'
    name = 'ilmeteo'
    
    def get_query_url(self, comune, day):
        id_ilmeteo = dc.get_id_ilmeteo(comune)
        return {
            '0': self.base_url + 'c=' + id_ilmeteo + '&g=0',
            '1': self.base_url + 'c=' + id_ilmeteo + '&g=1',
            '2': self.base_url + 'c=' + id_ilmeteo + '&g=2',
            '3': self.base_url + 'c=' + id_ilmeteo + '&g=3',
            '4': self.base_url + 'c=' + id_ilmeteo + '&g=4',
            '5': self.base_url + 'c=' + id_ilmeteo + '&g=5',
            '6': self.base_url + 'c=' + id_ilmeteo + '&g=6',
        }.get(day)
        
    def get_meteo_by_day(self, comune, day):
        logging.debug('Get Il Meteo: ' + comune + ' - ' + day)
        result = {}
        result[self.name] = []
        try:
            url = self.get_query_url(comune, day)
            request = urlfetch.fetch(url)
            if request.status_code == 200:
                html_data = request.content
                parsed_html = BeautifulSoup(html_data, "lxml")
                
                dark_rows = parsed_html.body.find_all('tr', attrs={'class':'dark'})
                light_rows = parsed_html.body.find_all('tr', attrs={'class':'light'})
                
                for dark_row in dark_rows:
                    currMeteo = DayMeteo()
                    currMeteo.ora = dark_row.find('span', attrs={'class':'ora'}).get_text(strip=True).strip() + ":00"
                    label = dark_row.find('td', attrs={'class':'col3'}).get_text(strip=True).strip()
                    currMeteo.setLabel(label, currMeteo.ora)                   
                    currMeteo.temperatura_value = dark_row.find('td', attrs={'class':'col4'}).get_text(strip=True).strip()[:-1]
                    currMeteo.temperatura = currMeteo.temperatura_value + u'\N{DEGREE SIGN}' + " C"
                    
                    col6 = dark_row.find('td', attrs={'class':'col6'})
                    currMeteo.vento_descr = col6.find('span', attrs={'class':'descri'}).get_text(strip=True).strip()
                    if col6.find('abbr'):
                        currMeteo.vento = col6.find('abbr').text + " Km/h"
                    else:
                        currMeteo.vento = "0 Km/h"
                    currMeteo.umidita = col6.find('span', attrs={'class':'hdata'}).get_text(strip=True).strip()
                    
                    col7 = dark_row.find('td', attrs={'class':'col7'})
                    currMeteo.precipitazioni_descr = col7.find('span', attrs={'class':'descri'}).get_text(strip=True).strip()
                    currMeteo.precipitazioni = col7.find('span').text.replace(currMeteo.precipitazioni_descr, '')
                    currMeteo.precipitazioni_value= currMeteo.precipitazioni[:-3]
                    if currMeteo.precipitazioni == ' ':
                        currMeteo.precipitazioni = '0.0 mm'
                        currMeteo.precipitazioni_value = '0'
                    currMeteo.grandine = col7.find('span', attrs={'class':'hdata'}).get_text(strip=True).strip()
                    
                    currMeteo.pressione = dark_row.find('td', attrs={'class':'col8'}).find('span', attrs={'class':'hdata'}).get_text(strip=True).strip()[:-2] + " mbar"
                    
                    col9 = dark_row.find('td', attrs={'class':'col9'})
                    currMeteo.visibilita_descr = col9.find('span', attrs={'class':'descri'}).get_text(strip=True).strip()
                    currMeteo.visibilita = col9.find('span').text.replace(currMeteo.visibilita_descr, '')
                    currMeteo.temp_percepita = col9.find('span', attrs={'class':'hdata'}).get_text(strip=True).strip()[:-1] + " C"
                    
                    col10 = dark_row.find('td', attrs={'class':'col10'})
                    currMeteo.ur = col10.find('span').get_text(strip=True).strip()
                    currMeteo.uv = col10.find('span', attrs={'class':'hdata'}).get_text(strip=True).strip()
                    result[self.name].append(currMeteo.__dict__)
                                                           
                for light_row in light_rows:
                    currMeteo = DayMeteo()
                    currMeteo.ora = light_row.find('span', attrs={'class':'ora'}).get_text(strip=True).strip() + ":00"
                    label = light_row.find('td', attrs={'class':'col3'}).get_text(strip=True).strip()
                    currMeteo.setLabel(label, currMeteo.ora)
                    currMeteo.temperatura_value = light_row.find('td', attrs={'class':'col4'}).get_text(strip=True).strip()[:-1]
                    currMeteo.temperatura = currMeteo.temperatura_value + u'\N{DEGREE SIGN}' + " C"
                    
                    col6 = light_row.find('td', attrs={'class':'col6'})
                    currMeteo.vento_descr = col6.find('span', attrs={'class':'descri'}).get_text(strip=True).strip()
                    if col6.find('abbr'):
                        currMeteo.vento = col6.find('abbr').text + " Km/h"
                    else:
                        currMeteo.vento = "0 Km/h"
                    currMeteo.umidita = col6.find('span', attrs={'class':'hdata'}).get_text(strip=True).strip()
                    
                    col7 = light_row.find('td', attrs={'class':'col7'})
                    currMeteo.precipitazioni_descr = col7.find('span', attrs={'class':'descri'}).get_text(strip=True).strip()
                    currMeteo.precipitazioni = col7.find('span').text.replace(currMeteo.precipitazioni_descr, '')
                    currMeteo.precipitazioni_value= currMeteo.precipitazioni[:-3]
                    if currMeteo.precipitazioni == ' ':
                        currMeteo.precipitazioni = '0.0 mm'
                        currMeteo.precipitazioni_value = '0'
                    currMeteo.grandine = col7.find('span', attrs={'class':'hdata'}).get_text(strip=True).strip()
                    
                    currMeteo.pressione = light_row.find('td', attrs={'class':'col8'}).find('span', attrs={'class':'hdata'}).get_text(strip=True).strip()[:-2] + " mbar"
                    
                    col9 = light_row.find('td', attrs={'class':'col9'})
                    currMeteo.visibilita_descr = col9.find('span', attrs={'class':'descri'}).get_text(strip=True).strip()
                    currMeteo.visibilita = col9.find('span').text.replace(currMeteo.visibilita_descr, '')
                    currMeteo.temp_percepita = col9.find('span', attrs={'class':'hdata'}).get_text(strip=True).strip()[:-1] + " C"
                    
                    col10 = light_row.find('td', attrs={'class':'col10'})
                    currMeteo.ur = col10.find('span').get_text(strip=True).strip()
                    currMeteo.uv = col10.find('span', attrs={'class':'hdata'}).get_text(strip=True).strip()
                    result[self.name].append(currMeteo.__dict__)
        except:
            traceback.print_exc(file=sys.stdout)
        finally:             
            return result
    