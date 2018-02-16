import os
import json
from flask import Flask, render_template, send_from_directory, request, jsonify, Response
from meteoit.meteoit_impl import ImplMeteoIt
from trebmeteo.trebmeteo_impl import ImplTreBMeteo
from ilmeteo.ilmeteo_impl import ImplIlMeteo
from meteolive.meteolive_impl import ImplMeteoLive
from prev_model import Previsione, PrevisioneOraria
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
    il_meteo = ImplIlMeteo()
    il_meteo_result = il_meteo.get_meteo_by_day(comune, giorno)
    return jsonify(il_meteo_result)

@app.route('/meteolive/<comune>/<giorno>', methods=['POST'])
def meteolive_prev(comune, giorno):
    meteo_live = ImplMeteoLive()
    meteo_live_result = meteo_live.get_meteo_by_day(comune, giorno)
    return jsonify(meteo_live_result)

@app.route('/test', methods=['POST'])
def test():
    previsioni = []
    prev1 = PrevisioneOraria("2018-02-13T11:00:00", "2018-02-13T12:00:00", "09", "Piovoso", 1, 16, 58, 5, 999.6, 2, 0.5)
    prev2 = PrevisioneOraria("2018-02-13T12:00:00", "2018-02-13T13:00:00", "09", "Piovoso Assai", 0.6, 162.6, 8.8, 4, 999.4)
    prev3 = PrevisioneOraria("2018-02-13T13:00:00", "2018-02-13T14:00:00", "09", "Piovoso", 3, 157.4, 8.8, 10, 1001)
    previsioni.extend([prev1, prev2, prev3])
    test = Previsione("Afragola", "Campania", previsioni)
    return jsonify(test.toJson())

@app.errorhandler(400)
@app.errorhandler(500)
def server_error(e):
    return "Error: " + str(e)