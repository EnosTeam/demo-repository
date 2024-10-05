from flask import Flask, request, render_template, redirect, url_for,flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
app = Flask(__name__, static_folder='static')
app.secret_key = 'supersecretkey12345'  # 경설컴 예시 secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)

db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    birth_date = db.Column(db.String(10), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

class Question_2(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    letter = db.Column(db.Text(), nullable = False)
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    letter = db.Column(db.Text, nullable=False)
    question = db.relationship('Question_2', backref=db.backref('answers', lazy=True))
    question_id = db.Column(db.Integer, db.ForeignKey('question_2.id'), nullable=False)
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    letter = db.Column(db.Text, nullable=False)
with app.app_context():
    db.create_all()

@app.route('/')
def door():
    return render_template('KSC_Web_Main_New.html')

@app.route('/h')
def home():
    return render_template('KSC_Web_Main_New.html')

@app.route('/i')
def intro():
    return render_template('KSC_Web_introduce.html')

@app.route('/inup', methods=['GET', 'POST'])
def inup():
    if request.method == 'POST':
        # HTML 폼에서 입력된 ID와 PW 값 가져오기
        username = request.form['ID']
        password = request.form['PW']
        
        # 데이터베이스에서 해당 유저 검색
        user = User.query.filter_by(username=username).first()
        
        # 유저가 존재하고 비밀번호가 일치하는 경우
        if user and user.password == password:
            session['user_id'] = user.id
            session['first_name'] = user.first_name
            session['last_name'] = user.last_name
            return redirect(url_for('intro'))  # 홈으로 리다이렉트
        else:
            flash('아이디 또는 비밀번호가 잘못되었습니다.', 'danger')  # 경고 메시지 띄우기

    return render_template('KSC_Web_Sign_in.html')  # 로그인 페이지 렌더링

@app.route('/Signup', methods=['GET', 'POST'])
def Signup():
    if request.method == 'POST':
        # Get form data from the request
        username = request.form.get('ID')
        password = request.form.get('PW')
        email = request.form.get('Mail')
        birth_date = request.form.get('BR')
        first_name = request.form.get('FN')
        last_name = request.form.get('LN')

        # Create a new User object
        new_user = User(
            username=username,
            password=password,  # You should hash the password for security purposes
            email=email,
            birth_date=birth_date,
            first_name=first_name,
            last_name=last_name
        )

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id
        session['first_name'] = new_user.first_name
        session['last_name'] = new_user.last_name
        
        # Redirect to the welcome page with the user's first name
        return redirect(url_for('welcome', username=first_name))
    return render_template('KSC_Web_Sign_up.html')

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
     return render_template('KSC_Web_Notice_QA_Search.html', posts=questions, keyword=keyword)

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


    
@app.route('/noti_QA/<int:question_id>/answer', methods=['GET', 'POST'])
def submit_answer(question_id):
    title = request.form.get('title')
    letter = request.form.get('letter')
    new_answer = Answer(title=title, letter=letter, question_id=question_id)
    db.session.add(new_answer)
    db.session.commit()
    return redirect(url_for('noti_QA_q_detail', question_id=question_id))

@app.route('/mypage')
def mypage():
    # Ensure user is logged in
    if 'user_id' in session:
        # Fetch user information from the database
        user = User.query.get(session['user_id'])

        return render_template('mypage.html', user=user)  # Pass user data to the template
    else:
        flash('Please log in to access your profile.', 'danger')
        return redirect(url_for('inup'))  # Redirect to login if not logged in

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_id' in session:
        user_id = session['user_id']
        # Fetch the user from the database
        user = User.query.get(user_id)

        if user:
            # Delete the user from the database
            db.session.delete(user)
            db.session.commit()

            # Clear the session after deleting the account
            session.clear()
            flash('Your account has been deleted successfully.', 'success')
            return redirect(url_for('home'))
    else:
        flash('You are not logged in.', 'danger')
        return redirect(url_for('inup'))    
    
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Clear the login session
    flash('You have successfully logged out.', 'success')
    return redirect(url_for('home'))  # Redirect to home page

@app.route('/noti')
def noti():
    return render_template('KSC_Web_Notice.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


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

@app.route('/welcome/<username>')
def welcome(username):
    return render_template('welcome.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)