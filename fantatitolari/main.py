from flask import Flask, render_template, send_from_directory, jsonify, request
from google.appengine.api import users
import os

import data
import scraper

app = Flask(__name__)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

def render_page(template, title, icon):
    user = users.get_current_user()
    username = str(user).split('@')[0]
    if user:
        logout_url = users.create_logout_url('/')
        return render_template(template, title = title, icon = icon, logout_url = logout_url, user=username)
    else:
        login_url = users.create_login_url('/')
        return render_template('home.html', title = 'Login', icon = 'home', login_url = login_url)

##### VIEWS #####
@app.route('/')
def home():
    return render_page('home.html', 'Home Page', 'home');

@app.route('/cs')
def crea_squadra():
    return render_page('crea_squadra.html', 'Crea Squadra', 'add_circle_outline');
    
@app.route('/ms')
def modifica_squadra():
    user = users.get_current_user()
    username = str(user).split('@')[0]
    if user:
        logout_url = users.create_logout_url('/')
        teams = data.get_teams(user)['teams']
        return render_template('modifica_squadra.html', title="Modifica Squadra", icon = "mode_edit", teams=teams, logout_url = logout_url, user=username)
    else:
        login_url = users.create_login_url('/ms')
        return render_template('home.html', login_url = login_url, title="Home Page", icon = "home")

@app.route('/is')
def importa_squadra():
    return render_page('importa_squadra.html', 'Importa Squadra', 'import_export');

@app.route('/tit')
def titolari():
    user = users.get_current_user()
    username = str(user).split('@')[0]
    if user:
        logout_url = users.create_logout_url('/')
        teams = data.get_teams(user)['teams']
        return render_template('titolari.html', title="Verifica Titolari", icon = "directions_run", teams=teams, logout_url = logout_url, user=username)
    else:
        login_url = users.create_login_url('/')
        return render_template('home.html', login_url = login_url, title="Home Page", icon = "home")

##### API ##### 
@app.route('/get_players')
def get_players():
    result = data.get_player_list()
    return jsonify(result)

@app.route('/save_team', methods=['POST'])
def save_team():
    user = users.get_current_user()
    if user:
        data.save_team(user, request.data)
        return "Squadra Salvata con successo"
    else:
        return "Login necessario"

@app.route('/get_teams')
def get_teams():
    user = users.get_current_user()
    if user:
        return jsonify(data.get_teams(user))
    else:
        return {}

@app.route('/get_team_players/<team>')
def get_team_players(team):
    user = users.get_current_user()
    if user:
        result = data.get_team_players(user, team)
        return jsonify(result)
    else:
        return {}

@app.route('/delete_team/<team>', methods=['DELETE'])
def delete_team(team):
    user = users.get_current_user()
    if user:
        data.delete_team(users.get_current_user(), team)
        return 'Eliminazione squadra riuscita con successo', 200
    else:
        return "Login necessario"

@app.errorhandler(400)
@app.errorhandler(500)
def server_error(e):
    return "Error: " + str(e)

##### Data Scraper #####
@app.route('/gazzetta/matches')
def get_matches():
    matches = scraper.matches()
    return jsonify(matches)

@app.route('/gazzetta', methods=['POST'])
def get_titolari_gazzetta():
    result = scraper.gazzetta(request.data)
    return jsonify(result)

@app.route('/fantagazzetta', methods=['POST'])
def get_titolari_fantagazzetta():
    result = scraper.fantagazzetta(request.data)
    return jsonify(result)
    
@app.route('/sky', methods=['POST'])
def get_titolari_sky():
    result = scraper.sky(request.data)
    return jsonify(result)

@app.route('/mediaset', methods=['POST'])
def get_titolari_mediaset():
    result = scraper.mediaset(request.data)
    return jsonify(result)

@app.route('/import', methods=['POST'])
def import_team():
    lega = request.form['lega']
    squadra = request.form['squadra']
    user = users.get_current_user()
    if user:
        team = scraper.get_team(lega, squadra)
        data.save_team(users.get_current_user(), team)
        return "Squadra Salvata con successo"
    else:
        return "Login necessario"