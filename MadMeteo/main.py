import os
import json
from flask import Flask, render_template, send_from_directory, request, jsonify
from meteoit.meteoit_impl import ImplMeteoIt
from trebmeteo.trebmeteo_impl import ImplTreBMeteo
import logging

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
def home():
    return render_template('home.html', title="Home Page", icon = "home")

@app.route('/meteoit/<comune>/<giorno>', methods=['POST'])
def meteoit_prev(comune, giorno):
    meteo_it = ImplMeteoIt()
    meteoit_result = meteo_it.get_meteo_by_day(comune, giorno)
    return jsonify(meteoit_result)

@app.route('/trebmeteo/<comune>/<giorno>', methods=['POST'])
def treb_meteo_prev(comune, giorno):
    treb_meteo = ImplTreBMeteo()
    treb_meteo_result = treb_meteo.get_meteo_by_day(comune, giorno)
    return jsonify(treb_meteo_result)

@app.route('/ilmeteo/<comune>/<giorno>', methods=['POST'])
def il_meteo_prev(comune, giorno):
    result = {}
    result['ilmeteo'] = []
    return jsonify(result)

@app.route('/meteoitalia/<comune>/<giorno>', methods=['POST'])
def meteoitalia_prev(comune, giorno):
    result = {}
    result['meteoitalia'] = []
    return jsonify(result)

@app.route('/test', methods=['GET'])
def get_comuni():
    comune = request.args['comune']
    day = request.args['giorno']
    meteo_it = ImplMeteoIt()
    #result = meteo_it.get_query_url(comune, day)
    result = meteo_it.get_meteo_by_day(comune, day)
    return jsonify(json.dumps(result))

@app.errorhandler(400)
@app.errorhandler(500)
def server_error(e):
    return "Error: " + str(e)