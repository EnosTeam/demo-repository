from flask import Flask, request, render_template, redirect, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#공지사항 클래스
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    letter = db.Column(db.Text, nullable=False)

#질문 클래스
class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    letter = db.Column(db.Text(), nullable = False)

#답변 클래스
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete = 'CASCADE'))
    question = db.relationship('Question', backref = db.backref('answer_set'))
    letter = db.Column(db.Text(), nullable = False)

with app.app_context():
    db.create_all()
    
# door
@app.route('/')
def door():
    return render_template('KSC_Web_Main_New.html')

#대분류 기능: 메인페이지, 회원가입/로그인, 공지사항, 질문게시판
@app.route('/h')
def home():
    return render_template('KSC_Web_Main_New.html')

@app.route('/i')
def intro():
    return render_template('KSC_Web_introduce.html')

@app.route('/inup')
def inup():
    return render_template('KSC_Web_Sign_in.html')

@app.route('/Signup')
def Signup():
    return render_template('KSC_Web_Sign_up.html')

@app.route('/p')
def index():
    posts = Post.query.all()
    return render_template('KSC_Web_Post.html', posts=posts)

@app.route('/noti')
def noti():
    questions = Question.query.all()
    return render_template('KSC_Web_Notice.html', questions=questions)    


#공지사항
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



#질문 게시판

question = Blueprint('question', __name__, url_prefix='/noti')

## 질문 생성
@app.route('/question', methods=['POST'])
def question_post():
    title = request.form.get('title')
    letter = request.form.get('letter')
    question = Question(title=title, letter=letter)
    db.session.add(question)
    db.session.commit()
    return redirect(url_for('noti'))

## 질문 상세 페이지
@app.route('/question/detail/<int:question_id>/')
def question_detail(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('notice_detail.html', question=question)

## 질문 삭제
@app.route('/question/delete/<int:question_id>', methods=['POST'])
def delete_question(post_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('noti'))

## 질문 편집
@app.route('/question/edit/<int:question_id>', methods=['GET', 'POST'])
def edit_question(question_id):
    question = Question.query.get_or_404(question_id)
    if request.method == 'POST':
        question.subject = request.form['title']
        question.content = request.form['letter']
        db.session.commit()
        return redirect(url_for('question_detail', question_id=post.id))
    return render_template('edit_notice.html', question=question)    

## 답변 생성
@app.route('/question/create/<int:question_id>', methods=('POST',))
def create_answer(question_id):
    question = Question.query.get_or_404(question_id)
    letter = request.form['letter']
    new_answer = Answer(content=content, create_date=datetime.now())
    question.answer_set.append(new_answer)
    db.session.commit()
    return redirect(url_for('noti', question_id=question_id))

'''
@app.route('/question/search', methods=['GET'])
def search_question():
    keyword = request.args.get('keyword', '')
    if keyword:
        questions = Question.query.filter(or_(Question.title.contains(keyword), Question.letter.contains(keyword))).all()
    else:
        questions = Question.query.all() 
    return render_template('KSC_Web_Notice_Search.html', questions=questions, keyword=keyword)
'''

if __name__ == '__main__':
    app.run(debug=True)