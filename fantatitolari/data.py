import csv
import json
import model
from google.appengine.ext import ndb

def get_player_list():
    result = {}
    with open('static/lista_giocatori.csv', 'rb') as players:
        reader = csv.reader(players, delimiter=';')
        for row in reader:
            id = row[0]
            role = row[1]
            name = row[2]
            team = row[3]
            quot = row[4]
            iconUrl = 'https://content.fantagazzetta.com/web/campioncini/small/' + name.replace(' ', '-') + '.png'
            teamUrl = 'http://content.fantagazzetta.com/web/img/team/' + row[3].lower() + '.png'
            statsUrl = 'https://www.fantagazzetta.com/squadre/Milan/' + name.replace(' ', '-') + '/' + id
            playerLabel = row[2] + ' (' + row[1] + ')'
            result[name] = {'id': id, 'role': role, 'name': name, 'team': team, 'quot': quot, 'iconUrl': iconUrl, 'teamUrl': teamUrl, 'playerLabel': playerLabel, 'statsUrl': statsUrl }
    return result

def save_team(user, inputteam):
    data = json.loads(inputteam)
    
    userEntity = model.User(key = ndb.Key('User', user.email()))
    userEntity.put()
    
    
    teamEntity = model.Team(key = ndb.Key('Team', data['teamName'], parent = userEntity.key))
    teamEntity.put()
        
    for player in data['teamPlayers']:
        teamplayer = model.TeamPlayer(key = ndb.Key('TeamPlayer', player, parent = teamEntity.key))
        teamplayer.put()
        
def get_teams(user):
    result = {}
    data = []
    result['data'] = data
    teams = model.Team.query(ancestor=ndb.Key('User', user.email()))
    for team in teams:
        result['data'].append(team.key.get())
    return result
        

def get_team_players(user, name):
    return "NON SO"
    
    
    
    
    
    