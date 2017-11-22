from flask import Flask, render_template, request
from google.appengine.api import users, taskqueue
import data

app = Flask(__name__)

@app.route('/admin/home')
def admin():
    return render_page('admin/home.html', 'Admin Page', 'home')   

@app.route('/admin/lp')
def load_players():
    return render_page('admin/load_players.html', 'Carica Giocatori', 'home')

@app.route('/admin/enqueue_players', methods=['POST'])
def enqueue_players():
    csv_file = request.form['csv']
    taskqueue.add(url='/admin/save_players', params={'csv_file': csv_file})
    return render_page('admin/load_players.html', 'Carica Lista', 'home')

@app.route('/admin/save_players', methods=['POST'])
def save_players():
    csv_file = request.form['csv_file']
    data.load_players(csv_file)
    return '', 200

def render_page(template, title, icon):
    user = users.get_current_user()
    if user:
        logout_url = users.create_logout_url('/admin/home')
        if users.is_current_user_admin():
            return render_template(template, title = title, icon = icon, logout_url = logout_url)
        else:
            return render_template('admin/access_denied.html', title = 'Accesso Negato', icon = 'home', logout_url = logout_url)
    else:
        login_url = users.create_login_url('/')
        return render_template('admin/login.html', title = 'Login', icon = 'home', login_url = login_url)
    
@app.errorhandler(400)
@app.errorhandler(500)
def server_error(e):
    return "Error: " + str(e)