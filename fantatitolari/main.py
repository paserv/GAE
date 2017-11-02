from flask import Flask, render_template, send_from_directory, jsonify, request
from google.appengine.api import users
import os

import data

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
def gestisci_squadra():
    user = users.get_current_user()
    if user:
        return render_template('crea_squadra.html', title="Crea Squadra", icon = "home")
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
    return str(data.get_teams(users.get_current_user()))


@app.errorhandler(400)
@app.errorhandler(500)
def server_error(e):
    return "Error: " + str(e)