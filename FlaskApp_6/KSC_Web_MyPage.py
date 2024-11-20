from flask import Flask, request, render_template, redirect, url_for, flash, session, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from DataBase.KSC_Web_Sign_InUp_DB import db, User

MyPage = Blueprint('MyPage', __name__)

@MyPage.route('/mypage')
def mypage():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('mypage.html', user=user)
    else:
        flash('Please log in to access your profile.', 'danger')
        return redirect(url_for('InUp.inup'))

@MyPage.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            session.clear()
            flash('Your account has been deleted successfully.', 'success')
            return redirect(url_for('Main.home'))
    else:
        flash('You are not logged in.', 'danger')
        return redirect(url_for('InUp.inup'))    
    
@MyPage.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have successfully logged out.', 'success')
    return redirect(url_for('Main.home'))
