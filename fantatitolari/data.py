import csv

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
            