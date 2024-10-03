from flask import Flask, request, render_template, redirect, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    birth_date = db.Column(db.String(10), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    letter = db.Column(db.Text, nullable=False)


@app.route('/')
def door():
    return render_template('KSC_Web_Main_New.html')

@app.route('/h')
def home():
    return render_template('KSC_Web_Main_New.html')

@app.route('/i')
def intro():
    return render_template('KSC_Web_introduce.html')

@app.route('/inup')
def inup():
    return render_template('KSC_Web_Sign_in.html')

@app.route('/Signup', methods = ['Get', 'Post'])
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
        return redirect(url_for('Signup'))
    return render_template('KSC_Web_Sign_up.html')

@app.route('/noti')
def noti():
    return render_template('KSC_Web_Notice.html')

@app.route('/p')
def index():
    posts = Post.query.all()
    return render_template('KSC_Web_Post.html', posts=posts)

@app.route('/post', methods=['POST'])
def post():
    title = request.form.get('title')
    letter = request.form.get('letter')
    new_post = Post(title=title, letter=letter)
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/post/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.letter = request.form['letter']
        db.session.commit()
        return redirect(url_for('post_detail', post_id=post.id))
    return render_template('edit_post.html', post=post)

@app.route('/search', methods=['GET'])
def search_post():
    keyword = request.args.get('keyword', '')
    if keyword:
        posts = Post.query.filter(or_(Post.title.contains(keyword), Post.letter.contains(keyword))).all()
    else:
        posts = Post.query.all() 
    return render_template('KSC_Web_Post_Search.html', posts=posts, keyword=keyword)



class Question_2(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    letter = db.Column(db.Text(), nullable = False)


@app.route('/noti_QA')
def noti_QA():
    questions = Question_2.query.all()
    return render_template('KSC_Web_Notice_QA.html', questions=questions)


@app.route('/noti_QA_q', methods=['POST'])
def noti_QA_q():
    title = request.form.get('title')
    letter = request.form.get('letter')
    new_Question =  Question_2(title=title, letter=letter)
    db.session.add(new_Question)
    db.session.commit()
    return redirect(url_for('noti_QA'))

@app.route('/noti_QA/<int:question_id>/detail')
def noti_QA_q_detail(question_id):
    question = Question_2.query.get_or_404(question_id)
    answers = Answer.query.filter_by(question_id=question_id).all()
    return render_template('notice_detail.html', question=question, answers=answers)


@app.route('/noti_QA/search', methods=['GET'])
def search_question():
     keyword = request.args.get('keyword', '')
     if keyword:
         questions = Question_2.query.filter(or_(Question_2.title.contains(keyword), Question_2.letter.contains(keyword))).all()
     else:
         questions = Question_2.query.all() 
     return render_template('KSC_Web_Notice_QA_Search.html', posts=posts, keyword=keyword)

@app.route('/noti_QA/edit/<int:question_id>', methods=['GET', 'POST'])
def edit_question(question_id):
    question = Question_2.query.get_or_404(question_id)
    if request.method == 'POST':
        question.title = request.form['title']
        question.letter = request.form['letter']
        db.session.commit()
        return redirect(url_for('noti_QA_q_detail', question_id=question.id))
    
    return render_template('edit_question.html', question=question)

@app.route('/noti_QA/delete/<int:question_id>', methods=['POST'])
def delete_question(question_id):
    question = Question_2.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('noti_QA'))


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    letter = db.Column(db.Text, nullable=False)
    question = db.relationship('Question_2', backref=db.backref('answers', lazy=True))
    question_id = db.Column(db.Integer, db.ForeignKey('question_2.id'), nullable=False)
    
@app.route('/noti_QA/<int:question_id>/answer', methods=['GET', 'POST'])
def submit_answer(question_id):
    title = request.form.get('title')
    letter = request.form.get('letter')
    new_answer = Answer(title=title, letter=letter, question_id=question_id)
    db.session.add(new_answer)
    db.session.commit()
    return redirect(url_for('noti_QA_q_detail', question_id=question_id))


if __name__ == '__main__':
    app.run(debug=True)

with app.app_context():
    db.create_all()