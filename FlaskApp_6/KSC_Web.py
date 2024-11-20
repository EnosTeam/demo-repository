from flask import Flask, request, render_template, redirect, url_for, flash, session, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__, static_folder='static')
app.secret_key = 'supersecretkey12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///KSC_Web_DataBase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)

from DataBase.KSC_Web_DB import db
db.init_app(app)
with app.app_context():
    db.create_all()
    
from KSC_Web_Main_New import Main
app.register_blueprint(Main)

from KSC_Web_Introduce import Introduce
app.register_blueprint(Introduce)

from KSC_Web_Sign_InUp import InUp
app.register_blueprint(InUp)

from KSC_Web_Notice import Notice
app.register_blueprint(Notice)

from KSC_Web_Post import Posts
app.register_blueprint(Posts)

from KSC_Web_Box import Box
app.register_blueprint(Box)

from KSC_Web_MyPage import MyPage
app.register_blueprint(MyPage)

from KSC_Web_DB_Control import admin_bp
app.register_blueprint(admin_bp, url_prefix='/admin')

if __name__ == '__main__':
    app.run(debug=True)