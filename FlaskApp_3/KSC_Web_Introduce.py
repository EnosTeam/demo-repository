from flask import render_template, Blueprint

Introduce = Blueprint('Introduce', __name__)

@Introduce.route('/i')
def intro():
    return render_template('KSC_Web_introduce.html')