from flask import request, render_template, redirect, url_for, flash, session, Blueprint
from DataBase.KSC_Web_Sign_InUp_DB import db, User

InUp = Blueprint('InUp', __name__)

@InUp.route('/inup', methods=['GET', 'POST'])
def inup():
    if request.method == 'POST':
        username = request.form['ID']
        password = request.form['PW']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            session['first_name'] = user.first_name
            session['last_name'] = user.last_name
            return redirect(url_for('Main.home'))
        else:
            flash('아이디 또는 비밀번호가 잘못되었습니다.', 'danger')
    return render_template('KSC_Web_Sign_in.html')

@InUp.route('/Signup', methods=['GET', 'POST'])
def Signup():
    if request.method == 'POST':
        username = request.form.get('ID')
        password = request.form.get('PW')
        email = request.form.get('Mail')
        birth_date = request.form.get('BR')
        first_name = request.form.get('FN')
        last_name = request.form.get('LN')
        new_user = User(
            username=username,
            password=password,
            email=email,
            birth_date=birth_date,
            first_name=first_name,
            last_name=last_name
        )
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        session['first_name'] = new_user.first_name
        session['last_name'] = new_user.last_name
        return redirect(url_for('Main.welcome', first_name=first_name, last_name=last_name))
    return render_template('KSC_Web_Sign_up.html')