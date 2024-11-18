from flask import Flask, render_template, Blueprint

app = Flask(__name__, static_folder='static')
app.secret_key = 'supersecretkey12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)

Main = Blueprint('Main', __name__)

@Main.route('/')
def door():
    return render_template('KSC_Web_Main_New.html')

@Main.route('/h')
def home():
    return render_template('KSC_Web_Main_New.html')

@Main.route('/welcome/<last_name>/<first_name>')
def welcome(first_name, last_name):
    return render_template('welcome.html', first_name=first_name, last_name=last_name)