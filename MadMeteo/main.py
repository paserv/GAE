from flask import Flask, render_template, send_from_directory, jsonify, request
from google.appengine.api import users
import os

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

@app.errorhandler(400)
@app.errorhandler(500)
def server_error(e):
    return "Error: " + str(e)