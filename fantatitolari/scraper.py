from google.appengine.api import urlfetch
from bs4 import BeautifulSoup

def matches(giornata):
    link = "http://www.gazzetta.it/Calcio/prob_form/"
    daily_matches = {}
    try:
        request = urlfetch.fetch(link)
        if request.status_code == 200:        
            html_data = request.content
            parsed_html = BeautifulSoup(html_data, "html.parser")
    
            parsed_gior = parsed_html.body.find('div', attrs={'class': 'mainHeading'})
            curr_giorn = parsed_gior.find('h3').get_text(strip=True).strip()
    
            if curr_giorn[:2] == giornata:
                matches = parsed_html.body.find_all('div', attrs={'class': 'matchFieldContainer'})
                for match in matches:
                    home_team = match.find('div', attrs={'class': 'homeTeam'}).find('a').get_text(strip=True).strip().lower()
                    away_team = match.find('div', attrs={'class': 'awayTeam'}).find('a').get_text(strip=True).strip().lower()
    
                    daily_matches[home_team.lower()] = {'home': home_team.lower(), 'away': away_team.lower()}
                    daily_matches[away_team.lower()] = {'home': home_team.lower(), 'away': away_team.lower()}
    finally:
        return daily_matches   
    
    
def gazzetta(giornata):
    link = "http://www.gazzetta.it/Calcio/prob_form/"
    result = {}
    try:
        request = urlfetch.fetch(link)
        if request.status_code == 200:        
            html_data = request.content
            parsed_html = BeautifulSoup(html_data, "html.parser")
    
            parsed_gior = parsed_html.body.find('div', attrs={'class': 'mainHeading'})
            curr_giorn = parsed_gior.find('h3').get_text(strip=True).strip()
    
            if curr_giorn[:2] == giornata:
                matches = parsed_html.body.find_all('div', attrs={'class': 'matchFieldContainer'})
                for match in matches:
                    home_team = match.find('div', attrs={'class': 'homeTeam'}).find('a').get_text(strip=True).strip().lower()
                    away_team = match.find('div', attrs={'class': 'awayTeam'}).find('a').get_text(strip=True).strip().lower()
                    result[home_team.lower()] = []
                    result[away_team.lower()] = []
    
                    titolari = match.find_all('ul', attrs={'class': 'team-players'})
    
                    titolari_home = titolari[0].find_all('span', attrs={'class': 'team-player'})
                    for titolare in titolari_home:
                        result[home_team.lower()].append(titolare.text.lower())
    
                    titolari_away = titolari[1].find_all('span', attrs={'class': 'team-player'})
                    for titolare in titolari_away:
                        result[away_team.lower()].append(titolare.text.lower())
    finally:
        return result   
    
def fantagazzetta(giornata):
    link = "https://www.fantagazzetta.com/probabili-formazioni-serie-a"
    result = {}
    try:
        request = urlfetch.fetch(link)
        if request.status_code == 200:
            html_data = request.content
            parsed_html = BeautifulSoup(html_data, "html.parser")
    
            parsed_gior = parsed_html.body.find('p', attrs={'class': 'titalign'}).text
    
            if parsed_gior[10:12] == giornata:
                matches = parsed_html.body.select('div.in.no-gutter')
                for match in matches:
                    teams = match.find_all('h3', attrs={'class': 'team-name'})
                    if teams:
                        home_team = teams[0].get_text(strip=True).strip().lower()
                        away_team = teams[1].get_text(strip=True).strip().lower()
                        result[home_team] = []
                        result[away_team] = []
    
                        titolari_home = match.select('div.pgroup.lf')
                        for titolare in titolari_home[0:11]:
                            result[home_team].append(titolare.find('a').text.lower())
    
                        titolari_away = match.select('div.pgroup.rt')
                        for titolare in titolari_away[0:11]:
                            result[away_team].append(titolare.find('a').text.lower())
    finally:
        return result
