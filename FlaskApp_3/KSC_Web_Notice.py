from flask import request, render_template, redirect, url_for, Blueprint
from sqlalchemy import or_
from DataBase.KSC_Web_Notice_DB import db, Question_2, Answer

Notice = Blueprint('Notice', __name__)

@Notice.route('/noti')
def noti():
    return render_template('KSC_Web_Notice.html')

@Notice.route('/noti_QA')
def noti_QA():
    questions = Question_2.query.all()
    return render_template('KSC_Web_Notice_QA.html', questions=questions)

@Notice.route('/noti_QA_q', methods=['POST'])
def noti_QA_q():
    title = request.form.get('title')
    letter = request.form.get('letter')
    new_Question =  Question_2(title=title, letter=letter)
    db.session.add(new_Question)
    db.session.commit()
    return redirect(url_for('Notice.noti_QA'))

@Notice.route('/noti_QA/<int:question_id>/detail')
def noti_QA_q_detail(question_id):
    question = Question_2.query.get_or_404(question_id)
    answers = Answer.query.filter_by(question_id=question_id).all()
    return render_template('notice_detail.html', question=question, answers=answers)

@Notice.route('/noti_QA/search', methods=['GET'])
def search_question():
     keyword = request.args.get('keyword', '')
     if keyword:
         questions = Question_2.query.filter(or_(Question_2.title.contains(keyword), Question_2.letter.contains(keyword))).all()
     else:
         questions = Question_2.query.all() 
     return render_template('KSC_Web_Notice_QA_Search.html', questions=questions, keyword=keyword)

@Notice.route('/noti_QA/edit/<int:question_id>', methods=['GET', 'POST'])
def edit_question(question_id):
    question = Question_2.query.get_or_404(question_id)
    if request.method == 'POST':
        question.title = request.form['title']
        question.letter = request.form['letter']
        db.session.commit()
        return redirect(url_for('Notice.noti_QA_q_detail', question_id=question.id))
    return render_template('edit_question.html', question=question)

@Notice.route('/noti_QA/delete/<int:question_id>', methods=['POST'])
def delete_question(question_id):
    question = Question_2.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('Notice.noti_QA'))
    
@Notice.route('/noti_QA/<int:question_id>/answer', methods=['GET', 'POST'])
def submit_answer(question_id):
    title = request.form.get('title')
    letter = request.form.get('letter')
    new_answer = Answer(title=title, letter=letter, question_id=question_id)
    db.session.add(new_answer)
    db.session.commit()
    return redirect(url_for('Notice.noti_QA_q_detail', question_id=question_id))