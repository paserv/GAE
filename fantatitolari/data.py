import csv
import json
import model
from google.appengine.ext import ndb

def get_player_list():
    result = {}
    players = model.Anagrafica.query()
    for player in players.iter():
        result[player.name] = {'id': player.ident, 'role': player.role, 'name': player.name, 'team': player.team, 'quot': player.quot, 'iconUrl': player.iconUrl, 'teamUrl': player.teamUrl, 'playerLabel': player.playerLabel, 'statsUrl': player.statsUrl }
    return result

def save_team(user, inputteam):
    data = json.loads(inputteam)
    
    delete_team(user, data['teamName'])
    userKey = ndb.Key('User', user.email())
    teamKey = ndb.Key('Team', data['teamName'], parent=userKey)
    #team_players = model.TeamPlayer.query(ancestor=teamKey)
    #for player in team_players:
    #    player.key.delete()
    
    userEntity = model.User(key = userKey)
    userEntity.put()
    
    teamEntity = model.Team(key = teamKey)
    teamEntity.put()
        
    for player in data['teamPlayers']:
        teamplayer = model.TeamPlayer(key = ndb.Key('TeamPlayer', player, parent = teamEntity.key))
        teamplayer.put()
        
def get_teams(user):
    result = []
    teams = model.Team.query(ancestor=ndb.Key('User', user.email()))
    for team in teams:
        result.append(team.key.string_id())
    return result
        

def get_team_players(user, team):
    result = {}
    result['players'] = []
    userKey = ndb.Key('User', user.email())
    teamKey = ndb.Key('Team', team, parent=userKey)
    team_players = model.TeamPlayer.query(ancestor=teamKey)
    for player in team_players:
        playerKey = ndb.Key('Anagrafica', player.key.string_id())
        anag = playerKey.get()
        result['players'].append({'id' : anag.ident, 'role' : anag.role, 'name' : anag.name, 'team' : anag.team, 'quot' : anag.quot, 'iconUrl' : anag.iconUrl, 'teamUrl' : anag.teamUrl, 'statsUrl' : anag.statsUrl, 'playerLabel' : anag.playerLabel})
    return result
    
def delete_team(user, team):
    userKey = ndb.Key('User', user.email())
    teamKey = ndb.Key('Team', team, parent=userKey)
    team_players = model.TeamPlayer.query(ancestor=teamKey)
    for player in team_players:
        player.key.delete()
    teamKey.delete();
    
    
##### ADMIN #####
def load_players():
    with open('static/lista_giocatori.csv', 'rb') as players:
        reader = csv.reader(players, delimiter=';')
        for row in reader:
            anagraficaEntity = model.Anagrafica(key = ndb.Key('Anagrafica', row[0]))
            anagraficaEntity.ident = int(row[0])
            anagraficaEntity.role = row[1]
            anagraficaEntity.name = row[2]
            anagraficaEntity.team = row[3]
            anagraficaEntity.quot = row[4]
            anagraficaEntity.iconUrl = 'https://content.fantagazzetta.com/web/campioncini/small/' + row[2].replace(' ', '-') + '.png'
            anagraficaEntity.teamUrl = 'http://content.fantagazzetta.com/web/img/team/' + row[3].lower() + '.png'
            anagraficaEntity.statsUrl = 'https://www.fantagazzetta.com/squadre/Milan/' + row[2].replace(' ', '-') + '/' + row[0]
            anagraficaEntity.playerLabel = row[2] + ' (' + row[1] + ')'
            anagraficaEntity.put()    
    
    