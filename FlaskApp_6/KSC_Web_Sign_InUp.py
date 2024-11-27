from flask import Flask, request, render_template, redirect, url_for, flash, session, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from DataBase.KSC_Web_Sign_InUp_DB import db, User
import requests

# Kakao API configuration
KAKAO_CLIENT_ID = '10659a8b72f2ca3e2f355de00b8b23aa'
KAKAO_REDIRECT_URI = 'http://localhost:5000/kakao/callback'
KAKAO_TOKEN_URL = 'https://kauth.kakao.com/oauth/token'
KAKAO_USER_INFO_URL = 'https://kapi.kakao.com/v2/user/me'

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

@InUp.route('/kakao-login')
def kakao_login():
    # Redirect to Kakao OAuth
    kakao_auth_url = (
        f"https://kauth.kakao.com/oauth/authorize?response_type=code"
        f"&client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_REDIRECT_URI}"
    )
    return redirect(kakao_auth_url)

@InUp.route('/kakao/callback')
def kakao_callback():
    # Get authorization code from Kakao
    code = request.args.get('code')
    if not code:
        flash('Authorization failed.', 'danger')
        return redirect(url_for('InUp.inup'))

    # Exchange authorization code for access token
    data = {
        'grant_type': 'authorization_code',
        'client_id': KAKAO_CLIENT_ID,
        'redirect_uri': KAKAO_REDIRECT_URI,
        'code': code
    }
    token_response = requests.post(KAKAO_TOKEN_URL, data=data).json()
    access_token = token_response.get('access_token')

    if not access_token:
        flash('Failed to retrieve access token.', 'danger')
        return redirect(url_for('InUp.inup'))

    # Get user info from Kakao
    headers = {'Authorization': f'Bearer {access_token}'}
    user_info_response = requests.get(KAKAO_USER_INFO_URL, headers=headers).json()

    kakao_id = user_info_response.get('id')  # Unique Kakao ID
    kakao_account = user_info_response.get('kakao_account', {})
    nickname = kakao_account.get('profile', {}).get('nickname')  # Fallback to nickname

    if not nickname:
        flash('Failed to retrieve nickname from Kakao account.', 'danger')
        return redirect(url_for('InUp.inup'))

    # Check if the user exists in the database by username (nickname)
    user = User.query.filter_by(username=nickname).first()
    
    
    if not user:
        # Create a new user with the Kakao nickname and ID
       # Provide placeholder values for required fields
        placeholder_password = f'kakao_{kakao_id}_password'
        placeholder_email = f'kakao_{kakao_id}@placeholder.com'
        placeholder_birth_date = '0000-00-00'
        placeholder_first_name = 'Kakao'
        placeholder_last_name = 'User'

        # Create a new user
        user = User(
            username=nickname,
            password=placeholder_password,
            email=placeholder_email,
            birth_date=placeholder_birth_date,
            first_name=placeholder_first_name,
            last_name=placeholder_last_name,
            email_verified=True  # Kakao OAuth ensures account verification
        )
        db.session.add(user)
        db.session.commit()

    # Log the user in
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    flash('Successfully logged in with Kakao.', 'success')
    return redirect(url_for('Main.home'))