from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__, static_folder='static')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# 게시글 예시
posts = [
    {'id': 1, 'title': '새로운 개발 도구 소개 및 사용법 공유', 'letter': 'GitHub를 알아보아요.'},
    {'id': 2, 'title': '세계가 주목하는 최신 IT 트렌드', 'letter': '머신러닝을 통한 데이터 분석이 세계적으로 각광받고 있다.'},
    {'id': 3, 'title': '경설컴 신입생을 위한 가이드북', 'letter': '매주 월요일과 수요일에 세미나가 진행됩니다.'},
]

i=3

@app.route('/')
def door():
    return render_template('KSC_Web_Door.html')

@app.route('/h')
def home():
    return render_template('KSC_Web_Main.html')

@app.route('/i')
def intro():
    return render_template('KSC_Web_introduce.html')

@app.route('/noti')
def noti():
    return render_template('KSC_Web_Notice.html')

@app.route('/p')
def index():
    return render_template('KSC_Web_Post.html', posts=posts)

@app.route('/inup')
def inup():
    return render_template('KSC_Web_Sign_in.html')

@app.route('/post', methods=['POST'])
def post():   
    global i 
    i = i + 1
    title = request.form.get('title')
    letter = request.form.get('letter')
    posts.append({'id': i, 'title': title, 'letter': letter})
    return redirect(url_for('index'))

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    for post in posts:
        if post['id'] == post_id:
            break
    else:
        post = None
    if post:
        return render_template('post_detail.html', post=post)
    else:
        return "게시물을 찾을 수 없습니다."

@app.route('/post/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    global posts
    for post in posts:
        if post['id'] == post_id:
            posts.remove(post)
            break
    return redirect(url_for('index')) 

@app.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = None
    for p in posts:
        if p['id'] == post_id:
            post = p
            break
    if not post:
        return "게시물을 찾을 수 없습니다."
    if request.method == 'POST':
        post['title'] = request.form['title']
        post['letter'] = request.form['letter']
        return redirect(url_for('post_detail', post_id=post_id))
    return render_template('edit_post.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)