from flask import Flask, render_template, send_from_directory, jsonify, request
from google.appengine.api import users, taskqueue
import os

import data
import scraper

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def home():
    user = users.get_current_user()
    if user:
        logout_url = users.create_logout_url('/')
        return render_template('home.html', logout_url = logout_url, title="Home Page", icon = "home")
    else:
        login_url = users.create_login_url('/')
        return render_template('home.html', login_url = login_url, title="Home Page", icon = "home")

@app.route('/cs')
def crea_squadra():
    user = users.get_current_user()
    if user:
        return render_template('crea_squadra.html', title="Crea Squadra", icon = "home")
    else:
        login_url = users.create_login_url('/')
        return render_template('home.html', login_url = login_url, title="Home Page", icon = "home")
    
@app.route('/ms')
def modifica_squadra():
    user = users.get_current_user()
    if user:
        teams = data.get_teams(user)['teams']
        return render_template('modifica_squadra.html', title="Modifica Squadra", icon = "home", teams=teams)
    else:
        login_url = users.create_login_url('/')
        return render_template('home.html', login_url = login_url, title="Home Page", icon = "home")

@app.route('/tit')
def titolari():
    user = users.get_current_user()
    if user:
        teams = data.get_teams(user)['teams']
        return render_template('titolari.html', title="Verifica Titolari", icon = "home", teams=teams)
    else:
        login_url = users.create_login_url('/')
        return render_template('home.html', login_url = login_url, title="Home Page", icon = "home")
    
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
@app.route('/gazzetta/<giornata>')
def get_titolari_fg(giornata):
    result = scraper.gazzetta(giornata)
    return jsonify(result);



##### ADMIN #####
@app.route('/enqueue_load_players')
def enqueue_load_players():
    taskqueue.add(url='/load_players')
    return '', 200

@app.route('/load_players', methods=['POST'])
def load_players():
    data.load_players()
    return '', 200