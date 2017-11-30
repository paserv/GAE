from google.appengine.api import urlfetch
from bs4 import BeautifulSoup
from itertools import izip
from unidecode import unidecode
import json
import sys, traceback

def pairwise(iterable):
    a = iter(iterable)
    return izip(a, a)

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
    except:
        traceback.print_exc(file=sys.stdout)
    finally:
        return daily_matches
    
    
def gazzetta(partite_string):
    link = "http://www.gazzetta.it/Calcio/prob_form/"
    result = {}
    partite = json.loads(partite_string)
    try:
        request = urlfetch.fetch(link)
        if request.status_code == 200:        
            html_data = request.content
            parsed_html = BeautifulSoup(html_data, "html.parser")
    
            first_match = parsed_html.body.find('div', attrs={'class': 'matchFieldContainer'})
            first_home_team = first_match.find('div', attrs={'class': 'homeTeam'}).find('a').get_text(strip=True).strip().lower()
            first_away_team = first_match.find('div', attrs={'class': 'awayTeam'}).find('a').get_text(strip=True).strip().lower()
            if (partite[first_home_team]['away'] == first_away_team):
                matches = parsed_html.body.find_all('div', attrs={'class': 'matchFieldContainer'})
                for match in matches:
                    home_team = match.find('div', attrs={'class': 'homeTeam'}).find('a').get_text(strip=True).strip().lower()
                    away_team = match.find('div', attrs={'class': 'awayTeam'}).find('a').get_text(strip=True).strip().lower()
                    result[home_team] = {}
                    result[home_team]['titolari'] = []
                    result[away_team] = {}
                    result[away_team]['titolari'] = []
    
                    homeDetails = match.find('div', attrs={'class': 'homeDetails'})
                    result[home_team]['details'] = str(homeDetails)
                    
                    awayDetails = match.find('div', attrs={'class': 'awayDetails'})
                    result[away_team]['details'] = str(awayDetails)
                    
                    titolari = match.find_all('ul', attrs={'class': 'team-players'})
    
                    titolari_home = titolari[0].find_all('span', attrs={'class': 'team-player'})
                    for titolare in titolari_home:
                        result[home_team]['titolari'].append(titolare.text.lower())
    
                    titolari_away = titolari[1].find_all('span', attrs={'class': 'team-player'})
                    for titolare in titolari_away:
                        result[away_team]['titolari'].append(titolare.text.lower())
    finally:
        return result   
    
def fantagazzetta(partite_string):
    link = "https://www.fantagazzetta.com/probabili-formazioni-serie-a"
    result = {}
    partite = json.loads(partite_string)
    try:
        request = urlfetch.fetch(link)
        if request.status_code == 200:
            html_data = request.content
            parsed_html = BeautifulSoup(html_data, "html.parser")
    
            matches = parsed_html.body.select('div.in.no-gutter')
            first_teams = matches[0].find_all('h3', attrs={'class': 'team-name'})
            first_home_team = first_teams[0].get_text(strip=True).strip().lower()
            first_away_team = first_teams[1].get_text(strip=True).strip().lower()
            
            if (partite[first_home_team]['away'] == first_away_team):
                for match in matches:
                    teams = match.find_all('h3', attrs={'class': 'team-name'})
                    if teams:
                        home_team = teams[0].get_text(strip=True).strip().lower()
                        away_team = teams[1].get_text(strip=True).strip().lower()
                        result[home_team] = {}
                        result[home_team]['titolari'] = []
                        result[away_team] = {}
                        result[away_team]['titolari'] = []
                        
                        teamDetails = match.select('div.probbar.pad10')
                        result[home_team]['details'] = str(teamDetails[0])
                        result[away_team]['details'] = str(teamDetails[1])
                        
                        titolari_home = match.select('div.pgroup.lf')
                        for titolare in titolari_home[0:11]:
                            result[home_team]['titolari'].append(titolare.find('a').text.lower())
                             
                        titolari_away = match.select('div.pgroup.rt')
                        for titolare in titolari_away[0:11]:
                            result[away_team]['titolari'].append(titolare.find('a').text.lower())
    finally:
        return result
    
def sky(partite_string):
    link = "https://sport.sky.it/calcio/serie-a/probabili-formazioni/"
    result = {}
    partite = json.loads(partite_string)
    try:
        request = urlfetch.fetch(link)
        if request.status_code == 200:
            html_data = request.content
            parsed_html = BeautifulSoup(html_data, "html.parser")
    
            matches = parsed_html.body.find_all('span', attrs={'class': 'team'})
            home_formazione = parsed_html.select('div.team-1.left')
            away_formazione = parsed_html.select('div.team-2.right')
            home_teams = []
            away_teams = []
            for x, y in pairwise(matches):
                home_teams.append(x.findNext('span').text.lower())
                away_teams.append(y.findNext('span').text.lower())
    
            first_home_team = home_teams[0]
            first_away_team = away_teams[0]
            if (partite[first_home_team]['away'] == first_away_team):
                for index in range(0,10):
                    curr_home_team = home_teams[index]
                    result[curr_home_team] = {}
                    result[curr_home_team]['titolari'] = []
                    players = home_formazione[index].find_all('li', attrs={'class': 'player'})
                    for player in players:
                        result[curr_home_team]['titolari'].append(unidecode(player.find('span', attrs={'class': 'name'}).text.lower()))
       
                for index in range(0,10):
                    curr_away_team = away_teams[index]
                    result[curr_away_team] = {}
                    result[curr_away_team]['titolari'] = []
                    players = away_formazione[index].find_all('li', attrs={'class': 'player'})
                    for player in players:
                        result[curr_away_team]['titolari'].append(unidecode(player.find('span', attrs={'class': 'name'}).text.lower()))
    finally:
        return result
    
def mediaset(partite_string):
    link = "http://www.sportmediaset.mediaset.it/squadre/probabili_formazioni.shtml"
    result = {}
    partite = json.loads(partite_string)
    try:
        request = urlfetch.fetch(link)
        if request.status_code == 200:
            html_data = request.content
            parsed_html = BeautifulSoup(html_data, "html.parser")
            
            matches = parsed_html.body.find_all('div', attrs={'class': 'boxFormazione'})
            first_teams = matches[0].find_all('span', attrs={'class': 'teamName'})
            first_home_team = first_teams[0].get_text(strip=True).strip().lower()
            first_away_team = first_teams[1].get_text(strip=True).strip().lower()
            
            if (partite[first_home_team]['away'] == first_away_team):
                for match in matches:
                    curr_teams = match.find_all('span', attrs={'class': 'teamName'})
                    home_team = curr_teams[0].get_text(strip=True).strip().lower()
                    away_team = curr_teams[1].get_text(strip=True).strip().lower()
                    result[home_team] = {}
                    result[home_team]['titolari'] = []
                    result[away_team] = {}
                    result[away_team]['titolari'] = []
                    
                    home_players = match.find('li', attrs={'class': 'home'}).find_all('span', attrs={'class': 'nome'})
                    for titolare in home_players:
                        result[home_team]['titolari'].append(titolare.text.lower())
                    
                    away_players = match.find('li', attrs={'class': 'away'}).find_all('span', attrs={'class': 'nome'})
                    for titolare in away_players:
                        result[away_team]['titolari'].append(titolare.text.lower())
    finally:
        return result
    
