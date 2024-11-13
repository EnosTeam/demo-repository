from flask import Flask, request, render_template, redirect, url_for, flash, session, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

Introduce = Blueprint('Introduce', __name__)

@Introduce.route('/i')
def intro():
    return render_template('KSC_Web_introduce.html')