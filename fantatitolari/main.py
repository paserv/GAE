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
    if user:
        logout_url = users.create_logout_url('/')
        return render_template(template, title = title, icon = icon, logout_url = logout_url, user=user)
    else:
        login_url = users.create_login_url('/')
        return render_template('home.html', title = 'Login', icon = 'home', login_url = login_url)

##### VIEWS #####
@app.route('/')
def home():
    return render_page('home.html', 'Home Page', 'home');

@app.route('/cs')
def crea_squadra():
    return render_page('crea_squadra.html', 'Crea Squadra', 'home');
    
@app.route('/ms')
def modifica_squadra():
    user = users.get_current_user()
    if user:
        logout_url = users.create_logout_url('/')
        teams = data.get_teams(user)['teams']
        return render_template('modifica_squadra.html', title="Modifica Squadra", icon = "home", teams=teams, logout_url = logout_url, user=user)
    else:
        login_url = users.create_login_url('/ms')
        return render_template('home.html', login_url = login_url, title="Home Page", icon = "home")

@app.route('/tit')
def titolari():
    user = users.get_current_user()
    if user:
        logout_url = users.create_logout_url('/')
        teams = data.get_teams(user)['teams']
        return render_template('titolari.html', title="Verifica Titolari", icon = "home", teams=teams, logout_url = logout_url, user=user)
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
    data.save_team(users.get_current_user(), request.data)
    return "Squadra Salvata con successo"

@app.route('/get_teams')
def get_teams():
    return jsonify(data.get_teams(users.get_current_user()))

@app.route('/get_team_players/<team>')
def get_team_players(team):
    result = data.get_team_players(users.get_current_user(), team)
    return jsonify(result)

@app.route('/delete_team/<team>', methods=['DELETE'])
def delete_team(team):
    data.delete_team(users.get_current_user(), team)
    return 'Eliminazione squadra riuscita con successo', 200

@app.errorhandler(400)
@app.errorhandler(500)
def server_error(e):
    return "Error: " + str(e)

##### Data Scraper #####
@app.route('/gazzetta/matches/<giornata>')
def get_matches(giornata):
    matches = scraper.matches(giornata)
    return jsonify(matches);

@app.route('/gazzetta/<giornata>')
def get_titolari_gazzetta(giornata):
    result = scraper.gazzetta(giornata)
    return jsonify(result);

@app.route('/fantagazzetta/<giornata>')
def get_titolari_fantagazzetta(giornata):
    result = scraper.fantagazzetta(giornata)
    return jsonify(result);

@app.route('/sky/<giornata>')
def get_titolari_sky(giornata):
    result = scraper.sky(giornata)
    return jsonify(result);