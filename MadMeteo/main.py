import os
import json
from flask import Flask, render_template, send_from_directory, request, jsonify
from meteoit.meteoit_impl import ImplMeteoIt

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def home():
    return render_template('home.html', title="Home Page", icon = "home")

#@app.route('/istat_code/<comune>', methods=['POST'])
#def istat_code(comune):
#    return dc.get_istat_code(comune)

@app.route('/meteoit/<comune>/<giorno>', methods=['POST'])
def prev_meteo(comune, giorno):
    meteo_it = ImplMeteoIt()
    meteoit_result = meteo_it.get_meteo_by_day(comune, giorno)
    return jsonify(meteoit_result)

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